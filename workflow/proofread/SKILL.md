---
name: proofread
description: Reactant tag-only proofreading. Use only when execute or execute-one dispatches an exact <@proofread> tag from a document; never activate from ordinary chat or another skill.
---

# Proofread

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@proofread...>` annotation in a target document and hands
off its context. Never activate it from an ordinary chat-window request,
semantic similarity, or any skill other than those two routers. Without that
router handoff, do not change the document; tell the user to add the tag and run
one of the routers.

Fix grammar, spelling, and punctuation in the surrounding block, then consume
the tag.

## Tag

```
<@proofread>
<@proofread: optional narrower instruction>
```

Example: `<@proofread: only fix punctuation>`.

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it.
- **Prompt** (optional) — narrows the scope. Default: fix all mechanical
  errors.

## Workflow

1. Read the surrounding block; read the full file if broader context helps
   (for example, to recognize intentional terminology).
2. Fix grammar, spelling, and punctuation errors only.
3. Write the result back: replace the surrounding block (including the
   `<@proofread>` tag) with the corrected text.

## Scope Modifiers

- **Protect `<< >>`** — must NOT be modified even if it contains errors.
  Preserve the content exactly; remove the delimiters in the output.
- **Field `(( ))`** — ONLY text inside may be corrected. Remove the delimiters
  in the output.

## Context References

Double-backtick references in the prompt point to resources to consult (for
example a glossary of domain terms that must not be "corrected"). Resolve
paths relative to the document's directory unless absolute. Remove the
delimiters from the output.

## Rules

- Do not change meaning, tone, or style; fix errors only, never rewrite.
- Consume this tag and its consumed modifier delimiters. Preserve every
  unrelated tag, `<@comment: ...>` tag, `<@chat-model>` block, and escaped
  literal byte-for-byte.
- On any error (for example an unreadable referenced file), fail cleanly:
  leave the tag, change nothing, report.
