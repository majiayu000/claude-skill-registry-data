---
name: figure
description: Reactant tag-only figure generation. Use only when execute or execute-one dispatches an exact <@figure> tag from a document; never activate from ordinary chat or another skill.
---

# Figure

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@figure...>` annotation in a target document and hands off
its context. Never activate it from an ordinary chat image request, semantic
similarity, or any skill other than those two routers. Without that handoff,
do not generate or save an image.

Generate an image described by the prompt and surrounding context, save it,
and replace the tag with an image reference.

## Tag

```
<@figure: description of the figure>
<@figure: description, save to ``figures/name.png``>
```

## Input

- **File path** — the document being processed.
- **Surrounding block** — the maximal run of non-blank lines containing the
  tag; blank lines bound it.
- **Prompt** (optional) — the figure description. If absent, infer the figure
  from the surrounding text.

## Workflow

1. Read the prompt and surrounding block. Resolve any double-backtick context
   references: input references are files to read for context; an output
   reference is the image destination.
2. Synthesize a detailed image-generation prompt from the user's intent and
   the document context.
3. Generate the image with whatever image-generation capability your host
   provides — a built-in tool, an MCP tool, or an API the user has
   configured. Reactant does not prescribe or hardcode a provider.
4. Save the image:
   - To the output context reference, when the prompt gives one (path
     relative to the document's directory unless absolute).
   - Otherwise to a `figures/` directory next to the document (create it if
     needed), with a sanitized name derived from the prompt: lowercase,
     underscores, no spaces or special characters (for example
     `figures/system_architecture.png`).
5. Replace the `<@figure: ...>` tag with a format-appropriate reference using
   a path relative to the document:
   - Markdown: `![description](figures/name.png)`
   - LaTeX: `\includegraphics{figures/name.png}` (inside a figure environment
     when the document's existing figures use one)

## Rules

- Consume only this tag; do not rewrite surrounding prose. Preserve every
  unrelated tag, `<@comment: ...>` tag, `<@chat-model>` block, and escaped
  literal byte-for-byte.
- If the host has no image-generation capability, fail cleanly: leave the
  tag, change nothing, and report the missing capability.
- The generated image is accepted as produced; Reactant runs no quality
  check, regeneration, or second model pass on it.
