---
name: nexus-engine
description: Debug and troubleshoot ettametta's Nexus Engine — the autonomous video production pipeline. Use when investigating compose failures, script generation issues, asset sourcing problems, Remotion render errors, DAG execution failures, style/blueprint issues, or job state machine problems.
---
# Nexus Engine Debug Skill

The Nexus Engine is ettametta's autonomous video production pipeline. It orchestrates LLM script generation, asset sourcing, Remotion rendering, and output delivery through a DAG-based execution model.

## Quick Diagnostics

```bash
# Check Nexus job status
docker compose exec -T db psql -U your_postgres_user_here -d ettametta -c "SELECT id, status, progress, niche, error_log FROM nexus_jobs ORDER BY created_at DESC LIMIT 10;"

# Check Nexus Celery task
docker compose exec -T celery_worker celery -A src.api.utils.celery inspect active | grep -A5 nexus

# Check Remotion service health
docker compose exec -T api curl -s http://localhost:8000/api/v1/nexus/health 2>&1

# Check WebSocket connections
docker compose exec -T api curl -s http://localhost:8000/api/v1/ws/health 2>&1

# Check Nexus-related errors in logs
docker compose logs --tail=100 api 2>&1 | grep -i "nexus\|remotion\|blueprint\|dag" | grep -i "error\|fail\|exception"
docker compose logs --tail=100 celery_worker 2>&1 | grep -i "nexus\|remotion\|blueprint" | grep -i "error\|fail"

# Check Remotion studio
docker compose exec -T api curl -s -o /dev/null -w '%{http_code}' http://remotion-studio:3000 2>&1

# Check available blueprints
docker compose exec -T api curl -s http://localhost:8000/api/v1/nexus/blueprints 2>&1 | head -50

# Check style library
python3 -c "from src.services.nexus_engine.style_library import STYLE_DEFINITIONS; print(f'{len(STYLE_DEFINITIONS)} styles available'); [print(f'  {k}') for k in sorted(STYLE_DEFINITIONS.keys())]"
```

## Architecture

### Data Flow
```
POST /nexus/compose
  → NexusOrchestrator.compose()
    → AutoCreator.generate_viral_script()  [LLM]
    → DAG execution:
      → ParallelAssetSourceNode            [stock/platform search]
      → VideoDownloadNode                  [download clips]
      → VisionAuditNode                    [LLM vision check]
      → ColorGradeNode                     [LUT grading]
      → AudioMixNode                       [voiceover + music]
      → SceneRenderNode                    [Remotion render]
    → Output video
    → WebSocket progress notifications
```

### Three Automation Modes
| Mode | Description |
|------|-------------|
| `manual` | User provides all assets, Nexus assembles |
| `partial` | AI generates DAG + scripts, user approves before execution |
| `full` | End-to-end AI-driven video compilation |

### 25+ Video Styles
Defined in `style_library.py`. Each style has:
- `name` / `description` / `prompt_modifier` — guides LLM script generation
- `visual_keywords` — for stock footage search
- `music_keywords` — for audio sourcing
- `voice_id` — ElevenLabs voice mapping
- `remotion_flags` — composition layout flags

Key styles: `CINEMATIC_DOC`, `VOX_EXPLAINER`, `DEEP_DIVE`, `REDDIT_STORY`, `FAST_HYPE`, `NOIR_MYSTERY`, `BROADCAST_NEWS`, `TOP_LISTICLE`, `MOTIVATIONAL`, `REACTION_COMMENTARY`

## Key Files

| File | Purpose |
|------|---------|
| `src/services/nexus_engine/orchestrator.py` | Main orchestrator — Remotion render, vibe analysis, input validation |
| `src/services/nexus_engine/auto_creator.py` | Autonomous video creation — LLM script generation, DAG assembly |
| `src/services/nexus_engine/dag_nodes.py` | DAG node implementations — stock search, download, audit, render |
| `src/services/nexus_engine/blueprints.py` | Blueprint execution engine, node handler registry |
| `src/services/nexus_engine/style_library.py` | 25+ style definitions with prompts and visual configs |
| `src/services/nexus_engine/tasks.py` | Celery task wrapper for `nexus.create_cinema_video` |
| `src/services/nexus_engine/audio_mixer.py` | Voiceover + music mixing with ducking |
| `src/services/nexus_engine/thumbnail_service.py` | Thumbnail generation for completed videos |
| `src/api/routes/nexus.py` | REST API — compose, status, blueprints, jobs |
| `src/api/utils/models.py` | `NexusJobDB`, `BlueprintDB` models |
| `src/shared/state_machine.py` | Job state transitions (COGNITION → SYNTHESIZING → COMPLETE) |
| `src/shared/enums.py` | `NodeStatus`, `SystemJobStatus` enums |

## Common Issues

### 1. Remotion Render Timeout
**Symptoms:** Job stuck at SYNTHESIZING, circuit breaker opens
**Root Cause:** Render exceeds `LLM_TIMEOUT * 60` seconds (default 3600s)
**Debug:**
```bash
docker compose logs --tail=200 api 2>&1 | grep -i "remotion.*timeout\|circuit.*open\|render.*fail"
```
**Fix:** Check `MAX_RENDER_FRAMES` (default 300), reduce video duration, or increase timeout

### 2. Script Generation Returns Empty
**Symptoms:** Job fails at COGNITION stage, "Script generation returned no segments"
**Root Cause:** LLM returns unparseable JSON or empty segments
**Debug:**
```bash
docker compose logs --tail=200 celery_worker 2>&1 | grep -i "script.*generation\|auto_creator\|intelligence_hub"
```
**Fix:** Check LLM provider health, verify API keys, check style prompt_modifier

### 3. Asset Sourcing Fails (Stock Videos)
**Symptoms:** No clips found, job fails at asset sourcing
**Root Cause:** Pexels API key missing, stock search returns empty
**Debug:**
```bash
docker compose exec -T api python3 -c "from src.api.config import settings; print('PEXELS:', 'SET' if settings.PEXELS_API_KEY else 'MISSING')"
docker compose logs --tail=100 celery_worker 2>&1 | grep -i "stock\|pexels\|asset.*search"
```

### 4. WebSocket Notifications Not Delivered
**Symptoms:** Frontend shows stale job progress
**Root Cause:** Redis pub/sub issue or WS connection dropped
**Debug:**
```bash
docker compose exec -T redis redis-cli -a your_redis_password_here psubscribe 'nexus:*' 2>&1 | head -5
docker compose logs --tail=50 api 2>&1 | grep -i "websocket\|ws.*error"
```

### 5. Dify/LangChain Vibe Analysis Fails
**Symptoms:** Logs show "Dify analysis failed, falling back" or "LangChain not enabled"
**Root Cause:** Missing API key or service down
**Debug:**
```bash
docker compose exec -T api python3 -c "from src.api.config import settings; print('DIFY_API_KEY:', 'SET' if settings.DIFY_API_KEY else 'MISSING')"
docker compose logs --tail=50 api 2>&1 | grep -i "dify\|langchain\|vibe"
```

### 6. Blueprint Execution Fails
**Symptoms:** "No handler registered for node type: X"
**Root Cause:** Missing node handler registration in blueprints.py
**Debug:**
```bash
docker compose exec -T api python3 -c "
from src.services.nexus_engine.blueprints import registry
print('Registered handlers:', list(registry._handlers.keys()))
"
```

### 7. Job State Machine Stuck
**Symptoms:** Job never transitions to COMPLETE
**Root Cause:** State machine transition fails silently
**Debug:**
```bash
docker compose exec -T db psql -U your_postgres_user_here -d ettametta -c "SELECT id, status, progress, error_log FROM nexus_jobs WHERE status NOT IN ('COMPLETED', 'FAILED') ORDER BY created_at DESC LIMIT 5;"
```

## Job States

```
QUEUED → COGNITION → SYNTHESIZING → COMPLETE
                ↓           ↓
             FAILED      FAILED
```

- `COGNITION`: Script generation + vibe analysis
- `SYNTHESIZING`: Asset sourcing + Remotion rendering
- Node statuses: `PENDING`, `ACTIVE`, `COMPLETED`, `FAILED`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/nexus/compose` | POST | Start video composition |
| `/nexus/jobs` | GET | List user's nexus jobs |
| `/nexus/jobs/{id}` | GET | Get job status + progress |
| `/nexus/jobs/{id}/cancel` | POST | Cancel running job |
| `/nexus/blueprints` | GET | List available blueprints |
| `/nexus/blueprints/{id}` | GET | Get blueprint details |
| `/nexus/styles` | GET | List available styles |
| `/nexus/auto-create` | POST | Full-auto video creation |

## Circuit Breakers

The Nexus engine uses circuit breakers for:
- `NexusRemotion` — Remotion render failures (threshold: 3, recovery: 300s)
- `AutoCreator-Pipeline` — Pipeline failures (threshold: 3, recovery: 300s)

Check circuit breaker state:
```bash
docker compose logs --tail=500 api 2>&1 | grep -i "circuit.*open\|breaker.*open"
```

## Dependencies

| Dependency | Required | Impact if Missing |
|------------|----------|-------------------|
| Remotion Studio | Yes | No video rendering |
| MoviePy | Optional | Video processing disabled |
| OpenCV | Yes | Frame counting fails |
| Pexels API | Yes | No stock footage |
| ElevenLabs | Yes | No voiceover |
| Dify | Optional | Vibe analysis falls back to LangChain |
| LangChain | Optional | Vibe analysis disabled |
