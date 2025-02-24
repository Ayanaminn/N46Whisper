# -*- coding: utf-8 -*-
#
# python-srt2ass: https://github.com/ewwink/python-srt2ass
# by: ewwink
# modified by:  一堂宁宁 Lenshyuu227

import sys
import os
import regex as re
import codecs


def fileopen(input_file):
    # use correct codec to encode the input file
    encodings = ["utf-32", "utf-16", "utf-8", "cp1252", "gb2312", "gbk", "big5"]
    srt_src = ''
    for enc in encodings:
        try:
            with codecs.open(input_file, mode="r", encoding=enc) as fd:
                # return an instance of StreamReaderWriter
                srt_src = fd.read()
                break
        except:
            # print enc + ' failed'
            continue
    return [srt_src, enc]


def srt2ass(input_file,sub_style, is_split, split_method):
    if '.ass' in input_file:
        return input_file

    if not os.path.isfile(input_file):
        print(input_file + ' not exist')
        return

    src = fileopen(input_file)
    srt_content = src[0]
    # encoding = src[1] # Will not encode so do not need to pass codec para
    src = ''
    utf8bom = ''

    if u'\ufeff' in srt_content:
        srt_content = srt_content.replace(u'\ufeff', '')
        utf8bom = u'\ufeff'
    
    srt_content = srt_content.replace("\r", "")
    lines = [x.strip() for x in srt_content.split("\n") if x.strip()]
    subLines = ''
    dlgLines = '' # dialogue line
    lineCount = 0
    output_file = '.'.join(input_file.split('.')[:-1])
    output_file += '.ass'

    for ln in range(len(lines)):
        line = lines[ln]
        if line.isdigit() and re.match('-?\d\d:\d\d:\d\d', lines[(ln+1)]):
            if dlgLines:
                subLines += dlgLines + "\n"
            dlgLines = ''
            lineCount = 0
            continue
        else:
            if re.match('-?\d\d:\d\d:\d\d', line):
                line = line.replace('-0', '0')
                if sub_style =='default':
                    dlgLines += 'Dialogue: 0,' + line + ',default,,0,0,0,,'
                elif sub_style =='ikedaCN':
                    dlgLines += 'Dialogue: 0,' + line + ',池田字幕1080p,,0,0,0,,'
                elif sub_style == 'sugawaraCN':
                    dlgLines += 'Dialogue: 0,' + line + ',中字 1080P,,0,0,0,,'
                elif sub_style == 'kaedeCN':
                    dlgLines += 'Dialogue: 0,' + line + ',den SR红色,,0,0,0,,'
                elif sub_style == 'taniguchiCN':
                    dlgLines += 'Dialogue: 0,' + line + ',正文_1080P,,0,0,0,,'
                elif sub_style == 'asukaCN':
                    dlgLines += 'Dialogue: 0,' + line + ',DEFAULT1,,0,0,0,,'
            else:
                if lineCount < 2:
                    dlg_string = line
                    if is_split == "Yes" and split_method == 'Modest':
                        # do not split if space proceed and followed by non-ASC-II characters
                        # do not split if space followed by word that less than 5 characters
                        split_string = re.sub(r'(?<=[^\x00-\x7F])\s+(?=[^\x00-\x7F])(?=\w{5})', r'|', dlg_string)
                        # print(split_string)
                        if len(split_string.split('|')) > 1:
                            dlgLines += (split_string.replace('|', "(adjust_required)\n" + dlgLines)) + "(adjust_required)"
                        else:
                            dlgLines += line
                    elif is_split == "Yes" and split_method == 'Aggressive':
                        # do not split if space proceed and followed by non-ASC-II characters
                        # split at all the rest spaces
                        split_string = re.sub(r'(?<=[^\x00-\x7F])\s+(?=[^\x00-\x7F])', r'|', dlg_string)
                        if len(split_string.split('|')) > 1:
                            dlgLines += (split_string.replace('|',"(adjust_required)\n" + dlgLines)) + "(adjust_required)"
                        else:
                            dlgLines += line
                    elif is_split == "Yes" and split_method == 'Punctuation':
                        split_string = dlg_string.replace('. ', '|')
                        # print(split_string)
                        if len(split_string.split('|')) > 1:
                            dlgLines += (split_string.replace('|',".\n" + dlgLines))
                        else:
                            dlgLines += line
                    else:
                        dlgLines += line
                else:
                    dlgLines += "\n" + line
            lineCount += 1
        ln += 1


    subLines += dlgLines + "\n"

    subLines = re.sub(r'\d(\d:\d{2}:\d{2}),(\d{2})\d', '\\1.\\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)
    # replace style
    # subLines = re.sub(r'<([ubi])>', "{\\\\\g<1>1}", subLines)
    # subLines = re.sub(r'</([ubi])>', "{\\\\\g<1>0}", subLines)
    # subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', "{\\\\c&H\\3\\2\\1&}", subLines)
    # subLines = re.sub(r'</font>', "", subLines)

    if sub_style == 'default':
        head_name = 'head_str_default'
    elif sub_style == 'ikedaCN':
        head_name = 'head_str_ikeda'
    elif sub_style == 'sugawaraCN':
        head_name = 'head_str_sugawara'
    elif sub_style == 'kaedeCN':
        head_name = 'head_str_kaede'
    elif sub_style == "taniguchiCN":
        head_name = 'head_str_taniguchi'
    elif sub_style == 'asukaCN':
        head_name = 'head_str_asuka'

    head_str = STYLE_DICT.get(head_name)
    output_str = utf8bom + head_str + '\n' + subLines
    # encode again for head string
    output_str = output_str.encode('utf8')

    with open(output_file, 'wb') as output:
        output.write(output_str)

    output_file = output_file.replace('\\', '\\\\')
    output_file = output_file.replace('/', '//')
    return output_file


# if len(sys.argv) > 1:
#     for name in sys.argv[1:]:
#         srt2ass(name,sub_style=)


STYLE_DICT = {
    'head_str_default':'''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: default,Meiryo,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00050506,-1,0,0,0,100,100,5,0,1,3.5,0,2,135,135,10,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text''',
    'head_str_ikeda': '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
Style: 池田字幕1080p,思源黑体,71,&H00FFFFFF,&H000000FF,&H00008A11,&H00000000,-1,0,0,0,100,100,1.49999,0,1,1.99999,1,2,8,8,5,1
Style: 池田字幕1080p - 不透明背景,思源黑体,71,&H00FFFFFF,&H000000FF,&H64202021,&H00000000,-1,0,0,0,100,100,1.49999,0,3,1.99999,0,2,8,8,5,1
Style: staff1080p,思源黑体,55,&H00FFFFFF,&H00FFFFFF,&H34000000,&H00000000,-1,0,0,0,100,100,3,0,1,2.5,0,7,16,13,4,1
Style: 注释1080p,思源宋体 CN,55,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,8,10,10,10,1
Style: 多美左上遮罩,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,1,8,8,11,1
Style: 多美紫色遮罩,Arial,48,&H00F05384,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,1,8,8,11,1
Style: 多美紫色屏字,仓耳渔阳体 W03,86,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,8,8,11,1
Style: 多美右上屏字,方正兰亭圆_GBK_细,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,94,100,6,0,1,0,3,9,8,45,100,1
Style: 屏字-黑,汉仪正圆-55S,71,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,8,8,11,1
Style: 免责,汉仪正圆-85W,56,&H00AE577B,&H000000FF,&H00FFFFFF,&H9D000000,0,0,0,0,100,100,1,0,1,1.5,2,8,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.30,0:00:03.00,staff1080p,,0,0,0,,{'''+r'''\fad(150,300)}特蕾纱熊猫观察会'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：
Dialogue: 0,0:00:00.30,0:00:50.30,免责,,0,0,0,Banner;7;0;50,片源来自互联网，仅作内部学习交流之用，严禁用于商业用途，严禁二次上传、修改，严禁转载。任何自行传播导致的法律问题均与字幕组无关。DO NOT distribute the content on the internet.''',
'head_str_sugawara':'''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: 中字 1080P,思源黑体 CN Medium,90,&H00FFFFFF,&H00FFFFFF,&H008F51CA,&H00A860F2,-1,0,0,0,100,100,5,0,1,3.5,0,2,135,135,10,1
Style: staff 1080P,思源宋体 CN Medium,70,&H00FFFFFF,&H000000FF,&H008F51CA,&H00000000,0,0,0,0,100,100,0,0,1,4,2,7,10,10,10,1
Style: 标注 1080P,思源黑体 CN Medium,70,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,3,1.5,8,0,0,15,1
Style: 中字 720P,思源黑体 CN Medium,60,&H00FFFFFF,&H00FFFFFF,&H008F51CA,&H00A860F2,-1,0,0,0,100,100,5,0,1,3,0,2,135,135,10,1
Style: staff 720P,思源宋体 CN Medium,50,&H00FFFFFF,&H000000FF,&H008F51CA,&H00000000,0,0,0,0,100,100,0,0,1,3,2,7,10,10,10,1
Style: 标注 720P,思源黑体 CN Medium,50,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,3,1.5,8,0,0,15,1
Style: staff msg,思源宋体 CN Medium,25,&H00FFFFFF,&H000000FF,&H008F51CA,&H00000000,0,0,0,0,100,100,0,0,1,4,2,7,10,10,10,1
Style: 中字 msg,思源黑体 CN Medium,25,&H00FFFFFF,&H00FFFFFF,&H008F51CA,&H00A860F2,-1,0,0,0,100,100,5,0,1,4,0,2,135,135,10,1
Style: 标注 msg,思源黑体 CN Medium,25,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,3,1.5,8,0,0,15,1
Style: 歌词日语 1080P,Swei Spring Sugar CJKtc,60,&H00FFFFFF,&H000000FF,&H009B46A5,&H5A9B46A5,0,0,0,0,100,100,0,0,1,2,0,2,10,10,30,1
Style: 歌词中文 1080P,Swei Spring Sugar CJKtc,90,&H00FFFFFF,&H000000FF,&H009B46A5,&H5F9B46A5,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,100,1
Style: 歌词中文 720P,Swei Spring Sugar CJKtc,60,&H00FFFFFF,&H000000FF,&H009B46A5,&H5F9B46A5,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,70,1
Style: 歌词日语 720P,Swei Spring Sugar CJKtc,40,&H00FFFFFF,&H000000FF,&H009B46A5,&H5A9B46A5,0,0,0,0,100,100,0,0,1,1,0,2,10,10,15,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.24,staff 1080P,,0,0,0,,{'''+r'''\fad(1200,50)\pos(15.2,0.4)}菅原咲月字幕组'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：''',
    'head_str_kaede':'''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: staff,微软雅黑,60,&H00FFFFFF,&H00923782,&H0076137B,&H00540D67,-1,0,0,0,100,100,0,0,1,3,0,7,15,15,15,1
Style: den SR红色,微软雅黑,70,&H0AFFFFFF,&H004B4B9E,&H322828E0,&H640A0A72,-1,0,0,0,100,100,0,0,1,3,0,2,15,15,70,1
Style: 注释,微软雅黑,68,&H00FFFFFF,&H000000FF,&H3D000000,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,4.5,0,8,23,23,23,1
Style: 红色,微软雅黑,75,&H00FFFFFF,&H000000FF,&H004243CB,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,2,15,15,15,1
Style: den - 中文歌词,微软雅黑,70,&H0AFFFFFF,&H004B4B9E,&H322828E0,&H640A0A72,-1,0,0,0,100,100,0,0,1,3,0,2,15,15,70,1
Style: den - 日文歌词,微软雅黑,50,&H0AFFFFFF,&H00F9F9F9,&H32000001,&H640A0A72,-1,0,0,0,100,100,0,0,1,1,0,2,15,15,9,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,staff,,0,0,0,,{'''+r'''\fad(300,300)}「三番目の楓」'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：''',
'head_str_taniguchi':'''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; The script is generated by N46Whisper
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
Style: 正文_1080P,思源黑体 CN Bold,75,&H00FFFFFF,&H000000FF,&H0077234B,&HA00000FF,-1,0,0,0,100,100,3,0,1,3,2,2,10,10,15,1
Style: staff_1080P,思源宋体 CN Heavy,60,&H00FFFFFF,&H000000FF,&H0077234B,&HA00000FF,-1,0,0,0,100,100,2,0,1,2,1,7,30,10,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:10.00,staff_1080P,,0,0,0,,{'''+r'''\fad(300,1000)}泪痣愛季応援団 '''+r'''\N源:'''+r'''\N制作:
Dialogue: 0,0:00:08.95,0:03:29.40,staff_1080P,,0,0,0,,{'''+r'''\fad(1000,1000)'''+r'''\pos(30,30)'''+r'''\bord0'''+r'''\shad0'''+r'''\c&HFFFFFF&'''+r'''\1a&H3C&}泪痣愛季応援団
Dialogue: 0,0:00:00.00,0:00:05.00,正文_1080P,,0,0,0,,谷口爱季字幕组''',
'head_str_asuka':'''[Script Info]
; The script is generated by N46Whisper
; http://www.aegisub.org/
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[Aegisub Project Garbage]

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
Style: DEFAULT1,微软雅黑,65,&H00FFFFFF,&HF08B581A,&H007E672E,&H0084561E,-1,0,0,0,100,100,0,0,1,2,1,2,20,20,5,1
Style: STAFF,Microsoft YaHei,50,&H00FFFFFF,&HF08B581A,&H007E672E,&HF084561E,-1,0,0,0,100,100,0,0,1,2.5,3,7,30,30,3,134
Style: 名单1,方正粗倩_GBK,45,&H00E7D793,&H00E9C116,&H004C3F00,&H0016161D,-1,0,0,0,100,100,0,0,1,3,2,2,10,10,10,1
Style: 名单2,方正粗黑简体,45,&H00FAF9EC,&H00493F15,&H008A4D1F,&H000A0A0B,-1,0,0,0,100,100,0,0,1,3,1.5,2,10,10,10,1
Style: 中文歌词,方正粗黑简体,50,&H00FFFFFF,&HF0000000,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,1.5,2,2,10,10,4,134
Style: 日文歌词,方正粗黑简体,40,&H00FFFFFF,&HF0000000,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,1.5,2,2,10,10,10,134
Style: 屏幕字/注释,微软雅黑,50,&H00FFFFFF,&HF0000000,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,1.5,2,2,10,10,10,134
Style: purple1,文鼎特圆简,26,&H00670067,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,4.6,0,2,10,10,10,1
Style: 鸟,微软雅黑,35,&H00FFFFFF,&HF08B581A,&H00F3B70F,&H0084561E,-1,0,0,0,100,100,0,0,1,2,1,2,100,20,465,1
Style: 哈利,微软雅黑,35,&H00FFFFFF,&HF08B581A,&H00445FE1,&H00445FE1,-1,0,0,0,100,100,0,0,1,2,1,2,0,150,220,1
Style: 期数,Berlin Sans FB,25,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,9,10,10,0,1
Style: HamAsuka-屏幕字,方正卡通_GBK,50,&H00FFFFFF,&H000000FF,&H00D08C27,&H00010102,-1,0,0,0,100,100,0,0,1,3.5,3,2,900,10,170,1
Style: HamAsuka-屏幕字 小黑,方正粗黑宋简体,65,&H00000000,&H000000FF,&H00FFFFFF,&H00010102,0,0,0,0,100,100,0,0,1,0,0,2,10,10,170,1
Style: HamAsuka-屏幕字 蓝底,微软雅黑,80,&H00FFFFFF,&H000000FF,&H00A21C14,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,4,0,2,10,10,10,1
Style: HamAsuka-屏幕字 标题,微软雅黑,90,&H00303030,&H0006C6F6,&H00FFFFFF,&H00010102,-1,0,0,0,100,100,0,0,1,0,0,2,10,10,10,1
Style: HamAsuka-屏幕字 问题 白底,微软雅黑,90,&H002C2C2C,&H00B77B1B,&H00FFFFFF,&H00010102,-1,0,0,0,100,100,0,0,3,5,0,2,10,10,10,1
Style: HamAsuka 歌词,微软雅黑,70,&H00FFFFFF,&H00000000,&H00000000,&H00010102,-1,0,0,0,100,100,0,0,1,0,0,2,10,10,10,1
Style: HamAsuka 小窗,微软雅黑,50,&H00FFFFFF,&HF0000000,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,1.5,2,9,10,10,300,134
Style: HamAsuka-屏幕字 标题 蓝底,微软雅黑,90,&H00F9F8FB,&H000000FF,&H00AC9769,&H00000000,-1,0,0,0,100,100,0,0,3,5,0,2,10,10,10,1
Style: HamAsuka-屏幕字 标题  黑字,微软雅黑,80,&H00292B2C,&H000000FF,&H00FFFFFF,&H00000000,-1,0,0,0,100,100,0,0,3,5,0,2,10,10,10,1
Style: 毕业曲MV 中文歌词,思源黑体 CN,76,&H0AFFFFFF,&H000000FF,&H0F000000,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,75,1
Style: 毕业曲MV 日文歌词,思源黑体 CN,58,&H0AFFFFFF,&H000000FF,&H0F000000,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,15,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,'''
    # ADD MORE

}


# if __name__ == "__main__":
#     srt2ass('sub_split_test.srt','sugawaraCN','No','Aggressive')