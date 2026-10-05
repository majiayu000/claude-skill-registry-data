---
name: writing-for-agents
description: Writing documents for agents. Use when creating or editing skills, modifying AGENTS.md or CLAUDE.md, or changing documents reached through agent context pointers.
---

# Writing For Agents

Use this reference for any document an agent consumes: a Skill, `AGENTS.md`,
`CLAUDE.md`, or a document reached through a pointer. Packaging differs; the
writing goal does not: make the agent take the same useful process on each run,
without forcing identical output.

Repository instructions, safety rules, privacy boundaries, and the user's
request remain authoritative. This reference improves how those instructions
are written; it never weakens them. When the document is a Skill, also read
[`SKILL-MECHANICS.md`](SKILL-MECHANICS.md).

## Context Pointers

A **context pointer** is an always-visible reference to material outside the
current context, together with the condition for loading it. A Skill description
is one. An `AGENTS.md` line naming a deeper document is another. The wording of
the pointer determines when the agent reaches the material.

A pointer should state what the material is and the distinct branches that
should trigger it. Front-load its leading word, keep one trigger per real branch,
and remove identity already carried by the target document. A critical target
behind a weak pointer is a routing defect: sharpen the pointer before inlining
the body.

## The Two Loads

- **Context load** is the always-present token and attention cost of pointers,
  descriptions, and repository instructions.
- **Cognitive load** is what a person must remember: which documents or explicit
  workflows exist and when to reach for them.

Spend context load only when the agent must discover something automatically.
Spend cognitive load where human judgment or deliberate invocation matters.

## Information Hierarchy

Arrange content by how immediately it is needed:

1. **In-file steps**: the ordered actions the agent performs.
2. **In-file reference**: definitions and rules consulted while performing them.
3. **Disclosed reference**: branch-specific material behind a context pointer.

**Progressive disclosure** moves branch-specific reference down that hierarchy.
Inline what every run needs; disclose what only some branches need. Keep each
concept's definition, rules, and caveats co-located under one heading.

**Sprawl** is a document that is too long even when every line is live. Cure it
by disclosing reference or splitting real branches, not by scattering one
meaning across several files.

## Steps And Completion Criteria

End each step with a condition that makes completion observable. Strong criteria
are both clear and demanding: “every modified model accounted for” drives more
legwork than “produce a change list.” Sharpen a vague bound before splitting a
sequence. Split only when visible later steps repeatedly pull the agent into
premature completion, and only across a real context boundary.

## Leading Words

A **leading word** is a compact concept already present in the model's training
that anchors a region of behavior, such as _tracer bullet_, _frontier_, or
_tight loop_. Reuse the token rather than repeating its full definition.

Leading words anchor both execution and invocation. Prefer an established term
over a newly coined one when it recruits the right prior with less explanation.
Describe the positive target behavior. Keep explicit prohibitions for genuine
hard guardrails, and pair them with the action the agent should take instead.

## Environment As Source Of Truth

The environment is already documentation: scripts, configuration, directory
layout, schemas, and `--help` output. A prose copy of an easy lookup is a cache
that can go stale. Write what the environment cannot reveal cheaply: intent,
unwritten convention, branch conditions, risk boundaries, and surprising
failure modes.

## Pruning

- Keep each meaning in one authoritative place.
- Remove stale or irrelevant sediment.
- Test every sentence for behavioral effect versus the model's default; delete
  no-ops rather than polishing them.
- Preserve hard safety and privacy guardrails even when they are repetitive by
  design; correctness outranks stylistic compression.

The result is complete when every instruction has an observable purpose, every
branch-specific detail has a reliable pointer, and the environment—not prose—
owns facts it can expose directly.
