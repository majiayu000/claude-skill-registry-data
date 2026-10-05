---
name: tui-observe-first
description: >-
  Use when building, fixing, polishing, or comparing any terminal UI —
  ratatui/crossterm REPLs, agent CLI chrome — or when a TUI shows a frozen
  spinner, dead keys, duplicated responses, stale cells, flicker, resume
  failures on dangling tool_use, or when you need side-by-side screenshots
  against reference CLIs.
---

# TUI observe-first

A TUI is judged **rendered in a real terminal**, never from its source. Render
it, screenshot it, compare it against strong CLIs at the **same terminal grid**,
and cite a screenshot for every finding and fix. Terminal sibling of
`ui-fix-observe-first`.

## The comparative loop

1. **Reference set**: spawn the CLIs you must beat (e.g. claude, codex, droid)
   and your TUI in the **same** rendering stack and viewport. Reuse the same
   browser/PTY tab for every capture — a resized tab makes an unfair comparison.
2. **Capture the same CUJ moments**: welcome, empty composer, slash palette,
   streaming/working, tool receipts, permission dialog, error, interrupt, quit.
3. **Teardown**: every finding cites a screenshot. No screenshot = not a finding.
   Rank by impact; fix one issue-class at a time.
4. **Re-render after every rebuild**, then dogfood real turns (tools, interrupts).
   Many worst bugs only appear live.

## What a strong agent TUI usually has

| Element | Shape |
|---|---|
| Welcome header | Logo + name/version, model · permission-mode, cwd · session — few lines |
| Bottom bar | Mode + key hints left; model · session · cost · ctx% right |
| Working line | Spinner + verb + elapsed + interrupt hint + queued count |
| Turn / tool receipts | Compact status; collapsed summaries, not raw dumps |
| Text | Markdown-lite: bold, inline code, tinted fences |
| Palette | Ranked search; clear selected row; dim aliases |
| Dialogs | Clear selection + quick keys + hint row |
| Input | Distinct prompt; status lives outside the input line |
| Flow | Type-to-queue while running; Esc interrupts; Ctrl+C arms quit |

## Render-loop laws

- **Never await a shared engine/session lock in the render loop.** Clone handles
  out and poll with `try_lock`, or the spinner, timer, and keyboard freeze.
- **Every new-turn path goes through one `begin_turn()`** that stamps start time.
  Setting `Running` without a stamp freezes a 0s spinner.
- **Drain completion channels before finalizing** a turn, or leftover deltas
  duplicate response blocks.
- **`Clear` the full frame before drawing** — otherwise stale cells bleed through.
- **Set the terminal cursor explicitly** from the edit column.
- **Repair histories at session load**: dangling `tool_use` without `tool_result`
  breaks resume (API 400). Insert synthetic error tool_results at load.
- **TestBackend tests gate layouts** — they are not proof; screenshots are.

## Capture traps

- Compare only at the same font/grid/renderer as your references.
- Browser attach pages can swallow Escape / chords — reproduce keyboard bugs
  against the raw PTY before changing code.
- Scrollback / ready-regex must match the **current** UI string after redesigns.
- `cargo test | tail` can eat exit codes — capture status yourself.

## Common mistakes

| Mistake | Reality |
|---|---|
| "It compiles / tests pass, ship it" | Many TUI bugs have green tests. Render + dogfood. |
| Diagnosing look/flow from source | Freeze, bleed-through, grid width, timing do not live in code. |
| Different tabs/sizes for comparisons | PTY grid follows viewport — same tab, same size. |
| Restyling without a reference set | Capture references first, then rank gaps. |

## Cross-references

- `ui-fix-observe-first` — web sibling (render → measure → cite → fix)
