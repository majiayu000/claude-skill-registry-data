---
name: gen-sora-video
description: Generate a Sora video from a text prompt via an Azure OpenAI endpoint, then download the resulting .mp4 locally. Use when the user asks to generate a Sora video/video.mp4 from a prompt or wants the generated video saved to disk.
---

# Generate Sora Video

Generate a Sora video from a prompt and save it as an `.mp4` file locally.



### Run

```bash
.venv/Scripts/python .claude/skills/gen_sora/scripts/gen_sora.py "<prompt>" "output.mp4" --seconds 8 --size 1280x720
```

### Parameters

- Required: `prompt` (text prompt), `output_path` (where to save the mp4)
- Optional: `--model` (default: env `SORA_MODEL` or `sora-2`), `--seconds` (default: 8), `--size` (default: `1280x720`), `--poll-seconds` (default: env `SORA_POLL_SECONDS` or `20`), `--input-reference` (default: omitted)

## Examples

Generate and save an mp4:

```bash
.venv/Scripts/python .claude/skills/gen_sora/scripts/gen_sora.py "A cinematic drone shot of a futuristic city at sunset" "my_city.mp4" --seconds 10 --size 1920x1080
```

