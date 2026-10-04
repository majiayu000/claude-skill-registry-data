---
name: spec-authoring
description: Applies repository-specific technical-specification standards to design and specification documents. Use this skill when drafting, editing, or reorganizing a technical specification.
---
# Specification Authoring

## Discover the Specification Contract

Before editing, find and read the repository's agent instructions, source-of-truth hierarchy, specification index, authoring and Markdown standards, identifier or domain registry, templates, lint configuration, and representative nearby specifications.
Treat repository rules as authoritative over this skill's general guidance.

Determine the following without assuming fixed names or locations:

- Canonical and draft specification roots.
- Specification identifier, anchor, heading, and numbering rules.
- Allowed item kinds and required contract subsections.
- Requirements-to-specification responsibility boundaries.
- Traceability placement and link format.
- Rules for algorithms, examples, language references, diagrams, and inline HTML.
- Formatting, validation, and repository task-runner commands.

Do not copy identifier prefixes, anchor formats, heading shapes, or directory layouts from another repository.
Ask for direction when source documents conflict or when the user has not authorized a required update to a higher-priority artifact.

## Write an Implementable Specification

- Describe how the required behavior is implemented with enough precision for independent implementation and review.
- Define inputs, outputs, state transitions, invariants, ordering, side effects, error conditions, cancellation, concurrency, security, and observability when relevant.
- State algorithms as ordered decisions when execution order affects behavior.
- Define return values and failure semantics explicitly.
- Keep terminology language-neutral unless the specification is intentionally language-specific.
- Keep code samples minimal and use them to clarify signatures, schemas, or wire formats rather than replace contract prose.
- Maintain one source of truth for each contract and link to it from related material.
- Avoid introducing normative requirement obligations in specifications when repository policy reserves them for requirements.
- Preserve compatibility constraints and edge cases from source requirements and existing contracts.

## Structure Each Specification Item

Follow the repository's exact item template.
Where the local standard requires them, include a stable item heading, identifier and anchor, metadata, contract subsections, algorithm or reference anchors, and a final traceability subsection.
Derive all identifiers and anchors mechanically from canonical repository rules.
Keep subsection order, heading depth, numbering, and permitted inline markup compliant with local validators.

## Maintain Traceability and Consistency

Link each specification item to applicable requirements using the repository's required placement and format.
Verify every referenced identifier and anchor against real files.
Check related specifications, schemas, tests, and implementation for contradictions.
Report gaps rather than silently modifying requirements or guessing the intended contract.

## Review for Completeness

Confirm that another engineer could implement the behavior without inferring unstated decisions.
Look especially for omitted boundary conditions, ambiguous defaults, partial failure behavior, retry semantics, idempotency, ordering, cancellation, data ownership, migration behavior, and compatibility guarantees.
Keep the specification internally consistent and free of duplicated obligations.

## Validate the Result

Run the repository-provided formatter, Markdown linter, identifier and anchor validators, link checker, traceability checks, and documentation build relevant to the changed files.
Prefer project task-runner commands over invoking underlying scripts directly.
Report commands run, failures encountered, and checks that could not be performed.
