---
name: cite
description: Reactant tag-only citation. Use only when execute or execute-one dispatches an exact <@cite> tag from a document; never activate from ordinary chat or another skill.
---

# Cite

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@cite...>` annotation in a target document and hands off its
context. Never activate it from ordinary chat, semantic similarity, or any
skill other than those two routers. Without that handoff, do not search or
change files; direct the user to add the tag and run a router.

Find a reference that supports the claim next to the tag, insert a citation,
then consume the tag.

## Tag

```
<@cite>
<@cite: source hint or search instruction>
```

Examples: `<@cite: search arxiv>`, `<@cite: ``refs.bib``>`,
`<@cite: the original transformer paper>`.

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it. The claim to support is the statement the tag is
  attached to.
- **Prompt** (optional) — where or how to find the reference: a bibliography
  file, an arXiv or web search, or a description of the intended source.

## Workflow

1. Read the surrounding block and identify the claim that needs support.
2. Determine the citation source: a referenced `.bib`/`.md` file, an arXiv or
   web search using whatever search capability the host provides, or a
   specific work named in the prompt. Prefer peer-reviewed or well-cited
   sources when searching.
3. Determine the citation format from the document itself: LaTeX uses
   `\cite{key}`; Markdown typically uses `[number]` or `[@key]`. Match the
   style already used in the document.
4. Insert the citation at the tag's position and remove the tag.
5. In a LaTeX project, when citing a work not already in the bibliography, add
   a BibTeX entry to the referenced or main `.bib` file. Do not duplicate an
   existing entry.

## Context References

Double-backtick references in the prompt usually name the citation source
(for example `<@cite: ``refs.bib``>`). Resolve paths relative to the
document's directory unless absolute. Remove the delimiters from the output.

## Rules

- Insert citation material only — do not rewrite the surrounding prose.
- Consume this annotation and its reference delimiters. Preserve every
  unrelated annotation, `<@comment: ...>` tag, `<@chat-model>` block, and
  contextual literal/example byte-for-byte.
- If no credible source can be found, replace the tag with
  `[citation needed]` and warn the user; that is a completed no-result, not a
  failure.
- If the host has no search capability and the prompt requires one, fail
  cleanly: leave the tag, change nothing, report the missing capability.
- Reactant adds no verification layer on top of this protocol; the citation
  is whatever this workflow produces.
