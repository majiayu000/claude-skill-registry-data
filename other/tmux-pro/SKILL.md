---
name: tmux-pro
description: Tmux guidance — sessions, windows, panes, keybindings, scripting layouts, and remote pairing workflows.
category: development
---

## Overview

Tmux is the terminal multiplexer: persistent sessions that survive SSH disconnects, split panes, multiple windows, and scriptable layouts. It's the difference between a fragile terminal and a durable workspace — long-running processes keep running, contexts stay organized, and remote pairing becomes trivial.

The learning curve is the prefix key and the session/window/pane model. Once internalized, tmux becomes invisible infrastructure. This skill covers the mental model, essential keybindings, configuration, scripted layouts, and remote workflows.

## When to use

- Keeping remote work alive across SSH disconnects.
- Organizing terminal work (sessions per project, windows per task).
- Scripting reproducible dev environments (editor + server + logs).
- Pairing or sharing a terminal session.
- Configuring tmux (prefix, mouse, plugins, status bar).
- Choosing between tmux, screen, or terminal tabs.

## Core concepts

- **The hierarchy.** Server → sessions → windows → panes. Sessions group a project's windows; windows are full-screen workspaces; panes split a window. Name sessions (`tmux new -s shop`) — unnamed sessions are lost sessions.
- **The prefix.** Default `C-b`, remapped by most to `C-a` or `C-Space`. Every command starts with it. The single biggest usability change: pick a prefix your fingers reach, and make it consistent everywhere.
- **Detaching.** `prefix d` detaches; the session persists server-side. `tmux attach -t name` reattaches. This is the core value: disconnect-proof work.
- **Windows vs panes.** Windows (`prefix c`, `n`/`p` navigate) for distinct tasks; panes (`prefix %` vertical split, `prefix "` horizontal) for side-by-side views. Don't nest panes four deep — that's what windows are for.
- **Copy mode.** `prefix [` enters scrollback/copy mode (vi keys with `mode-keys vi`); search, select, yank to tmux buffers; `prefix ]` pastes. Integrate with system clipboard (osc52 or `xclip`/`pbcopy` bindings) — without this, copy-paste is painful.
- **Configuration.** `~/.tmux.conf`: prefix remap, `mouse on` (sensible in 2026), vi mode-keys, sensible defaults (base-index 1, renumber-windows), plugin manager (tpm) with a curated set (sensible, yank, resurrect).
- **Plugins (tpm).** `tmux-plugins/tpm` + a short list: `sensible` (baseline), `yank` (clipboard), `resurrect` + `continuum` (session restore across reboots). Few plugins, each earning its place.
- **Status bar.** Show session name, window list, hostname, load, time — enough context to know where you are. Keep it informative, not decorative.
- **Scripting layouts.** `tmux new-session -d -s dev`, `send-keys`, `split-window`, `select-layout` — a script that builds your whole dev environment (editor, server, logs, shell) in one command. Dotfile this.
- **Nesting.** tmux inside tmux (local + remote): distinct prefixes per level (e.g., `C-Space` local, `C-a` remote) or `prefix prefix` passthrough. Confusing until the prefixes differ.
- **Pairing.** `tmux attach -t pair` — two people, one session, shared view. Read-only attach (`-r`) for observers. Combined with SSH, it's zero-setup pairing.
- **Resurrect/continuum.** Automatic session save/restore across machine reboots — your layout survives restarts. Configure save intervals and process restore lists.
- **True color and terminfo.** `set -g default-terminal "tmux-256color"`, terminal overrides for RGB — without this, colorschemes render wrong and you'll blame the theme.

## Practical workflow

1. **Remap the prefix and set basics.** The config 90% of users converge on:
   ```tmux
   unbind C-b; set -g prefix C-Space; bind C-Space send-prefix
   set -g mouse on
   setw -g mode-keys vi
   set -g base-index 1; setw -g pane-base-index 1
   set -g renumber-windows on
   set -g default-terminal "tmux-256color"
   ```
2. **Learn the core keys.** `prefix d` detach, `prefix c` new window, `prefix n/p` navigate, `prefix %`/`"` splits, `prefix z` zoom pane, `prefix [` copy mode, `prefix ,` rename window. Muscle memory over cheat sheets.
3. **Name everything.** Sessions per project (`shop`, `infra`), windows per task (`editor`, `server`, `logs`). `prefix $` renames sessions; named sessions attach unambiguously.
4. **Fix clipboard.** yank plugin or manual bindings piping to `pbcopy`/`xclip`/OSC52 — copy mode must reach the system clipboard or it's half-useless.
5. **Script your layout.** A `dev-session` script per project:
   ```bash
   tmux new-session -d -s shop -n editor -c ~/code/shop
   tmux send-keys -t shop:editor 'nvim' Enter
   tmux new-window -t shop -n server -c ~/code/shop
   tmux send-keys -t shop:server 'npm run dev' Enter
   tmux new-window -t shop -n logs
   tmux send-keys -t shop:logs 'tail -f /var/log/shop/app.log' Enter
   tmux attach -t shop
   ```
6. **Add resurrect.** tpm + resurrect + continuum — sessions restored after reboot; verify restore works before relying on it.
7. **Pair deliberately.** Share the session name; observer uses read-only attach; agree on driver/navigator roles — two cursors fighting is worse than one.
8. **Handle nesting.** Different prefix per nesting level; document which is which in the status bar if you nest often.

## Common pitfalls

- **Default prefix kept** — `C-b` is awkward; remap to something reachable.
- **Unnamed sessions** — `tmux ls` full of numbers; name sessions at creation.
- **Mouse left off** — 2026 defaults should include `mouse on`; scrolling and resizing without it is masochism.
- **Clipboard not integrated** — copy mode that can't reach the OS; fix with yank/OSC52.
- **No resurrect** — layouts lost on reboot; automate session persistence.
- **Deeply nested panes** — 6 tiny panes instead of windows; windows for tasks, panes for pairs.
- **Prefix conflicts when nested** — same prefix on both levels; differentiate.
- **True color broken** — wrong `default-terminal`; set `tmux-256color` with RGB overrides.
- **Killing the server accidentally** — `kill-server` vs `kill-session`; know the difference before binding keys.
- **Over-pluginning** — 20 tpm plugins slowing startup; curated minimal set.
- **Not detaching on disconnect** — relying on terminal tabs for remote work; tmux is the persistence layer.
- **Status bar noise** — decorative widgets eating width; context (session, host, time) only.
- **Forgetting `send-prefix`** — nested commands going to the wrong level; bind and use it.
