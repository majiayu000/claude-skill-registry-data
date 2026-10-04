---
name: demo-play
description: >
  Drive LibrAgent desktop chrome for product/hero demos via App Control MCP
  (POST /mcp/control) and optional session HTTP APIs. Use when filming README
  hero clips, pacing Extensions install → chat → deliverable, remote UI
  automation for demos, or when asked to demo-play / run hero shot list /
  app-control demo. Not for registering MCP servers into an agent session
  (use tool-installer) and not for window screenshots (use app-screenshot).
---

# Demo Play

Compose **generic** App Control primitives into timed demo beats. There is no
`demo__run_hero` server tool — sequences live in this skill / scripts.

## Preconditions

1. Prefer **demo profile** (isolated DB + env-seeded LLM):
   - `scripts/run-demo.sh` or `libragent --demo --mcp --app-control`
   - Loads `.env.demo` (`LIBRAGENT_LLM_*` OpenAI-compat endpoint)
2. Or open any build with **both**:
   - `--mcp` / `LIBRAGENT_MCP_ENABLE=1`
   - `--app-control` / `LIBRAGENT_APP_CONTROL=1`
3. HTTP port: `~/.libragent/http_port` (fallback `3030`).
4. Control endpoint: `http://127.0.0.1:<port>/mcp/control`

If `tools/list` on `/mcp/control` fails, stop and ask the operator to restart
with the flags above. Details: [references/app-control.md](references/app-control.md).

## Core workflow

### 1. Pick the beat

| Intent | Action |
| ------ | ------ |
| Primary hero (Extensions → install → chat) | Run [scripts/play_hero_chrome.sh](scripts/play_hero_chrome.sh) or call primitives below |
| Custom path / highlight only | Call primitives via [scripts/app_control.sh](scripts/app_control.sh) |
| Full product story + prompts | Read [references/hero-shot-list.md](references/hero-shot-list.md) |

### 2. Drive chrome (primitives)

Prefer the helper script (resolves port, posts JSON-RPC):

```bash
bash "<skill-base-dir>/scripts/app_control.sh" app__highlight '{"target":"preset","name":"hn","ms":2500}'
bash "<skill-base-dir>/scripts/app_control.sh" app__wait_ui '{"ms":800}'
bash "<skill-base-dir>/scripts/app_control.sh" app__install_preset '{"name":"hn"}'
```

**Quiet zero-config presets only** (no extra browser/dashboard):
`hn`, `arxiv`, `ddg-search`, `docx`, `yahoo-finance`.

**Do not use for hero chrome:** `serena` (opens a local web dashboard in the
browser and steals focus), key/OAuth presets (`github`, `exa`, …), or anything
that launches a separate GUI.

### 3. Session + deliverable (optional)

After chrome beats:

1. `POST /api/sessions` with `assistantId` (+ optional `workspacePath`, `request`)
2. `app__focus_session` with returned `id`
3. Deliverable prompt from [references/hero-shot-list.md](references/hero-shot-list.md)

Pacing: linger ~2s on Install success; use `app__wait_ui` between steps (500–1500ms).

### 4. Capture

Operator records the window. For stills/pixel capture, hand off to
`@skill:app-screenshot` — this skill does not capture video.

## Rules

- Compose sequences in the client/scripts — do not invent composite MCP tools.
- Prefer one chrome path: Extensions → agent chat. Avoid Settings tours.
- Keep positioning: *Install tools like apps. Keep your model. Keep the file.*
- Idempotent install is OK (already installed → no-op); for filming Install,
  **uninstall a quiet preset first** (or use a clean demo profile). Never switch
  to `serena` just because it was free — its dashboard browser ruins the take.
