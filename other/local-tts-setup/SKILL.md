---
name: local-tts-setup
description: "Set up a local TTS server (Qwen3-TTS, LM Studio) with voice cloning, and configure Hermes TTS to use it. Covers Qwen3-TTS deployment on Windows/Linux, voice cloning from reference audio, Hermes TTS provider config for custom OpenAI-compatible endpoints, and Python/CUDA troubleshooting. Trigger on 'set up voice cloning', 'local TTS', 'want my own voice', 'Qwen3-TTS setup'."
version: 1.0.0
platforms: [windows, linux]
metadata:
  hermes:
    tags: [tts, voice-cloning, qwen3-tts, audio, local-tts]
---

# Local TTS with Voice Cloning

Set up a local TTS server with voice cloning and wire it into Hermes as a custom TTS provider. Primary target: **Qwen3-TTS** via the OpenAI-compatible FastAPI server. Also covers LM Studio fallback and ElevenLabs cloud option.

## Architecture

```
Hermes agent → hermes config (tts.openai.base_url) → Qwen3-TTS server (localhost:8880 or LAN)
                                                              ↕
                                                   Custom voice clone prompt (.pkl)
                                                              ↕
                                                   Reference audio clip (5-15s)
```

## Option Comparison

| Approach | Quality | Voice Cloning | Setup | Notes |
|---|---|---|---|---|
| **Qwen3-TTS** | ⭐⭐⭐⭐⭐ | ✅ 3-second clone | Moderate | Best overall — recommended |
| **LM Studio + CosyVoice GGUF** | ⭐⭐⭐ | ❌ No clone via API | Easy | TTS only, no cloning |
| **ElevenLabs** (cloud) | ⭐⭐⭐⭐⭐ | ✅ Upload clip | Easy | Best fallback — voice settings tunable |
| **Piper** (built into Hermes) | ⭐⭐ | ❌ | None | Fallback, always available |

## Quickest Win: ElevenLabs Voice Cloning

When local GPU/TTS setup is blocked (Python version mismatches, CUDA issues, time constraints), ElevenLabs is the fastest path to a cloned voice.

### Workflow

1. **Get a clip** — Same as Qwen3-TTS: 5-15s clean audio of the target voice
2. **Upload to ElevenLabs Voice Lab** — https://elevenlabs.io/app/voice-lab → "Add Voice" → "Instant Voice Cloning"
3. **Get the voice_id** — The cloned voice gets an ID. Verify via API:
   ```bash
   curl -s -H "xi-api-key: $ELEVENLABS_API_KEY" https://api.elevenlabs.io/v1/voices
   ```
   Look for `[CLONED]` category in the response.
4. **Configure Hermes**:
   ```bash
   hermes config set tts.provider elevenlabs
   hermes config set tts.elevenlabs.voice_id "<voice_id_from_step_3>"
   hermes config set tts.elevenlabs.model_id eleven_multilingual_v2
   ```
   Set the API key in `~/.hermes/<profile>/.env`:
   ```
   ELEVENLABS_API_KEY=sk_...
   ```

### Voice Settings Tuning

ElevenLabs defaults are conservative (stable/flat). For a more expressive, lively voice, tune these:

```bash
hermes config set tts.elevenlabs.stability 0.35
hermes config set tts.elevenlabs.similarity_boost 0.75
hermes config set tts.elevenlabs.style 0.5
hermes config set tts.elevenlabs.speaker_boost true
```

| Setting | Range | Lower | Higher |
|---|---|---|---|
| `stability` | 0.0-1.0 | More expressive, varied | More stable, robotic |
| `similarity_boost` | 0.0-1.0 | Less like original | Very close to original |
| `style` | 0.0-1.0 | Less character | More exaggerated style |
| `speaker_boost` | bool | — | Boosts presence/clarity |

**Recommended start:** `stability: 0.35`, `similarity_boost: 0.75`, `style: 0.5`, `speaker_boost: true`. Adjust stability downward to 0.2 for more emotion, upward to 0.5+ for consistency.

> **Note:** Hermes' ElevenLabs provider needs `voice_settings` passed in the API call. See `references/elevenlabs-voice-settings-patch.md` for the exact diff and config keys.

## Qwen3-TTS Setup

### Prerequisites

- **Python 3.12** (NOT 3.13 — PyTorch CUDA wheels don't support 3.13 yet)
- **CUDA-capable GPU** (RTX 4070+ recommended, ~4GB VRAM needed for 1.7B model)
- **Git**

### Installation

```bash
# Clone the optimized FastAPI server
git clone https://github.com/pasky/Qwen3-TTS-Openai-Fastapi
cd Qwen3-TTS-Openai-Fastapi

# Create venv with Python 3.12 (critical!)
uv venv --python 3.12

# Sync dependencies
uv sync

# Install CUDA PyTorch — MUST use --extra-index-url
# NOTE: --extra-index-url (not --index-url) so uv can find non-torch deps on PyPI
uv pip install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu124
```

> **`--extra-index-url` vs `--index-url`:** Using `--index-url` replaces the default PyPI index entirely, which breaks resolution of non-PyTorch dependencies. Use `--extra-index-url` to add PyTorch's index as a secondary source.

### Verify CUDA

```bash
uv run python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Version:', torch.__version__)"
# Expected: CUDA: True, Version: 2.6.0+cu124 (or similar +cu*)
```

If it says `False` with `+cpu` suffix, the venv is using Python 3.13 or `--extra-index-url` didn't take. Recreate with `--python 3.12`.

### Voice Cloning

**Step 1: Prepare reference audio**

Grab a 5-15 second clean audio clip of the target voice speaking clearly. Best sources:
- Podcast interviews (clean studio audio, single speaker)
- LibriVox public domain audiobooks
- YouTube interview clips (cut with Audacity)

**Step 2: Transcribe the clip**

Use Whisper or have the agent transcribe it. The transcript MUST match the audio exactly for best clone quality.

**Step 3: Create the clone prompt**

Save this as a script (e.g. `clone_voice.py`) in the repo folder:

```python
from qwen_tts import Qwen3TTSModel
import torch, pickle

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

prompt = model.create_voice_clone_prompt(
    ref_audio="reference_clip.wav",
    ref_text="Exact transcript of what's said in the audio."
)

with open("my_voice.pkl", "wb") as f:
    pickle.dump(prompt, f)
print("Voice prompt saved!")
```

```bash
uv run python clone_voice.py
```

This downloads the ~3.4GB model on first run (takes a minute), then creates the `.pkl` prompt file.

**Step 4: Start the server**

```bash
# Windows PowerShell
$env:ENABLE_VOICE_STUDIO="true"
$env:CUSTOM_VOICE="my_voice.pkl"
uv run python -m api.main

# Linux
ENABLE_VOICE_STUDIO=true CUSTOM_VOICE=./my_voice.pkl uv run python -m api.main
```

The server starts on `http://0.0.0.0:8880`. The web UI is at `http://localhost:8880`, Voice Studio at `http://localhost:8880/voice-studio`.

**Step 5: Verify TTS**

```bash
curl -X POST http://localhost:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, this is a test of the cloned voice.", "voice": "alloy", "model": "qwen3-tts"}' \
  --output test.mp3
```

## Hermes TTS Configuration

### Pointing at a Local Qwen3-TTS / LM Studio Server

```bash
# Set the TTS provider to OpenAI-compatible with custom base_url
hermes config set tts.provider "openai"
hermes config set tts.openai.base_url "http://<server-ip>:8880/v1"
hermes config set tts.openai.model "qwen3-tts"
hermes config set tts.openai.api_key "not-needed"
```

For a LAN server (laptop running Qwen3-TTS, VM running Hermes), use the laptop's LAN IP:
```yaml
# In ~/.hermes/profiles/<name>/config.yaml:
tts:
  provider: openai
  openai:
    base_url: http://192.168.0.34:8880/v1
    model: qwen3-tts
    api_key: not-needed
```

### Verification

```bash
# Quick test — generates an audio file
hermes tts "Hello, this is a test of my new voice." --output test_output.mp3
```

Or use the `text_to_speech` tool from within a conversation.

## Platform-Specific Issues

### Windows + PowerShell

- **`.venv` paths**: PowerShell tries to load `.venv` as a module. Use full path:
  ```powershell
  C:\Users\Name\Project\.venv\Scripts\python -c "import torch; ..."
  ```
  NOT:
  ```powershell
  .venv\Scripts\python -c "..."  # ❌ PowerShell module load error
  ```
- For PowerShell quoting tricks, CUDA Python version traps, and `uv` cache issues, see `references/windows-troubleshooting.md`.

### Linux

- The official backend auto-detects GPU. No special config needed.
- For CPU-only: `TTS_BACKEND=pytorch TTS_DEVICE=cpu`

## Troubleshooting

### Windows + CUDA + uv: Complete Failure Chain (July 2026)

This is the most common blocker on Windows laptops with RTX GPUs. Follow this exact sequence:

**Symptom:** `AssertionError: Torch not compiled with CUDA enabled`

**Root cause:** The venv is using CPU-only PyTorch, usually because:
1. **Python 3.13** — PyTorch CUDA wheels don't exist for 3.13 yet. `uv` will silently install CPU-only and pretend it worked.
2. **`--index-url` instead of `--extra-index-url`** — using `--index-url` replaces PyPI entirely, so `uv` can't resolve non-torch deps and falls back to CPU.
3. **`uv` cache staleness** — `uv cache clean` alone doesn't fix stale resolution; you need `--force-reinstall`.

**Fix sequence:**
```powershell
# 1. Recreate venv with Python 3.12
uv venv --python 3.12
# (Say 'y' when it asks to replace existing)

# 2. Clean uv cache (optional but recommended)
uv cache clean

# 3. Force-reinstall CUDA PyTorch with --extra-index-url (NOT --index-url)
uv pip install --force-reinstall torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu124

# 4. Verify — use full path (NOT .venv\Scripts\python which PowerShell misinterprets)
C:\Users\Name\Project\.venv\Scripts\python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Version:', torch.__version__)"
# Expected: CUDA: True, Version: 2.6.0+cu124 (or similar +cu*)
```

**PowerShell gotchas:**
- `.\venv\Scripts\pip` → "not found" (PowerShell sees `.` as module prefix)
- `.venv\Scripts\python -m pip` → ".venv could not be loaded" (same reason)
- **Fix:** use full path: `C:\Users\Name\Project\.venv\Scripts\python -c "..."`
- Or use `uv run python -c "..."` (uv handles the venv internally)

### ElevenLabs Voice Settings Patch (Hermes Core, July 2026)

Hermes' `_generate_elevenlabs()` in `tools/tts_tool.py` was patched to pass `voice_settings` to the ElevenLabs API, enabling `stability`, `similarity_boost`, `style`, and `use_speaker_boost` config keys.

**The patch:** Added a `voice_settings` dict built from `el_config` values (defaults: stability=0.35, similarity_boost=0.75, style=0.5, speaker_boost=True) and passed it as a kwarg to `client.text_to_speech.convert()`.

**To verify it's installed:** grep for `voice_settings` in `~/.hermes/hermes-agent/tools/tts_tool.py` around line 996.

**If the patch is missing** (e.g., after a Hermes update), see `references/elevenlabs-voice-settings-patch.md` for the exact diff.

| Symptom | Likely Cause | Fix |
|---|---|---|
| `Torch not compiled with CUDA enabled` | CPU-only PyTorch installed | Use `--extra-index-url https://download.pytorch.org/whl/cu124` and verify Python ≤3.12 |
| `uv pip install` shows `Checked 2 packages in 7ms` | Cached resolution, no-op | `uv cache clean` then `--force-reinstall` |
| `torch.__version__` shows `+cpu` after installing `+cu124` | Python 3.13+ incompatibility | Recreate venv: `uv venv --python 3.12` then reinstall |
| Server starts but TTS returns gibberish | Model not fully downloaded | Check `~/.cache/huggingface/` for partial downloads |
| Voice studio loads but cloning fails | Reference audio too long or wrong format | Use 5-15s WAV/MP3, clean single-speaker audio |
| Hermes TTS returns error | Wrong port or IP | Test with curl first, verify `base_url` ends in `/v1` |
| Windows: `.venv` not recognized as cmdlet | PowerShell interprets leading dot as module | Use full absolute path: `C:\\...\\.venv\\Scripts\\python` |
| `uv run` shows different torch version than just installed | uv cache or lockfile | `uv cache clean` + `--force-reinstall`, or recreate venv |
| Inline Python with `-c` breaks on apostrophes | PowerShell quoting conflict | Use `@'...'@` here-string or save as .py file (see `references/windows-troubleshooting.md`)

## References

- [Qwen3-TTS GitHub (pasky fork)](https://github.com/pasky/Qwen3-TTS-Openai-Fastapi)
- [Qwen3-TTS Original (QwenLM)](https://github.com/QwenLM/Qwen3-TTS)
- [Official Qwen3-TTS Paper](https://arxiv.org/abs/2601.15621)
- `devops/profile-identity-bootstrap` — profile setup that pairs with TTS identity work