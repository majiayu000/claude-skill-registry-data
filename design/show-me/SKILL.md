---
name: show-me
description: Show the current topic visually, inline in the conversation. Use when the user asks to see the shape of code, a flow, an architecture, or a change ("/show-me", "show me", "sketch it", "draw the flow", "what does the structure look like"). For a rendered standalone document, use html-artifact instead.
disable-model-invocation: true
---

# show-me

Explain the current topic visually, inline, with the smallest view that makes the point. Skip preamble; keep the prose around each visual to a sentence or two. Use one form, occasionally two — never a gallery.

## The forms

- **Pseudocode** — logic or an algorithm, stripped to control flow. Fenced `text`, indentation as structure.
- **Call tree** — runtime control flow: caller above, callees indented below. One branch per line.
- **Component tree** — UI or module structure, with the file path and the hooks/state that matter in parentheses on the owning line.
- **File tree** — responsibility layout: a shallow tree with a `# one-phrase role` comment per entry. Show only the directories the question touches.
- **Mermaid** — interaction, sequence, or data flow between components. Renders only where the client supports it — never in a plain terminal (rule below); keep it under ~10 nodes.
- **Whole block** — real code, when most of it is new or the user needs a copyable target shape.

## Diff shaped to the topic

The strongest device here: when the point is *what changes* and the surrounding shape already exists, show a fenced `diff` against that **shape**, not against raw source — a component tree with `+` lines for new components, a file tree with `+`/`-` for moved files, a call tree with the new call inserted, pseudocode with the changed branch. The reader sees the change in the structure they already hold.

## Rules

- Place each visual immediately after the sentence it supports; include only the calls, files, props, or states the current question needs.
- Real names from the actual code — never invented placeholders.
- Prefer the text forms over Mermaid when the reader is in a terminal; prefer a table over any of these when the content is a flat list or comparison.
- Escalate to the **html-artifact** skill when its own "HTML when all hold" gate is met — never on a single criterion. Its `references/svg-craft.md` owns rendered figures; this skill never emits HTML.

## Discovery

This is a manual skill. Some Codex integrations do not link this entrypoint;
when explicitly requested by path, read this file directly. Adding a discovery
link is separate integration work and must fit the authorized write scope.
