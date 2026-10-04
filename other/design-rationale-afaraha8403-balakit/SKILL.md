---
name: design-rationale
description: >-
  Investigate why code is shaped this way. Git and PRs first, then every
  evidence category that actually exists (tickets, docs, chat, observability,
  errors, analytics). Every claim is labeled Direct / Supported / Inferred /
  Speculative / Unknown. Never treat code as its own intent.
  Apply when the user asks why a design exists, why a flag is off, or why
  a threshold is what it is. Use subsystem-walkthrough for runtime behavior.
  Use dissect to audit entities. Use proving-change-safety before merge.
user-invocable: true
disable-model-invocation: false
version: "1.2.0"
author: "Ali Farahat"
tags: ["investigation", "epistemics", "history"]
when_to_use: |
  USE WHEN:
  - The user asks why something was built this way, why a flag is off, or
    why a number or shape was chosen.
  DO NOT USE WHEN:
  - The question is how it works at runtime (use subsystem-walkthrough).
  - There is no historical question, only "what should we change" (use dissect
    or deep-deliberation).
---

# Design rationale

> **Leading words:** code is not intent, coverage map, Direct Supported
> Inferred Speculative Unknown.

Companion to `subsystem-walkthrough`. That skill is runtime. This one is the
forces that produced the shape.

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Parse the target and the question. If vague, state your guess and proceed.
2. Code-anchor: paths, symbols, `git blame` / `git log --follow`, PR numbers, `gh pr view` when `gh` exists.
3. Coverage map of seven categories. Spawn one investigator per category that exists. Document the null; do not skip the search silently.
4. Synthesize with [references/epistemics.md](references/epistemics.md). Keep confidence language intact.
5. Present. If this investigation precedes a change, add Preserve / Change / Avoid / Risk.

## Categories

1. Source control — git + `gh`. Always run.
2. Issue / ticket tracker
3. Long-form docs
4. Real-time chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics

Discover tools from what this host actually exposes. Do not require a Cursor
`mcps/` directory. Inherit the host model. A missing category is a finding:
"Real-time chat skipped. No matching tool available."

Skip a category only when no tool exists or it is provably irrelevant (a
build-time script has no Sentry). Write the reason in Sources Consulted.

## Output

The Question / The Code in Question / What We Found / What We Can Reasonably
Infer / Competing Hypotheses / What We Don't Know / Sources Consulted
(one line per category, including nulls) / Confidence Summary.

Sources Consulted is a 7-row list. A missing tool is a row, not an omitted
heading. Do not open with "the user is wrong." Put their guess under
Competing Hypotheses.

## Reply contract

The synthesis above. Confidence language from epistemics is not rewritten.
