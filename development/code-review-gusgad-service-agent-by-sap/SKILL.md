---
name: code-review
description: Use when finishing a task, before merging, or when giving or receiving code review feedback on this repo - covers when to request a review, how to scope it, and how to respond to feedback with technical rigor instead of reflexive agreement.
---

# Code Review

Two halves: requesting review of your own work, and responding to feedback you receive. Both matter — a good review request produces useful feedback; a bad response to feedback wastes it.

This skill is about review *discipline*. For the platform's automated review tooling in this environment, see `/code-review` (built-in) — this skill covers how to scope that review and how to act on what it finds.

## Requesting Review

**When:**
- After completing a task or a meaningful chunk of one
- Before merging to `main`
- After a non-trivial bug fix, especially one that took several attempts
- When stuck — a fresh pass over the diff often surfaces what's actually wrong

**How to scope it:**
1. Get the actual boundary of the change:
   ```bash
   BASE_SHA=$(git merge-base HEAD origin/main 2>/dev/null || git rev-parse HEAD~1)
   HEAD_SHA=$(git rev-parse HEAD)
   ```
2. State what was built and what it was supposed to do — a reviewer (human or agent) without your context needs the "why," not just the diff. If this repo has a design note or plan for the change (see the `brainstorming` skill under `superpowers/`), point at it instead of re-explaining.
3. Prefer reviewing incrementally (after each meaningful task) over one giant review at the end — smaller diffs get sharper feedback and issues get caught before they compound across the rest of the change.

**Acting on feedback:**
- Fix anything that's clearly a bug or a security/correctness issue immediately
- Fix anything "important" before moving on to the next task
- Note anything cosmetic/minor for later rather than blocking on it
- Push back on feedback that's wrong — see below. Don't implement something you believe is incorrect just because it was suggested.

## Receiving Feedback

**Core principle:** verify before implementing, ask before assuming. Technical correctness matters more than sounding agreeable.

The response pattern:
1. **Read** the full feedback before reacting
2. **Restate** the requirement in your own words (or ask, if unclear)
3. **Verify** it against the actual codebase — don't take the claim at face value
4. **Evaluate** whether it's technically sound *for this codebase specifically* (this repo's multi-tenant Postgres/Sequelize backend, its Kafka messaging flow, and its Angular client each have constraints a generic suggestion might not account for)
5. **Respond** — a technical acknowledgment, or reasoned pushback
6. **Implement** one item at a time, verifying each before moving to the next (see `verification-before-completion` under `superpowers/`)

**If any item in a batch of feedback is unclear, stop and ask before implementing any of it** — items are often related, and partial understanding produces a wrong implementation of the parts you thought you understood too.

**Don't perform agreement.** Skip "You're absolutely right!" / "Great catch!" / "Thanks for that!" — fix it and let the diff show you heard it. If you catch yourself typing gratitude or enthusiasm before the fix itself, delete it and state the fix instead.

**When feedback conflicts with an existing decision or working code:**
```
Before implementing:
1. Is this actually correct for this codebase's stack and constraints?
2. Does it break something that currently works?
3. Is there a reason the current implementation looks the way it does?
4. Does the reviewer have the full context, or might they be missing something?
```
If a suggestion looks wrong, push back with the specific technical reason — reference the working test or the code path that contradicts it. If you can't verify it either way, say so explicitly rather than guessing: "I can't confirm this without checking X — should I investigate, or do you want to confirm first?"

**YAGNI check for "do this properly" suggestions:** if a reviewer suggests fully building out something (better error handling, a generic abstraction, extra config), grep for whether it's actually used/called anywhere first. If it isn't, that's worth surfacing before implementing it — "this path isn't called from anywhere yet, do we still want to fully build it out?"

**If you pushed back and turn out to be wrong:** state the correction factually and move on — "Checked X, it does do Y, I was wrong — fixing now." No lengthy apology, no over-explaining.

## Implementation Order for Multi-Item Feedback

1. Clarify anything unclear, for all items, before implementing any of them
2. Blocking issues first (breaks, security, data integrity — this repo touches tenant-isolated data and job execution, so isolation bugs are always blocking)
3. Simple fixes next (naming, typos, imports)
4. Complex fixes last (refactors, logic changes)
5. Verify after each fix, not just at the end

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reviewing the whole feature in one giant diff at the end | Request review after each meaningful chunk |
| Performative agreement before verifying | Restate the requirement or just fix it — no "you're right!" |
| Implementing a suggestion without checking it against this codebase | Verify first; this stack (multi-tenant, Kafka, Sequelize) has constraints a generic review might miss |
| Batch-implementing unclear feedback | Stop and clarify every unclear item before touching any of them |
| Treating reviewer suggestions as automatically correct | Push back with technical reasoning when something looks wrong |
| Treating reviewer suggestions as automatically wrong | Verify before dismissing — "probably fine as-is" isn't verification either |
