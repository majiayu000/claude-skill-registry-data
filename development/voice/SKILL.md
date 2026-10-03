---
name: voice
description: Transcribe local audio / Discord voice messages with the deployed Breeze ASR 26 HTTP service. Use when the user says /voice, asks to transcribe a voice message/audio file, debug Breeze ASR, test Pi Discord voice integration, or check ASR service health/performance.
version: 1.0.0
author: AyaSakura / Pi Agent
license: MIT
metadata:
  hermes:
    tags: [voice, asr, transcription, breeze-asr, discord, audio, qwen]
---

# Voice Transcription via Breeze ASR 26

This machine has a deployed local ASR service for Discord voice/audio transcription:

- Project: `/home/chihmin/models-work/breeze-asr-26`
- Model: `MediaTek-Research/Breeze-ASR-26`
- Service URL: `http://127.0.0.1:8025`
- systemd user unit: `breeze-asr.service`
- Main endpoints:
  - `GET /health`
  - `POST /transcribe` multipart upload
  - `POST /transcribe_path` local path form field

## Quick Commands

### Check service health

```bash
curl -fsS http://127.0.0.1:8025/health | python3 -m json.tool
systemctl --user --no-pager --plain status breeze-asr.service
```

Expected health fields include:

- `ok: true`
- `model: MediaTek-Research/Breeze-ASR-26`
- `device: cuda` on ROCm
- `dtype: bfloat16`

### Transcribe an audio file by upload

```bash
curl -fsS -F "file=@/path/to/audio.ogg" http://127.0.0.1:8025/transcribe | python3 -m json.tool
```

### Transcribe a local path directly

```bash
curl -fsS -F "path=/path/to/audio.ogg" http://127.0.0.1:8025/transcribe_path | python3 -m json.tool
```

### Use bundled helper script

```bash
~/.pi/agent/skills/voice/scripts/voice-transcribe.sh /path/to/audio.ogg
```

## Service Management

### Start / restart / stop

```bash
systemctl --user start breeze-asr.service
systemctl --user restart breeze-asr.service
systemctl --user stop breeze-asr.service
```

### Logs

```bash
journalctl --user -u breeze-asr.service --since '30 minutes ago' --no-pager | tail -120
```

### Manual project scripts

```bash
/home/chihmin/models-work/breeze-asr-26/start.sh
/home/chihmin/models-work/breeze-asr-26/start-bg.sh
/home/chihmin/models-work/breeze-asr-26/stop.sh
```

Prefer the systemd unit for normal operation.

## Discord / Pi Gateway Integration

Pi Discord gateway source:

- `/home/chihmin/src/pi-discord-gateway`
- Voice ASR helper: `src/discord/voice-asr.ts`
- Invocation integration: `src/agent/invoke.ts`
- Runtime service: `pi-discord-gateway.service`

Current behavior:

1. Discord attachment is downloaded into the channel session media folder.
2. Audio files (`.ogg`, `.opus`, `.wav`, `.mp3`, `.m4a`, `.webm`, `.flac`, `.aac`) are sent to Breeze ASR.
3. The transcription is injected into the prompt as:

   ```text
   [Voice message transcription: voice-message.ogg]
   <transcribed text>
   ```

4. If ASR succeeds, the original audio file is **not** forwarded to Qwen as `@file`, because local Qwen cannot process raw `.ogg` audio and may return an empty response.
5. Non-audio attachments still go to pi as `@file`.

Relevant config in `/home/chihmin/.config/pi-discord-gateway/config.env`:

```dotenv
VOICE_ASR_ENABLED=true
VOICE_ASR_URL=http://127.0.0.1:8025
VOICE_ASR_TIMEOUT_MS=30000
VOICE_ASR_RETRIES=1
VOICE_ASR_RETRY_DELAY_MS=10000
```

After changing gateway code/config:

```bash
cd /home/chihmin/src/pi-discord-gateway
npm test
npm run lint
npm run build
systemctl --user restart pi-discord-gateway.service
```

## Known Good Test Files

Archived Discord voice messages:

```bash
/tmp/pi-discord-files/2026-07-09/mrdlvcscyi49_voice-message.ogg
/tmp/pi-discord-files/2026-07-09/mrdlw2al91tg_voice-message.ogg
/tmp/pi-discord-files/2026-07-09/mrdlxxiwkvev_voice-message.ogg
/tmp/pi-discord-files/2026-07-09/mrdmkhlydlht_voice-message.ogg
/tmp/pi-discord-files/2026-07-09/mrdmmdl162jo_voice-message.ogg
```

Known transcriptions:

- `mrdlvcscyi49_voice-message.ogg` → `你可以試試看這個音檔嗎我現在要開始念一些東西喔`
- `mrdlw2al91tg_voice-message.ogg` → `我是講台語 你們知道我要講什麼`
- `mrdmkhlydlht_voice-message.ogg` → `哈囉你知道我在說什麼東西嗎`
- `mrdmmdl162jo_voice-message.ogg` → `你知道我在做些什麼東西嗎`

## Performance Expectations

Observed on AMD Radeon 8060S / ROCm / bfloat16:

- 2.6s audio → about 1.7s
- 3.16s audio → about 2.6–3.8s
- 4.86s audio → about 2.5s
- 7s audio rough estimate → about 3.5–7s when idle; 7–12s+ if Qwen is busy

Gateway timeout is currently 30 seconds.

## Qwen + Breeze Caveat

Qwen MTP (`qwen-lcpp.service`, port 8001) and Breeze ASR share the same ROCm GPU. Running both is usually possible, but heavy concurrent use can trigger ROCm instability:

```text
ROCm error: unspecified launch failure
hipErrorLaunchFailure
CUDA error: unspecified launch failure
```

If this happens:

```bash
systemctl --user restart breeze-asr.service
systemctl --user restart qwen-lcpp.service
```

Check both services:

```bash
curl -fsS http://127.0.0.1:8025/health | python3 -m json.tool
curl -fsS http://127.0.0.1:8001/v1/models | python3 -m json.tool
```

## Debugging Checklist

1. Is Breeze healthy?

   ```bash
   curl -fsS http://127.0.0.1:8025/health | python3 -m json.tool
   ```

2. Can the file be transcribed manually?

   ```bash
   ~/.pi/agent/skills/voice/scripts/voice-transcribe.sh /path/to/audio.ogg
   ```

3. Did Discord gateway transcribe it?

   ```bash
   journalctl --user -u pi-discord-gateway.service --since '10 minutes ago' --no-pager \
     | grep -Ei 'Transcribed Discord voice|Voice ASR|Attached files|empty response|Agent returned error'
   ```

4. If Qwen returns `(empty response)`, verify the `.ogg` was not forwarded as `@file` after successful transcription. The fix lives in `src/agent/invoke.ts`.

5. If ROCm errors appear, restart affected services and consider lowering concurrent GPU load.
