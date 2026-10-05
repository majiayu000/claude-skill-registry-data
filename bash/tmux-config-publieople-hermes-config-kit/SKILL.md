---
name: tmux-config
description: Author, review, and deploy tmux.conf across heterogeneous hosts (WSL2, Linux server, macOS). Triggers when configuring tmux, picking a prefix key, wiring the system clipboard bridge, or reconciling per-host variants.
---

# tmux-config

## When to load

- User asks to "set up tmux" / "configure tmux" / "fix tmux"
- Authoring a fresh `~/.tmux.conf` or auditing one that misbehaves
- Reconciling a config across WSL2 (Windows clipboard), Linux server (xsel/wl-copy), or macOS (pbcopy)
- Choosing a prefix key, color mode, or copy/paste strategy

## Decision ladder (pick before writing)

1. **Prefix** — `Ctrl-a` is the lazy default. `Ctrl-b` is tmux stock (awkward, home row left hand). `Ctrl-c` collides with SIGINT. `Ctrl-\` is SIGQUIT. Stop arguing, take `C-a` unless user insists.
2. **Color** — `tmux-256color` + `terminal-overrides ",*256col*:Tc"` (Linux) or `",xterm-256color:RGB"` (WSL). Both work, neither needs a vendor terminfo.
3. **Shell** — match the user's login shell. fish users: `set -g default-shell /usr/bin/fish`. Don't override — half the time the user has a `.bashrc` that `exec fish` and tmux's shell start fights with it.
4. **Clipboard bridge** — this is the only per-host difference. See `references/clipboard-bridge.md`.
5. **Mouse + vi copy** — almost always `set -g mouse on` + `mode-keys vi`. Trivial wins.
6. **Status bar** — bottom by default (matches tmux/literature). Only flip to top if user has an embedded terminal/IDE pattern that needs it.

## Verification ritual (ponytail)

The tmux server I'm running inside is my own host. Killing it kills me. So:

```sh
# WRONG — wipes my own session
tmux kill-server

# RIGHT — verify in a fresh session, on the same server, then kill only that session
tmux new-session -d -s _vverify fish -l
tmux source-file ~/.tmux.conf
tmux display-message -p "prefix=[#{prefix}] mouse=[#{mouse}] shell=[#{default-shell}]"
tmux kill-session -t _vverify
```

`-p` prints to stdout (scriptable), the named session makes cleanup explicit. Never `kill-server` during verification.

If the user is on fish and you must check `$?` after a tmux command, use `tmux display-message -p` to embed the check inside tmux itself — fish won't see the `$?` and won't choke.

## SSH + fish login shell (the recurring foot-gun)

When the remote user's login shell is **fish** and you run inline `ssh user@host '...'`:

- `ssh user@host 'echo $?'` → fish expands `$?` to literal `$?` because the command string is passed as argv, then fish sees `$?` and errors: `fish: $? is not the exit status. In fish, please use $status.`
- Symptom: exit code 127, fish error in stderr, your command never ran.

**Fixes (pick one):**
- `ssh user@host bash -c '...'` — ssh then runs bash; bash handles `$?` correctly.
- `ssh user@host /bin/sh <<'EOF' ... EOF` — heredoc forces the remote interpreter to sh, bypassing login shell.
- Never use bare `$?` in a single-quoted remote command when remote shell is fish.

Diagnose: if a remote command fails with `fish: $? is not the exit status`, the cause is fish login shell expanding `$?`, not your command syntax.

## Cross-host config variants

The WSL2 and Linux-server configs in `references/wsl-tmux.conf` and `references/linux-server-tmux.conf` differ in **only two lines**: the clipboard bridge (`clip.exe` vs `xsel --clipboard`) and one `terminal-overrides` flavor. Keep the rest identical so muscle memory survives `ssh` jumps.

## Output style for the user

User wants the config to "just work" with a 1-3 line usage summary at the end, not a 500-word config dump. After deploying, print:
- The 5-7 most-used key bindings (prefix + key)
- One line of "skipped" for what was not done (status bar theme, powerline, etc.)
- A note if any active session needs manual `prefix r` to pick up changes

## Skipped by default (ponytail)

- Powerline / Nerd Font status bar — adds a font dep, asks the user to install fonts. Only do it on explicit request.
- Plugin managers (tpm, catppuccin) — heavy, lazy default is stock tmux. Add when user asks.
- Custom key bindings beyond `C-a`, `r`, `|`, `-`, `p` — no guesswork.
- Per-window themes, icons in status bar — visual noise.
