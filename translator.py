# Migrated from Colab

# Required packages: pysubs2, openai, tqdm, toml

import toml

# Load the configuration file
config = toml.load("config.toml")

# Accessing the data
target_language = config["translation"]["target_language"]
prompt = config["translation"]["prompt"]
temperature = config["translation"]["temperature"]
output_format = config["translation"]["output_format"]

import os
import time
from pathlib import Path
from tqdm import tqdm
import argparse

# Command line arguments
parser = argparse.ArgumentParser("AI translator for subtitles")
parser.add_argument("input_file", help="The path of input subtitle file")
args = parser.parse_args()

# Check if the input file exists
if not Path(args.input_file).exists():
    raise Exception(f"File {args.input_file} does not exist")
sub_name = args.input_file
sub_basename = Path(sub_name)

print("Input file path is basename + sub_name: ", sub_basename, sub_name)

import openai

# Cannot change the base url for openai sdk now
# Workaround is set the environment variable
os.environ["OPENAI_API_BASE"] = config["openai"]["api_base"]
# Or set it via command line: export OPENAI_API_BASE="https://api.openai.com/v1"
openai.base_url = config["openai"]["api_base"]
openai.api_key = config["openai"]["api_key"]

import pysubs2


class ChatGPTAPI:
    def __init__(self, key, language, prompt, temperature):
        self.key = key
        # self.keys = itertools.cycle(key.split(","))
        self.language = language
        self.key_len = len(key.split(","))
        self.prompt = prompt
        self.temperature = temperature

    # def rotate_key(self):
    #     openai.api_key = next(self.keys)

    def translate(self, text):
        # print(text)
        # self.rotate_key()
        client = openai.OpenAI(
            api_key=self.key,
        )

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        # english prompt here to save tokens
                        "content": f"{self.prompt}",
                    },
                    {
                        "role": "user",
                        "content": f"Original text:`{text}`. Target language: {self.language}",
                    },
                ],
                temperature=self.temperature,
            )
            t_text = completion.choices[0].message.content.encode("utf8").decode()
            total_tokens = (
                completion.usage.total_tokens
            )  # include prompt_tokens and completion_tokens
        except Exception as e:
            # TIME LIMIT for open api , pay to reduce the waiting time
            sleep_time = int(60 / self.key_len)
            time.sleep(sleep_time)
            print(e, f"will sleep  {sleep_time} seconds")
            # self.rotate_key()
            client = openai.OpenAI(
                api_key=self.key,
            )
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{self.prompt}"},
                    {
                        "role": "user",
                        "content": f"Original text:`{text}`. Target language: {self.language}",
                    },
                ],
                temperature=self.temperature,
            )
            t_text = completion.choices[0].message.content.encode("utf8").decode()
        total_tokens = completion.usage.total_tokens
        return t_text, total_tokens


class SubtitleTranslator:
    def __init__(self, sub_src, model, key, language, prompt, temperature):
        self.sub_src = sub_src
        self.translate_model = model(key, language, prompt, temperature)
        self.translations = []
        self.total_tokens = 0

    def calculate_price(self, num_tokens):
        price_per_token = 0.000002  # gpt-3.5-turbo	$0.002 / 1K tokens
        return num_tokens * price_per_token

    def translate_by_line(self):
        sub_trans = pysubs2.load(self.sub_src)
        total_lines = len(sub_trans)
        for line in tqdm(sub_trans, total=total_lines):
            line_trans, tokens_per_task = self.translate_model.translate(line.text)
            line.text += r"\N" + line_trans
            print(line_trans)
            self.translations.append(line_trans)
            self.total_tokens += tokens_per_task

        return sub_trans, self.translations, self.total_tokens


translate_model = ChatGPTAPI

assert translate_model is not None, "unsupported model"
OPENAI_API_KEY = config["openai"]["api_key"]

if not OPENAI_API_KEY:
    raise Exception("OpenAI API key not provided, please google how to obtain it")
# else:
#     OPENAI_API_KEY = openai_key

t = SubtitleTranslator(
    sub_src=sub_name,
    model=translate_model,
    key=OPENAI_API_KEY,
    language=target_language,
    prompt=prompt,
    temperature=temperature,
)

translation, _, total_token = t.translate_by_line()
total_price = t.calculate_price(total_token)
# Download ass file

if output_format == "ass":
    translation.save(sub_basename + "_translation.ass")
    print("Saved translation file:", sub_basename + "_translation.ass")
elif output_format == "srt":
    translation.save(sub_basename + "_translation.srt")
    print("Saved translation file:", sub_basename + "_translation.srt")


print("双语字幕生成完毕 All done!")
print(f"Total number of tokens used: {total_token}")
print(f"Total price (USD): ${total_price:.4f}")
