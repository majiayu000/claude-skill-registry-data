---
name: restart-taigi
description: 重啟 Taigi / Breeze ASR 26 即時語音辨識與翻譯服務。當使用者說「重啟 taigi / 台語服務 / Breeze ASR / 翻譯服務」、Discord 回報網頁能開但 Start Listening 連不上、WebSocket connection refused、ASR 沒反應、TTS/翻譯卡住、換了 TTS 聲音/ref.wav 之後、或 /restart-taigi 時使用。會重啟 host 上的 Breeze ASR 後端 supervisor、確認/必要時重啟 MERaLiON OmniVoice TTS（ref.wav 比服務新會自動強制重啟）、重啟 frontend + Tailscale sidecar，最後驗證 health、公開 URL、WebSocket。
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [taigi, breeze-asr, asr, translation, tts, tailscale, docker, restart, discord]
---

# Restart Taigi / Breeze ASR Streaming

Use when the Taigi realtime ASR/translation web app needs restarting — page opens but
microphone/WebSocket does not connect, ASR stops responding, translation/TTS appears stuck, or the
user says `/restart-taigi`,「重啟 taigi / 台語服務 / Breeze ASR」.

## Just run it

```bash
bash ~/.hermes/skills/restart-taigi/scripts/restart.sh
```

Options:

```bash
bash ~/.hermes/skills/restart-taigi/scripts/restart.sh --tts      # force-restart MERaLiON/OmniVoice too
bash ~/.hermes/skills/restart-taigi/scripts/restart.sh --rebuild  # rebuild frontend, then force-recreate Tailscale sidecar
bash ~/.hermes/skills/restart-taigi/scripts/restart.sh --no-ui    # backend/TTS only; skip frontend/Tailscale
```

Report the final health lines **and the `MIOpen mode` line** to the user. If the script says `Done`, tell the user to reload
`https://taigi.crayfish-monitor.ts.net/` and try again. Production requires `MIOPEN_FIND_MODE=FAST`; a mode mismatch makes the script exit unhealthy even if the TTS health endpoint responds.

## Live architecture

| Piece | What | Managed by |
| --- | --- | --- |
| Breeze ASR backend | FastAPI + WebSocket on host `:8025`; Breeze ASR for Taigi, Whisper Turbo for non-Taigi, Gemma translation routing | `systemctl --user breeze-asr.service` (drop-in `Wants=ollama.service meralion-tts.service`) |
| Ollama (translation) | Local `gemma4:e2b` on host `:11434` | `systemctl --user ollama.service` (pulled in by breeze-asr) |
| MERaLiON/OmniVoice TTS | Local non-Taigi TTS on host `:8026`, default speaker/ref audio | `systemctl --user meralion-tts.service` (pulled in by breeze-asr) |
| Frontend | Nginx static web client on Docker `:8080` | `~/src/breeze-asr-streaming/docker-compose.yml` service `frontend` |
| Tailscale sidecar | Serves `https://taigi.crayfish-monitor.ts.net/` and `/ws/stream` → host backend | Docker service `tailscale` sharing frontend netns |

The backend can crash from fatal ROCm/HIP C++ exceptions (`HSA_STATUS_ERROR_EXCEPTION`,
`unspecified launch failure`). `breeze-asr.service` (`Restart=on-failure`) supervises uvicorn and
restarts automatically, but this skill forcibly cycles the stack and verifies it end-to-end.

## What the script does

1. Restarts the Breeze ASR backend via `systemctl --user restart breeze-asr.service`, which — via its
   drop-in `Wants=ollama.service meralion-tts.service` — also brings the local translation model and
   TTS up. (The retired `./stop.sh && ./start-bg.sh` manual supervisor double-booked `:8025` and is no
   longer used.)
2. Waits for `http://127.0.0.1:8025/health`.
3. Checks MERaLiON/OmniVoice `http://127.0.0.1:8026/health`; restarts it if unhealthy, if `--tts` is
   passed, **if `~/src/taigi-id-translator/samples/ref.wav` is newer than the running service**, **or
   if a real synthesis probe fails.** `/health` only confirms the model *loaded*, NOT that it can
   synthesize: a prior GPU launch fault can corrupt the process's HIP context so `/health` stays green
   while every `/synthesize` returns HTTP 500 (`CUDA error: unspecified launch failure`). So the script
   actually POSTs a tiny phrase to `/synthesize` (`language:nan`, `num_step:6`) and requires a `200` +
   RIFF/WAV body; on failure it force-restarts TTS and **re-probes after restart** (a still-failing
   synthesis marks the run unhealthy). The default speaker prompt is pre-loaded ONCE at TTS startup
   (`DEFAULT_VOICE_PROMPT_BASE` in `meralion_server.py`), so after replacing `ref.wav` a "healthy" TTS
   still speaks with the OLD voice — the mtime check catches that automatically. It then reads the
   running `meralion-tts.service` process environment and requires `MIOPEN_FIND_MODE=FAST`, matching
   the production low-latency policy used by the project and `/taigi-speak`.
4. Restarts Docker frontend + Tailscale sidecar. With `--rebuild`, it runs the safe deploy flow:
   `docker compose up -d --build frontend` then `docker compose up -d --force-recreate tailscale`.
   This matters because the Tailscale sidecar uses `network_mode: service:frontend`; any frontend
   recreate invalidates the old sidecar network namespace.
5. Verifies local frontend, public URL, public WebSocket, container states, and Tailscale node status.

The frontend's WebSocket `onclose` path calls `stopListening()`, which must call
`resetTranslationPlayback()` before reconnecting. This stops active playback, empties the FIFO,
and revokes old audio object URLs whenever the backend service restarts. **Never remove this cleanup:**
old TTS audio must not survive a service restart.

## Correct deploy flows

### Backend-only code change or ASR/translation crash

```bash
bash ~/.hermes/skills/restart-taigi/scripts/restart.sh --no-ui
```

This runs `systemctl --user restart breeze-asr.service`. The unit is `Type=simple` (start.sh `exec`s
uvicorn) with `Restart=on-failure`, so systemd is the sole supervisor and cleans up the old process on
restart — no stale ROCm/uvicorn sharing the GPU/port. Its drop-in
(`~/.config/systemd/user/breeze-asr.service.d/deps.conf`) `Wants` ollama + TTS, so they come up too.

Manual equivalent:

```bash
systemctl --user restart breeze-asr.service        # also pulls up ollama + meralion-tts
systemctl --user is-active ollama.service meralion-tts.service breeze-asr.service
curl http://127.0.0.1:8025/health
```

### Frontend/UI code change

```bash
bash ~/.hermes/skills/restart-taigi/scripts/restart.sh --rebuild
```

Manual equivalent if the skill is unavailable:

```bash
cd ~/src/breeze-asr-streaming
docker compose up -d --build frontend
docker compose up -d --force-recreate tailscale
curl -s -o /dev/null -w '%{http_code}\n' https://taigi.crayfish-monitor.ts.net/
```

Do **not** rely on plain `docker restart breeze-asr-tailscale-taigi` after a frontend rebuild; the
sidecar may still point at the deleted frontend network namespace.

## Troubleshooting notes

- If frontend works but WebSocket fails with `connection refused`, the backend on `:8025` is down or
  still loading. Check `~/models-work/breeze-asr-26/logs/server.log` and run `pgrep -af 'uvicorn app.server:app.*8025'`.
- If TTS fails but ASR/translation text works, check `systemctl --user status meralion-tts.service`
  and `curl http://127.0.0.1:8026/health`.
- Do **not** use system/default Python for Breeze/Whisper; use the ROCm 7.2 venv wired by
  `~/models-work/breeze-asr-26/start.sh`.
- Frontend code changes need `--rebuild`; normal outage recovery usually does not.
- If there are multiple backend PIDs, something started the retired `./start-bg.sh` alongside systemd — `cd ~/models-work/breeze-asr-26 && ./stop.sh`, then `systemctl --user restart breeze-asr.service` so systemd is the only supervisor.
