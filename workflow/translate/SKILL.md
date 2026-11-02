---
name: translate
description: Reactant tag-only translation. Use only when execute or execute-one dispatches an exact <@translate> tag from a document; never activate from ordinary chat or another skill.
---

# Translate

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@translate...>` annotation in a target document. Never
activate it from ordinary chat, semantic similarity, or another non-router
skill. Without that handoff, change nothing.

Translate the surrounding block into the requested language, then consume
the tag.

## Tag

```
<@translate: target language>
```

Example: `<@translate: German>`.

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it.
- **Prompt** — the target language, optionally with style notes.

## Workflow

1. Read the surrounding block; read the full file if terminology context
   helps.
2. Translate the authored prose into the target language. Leave citation
   keys, code spans, and LaTeX commands untranslated.
3. Write the result back: replace the surrounding block (including the
   `<@translate: ...>` tag) with the translation.

## Scope Modifiers

- **Protect `<< >>`** — content stays in the original language, untouched;
  remove the delimiters in the output.
- **Field `(( ))`** — translate only inside the field; remove the delimiters
  in the output.

## Context References

Double-backtick references in the prompt (for example a glossary file) are
inputs; resolve paths relative to the document's directory unless absolute.

## Rules

- Consume this tag and its consumed modifier delimiters. Preserve every
  unrelated tag, `<@comment: ...>` tag, `<@chat-model>` block, and contextual
  literal/example byte-for-byte.
- If no target language is given or a referenced file is unreadable, fail
  cleanly: leave the tag, change nothing, report the error.
