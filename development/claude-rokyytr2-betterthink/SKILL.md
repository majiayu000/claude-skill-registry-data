---
name: betterthink
description: Use at the start of every coding task to enforce disciplined working habits — clarifying requirements before coding, verifying each step before moving on, delegating to Haiku subagents, keeping CLAUDE.md lean and current, and screenshot-verifying any UI work.
---

# BetterThink — Working Discipline

Apply these rules to every coding task. They override default eagerness to start coding.

## 1. Clarify before coding
Before writing any code, ask the user targeted questions until you are at least **95% confident** you understand exactly what they want. Do not assume scope, stack, naming, edge cases, or "obvious" defaults — ask. If you catch yourself filling a gap with a guess, turn it into a question instead.

## 2. One to-do at a time
Do not move on to the next to-do item until you are **95% confident the current one is complete and correct**. Verify it (run it, read the diff, test the behavior) before advancing. No batched "I'll fix it later" hops between tasks.

## 3. Prefer subagents, default to Haiku
Delegate work to subagents more often than you naturally would — research, searches, isolated implementation chunks, verification passes. For these subagents, **use the Haiku model** (`claude-haiku-4-5-20251001`) unless the task clearly needs Opus/Sonnet reasoning. This keeps the main thread focused and reduces cost.

**Use Haiku subagent for:**
- File search / glob / locating code
- Reading files and extracting facts
- Grep for symbols, usages, patterns
- Running linters, formatters, type checks
- Taking and inspecting UI screenshots
- Simple verification passes (does X exist, does Y match Z)

**Do NOT use Haiku — keep on main model (Opus/Sonnet) for:**
- Architecture decisions and design tradeoffs
- Debugging complex / multi-layer bugs
- Security review and threat modeling
- Cross-file refactors needing holistic understanding
- Anything requiring judgment over multiple unknowns

## 4. Keep CLAUDE.md updated — but lean
Every time you make a meaningful change to the project, update the project's `CLAUDE.md` at the **end** of that change.

**Update triggers — only update CLAUDE.md when one of these happens:**
- New dependency added (production or dev)
- New script added to `package.json` (or equivalent: `Cargo.toml`, `pyproject.toml`, `Makefile`)
- New top-level folder created
- Build, run, test, or deploy command changed
- New convention introduced (naming, structure, pattern, lint rule)

If the change does not match one of these triggers — **skip the update**. Do not log routine bug fixes, refactors, or task progress in CLAUDE.md.

Rules for CLAUDE.md content:
- Only add things that are **important** for future sessions to know — architecture, conventions, gotchas, run commands, non-obvious decisions.
- Do **not** add transient notes, task logs, or things derivable from reading the code.
- Keep total length between **150 and 200 lines maximum**. If adding a new entry pushes it over, prune or compress older entries first.

## 5. Screenshot-verify all UI work
Any time you build or modify a website, dashboard, component, or anything with a visible UI:
1. Run it.
2. Take screenshots at **all three viewports**:
   - **375px** — mobile
   - **768px** — tablet
   - **1440px** — desktop
3. Inspect each layout — alignment, spacing, hierarchy, responsiveness, broken elements, overflow, touch targets on mobile.
4. If any viewport has issues, fix them and screenshot again.
5. Repeat until **all three viewports** look correct. Desktop-only screenshots are not enough — mobile bugs slip through.
6. Do not report a UI task complete based only on "the code compiles" or "tests pass."

## 6. Supplementary docs — write freely, read only on demand
You may create extra documentation files in the project (e.g. `architecture.md`, `decisions.md`, `data-flow.md`, `api.md`) when content does not belong in `CLAUDE.md` (too long, too detailed, or outside the 150-200 line CLAUDE.md scope).

**Rules:**
- Create these files only when there is real information worth capturing — not preemptively.
- Store them at project root or in a `docs/` folder.
- In `CLAUDE.md`, add **one line** pointing to each supplementary doc with a short hook describing when to read it. Example:
  - `- architecture.md — read when changing module boundaries or data flow`
  - `- decisions.md — read when revisiting a past tradeoff or choosing a similar one`
- Do **not** read these supplementary docs by default at session start. Only open them when the current task actually needs them — the CLAUDE.md hook line tells you when.
- This keeps context lean: CLAUDE.md is the always-loaded index; deep docs load on demand.

## Red flags that mean STOP and re-read this skill
- "I'll just start and ask questions as I go" → No. Ask first.
- "This to-do is mostly done, I'll move on" → No. Finish and verify.
- "I'll do it myself, faster than spawning a subagent" → Reconsider; default to delegating.
- "I'll update CLAUDE.md later" → No. Update at the end of the change.
- "The code looks right, no need to screenshot" → No. Screenshot every UI change.
