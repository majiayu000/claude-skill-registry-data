---
name: 1password
description: using 1Password cli to manage secrets via op cli.
homepage: https://developer.1password.com/docs/cli/get-started/
---

# 1Password CLI

Follow official CLI get-started steps. Don't guess install commands.

## References

- `references/get-started.md` (install + app integration + sign-in flow)
- `references/cli-examples.md` (real `op` examples)

## Workflow

1. Check OS + shell
2. Verify CLI: `op --version`
3. Confirm desktop app integration enabled (per get-started) and app unlocked
4. **REQUIRED**: create fresh tmux session for all `op` commands (no direct `op` calls outside tmux)
5. Sign in/authorize inside tmux: `op signin` (expect app prompt)
6. Verify access inside tmux: `op whoami` (must succeed before any secret read)
7. Multiple accounts → use `--account` or `OP_ACCOUNT`

## REQUIRED tmux session (T-Max)

Shell tool uses fresh TTY per command. Run `op` inside dedicated tmux session with fresh socket/session name to avoid re-prompts.

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/clawdbot-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/clawdbot-op.sock"
SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op signin --account my.1password.com" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op vault list" Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

See `tmux` skill for socket conventions; don't reuse old session names.

## Guardrails

- Never paste secrets into logs, chat, or code
- Prefer `op run` / `op inject` over writing secrets to disk
- Sign-in without app integration → use `op account add`
- "account is not signed in" → re-run `op signin` inside tmux, authorize in app
- Don't run `op` outside tmux; stop + ask if tmux unavailable
