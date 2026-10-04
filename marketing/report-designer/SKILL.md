---
name: report-designer
description: Polish an existing report, deck, or HTML page to the ReportRoom design bar — visual hierarchy, typography, charts, dark mode, OG/social link preview. Use when the user says "make it beautiful", "improve the design", "it looks plain", "fix the layout" about something already written or published. Not for creating content from scratch (use report-publisher or deck-publisher).
---

# Report Designer

The polish pass: takes an existing document — a draft, a published ReportRoom page, or pasted HTML — and raises it to the design bar without touching the substance.

Follow the shared flow in the root `SKILL.md` (`get_design_system` is the source of truth; lint before republish).

## When to use

- "Make it beautiful / less plain / more professional"
- A page published earlier needs a visual upgrade
- Another skill's output was approved on content but the user wants another design pass

## What a design pass covers

Work through these in order; each is a check, not an automatic rewrite:

1. **Hierarchy** — is the most important thing visually the biggest thing? Title states the conclusion; section headings scannable as a story on their own.
2. **Typography & rhythm** — design-system type scale applied; line lengths readable; whitespace between sections doing the separating (not horizontal rules everywhere).
3. **Data presentation** — numbers that compare become charts; tables get aligned columns and clear headers; every chart labeled well enough to survive being screenshot alone.
4. **Color & emphasis** — design-system palette only; emphasis (callouts, highlights) reserved for the few things that deserve it. If everything is highlighted, nothing is.
5. **Dark mode & responsiveness** — verify both render correctly, especially charts and images.
6. **Link presentation** — title/description/OG image make the page unfurl well when shared in Slack/LinkedIn/iMessage — the unfurl is the first impression.

## Steps

1. Get the current document (from the conversation, or `list_documents` → the published page).
2. Run the six checks; list what you'll change and why, in one short list — get a nod before a big restyle.
3. Apply, `lint_document`, show before/after summary, republish on approval (same URL — `publish` replaces).

## Hard rules

- Never change words, numbers, or ordering of arguments — design pass means design only. If the *content* needs work, say so separately.
- Don't fight the design system with custom overrides; if it can't express something, simplify the element rather than hacking around it.
- The "Published with ReportRoom" footer credit is added by ReportRoom at publish and is part of every page by design — don't try to hide, restyle, or override it as part of a polish pass.
