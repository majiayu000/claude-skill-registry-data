---
name: grill-me
description: Use when a user asks for or clearly wants to be grilled, interviewed, or to stress-test a plan or design, including when they mention "grill me". Resolve material decisions one at a time until scope, success criteria, and resources are explicit.
license: MIT
---

# Grill Me

Use this skill when the user asks for or clearly wants to be grilled, interviewed,
or to stress-test a plan or design. It is an interview workflow, not
authorization to implement or modify anything.

- Inspect the repository, configuration, and available artifacts for facts that
  can be answered locally; do not ask the user for answerable facts.
- Identify unresolved decisions that materially affect scope, success criteria,
  constraints, resources, or execution order. Skip settled choices and
  low-impact minutiae.
- Ask exactly one focused question at a time. Include your recommended answer
  with each question and briefly explain why it is the recommended default.
- After each answer, update the decision state and continue to the next material
  branch. Do not reopen settled details unless new information creates a real
  conflict.
- Stop when material scope, success criteria, and resources or constraints are
  settled, or when the user switches to execution. Summarize the decisions and
  handoff; handle later implementation under the normal authorization and scope
  rules for that task.

Invocation of this skill alone never authorizes implementation, external writes,
or other mutations.
