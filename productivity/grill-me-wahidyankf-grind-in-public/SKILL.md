---
name: grill-me
description: >-
  Resolve open design decisions by interrogating the owner with structured multiple-choice questions, one decision at a
  time, until nothing is left ambiguous.
when_to_use: >-
  Use when the owner says "grill me", asks to stress-test a plan or design, or when a task cannot proceed without a
  decision only the owner can make.
---

# Grill Me

Resolve every open decision before building, by asking rather than assuming.

## When to Activate

Activate when the owner says "grill me", asks for a plan or design to be stress-tested, or when work is blocked on a
decision the repository does not already answer. Do not activate for a drill: there the owner answers questions to
practice, and this skill is the reverse.

## Rules

The [grilling-with-options policy](../../../repo-governance/conventions/grilling-with-options-policy.md) is normative.
Read it rather than working from memory. In short: explore first, offer two to four mutually exclusive options, give
each a specific trade-off, mark exactly one Recommended in that option's label, ask one decision per question, and
always carry the write-in and chat options.

## Mechanism

Use the question tool your harness provides, whenever the session is interactive. The
[question tools](../../../repo-governance/conventions/grilling-harness-binding/question-tools.md) table names the tool
for each harness and the setting it needs, and the
[Markdown fallback](../../../repo-governance/conventions/grilling-harness-binding/markdown-fallback.md) covers a session
that cannot ask. Read the row for the harness you are running in rather than assuming a tool name: this file is shared,
and the harness reading it is not always the one it was written from.
[Shaping a question](../../../repo-governance/conventions/grilling-harness-binding.md#shaping-a-question) owns the rest
of the form, including the `(Recommended)` suffix and the twelve-character header.

Shape the question as the [harness binding](../../../repo-governance/conventions/grilling-harness-binding.md) says under
Shaping a Question, and follow that table's row for your harness on whether the client supplies the free-text write-in
or you must add it yourself.

## After the Grilling

Summarize each decision and the reason it was chosen, then say what the answers changed about the plan. A decision the
owner cannot trace back to a question is one they never really made.
