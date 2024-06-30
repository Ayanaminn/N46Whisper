# Migrated from Colab

# Required packages: pysubs2, openai, tqdm
import os
import time
from pathlib import Path
from tqdm import tqdm
import argparse

# Command line arguments
parser = argparse.ArgumentParser(
    "AI translator for subtitles",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("input_file", help="The path of input subtitle file")
parser.add_argument("--openai_key", help="The OpenAI API key", required=True)
parser.add_argument("--openai_model", default="gpt-3.5-turbo", help="The OpenAI model")
parser.add_argument(
    "--target_language", default="zh_hans", help="The target language to translate to"
)
parser.add_argument(
    "--prompt",
    default="""
You are a language expert.
Your task is to translate the input subtitle text, sentence by sentence, into the user specified target language.
However, please utilize the context to improve the accuracy and quality of translation.
Please be aware that the input text could contain typos and grammar mistakes, utilize the context to correct the translation.
Please return only translated content and do not include the origin text.
Please do not use any punctuation around the returned text.
Please do not translate people's name and leave it as original language.
""",
    help="The prompt",
)
parser.add_argument("--temperature", default=0.6, help="The temperature")
parser.add_argument(
    "--output-format", default="ass", choices=["srt", "ass"], help="The output format"
)
args = parser.parse_args()


# Check if the input file exists
if not Path(args.input_file).exists():
    raise Exception(f"File {args.input_file} does not exist")
sub_name = args.input_file
sub_filename = (
    Path(sub_name)
    .with_stem(Path(sub_name).stem + "_translation")
    .with_suffix("." + args.output_format)
)

print("Input file path is: ", sub_name)

# Cannot change the base url for openai sdk now
# Workaround is set the environment variable
# os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1"
# Or set it via command line: export OPENAI_BASE_URL="https://api.openai.com/v1"

import openai

# openai.base_url = config["openai"]["api_base"]
openai.api_key = args.openai_key

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
                model=args.openai_model,
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
OPENAI_API_KEY = args.openai_key

if not OPENAI_API_KEY:
    raise Exception("OpenAI API key not provided, please google how to obtain it")
# else:
#     OPENAI_API_KEY = openai_key

t = SubtitleTranslator(
    sub_src=sub_name,
    model=translate_model,
    key=OPENAI_API_KEY,
    language=args.target_language,
    prompt=args.prompt,
    temperature=args.temperature,
)

translation, _, total_token = t.translate_by_line()
total_price = t.calculate_price(total_token)
# Download ass file

translation.save(sub_filename)
print("Saved translation file:", sub_filename)


print("双语字幕生成完毕 All done!")
print(f"Total number of tokens used: {total_token}")
print(f"Total price (USD): ${total_price:.4f}")
