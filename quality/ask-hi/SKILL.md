---
name: ask-hi
description: Explain how the Harness Intelligence (HI) Baseline works. Use when asked which HI skill or phase to run, how HI skills chain and hand off, what an HI artifact, Pack, prompt surface, rule, hook, tool runtime or verifier does, or how `hi init`/`hi update` install them.
---

# Ask HI

Answer questions about the HI Baseline from its skill graph and install mechanics. The references are a map: they hold the relations no single `SKILL.md` shows. The installed skill files hold the exact contract.

## Steps

1. **Classify** the question to its branch below. A question that spans branches reads each branch's reference. Done when every named skill, artifact or mechanism in the question maps to one branch.

   | Question about                                                                           | Read                                                                 |
   | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
   | Which phase or skill fits a task; how phases hand off                                    | [phase-graph.md](references/phase-graph.md)                          |
   | Requirements: grill, brainstorm, flow lenses, glossary, architecture, spec, backlog      | [requirements.md](references/requirements.md)                        |
   | Delivery: plan, workers, TDD, validation, behavior verification, goals, closeout         | [delivery.md](references/delivery.md)                                |
   | Review, debugging, bug hunts, tech debt, research, security                              | [quality.md](references/quality.md)                                  |
   | Finder, prototypes, design, docs ingest, wiki, writing skills                            | [discovery-and-docs.md](references/discovery-and-docs.md)            |
   | Packs, install paths, Harness Adapters, prompt specs, rules, hooks, tools, release, drift | [baseline.md](references/baseline.md)                                |
   | Behavior that looks contradictory or a skill that seems unreachable                      | [known-gaps.md](references/known-gaps.md)                            |

2. **Ground** each claim in the installed source the reference points to: `.agents/skills/<skill>/SKILL.md` and its `references/` or `phases/` files, or the repository file named for a mechanism. When the installed file and the reference disagree, the installed file wins; name the difference. Done when every claim in the answer has one source path.
3. **Answer** with the route first: the entry skill to invoke (`$skill`), its invocation mode, what it calls in order, the artifacts it writes and where, and where it stops. Use `$show-me` when the answer has three or more steps, branches or handoffs. Done when the asker can act without opening another document, and each source path is listed.

## Vocabulary

- **Phase**: a lifecycle entrypoint skill under `phases/`; it routes and composes other skills.
- **Explicit-only**: the skill sets `disable-model-invocation: true` (Claude) or `allow_implicit_invocation: false` (Codex). Only a human can start it; tell the asker to type `$<skill>`.
- **Model-invoked**: an agent or another skill can start it from its description.
- **Pack**: a named set of skills, hooks and lint assets that `hi` installs; selection lives in `.devpunks/settings.json`.
