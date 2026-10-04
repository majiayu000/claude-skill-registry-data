---
name: codex-design-brief
description: Use when product, UI, documentation, or workflow decisions need a lightweight human-readable source of truth before implementation; create or refresh a native repo design brief that guides build, review, and visual acceptance.
---

# Codex Design Brief

Capture the design decision source before building or changing a user-facing workflow, documentation surface, or reusable process.

This is the native Codex adaptation of OMX `$design` as of upstream `oh-my-codex` main `f947e3a`: keep a maintained design source of truth for product goals, users, information architecture, visual language, components, accessibility, constraints, and open questions; replace OMX state and automatic handoffs with repo-local `DESIGN.md`, task notes, HTML artifacts, or project decision records.

## Relationship To Visual Acceptance

`$codex-design-brief` owns the design contract: what the artifact is for, who uses it, what information matters, which states exist, and what good looks like.

`$codex-visual-acceptance` owns rendered evidence: screenshots, browser/PDF inspection, visual verdicts, and reference matching.

When both are needed, write or refresh the design brief first, then validate the built artifact visually.

## Intake

Inspect existing sources before writing:

- `DESIGN.md`, ADRs, product specs, task cards, README, style guides
- screenshots, mockups, Figma exports, brand files, Storybook or component examples
- existing UI routes, CSS tokens, theme files, HTML notes, PDF/figure examples
- user constraints, non-goals, target audience, and prior decisions

If key choices are unclear, use a short `$codex-deep-interview` style pass. Do not invent brand/product requirements.

## Brief Contents

Keep the brief compact enough to guide implementation:

- Purpose and audience
- Primary workflow or reading path
- Non-goals and decision boundaries
- Information hierarchy
- Interaction states and empty/error/loading states
- Content rules and terminology
- Visual language: layout density, typography, color, spacing, imagery, components
- Accessibility and responsive constraints
- Technical or repo constraints
- Acceptance checks and visual verification plan
- Open questions and deferred decisions

## Design Quality Rules

- Prefer concrete choices over vague taste words.
- Tie choices to existing repo conventions unless the task is explicitly a redesign.
- Keep operational tools dense, scannable, and workflow-first; do not default to landing-page or hero-page framing.
- Separate confirmed facts, recommendations, and assumptions.
- Update the brief when implementation changes the decision.
- Do not use the brief as a pixel-matching loop; route that to `$codex-visual-acceptance`.

## Output

Produce or update the brief in the user's requested format. If no format is specified, use the repo's existing design-note convention, otherwise concise Markdown or a self-contained HTML artifact.

## Handoff

- For implementation planning, pair with `$codex-consensus-plan`.
- For execution, pair with `$codex-completion-loop`.
- For UI/HTML/PDF/figure review, pair with `$codex-visual-acceptance`.

## References

Read `references/design-brief-template.html` when drafting a brief from scratch.
