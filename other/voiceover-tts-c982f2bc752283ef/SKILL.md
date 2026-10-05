---
name: voiceover-tts
description: Debug and troubleshoot ettametta's voiceover/TTS system — Fish Speech, ElevenLabs fallback, audio mixing, and the voice-to-video pipeline. Use when voiceover generation fails, audio quality degrades, or mixing produces silence.
---
# Voiceover & TTS Debugging

Three-tier TTS: Fish Speech (local) → ElevenLabs (cloud) → gTTS (free fallback). Voiceover output feeds into Nexus audio mixing.

## Quick Diagnostics

```bash
# Voiceover service health
docker compose exec -T api curl -s http://voiceover:8080/health 2>&1

# Check voice engine setting
docker compose exec api python3 -c "from src.api.config import settings; print('ENGINE:', settings.VOICE_ENGINE); print('FISH_EP:', settings.FISH_SPEECH_ENDPOINT)"

# Test TTS generation
curl -X POST http://localhost:8000/api/v1/no-face/synthesize-audio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice_id": "default"}'

# Check voiceover container logs
docker compose logs --tail=50 voiceover

# Check ElevenLabs key
docker compose exec api python3 -c "from src.api.config import settings; print('ELEVENLABS:', 'SET' if settings.ELEVENLABS_API_KEY else 'MISSING')"
```

## Architecture

### Three-Tier Fallback Chain (`src/services/voiceover/service.py`)

```
Fish Speech (local, CPU)
  → on failure: ElevenLabs (cloud, API key required)
    → on failure: gTTS (free, Google Translate TTS)
```

Each tier has:
- Circuit breaker (threshold: 3, recovery: 300s)
- Tenacity retry (3 attempts, exponential backoff 1-4s)

### Fish Speech Setup

- Model: `fishaudio/fish-speech-1.5` from HuggingFace
- Downloaded at container startup via `download_models.py`
- Runs on CPU (`DEVICE=cpu` in Dockerfile)
- Endpoint: `http://voiceover:8080` (Docker internal)

### Audio Mixing (`src/services/nexus_engine/audio_mixer.py`)

`AudioMixer.mix_tracks(voiceover_path, music_path, duration, voice_vol=1.0, music_vol=0.1)`
- FFmpeg-based two-track mix
- Music ducked to 10% during voiceover

### Voice Stitching (`src/services/nexus_engine/orchestrator.py`)

`_stitch_voiceovers()` (line 445) concatenates multiple voiceover clips via FFmpeg into a master MP3.

### Key Files

| File | Purpose |
|------|---------|
| `src/services/voiceover/service.py` | `VoiceoverService` — three-tier fallback, circuit breakers |
| `src/services/voiceover/main.py` | FastAPI microservice — `/health`, `/generate` on port 8080 |
| `src/services/voiceover/download_models.py` | HuggingFace model download at startup |
| `src/services/voiceover/requirements.txt` | PyTorch (CPU), numpy, scipy, soundfile, librosa |
| `src/services/nexus_engine/audio_mixer.py` | FFmpeg two-track mixing with ducking |
| `src/services/nexus_engine/orchestrator.py` | `_stitch_voiceovers()` — clip concatenation |
| `src/services/nexus_engine/auto_creator.py` | `_generate_voiceovers()` — per-segment TTS |
| `src/services/nexus_engine/dag_nodes.py` | `AudioMixNode` — voiceover + music mixing |
| `src/api/routes/no_face.py` | `POST /no-face/synthesize-audio` endpoint |
| `infra/docker/voiceover.Dockerfile` | Fish Speech container definition |

## Configuration

| Setting | Default | Purpose |
|---------|---------|---------|
| `VOICE_ENGINE` | `fish_speech` | Engine: `fish_speech` or `elevenlabs` |
| `FISH_SPEECH_ENDPOINT` | `http://voiceover:8080` | Fish Speech service URL |
| `ELEVENLABS_API_KEY` | — | ElevenLabs API key (vault fallback) |
| `VOICEOVER_TIMEOUT` | 30 | Seconds before TTS times out |
| `RENDER_NODE_URL` | — | Override Fish endpoint for remote GPU |

## Common Issues

### Voiceover service not responding
```bash
docker compose ps voiceover
docker compose exec -T api curl -s http://voiceover:8080/health
```
If container is running but unresponsive, model download may have failed:
```bash
docker compose logs voiceover | grep -i "download\|model\|error"
```

### Fish Speech returns garbage audio
Model may be corrupted. Force re-download:
```bash
docker compose exec voiceover rm -rf /app/models/fish-speech-1.5
docker compose restart voiceover
```

### ElevenLabs 429 rate limit
Circuit breaker opens after 3 failures. Wait 300s or reset:
```bash
docker compose logs api | grep -i "elevenlabs\|circuit.*open"
```

### gTTS quality too low
gTTS is the last-resort fallback. It produces robotic speech. Fix the upstream issue (Fish Speech or ElevenLabs) to avoid falling through to gTTS.

### Audio mix produces silence
Check if voiceover file exists and is non-zero:
```bash
ls -la outputs/*voiceover* 2>/dev/null
```
Check FFmpeg availability:
```bash
docker compose exec api which ffmpeg
```

### Voice file 404 during Remotion render
Known bug: silent staging failure + path mangling + inconsistent types. Bypassed by running single-voiceover renders. See team memory `remotion-voice-file-404.md`.

### Timeout on long scripts
Default `VOICEOVER_TIMEOUT` is 30s. For long segments, increase:
```bash
# In .env
VOICEOVER_TIMEOUT=60
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/no-face/synthesize-audio` | POST | User | Generate voiceover from text |
| `/health` (voiceover service) | GET | None | Microservice health check |
| `/generate` (voiceover service) | POST | Internal | Direct TTS generation |

## ElevenLabs Voices

Default voice: `21m00Tcm4TlvDq8ikWAM` (Rachel). Style library maps voices in `style_library.py`:
- Each style has a `voice_id` field
- Nexus auto_creator uses the style's voice_id for TTS

## Debugging Checklist

1. Voiceover service up? `curl http://voiceover:8080/health`
2. Voice engine setting: `settings.VOICE_ENGINE`
3. Fish Speech model downloaded? `ls /app/models/fish-speech-1.5/`
4. ElevenLabs key set? `settings.ELEVENLABS_API_KEY`
5. FFmpeg available? `which ffmpeg`
6. Output files exist? `ls -la outputs/*voiceover*`
7. Circuit breakers open? `docker compose logs api | grep circuit`
8. Timeout: `VOICEOVER_TIMEOUT` setting
