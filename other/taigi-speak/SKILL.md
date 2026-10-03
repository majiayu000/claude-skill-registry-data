---
name: taigi-speak
description: Directly convert Taiwanese Hokkien or other languages to speech using the local OmniVoice dual-model server. Trigger when the user requests "/taigi-speak [台詞]" or asks to synthesize Taiwanese lines/phrases.
---

# Taigi Speak & Multi-Language TTS Skill

This skill allows the agent to convert Taiwanese Hokkien (台語), Mandarin (國語), Japanese (日文), English (英文), and other languages directly into synthesized speech audio using the local OmniVoice TTS server.

The server operates on port `8026` and dynamically routes synthesis requests based on the requested language code.

### Default synthesis settings

`/taigi-speak` explicitly sends `num_step: 10`. This is the production low-latency default;
do not omit it or raise it without a deliberate quality/latency decision.

### MIOpen first-request latency policy

The systemd service has the persistent drop-in
`~/.config/systemd/user/meralion-tts.service.d/miopen-fast.conf`, which sets
`MIOPEN_FIND_MODE=FAST`. On a kernel-cache miss it uses MIOpen's immediate-mode fallback
rather than first-request autotuning. Keep it enabled: the restart-to-first-request benchmark
for a medium Indonesian phrase improved 10-step cold latency from **19.933s to 5.339s** and
warm latency from **1.180s to 0.725s** (12/16 steps improved too).

After editing this setting, reload and restart the service, then confirm the running process:
```bash
systemctl --user daemon-reload
systemctl --user restart meralion-tts.service
pid=$(systemctl --user show meralion-tts.service -p MainPID --value)
tr '\0' '\n' </proc/$pid/environ | grep '^MIOPEN_FIND_MODE='
```

Do not substitute `MIOPEN_FIND_ENFORCE` tuning/DB-clean modes without an equivalent cold-and-warm benchmark.

---

## 🛠️ Model Architecture

The backend runs a single instance of the **Original OmniVoice base model** (`k2-fsa/OmniVoice`) for all languages (including Taiwanese/Hokkien `nan`, Mandarin `zh`, Japanese `ja`, and English `en`). This unified setup saves VRAM and uses the original multilingual weights.

---

## 🚀 Running the Server

The OmniVoice/MERaLiON TTS server is run and managed as a standard systemd user service on the host:
* **Start service**: `systemctl --user start meralion-tts.service`
* **Restart service**: `systemctl --user restart meralion-tts.service`
* **Stop service**: `systemctl --user stop meralion-tts.service`
* **Check status**: `systemctl --user status meralion-tts.service`
* **View service logs**: `journalctl --user -u meralion-tts.service -f`
* **Verify API endpoint**: `curl http://localhost:8026/health`

---

## 🎙️ Reference Audio (`ref.wav`) Optimization

The default voice cloning prompt is preloaded from:
`[ref.wav](file:///home/chihmin/src/taigi-id-translator/samples/ref.wav)`

**Current production reference (2026-07-15):** cleaned from the user-approved
YouTube source `https://youtu.be/hKCzB-O5MV8`, original interval **00:32–00:37**.
It is rendered as mono 16 kHz PCM, boundary-silence trimmed, and peak-normalized to
0.95 before becoming `ref.wav`. This is the shared default speaker for all OmniVoice
languages, including `nan`, `zh`, `ja`, `en`, `id`, and `ko`.

### Built-in Speaker Profiles

`/synthesize` accepts a request-local `speaker` field, so no restart is required:
- `default` — the existing `samples/ref.wav` voice (the `/taigi-speak` default).
- `chinese` — `samples/ref_tong.wav`, used automatically for Taiwan Chinese output in the Breeze live translator.

The helper accepts it as its fourth optional argument:
```bash
python3 /home/chihmin/.pi/agent/skills/taigi-speak/scripts/speak.py "你好" "/tmp/chinese.wav" "zh" "chinese"
```

For any other local reference file, pass `--ref-audio`; it uses `/clone` for that request only and does not alter either built-in profile:
```bash
python3 /home/chihmin/.pi/agent/skills/taigi-speak/scripts/speak.py "你好" "/tmp/custom.wav" "zh" --ref-audio "/path/to/ref.wav"
```

### Best Practices for the Reference Audio:
- **Leading/Trailing Silence**: Must be trimmed (less than 100ms). Excessive silence causes the diffusion model to hallucinate prefix words (e.g., `し、` or `はい、` in Japanese).
- **Volume**: Peak amplitude should be normalized to `0.95` to maximize the signal-to-noise ratio for speaker embedding extraction.
- **Purity**: Avoid background music (BGM), breathing noises, sighs, or conversational fillers.
- **Updating the Speaker**:
  1. Overwrite `file:///home/chihmin/src/taigi-id-translator/samples/ref.wav` with a new, cleaned audio file.
  2. Restart the service to apply the change and preload the prompt:
     ```bash
     systemctl --user restart meralion-tts.service
     ```

---

## 💻 Workflow

### 1. Extract the Text and Target Language
Identify the target script and the language from the user's request. Default to `"nan"` (Hokkien) if only Taiwanese Hokkien is implied, or use the appropriate language code for other languages:
- **台語 (Hokkien)**: `nan`
- **國語 (Mandarin)**: `zh` (or `chinese`)
- **日本語 (Japanese)**: `ja` (or `japanese`)
- **English (English)**: `en` (or `english`)

### 2. Execute the speak.py Script
Run the helper script with the target text, output path, and target language code:
```bash
python3 /home/chihmin/.pi/agent/skills/taigi-speak/scripts/speak.py "<文字>" "/home/chihmin/src/taigi-id-translator/taigi_speak.wav" "<語言代碼>"
```

#### Example Commands:
* **Hokkien (台語)**:
  ```bash
  python3 /home/chihmin/.pi/agent/skills/taigi-speak/scripts/speak.py "你好，真歡喜看見你。" "/home/chihmin/src/taigi-id-translator/taigi_speak.wav" "nan"
  ```
* **Mandarin (國語)**:
  ```bash
  python3 /home/chihmin/.pi/agent/skills/taigi-speak/scripts/speak.py "捷運站就在附近，走路大概五分鐘。" "/home/chihmin/src/taigi-id-translator/taigi_speak.wav" "zh"
  ```
* **Japanese (日文)**:
  ```bash
  python3 /home/chihmin/.pi/agent/skills/taigi-speak/scripts/speak.py "こんにちは、これは日本語の音声合成テストです。" "/home/chihmin/src/taigi-id-translator/taigi_speak.wav" "ja"
  ```

### 3. Respond with File Marker
The script will output success details and the LazyGravity attachment marker:
`[[file:/home/chihmin/src/taigi-id-translator/taigi_speak.wav]]`

Include this exact marker in your response so the LazyGravity bot automatically uploads the WAV file to the user's chat.
