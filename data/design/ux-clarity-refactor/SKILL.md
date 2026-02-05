---
name: ux-clarity-refactor
description: General UX/UI refactor patterns for dense information products, including layout compression, view-mode clarity, selection-to-results flow, research workspace design (non-chat), and enforcing a no-emoji UI policy. Use when restructuring existing UIs for clarity while preserving all features.
---

# UX Clarity Refactor

## Use this workflow

1) Audit the current UI
- List primary user tasks and critical features that must remain.
- Map the main views/modes and the current navigation paths.
- Identify where vertical space is being spent without adding value.

2) Apply layout compression
- Replace oversized hero blocks with a compact summary + actions row.
- Move long descriptive copy into a short paragraph or collapsible panel.
- Use a split layout: primary content on the left, compact summary cards on the right.

3) Clarify view modes
- Separate mode switching (globe/grid/scroll) from filter controls.
- Add a view header that states what is being shown, and why.
- Show quantitative context (article count, source count, filters active).

4) Improve selection-to-results flow
- A selection should update a dedicated context panel instantly.
- Always show the selected state and a single clear action to reset.
- Order results by importance: top sources first, then top articles.

5) Build research workspaces (non-chat)
- Use an input bar at the top.
- Output in two columns: Brief on the left, Evidence/Steps on the right.
- Provide a Flow view that shows reasoning steps in sequence.
- Keep chat history optional and secondary (sidebar or history tab).

6) Enforce the no-emoji rule
- Remove emojis from UI text, logs, and docs.
- Replace with icons, bullets, or plain text labels.
- Scan the repo for emojis using ripgrep and clean all hits.

## References
- See `references/patterns.md` for compact layout patterns, status display conventions, and sample copy rules.
