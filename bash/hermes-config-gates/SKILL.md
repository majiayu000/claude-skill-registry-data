---
name: hermes-config-gates
description: |-
  Diagnose why a Hermes Agent setting/flag/env var is or isn't taking effect.
  Use when the user reports "I set X, reloaded, still Y happens" against ANY
  Hermes surface (CLI prompt_toolkit, TUI Ink overlay, gateway, Electron
  desktop, dashboard PTY, env vars from config.yaml). Triggers: "why does
  /new still prompt", "I set approvals.X = false but it still asks", "the
  config flag isn't honored", "env var not reaching the subprocess", "TUI
  vs CLI setting", "which config does this read".

  Hermes is a polyglot stack: a single user-facing behavior (e.g. "destructive
  command confirmation") is gated in MULTIPLE independent surfaces, each with
  its own config key, env var, or read path. The fix that "didn't work" is
  almost always the right toggle applied to the wrong surface.
---

# Diagnosing Hermes config gates that "don't work"

When the user reports a Hermes setting/flag/env var isn't taking effect, the
bug is almost never the value — it's the surface. Hermes has at least four
parallel config reads for the same user-facing behavior, and the gating is
deliberately split so a single env var can be set without dragging side
effects across runtimes.

## Trigger conditions

- "I set `approvals.foo = false` in config.yaml, restarted, still prompts"
- "I exported `HERMES_X=1`, the modal still shows"
- "TUI and CLI behave differently for the same command"
- "the gate works in CLI but not in TUI" (or vice versa)
- "config.set says success but nothing changes"
- Any phrase that includes "still" + a previous-fix attempt

## The four surfaces — find the right one FIRST

Before changing any config, identify which surface is rendering the UI the
user actually sees. The user almost always sees exactly one of these:

| Surface | Backend | Gating pattern | Where to look |
|---------|---------|----------------|---------------|
| **Classic CLI** (REPL with prompt_toolkit) | `cli.py` | `config.yaml` `approvals.*` keys via `load_cli_config()` | `cli.py:_confirm_destructive_slash`, `hermes_cli/config.py` |
| **TUI** (Ink/Node overlay) | `ui-tui/src/app/slash/commands/core.ts` | `process.env.HERMES_TUI_*` booleans via `truthy()` | `ui-tui/src/config/env.ts` |
| **Gateway** (Telegram/Discord/Slack) | `gateway/run.py` + `gateway/slash_commands.py` | `config.yaml` `approvals.*` + native platform buttons | `gateway/run.py:_request_slash_confirm` |
| **Dashboard PTY** (browser-embedded TUI) | `hermes_cli/web_server.py` `/api/pty` | Same as TUI + `HERMES_TUI_DASHBOARD=1` | `web_server.py:_pty_ws_handler` |

**Heuristic:** if the user shows a screenshot and the buttons say
"Approve Once / Always Approve / Cancel", that's the **CLI/gateway** surface
(`config.yaml` `approvals.<gate>: false`). If the buttons say
"No, keep going / Yes, start a new session" or "Yes, clear the session",
that's the **TUI** surface (`HERMES_TUI_NO_CONFIRM=1`).

## Step 1: Grep the exact UI text, not a paraphrase

The single highest-ROI move. Open `apps/desktop`, `cli.py`, `ui-tui/src`,
`gateway/platforms/`, `hermes_cli/` and grep the literal strings the user
sees in the dialog. Don't paraphrase ("confirmation dialog", "new session
prompt") — paraphrase misses because the same UX can have 3 different
copies in 3 surfaces, each with its own gate.

```bash
# In a checkout of hermes-agent
rg -n '"No, keep going"|"Yes, start a new session"' ui-tui/ apps/ gateway/
rg -n '"Approve Once"|"Always Approve"' cli.py hermes_cli/ gateway/
rg -n 'NO_CONFIRM_DESTRUCTIVE|destructive_slash_confirm' .
```

The first hit usually tells you:
- which file renders the UI (so you know which surface)
- which env var / config key it reads
- whether it's gated at all (some are unconditional)

## Step 2: Trace the env-var bridge, not just the value

`HERMES_TUI_NO_CONFIRM=1` won't help if the variable never reaches the
subprocess. Three common breaks:

1. **WSL/Windows shell aliasing.** The user's interactive shell on WSL is
   `fish` (because `~/.bashrc` does `exec fish`). Fish does NOT source
   `~/.bashrc`. Writing the export to `~/.bashrc` does nothing for a fish
   session. Also, `~/.bashrc` typically has `[[ $- != *i* ]] && return` at
   the top, so even from bash, non-interactive subshells (which is what
   `hermes` Python launches into) skip everything below the guard.

   Fix: write the export to `~/.config/fish/config.fish` as
   `set -x HERMES_TUI_NO_CONFIRM 1`, AND to `~/.bashrc` after the guard
   (so interactive bash still sees it). For non-shell processes started
   from a desktop launcher, you'll also need to set it in the launcher's
   env (Windows shortcut → "Properties → Environment").

2. **Hermes overrides with config.yaml.** Some env vars are *bridged* from
   `config.yaml` keys by `apply_terminal_config_to_env(env=env)` in
   `hermes_cli/config.py:6829`. That helper only touches keys in
   `TERMINAL_CONFIG_ENV_MAP`. If your env var is not in that map, it's
   safe — but if the *config.yaml* key exists and the file has a
   `terminal:` section, the file value wins and overrides your env export
   (`should_override = file_has_terminal_config`).

3. **Node child process.** When the Python parent `os.execvp`'s the TUI
   Node bundle, env passes through `os.environ.copy()` (see
   `hermes_cli/main.py:_launch_tui`). It WILL inherit, but only if it
   was in the parent's env in the first place — i.e. the shell that
   started `hermes` had it set.

## Step 3: Verify before claiming fixed

Don't just write the config and report done. Verify the variable is
actually visible in the runtime that needs it:

```bash
# Did the value reach the TUI Node process? Inspect from inside.
# Inside TUI, run a shell command; the spawned bash inherits TUI's env.
bash -c 'echo "HERMES_TUI_NO_CONFIRM=$HERMES_TUI_NO_CONFIRM"'

# Or from outside: find the TUI node PID and read its env.
pgrep -af 'tui_gateway.entry|ui-tui' | head
# Then in a Python one-liner:
python3 -c "import os; pid=12345; print(open(f'/proc/{pid}/environ').read().split(chr(0))[:20])"
```

If the env var is unset in the target process, walk back up the chain
until you find where it was lost — usually shell rc file.

## Step 4: When there's no gate at all

Some modals are unconditional. `grep` will find a `patchOverlayState({...})`
or `input(...)` call with no `if (NO_CONFIRM_X) return commit()`. In that
case:

- The fix is a code change, not a config change.
- Check upstream issues / changelog — the gate may have been added after
  the version you're on. `hermes --version` and compare.
- If the user wants the gate added, point them at the right file and line
  number so they can decide whether to patch locally or wait for upstream.

## Known surface splits (use as a reference table)

| Behavior | CLI gate | TUI gate | Gateway gate |
|----------|----------|----------|--------------|
| `/new` / `/clear` / `/reset` / `/undo` confirmation | `approvals.destructive_slash_confirm: false` in config.yaml | `HERMES_TUI_NO_CONFIRM=1` env | `approvals.destructive_slash_confirm: false` (via slash-confirm buttons) |
| `/reload-mcp` confirmation | `approvals.mcp_reload_confirm: false` | n/a (uses same env as destructive) | `approvals.mcp_reload_confirm: false` |
| Model switch (expensive model warning) | gate in `cli.py` + per-session suppression | gate in TUI command | per-platform native button |
| Voice/TTS enable | `voice.*` in config.yaml | n/a | n/a |

The pattern: `approvals.*` keys live in `config.yaml` and are read by both
the Python CLI and the gateway (which has its own `gateway/run.py`
config-loader). The TUI is the odd one out — it's a Node process and reads
`HERMES_TUI_*` env vars only. Documented in
`hermes_cli/config.py:2542-2548` ("TUI has its own modal overlay
(HERMES_TUI_NO_CONFIRM=1 to opt out there)") — when you find a "TUI
doesn't honor my config.yaml setting" report, this comment is the smoking
gun.

**Case study**: the destructive-confirm dialog is the canonical example —
see `references/destructive-confirm-surfaces.md` for the full
surface-by-surface breakdown, button-label fingerprints, code locations,
and the WSL+fish+bashrc trap that causes the env var to silently miss
the target.

## Pitfalls

- **Don't trust config.set's success message alone.** `hermes config set`
  writes the file and reports success, but the surface you care about
  may not be reading that file path. Always check the actual rendered
  behavior, not the config state.
- **Don't grep paraphrase.** "Confirmation dialog" matches 200 lines and
  tells you nothing. The exact button labels match 1-5 lines and tell
  you everything.
- **Don't fix the wrong surface.** Most "I set the flag, still prompts"
  tickets are closed by changing the same flag the user already tried,
  just on the correct surface. Verify by reading the rendered button
  text, not the user's description.
- **WSL + fish trap.** `~/.bashrc` exports are invisible to the fish
  session the user is actually in. Don't believe the value is set
  because `tail ~/.bashrc` shows it.
- **Restart ≠ re-source.** A running TUI's env is frozen at process
  start. After changing rc files, the user must close all TUI windows
  and open a new one. `hermes` re-reading config.yaml doesn't reload
  `process.env` in the running Node bundle.
