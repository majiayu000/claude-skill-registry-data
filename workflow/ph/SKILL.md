---
name: ph
description: Reactant tag-only placeholder. Use only when execute or execute-one dispatches an exact <@ph> tag from a document; never activate from ordinary chat or another skill.
---

# Placeholder

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@ph...>` annotation in a target document and hands off its
context. Never activate it from ordinary chat, semantic similarity, or any
skill other than those two routers. Without that handoff, produce no
placeholder and direct the user to add the tag and run a router.

Generate content that fits naturally at the tag position and replace only the
tag with it.

## Tag

```
<@ph>
<@ph: hint about what to fill>
```

Example: `We evaluated <@ph: the number of participants> participants.`

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it.
- **Prompt** (optional) — a hint (for example "a transition sentence").
  Default: infer from context.

## Workflow

1. Read the text before and after the tag; read the full file if broader
   context helps.
2. Generate content that fits naturally at that exact position in tone,
   style, and meaning.
3. Write the result back: replace ONLY the `<@ph>` tag with the generated
   text. All surrounding text stays untouched.

## Scope Modifiers

`<@ph>` never modifies surrounding content, so modifiers mainly provide
context:

- **Protect `<< >>`** — context only; never modify. This skill does not
  remove protect delimiters outside its own insertion.
- **Field `(( ))`** — when the tag sits inside a field, generate content that
  belongs in that field.

## Context References

Double-backtick references in the prompt point to resources that inform the
generated content (for example `<@ph: a summary based on ``results.md``>`).
Resolve paths relative to the document's directory unless absolute.

## Rules

- The output must read as if it had always been part of the text; keep it
  concise and contextually appropriate.
- Replace only the selected annotation. Preserve every unrelated annotation,
  `<@comment: ...>` tag, `<@chat-model>` block, and contextual literal/example
  byte-for-byte.
- On any error (for example an unreadable referenced file), fail cleanly:
  leave the tag, change nothing, report.
