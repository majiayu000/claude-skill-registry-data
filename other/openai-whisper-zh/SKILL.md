---
name: openai-whisper-zh
description: 使用 Whisper CLI 进行本地语音转文字（无需 API 密钥）。
homepage: https://openai.com/research/whisper
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "bins": ["whisper"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "openai-whisper",
              "bins": ["whisper"],
              "label": "安装 OpenAI Whisper (brew)",
            },
          ],
      },
  }
---

# Whisper (CLI)

使用 `whisper` 在本地转录音频。

快速开始

- `whisper /path/audio.mp3 --model medium --output_format txt --output_dir .`
- `whisper /path/audio.m4a --task translate --output_format srt`

注意事项

- 模型会在首次运行时下载到 `~/.cache/whisper`。
- `--model` 在此安装中默认为 `turbo`。
- 使用较小的模型以获得速度，使用较大的模型以获得准确性。
