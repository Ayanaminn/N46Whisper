# N46Whisper

Language : [English](./README.md)  | 简体中文

N46Whisper 是基于 Google Colab 的应用。开发初衷旨在提高乃木坂46（以及坂道系）字幕组的工作效率。但本应用亦适于所有日语视频的字幕制作。

此应用基于AI语音识别模型 [Whisper](https://github.com/openai/whisper)的优化部署 [faster-whisper](https://github.com/guillaumekln/faster-whisper).

应用输出文件为ass或srt格式，内置指定字幕组的字幕格式，可直接导入 [Aegisub](https://github.com/Aegisub/Aegisub) 进行后续翻译及时间轴校正。

## 最近更新:
由于个人比较忙，此项目仍然只能不定期进行维护和更新，感谢各位。


2023.11.7:
* 可以使用最新的Whisper V3 model。
* 可以自定义beam size参数。

2023.4.30:
* 优化提示词
* 允许用户使用个人提示词并调节Temperature参数
* 显示翻译任务消费统计

2023.4.15:
* 使用faster-whisper模型重新部署以提高效率，节省资源
* 提供faster-whisper集成的vad filter选项以提高转录精度


## 如何使用
* [点击这里](https://colab.research.google.com/github/Ayanaminn/N46Whisper/blob/main/N46Whisper.ipynb) 在Google Colab中打开应用.
* 上传要识别的文件并运行应用
* 识别完成后ass文件会自动下载到本地.

## AI翻译
应用现在可以使用AI翻译工具对转录的文本进行逐行翻译。

用户也可以单独上传srt或ass文件来使用翻译模块。

目前支持`chatGPT` 的翻译。

翻译后的文本将于原文合并在一行，以 `/N`分割，生成双语对照字幕。

例如: 

![QQ截图20230312155700](https://user-images.githubusercontent.com/49441654/224525469-18a43cbc-33b9-4b2f-b7ca-7ae0c1865b17.png)

双语字幕效果为:

![QQ截图20230312160015](https://user-images.githubusercontent.com/49441654/224525526-51e2123c-6e1c-427c-8d67-9ccd4a7e6630.png)

用户需要自己的OpenAI API Key来使用翻译功能. 要生成免费的Key，进入自己账户设定 https://platform.openai.com/account/api-keys

请注意免费Key有用量限制，翻译速度会较慢。用户可以自己选择付费方案。

## 自动分行
当一行中有若干句话时，用户可选择按空格分割成多行。分割后的若干行均临时采用原行相同的时间戳，且添加了adjust_required标记提示调整时间戳避免叠轴。

普通分割只有在单（词）句字符长度大于5时才进行分割：
分割前：

![No](https://user-images.githubusercontent.com/49441654/225230578-2977511d-324f-463f-b783-fa9251df8e9f.PNG)

分割后：

![Modest](https://user-images.githubusercontent.com/49441654/225230645-efe8b26a-3392-4234-ad3f-f9b8d4e95d10.PNG)

可以看到，尤其以第7行为例，短句和语气词被保留，只有长句被分割。字符长度5为默认值，一般来说日语大部分短句和语气词都可以过滤掉。

全面分割则是对任何空格都另起一行，分割后：

![Aggre](https://user-images.githubusercontent.com/49441654/225231063-3e60561b-a821-4c61-8c8e-4ce53e6c1a12.PNG)


此外可以看到，在两种情况下英文单字都不会被分割。

## 更新日志
2023.4.10:
* 支持选择/上传多个文件以批量转录。

2023.4.1:
* 更新工作流程，使用pysubs2库代替Whisper自带的WriteSRT类处理字幕文件格式。
* 支持单独上传srt或ass文件来使用翻译功能，支持显示翻译进度条。
* 修订文档以及其它一些优化。

2023.3.15:
* 添加根据空格自动分行功能。
* 修订文档以及其它一些优化。

2023.3.12:
* 添加chatGPT翻译并生成双语字幕功能.
* 修订文档以及其它一些优化。

2023.01.26：
* 更新脚本以反映近期Whisper的更新。

2022.12.31：
* 添加了允许用户从挂载的谷歌云盘中直接选择要转换的文件的功能。本地上传文件的选项仍然保留。
* 修订文档以及其它一些优化。

## 支持
根据我们使用若干视频的测试结果，输出**原文字幕**的识别准确率可以达到90%以上，这无疑能极大地节省听译及打轴所需的人手和时间。但本应用的目标并非生产完美的字幕文件， 而旨在于搭建并提供一个简单且自动化的使用平台以节省生产成品字幕的时间和精力。Whisper模型有其本身的应用场景限制，例如视频中出现明显地背景音，长时间空白和多人对话，都可能影响识别准确度。AI翻译的质量也还不能尽如人意。您可以阅读官方文档及讨论区来进一步了解如何使用Whisper以及常见问题。

但如果您有针对应用本身或字幕制作相关的建议、需求、或问题，欢迎随时提出issue或者[联系我们](mailto:admin@ikedateresa.cc)
