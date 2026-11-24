---
name: tts
description: Text-to-speech for voiceovers and spoken output. Renders narration for product, feature, and demo videos as per-scene audio files with exact durations, timing offsets, and captions, and speaks text aloud. Supports the built-in macOS/Linux voice, local Kokoro, OpenAI, ElevenLabs, Gemini, Cartesia, and Deepgram. Use when the user wants a voiceover, narration, or audio for a video or screencast, wants something read aloud or announced, wants an audio file (.wav/.mp3/.m4a), wants to compare or choose voices, or wants to set up TTS providers and API keys.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/tts *)
---

# Text to speech

Run the launcher at `${CLAUDE_SKILL_DIR}/scripts/tts`, which is `scripts/tts` in this skill's directory. Below it's written as `tts`. The first run downloads a ~7 MB binary and checks its SHA-256 before running it.

Run each `tts` command as its own Bash call. Don't chain it with `;`, `&&`, or pipes, so it stays covered by the skill's pre-approved permission.

There are two jobs:
- **Voiceovers for videos:** `tts render`. Produces files plus a timing manifest for the rest of the video pipeline.
- **Speaking aloud:** `tts "text"`. Plays through the speakers and returns immediately.

## Voiceovers for videos

### 1. Write a script

Put one segment per scene or shot, and reuse the video's scene ids so audio and visuals line up:

```json
{
  "provider": "elevenlabs",
  "voice": "JBFqnCBsd6RMkjVDRZzb",
  "instructions": "warm, confident product narrator",
  "pause": 0.5,
  "segments": [
    {"id": "01-intro",   "text": "Meet the new Insights dashboard."},
    {"id": "02-filters", "text": "Filter any chart in one click: by team, by service, or by release."},
    {"id": "03-alerts",  "text": "Set an alert once, and we'll tell you the moment a metric drifts.", "pause": 1.0},
    {"id": "04-outro",   "text": "Insights is available today, on every plan."}
  ]
}
```

- **Top-level fields** (`provider`, `voice`, `model`, `instructions`, `speed`, `pause`) apply to every segment. Each segment can override `voice`, `model`, `instructions`, `speed`, and `pause`, which is the silence after it in the combined track.
- **Keep one provider and voice for the whole video** so it sounds like one narrator.
- **Write for the ear:** short sentences, numbers as spoken ("forty percent", "version two"), no markdown. If a product name is mispronounced, spell it phonetically in `text`.
- **Choosing a provider and voice.** If the script doesn't set a provider and `tts config show` has no `voiceover_provider`, ask the user which provider and voice to use. To let them compare, render short samples with `tts -o sample-NAME.wav -p PROVIDER -v VOICE "One line of the script."`. Offer to save their choice with `tts config set voiceover_provider NAME` and `tts config set NAME.voice VOICE`. Kokoro and `system` are free and local; the rest are paid. ElevenLabs, OpenAI with `instructions`, and Gemini sound the most natural.

### 2. Render

```bash
"${CLAUDE_SKILL_DIR}/scripts/tts" render script.json -o voiceover/
```

This writes:
- `voiceover/<id>.wav` for each segment, with leading and trailing silence trimmed so durations are exact.
- `voiceover/voiceover.wav`, all segments joined with their pauses.
- `voiceover/voiceover.srt`, captions.
- `voiceover/manifest.json`, which is also printed to stdout:

```json
{"provider": "elevenlabs", "sample_rate": 24000, "channels": 1, "duration": 17.08,
 "combined": {"file": "/abs/voiceover/voiceover.wav", "duration": 17.08},
 "captions": "/abs/voiceover/voiceover.srt",
 "segments": [{"id": "01-intro", "file": "/abs/voiceover/01-intro.wav", "duration": 3.872,
               "start": 0, "end": 3.872, "text": "...", "voice": "...", "cached": false}, ...]}
```

Render options:
- `--format mp3|m4a` sets the combined track's format.
- `--no-combine` writes only the per-segment files.
- `-p/-v/-i/-s` set defaults the script doesn't specify.
- `--jobs N` sets parallelism.

`render` uses each provider's highest-fidelity model unless one is set: `eleven_multilingual_v2` and `gemini-3.8-flash-tts`.

### 3. Use the timings

- **Scene lengths:** each scene should last at least its segment's `duration`. Add a beat of breathing room, or extend the scene to match.
- **Placing audio:** put each segment's file at its scene's start time, or use `voiceover.wav` as a single track with `start`/`end` as offsets.
- **Muxing with ffmpeg:**
  - The whole track: `ffmpeg -i video.mp4 -i voiceover/voiceover.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest out.mp4`
  - One segment at 4.47 s: add the input `-i voiceover/02-filters.wav`, then `-filter_complex "[1]adelay=4470:all=1[a]" -map 0:v -map "[a]"`.

### 4. Iterate

Edit the script and run the same command again. Segments whose text, voice, model, style, and speed are unchanged are reused from the last render (`"cached": true`). Only the changed segments are re-rendered and billed. Use `--force` to re-render everything. If some segments fail, the others are kept, and re-running retries only the failures.

## Speaking aloud

```bash
"${CLAUDE_SKILL_DIR}/scripts/tts" "The build passed and all 214 tests are green."
"${CLAUDE_SKILL_DIR}/scripts/tts" <<'EOF'
Longer text, or anything with quotes, goes on stdin.
EOF
```

This returns once audio is playing, and playback continues in the background. New speech interrupts current speech; `-q` queues it instead, and `tts stop` silences everything.

Other options:
- `-p` provider, `-v` voice, `-i "style"`, `-s` speed.
- `-w` waits for playback to finish.
- `-o FILE [--json]` writes one file instead of playing. `--json` prints its duration and path.

When speaking:
- **Summarize; don't recite.** Use two to four spoken sentences unless asked to read the full text.
- **Describe code in words** instead of reading it. Markdown and code blocks are stripped automatically.
- **Keep notifications short**, and use `-q` for a series of them.

## Providers, cost, and privacy

- Use the configured defaults (`tts config show`). Pass `-p` only when the user or the script names a provider.
- `system` and `kokoro` stay on this machine and are free. The other providers send the text to that company and bill the user's account. Never change the default provider without asking.
- Never send secrets, credentials, or private data to a cloud provider.
- Paid providers refuse more than 20,000 new characters per command. Shorten the text, or pass `--max-chars N` if the user wants it all.

## Setup and troubleshooting

- `tts doctor` shows the audio output, the default provider, and which providers are ready.
- `tts providers` and `tts voices -p NAME [filter]` list providers and voices.
- `tts config set KEY VALUE` sets defaults. Keys are `provider`, `voiceover_provider`, `max_chars`, and `NAME.voice|model|speed|instructions|base_url`.
- **Missing API key:** tell the user to set the env var (e.g. `ELEVENLABS_API_KEY`) or run `tts auth set elevenlabs` **in their own terminal**. Never ask the user to paste a key into the chat, and never put one on a command line.
- **Untested cloud providers:** `openai`, `gemini`, `cartesia`, and `deepgram` haven't been tested against their live APIs yet. Only `system`, `kokoro`, and `elevenlabs` have. If one of them fails with an error about the request itself (an unknown field, invalid parameter, or unexpected response), it's probably a bug in this skill, not something the user did. Show the user the exact error, suggest reporting it at github.com/captjt/skill-tts/issues, and offer `kokoro` or `system` as a fallback. Don't keep retrying with guessed parameters. Auth (401/403) and quota (429) errors are the user's to fix as usual.
- **Kokoro not reachable:** start it with `docker run -d --name kokoro -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:v0.9.0`.
- **No audio device** (SSH, containers): use `render` or `-o`; they don't need speakers.

Voices, models, and options for each provider are in [references/providers.md](references/providers.md).
