---
name: agent-browser
description: Automate web interactions with agent-browser using Lightpanda by default. Use for navigation, data extraction, form filling, and browser behavior checks; use an explicit Chrome session when rendering or Chrome-only capabilities are required.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["agent-browser","lightpanda"]}}}
---

# Agent Browser

## Activate Lightpanda

On every skill activation, select `--engine lightpanda` and a fresh task-specific `--session` before the first browser command. Repeat the engine and session on **every invocation**, including `snapshot`, actions, `batch`, and `close`. Keep custom `--executable-path` and other launch options consistent across calls. CLI flags override environment and config defaults; a previous session can already own a different engine.

1. Check `agent-browser --version`, `agent-browser --help`, and `lightpanda version`. The CLI must expose `--engine`. For missing binaries or startup failures, read [installation and diagnostics](references/lightpanda.md).
2. Start a fresh Lightpanda session. Replace `task-lp-123` below with a unique name for this task. Inspect `session info --json` and confirm `data.runtime.engine` is `lightpanda` before relying on results. If the installed CLI lacks this diagnostic, inspect its version-matched help and process launch evidence.
3. Navigate, snapshot, act using current refs, and verify the resulting page state. Refresh refs after navigation or DOM changes. Close every session you started on success or failure.

```bash
agent-browser --engine lightpanda --session task-lp-123 open https://example.com
agent-browser --engine lightpanda --session task-lp-123 session info --json
agent-browser --engine lightpanda --session task-lp-123 snapshot -i
# Choose an actual ref from that snapshot before acting:
agent-browser --engine lightpanda --session task-lp-123 click @e1
agent-browser --engine lightpanda --session task-lp-123 snapshot -i
agent-browser --engine lightpanda --session task-lp-123 get text body
agent-browser --engine lightpanda --session task-lp-123 close
```

Treat a missing binary, launch failure, or unsupported operation as a diagnostic branch. Report the failed command and resolve the Lightpanda prerequisite; **never silently retry in Chrome**.

## Choose Chrome for rendering

Lightpanda executes JavaScript and exposes the DOM without graphical rendering. Use a **separate, explicitly selected Chrome session** for screenshots of page appearance, PDF layout, video, visual/layout assertions, coordinate interactions, headed/manual login, Chrome CDP attachment, extensions, persistent profiles, or startup state replay (`--state`). A Lightpanda text/semantic snapshot does not prove appearance. Its markdown-to-image/PDF output is not a rendered webpage.

State the capability requiring Chrome, open the target again, and take new refs in that session. Keep `--engine chrome` on each command in the Chrome workflow. Return to a fresh Lightpanda session for the next activation.

```bash
# Chrome is required here to capture the rendered page.
agent-browser --engine chrome --session task-visual-123 open https://example.com
agent-browser --engine chrome --session task-visual-123 snapshot -i
agent-browser --engine chrome --session task-visual-123 screenshot --full page.png
agent-browser --engine chrome --session task-visual-123 close
```

For an already authenticated Chrome browser, read [authentication](references/authentication.md). Session names isolate running browsers; use explicit state persistence for reuse across restarts.

## Batch independent reads

Batch commands that do not depend on unseen output. Keep snapshot-driven decisions between batches. Use one session per independent site, bounded by available machine capacity.

```bash
agent-browser --engine lightpanda --session task-docs-123 batch --bail "open https://example.com" "get title" "get text body"
agent-browser --engine lightpanda --session task-docs-123 close
```

## References and templates

Load the relevant branch; retain the selected engine and task session throughout:

- [Commands](references/commands.md): command lookup, extraction, and engine-specific capabilities.
- [Snapshots and refs](references/snapshot-refs.md): compact snapshots and ref lifecycle.
- [Sessions](references/session-management.md): isolation, concurrency, persistence, and cleanup.
- [Authentication](references/authentication.md): login, saved state, and manual authentication.
- [Proxy support](references/proxy-support.md): proxy configuration and diagnosis.
- [Video recording](references/video-recording.md): explicit Chrome recording workflow.
- [Form automation](templates/form-automation.sh): Lightpanda snapshot–act–verify template.
- [Authenticated session](templates/authenticated-session.sh): Chrome saved-state replay template.
- [Content capture](templates/capture-workflow.sh): Chrome screenshot/PDF template.

Use `agent-browser skills get core --full` when the installed version provides it, or `<command> --help`, for version-matched syntax. Adapt upstream examples to this skill's engine/session contract before running them.
