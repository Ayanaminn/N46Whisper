# N46Whisper

Language : English | [简体中文](./README_CN.md) 

N46Whisper is a Google Colab notebook application that developed for streamlined video subtitle file generation to improve productivity of Nogizaka46 (and Sakamichi groups) subbers.

The notebook is based on [faster-whisper](https://github.com/guillaumekln/faster-whisper), a reimplementation of OpenAI's [Whisper](https://github.com/openai/whisper) , a general-prupose speech recognition model.
This implementation is up to 4 times faster than original Whisper for the same accuracy while using less memory.

The output file will be in Advanced SubStation Alpha(ass) format with built-in style of selected sub group so it can be directly imported into [Aegisub](https://github.com/Aegisub/Aegisub) for subsequent editing.

## What's Latest：

This projuct can only be maintained and updated irregularly due to perosonal busyness. Thank you.

2024.1.31:
* [N46WhisperLite](https://colab.research.google.com/github/Ayanaminn/N46Whisper/blob/dev/N46WhisperLite.ipynb) is available for daily tasks that do not need advanced settings.

2023.12.4:
* Add support for v3 model based on faster-whisper

2023.11.7:
* Enable users to load lastest Whisper V3 model.
* Enable customerize beam size parameter.


## How to use
* [Click here](https://colab.research.google.com/github/Ayanaminn/N46Whisper/blob/main/N46Whisper.ipynb) to open the notebook in Google Colab.
* Upload file and follow the instruction to run the notebook.
* The subtitle file will be automatically downloaded once done.

## AI translation
The notebook now allow users to translate transcribed subtitle text line by line using AT translation tools.

Users can also upload local subtitle files or select files from google drive for translation.

Currently, it supports `chatGPT` translation. 

The translated text will be append in the same line after the original text and sepearted by `/N`, such that a new bilingual subtitle file is generated.

For instance: 

![QQ截图20230312155700](https://user-images.githubusercontent.com/49441654/224525469-18a43cbc-33b9-4b2f-b7ca-7ae0c1865b17.png)

An example of bilingual subtitle:

![QQ截图20230312160015](https://user-images.githubusercontent.com/49441654/224525526-51e2123c-6e1c-427c-8d67-9ccd4a7e6630.png)

To use the AI translation, users must use their own OpenAI API Key. To obtain a free Key, go to https://platform.openai.com/account/api-keys

Please note there will be limitaions on usage for free keys, choose a paid plan to speed up at your own cost.

## Split lines
Users can choose to split text in a single line by space.The child lines will have same time stamp with the parent line, respectively.

For instance, for a line contains multiple long sentences:
>Dialogue: 0,0:01:00.52,0:01:17.52,default,,0,0,0,,Birthday Liveについて話そうかなと思います よろしくお願いします

After split:
>Dialogue: 0,0:01:00.52,0:01:17.52,default,,0,0,0,,Birthday Liveについて話そうかなと思います(adjust_required)

>Dialogue: 0,0:01:00.52,0:01:17.52,default,,0,0,0,,ろしくお願いします(adjust_required)

## Update history：

2023.4.30:
* Refine the translation prompt.
* Allow user to custom prompt and temperature for translation.
* Display the token used and total cost for the translation task.

2023.4.15:
* Reimplement Whsiper based on faster-whisper to improve efficiency
* Enable vad filter that integrated within faster-whisper to improve transcribe accuracy
2023.4.10:
* Support for select/upload multiple files to batch process.

2023.4.1:
* Update workflow, use pysubs2 library instead of Whisper WriteSRT class for sub file manipulation.
* Support upload srt or ass file to use AI translation function independently, support display translation progress.
* Update documents and other minor fixes.

2023.3.15:
* Add functions to split multiple words/sententces in one line.
* Update documents and other minor fixes.

2023.3.12:
* Add chatGPT translation and bilingual subtitle file generation features.
* Update documents and other minor fixes.

2023.01.26：
* Update scripts to reflect recent changes in Whisper.

2022.12.31：
* Allow user to select files directly from mounted google drive.
* Other minor fixes.

## Support
The application could significantly reduce the labour and time costs of sub-groups or individual subbers. However, despite its impressive performance, the Whisper model and the application itself are not without limitations.Please read the orgininal documents and Discussions to learn more about the usage of Whisper and the common issues.

However, if you have any throughts, requests or questions that directly related to making subtitiles for Sakamichi group girls, please feel free to post here or [contact me](mailto:admin@ikedateresa.cc)

## License
The code is released under the MIT license. See [License](./LICENSE.md) for details.

