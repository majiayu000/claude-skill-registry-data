---
name: "Artefact: Playground"
description: "Creates interactive HTML playgrounds: self-contained single-file explorers that let users configure something visually through controls, see a live preview and copy out a prompt. Use when the user asks to make a playground, explorer or interactive tool for a topic."
when_to_use: "When the user asks for an interactive playground, explorer or visual tool for a topic, especially when the input space is large, visual or structural and hard to express as plain text."
model: sonnet
effort: high
metadata:
  glyph: ᛊ
  family: artefact
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Bash(open:*)"]
argument-hint: "[topic or thing to explore]"
---

# Playground Builder

A playground is a self-contained HTML file with interactive controls on one side, a live preview on the other and a prompt output at the bottom with a copy button. The user adjusts controls, explores visually, then copies the generated prompt back into Claude.

## When to use this skill

When the user asks for an interactive playground, explorer or visual tool for a topic, especially when the input space is large, visual or structural and hard to express as plain text.

## How to use this skill

1. **Identify the playground type** from the user's request
2. **Load the matching template** from `templates/`:
   - `templates/design-playground.md`: Visual design decisions (components, layouts, spacing, colour, typography)
   - `templates/data-explorer.md`: Data and query building (SQL, APIs, pipelines, regex)
   - `templates/concept-map.md`: Learning and exploration (concept maps, knowledge gaps, scope mapping)
   - `templates/document-critique.md`: Document review (suggestions with approve/reject/comment workflow)
   - `templates/diff-review.md`: Code review (git diffs, commits, PRs with line-by-line commenting)
   - `templates/code-map.md`: Codebase architecture (component relationships, data flow, layer diagrams)
3. **Follow the template** to build the playground. If the topic doesn't fit any template cleanly, use the one closest and adapt.
4. **Open in browser.** After writing the HTML file, run `open <filename>.html` to launch it in the user's default browser.

## Core requirements (every playground)

- **Single HTML file.** Inline all CSS and JS. No external dependencies.
- **Live preview.** Updates instantly on every control change. No "Apply" button.
- **Prompt output.** Natural language, not a value dump. Only mentions non-default choices. Includes enough context to act on without seeing the playground. Updates live.
- **Copy button.** Clipboard copy with brief "Copied!" feedback.
- **Sensible defaults + presets.** Looks good on first load. Include 3-5 named presets that snap all controls to a cohesive combination.
- **Palette and theming.** Source the palette and typography pairing from `~/.claude/library/references/artefact-conventions.md`, not from this skill or from any hardcoded example colours in `templates/`. Implement the full three-state contract from that reference: a bare `:root` light palette, `@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`, and `:root[data-theme="dark"]` so an explicit toggle wins in both directions. Give `body` an explicit background from a token. System font for UI, monospace for code/values. Minimal chrome.
- **Toggle control.** Ship the reference doc's masthead light/system/dark control verbatim rather than reconstructing it; a playground is a standalone HTML file, so the control is required, not the `Artifact`-only exception.

## State management pattern

Keep a single state object. Every control writes to it, every render reads from it.

```javascript
const state = { /* all configurable values */ };

function updateAll() {
  renderPreview(); // update the visual
  updatePrompt();  // rebuild the prompt text
}
// Every control calls updateAll() on change
```

## Prompt output pattern

```javascript
function updatePrompt() {
  const parts = [];

  // Only mention non-default values
  if (state.borderRadius !== DEFAULTS.borderRadius) {
    parts.push(`border-radius of ${state.borderRadius}px`);
  }

  // Use qualitative language alongside numbers
  if (state.shadowBlur > 16) parts.push('a pronounced shadow');
  else if (state.shadowBlur > 0) parts.push('a subtle shadow');

  prompt.textContent = `Update the card to use ${parts.join(', ')}.`;
}
```

## Common mistakes to avoid

- Prompt output is just a value dump → write it as a natural instruction
- Too many controls at once → group by concern, hide advanced in a collapsible section
- Preview doesn't update instantly → every control change must trigger immediate re-render
- No defaults or presets → starts empty or broken on load
- External dependencies → if CDN is down, playground is dead
- Prompt lacks context → include enough that it's actionable without the playground
