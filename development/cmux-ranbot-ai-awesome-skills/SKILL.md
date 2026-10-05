---
name: cmux
description: Control cmux workspaces, panes, surfaces, and agent sessions safely from macOS terminal workflows. 
category: Document Processing
source: antigravity
tags: [python, pdf, markdown, api, claude, ai, agent, automation, workflow, document]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/cmux
---


# cmux Control

## When to Use

- Use when you need to inspect, create, close, or rearrange cmux panes, surfaces, or workspaces.
- Use when you need to send input to or monitor agents running inside cmux.

cmux is a native macOS terminal app for running multiple AI coding agents in parallel. It exposes a CLI (`cmux`) and a Unix-socket JSON-RPC API (`/tmp/cmux.sock`) for full topology and browser control.

## Core Concepts

- **Window** — top-level macOS cmux window
- **Workspace** — sidebar tab within a window (one git branch / project context)
- **Pane** — split region inside a workspace
- **Surface** — tab inside a pane (terminal or browser)

Handles default to short refs (`workspace:2`, `pane:1`, `surface:7`); UUIDs accepted as input. Add `--id-format uuids|both` for UUID output.

### Ref syntax — get this right or fail silently

- **Always use PREFIXED refs** (`pane:38`, `surface:46`). A **bare number is treated as an INDEX, not an ID** — `--surface 46` means "the surface at index 46" (usually nonexistent → silent failure), NOT `surface:46`.
- **`read-screen` and `capture-pane` have NO `--pane` flag** — they target `--workspace` or `--surface` only. Passing `--pane` errors, and a bare/missing target falls back to your OWN surface (you'll read your own footer and draw wrong conclusions). To read a pane: resolve it to a surface FIRST with `cmux list-pane-surfaces --pane pane:N`, then `cmux read-screen --surface surface:N`.
- **Never append `2>/dev/null` to cmux commands.** Errors go to stderr with exit code 1; suppressing them blinds you to your own ref/flag mistakes (the #1 cause of "(no output)").

## Detect cmux in a Shell

```bash
[ -S "${CMUX_SOCKET_PATH:-/tmp/cmux.sock}" ] || exit 0   # bail if not in cmux
[ -n "${CMUX_WORKSPACE_ID:-}" ] && echo "inside cmux surface"
```

Injected env vars in every cmux-spawned terminal: `CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH`, `CMUX_PORT`. **Always anchor automation to `CMUX_WORKSPACE_ID`** — the visually focused workspace may not be the agent's caller workspace.

## Fast Start — Topology

```bash
cmux identify --json                              # who am I (window/workspace/pane/surface)
cmux tree                                         # full hierarchy
cmux list-workspaces --json
cmux list-panes --workspace "$CMUX_WORKSPACE_ID"
cmux list-surfaces --workspace "$CMUX_WORKSPACE_ID"

cmux new-workspace --name "feature-x" --cwd /path/to/repo
cmux new-pane --workspace "$CMUX_WORKSPACE_ID" --type terminal --direction right --focus false
cmux new-pane --workspace "$CMUX_WORKSPACE_ID" --type browser  --direction right --url http://localhost:3000
cmux move-surface --surface surface:7 --pane pane:2 --focus false
cmux split-off --surface surface:7 right
cmux reorder-surface --surface surface:7 --before surface:3
cmux close-surface --surface surface:7
```

## Polling Pi Agents in Panes — Keep Sleeps Short

When launching a Pi Agent inside a cmux pane and polling for output, use **short `sleep` intervals (2–5s)**. Pi is fast and minimal, and the user runs it on Opus 4.8 Fast via OpenRouter, which streams tokens extremely quickly. Do NOT use `sleep 15` unless genuinely needed (a big build/refactor) — most of the time `sleep 2`–`sleep 5` is more than enough.

After every agent check, send the user a one-line status update: what the agent is doing and whether it is on track. Keep it extremely concise.

Claude Code cmux note: after Claude finishes, it may prefill a predicted next user message; that draft is Claude, not the user speaking.

## Send Input

**Command names:** there is NO `send-surface` / `send-key-surface`. Target a specific surface with the `--surface` flag on `send` / `send-key` (same commands as the focused terminal). `send-panel` / `send-key-panel` exist ONLY for panels (`--panel`), not surfaces.

```bash
cmux send "echo hi\n"                                       # focused terminal
cmux send-key "ctrl+c"                                       # enter|tab|esc|backspace|arrows|ctrl+x|shift+tab
cmux send --surface surface:7 "npm run build"               # specific surface (NOT send-surface)
cmux send-key --surface surface:7 enter                     # specific surface (NOT send-key-surface)
```

## Notifications & Sidebar Metadata

```bash
cmux notify --title "Done" --body "tests passed"
cmux set-status build "compiling" --icon hammer --color "#ff9500"
cmux set-progress 0.5 --label "Building..."
cmux log --level success "All 42 tests passed"               # info|progress|success|warning|error
cmux trigger-flash --workspace "$CMUX_WORKSPACE_ID"          # blue-ring attention cue
cmux sidebar-state --json                                    # dump all sidebar metadata
```

## Browser Automation (WKWebView)

Workflow: open → wait → snapshot → act → re-snapshot.

```bash
S=$(cmux --json browser open https://example.com | jq -r .result.surface_ref)
cmux browser "$S" wait --load-state complete --timeout-ms 15000
cmux browser "$S" snapshot --interactive  
