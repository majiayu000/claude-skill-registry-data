---
name: web-design-guidelines
description: Review the starter's web UI for clear states, keyboard access, responsive layout, readable tables, and accessible forms.
---

# Interface review for this starter

This file is original project guidance. The broader upstream guidance is available at [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines); it is linked rather than redistributed here.

For UI changes, review the actual page at narrow and wide viewport sizes and check these points:

1. Every input has a visible label and a useful error message. Keyboard users can reach and operate upload, selection, token, and run controls.
2. Focus remains visible. Disabled and pending states explain what the user should expect next.
3. Transaction status is communicated in text, with color as a secondary cue. Screen readers receive updated status without excessive announcements.
4. Tables retain understandable headings and cell associations. On a small screen, users can still find descriptions, amounts, decisions, and progress.
5. Empty, loading, retry, error, review, and completion states are distinct. Avoid hiding a failed stream or uncertain classification.
6. Run `bun run lint:design` and verify the page in a browser after significant visual changes.

Standards reference: [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
