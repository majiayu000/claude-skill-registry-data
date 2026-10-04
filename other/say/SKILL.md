---
name: say
description: Text-to-Speech via macOS say command with Siri Natural Voices. Use for generating speech audio, TTS clips, or speaking text aloud on macOS.
metadata: {"openclaw":{"emoji":"🔊","os":["darwin"],"requires":{"bins":["say","ffmpeg"]}}}
---

# say

Use `say` for on-device text-to-speech on macOS.

## Siri Natural Voices (recommended)

Siri voices are the best macOS TTS voices but **cannot be selected via `-v`**. Instead, run `say` without `-v` — it uses the system default voice. Switch languages via `defaults write`:

```bash
# Switch to German
defaults write com.apple.speech.voice.prefs SystemTTSLanguage -string "de"
say "Hallo, wie geht's?" -o output_de.aiff

# Switch to Chinese (Mandarin)
defaults write com.apple.speech.voice.prefs SystemTTSLanguage -string "cmn"
say "你好，世界" -o output_zh.aiff
```

No process restart needed — the next `say` invocation picks up the new language immediately.

### Prerequisites

Download the desired Siri voices first in **System Settings > Accessibility > Spoken Content** and set them as the system voice for each language.

Check which voices are currently configured:

```bash
defaults read com.apple.Accessibility SpokenContentDefaultVoiceSelectionsByLanguage
```

## Fallback: select voice via `-v`

For non-Siri voices, use `-v` directly:

```bash
say -v 'Tingting (Enhanced)' "你好，世界"
say -v '?'  # list all installed voices (Siri voices not listed)
```

## Output to file

```bash
say -o output.aiff "Hello world"
ffmpeg -y -i output.aiff -ar 22050 -ac 1 output.wav  # convert to WAV
```

## Options

- `-v <voice>` — Select a non-Siri voice
- `-r <rate>` — Speaking rate in words per minute (e.g. `-r 150`)
- `-o <file>` — Save to AIFF file instead of playing aloud

## Notes

- `say` adds natural pauses at punctuation — no manual sentence splitting needed
- AIFF is the native output format; convert with ffmpeg for WAV/MP3
- For batch generation: set language once, generate all clips, then switch — minimizes `defaults write` calls
