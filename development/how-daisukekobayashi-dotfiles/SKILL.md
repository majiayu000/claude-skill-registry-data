---
name: how
description: Explain how an existing subsystem works, trace its execution and data flow, or identify where behavior belongs. Use for code walkthroughs and ownership questions; use why for historical rationale.
license: MIT
---

# How

Build a working mental model from the current code. This is a read-only
investigation, including when another skill delegates it.

## Trace the behavior

1. Resolve the requested entry point, scenario, and revision. Inspect applicable
   instructions and working-tree state. Keep committed code and local changes
   distinguishable.
2. Read relevant CONTEXT.md, ADRs, and entry points. Trace a representative input
   through the real callers, state transitions, boundaries, and observable result.
   Follow actual dispatch, configuration, and error paths rather than describing
   filenames in isolation.
3. Identify who owns the state, who can mutate it, and where work starts and ends.
   Include ordering, persistence, retries, and cleanup only when they affect the
   question.
4. Check material claims against the source. Cite file locations and label
   unexecuted behavior as source-derived. A passing existing test is evidence
   only for the path it exercises.

For a narrow question, investigate directly. For independent, substantial parts
of a subsystem, use bounded read-only subagents when permitted and useful.
Give each the same scope, revision, and no-write restriction, and a distinct
question. The parent verifies citations and reconciles disagreements.

Do not edit files, start services, install tools, fetch Git refs, or run code
that can mutate state to answer a read-only question. If runtime observation
would settle an uncertainty, describe that check as pending. Read existing
observations when available.

## Explain the result

Lead with the behavior the reader needs to understand, then explain the key
concepts, one execution path, ownership, and consequential failure paths. Link
to a small set of relevant locations. Use a diagram only when it reduces the
explanation.

Distinguish facts, inferences, and unknowns. Current code alone does not establish
why its authors chose that shape; use [why](../why/SKILL.md) when rationale
matters. Mention supported defects without starting a fix.

When used inside an already authorized implementation task, return the traced
model and uncertainties to the caller. This investigation adds no write authority.

## Source

Adapted from Lauren Tan's [pstack how](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/how/SKILL.md).
Local changes: direct investigation for small questions, strict read-only scope,
runtime-neutral delegation, and parent verification of evidence. See [LICENSE](LICENSE).
