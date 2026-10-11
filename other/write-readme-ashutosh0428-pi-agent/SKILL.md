---
name: write-readme
description: Write or improve a README that gets a stranger from landing to running in minutes.
trigger: when the user asks for a README or project documentation
---
## When to use
The user wants a README written or improved.

## How
1. Read the project first: entry points, install method, license, tests.
2. Structure, in order:
   - One-sentence value proposition (what + for whom).
   - Badges only if real (CI, version, license).
   - **Install** — the one command that works (`pip install x`), then
     alternatives.
   - **Quickstart** — smallest copy-pasteable example that does something
     visible.
   - Features as a short table or list — capabilities, not adjectives.
   - Configuration/flags table when relevant.
   - Contributing/license pointers at the bottom.
3. Every command must be copy-pasteable and correct for THIS project —
   verify paths and names against the repo.
4. Write for a stranger: no internal jargon, no assumed context.

## Avoid
- Marketing fluff ("blazingly fast", "next-generation").
- Documenting aspirations as features.
- Walls of prose where a table or code block works.

## Done well
A stranger lands, understands the value in 10 seconds, installs in one
command, and sees output in two minutes.
