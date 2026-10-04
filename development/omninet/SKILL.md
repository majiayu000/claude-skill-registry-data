---
name: omninet
description: ChefFlow task router for choosing the smallest correct set of repo skills and safety rules before work starts. Use at the start of ChefFlow tasks, ambiguous requests, multi-skill requests, build/debug/review/research/planning work, or when deciding whether to queue, route, or implement.
user-invocable: true
---

# Omninet

Omninet is a lightweight routing loop. It does not run every skill. It decides which rules and skills apply, reports missing skills, and keeps work inside ChefFlow hard stops.

## Routing Loop

1. Read the user request and classify it as intake, queue, fire/build, debug, review, research, ship, health/status, docs, skill maintenance, or app implementation.
2. Apply always-on rules first: `AGENTS.md`, dirty workspace protection, database and git hard stops, Build Queue First, and direct work exceptions.
3. Load any skill named by the user if its `SKILL.md` or `skill.md` exists.
4. Load only the most specific implied skill for the classified task. Do not load the whole inventory.
5. If a referenced skill is missing, say it is missing and use the nearest available fallback.
6. If the request is broad, risky, or spans independent domains, prefer queue planning or a bounded execution plan before editing.
7. Before code edits, inspect `git status --short`, current branch, and likely file ownership.
8. After code edits, verify with the smallest commands that prove the changed surface.

## Skill Contract

- Always active: repo safety rules, queue policy, dirty workspace rule, and user instructions.
- User-named skill: load when present; report and fallback when missing.
- Implied skill: load only when the task clearly matches its trigger.
- Missing skill: never pretend it ran.
- Historical skill reference: treat as guidance only until a current skill file exists.

## Common Routing

- Casual feature idea: spec intake first, then queue if requested.
- `queue`, `backlog`, `save`, `batch`: use `build-queue`.
- `fire`, `build the queue`, `execute queue`: use `build-queue` firing rules.
- Bug, broken, failing, regression: use `debug` or `diagnose`.
- Code review: use `review`.
- Ship, commit, push, close out: use `ship` or `close-session`.
- Skill drift, missed rule, recurring behavior: use `heal-skill` for one failed skill or `write-a-skill` for a new skill.
- Broad research: use `research`.
- Live web/app/search inspection, screenshots, logged-in/session-personalized flows, ChefFlow route studies, or evidence-backed UX/SERP/local research: use `live-browser-experience-audit`.
- Architecture/refactor: use `improve-codebase-architecture`.
- Price, cost, ingredient cost, PIE, pricing: use the matching `pie-*` skill (`pie-measure`, `pie-forecast`, `pie-simulate`, `pie-census`, `pie-ratchet`, `pie-accuracy`, `pie-alert`, `pie-fix`).
- Session start, resume, status, context: use `morning` (fresh), `pick-up` (resume), `status` (quick check), or `warmup` (pre-work).
- Connect, wire, integrate, hook up: use `wire` for new connections, `wiring-audit` for checking existing.
- Document, explain, write docs: use `document`.
- Signals, intelligence, CIL, insights, automated detection: use `intensify` for depth mining or check `lib/cil/` directly.
- Implement, build feature, add functionality: use `feature-dev` or `builder`. All new features use `tdd` by default.

## Inventory Audit

Run this when skill references look stale:

```powershell
node .claude/skills/omninet/scripts/skill-inventory.mjs
```

The audit lists current `.claude/skills`, current Codex skills if present, and references to missing skill names in `AGENTS.md` and `CLAUDE.md`.
