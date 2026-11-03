---
name: afk-lessons
description: Turn repeated mistakes from recent agent PRs into durable rules - a lint rule or test when mechanical, CODE_REVIEW.md when a judgement call, AGENTS.md or an afk-* skill when operational - and open at most one PR. Use for a scheduled retro, or when asked what the pipeline keeps getting wrong.
---

# AFK lessons

**These instructions are already in your system prompt.** Never call the `Skill` tool for an `afk-*` skill - a repo-local skill is not in the agent's registry, so the call fails with `Unknown skill`.

Institutional memory: every mistake that repeats becomes a rule, so it does not repeat again.
- **Output:** at most one PR per run, or nothing.
- **Rules only get added or tightened.** Never weaken, delete or loosen one.

## 0. Setup

Load `.ai/agentic.config.json` and `.ai/trackers/github.md`. The window is the last 14 days.

## 1. Collect evidence

- Run `om-pipeline-retro` with `--since <date 14 days ago>` and keep its ranked causes. Skip its handoff offer.
- For merged and closed PRs in the window, collect every changes-requested review and every blocker or major finding. Each item needs its PR number and the comment link.
- Collect PRs that needed a second push after a failing validation gate.
- Collect the lessons unattended runs recorded themselves: the `## Lessons` section of PR bodies in the window, and of run handoff files (`.ai/cezar/runs/*.handoff.md`) modified in the window. A run cannot edit a user's global instructions, so this is where its lesson goes; each run's lesson counts as one piece of evidence.

## 2. Group into lessons

A **lesson** is one root cause stated as a rule. Example: "New persisted fields on RunRecord must be optional."
- Keep only lessons seen in **at least two different PRs or runs**.
- Drop any lesson an existing rule already covers: search `AGENTS.md`, `CODE_REVIEW.md`, `SDLC.md`, `CONTEXT.md`, `.ai/skills/afk-*`, and the lint and test setup.
- If an existing rule was ignored rather than missing, the fix is to make that rule harder to miss: move it earlier, or make it mechanical. Do not write it a second time.

## 3. Place each lesson where it is enforced

| Kind | Where it goes |
|---|---|
| Mechanical: a tool can detect it | A test or lint check in the existing suites. Include a case that fails without the rule. |
| Judgement: a reviewer must decide | A bullet in the matching `CODE_REVIEW.md` checklist section, plus its severity. |
| Operational: how agents run | `AGENTS.md` (the section it belongs to), or the `afk-*` skill that made the mistake. |
| Vocabulary: the wrong word or a confused concept | A `CONTEXT.md` entry, following `afk-domain-modeling`. |

Keep each rule to one or two sentences, and cite the PRs that motivated it, the way existing rules cite `#810`.

## 4. Ship

Put all lessons in one branch and one PR through `om-open-pr`, with category `documentation`, or `refactor` when it adds a test. The PR body gets one section per lesson: the rule, where it went, and the evidence links. A PR that adds a test must pass the full validation gate first.

## Done when

Either one PR is open, and every rule in it cites at least two PRs and is placed where it is enforced; or the run report says no lesson met the threshold, and lists the candidates it saw.
