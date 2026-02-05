---
name: oe-llm-provider-toggle
description: Switch OpenEvent-AI between OpenAI, Gemini, hybrid, or stub LLM modes via environment variables or the /api/config/llm-provider admin endpoints. Use when Codex/Claude needs to verify or change AGENT_MODE, INTENT/ENTITY/VERBALIZER providers, or OE_LLM_PROFILE settings.
---

# LLM Provider Toggle Playbook

Use this skill to move the stack between OpenAI-only, Gemini-only, hybrid (Gemini extraction + OpenAI verbalization), or stub heuristics. Defaults live in `README.md` (LLM Provider Settings) and `backend/api/routes/config.py`.

## Provider Layers & Defaults

1. **Global adapter (`AGENT_MODE`)** – `backend/adapters/agent_adapter.py` switches between OpenAI, Gemini, and stub adapters. Default comes from `backend/main.py` (`openai`).
2. **Per-operation overrides** – `INTENT_PROVIDER`, `ENTITY_PROVIDER`, `VERBALIZER_PROVIDER` env vars or persisted config rows override `AGENT_MODE`. Hybrid = Gemini intent/entity + OpenAI verbalization (see `LLMProviderConfig`).
3. **Admin runtime config** – `/api/config/llm-provider` GET/POST stores overrides under `db['config']['llm_provider']` in `backend/workflow_email.py`'s JSON DB. When present, DB values beat env vars.
4. **Profiles** – `OE_LLM_PROFILE` selects reasoning chains defined in `configs/llm_profiles.json`. Profiles do not change vendor; combine with provider toggles when you need both.
5. **API keys** – `OPENAI_API_KEY` (required whenever `openai` is active) and `GOOGLE_API_KEY` (required for Gemini). `scripts/dev/oe_env.sh` shows expected setup.

## Quick CLI Recipes

Source `. scripts/dev/oe_env.sh` first so `PYTHONPATH` is set and default keys load. Then pick one of these before starting backend/tests:

### 1. Full OpenAI
```bash
export AGENT_MODE=openai
unset INTENT_PROVIDER ENTITY_PROVIDER VERBALIZER_PROVIDER
uvicorn backend.main:app --reload
```
- Also set `OPENAI_AGENT_MODEL` if you need a specific model (`gpt-4o-mini`, etc.).

### 2. Hybrid (Recommended)
Gemini handles intent/entity, OpenAI verbalizes.
```bash
export AGENT_MODE=gemini          # acts as default + fallback
export INTENT_PROVIDER=gemini
export ENTITY_PROVIDER=gemini
export VERBALIZER_PROVIDER=openai
export GOOGLE_API_KEY="$(security find-generic-password -a "$USER" -s 'openevent-gemini-key' -w 2>/dev/null)"
uvicorn backend.main:app --reload
```
- Hybrid keeps UX quality while cutting 50% cost (`README.md` cost table).

### 3. Full Gemini
```bash
export AGENT_MODE=gemini
export INTENT_PROVIDER=gemini
export ENTITY_PROVIDER=gemini
export VERBALIZER_PROVIDER=gemini
export GOOGLE_API_KEY=...  # must be valid free-tier key
uvicorn backend.main:app --reload
```
- Expect slightly lower verbal quality but ultra-low cost (~$0.007/event).

### 4. Stub / Deterministic
```bash
export AGENT_MODE=stub
unset INTENT_PROVIDER ENTITY_PROVIDER VERBALIZER_PROVIDER
pytest backend/tests/regression -k billing
```
- Stub mode skips LLM calls; used for deterministic regression suites and manual UX scripts (`scripts/manual_ux/`).

### 5. Tests with explicit provider
```bash
AGENT_MODE=gemini GOOGLE_API_KEY=... pytest backend/tests_integration -m integration
AGENT_MODE=openai OPENAI_AGENT_MODEL=gpt-4o-mini pytest backend/tests_integration -m integration
```
- Always pass provider env inline so CI context is unambiguous.

## Runtime Toggle via Admin API/UI

You can flip providers without restarting by talking to `/api/config/llm-provider` (same endpoint the `LLMSettings` React component hits).

1. **Inspect current settings**
```bash
curl -s http://localhost:8000/api/config/llm-provider | jq
# → {"intent_provider":"gemini","entity_provider":"gemini","verbalization_provider":"openai","source":"database"}
```
2. **Update providers**
```bash
curl -s -X POST http://localhost:8000/api/config/llm-provider \
  -H 'Content-Type: application/json' \
  -d '{
        "intent_provider": "gemini",
        "entity_provider": "gemini",
        "verbalization_provider": "openai"
      }'
```
- Valid values: `openai`, `gemini`, `stub`. Backend lowercases and persists to DB, then calls `reset_agent_adapter()` so the next request uses the new providers.
- Equivalent UI flow: open the admin panel (Next.js app) → Settings → "LLM Settings" (component lives at `app/components/LLMSettings.tsx`), pick providers, save.

3. **Revert to env defaults** – remove the DB override so env vars (or `AGENT_MODE`) apply again:
```bash
python - <<'PY'
from backend.workflow_email import load_db, save_db

db = load_db()
if db.get('config', {}).pop('llm_provider', None) is not None:
    save_db(db)
    print('Cleared stored llm_provider config; env vars now take effect.')
else:
    print('No llm_provider config found; nothing to reset.')
PY
```
- Alternatively, delete `backend/events_database.json` entirely if you are okay with wiping state (dev-only).

## Verification Checklist

- `env | grep -E 'AGENT_MODE|INTENT_PROVIDER|ENTITY_PROVIDER|VERBALIZER'` before launches/tests.
- `curl /api/config/llm-provider` → confirm `source` (`database` vs `environment`).
- Backend log `[Config] LLM providers updated...` after POST.
- New Gemini usage requires dependency + key:
  - `pip install -r requirements.txt` ensures `google-generativeai` exists.
  - `python - <<'PY' import google.generativeai as genai; print(genai.__version__)` to double-check.
- When switching from stub → OpenAI/Gemini, restart background workers/tests so they rebuild adapters (or run `from backend.adapters.agent_adapter import reset_agent_adapter; reset_agent_adapter()` in a REPL if hot-swapping).

## Troubleshooting

- **"GOOGLE_API_KEY environment variable is required"** – set the key (see `scripts/dev/oe_env.sh` comments) or export `AGENT_MODE=openai`.
- **Still hitting OpenAI after switching to Gemini** – inspect `/api/config/llm-provider`; if `source` is `database`, DB overrides may still point to `openai`. Clear and reapply.
- **Gemini package missing** – run `pip install google-generativeai>=0.8.0` (already in `requirements.txt`).
- **Need quick rollback** – `export AGENT_MODE=openai` and unset per-operation vars, or post `{ "intent_provider":"openai", "entity_provider":"openai", "verbalization_provider":"openai" }`.
- **CI parity** – Document the exact env snippet you used in PR descriptions or `DEV_CHANGELOG.md` so reviewers know whether a change was tested under OpenAI, Gemini, or hybrid.

## References
- README.md (LLM Provider Settings table, cost comparisons, Gemini free-tier guidance)
- backend/api/routes/config.py (LLMProviderConfig logic + endpoints)
- atelier-ai-frontend/app/components/LLMSettings.tsx (admin UI hitting those endpoints)
- backend/adapters/agent_adapter.py (factory + error messages when env setup is wrong)
- configs/llm_profiles.json (profile names for OE_LLM_PROFILE)
