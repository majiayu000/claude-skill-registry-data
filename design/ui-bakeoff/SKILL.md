---
name: ui-bakeoff
description: "Orchestrator that runs one UI brief through all four ui-* posture skills in parallel, then picks and merges a winner. Use when a screen matters enough to explore several directions, or the user says 'build it a few ways', 'design options', 'bake-off', 'show me variations', or 'compare approaches'."
---

# ui-bakeoff — design it four ways, then pick and merge

Running the same brief through four different design postures in parallel, then choosing the best and merging the rest, is the most reliable way to get a great UI here. This skill orchestrates that. You (the agent that triggered this skill) are the conductor — you interview, you spawn, you present, you merge. You do **not** design anything yourself.

## The environment constraints — design around these

- You **can** run subagents in parallel — issue all four `Agent` calls in a single message so they run concurrently.
- Subagents **cannot** stop to ask the user questions — they run autonomously to completion. The interview therefore cannot happen inside them.
- **So you, the conductor, run the interview once, up front**, and inject the answers into all four subagents. This is the whole reason the interview lives here and not in the children.

## Step 1 — Merge the interviews, ask once, in prose

Read the **"Interview first"** section of all four posture skills:
- `.claude/skills/ui-sharp/SKILL.md`
- `.claude/skills/ui-reimagine/SKILL.md`
- `.claude/skills/ui-refine/SKILL.md`
- `.claude/skills/ui-dense/SKILL.md`

Take the **union** of their questions, dedupe the overlap (persona / primary job / reference recur across all four), and ask the user the combined short list — **in plain numbered chat text, never a structured question picker** (Arman ruled 2026-09-12). Always include the two universal ones:
- Who is this for and what's the one job they came to do?
- What in the current version already works and must NOT be regressed?

Keep it tight. If the user says "just go," proceed with your best inferences and tell them what you assumed.

## Step 2 — Spawn four parallel subagents (one message, four `Agent` calls)

Each subagent gets **identical** instructions: the brief + the interview answers + an explicit "the interview is already done — do NOT ask the user anything; build with these answers." Tell each to read `ground-rules.md` + `design-system-anchors.md` (paths in `.claude/ui-skills/shared/`) **and its one assigned posture skill**, and name which posture it is. Assign:

- subagent 1 → **ui-sharp**
- subagent 2 → **ui-reimagine**
- subagent 3 → **ui-refine**
- subagent 4 → **ui-dense**

**Keep each subagent prompt minimal — this is the most important rule here.** Tell it only: which surface(s) to redesign and where they currently live, to read its assigned posture skill + the shared floor, where to build, and to build it real. **Do NOT add design direction, component names, "reuse X", "rebuild only the presentation," or any verification choreography.** Every such instruction you add silently overrides the skill and flattens the result back toward the existing UI — this is the documented way a bake-off loses all its creativity. The skill carries the design intelligence; your job is to get out of its way. The *only* exception: a posture the user gave specific guidance for — pass that guidance verbatim, and nothing more of your own.

## Step 3 — REAL, not fake (hard rule, no exceptions for real work)

Every subagent builds a **real, fully-wired implementation** against the actual data, service, and stream — with real loading / empty / error / stalled-stream handling — **not a mock demo.** (This is ground-rules §1, the rule that matters most. A bake-off of fakes teaches you nothing about the unknowns that actually kill a page.)

To let four real implementations run in parallel without colliding, give each its **own route** (e.g. `…/create-sharp`, `…/create-reimagine`, `…/create-refine`, `…/create-dense`) — never a git worktree or branch (this repo is one shared checkout on `main`). If two variants would touch the same shared file, give each its own copy under its route instead. Confine each subagent to its own route/files. Each must **verify it runs against real data** — including an error and an empty path — before reporting.

> Only stub if the user *explicitly* asks for a throwaway visual exploration (skill/design experimentation, not feature work) — and then say so loudly. Default is always real.

## Step 4 — Present, recommend, then merge

Collect the four. For each, summarize: the posture, the reference product it chose, its standout features, and its weak spots. Recommend a winner with reasoning. Then offer the **consolidation pass**: spawn one more agent that takes the winner as the base and grafts the *specific* strengths the user liked from the others ("take reimagine's stream animation, refine's error state, dense's table") into a **single real, canonical implementation on the true route** — then delete the throwaway variant routes.

## Notes

- Real implementations on **parallel routes** so the user can view all four on one dev server; no worktrees.
- The four postures are designed to diverge — converging outputs usually means the brief over-specified the design. If that happens, loosen the brief (say only *what the surface is and must do*) and let the postures express themselves.
