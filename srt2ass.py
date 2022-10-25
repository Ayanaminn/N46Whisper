# -*- coding: utf-8 -*-
#
# python-srt2ass: https://github.com/ewwink/python-srt2ass
# by: ewwink
# modified by: 一堂宁宁

import sys
import os
import re
import codecs


def fileopen(input_file):
    # use correct codec to encode the input file
    encodings = ["utf-32", "utf-16", "utf-8", "cp1252", "gb2312", "gbk", "big5"]
    tmp = ''
    for enc in encodings:
        try:
            with codecs.open(input_file, mode="r", encoding=enc) as fd:
                # return an instance of StreamReaderWriter
                tmp = fd.read()
                break
        except:
            # print enc + ' failed'
            continue
    return [tmp, enc]


def srt2ass(input_file):
    if '.ass' in input_file:
        return input_file

    if not os.path.isfile(input_file):
        print(input_file + ' not exist')
        return

    src = fileopen(input_file)
    tmp = src[0]
    # encoding = src[1] # Will not encode so do not need to pass codec para
    src = ''
    utf8bom = ''

    if u'\ufeff' in tmp:
        tmp = tmp.replace(u'\ufeff', '')
        utf8bom = u'\ufeff'
    
    tmp = tmp.replace("\r", "")
    lines = [x.strip() for x in tmp.split("\n") if x.strip()]
    subLines = ''
    tmpLines = ''
    lineCount = 0
    output_file = '.'.join(input_file.split('.')[:-1])
    output_file += '.ass'

    for ln in range(len(lines)):
        line = lines[ln]
        if line.isdigit() and re.match('-?\d\d:\d\d:\d\d', lines[(ln+1)]):
            if tmpLines:
                subLines += tmpLines + "\n"
            tmpLines = ''
            lineCount = 0
            continue
        else:
            if re.match('-?\d\d:\d\d:\d\d', line):
                line = line.replace('-0', '0')
                tmpLines += 'Dialogue: 0,' + line + ',池田字幕1080p,,0,0,0,,'
            else:
                if lineCount < 2:
                    tmpLines += line
                else:
                    tmpLines += "\n" + line
            lineCount += 1
        ln += 1


    subLines += tmpLines + "\n"

    subLines = re.sub(r'\d(\d:\d{2}:\d{2}),(\d{2})\d', '\\1.\\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)
    # replace style
    # subLines = re.sub(r'<([ubi])>', "{\\\\\g<1>1}", subLines)
    # subLines = re.sub(r'</([ubi])>', "{\\\\\g<1>0}", subLines)
    # subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', "{\\\\c&H\\3\\2\\1&}", subLines)
    # subLines = re.sub(r'</font>', "", subLines)

    head_str = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
; 池田瑛纱中国应援会版权所有
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubStyle,Arial,20,&H0300FFFF,&H00FFFFFF,&H00000000,&H02000000,-1,0,0,0,100,100,0,0,3,2,0,2,10,10,10,1
Style: 池田字幕1080p,思源黑体,70,&H00FFFFFF,&H000000FF,&H00008A11,&H00000000,-1,0,0,0,100,100,1.5,0,1,2,1,2,8,8,5,1
Style: staff1080p,思源黑体,55,&H00FFFFFF,&H00FFFFFF,&H34000000,&H00000000,-1,0,0,0,100,100,2.25,0,1,2.5,0,7,12,10,4,1
Style: 注释1080p,思源宋体,55,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,8,8,8,10,1
Style: 歌词1080p,方正兰亭圆_GBK,60,&H00FCFDFD,&H000000FF,&H00000000,&H00030202,-1,0,0,0,100,100,0,0,1,1.5,1.5,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.30,0:00:03.00,staff1080p,,0,0,0,,特蕾纱熊猫观察会'''+r'''\N片源：'''+r'''\N翻译：'''+r'''\N时间：'''+r'''\N校压：'''

    output_str = utf8bom + head_str + '\n' + subLines
    # encode again for head string
    output_str = output_str.encode('utf8')

    with open(output_file, 'wb') as output:
        output.write(output_str)

    output_file = output_file.replace('\\', '\\\\')
    output_file = output_file.replace('/', '//')
    return output_file


if len(sys.argv) > 1:
    for name in sys.argv[1:]:
        srt2ass(name)

