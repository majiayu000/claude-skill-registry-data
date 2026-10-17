---
name: whisper-stt
description: >
  Whisper STT in-cluster (sin API keys) + pipeline de audio de OpenClaw:
  voice notes de Telegram → transcripción local; respuestas → voz con Edge TTS gratis.
tags: [kubernetes, ai, whisper, stt, tts, openclaw, telegram, arm64, audio]
---

# Whisper STT + Audio en OpenClaw

## Qué hace

Audio bidireccional en el bot de Telegram de OpenClaw, **100% gratis y sin API keys externas**:

- **Entrante (STT):** voice note → OpenClaw la descarga → la manda a `whisper-stt`
  (in-cluster, OpenAI-compatible) → el transcript reemplaza el body del mensaje.
- **Saliente (TTS):** con `auto: "inbound"`, si mandaste audio te responde con audio
  (voice note de Telegram), usando Microsoft Edge neural TTS (`node-edge-tts`, sin key).
  Texto → texto, audio → audio.

## Arquitectura

```
Telegram voice note (OGG/Opus)
  → OpenClaw (tools.media.audio, provider "openai" con baseUrl custom)
  → http://whisper-stt.ai.svc.cluster.local:9000/v1/audio/transcriptions
  → hwdsl2/whisper-server (faster-whisper "small", int8, CPU, pinned a RK1)
  → transcript → agente → respuesta
  → messages.tts (provider "microsoft", es-AR-TomasNeural) → voice note
```

- Role: `roles/install-whisper-stt/` — PVC (cache de modelos, longhorn-nvme) +
  Deployment (strategy Recreate por RWO) + Service ClusterIP. Namespace `ai`.
- Config OpenClaw: bloques `tools.media.audio` y `messages.tts` en
  `roles/install-openclaw/templates/openclaw-configmap.yaml.j2`,
  variables en `roles/install-openclaw/defaults/main.yml`.

## Deploy

```bash
make ai-stt        # solo el servidor Whisper
make openclaw      # whisper-stt + OpenClaw (el tag openclaw incluye install-whisper-stt)
```

Primer arranque: descarga el modelo `small` (~465 MB) de HuggingFace → el
startupProbe espera hasta 10 min. Después queda cacheado en el PVC.

## Variables clave

| Var | Default | Nota |
|---|---|---|
| `whisper_stt_model` | `small` | `base` más rápido / `large-v3-turbo` más preciso (~6 GB RAM) |
| `whisper_stt_language` | `es` | `auto` para autodetectar |
| `whisper_stt_node_hostname` | `srv-rk1-nvme-03` | RK3588 — CPU inference mucho más rápida que CM4 |
| `openclaw_tts_auto` | `inbound` | `always` = todas las respuestas con audio; `off` = apagar |
| `openclaw_tts_voice` | `es-AR-TomasNeural` | `es-AR-ElenaNeural` femenina |

## Verificación

```bash
kubectl get pods -n ai -l app=whisper-stt
kubectl run curl-test --rm -i --restart=Never -n ai --image=curlimages/curl -- \
  curl -s http://whisper-stt.ai.svc.cluster.local:9000/v1/models
# transcripción real:
kubectl run curl-test --rm -i --restart=Never -n ai --image=curlimages/curl -- \
  sh -c 'curl -s http://whisper-stt.ai.svc.cluster.local:9000/v1/audio/transcriptions -F file=@/dev/null -F model=whisper-1; echo'
# en Telegram: /tts status — muestra provider y último intento de TTS
```

## Gotchas

- **baseUrl debe terminar en `/v1`** — OpenClaw (cliente OpenAI) appendea
  `/audio/transcriptions`. El server expone `/v1/audio/transcriptions`.
- **NUNCA pongas `apiKey` dentro de `tools.media.audio.models[]`** — el zod schema
  de OpenClaw es `.strict()` y NO tiene ese campo → invalida el entry completo y el
  gateway NO ARRANCA ("models.0: Invalid input"). Campos válidos: provider, model,
  baseUrl, timeoutSeconds, headers, language, prompt, type(provider|cli).
  Si el server exigiera auth: usar `headers: {"Authorization": "Bearer ..."}`.
  (Causa raíz del crash 2026-06-10, resuelta 2026-06-12 — ver docs/audio-honcho-a2a-2026-06-12.md)
- whisper-stt no exige auth dentro del cluster.
  NO exponer whisper-stt vía HTTPRoute sin `WHISPER_API_KEY`.
- **TTS local (piper) no es posible** con la imagen actual de OpenClaw: el único
  speech provider implementado es `microsoft` (alias `edge`, node-edge-tts, cloud
  gratis, voz es-AR). No hay provider TTS openai/baseUrl. Requiere upgrade de imagen.
- Edge TTS es best-effort (servicio público de Microsoft sin SLA). Si falla,
  alternativa con la key de OpenRouter ya existente: provider `openrouter`,
  modelo `hexgrad/kokoro-82m` en `messages.tts.providers`.
- Voice notes >20 MB se saltean (`maxBytes`). Transcripción de 1 min de audio
  en RK1 con `small` int8 ≈ 10–30 s; el timeout está en 120 s.
- **Hermes también usa whisper-stt**: sin `hermes_groq_api_key`, el ConfigMap
  (`hermes-config-configmap.yaml.j2`) configura `stt.provider: openai` con
  `base_url` → whisper-stt (fix upstream #4102, requiere >= v2026.5.16 — la
  versión pineada). Con key de Groq presente, usa Groq.
- El cliente OpenAI de Hermes tiene timeout hardcoded de 30 s para STT
  (`tools/transcription_tools.py`). Si audios largos dan timeout en Hermes,
  bajar `whisper_stt_model` a `base`. OpenClaw no sufre esto (timeout 120 s configurable).
- El `/sethome` de Hermes no corre mid-turn: esperar a que termine el saludo
  de arranque (o `/stop`) y recién ahí mandarlo. Persiste en el PVC.
