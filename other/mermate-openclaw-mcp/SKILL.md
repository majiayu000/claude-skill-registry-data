---
name: mermate-openclaw-mcp
description: Use when the user wants to build, extend, or debug the Python MCP bridge that exposes Mermate actions and stage flows to OpenClaw or other MCP clients.
---

# Mermate OpenClaw MCP

Treat the Express API as the source of truth. The MCP layer should stay thin and map directly onto real routes.

Files to inspect first:

- `mcp_service/server.py`
- `mcp_service/client.py`
- `.mcp.json`
- `server/routes/render.js`
- `server/routes/tla.js`
- `server/routes/ts.js`
- `server/routes/agent.js`
- `server/routes/search.js`
- `server/routes/transcribe.js`

Build rules:

- Keep stage parity with the live pipeline: render -> TLA+ -> TypeScript, plus `agent/run` and `agent/finalize`.
- When a new Mermate route is added, add or update a matching MCP tool instead of inventing a synthetic workflow first.
- Keep HTTP transport logic in `mcp_service/client.py`; keep tool definitions in `mcp_service/server.py`.
- For SSE routes, preserve stage transitions and terminal events. Do not drop `preview_ready`, `final_render`, `done`, or `error`.
- Normalize `markdown` to `md` at the bridge boundary so clients can use human-friendly input while Mermate keeps its native mode values.
- Use resources for stable reference material like the stage map or tool-to-route map.

Expected stage mapping:

- `/api/render` -> `mermate_render`
- `/api/render/tla` -> `mermate_render_tla`
- `/api/render/ts` -> `mermate_render_ts`
- `/api/agent/run` -> `mermate_agent_run`
- `/api/agent/finalize` -> `mermate_agent_finalize`
- `/api/projects/:id/pipeline` -> `mermate_get_project_pipeline`

OpenClaw integration rules:

- Keep the repo-level `.mcp.json` pointing at the repo-local `.venv-mcp/bin/python -m mcp_service` command on this machine.
- Use `MERMATE_URL` for the sidecar base URL; default to `http://127.0.0.1:3333`.
- If the repo moves, update the absolute `command` and `cwd` values in `.mcp.json`.
- Prefer additive tool coverage over changing existing tool names, because wrapper prompts may already depend on them.

Verification:

- `python3 -m unittest test/test_mermate_mcp_service.py`
- `python3 -m compileall mcp_service`
- `PYTHONPATH=/tmp/mermate_mcp_inspect:. python3 -c "from mcp_service.server import mcp; print(mcp.name)"`
