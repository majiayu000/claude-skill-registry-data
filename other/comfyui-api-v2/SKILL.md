---
name: comfyui-api-v2
description: Operate a user-selected Comfy API v2 endpoint such as comfy-api-proxy using durable jobs, poll-first state, UUID assets, API-format workflow submission, targeted cancellation, safe asset retrieval, optional bearer auth, and idempotent submission practices.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Comfy API v2

## Read

- `../../references/COMFY_API_V2.md`
- `../../references/COMFYUI_SECURITY.md`

## Procedure

1. Confirm the user selected a v2 endpoint or proxy surface.
2. Probe `/api/v2/health` when supported.
3. Submit API-format workflow JSON to `/api/v2/jobs`.
4. Keep the returned job ID.
5. Poll `/api/v2/jobs/{id}` as the source of truth.
6. Use the job's returned output and asset links rather than inventing URL shapes where links are provided.
7. Cancel only the selected job.
8. Keep bearer tokens and partner API keys out of project files and logs.

Bundled command:

```text
python scripts/comfy_api_v2.py health
python scripts/comfy_api_v2.py submit --workflow WORKFLOW.json
python scripts/comfy_api_v2.py wait JOB_ID
python scripts/comfy_api_v2.py cancel JOB_ID
```

## Assets

Use v2 multipart asset upload when v2 asset identity or proxy placement is required. Do not use model upload to place executable content or arbitrary configuration files.

## Done

The job is represented by its durable v2 ID and outputs are followed through server-provided asset records or links.
