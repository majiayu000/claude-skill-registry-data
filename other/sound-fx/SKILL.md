---
name: sound-fx
description: "Use this skill whenever the user wants to generate sound effects, ambient audio, or short audio clips from a text description. Triggers include: any mention of 'sound effect', 'sfx', 'generate sound', 'make a sound', 'audio effect', 'ambient sound', 'foley', 'sound clip', 'noise', or requests to produce a specific sound (e.g. 'make a gunshot sound', 'generate thunder', 'create the sound of rain'). Also use when the user describes an action or scenario and wants the corresponding audio (e.g. 'someone getting spanked', 'a door slamming', 'cartoon boing'). Do NOT use for speech synthesis, music generation with melody/lyrics, or voice cloning."
permissions:
  - network
  - filesystem
metadata: {"openclaw": {"primaryEnv": "NOIZ_API_KEY"}}
---

# sound-fx

Generate any sound effect from a text description — footsteps, explosions, cartoon boings, ambient rain, or whatever you can imagine.

## Triggers

- sound effect / sfx / foley
- generate sound / make a sound / create audio
- ambient sound / background noise
- what does X sound like / make the sound of X
- 音效 / 声音 / 音频效果

## Quick Start

```bash
# Animals
python3 skills/sound-fx/scripts/sfx.py "a cat purring contentedly, deep rumbling vibration" -d 8
python3 skills/sound-fx/scripts/sfx.py "dog sneezing three times in a row" -d 3
python3 skills/sound-fx/scripts/sfx.py "dog eating food really fast, chomping and gulping" -d 4

# Funny
python3 skills/sound-fx/scripts/sfx.py "cartoon character getting spanked, exaggerated squeaky yelp" -d 2
python3 skills/sound-fx/scripts/sfx.py "someone sitting on a whoopee cushion mid-meeting" -d 2

# Ambient (save to file)
python3 skills/sound-fx/scripts/sfx.py "heavy rain on a tin roof" -d 15 -o rain.wav
python3 skills/sound-fx/scripts/sfx.py "campfire crackling at night, crickets in background" -d 15 -o campfire.wav
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `prompt` | required | Text description of the sound to generate |
| `--duration` / `-d` | auto | Length in seconds (1–30). Omit to let the model decide. |
| `--format` / `-f` | `wav` | Output format: `wav`, `mp3`, `flac` |
| `--output` / `-o` | `output.wav` | Path to save the generated audio |
| `--api-key` | from env/config | Noiz API key (overrides stored key) |

## Configuration

```bash
# Save your API key once
python3 skills/sound-fx/scripts/sfx.py config --set-api-key YOUR_KEY

# Or set via environment variable
export NOIZ_API_KEY=YOUR_KEY
```

Get your API key at [developers.noiz.ai](https://developers.noiz.ai/api-keys).

## Fun Example Prompts

### 🐾 Animals
| Prompt | Suggested Duration |
|--------|--------------------|
| `"a cat purring contentedly, deep rumbling vibration"` | 8s |
| `"cat hissing and yowling aggressively"` | 3s |
| `"cat knocking a glass off the table, crash"` | 2s |
| `"dog sneezing three times in a row"` | 3s |
| `"small dog barking excitedly at a doorbell"` | 4s |
| `"dog howling dramatically at the moon"` | 5s |
| `"dog eating food really fast, chomping and gulping"` | 4s |
| `"hamster running furiously on a squeaky wheel"` | 6s |
| `"parrot perfectly mimicking a phone ringing"` | 3s |
| `"frog croaking in a pond at night"` | 8s |

### 😂 Funny & Expressive
| Prompt | Suggested Duration |
|--------|--------------------|
| `"cartoon character getting spanked, exaggerated squeaky yelp"` | 2s |
| `"dramatic fail horn (wah wah wah wah)"` | 3s |
| `"someone sitting on a whoopee cushion mid-meeting"` | 2s |
| `"anime power-up charging sound"` | 5s |
| `"someone slipping on a banana peel, cartoon slide and crash"` | 3s |
| `"dramatic chipmunk stare — suspenseful strings"` | 3s |
| `"rubber duck squeak three times"` | 2s |
| `"evil villain laugh echoing in a dungeon"` | 5s |
| `"crowd gasping in disbelief"` | 3s |
| `"a notification sound that sounds passive-aggressive"` | 2s |
| `"someone aggressively typing on a mechanical keyboard"` | 5s |

### 🌍 Ambient & Atmosphere
| Prompt | Suggested Duration |
|--------|--------------------|
| `"heavy rain and thunder on a metal roof"` | 15s |
| `"busy coffee shop, background chatter and espresso machine"` | 15s |
| `"old dial-up modem connecting to the internet"` | 10s |
| `"campfire crackling at night, crickets in background"` | 15s |
| `"ocean waves gently crashing on a beach"` | 15s |

### 🎮 Action & Sci-Fi
| Prompt | Suggested Duration |
|--------|--------------------|
| `"spaceship laser blaster"` | 2s |
| `"monster truck engine revving"` | 5s |
| `"sword being unsheathed from scabbard"` | 2s |
| `"video game level-up fanfare"` | 3s |

## Output

On success, the audio file is saved to the output path and the URL is printed:

```
✓ Saved to output.wav (3.2s, 282 KB)
  URL: https://storage.googleapis.com/...
```

## Third-Party Integration

To send generated sound effects to Discord, Telegram, Feishu, or mix them into videos with ffmpeg, see [ref_3rd_party.md](ref_3rd_party.md).

## Requirements

- Python 3.6+
- `requests` package: `pip install requests`
- Noiz API key from [developers.noiz.ai](https://developers.noiz.ai/api-keys)

## Security & Data Disclosure

- **API key**: Stored in `~/.config/noiz/api_key` (permissions `0600`) or via `NOIZ_API_KEY` env variable.
- **Network**: The text prompt is sent to `https://noiz.ai/v1/text-to-sound` for generation. No other data is transmitted.
- **Output**: Generated audio is downloaded from a Noiz GCS URL and saved locally.
