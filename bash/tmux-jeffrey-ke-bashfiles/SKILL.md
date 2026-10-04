---
name: tmux
description: Reference for tmux's data model, command system, quoting rules, and configuration patterns. Use when writing or debugging tmux config, bind-key commands, run-shell scripts, or format strings.
argument-hint: [optional: describe what you're configuring or debugging]
---

# tmux — Program and Data Model

## Object Hierarchy

tmux is a client-server terminal multiplexer. The server owns all state; clients attach to view and interact with it.

```
server (one per socket, usually one per user)
  └── session (named group of windows)
        └── window (a tab within a session, has a layout)
              └── pane (a single terminal instance)
```

- **Server** — The persistent process. Survives client disconnection. Owns all sessions, windows, panes. Started implicitly by `tmux new-session` or explicitly with `tmux start-server`.
- **Session** — A named collection of windows. Each client is attached to exactly one session. Sessions persist until explicitly killed or the last window closes.
- **Window** — A tab within a session. Has a layout (how its panes are arranged) and a name. Windows are numbered per-session (the index can have gaps).
- **Pane** — A single pseudo-terminal. Runs one shell or process. Panes are numbered per-window starting at 0.

### Target Syntax

Most commands accept a target to identify a session, window, or pane:

```
-t session_name           # target a session
-t session:window         # target a window (by index or name)
-t session:window.pane    # target a specific pane
-t :window                # window in current session
-t :.pane                 # pane in current window
-t !                      # last active window
-t +                      # next window
-t -                      # previous window
```

Special tokens: `$` = current session, `@` = current window, `%` prefix = pane ID (global).

## Command System

tmux commands can be run from:
1. **Shell** — `tmux command args...`
2. **Config file** — one command per line in `.tmux.conf`
3. **Command prompt** — `prefix :` then type a command
4. **Key bindings** — `bind-key` associates a key with one or more commands

### Command Sequencing

Commands in a binding are separated by `\;` (escaped semicolon):

```
bind-key x kill-pane \; display-message "pane killed"
```

Without the backslash, the shell or tmux parser treats `;` as a line terminator.

### Blocking vs Background

- `run-shell "cmd"` — blocks the command queue until the shell command finishes
- `run-shell -b "cmd"` — runs in background, queue continues immediately
- `command-prompt` and `confirm-before` — block by default (since tmux 3.2+)

When chaining with `\;`, a blocking command delays subsequent commands. Use `-b` when the result isn't needed before the next command runs.

## Quoting and Format Expansion

This is the single most error-prone area of tmux configuration. There are three quoting styles, each with different expansion rules:

### Double Quotes `"..."`

- tmux **expands** format variables: `#I`, `#W`, `#S`, `#{...}`
- tmux **expands** environment variables: `$HOME`
- Backslash escapes work: `\"`, `\\`, `\;`, `\$`

### Single Quotes `'...'`

- Documented as "literal" but **`run-shell` still expands format variables inside single-quoted arguments**
- Safe from shell interpretation but NOT safe from tmux format expansion in `run-shell`

### Braces `{...}`

- Text inside is taken literally without replacements
- Supports line continuation (can span multiple lines)
- Designed for passing groups of tmux or shell commands as arguments (e.g., to `if-shell`)
- Note: historically had bugs with `run-shell` (issue #2841, fixed in ~3.3)

### The Critical Rule for `run-shell`

**`run-shell` always expands tmux format variables in its argument, regardless of quoting style.** To pass a literal `#X` through to the shell, you must double the hash:

```
# WRONG — tmux expands #I and #W before the shell sees them
run-shell 'tmux list-windows -F "#I:#W"'

# RIGHT — ## produces literal # after tmux expansion
run-shell 'tmux list-windows -F "##I:##W"'
```

This applies to all format sequences: `##I` (window index), `##W` (window name), `##S` (session name), `##{...}` (conditional formats), etc.

### Format Strings

Formats are tmux's variable/expression system. They appear wherever tmux expands strings (status line, `display-message`, `list-windows -F`, `if-shell` conditions, etc.).

```
#S                  — session name
#I                  — window index
#W                  — window name
#P                  — pane index
#T                  — pane title
#{pane_current_path} — long-form variable
#{?condition,true,false} — conditional
#{==:#{a},#{b}}     — comparison
#(shell-command)    — output of shell command (cached, re-run periodically)
```

The `#()` form runs a shell command and substitutes its stdout. It's cached and re-evaluated periodically (useful in status-line formats). It does NOT run on every keystroke.

## Key Binding Model

```
bind-key [-n] [-T table] key command [args...]
```

- **Prefix table** (default) — key is pressed after the prefix key (e.g., `C-Space`)
- **Root table** (`-n` or `-T root`) — key fires without prefix (use carefully)
- **Copy-mode tables** (`-T copy-mode-vi`, `-T copy-mode`) — active during copy mode

Key names: `C-x` (ctrl), `M-x` (alt/meta), `S-x` (shift for special keys), `F1`-`F12`, `Up`/`Down`/`Left`/`Right`, `Enter`, `Space`, `BSpace`, `Tab`, `DC` (delete), `IC` (insert), `NPage`/`PPage` (page down/up).

## Configuration Patterns

### Dynamic Prompts with Window/Session Lists

The proven pattern for showing a dynamic list in a `command-prompt`:

```
# Build window list in shell, pass to command-prompt
bind-key X run-shell 'wins=$(tmux list-windows -F "##I:##W" \
  | tr "\n" "|" | sed "s/|$//; s/|/ | /g"); \
  tmux command-prompt -p "[$wins] Prompt:" "some-command \"%%\""'
```

Key points:
- `##I:##W` — double hash to survive `run-shell` format expansion
- `tr` + `sed` for joining — `paste -sd " | "` does NOT produce ` | ` separators (it cycles through ` `, `|`, ` ` as individual delimiter characters)
- `%%` — `command-prompt`'s placeholder, replaced with user input
- `\"%%\"` — escaped quotes so tmux passes `"user_input"` to the command

### Dynamic Menus

For selection (rather than free-text input), `display-menu` is often better:

```
# Build a menu from session list
bind-key S run-shell 'tmux list-sessions -F "##S" \
  | awk '\''BEGIN{ORS=" "}{print $1, NR, "\"switch-client -t " $1 "\""}'\'' \
  | xargs tmux display-menu -T "Switch session"'
```

`display-menu` takes triplets: `name key command`. The user navigates with arrows or presses the shortcut key.

### Environment and Options

```
# Server options
set -g option value          # -g = global (server-wide)
set -s option value          # -s = server option

# Session options
set option value             # current session

# Window options
set -w option value          # current window
set -wg option value         # global window default

# User options (arbitrary key-value storage)
set -g @myvar "hello"        # set
display-message "#{@myvar}"  # read in format string
```

User options (prefixed with `@`) are useful for communication between `run-shell` scripts and format strings: set the value in a shell command, read it in a format expansion.

### Conditional Execution

```
# if-shell runs a shell command; branches on exit code
if-shell "command -v fzf" {
  bind-key f run-shell "fzf-tmux"
} {
  bind-key f choose-tree
}

# Format conditionals (inline, for status line etc.)
#{?window_zoomed_flag,ZOOMED,}
```

### Pane Border Status (labels on the border)

`pane-border-status` (`off` | `top` | `bottom`; plus `top-floating` | `bottom-floating`
from 3.8) turns one row of every pane's border
into a label line rendered from `pane-border-format`. Measured on tmux 3.4 against a
nested test server (see `session-log.md`, 2026-08-21):

- The format is evaluated **per pane**, so `#{?pane_active,LABEL,}` yields a label only
  the focused pane shows. An empty expansion draws the plain border: the label vanishes,
  the row stays.
- `#[align=left|centre|right]` **is** honoured here. Default is left, inset 2 cells from
  the pane's left edge; `align=right` reaches the pane's right edge. Alignment is
  relative to the pane, not the window, so each pane labels its own corner.
- The row is spent even when the window holds a single pane. Reclaim it with a hook:
  `set-hook -g window-layout-changed 'if -F "#{==:#{window_panes},1}" "set -w pane-border-status off" "set -w pane-border-status top"'`
- Only one of `top`/`bottom` is active at a time — you cannot label the top border and
  the bottom border differently.
- **On 3.4 there is no floating/boxed pane label**, and the label line is the only
  per-pane decoration tmux draws. The floating rectangles 3.4 *can* draw are modal client
  overlays, not pane decorations: `display-popup` ("a rectangular box drawn over the top of
  any panes" — but "**panes are not updated while a popup is present**", so a persistent
  badge freezes the session), `display-menu` (same), and `display-panes` (per-pane
  indicators; `-b` makes it non-blocking and `-N` is documented as not closing on a key
  press, but measured it dies on the first keystroke and does not return on
  `refresh-client` — a flash, not a label; its big digits are reverse-video spaces, so they
  are invisible to `capture-pane -p`, use `-e`).
- **Upstream has since added real floating panes — check the version before repeating the
  above.** tmux **3.7** added non-modal floating panes (`new-pane`, bound to `*`): they sit
  above the tiled layout like a popup but behave like panes, sized with `-x`/`-y` and
  positioned with `-X`/`-Y` in cells from the window's top-left, so a persistent rectangle
  in a corner *is* possible there. **3.8** adds `new-pane -T` (title) and `-B` (border
  lines), `new-pane -O` for modal panes, `break-pane -W` to float a tiled pane and
  `join-pane` to tile a floating one, `move-pane`/`resize-pane` support, and two new
  `pane-border-status` values, `top-floating` / `bottom-floating`.
- **What `top-floating` actually means** (read the source, not the name): it scopes the
  border status to *floating* panes. `window_pane_get_pane_status()` returns
  `PANE_STATUS_TOP` for a floating pane when the option is `top-floating`, while a tiled
  pane falls through to the window-level resolution. It is **not** an overlay mode for
  tiled panes. Relatedly, `layout_add_horizontal_border()` returns true only for plain
  `top`/`bottom`, so the floating variants never reserve a layout row — a floating pane's
  label is drawn at `yoff - 1`, over whatever is beneath it.
- Even on 3.8 there is still no label that *follows focus* around the tiled panes; that
  remains the border line plus a `#{?pane_active,...}` conditional.
- The upstream default `pane-border-format` is itself worth reading — it uses
  `#[align=right]` with `#[range=control|7|8|9]` clickable controls (float, zoom, close),
  which is direct confirmation that `align` and ranges are intended in pane borders.
- Non-textual active-pane markers that *are* persistent: `pane-border-indicators`
  (`arrows` draws markers pointing at the active pane; `colour` only acts "in windows with
  exactly two panes"), `pane-border-lines number`, and `window-active-style` dimming.
- `pane-border-style` / `pane-active-border-style` also take formats, so the border can
  react to client state: `set -g pane-active-border-style '#{?client_prefix,fg=colour226,fg=colour39}'`
  flashes the active border while the prefix is held.


### Testing Config Changes Without Touching Your Session

Borders, the status line, and pane dimming are drawn by the *client*, so
`capture-pane` — which returns a pane's own content — cannot see them. To inspect them,
run the config under test on a throwaway socket and view it through a second throwaway
socket, whose `capture-pane` sees the inner client's full rendering as ordinary text:

```sh
tmux -L inner -f /dev/null new-session -d -x 78 -y 16 'bash --norc'
tmux -L inner split-window -h 'bash --norc'
tmux -L inner set -g pane-border-status top          # the thing under test
tmux -L outer -f /dev/null new-session -d -x 80 -y 20 "tmux -L inner attach"
sleep 1
tmux -L outer capture-pane -p -t 0 | head -4         # borders now visible as text
tmux -L inner kill-server; tmux -L outer kill-server
```

`-f /dev/null` keeps your own `.tmux.conf` out of it, and `-L` guarantees a separate
server, so nothing here can disturb a live session.


## Common Pitfalls

1. **`#` eaten by `run-shell`** — Always use `##` for literal `#` in `run-shell` arguments. This is the most common tmux scripting bug.

2. **`paste -sd " | "` doesn't join with ` | `** — It cycles through space, pipe, space as separate delimiters. Use `tr "\n" "|" | sed "s/|$//; s/|/ | /g"` instead.

3. **`\;` vs `;`** — In config files, `\;` separates commands in a binding. A bare `;` ends the line. In shell (`tmux bind ...`), you often need `\\;` because the shell eats one backslash.

4. **`run-shell -b` with interactive commands** — Background `run-shell` works with `command-prompt` and `display-menu` because those are tmux commands that register their own input handlers.

5. **Format expansion timing** — Formats in `bind-key` arguments are expanded when the key is pressed, not when the config is loaded. But `run-shell` arguments are expanded once at execution time, then passed to the shell.

6. **Nested tmux commands** — When `run-shell` calls `tmux command-prompt`, the inner tmux command connects to the same server as a client command. Format expansion in the inner command is independent of the outer `run-shell` expansion.

7. **Implicit "current window/pane" is unreliable in nested `run-shell`** — A script invoked via `command-prompt` → `run-shell` does not reliably inherit the current window/pane context. Always capture `#{window_id}` or `#{pane_id}` in the outer `run-shell` (where context is valid) and pass as explicit arguments. See `session-log.md` for a detailed case study.

8. **`display-popup`'s shell-command is not format-expanded on tmux 3.4** (3.5 does expand
   it). To get `#{pane_id}` into a popup on 3.4, hop through `run-shell -b`, which does
   expand, and pass the value as an argument:
   `bind-key e run-shell -b 'tmux display-popup -E "script.sh \"#{pane_id}\""'`

9. **`$TMUX_PANE` inside a `run-shell` child is stale, not absent.** `run-shell` expands
   `#{pane_id}` correctly in its argument, but the child process inherits the *server's*
   environment — so `TMUX_PANE` holds whatever value the process that started the server
   happened to carry. Measured: a `run-shell` on a fresh server saw
   `#{pane_id}` = `%0` (correct) while `$TMUX_PANE` = `%11`, a pane belonging to a
   different server entirely. A script that reads `$TMUX_PANE` therefore fails *silently
   by targeting the wrong pane* rather than erroring out. Always pass the pane id as an
   argument (same rule as #7).

## Session Log

`session-log.md` (in this directory) documents what was tried, what failed, and what worked when building tmux keybindings. **Read it before implementing new bindings** to avoid repeating past mistakes. Key topics covered:
- `##` vs `#` expansion rules in practice (when to use which)
- Why `move-window` / `join-pane` without explicit `-s` fails in nested contexts
- The `new-session` + `move-window` + `kill-window` pattern for breaking a window into a new session
- Driving a Claude Code session from a keybinding (`prefix X` fork, `prefix e` explain): resolving pane → session id, and why the pane id must be passed explicitly
- Labelling only the active pane's border, and how the nested-server test rig measured it
