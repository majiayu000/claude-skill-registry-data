---
name: edit
description: Reactant tag-only text edit. Use only when execute or execute-one dispatches an exact <@edit> tag from a document; never activate from ordinary chat or another skill.
---

# Edit

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@edit...>` annotation in a target document and hands off its
context. Never activate it from an ordinary chat-window editing request,
semantic similarity, or any skill other than those two routers. Without that
router handoff, do not edit anything; tell the user to place an `<@edit>` tag in
the document and run `execute` or `execute-one`.

Apply the edit described in the prompt to the surrounding block, then consume
the tag.

## Tag

```
<@edit: instruction>
```

Examples: `<@edit: make this shorter>`, `<@edit: rewrite in formal tone>`,
`<@edit: revise to align with ``intro.md``>`.

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it. Read the full file when broader context helps.
- **Prompt** — what to change.
- **Modifiers and context references** — see below.

## Workflow

1. Read the surrounding block; read the full file if you need broader context.
2. Resolve any context references in the prompt.
3. Apply the requested edit to the block's authored prose.
4. Write the result back to the file: replace the surrounding block (including
   the `<@edit: ...>` tag) with the edited text.

## Scope Modifiers

- **Protect `<< >>`** — text inside must NOT be modified. Preserve it exactly;
  remove the `<<` `>>` delimiters in the output.
- **Field `(( ))`** — ONLY text inside may be modified; everything else in the
  block is context. Remove the `((` `))` delimiters in the output.
- Neither present: the whole surrounding block is editable.

## Context References

Double-backtick references in the prompt point to external resources.

- **As input**: read the referenced file or section for context.
- **As output**: write the requested content to the referenced destination
  (a path is resolved relative to the document's directory unless absolute).
- Remove the reference and its delimiters from the document output.

## Rules

- Only change what the prompt asks for; preserve meaning otherwise.
- Never edit protected regions; edit only field regions when fields exist.
- Consume this annotation and its consumed modifier delimiters. Preserve every
  unrelated annotation, `<@comment: ...>` tag, `<@chat-model>` block, and
  contextual literal/example byte-for-byte; if other actionable annotations
  share this block, leave them in place for the next router pass.
- If the instruction cannot be followed (for example, a referenced file does
  not exist), fail cleanly: leave the tag in place, change nothing, and report
  the error.
