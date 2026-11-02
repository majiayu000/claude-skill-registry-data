---
name: resolve
description: Reactant tag-only chain resolution. Use only when execute or execute-one dispatches an exact <@resolve> tag attached to a complete chat chain; never activate from ordinary chat or another skill.
---

# Resolve

## Activation Boundary

This is a tag-only worker skill. Use it only after `execute` or `execute-one`
selects an exact `<@resolve>` annotation and supplies its attached document
chat chain. Never activate it from a chat-window request, semantic similarity,
or any skill other than those two routers. Without that handoff, do not apply
conversation content to authored prose.

Consume a complete document-local chat chain: apply its final intent to the
authored text, then remove every chain tag so only clean prose remains.

## Tag

```
<@resolve>
```

Placed as the next annotation after the last element of a chain that contains
at least one `<@chat-model>` response:

```
original paragraph...
<@chat-user: how can this be improved>
<@chat-model name="some-model">
suggestion text
</@chat-model>
<@resolve>
```

## Input

- **File path** — the document being processed.
- **The chain** — all `chat-user`/`chat-model` turns in order. The user may
  have edited any turn, including model responses; the edited text is the
  authoritative history.
- **Preceding authored block** — the text the chain discusses and that this
  skill will revise.

## Workflow

1. Read the preceding authored block and the full ordered chain.
2. Determine the final intent: the latest `<@chat-model>` response (and any
   later user follow-up) takes precedence; earlier turns resolve ambiguity
   about goals and constraints.
3. Apply that intent to the authored block's prose.
4. Write the result back: replace the authored block plus the entire chain —
   every `<@chat-user>` tag, every `<@chat-model>` block, and the
   `<@resolve>` tag — with the revised prose alone.

## Scope Modifiers

- **Protect `<< >>`** — content must NOT be modified, even if the chain
  suggests changing it. Keep the content exactly; remove the delimiters in
  the output.
- **Field `(( ))`** — ONLY text inside fields may be modified. Remove the
  delimiters in the output.
- Neither present: the whole authored block is editable.

## Rules

- Follow the chain's final intent faithfully; this step applies decisions
  that were already made in the conversation.
- Remove the complete chain and consumed modifier delimiters; leave no
  `chat-user`, `chat-model`, or `resolve` syntax behind. Preserve every
  unrelated annotation, `<@comment: ...>` tag, and contextual literal/example
  byte-for-byte.
- Only this skill moves chain content into authored prose; if the chain is
  somehow incomplete (no `<@chat-model>` present), fail cleanly: change
  nothing and report.
