# -*- coding: utf-8 -*- #
# https://mp.weixin.qq.com/s/KDmR43GDPog-nhrNL1cHZQ

import os
import sys
import re


mp3 = sys.argv[1]
eng = len(sys.argv) > 2 and sys.argv[2].startswith("e")

# 1. mp3 -> VTT
vtt = mp3.replace(".mp3", ".vtt")

if not os.path.exists(vtt) or input("vtt已存在，覆盖(y/[n])?").startswith("y"):
    print("请稍候...")

    # 如果GPU够好，用 large-v3-turbo 效果更好
    import whisper
    model = whisper.load_model("base.en" if eng else "base")
    result = model.transcribe(
        mp3,
        word_timestamps=True,
        language="en" if eng else "zh",
        initial_prompt="" if eng else "以下是普通话"
    )

    with open(vtt, "w") as f:
        f.write("WEBVTT\n\n")
        for segment in result["segments"]:
            f.write(f"{segment['start']} --> {segment['end']}\n")
            f.write(f"{segment['text']}\n\n")

    print("vtt生成完毕，请添加分割标记'**'.")


# 2. VTT -> cue
if input("vtt是否已经添加好分割标记'**' (y/[n])?").startswith("y"):

    cue = mp3.replace(".mp3", ".cue")

    segments = []
    with open(vtt, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # 跳过VTT头部（通常第一行是"WEBVTT"）
    start_idx = 0
    if lines and lines[0].upper() == "WEBVTT":
        start_idx = 1

    # 按“时间戳行+文本行”解析（VTT格式特点）
    for i in range(start_idx, len(lines), 2):
        time_line = lines[i]
        if " --> " not in time_line:
            continue  # 跳过非时间戳行

        # 提取浮点型起始时间（如 "1.234 --> 3.456" → 取1.234）
        start_seconds = float(time_line.split(" --> ")[0])

        text = lines[i + 1] if (i + 1 < len(lines)) else ""
        if text.startswith("**"):
            segments.append(start_seconds)

    if not segments:
        print("未找到任何含“**”的标记，无法生成CUE")
        exit(1)

    print(f'共有 {len(segments)} 段. ')

    # 为了输出的切片文件名和毛毛虫贴纸直接对应上
    ttl = ''
    tag = 1
    m = input('封面贴纸文件名 (如"RECP1201"): ')
    m = re.match(r'^([^\d]*)(\d+)$', m)
    if m:
        ttl = m.group(1)
        tag = int(m.group(2))

    # 生成CUE文件（转换时间格式）
    with open(cue, "w", encoding="utf-8") as f:
        f.write(f'FILE "{os.path.basename(mp3)}" MP3\n')

        for track, total_seconds in enumerate(segments, 1):
            # 转换浮点秒数 → 分:秒:帧（1秒=75帧）
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            milliseconds = int((total_seconds - int(total_seconds)) * 1000)
            frames = int(milliseconds * 75 / 1000)  # 毫秒转帧（四舍五入）

            f.write(f'  TRACK {track:02d} AUDIO\n')
            f.write(f'    TITLE "{ttl}{tag + track} AUDIO"\n')
            f.write(f'    INDEX 01 {minutes:02d}:{seconds:02d}:{frames:02d}\n')

    print("cue生成完毕.")
