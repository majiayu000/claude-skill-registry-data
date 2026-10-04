---
name: hyperframes-media
description: Asset preprocessing for HyperFrames compositions — text-to-speech narration (Kokoro), audio/video transcription (Whisper), and background removal for transparent overlays (u2net). Use when generating voiceover from text, transcribing speech for captions, removing the background from a video or image to use as a transparent overlay, choosing a TTS voice or whisper model, or chaining these (TTS → transcribe → captions). Each command downloads its own model on first run.
---

# HyperFrames Media Preprocessing

Three CLI commands that produce assets for compositions: `tts` (speech), `transcribe` (timestamps), and `remove-background` (transparent video). Each downloads a model on first run and caches it under `~/.cache/hyperframes/`. Drop the output into the project, then reference it from the composition HTML — see the `hyperframes` skill for the audio/video element conventions.

## Text-to-Speech (`tts`)

Generate speech audio locally with Kokoro-82M. No API key.

```bash
npx hyperframes tts "Text here" --voice af_nova --output narration.wav
npx hyperframes tts script.txt --voice bf_emma --output narration.wav
npx hyperframes tts --list                       # all 54 voices
```

### Voice Selection

Match voice to content. Default is `af_heart`.

| Content type      | Voice                 | Why                           |
| ----------------- | --------------------- | ----------------------------- |
| Product demo      | `af_heart`/`af_nova`  | Warm, professional            |
| Tutorial / how-to | `am_adam`/`bf_emma`   | Neutral, easy to follow       |
| Marketing / promo | `af_sky`/`am_michael` | Energetic or authoritative    |
| Documentation     | `bf_emma`/`bm_george` | Clear British English, formal |
| Casual / social   | `af_heart`/`af_sky`   | Approachable, natural         |

### Multilingual

Voice IDs encode language in the first letter: `a`=American English, `b`=British English, `e`=Spanish, `f`=French, `h`=Hindi, `i`=Italian, `j`=Japanese, `p`=Brazilian Portuguese, `z`=Mandarin. The CLI auto-detects the phonemizer locale from the prefix — no `--lang` needed when the voice matches the text.

```bash
npx hyperframes tts "La reunión empieza a las nueve" --voice ef_dora --output es.wav
npx hyperframes tts "今日はいい天気ですね" --voice jf_alpha --output ja.wav
```

Use `--lang` only to override auto-detection (stylized accents). Valid codes: `en-us`, `en-gb`, `es`, `fr-fr`, `hi`, `it`, `pt-br`, `ja`, `zh`. Non-English phonemization requires `espeak-ng` system-wide (`brew install espeak-ng` / `apt-get install espeak-ng`).

### Speed

- `0.7-0.8` — tutorial, complex content, accessibility
- `1.0` — natural pace (default)
- `1.1-1.2` — intros, transitions, upbeat content
- `1.5+` — rarely appropriate; test carefully

### Long Scripts

For more than a few paragraphs, write to a `.txt` file and pass the path. Inputs over ~5 minutes of speech may benefit from splitting into segments.

### Requirements

Python 3.8+ with `kokoro-onnx` and `soundfile` (`pip install kokoro-onnx soundfile`). Model downloads on first use (~311 MB + ~27 MB voices, cached in `~/.cache/hyperframes/tts/`).

## Transcription (`transcribe`)

Produce a normalized `transcript.json` with word-level timestamps.

```bash
npx hyperframes transcribe audio.mp3
npx hyperframes transcribe video.mp4 --model small --language es
npx hyperframes transcribe subtitles.srt          # import existing
npx hyperframes transcribe subtitles.vtt
npx hyperframes transcribe openai-response.json
```

### Language Rule (Non-Negotiable)

**Never use `.en` models unless the user explicitly states the audio is English.** `.en` models (`small.en`, `medium.en`) **translate** non-English audio into English instead of transcribing it. This silently destroys the original language.

1. Language known and non-English → `--model small --language <code>` (no `.en` suffix)
2. Language known and English → `--model small.en`
3. Language unknown → `--model small` (no `.en`, no `--language`) — whisper auto-detects

**Default model is `small`, not `small.en`.**

### Model Sizes

| Model      | Size   | Speed    | When to use                           |
| ---------- | ------ | -------- | ------------------------------------- |
| `tiny`     | 75 MB  | Fastest  | Quick previews, testing pipeline      |
| `base`     | 142 MB | Fast     | Short clips, clear audio              |
| `small`    | 466 MB | Moderate | **Default** — most content            |
| `medium`   | 1.5 GB | Slow     | Important content, noisy audio, music |
| `large-v3` | 3.1 GB | Slowest  | Production quality                    |

Music with vocals: start at `medium` minimum; produced tracks often need manual SRT/VTT import. For caption-quality checks (mandatory after every transcription), the cleaning JS, retry rules, and the OpenAI/Groq API import path, see [hyperframes/references/transcript-guide.md](../hyperframes/references/transcript-guide.md).

### Output Shape

Compositions consume a flat array of word objects. The `id` field (`w0`, `w1`, ...) is added during normalization for stable references in caption overrides; it's optional for backwards compatibility.

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

## Background Removal (`remove-background`)

Remove the background from a video or image so it can sit as a transparent overlay in a composition (e.g. an avatar floating on a background plate).

```bash
npx hyperframes remove-background avatar.mp4 -o transparent.webm  # default: VP9 alpha WebM
npx hyperframes remove-background avatar.mp4 -o transparent.mov   # ProRes 4444 (editing)
npx hyperframes remove-background portrait.jpg -o cutout.png      # single-image cutout
npx hyperframes remove-background avatar.mp4 -o transparent.webm --device cpu
npx hyperframes remove-background --info                          # detected providers
```

Uses `u2net_human_seg` (MIT). First run downloads ~168 MB of weights to `~/.cache/hyperframes/background-removal/models/`.

### Output Format

| Format                | When                                                          |
| --------------------- | ------------------------------------------------------------- |
| `.webm` (VP9 + alpha) | Default. Compositions play this directly via `<video>`.       |
| `.mov` (ProRes 4444)  | Editing in DaVinci/Premiere/FCP. Large files.                 |
| `.png`                | Single-image cutout (still subject, layered over a backdrop). |

Chrome decodes VP9 alpha natively, so the `.webm` plugs into a composition like any other muted-autoplay video — see the `hyperframes` skill for the `<video>` track conventions.

## TTS → Transcribe → Captions

When there's no pre-recorded voiceover, generate one and transcribe it back to get word-level timestamps for captions:

```bash
npx hyperframes tts script.txt --voice af_heart --output narration.wav
npx hyperframes transcribe narration.wav   # → transcript.json
```

Whisper extracts precise word boundaries from the generated audio, so caption timing matches delivery without hand-tuning.
