---
name: developer-note-writer
description: Turns implementation details into a brief, technically accurate developer-facing explanation for a README, example HTML file, or documentation page. Use when the user asks for a concise implementation note, code-example explanation, integration rationale, behavior summary, or maintainer note grounded in source code and repository conventions.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: docs-seo
  task_type: writer
  audience: developers-and-maintainers
  tags:
    - documentation
    - readme
    - code-examples
    - developer-experience
    - implementation-notes
  status: draft
  side_effects: none
---

# Developer Note Writer

## Purpose

Turn verified implementation details into a short explanation that tells developers what the code does, why the detail matters, and what they need to know when using or maintaining it.

## When to use this skill

Use this skill when:

- A README needs a brief explanation of an implementation choice or integration detail.
- An example HTML file needs nearby prose that explains its markup, script, styles, or behavior.
- A documentation page needs a compact note about setup, lifecycle, configuration, fallback behavior, or developer responsibility.
- A code change or existing implementation must be translated into clear developer-facing language.
- The user wants concise documentation rather than a tutorial, API reference, or marketing copy.

Do not use this skill when:

- The request is for a full README, documentation site, tutorial, or API reference.
- The user wants a code review, architecture decision record, changelog entry, or release note.
- The explanation cannot be grounded in supplied requirements or repository evidence.
- The task is primarily public-facing promotional copy.

## Inputs to inspect

Inspect only the files needed to verify the note, such as:

- The target `README.md`, documentation page, or example HTML file.
- The implementation code discussed by the note.
- Public exports, types, options, events, or lifecycle methods involved.
- Relevant tests, fixtures, examples, or generated markup.
- Nearby documentation for terminology, tone, heading level, and formatting conventions.

If the target location is not specified, identify the smallest suitable documentation surface before writing.

## Workflow

1. Identify the target reader, destination, and implementation detail to explain.
2. Inspect the smallest set of source, test, example, and documentation files needed to verify the behavior.
3. Separate confirmed behavior from assumptions. Omit uncertain claims or label them for verification.
4. Reduce the implementation detail to the information a developer needs:
   - what the code does
   - why it exists or matters
   - what the developer must provide, preserve, configure, or expect
   - any important constraint, fallback, or lifecycle consequence
5. Write one compact paragraph or a short note block in the repository's existing terminology and voice.
6. Keep identifiers and code syntax only when they improve precision. Link or point to fuller documentation instead of duplicating it.
7. Check the note beside its destination and remove repetition, unsupported claims, generic praise, and unnecessary implementation history.
8. Apply the note to the file only when the user requested file changes; otherwise return insertion-ready copy and a suggested location.

## Writing guidance

- Lead with observable behavior or the developer action, not background history.
- Prefer concrete verbs such as “adds,” “reads,” “preserves,” “dispatches,” or “falls back.”
- Explain rationale only when it helps someone integrate, debug, extend, or maintain the code.
- Distinguish library behavior from developer responsibility.
- Preserve exact names for APIs, attributes, events, classes, and files.
- Match the destination: concise prose in a README, a nearby explanatory note in an example, or a focused callout in longer docs.
- Avoid claims such as “simple,” “seamless,” “powerful,” or “automatic” unless the implementation and context make them meaningful.

## Output format

Return:

```md
## Developer note

<One concise paragraph or short note block.>

## Placement

- Target: `<file or documentation surface>`
- Location: <where the note belongs and why>

## Evidence

- `<file, symbol, test, or supplied requirement>`: <behavior it confirms>

## Verification needed

- <Unconfirmed claim, or “None.”>
```

If the user requests direct editing, replace `Placement` with `Changes made` and report the edited file.

## Quality bar

The task is complete only when:

- The note is brief enough to sit naturally near the relevant code or documentation.
- Every technical claim is supported by repository evidence or supplied requirements.
- The note explains practical significance, not merely what the code looks like.
- Developer responsibilities and implementation behavior are not conflated.
- Terminology, tone, and formatting match the destination.
- The result does not duplicate nearby documentation or expand into a tutorial.

## Edge cases

- If behavior differs by environment or configuration, state the condition rather than presenting one path as universal.
- If comments, docs, tests, and source disagree, treat executable behavior and tests as stronger evidence and report the conflict.
- If the detail is too complex for one note, write a short summary and recommend a link to dedicated documentation.
- If the destination is an HTML example, ensure prose remains understandable when the example is viewed without repository context.
- If the rationale is unknown, explain confirmed behavior and developer impact without inventing intent.

## Related skills

- `repo-demo-copywriter`
- `docs-discoverability-audit`
- `before-after-diff-summary`
