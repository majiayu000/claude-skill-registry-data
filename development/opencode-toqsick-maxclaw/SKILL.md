---
name: opencode
description: Delegate coding to OpenCode CLI (features, PR review).
version: 1.2.0
author: Hermes Agent
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Coding-Agent
    - OpenCode
    - Autonomous
    - Refactoring
    - Code-Review
    related_skills:
    - claude-code
    - codex
    - hermes-agent
lane: koenigin
reasoning_effort: xhigh
---
# OpenCode CLI

Use [OpenCode](https://opencode.ai) as an autonomous coding worker orchestrated by Hermes terminal/process tools. OpenCode is a provider-agnostic, open-source AI coding agent with a TUI and CLI.

## When to Use

- User explicitly asks to use OpenCode
- You want an external coding agent to implement/refactor/review code
- You need long-running coding sessions with progress checks
- You want parallel task execution in isolated workdirs/worktrees

## Prerequisites

- OpenCode installed: `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`
- Auth configured: `opencode auth login` or set provider env vars (OPENROUTER_API_KEY, etc.)
  - **Ollama-only setups do NOT need `opencode auth login`** — Ollama is auto-discovered. Zero credentials is normal.
- Verify: `opencode auth list` shows expected providers (may be empty for Ollama-only)
- Git repository for code tasks (recommended)
- `pty=true` for interactive TUI sessions

## Binary Resolution (Important)

Shell environments may resolve different OpenCode binaries. On this system, npm global installs to `~/.hermes/node/bin/`, which is often not in the default PATH.

If behavior differs between your terminal and Hermes, or `opencode` is not found after install:

```

set -euo pipefail
terminal(command="which -a opencode")
terminal(command="opencode --version")
terminal(command="npm root -g")   # find where npm put it
```

If needed, pin an explicit binary path:

```

set -euo pipefail
terminal(command="$HOME/.hermes/node/bin/opencode run '...'", workdir="~/project", pty=true)
```

Or add to PATH inline:

```

set -euo pipefail
terminal(command="export PATH=\"$HOME/.hermes/node/bin:$PATH\" && opencode run '...'", workdir="~/project")
```

## Ollama Integration (Local Models)

The official way to use OpenCode with locally-running Ollama models is via `ollama launch opencode`:

```

set -euo pipefail
ollama launch opencode --model <modelname>
```

This auto-configures the provider, passes model list inline via `OPENCODE_CONFIG_CONTENT`, and skips the need for `opencode auth login`.

**Model naming:** Use the exact Ollama tag (e.g. `qwen3.6:27b`, not `ollama/qwen3.6:27b`). If you get `model not found`, add `--yes` to auto-pull:

```

set -euo pipefail
ollama launch opencode --model qwen3.6:27b       # launch with existing model
ollama launch opencode --model qwen3.6 --yes      # auto-pull if missing
```

**WARNING:** The `opencode run --model ollama/<name>` syntax does NOT work with Ollama. `ollama launch opencode` is the correct entry point.

Launch with `background=true, pty=true` for Hermes-orchestrated interactive use:

```

set -euo pipefail
terminal(command="ollama launch opencode --model qwen3.6:27b", background=true, pty=true)
```

The TUI shows the model name in the bottom bar (e.g. `Build · qwen3.6:27b Ollama`). Interact via `process(action="submit", ...)` and exit via `process(action="write", data="\\x03")`.

## One-Shot Tasks

Use `opencode run` for bounded, non-interactive tasks:

```

set -euo pipefail
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")
```

Attach context files with `-f`:

```

set -euo pipefail
terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")
```

Show model thinking with `--thinking`:

```

set -euo pipefail
terminal(command="opencode run 'Debug why tests fail in CI' --thinking", workdir="~/project")
```

Force a specific model:

```

set -euo pipefail
terminal(command="opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

## Interactive Sessions (Background)

For iterative work requiring multiple exchanges, start the TUI in background:

```

set -euo pipefail
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# Returns session_id

# Send a prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send follow-up input
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit cleanly — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# Or just kill the process
process(action="kill", session_id="<id>")
```

**Important:** Do NOT use `/exit` — it is not a valid OpenCode command and will open an agent selector dialog instead. Use Ctrl+C (`\x03`) or `process(action="kill")` to exit.

### TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Submit message (press twice if needed) |
| `Tab` | Switch between agents (build/plan) |
| `Ctrl+P` | Open command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+X E` | Open editor |
| `Ctrl+C` | Exit OpenCode |

### Resuming Sessions

After exiting, OpenCode prints a session ID. Resume with:

```

set -euo pipefail
terminal(command="opencode -c", workdir="~/project", background=true, pty=true)  # Continue last session
terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)  # Specific session
```

## Common Flags

| Flag | Use |
|------|-----|
| `run 'prompt'` | One-shot execution and exit |
| `--continue` / `-c` | Continue the last OpenCode session |
| `--session <id>` / `-s` | Continue a specific session |
| `--agent <name>` | Choose OpenCode agent (build or plan) |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output/events |
| `--file <path>` / `-f` | Attach file(s) to the message |
| `--thinking` | Show model thinking blocks |
| `--variant <level>` | Reasoning effort (high, max, minimal) |
| `--title <name>` | Name the session |
| `--attach <url>` | Connect to a running opencode server |

## Procedure

1. Verify tool readiness:
   - `terminal(command="opencode --version")`
   - `terminal(command="opencode auth list")`
2. For bounded tasks, use `opencode run '...'` (no pty needed).
3. For iterative tasks, start `opencode` with `background=true, pty=true`.
4. Monitor long tasks with `process(action="poll"|"log")`.
5. If OpenCode asks for input, respond via `process(action="submit", ...)`.
6. Exit with `process(action="write", data="\x03")` or `process(action="kill")`.
7. Summarize file changes, test results, and next steps back to user.

## PR Review Workflow

OpenCode has a built-in PR command:

```bash

set -euo pipefail
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

Or review in a temporary clone for isolation:

```bash

set -euo pipefail
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, and style issues.' -f $(git diff origin/main --name-only | head -20 | tr '\\n' ' ')", pty=true)
```

## Security & Bug Fix Workflow

Use OpenCode for targeted security patches and bug fixes, especially during
multi-agent research (Phase 2: Immediate Fixes):

### Use Cases

- **Security-Lücken schließen:** Identifizierte Schwachstellen (Injection,
  XSS, unsichere Deserialisierung, hardcodierte Secrets) automatisiert fixen
- **Bug-Fixes:** Defekte Logik, Edge Cases, Race Conditions, Memory Leaks
- **Refactoring:** Dead Code entfernen, Error-Handling nachrüsten

### One-Shot Security Fixes

```bash

set -euo pipefail
terminal(command="opencode run 'Fix the SQL injection in login.py by using parameterized queries'", workdir="~/project")
```

```bash

set -euo pipefail
terminal(command="opencode run 'Add input validation to all API endpoints in routes/' -f routes/", workdir="~/project")
```

```bash

set -euo pipefail
terminal(command="opencode run 'Replace hardcoded API keys with env vars and add .env.example'", workdir="~/project")
```

### Batch Security Fixes (Multiple Files)

```bash

set -euo pipefail
terminal(command="opencode run 'Scan auth/ for session management bugs:
- Missing expiry checks
- Weak token generation
- Missing CSRF tokens on state-changing endpoints
Fix everything you find and add tests'", workdir="~/project")
```

### Integration in Multi-Agent Research (via `multi-agent-research` Skill)

Wenn `multi-agent-research` läuft, kann der Parent in Phase 2 (Immediate Fixes)
parallel zu den Experts OpenCode für schnelle Security-Fixes starten:

```bash

set -euo pipefail
# Während Experts laufen: Schnelle Bug-Fixes via OpenCode
terminal(command="opencode run 'Fix: add OAuth token refresh error handling in api/client.py'",
         workdir="~/project", background=true, notify_on_complete=true)

# Verifizieren nach Fertigstellung
terminal(command="cd ~/project && git diff --stat")
```

### Best Practices

1. **Präzise Prompts:** Sag genau WELCHE Lücke und WELCHER Fix — nicht "mach
   sicherer", sondern "Ersetze hardcodierte Secrets in config.py durch env vars"
2. **Isoliert arbeiten:** Ein Fix pro `opencode run` — nicht mehrere Bugs in
   einem Durchlauf (erschwert Review)
3. **Verifizieren:** Immer `git diff` oder `diff -u` nach dem Fix prüfen
4. **Tests:** Lass OpenCode Tests zum Fix mitgenerieren — `... and add a test
   that verifies the fix`

## Parallel Work Pattern

Use separate workdirs/worktrees to avoid collisions:

```

set -euo pipefail
terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

## Session & Cost Management

List past sessions:

```

set -euo pipefail
terminal(command="opencode session list")
```

Check token usage and costs:

```

set -euo pipefail
terminal(command="opencode stats")
terminal(command="opencode stats --days 7 --models anthropic/claude-sonnet-4")
```

## Pitfalls

- Interactive `opencode` (TUI) sessions require `pty=true`. The `opencode run` command does NOT need pty.
- `/exit` is NOT a valid command — it opens an agent selector. Use Ctrl+C to exit the TUI.
- PATH mismatch: `npm i -g opencode-ai` may install to `~/.hermes/node/bin/` (this system) or other non-standard locations. If `opencode` isn't found, check `npm root -g` and use the full path.
- Ollama + OpenCode: Do NOT use `opencode run --model ollama/<name>` — it fails with "Provider not found: ollama". Use `ollama launch opencode --model <name>` instead.
- If OpenCode appears stuck, inspect logs before killing:
  - `process(action="log", session_id="<id>")`
- Avoid sharing one working directory across parallel OpenCode sessions.
- Enter may need to be pressed twice to submit in the TUI (once to finalize text, once to send).

## Verification

Smoke test:

```

set -euo pipefail
terminal(command="opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'")
```

Success criteria:
- Output includes `OPENCODE_SMOKE_OK`
- Command exits without provider/model errors
- For code tasks: expected files changed and tests pass

## Rules

1. Prefer `opencode run` for one-shot automation — it's simpler and doesn't need pty.
2. Use interactive background mode only when iteration is needed.
3. Always scope OpenCode sessions to a single repo/workdir.
4. For long tasks, provide progress updates from `process` logs.
5. Report concrete outcomes (files changed, tests, remaining risks).
6. Exit interactive sessions with Ctrl+C or kill, never `/exit`.
