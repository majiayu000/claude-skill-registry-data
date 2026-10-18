---
name: next-step
description: Pick the next build step from the build plan and PROGRESS.md, state the plan briefly, then build it.
disable-model-invocation: true
---

Plan and build the next step.

1. Read docs/progress/PROGRESS.md and the relevant phase in docs/build-plan.md.
2. Pick the smallest next step that is useful on its own and testable.
3. State it in a few lines: **Goal**, **Plan** (3–6 steps), **Done when** (the tests/commands
   that prove it), **Out of scope**. Flag anything that needs the owner (money, accounts,
   product decisions) and stop only for those.
4. Build it to the definition of done in CLAUDE.md, committing and pushing to `main`.
