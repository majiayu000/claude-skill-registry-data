---
name: subsystem-walkthrough
description: >-
  Walk through how a subsystem works: architecture, runtime flow, ownership,
  layering. Apply when the user asks "how does X work", "where should this
  live", or wants an onboarding mental model before changing code. Use
  design-rationale for motivation. Use dissect to audit entities. Use
  proving-change-safety before merging a change you do not trust.
user-invocable: true
disable-model-invocation: false
version: "1.2.0"
author: "Ali Farahat"
tags: ["explainer", "architecture", "onboarding"]
when_to_use: |
  USE WHEN:
  - The user asks how a subsystem, feature, or function works.
  - Placement or ownership questions: where should this live, which package owns it.
  DO NOT USE WHEN:
  - The question is why it was built this way (use design-rationale).
  - The task is an entity-level audit (use dissect).
---

# Subsystem walkthrough

> **Leading words:** mental model, one explainer, parallel slices, inherit host
> model.

Answer "how does X work?" at the level of a senior engineer onboarding onto
the subsystem. Not annotated source.

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Assess complexity. Simple → one explainer. Complex → 2–4 read-only explorers, then one synthesizer. Write `Complexity: simple` or `Complexity: complex (N slices)` as the first line of the output.
2. Explore or explain (see below). Inherit the host model. Do not hardcode a slug.
3. Present the explainer output with light edits only. Keep the Complexity line.

When in doubt, take the simple path.

## Simple

One read-only subagent explores and explains in a single pass. Fill
[references/explainer-prompt.md](references/explainer-prompt.md) without
explorer findings.

## Complex

Decompose into 2–4 distinct slices. Spawn explorers in one message, each with
[references/explorer-prompt.md](references/explorer-prompt.md). Then one
synthesizer with the explainer template and every explorer's findings filled in.
If the host cannot spawn subagents, run the slices sequentially yourself.

## Output

First line: `Complexity: simple` or `Complexity: complex (N slices)`.

Then: Overview / Key Concepts / How It Works / Where Things Live / Placement /
Gotchas. Drop a section that does not apply. **Placement** is where new code
for this subsystem should live (package, file, layer) — one short paragraph,
not a second architecture essay.

## Reply contract

The Complexity line, then the explanation. Do not rewrite it into a
different structure after the explainer returns.
