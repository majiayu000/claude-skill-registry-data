---
name: propose
description: Design a concrete technical proposal with evidence and tradeoffs when a decision needs design. No implementation or automatic reviewer.
argument-hint: "<question> [--short|--full] [--auto] [--scope path] [--no-review] [--out dir] [--html]"
---

# Propose

Gather only the context needed to answer the design question. Prefer the
smallest sufficient format: short for a bounded reversible choice, standard
for one system, full for a genuine cross-system design. No format interview
when the request already determines the appropriate size.

Use references/proposal-template.md for stable section numbers and artifact
shape. Write problem, real alternatives (including status quo when relevant),
tradeoffs, design, risks, recommendation and runnable implementation tasks.
Do not manufacture alternatives, diagrams, metrics or verification layers
to fill a template. Research only unresolved external questions.

## Interview

Without --auto, interview the user before drafting: problem, scope,
goals/non-goals, alternatives direction, design choices. One question per
message, in plain text, then wait for the answer. Draw questions from
references/interview-questions.md; skip one only when the request already
answers it. Never infer an answer the user can give. Under --auto, infer
from code and the request and ask only about a blocking decision.

Review the draft yourself. An independent review is optional and requires
explicit user consent, never merely omission of --no-review. Retain supported
findings only. Leave status Draft or Review until the user explicitly accepts
the proposal; writing it is not implementation approval.

Keep the existing docs/proposals/<id>-<slug>/PROPOSAL.md layout and links to
a source brief. Do not supersede that brief until the design is accepted.
On acceptance, record the Git `base` and `branch` in the frontmatter
(steps/step-09-finalize.md) so ship branches without asking again.
Render via scripts/render.py only on --html or request. Do not launch ship,
open a browser, create an index, or start another agent just to finish.

## Arsenal handoff

When called by Arsenal, return the proposal, status and unresolved decisions
to Arsenal. Do not launch ship yourself. Explicit user acceptance remains
required before Arsenal can consume the proposal for implementation, even
when the original request was to build the feature.

## Verify external facts

Before stating an external fact (a version, an API, a price, a date, a
regulation, the behaviour of a tool or library, a person or company), search
first when the runtime offers web search: read the `websearch` skill and run
one quick search, then cite the source. One search per fact; `--deep` only on
request. Without web search, mark the claim unverified. Facts visible in the
repository or the request need no search.

## Execution policy

Work solo. Ask before any subagent or reviewer, even in auto mode. Explain
the independent scope and expected benefit first. No hidden advisor, nested
delegation, model retuning, repeated successful checks, or progress spam.
Stop when the requested result
is delivered. User stops and scope changes override pending steps.
