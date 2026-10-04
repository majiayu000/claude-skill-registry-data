---
name: pd-showcase
description: >
  Toggle PD showcase mode on/off for live demos. When ON, /pd-spawn and /pd-resume
  spawn PDs in the foreground with verbose narration so the audience sees every
  tool call, reasoning step, and decision in real-time. When OFF (default), PDs
  run silently in the background as usual. Invoke as /pd-showcase on, off, or
  status. State is a single marker file at ~/.claude/state/pd-showcase.flag —
  read by pd-spawn and pd-resume at spawn-time.
---

# /pd-showcase — Demo Visibility Toggle

A single marker file flips PD-spawning skills between two modes:

- **OFF (default)** — PDs spawn with `run_in_background: true`, silent until done.
- **ON (showcase)** — PDs spawn with `run_in_background: false` and a narration
  directive injected into their briefing. Every tool call and decision is
  visible in the main session. Trade-off: one PD at a time, main session blocks.

## SSOT

Flag file: `~/.claude/state/pd-showcase.flag`
- Exists → showcase ON
- Absent → showcase OFF

The file's contents are advisory (timestamp + reason) but only its existence
matters. `pd-spawn` and `pd-resume` test for presence via `test -f`.

## Argument Parsing

Accept one of:
- `on` | `enable` | `start` — turn showcase on
- `off` | `disable` | `stop` — turn showcase off
- `status` | (no argument) — report current state
- `toggle` — flip whatever the current state is

## Step 1 — Determine Action

From the slash-command argument, pick one of: `on`, `off`, `status`, `toggle`.

If the argument is missing or unrecognized, default to `status` (read-only).

## Step 2 — Read Current State

Check whether `~/.claude/state/pd-showcase.flag` exists. Record the result
as `currently_on = true | false`.

## Step 3 — Apply Action

**`on` (or `enable`, `start`):**
1. If `currently_on` → output "Showcase already ON — no change." and stop.
2. Otherwise, write `~/.claude/state/pd-showcase.flag` with body:
   ```
   enabled_at: {ISO timestamp}
   note: PD showcase mode — foreground spawns + narration injected
   ```
3. Output the "ENABLED" confirmation (see Step 4).

**`off` (or `disable`, `stop`):**
1. If not `currently_on` → output "Showcase already OFF — no change." and stop.
2. Otherwise, delete `~/.claude/state/pd-showcase.flag`.
3. Output the "DISABLED" confirmation (see Step 4).

**`toggle`:**
- If `currently_on` → run the `off` branch.
- Else → run the `on` branch.

**`status` (or no argument):**
- Read the flag file body if present; show timestamp and note.
- Output the "STATUS" report (see Step 4).

## Step 4 — Output Format

**ENABLED:**
```
PD SHOWCASE: ON
  Flag: ~/.claude/state/pd-showcase.flag
  Effect: Next /pd-spawn and /pd-resume run PDs in the foreground with verbose narration.
  Trade-off: One PD at a time. Main session blocks until each PD finishes.

To turn off: /pd-showcase off
```

**DISABLED:**
```
PD SHOWCASE: OFF
  Flag removed.
  Effect: Next /pd-spawn and /pd-resume return to silent background spawning.
```

**STATUS (when ON):**
```
PD SHOWCASE: ON (since {enabled_at})
  Note: {note from flag body}
  Flip with /pd-showcase off or /pd-showcase toggle.
```

**STATUS (when OFF):**
```
PD SHOWCASE: OFF (default)
  Flip with /pd-showcase on or /pd-showcase toggle.
```

## How pd-spawn and pd-resume Honor Showcase Mode

**Two activation paths — both explicit, neither automatic:**

**Path A — Per-invocation flag (`--showcase` argument):**
Pass `--showcase` directly to `/pd-resume` or `/pd-spawn`. Showcase activates for
that spawn only. The flag file is not read or written.
```
/pd-resume ltv --showcase
/pd-spawn ltv --showcase
```

**Path B — Persistent demo session (`/pd-showcase on` toggle):**
For a live demo where you want all subsequent PD spawns to use showcase mode,
run `/pd-showcase on` first. This writes the flag file. Subsequent `/pd-resume`
and `/pd-spawn` calls check for the flag IF `--showcase` was not explicitly
passed. Run `/pd-showcase off` to end the demo session.

**The default behavior:**
Without `--showcase` AND without a prior `/pd-showcase on` in this session,
`pd-resume` and `pd-spawn` NEVER check the flag file. They default to
background + silent mode. The flag file on disk has zero effect unless
`/pd-showcase on` was explicitly run.

**pd-resume Step 2.5 logic (simplified):**
```
if args.include("--showcase"):
    showcase_on = true
elif pd_showcase_on_was_run_this_session:
    showcase_on = test -f ~/.claude/state/pd-showcase.flag
else:
    showcase_on = false   # no file probe
```

**pd-spawn Step 4.5 logic (same pattern):**
Same as pd-resume. Only probe the flag file when `/pd-showcase on` was explicitly
invoked in the current session. `--showcase` argument takes precedence.

## Showcase Narration Directive (injected into PD briefing when showcase_on = true)

```
--- SHOWCASE MODE ---
A live audience is watching this session. Optimize for comprehension over speed:

1. Before each tool call, write ONE short sentence explaining what you're
   about to do and why.
2. After each tool result, write ONE short sentence summarizing what you
   learned before choosing the next step.
3. When deciding between approaches, narrate the trade-off out loud
   ("I could either X or Y — going with X because...").
4. When you finish a phase (research, planning, implementation, verification),
   call it out explicitly so the audience knows where you are.

Keep narration tight — one sentence each, no lectures. The audience reads
your tool calls; you just connect the dots.
--- END SHOWCASE MODE ---
```

## Notes

- **Default is OFF and stays OFF** — no per-resume flag probe. Showcase only
  activates when explicitly requested (`--showcase` arg or `/pd-showcase on`).
- The flag file persists until explicitly cleared with `/pd-showcase off`.
  After a demo, always run `/pd-showcase off` to prevent leakage into the next session.
- This toggle does NOT affect Curator, Delegator, codebase-search, or any
  non-PD agent. Only `/pd-spawn` and `/pd-resume` honor it.
- If a PD spawn blocks the main session unexpectedly, check flag state with
  `/pd-showcase status`, then `/pd-showcase off` to restore background mode.
