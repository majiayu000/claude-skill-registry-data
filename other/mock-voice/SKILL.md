---
name: mock-voice
description: Clone a voice from YouTube audio and synthesize custom dialogue using OmniVoice (k2-fsa, diffusion-LM TTS), with gemma4:e2b (Ollama) for fast reference transcription. Use when the user provides a YouTube URL and wants to generate speech in that voice — anime character impersonations, VTuber-style lines, voice-over demos, multilingual (600+ languages) output.
version: 4.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [yt-dlp, ffmpeg]
  paths: [~/src/OmniVoice]
  services: [ollama (gemma4:e2b)]
  # Note: detect_lang.py is no longer used — agent must detect language and pass -l
metadata:
  hermes:
    tags: [voice, TTS, cloning, YouTube, OmniVoice, diffusion, anime, cosplay, multilingual]
---

# Mock Voice — YouTube Voice Cloning + OmniVoice TTS

Download audio from a YouTube link, extract a short voice prompt, then synthesize custom
dialogue using **OmniVoice** (k2-fsa diffusion-LM zero-shot TTS, 600+ languages,
GPU-accelerated on ROCm / gfx1151).

## When to use this skill

- "Clone this anime character's voice and make them say X"
- "Use this YouTube video as voice prompt for: [dialogue]"
- "/mock-voice [URL] '台詞'"
- Any request combining a YouTube video + custom speech output (any of 600+ languages)

## Prerequisites

- `yt-dlp` — YouTube audio extraction (`~/.local/bin/yt-dlp`)
- `ffmpeg` — audio trim / format conversion
- OmniVoice at `~/src/OmniVoice` with GPU torch (`torch 2.11.0+rocm7.2`), installed in
  `.venv` (see `~/SOUND.md`). Model `k2-fsa/OmniVoice` auto-downloads on first run.

## No vocal isolation needed

OmniVoice tolerates background music well — it auto-transcribes the reference with
Whisper-large-v3-turbo and clones via diffusion. **You do NOT need to strip BGM with
demucs/UVR for normal clips.** Just trim to a clean window and go. (Only if the source has
very loud music drowning the voice, see the optional demucs fallback at the bottom.)

## Quick start (one-shot wrapper)

The whole pipeline (download → trim → gemma4:e2b ref_text → OmniVoice GPU synth) is wrapped in
`~/.claude/skills/mock-voice/mock_voice.sh`. For most requests, just run:

```bash
~/.claude/skills/mock-voice/mock_voice.sh \
  -u "https://youtube.com/shorts/Ir3C_O7r3IA" \
  -t "今日はいい天気ですね、散歩に行きましょう。" \
  -l Japanese \
  -o results_omni/mock.wav
```

Options: `-u` URL, `-t` text, `-l` language (**REQUIRED** — agent must detect and pass, e.g. `ja`/`zh`/`en`/`ko`), `-o` output,
`-s` ref start second (default 2), `-d` ref duration (default 8), `-n` diffusion steps
(16 fast / 32 quality, default 32), `-r` override ref_text (skip gemma).

**Language detection**: The script no longer auto-detects language (bash regex lacks reliable Unicode support). The agent (you) must inspect the `-t` text and pass the correct `-l` code:
- `ja` — Japanese (hiragana/katakana/kanji)
- `zh` — Chinese (simplified/traditional)
- `en` — English
- `ko` — Korean (hangul)
- `ru` — Russian (Cyrillic)
- `ar` — Arabic
- `th` — Thai
- `hi` — Hindi (Devanagari)
- Japanese kanji-only text without kana may be ambiguous; when in doubt, use `ja`.

The result is at the `-o` path (default `~/src/OmniVoice/results_omni/mock.wav`). Use the manual
steps below only when you need to tweak a stage (e.g. pick a cleaner reference window).

## Workflow (manual / step-by-step)

### Step 0: Clean old WAV files

Clear all previous WAV outputs before starting — prevents stale references from interfering:
```bash
rm -f ~/src/OmniVoice/asset_mock/*.wav
rm -f ~/src/OmniVoice/results_omni/*.wav
```

### Step 1: Download audio from YouTube

```bash
cd ~/src/OmniVoice/asset_mock   # mkdir -p if needed
yt-dlp -f "bestaudio" --extract-audio --audio-format wav \
  --output "ref.%(ext)s" --no-playlist \
  "https://youtube.com/shorts/Ir3C_O7r3IA" 2>&1 | tail -5
```

Reference voice source used to build this skill: `https://youtube.com/shorts/Ir3C_O7r3IA`

### Step 2: Find a transcribable clip with gemma4:e2b

OmniVoice needs a clean speech reference. **After downloading, don't guess a time window — scan**
until gemma4:e2b produces a non-empty transcription. This avoids wasting time on BGM-only or
silence windows.

```bash
cd ~/src/OmniVoice/asset_mock

# Get total duration
DUR=$(ffprobe -v quiet -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 ref.wav)

# Scan: try samples every 15s, pick the first one where gemma returns text
for start in $(seq 0 15 $(int ${DUR%.*})); do
  ffmpeg -y -i ref.wav -ss "$start" -t 6 -ar 16000 -ac 1 -c:a pcm_s16le /tmp/ref_probe.wav 2>/dev/null
  RT=$(~/src/OmniVoice/.venv/bin/python ~/.claude/skills/mock-voice/ref_transcribe.py /tmp/ref_probe.wav 2>/dev/null)
  if [ -n "$RT" ]; then
    echo "Found transcribable window at start=${start}s: $RT"
    # Copy this as the ref
    ffmpeg -y -i ref.wav -ss "$start" -t 8 -ar 16000 -ac 1 -c:a pcm_s16le ref_16k.wav 2>/dev/null
    REF_START=$start
    break
  fi
  echo "start=${start}s: empty gemma output — trying next window"
done

# Fallback: if no window works, use first window anyway
[ -z "${REF_START:-}" ] && {
  echo "WARNING: no transcribable window found — using first 8s as fallback"
  ffmpeg -y -i ref.wav -ss 0 -t 8 -ar 16000 -ac 1 -c:a pcm_s16le ref_16k.wav 2>/dev/null
}
```

OmniVoice wants a 3–10s reference of clear speech. The scan above picks 6–8s windows spaced
15s apart. Adjust the interval if the video is short (e.g., `< 60s` → try every 3s).

### Step 3: Verify ref_text (if scan already transcribed, skip)

If Step 2 found a window with gemma output, `$RT` is already set. Otherwise verify:
```bash
cd ~/src/OmniVoice
RT=$(~/src/OmniVoice/.venv/bin/python ~/.claude/skills/mock-voice/ref_transcribe.py asset_mock/ref_16k.wav)
echo "ref_text: $RT"
```

### Step 4: Synthesize with OmniVoice (GPU)

```bash
cd ~/src/OmniVoice
PYTHONUTF8=1 .venv/bin/python -m omnivoice.cli.infer \
  --text "こんにちは、私の声をクローンできましたか？" \
  --language Japanese \
  --ref_audio asset_mock/ref_16k.wav \
  --ref_text "$RT" \
  --output results_omni/mock.wav \
  --device cuda
```

Notes:
- `--language` here is set automatically by the wrapper (see auto-detection below). When running
  by hand, detect it: `LANG=$(~/src/OmniVoice/.venv/bin/python ~/.claude/skills/mock-voice/detect_lang.py "<your text>")` then pass `--language "$LANG"`.
  Omitting `--language` works but uses language-agnostic mode (slightly lower quality).
- **Japanese takes natural kanji/kana directly** — no katakana conversion needed (unlike CosyVoice).
- `--ref_text "$RT"` (from Step 3, gemma) skips OmniVoice's slow Whisper.
- `--device cuda` uses the AMD GPU (ROCm). `PYTHONUTF8=1` must be set or CJK text garbles.
- Diffusion knobs: `--num_step` (16 fast / 32 quality, default 32), `--speed` (>1 faster).
- Voice design instead of cloning: drop `--ref_audio`/`--ref_text`, add `--instruct "a calm young
  female voice"`.

### Language detection (agent-driven)

`detect_lang.py` still exists but is **no longer called by the wrapper**. The agent must inspect
the synthesis text and pass the correct `-l` code:

| Script detected | Language code |
|---|---|
| Hiragana/Katakana (あいうアィウ) | `ja` |
| Hangul (한글) | `ko` |
| Han characters (漢字) | `zh` or `ja` (ambiguity — use context) |
| Cyrillic (кириллица) | `ru` |
| Arabic (عربي) | `ar` |
| Thai (ไทย) | `th` |
| Devanagari (हिन्दी) | `hi` |
| Latin / other | `en` |

Caveat: **pure-kanji Japanese with no kana** looks like `zh`. When the context is Japanese
(anime lines, Japanese voice actors, etc.), use `-l ja`.

### Step 4: Output

```bash
cp ~/src/OmniVoice/results_omni/mock.wav /tmp/mock_voice.wav
```

## Parameter Reference (`omnivoice.cli.infer`)

| Parameter | Required | Description |
|---|---|---|
| `--text` | ✅ | Text to synthesize (natural script, 600+ languages) |
| `--output` | ✅ | Output WAV path |
| `--ref_audio` | for cloning | Reference voice WAV (3–10s clean speech, 16kHz mono) |
| `--ref_text` | optional | Transcription of the ref — **skips Whisper, much faster** |
| `--language` | ✅ (via `-l`) | Language name or code (`Japanese`/`ja`, …); **agent must detect and pass `-l`** |
| `--instruct` | voice design | Style description (use instead of `--ref_audio`) |
| `--device` | — | `cuda` (AMD GPU via ROCm) / auto |
| `--num_step` | — | Diffusion steps (16 fast / 32 quality) |
| `--speed` | — | Speaking rate (>1 faster, <1 slower) |
| `--guidance_scale` | — | CFG scale (default 2.0) |

## Example: one-shot (used to build this skill)

```bash
# Agent detects language from text (Japanese kana/kanji -> ja); gemma4:e2b makes the ref_text; OmniVoice on GPU.
~/.claude/skills/mock-voice/mock_voice.sh \
  -u "https://youtube.com/shorts/Ir3C_O7r3IA" \
  -t "こんにちは、私の声をクローンできましたか？テスト成功ですね。" \
  -l ja \
  -o results_omni/mock.wav
# -> ref_text via gemma ; Saved to results_omni/mock.wav
```

## Performance (Strix Halo gfx1151, ROCm 7.2)

Measured breakdown (warm, per process):
- **Model load (OmniVoice TTS): ~1.9s** — fast, not a bottleneck.
- **Whisper load + transcribe of the ref: ~0.8s + ~6s** — fixed cost, independent of output
  length. Skip entirely with `--ref_text` (saves ~7s/run, and avoids Whisper hallucinating on
  noisy/BGM refs).
- **Diffusion: the dominant cost** — ~RTF 1.4–2.7, scales with output length. Speed it up with
  `--num_step 16` (~2× faster, slightly lower quality) and optionally
  `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1` (enables ROCm flash attention; otherwise SDPA
  falls back to a slower path).

So for fastest runs: pass `--ref_text` + `--num_step 16`. GPU runs ~100% during diffusion.

## Common Pitfalls

- **Garbled text**: missing `PYTHONUTF8=1`.
- **Slow every run**: Whisper re-transcribing the ref → pass `--ref_text`.
- **`MIOpen(HIP): Warning [IsEnoughWorkspace]` / "Flash/Mem Efficient attention experimental"**:
  harmless AMD ROCm warnings, ignore. (Optional: `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1`.)
- **yt-dlp "No supported JavaScript runtime"**: non-fatal; falls back. Install `deno` to silence.
- **Wrong language/accent**: set `--language` explicitly to the target language.

## Optional: demucs vocal isolation (only for very noisy sources)

Normally unnecessary. If the clip has loud music drowning the voice, isolate vocals first
using the separate demucs venv (CPU), then feed the result as `--ref_audio`:
```bash
cd ~/src/CosyVoice   # demucs lives here: .venv-demucs (CPU torch 2.3.1 + soundfile)
.venv-demucs/bin/demucs --two-stems vocals -o /tmp/demucs_out /path/to/ref_trim.wav
ffmpeg -y -i /tmp/demucs_out/htdemucs/ref_trim/vocals.wav -ar 16000 -ac 1 \
  -c:a pcm_s16le ~/src/OmniVoice/asset_mock/ref_16k.wav
```
