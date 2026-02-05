---
name: tmux-workflow
description: Portable tmux-based workflow to drive one or multiple long-running Codex CLI “workers” from another process (e.g. Claude CLI) by (1) starting/reusing a tmux session running `codex`, (2) injecting prompts into the Codex pane via `tmux send-keys`/buffer paste, and (3) polling the worker’s Codex JSONL session logs to extract the next assistant reply. Each worker runs with an isolated `CODEX_HOME` (default `~/.codex-workers/<worker_id>`) to prevent log cross-talk when multiple Codex workers run concurrently. Use when you need to submit/wait/read Codex replies in tmux, manage multiple Codex workers, or troubleshoot the tmux worker and log binding.
---

# tmux-workflow

This skill is a self-contained toolkit under `scripts/` (copy this whole folder to any repo’s `.codex/skills/` or to `~/.codex/skills/`).

## Quick start (Claude → Codex)

1. (Optional) Check deps:
   - `bash .codex/skills/tmux-workflow/scripts/check_deps.sh`
2. Start a worker and ask with short names (state directory is configurable; default is `<skill_root>/.twf/`):
   - `bash .codex/skills/tmux-workflow/scripts/twf codex-a`
   - `bash .codex/skills/tmux-workflow/scripts/twf codex-a "你好"`

## Scripts

- `scripts/codex_up_tmux.sh`: start/reuse the worker and write `./.codex-tmux-session.json` (JSON) in the current directory; sync `~/.codex` into per-worker `CODEX_HOME`.
- `scripts/codex_ask.py`: inject text into the tmux pane and poll Codex `sessions/*.jsonl` until the next assistant reply appears.
- `scripts/codex_pend.py`: print the latest reply (or last N Q/A pairs) from the bound or auto-detected Codex log.
- `scripts/codex_ping.py`: health check for tmux worker and log binding.
- `scripts/sync_codex_home.py`: sync `~/.codex` into a per-worker `CODEX_HOME` (excludes `sessions/`, `log/`, `history.jsonl`).
- `scripts/twf`: recommended wrapper for managing many workers: `up/ask/pend/ping/stop/resume/spawn/tree/list/remove` with automatic naming and “pick latest” behavior.
- `scripts/install_claude_cmds.sh` (optional): install Claude custom commands (`/cask`, `/cpend`, `/cping`) that call this skill’s scripts.

## Recommended usage (`twf`)

### Naming rules (base vs full name)

- **Base name**: short label like `codex-a`.
- **Full name**: auto-generated unique worker id: `<base>-YYYYmmdd-HHMMSS-<pid>` (also used as tmux session name).
- `twf <base>` creates a new full-name worker and writes state to `<state_dir>/<full>.json`.
- `twf <base> "msg"` will use the **latest** full-name worker for that base (by state-file mtime). If none exists, it auto-creates one.
- `remove` always requires **full name** to avoid deleting the wrong worker.

State directory:
- default: configured via `scripts/twf_config.yaml` (`twf_state_dir_mode`, default `auto`)
  - `auto`: `<skill_root>/.twf/` (project install default: `./.codex/skills/tmux-workflow/.twf/`)
  - `global`: `~/.twf/`
  - `manual`: `twf_state_dir` (must be set in config; relative paths resolve from current directory)
- override: `TWF_STATE_DIR=/some/path` (highest priority; ignores `twf_state_dir_mode`)

### Core commands

- Start a worker (returns the state json path on stdout):
  - `bash .codex/skills/tmux-workflow/scripts/twf codex-a`
  - `bash .codex/skills/tmux-workflow/scripts/twf up codex-a`
- Ask a worker and print Codex reply to stdout:
  - `bash .codex/skills/tmux-workflow/scripts/twf codex-a "your prompt"`
  - `bash .codex/skills/tmux-workflow/scripts/twf ask codex-a "your prompt"`
- Inspect:
  - `bash .codex/skills/tmux-workflow/scripts/twf pend codex-a [N]`
  - `bash .codex/skills/tmux-workflow/scripts/twf ping codex-a`

### Stop / Resume (resume keeps logs)

- `twf stop <name|full-name>`: stop tmux session, keep state + `CODEX_HOME` (so it can be resumed later).
- `twf resume <name|full-name>`: resume a stopped worker.
  - default: resume the worker **and its subtree** (children).
  - `--no-tree`: resume only this node.

Resume source id:
- `twf stop` stores `codex_resume_from_id` by reading the latest `session_meta.payload.id` from that worker’s newest `*.jsonl` log.
- `twf resume` uses `codex resume <id>` when `codex_resume_from_id` exists; otherwise falls back to a fresh `codex` session.

### Parent/Child workers (“sub-codex”)

Create a child worker and link it to a parent:
- `twf spawn <parent-full> <child-base> [up-args...]`

Notes:
- parent must be **full name** (unique).
- child is created as a new full-name worker and recorded into:
  - child: `parent=<parent-full>`
  - parent: `children[] += <child-full>`

Show structure:
- `twf tree [root-full]`
- `twf list [--running|--stopped|--orphans]`

### Remove (destructive)

- `twf remove <full-name>`: **default recursive** delete of the node + its subtree:
  - kills tmux sessions
  - deletes worker `CODEX_HOME`
  - deletes state json files
- `twf remove <full-name> --no-recursive`: delete only the single node

Safety:
- `remove` only deletes `codex_home` if it is under `TWF_WORKERS_DIR` (or default `~/.codex-workers`); otherwise it refuses and asks you to delete manually.

## Environment knobs

### Low-level (`codex_up_tmux.sh` and friends)

- `TWF_SESSION_FILE`: session file path (default: `./.codex-tmux-session.json`).
- `TWF_TMUX_SESSION`: override tmux session name (default: `codex-<hash(cwd)>`).
- `TWF_CODEX_CMD_CONFIG`: YAML config path (default: `scripts/twf_config.yaml` in this skill). Keys:
  - `model` (default `gpt-5.2`)
  - `model_reasoning_effort` (default `xhigh`)
  - `twf_state_dir_mode` (default `auto`; `auto|global|manual`)
  - `twf_state_dir` (required when `twf_state_dir_mode=manual`)
  - `twf_use_load_balancer` (default `false`; when `true`, asks `codex-load-balancer` to choose a `CODEX_HOME` source per worker)
  - `twf_load_balancer_cmd` (optional path override to the load balancer command; otherwise auto-detected)
- `TWF_CODEX_CMD`: override the full command used inside tmux (if unset, it is built from `TWF_CODEX_CMD_CONFIG`).
- `TWF_WORKERS_DIR`: per-worker `CODEX_HOME` base dir (default: `~/.codex-workers`).
- `TWF_CODEX_HOME_SRC`: source `CODEX_HOME` to copy from (default: `~/.codex`).
- `TWF_AUTH_SRC`: optional auth file to copy into worker as `auth.json` (overrides synced `auth.json`).
- `TWF_LOAD_BALANCER_CMD`: optional path to `codex-load-balancer/scripts/clb` (takes precedence over `twf_load_balancer_cmd`).
- `TWF_CODEX_SESSION_ROOT` / `CODEX_SESSION_ROOT` / `CODEX_HOME`: where to scan logs (default: `~/.codex/sessions`).
- `TWF_WATCH_MODE` (default `auto`):
  - `auto`: on Linux/WSL use `inotify` to block until the log file changes; otherwise fall back to polling.
  - `poll`: always polling with `TWF_POLL_INTERVAL`.
  - `inotify`: force `inotify` (falls back to polling if unavailable).
- `TWF_POLL_INTERVAL` (seconds, default `0.05`), `TWF_TIMEOUT` (seconds, default `3600`).
- `TWF_STATE_DIR`: override twf wrapper state dir (highest priority).
- `TWF_SUBMIT_DELAY` (seconds, default `0.5`): delay between injecting text and pressing Enter in tmux (workaround for Codex TUI paste-burst behavior).
- `TWF_SUBMIT_NUDGE_AFTER` (seconds, default `0.7`) and `TWF_SUBMIT_NUDGE_MAX` (default `2`): if the prompt appears to be typed but not submitted, send extra Enter keypresses while waiting for logs to acknowledge the user message.
