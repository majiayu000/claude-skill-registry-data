---
name: grid-help
description: Explain how to use the-grid (which slash command or subagent to reach for, orchestrators vs specialists, the four factories). Use when the user asks "how do I use the-grid", "what can I do here" or "how do I add a skill/agent/automation".
---

# grid-help

A live, in-session guide to the-grid. Answer from the summary in `sections/orientation.md`; point to
[USAGE.md](https://github.com/oneafrikan/the-grid/blob/main/USAGE.md) (repo root) for the full walkthrough rather than
reproducing it verbatim — it changes independently of this skill.

## Quick orientation

Read `sections/orientation.md` for the summary to answer from.

## Sibling help skills

Don't reproduce their content — hand off:

| Command | Owns |
|---|---|
| `/openspec-help` | The 12 openspec skills, spec format, adoption paths |
| `/ponytail-help` | ponytail modes and intensity levels |

## Answering well

- **Give a pointer, not a tutorial.** One or two lines plus the file to read.
- **Check before asserting.** [SKILLS.md](https://github.com/oneafrikan/the-grid/blob/main/SKILLS.md) is generated and
  current; your memory of what's wired is not. Same for which agents exist —
  use the agent list your harness shows you.
- **Private projects: mechanism yes, names never.** A machine may run a project
  composed from roles outside this repo (`GRID_PRIVATE_ROLES_DIR`, gated in
  gitignored `machines/<host>.local.txt`). Explain how that works to anyone who
  asks; never enumerate the roles of a private desk in this repo or in a shared
  session.

If the question is deeper than a pointer — which template to pick, how a
pattern composes, how the delegation topology works — read the relevant
section of [USAGE.md](https://github.com/oneafrikan/the-grid/blob/main/USAGE.md), [README.md](https://github.com/oneafrikan/the-grid/blob/main/README.md), or
the repo's project instructions file rather than guessing.

## Sections
Read a section only when its condition applies; do not preload them.
- sections/orientation.md: read before answering any question about using the-grid
