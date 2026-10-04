---
name: Qdashboard
user_invocable: true
description: Opens a local read-only dashboard for QE database state. Use when asked to view, inspect, or check the QE DB, dashboard, stored tasks, sessions, plans, verification results, or .qe state.
allowed-tools: "Bash(node:*), Bash(open:*), Bash(xdg-open:*), Bash(cmd.exe:*)"
invocation_trigger: When the user wants an easy visual view of the local QE state database.
recommendedModel: haiku
---

# Qdashboard — Local QE State Dashboard

## Role

Generate a self-contained HTML snapshot of the current project's `.qe/qe.db`
and open it locally. Reuse `scripts/qe-inspector.mjs`; do not implement another
dashboard or query the database with a writable connection. The generated
dashboard automatically detects Korean, English, Japanese, or Simplified
Chinese and lets the user change and retain the language and theme locally.

## Options

| Invocation | Behavior |
|---|---|
| `Qdashboard` | Regenerate `.qe/inspector.html` and open it in the browser |
| `Qdashboard --assistant` | Start a loopback-only dashboard that can query the locally logged-in Claude or Codex |
| `Qdashboard --status` | Print schema, document-count, latest-write, and active-session status without generating or opening HTML |
| `Qdashboard --no-open` | Regenerate the HTML without opening a browser |
| `Qdashboard --path` | Print the absolute dashboard path; do not regenerate or open it |

## Execution Procedure

### Step 1: Preflight

Treat the user's current working directory as the project root. Confirm that
`.qe/qe.db` exists. If it does not, stop and report that no QE store exists for
the current project. Do not create or migrate a database just to render a view.

Resolve the installed inspector in this order:

1. `scripts/qe-inspector.mjs` in a QE Framework source checkout
2. `${CLAUDE_PLUGIN_ROOT}/scripts/qe-inspector.mjs`
3. `${HOME}/.codex/scripts/qe-inspector.mjs`
4. `${HOME}/.claude/scripts/qe-inspector.mjs`

Use the first existing file. Preserve the current working directory when
running it so it reads the current project's `.qe/qe.db`.

### Step 2: Select one mode

- Default: run the inspector with `--out <project>/.qe/inspector.html`, then
  open that file with `open` on macOS, `xdg-open` on Linux, or
  `cmd.exe /c start "" <path>` on Windows.
- `--no-open`: run the same generation command and skip the browser command.
- `--path`: print the absolute `.qe/inspector.html` path and whether it exists.
- `--status`: use the `qe-schema.mjs` and `qe-query.mjs` beside the resolved
  inspector. Run read-only schema status, count `qe_files`, report
  `MAX(mtime_ms)`, and list active sessions. Do not generate HTML.
- `--assistant`: resolve `scripts/qe-dashboard-server.mjs` beside the inspector
  and run it from the project root. It regenerates the same snapshot, binds an
  ephemeral port on `127.0.0.1`, opens the HTTP dashboard, and stays attached
  until Ctrl+C or its idle timeout. Report the URL and which local providers
  are available. Do not run a provider until the user submits a question.

Never open an older report after generation fails. If the browser launcher is
unavailable, keep the generated report and return its absolute path.

### Step 3: Report

Report the selected mode, database path, dashboard path, and whether the browser
was opened. For status mode, separate verified values from interpretation.

## Safety

- Keep the dashboard local; it can contain task, plan, session, and verification data.
- Do not publish, upload, email, or attach the HTML without explicit user authorization.
- Do not edit `.qe/qe.db`, run migrations, or execute non-`SELECT` SQL.
- Regeneration may overwrite only `.qe/inspector.html`.
- Assistant mode accepts requests only from its exact loopback origin with an
  in-memory random token. It does not store credentials or conversation data.
- Assistant mode sends only the user's question and a compact current-dashboard
  context to the selected local CLI. Claude runs with tools disabled; Codex
  runs ephemerally in a read-only sandbox. Account usage may apply.

## Will

- Provide one-command access to the existing QE Inspector
- Read the current project's database and regenerate a local snapshot
- Explain datasets and project task history before exposing raw rows
- Offer an explicit local Claude/Codex question mode when requested
- Degrade to a clickable path when automatic browser opening is unavailable

## Will Not

- Build a second snapshot implementation
- Treat the generated HTML snapshot as live or auto-refreshing
- Expose the dashboard outside the local machine
