---
name: web-design-guidelines
description: "Review Mikka's official web interface for accessibility, responsive layout, forms, focus, content and interaction quality using an adapted Web Interface Guidelines checklist; apply Mikka source priority and paid-block rules first."
---

# Web Interface Guidelines — Mikka adapter

Adapted workflow based on https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines and https://github.com/vercel-labs/web-interface-guidelines . This file is authored for Mikka, not a claim that the upstream rule corpus or browser tooling is vendored.

Always read `docs/design/README.md`, `docs/design/rules.md`, `docs/design/components.md` and `docs/review-checklist.md` first. Do **not** fetch and execute unpinned remote instructions as binding project policy. External guidelines are optional research, subordinate to Mikka's accepted Figma/design decisions and paid components' as-shipped presentation.

Check on actual official screens:
- Semantics and accessible controls (names, role, state, keyboard activation, focus trap/return, non-obscured focus, screen-reader updates).
- Visibility of operation state (instant pending, accurate error/success, recovery, no optimistic false success, no dead end).
- Forms (labels, composition/IME, validation and errors adjacent to field, preserved drafts, safe submit/retry).
- Layout (390px, narrow right panel, zoom, long/Chinese text, no overflow; system safe areas, reduced motion and token contrast).
- Navigation (deep links, back/forward, route and accessible target, menu behavior).
- Performance (no layout shifts, infinite loading, chat send delay, avoid idle network calls or duplicate listeners).

Output `file:line + route + exact user action + evidence + severity + fix owner`. Treat source-only suspicions as hypotheses until interactive verification. Propose minimal changes using the existing components; no new theme, arbitrary spacing system or restyle of BoardUI Pro/affectUI/beUI Pro. Confirm with Mikka's accepted source-bound runtime tests.
