---
name: implement-client-feedback
description: Convert client revision notes into scoped implementation work with traceable decisions and verification. Use when a user provides comments, marked-up files, approval notes, or a feedback handoff and asks to implement changes, preserve approved elements, enforce exclusions, prepare a new version, or prove that every requested item was handled.
---

# Implement Client Feedback

Turn client language into a controlled implementation contract, apply the authorized changes, and verify the result against the feedback source.

## 1. Establish the authoritative feedback set

- Confirm the project root, current artifact or version, feedback source, and requested outcome.
- Read the latest approved brief, feedback, current implementation, and relevant handoff material before changing files.
- Treat the latest explicit decision as authoritative when it overrides earlier direction.
- Preserve literal replacement text, names, exclusions, filenames, and approved claims.

## 2. Build the feedback matrix

- Use [assets/feedback-implementation-brief.md](assets/feedback-implementation-brief.md).
- Classify every item as `change`, `keep`, `remove`, `exclude`, `question`, or `future`.
- Record the literal instruction, minimal interpretation, target, acceptance evidence, and status.
- Keep rejected concepts in a prominent exclusion list so older files or templates cannot reintroduce them.
- Separate client requests from optional internal improvements.

## 3. Resolve only material ambiguity

- Inspect the current artifact to resolve locations, nearby patterns, and implementation details.
- Record small reversible assumptions that cannot change the intended outcome.
- Ask before choosing a visual direction, changing approved scope, removing a public route, altering rights or deliverables, or contradicting literal feedback.
- Do not turn a focused revision into a redesign.

## 4. Implement with controlled scope

- Follow the project's existing architecture, versioning, and file conventions.
- Start from the latest approved foundation.
- Preserve approved elements and unrelated user-owned changes.
- Apply only confirmed changes and keep excluded items absent.
- Use the appropriate project tools for code, copy, images, documents, or website work.
- Do not deploy, publish, upload, send, or change external permissions unless the user explicitly authorizes that separate action.

## 5. Verify every feedback item

- Check each matrix row against the final files or rendered result.
- Confirm additions, exact replacements, removals, preserved elements, and exclusions.
- Run checks appropriate to the artifact, such as syntax, build, route, browser, dimensions, contrast, packaging, or document inspection.
- Mark every item `verified`, `partial`, `blocked`, or `awaiting client`.
- Do not call the revision complete while a required item is partial or unverified.

## 6. Report the review state

Return the implementation-brief location, version or artifact location, changed items, verification results, preserved exclusions, unresolved questions, and next client-review action.
