---
name: build-sub-feature
type: Skill
title: "build-sub-feature — add a capability INTO a live feature, to a world-class bar"
description: "Doctrine for adding a capability INTO a live, existing feature to a world-class bar. Use on 'add X to Y', 'extend Y to support X', a new option, button, setting, endpoint, or tool for Y, or a sub-feature spec to implement. NOT for whole-feature audits or overhauls (use feature-deep-dive)."
tags: [execution, features, implementation, doctrine]
timestamp: 2026-09-10T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/build-sub-feature/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Build a Sub-Feature

You're implementing a new sub-feature — an addition to something that already exists in the platform. The spec comes from the user (interview below); the standards are non-negotiable acceptance criteria. Implement to them, and loop until the result actually satisfies them. You're done when it's real, complete, verified, and at parity or better with the discipline's champion (`common-docs/policies/champions.md`) — not before.

This isn't greenfield. It's an addition to something live, so the surrounding system is your first concern, not an afterthought. Build so the whole ecosystem is better for this — not just the one spot it lands in.

**Not this skill:** whole-feature audits or overhauls (`feature-deep-dive`), greenfield standalone features, pure bug fixes, or trivial copy/style tweaks.

## Step 1 — Interview: nail the spec before touching code

If the invocation already includes a description, treat it as the overview and interview only for the gaps. Ask in plain numbered chat text — **never a structured question picker** (Arman ruled 2026-09-12); a picker blocks free-form replies.

Interview per the `grilling` skill (prune, frontier rounds, a recommendation on every closed question, skips ship as defaults). Specific here: round 1 holds only what exploration cannot answer. Send it, and **start exploring in the same turn**; do not wait for the answers. Say "exploring now — you can step away." Questions that come out of exploration join the next round. Stop when the frontier is empty.

**Ratchet:** if exploration shows this is really a whole-feature overhaul or several independent subsystems, say so in one line and switch to feature-deep-dive (or vision-to-fleet). Hidden complexity only ever moves the work to a heavier path, never a lighter one.

## Step 2 — Explore: know the ground

Before designing or writing anything, establish from the actual code: what this lands inside, what consumes it, what it depends on, what already exists to reuse, and which of the world's best systems already solve this problem well. The standards below tell you what to look for; exploration is where you look.

## Step 3 — Attack (when adding a contract, table, or cross-surface change)

Write a ≤20-line design note in scratch and run `plan-attack` (one reviewer) on it before writing code.

## The standards — non-negotiable acceptance criteria

**Reuse before you write.** Assume what you need already exists — a component, hook, utility, service, type, or pattern — and go find it. If it almost exists, extend the canonical one rather than forking a variant. Write something new only when nothing reusable fits, and when you do, write it so the next person consumes it instead of rebuilding it.

**Build into the ecosystem, not beside it.** Know the blast radius before you start: what consumes this, what it depends on, and whether the server, database, or shared packages need to change for it to be done *right*. If the backend needs a new contract to support this properly, that contract is part of the work — not a follow-up ticket. A sub-feature that works in isolation while ignoring everything around it is unfinished.

**Propagate across surfaces.** We ship on web, desktop, Chrome extension, mobile, and admin surfaces. Web usually goes first, but "done on web" is not "done." Put shared logic in shared code so every surface inherits it at once, then carry the change to each surface that needs it — or explicitly state why one is excluded. Never reimplement per surface what belongs in one place.

**No legacy — until go-live.** We are pre-production with no outside code depending on us (~90 days from 2026-09-10), so if this replaces something, annihilate the old thing: delete it, repoint every caller at the new implementation, move every touched package to latest, and leave nothing behind — no shims, no compatibility layers, no fallback paths, no dead code. That freedom is one of the few structural advantages we hold over companies a thousand times our size — so we spend it on purpose, and it ends on go-live day, when customer-facing edges get versioned stability ([pre-launch-mode](/policies/pre-launch-mode.md)). The single exception: two approaches that genuinely coexist because we don't yet know which one wins. Name that explicitly. Everything else gets erased.

**Quality is the baseline, not the target.** Do it correctly and completely the first time — no half-wired states, no "good enough for now," no TODOs left as landmines. Compiling isn't working; it works when it's verified, handles the real edges, and reads like someone competent maintains it tomorrow.

**Mimic what works.** Before you design or implement, explicitly consider the best systems in the world that already do something similar — their principles, layouts, patterns, and concepts. Don't invent from scratch — reuse as much as possible from what has proven to work at scale. Agents produce significantly better results when they emulate excellence rather than reinvent mediocrity. The ruled set of leaders per discipline is `common-docs/policies/champions.md`; absorb what makes them successful and apply those patterns here. Stand on the shoulders of giants.

## Done means

The sub-feature fully delivers what was specified, the next person could reuse what you built, every surface that needs it has it, everything it touches across the stack has been brought along, and not a single trace of the old way is still alive. Verified by exercising it — not by it compiling. If any of that is untrue, you're not finished — keep going.

Build something incredible.
