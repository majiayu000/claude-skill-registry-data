---
name: debug-microflows
description: "Drive the Mendix runtime's microflow and nanoflow debugger from the command line with `mxcli debug` — breakpoints by name, variable inspection, step and continue. Use when a microflow produces the wrong result and reading it is not enough."
---

# Debug Microflows — `mxcli debug`

## Overview

`mxcli debug` drives the Mendix runtime's **microflow debugger** from the command
line: set breakpoints **by name**, inspect a paused microflow's variables, and
step/continue — against an app started by `mxcli run --local`. It is the headless
counterpart to Studio Pro's debugger, so you can debug a server-side microflow
without leaving the warm loop.

mxcli is uniquely able to offer breakpoints **by name** because it owns both
halves: the admin password + app URL (from `run --local`) and the activity model
GUIDs (from the `.mpr`). You never deal with raw GUIDs.

## When to use this skill

- A page action throws or misbehaves and you need to see *where* in a microflow it
  goes wrong, with the in-scope variables.
- You want to confirm a microflow takes the branch/value you expect.

For a server **stack trace / `LOG` output** (not stepping), you usually just want
the runtime log — see `run-local` (`--runtime-log`). Use the debugger when you
need to **pause and inspect** live execution.

## Prerequisites

- The app running under `mxcli run --local` (Mendix 11.x).
- Start it with **`--debug`** so the debugger is enabled and a session is ready:

  ```bash
  mxcli run --local -p app.mpr --debug
  ```

  `--debug` alone does **not** change runtime behaviour — nothing pauses until you
  set a breakpoint. It caches a debug session token under `<projectDir>/.mxcli/`
  so the `mxcli debug` commands below (run from another terminal, **same `-p`**)
  work immediately, with no separate `mxcli debug enable`.

## The loop

```bash
# terminal 1: app + debugger
mxcli run --local -p app.mpr --debug

# terminal 2: find the activity, break on it by name
mxcli debug activities Sudoku.ACT_Hint -p app.mpr
mxcli debug break Sudoku.ACT_Hint --activity 'Retrieve' -p app.mpr

# now trigger the microflow in the browser — the request pauses. Then:
mxcli debug paused -p app.mpr                 # which flow is paused + its variables
mxcli debug inspect Game -p app.mpr           # one variable in detail
mxcli debug step over -p app.mpr              # over | into | out
mxcli debug continue -p app.mpr               # resume (the browser request completes)

# when done — ALWAYS:
mxcli debug disable -p app.mpr
```

## Commands

| Command | What it does |
|---------|--------------|
| `mxcli debug status` | Is the debugger on? How many microflows are paused? |
| `mxcli debug enable` / `disable` | Turn the debugger on/off (use `--debug` on `run --local` instead of `enable` for the warm loop) |
| `mxcli debug activities <Module.Flow>` | List a microflow's activities with the object IDs you can break on |
| `mxcli debug break <Module.Flow> --activity <#n\|caption> [--if <expr>]` | Set a breakpoint, resolved by name (`--if` = conditional) |
| `mxcli debug unbreak <Module.Flow> --activity <#n\|caption>` | Clear a breakpoint |
| `mxcli debug breaks` | List the breakpoints mxcli has set this session (name → object ID) |
| `mxcli debug paused` | Show paused microflows + full state (variables) |
| `mxcli debug inspect <var> [--list] [--flow <debug_id>]` | Inspect one variable of a paused flow (`--list` for a list variable → `get_list`) |
| `mxcli debug step [over\|into\|out] [--flow <debug_id>]` | Advance one step (default `over`) |
| `mxcli debug continue [--all]` | Resume the paused flow (or all with `--all`) |

Selecting an activity: `--activity '#2'` (the index from `activities`) or a
caption substring like `--activity 'Retrieve'` (must match exactly one, case-
insensitive). Selecting a paused flow: `--flow <debug_id>` (from `paused`); with a
single paused flow it is auto-selected.

## Nanoflows (client-side)

`mxcli debug` works for **nanoflows** too — `break`/`activities`/`unbreak` auto-detect
whether `Module.Flow` is a microflow or a nanoflow and set the breakpoint the right
way (a nanoflow needs the `nanoflow_name` param; the wrong key NPEs the runtime —
mxcli handles this for you). Break by name exactly as for a microflow:

```bash
mxcli debug break Sudoku.NF_ToggleNotes --activity 'Change' -p app.mpr
```

A paused **nanoflow** does not appear in `get_paused_microflows` — it surfaces only
in the runtime's `poll_events`. `mxcli debug paused` (and `step`/`inspect`/`continue`)
merge both sources, so a paused nanoflow shows up with its `debug_id` like any other;
its variables are in the "Client events (poll_events)" section of `paused`.

Symptom of a paused nanoflow **without** mxcli: a frozen browser, the console logging
"Starting execution" but never "Finished", and `mxcli debug status` showing
`client_connected: true`.

**Nanoflow `debug_id` is single-use.** Unlike a microflow (stable id), a nanoflow
gets a **new** `debug_id` after every step — the old one is invalidated. Because each
`mxcli debug` command re-reads the current state, just let `step`/`inspect`/`continue`
**auto-resolve** the flow (don't pass `--flow`): a bare `mxcli debug step over` picks up
the fresh id each time. Reusing a `--flow <debug_id>` copied from an earlier `paused`
will fail on the second nanoflow step with "could not find … in debug with id".

For **nanoflow log output**, see `write-nanoflows` — the runtime rewrites the log
node to `Client_Nanoflow`, so grep `runtime.log` for `Client_Nanoflow`, not your node
name.

## Gotchas

1. **A breakpoint pauses whoever hits it — the browser included.** The triggering
   request hangs until `continue` (or `disable`). This is normal; just don't walk
   away from a paused session.
2. **Always finish with `mxcli debug disable`.** `run --local --debug` disables it
   for you on shutdown, but if you enabled it by hand, turn it off by hand.
3. **Use the same `-p` everywhere.** The session token and breakpoint record live
   under `<projectDir>/.mxcli/`; a different `-p` (or none) looks in a different
   place and won't see the session `run --local --debug` started.
4. **Conditions are Mendix expressions** (`--if '$Game/Solved = false'`), same
   syntax as a Studio Pro conditional breakpoint.
5. **Overriding the target runtime:** `--app-url`, `--admin-port`, `--admin-pass`,
   `--debug-pass` (or `MXCLI_APP_URL` / `MXCLI_ADMIN_PASS` / `MXCLI_DEBUG_PASS`)
   default to a `run --local` runtime; set them to debug a differently-configured
   or remote runtime.

## Validation checklist

- [ ] App started with `mxcli run --local --debug`.
- [ ] `mxcli debug status` shows `enabled`.
- [ ] `mxcli debug activities <Module.Flow>` lists the activity you want.
- [ ] After triggering the flow, `mxcli debug paused` shows it with variables.
- [ ] Finished with `mxcli debug disable`.

## Microflow/nanoflow debugger (`mxcli debug`)

set breakpoints **by name** (activity resolved from the model), inspect paused flows + variables, step over/into/out, continue — against a `run --local` runtime. Two M2EE planes wired behind one command (admin `enable/disable/status`, app `/debugger/` session); `run --local --debug` enables it at boot. **Nanoflows** are auto-detected (uses the `nanoflow_name` breakpoint param; paused nanoflows are merged from `poll_events`, which `get_paused_microflows` omits). Nanoflow `LOG` output is rewritten to the `Client_Nanoflow` node in the runtime log. and `docs/11-proposals/PROPOSAL_microflow_debugger.md`
