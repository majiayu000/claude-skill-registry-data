---
name: pi-plugin-dev
description: Build, run and debug pi extensions by observation — tmux-driven TUI sessions, color screenshots, session digests, and a replay provider for deterministic tool calls. Use when developing, fixing or reviewing a pi extension, tool, command, renderer, overlay or theme; when an extension fails to load or a tool is never called; or when asking how something renders.
compatibility: Requires tmux, nix and python3.
---

A pi extension runs inside the host process, so the thing under test is a running session, not a function. Observe a real session, then read what the model was actually offered.

`scripts/tui.sh` drives a session. `scripts/digest.py` flattens one session file into the facts that matter. `assets/fixture-provider.ts` replays canned assistant turns so tool paths cost nothing.

## Tools

| Command                                          | Does                                                              |
| ------------------------------------------------ | ----------------------------------------------------------------- |
| `tui.sh start [--cols N --lines N] [-- pi args]` | New session in tmux, session file under the run dir               |
| `tui.sh wait <regex> [secs]`                     | Block until the pane matches, default 20s                         |
| `tui.sh cap [-e]`                                | Pane text to stdout, also saved; `-e` keeps ANSI                  |
| `tui.sh type <text>` / `tui.sh keys <key...>`    | Literal text / named keys (`Enter`, `Tab`, `Escape`, `C-c`, `Up`) |
| `tui.sh resize <cols> <lines>`                   | Re-lay out at another width                                       |
| `tui.sh shot [file]`                             | Color PNG of the current pane                                     |
| `tui.sh digest [file]`                           | Digest the newest session file of this run                        |
| `tui.sh stop`                                    | Kill the session                                                  |

Run dir: `~/.local/share/agents/pi-plugin-dev/<dir-hash>/`. Sessions are per working directory, so `tui.sh` works from wherever the plugin lives without naming anything.

## The loop

```bash
skills/pi-plugin-dev/scripts/tui.sh start -- --extension ./todo.ts
skills/pi-plugin-dev/scripts/tui.sh wait 'todo|error|Extension'
skills/pi-plugin-dev/scripts/tui.sh cap
```

`cap` first: startup diagnostics are the fastest signal there is. Then drive it (`type '/todo add x'`, `keys Enter`), `cap` again, and `digest` when the question is about tools, events, entries or cost.

## Failure modes

| Symptom                                 | Look at                                                                                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Extension absent, or a conflict warning | `cap` at startup. `[Extension issues]` names the file and the exact conflict                                                               |
| Tool never called                       | `digest`: is it in the declared set? Is `exposure` what you expect? A `hidden` tool is registered and unreachable                          |
| Tool called, wrong result               | `digest` pairs `toolCall` with `toolResult`; an `isError` result with no thrown error means `execute()` returned rather than threw         |
| Renders wrong                           | `cap` for text and widths, `shot` for color. Verify at 60 and 160 columns                                                                  |
| Works in TUI, breaks headless           | Re-run with `--mode rpc`. `ctx.ui.custom()` returns `undefined` there, `getTheme()` returns `undefined`, `setEditorComponent()` is a no-op |

## Traps

These are the ones that pass a casual look and break in use:

- Processes, sockets, watchers and timers started in the factory instead of `session_start`. Some invocations load extensions without starting a session.
- Cleanup that is not idempotent in `session_shutdown`, or missing entirely. Reload, cancellation, session replacement and exit all converge there.
- Module-level mutable state across `ctx.reload()`. Everything after `await ctx.reload()` runs in a new runtime; do not reuse captured state.
- Theme-colored strings cached without `invalidate()`. Theme changes clear render caches but cannot recolour strings already embedded in state.
- Renderer output built without `visibleWidth`/`truncateToWidth`. Measure columns, not `length`, and wrap wide characters and emoji.
- Branch state rebuilt from every entry. Use `ctx.sessionManager.getBranch()`, or a fork shows state from an abandoned branch.
- `pi.setActiveTools()` with names that are not registered yet. Unknown names are ignored silently. Register first, then activate.
- `ctx.ui.custom()` without a `ctx.mode === "tui"` guard.
- `content` and `details` confused: `content` is model-facing, `details` reconstructs state. `undefined` is a valid `details`.

## Deterministic runs

Prompting a real model to exercise an error path is slow, costly and flaky. Register the replay provider instead:

```bash
FIXTURE=$PWD/turns.json skills/pi-plugin-dev/scripts/tui.sh start -- \
  --extension skills/pi-plugin-dev/assets/fixture-provider.ts \
  --provider fixture --model replay
```

`turns.json` is a list, consumed in order, one entry per assistant turn:

```json
[
  { "text": "Listing files." },
  { "toolCall": { "name": "todo", "arguments": { "op": "add", "text": "x" } } },
  { "toolCall": { "name": "todo", "arguments": { "wrong": "shape" } } },
  { "error": "provider exploded" }
]
```

A turn can carry `text`, `thinking`, `toolCall` or `error`. Malformed arguments are the point: they exercise validation and tool-call error paths without waiting on a model.

## Limits

- `digest.py` reports what the session recorded: declared tools, calls, results, entries, cost. It cannot see tools that were registered but never declared, so "registered but invisible" is a `pi.getAllTools()` question, asked from inside the extension.
- A digest shows that a tool ran, not whether the model had a fair chance of picking it. Tool-choice quality needs one real prompt.
- Screenshots use Nerd Font PUA glyphs for some chrome icons; those can rasterize as boxes depending on the font available to the rasterizer. Read `cap` for glyph identity, `shot` for color and layout.
