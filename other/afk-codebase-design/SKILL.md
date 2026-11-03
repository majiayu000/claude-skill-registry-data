---
name: afk-codebase-design
description: Shared vocabulary and rules for designing deep modules in money-tracker.online - module, interface, depth, seam, adapter, leverage, locality, the deletion test. Use when designing or changing a module's interface, choosing where a seam or test goes, judging whether an abstraction earns its keep, or when another skill (afk-architecture-review, afk-to-tickets) needs this vocabulary.
---

# AFK codebase design

**These instructions are already in your system prompt.** Never call the `Skill` tool for an `afk-*` skill - a repo-local skill is not in the agent's registry, so the call fails with `Unknown skill`.

Adapted from mattpocock/skills `codebase-design` for unattended runs. Use these words exactly in designs, briefs, review findings and PR bodies. Do not substitute "component", "service", "API" or "boundary".

**This file is the shared half.** The vocabulary and the rules below are kept identical across the repositories that share this agent layer - `planned.travel` and `cezar` - because `afk-triage`, `afk-to-tickets` and `afk-architecture-review` all read this literal path for terms they name exactly. Nothing renders it any more: ADR 0021 retired `design4pro/agent-kit`, so a change here is a change made by hand in each of them. The other half - this repository's own house idiom, seam table, dependency examples, test layout and risk-high list - is at `.ai/cezar/skills/afk-codebase-design/SKILL.md`, which shadows this file by name in the cockpit's registry. Read both before designing anything.

## Vocabulary

- **Module**: anything with an interface and an implementation, at any scale: a function, a file, a package, a whole subsystem.
- **Interface**: everything a caller must know to use the module correctly: types, invariants, ordering, error modes, required state, performance. Not just the TypeScript signature.
- **Implementation**: the code behind the interface.
- **Depth**: behaviour a caller or test can exercise per unit of interface it must learn. Deep = small interface, lots of behaviour. Shallow = interface nearly as complex as what it hides.
- **Seam**: the place where behaviour can change without editing that place; where an interface lives.
- **Adapter**: a concrete thing that fills a seam.
- **Leverage**: what callers gain from depth.
- **Locality**: what maintainers gain from depth: change, bugs and verification concentrate in one place.

## Rules

- **Deletion test.** Imagine deleting the module. If the complexity vanishes, it was a pass-through: inline it. If the complexity reappears across callers, it earns its keep.
- **The interface is the test surface.** Tests cross the same seam callers do. Needing to test past the interface means the module is the wrong shape.
- **One adapter is a hypothetical seam; two adapters are a real one.** Do not add a seam until something actually varies across it.
- **Accept dependencies, return results.** Pass collaborators in and return values rather than mutating shared state, so the seam is testable.
- **Replace, don't layer.** When you deepen a module, the shallow tests it makes redundant should go rather than sit beside the new ones. The default is to re-point each one at the new interface. Delete a test only when the test engineer specialist (`.ai/skills/afk-decide/SKILL.md`) confirms that every assertion it makes is covered through the new interface, and list each deleted test with its verdict in the PR's Resolved assumptions.

## Dependency categories (where to put the seam)

Four categories, and what each is tested with. This repository's own examples for every row are in its override.

| Category             | What it is                                     | Test with                                  |
| -------------------- | ---------------------------------------------- | ------------------------------------------ |
| In-process           | logic with no I/O of its own                    | the real code                              |
| Local, substitutable | something on this machine: files, a local store | a temp directory or a small fake           |
| Remote you own       | a service defined in this repository            | its own contract, plus an in-process server |
| True external        | a third-party API or CLI                        | a fake at the seam, never the real thing   |

## Design it twice (risk-high interfaces only)

Use this when a new or changed interface touches something `SDLC.md` marks `risk-high`; the override names which interfaces those are here.

1. Dispatch two child tasks with `cez task create`. Constrain one to the smallest possible interface and the other to the most common caller's convenience.
2. Compare their designs on depth, locality and seam placement. Pick one, or a merge of both.
3. Record the choice and the rejected design as a row in the Resolved assumptions table.

If dispatch is unavailable, write both designs yourself, in sequence, before choosing.

## Done when

The design or finding names the module, its interface, and its seam in these terms, and states which rule above justifies the change.
