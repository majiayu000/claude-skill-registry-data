---
name: html-artifact
description: Use for requested standalone HTML documents or interactive explanations when that format materially helps. Skip agent-facing files, Markdown-native deliverables, and ordinary short answers.
---

# HTML Artifact

Create a self-contained HTML document for human reading or interaction. Use it
when explicitly requested or when a standalone visual materially helps explain,
compare or explore the content. A report, plan or one-pager alone is not a trigger.
Keep agent instructions, source documents and Markdown-native deliverables in
Markdown; brief inline explanations need no HTML scaffold.

## Artifact contract

- One file with inline CSS/JS, viewport metadata and no build step. Work offline
  from a local file: no external fonts, trackers, API fetches or runtime assets.
- Semantic markup, keyboard access and adequate contrast. Layout adapts to narrow
  screens; honor reduced motion for animation and provide readable print styles.
- Explanatory content exists before scripts run. With JS disabled, preserve the
  explanation, data and limitations even when interactive computation is unavailable.
- Use project visual conventions where compatible with this contract. Show only
  sourced data; label assumptions and illustrative values explicitly.

## Choose the shape

Select the matching preset when its layout helps:

| Main purpose | Reference |
|---|---|
| Narrative report or comparison | `references/preset-report.md` |
| Charts carry the argument | `references/preset-dashboard.md` |
| Teach a concept | `references/preset-explainer.md` |
| User edits values or copies a configuration | `references/preset-editor.md` |

For an unfamiliar figure, consult `references/svg-craft.md`; for optional default
styling/components, use `references/visual-style.md`. Read only relevant sections,
and do not invent content to satisfy a preset. Prefer a simpler shape when it
communicates the source faithfully.

## Deliver and verify

Use the supplied output location, otherwise a descriptive file under scratchpad.
Provide a link/path rather than pasting HTML source. Check content fidelity and
local links, then exercise key interactions and responsive/print behavior using
available browser tools. Inspect JS-disabled readability and motion settings when
relevant. Report checks that could not run; do not automatically assign them to
the user. Name material omissions or transformations when condensing a source.
