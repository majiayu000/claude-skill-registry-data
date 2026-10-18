---
name: show-me
description: Show the current topic visually when the user explicitly asks to explain, show, visualize, or walk through it, or when it contains three or more mappings, branches, dependencies, steps, states, or interacting parts whose relationships are harder to understand in prose.
---

# Show Me

Help the user understand the current topic visually. Skip the preamble. Pick the smallest view that makes the key relationship clear, then place a brief textual conclusion next to it.

The visual is a presentation layer. It does not replace the authority of requirements, specifications, plans, tickets, source code, evidence, approvals, or verdicts. Preserve their labels, status, uncertainty, ordering, and ownership. Surface contradictions instead of resolving them in the visual.

## Choose the View

Show logic or an algorithm as pseudocode:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

Show runtime control flow as a call tree:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

Show UI structure as a component tree, including only state and module boundaries that matter:

```tsx
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

Show file responsibility or a broad refactor as a shallow file tree:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

Show a mapping where each row carries two or more attributes as a Markdown table:

| Route       | Label | Contents          |
| ----------- | ----- | ----------------- |
| `/sessions` | Inbox | active sessions   |
| `/settings` | Setup | provider accounts |

Show component interaction, control flow, or data flow with Mermaid:

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant Daemon
    User->>UI: choose command
    UI->>Daemon: send expanded prompt
    Daemon-->>UI: stream result
```

Use `diff` when the point is what changes and the surrounding shape already exists. Match the diff shape to the topic:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
-  navigateToSession
+  navigateToSession
+    subscribeToEvents
```

Show the whole block when most of it is new, omitted context would hide ownership or order, or the user needs a copyable target shape:

```ts
function expandSkill(command: string): string {
  const skillName = command.slice(1)
  return `use the ${skillName} skill`
}
```

Use one view when it is sufficient. Combine views only when each answers a distinct part of the question.

Keep text fences narrow: every pseudocode, tree, and diff line fits in 80 columns. Columns belong in a table or rendered HTML, where the chat column cannot wrap them.

## Rendered HTML

Pick the first rendering surface the host supports:

1. **Inline renderer.** When the host exposes one (for example T3 Code `html_preview` then `html_render`), use it for dense, multi-part, or tabular topics: build one self-contained page, check it with the preview tool, then render it above the reply.
2. **HTML file.** Create one focused HTML diagram, infographic, or short slide deck only when the user has explicit artifact intent and the environment supports both creating the file and presenting it through an available opener.
3. **Markdown.** Otherwise render the smallest inline table, text, diff, code, or Mermaid view.

On both HTML surfaces, match the product's colors, type, spacing, and components; use real labels and data; support desktop and mobile.

## Completion

Place each visual next to its textual conclusion. Keep only the calls, files, props, states, mappings, and boundaries needed for the current question. Completion requires that every multi-column mapping sits in a table or rendered HTML, every text fence line fits in 80 columns, the conclusion remains traceable to the authoritative source, and the visual introduces no new decision, evidence, approval, or certainty.

These criteria bind the final reply even when `show-me` shares the prompt with research, subagents, or another skill: apply the view choice to the reply that closes the turn.
