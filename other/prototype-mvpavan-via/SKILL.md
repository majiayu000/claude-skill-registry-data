---
name: prototype
description: Use when a runnable throwaway experiment can resolve a specific design, state-model, algorithm, or UI question.
---

# Prototype

Build a throwaway artifact to answer a named design question. Choose the smallest
runnable form that exposes the uncertainty: a script for algorithms, a state demo
for domain behavior, or a UI mockup for interaction/layout.

State the question and observable success before building. Use the authorized
location, otherwise an isolated scratch artifact. Keep prototypes clearly marked,
reproducible and separate from production behavior. Use synthetic or appropriately
scoped data; retain safety checks and accessibility that the experiment requires.

- State/logic exploration: `LOGIC.md` offers script and shareable HTML options.
- UI exploration: `UI.md` covers contextual mockups and optional variants.

Persistence, external calls and realistic integration belong only when needed to
answer the question and authorized. A small assertion may be the cheapest proof;
a prototype does not imply either a full test suite or a ban on checks.

Record the outcome, exercised cases, limitations and artifact/run pointer in the
existing task or requested report. An inconclusive experiment is a valid result.
Promoting the decision or code into production is separate work requiring its own
scope and normal checks. Preserve the artifact when it supports the conclusion;
committing, creating production routes and cleanup retain their authority gates.
