---
name: vkc-ux-audit
description: Run a VKC UX expert audit (Nielsen-style heuristic review + mobile-first flow check) and produce a prioritized issue list with severity and fixes.
metadata:
  short-description: UX expert audit (heuristics + priorities)
---

# VKC UX Audit (P0 QA Gate)

## Purpose

Use an external expert lens to catch UX defects early and keep shipping quality stable:

- mobile-first flows don’t break
- STEP3 conversion paths stay coherent
- i18n(ko/vi) doesn’t break layouts
- a11y + CWV basics are respected

## Source of truth

- Persona: `docs/UX_REVIEW_AGENT_PERSONA.md`
- Wizard guide voice: `docs/UX_AGENT_PERSONA.md`

## Scope (default)

Audit these flows end-to-end (both `ko` and `vi`):

- Visa assessment wizard → results → consult CTA
- Docgen (`docgen_unified`) wizard → preview → download
- Docgen (`docgen_parttime`) wizard → package download
- Admin leads list/detail (hot lead visibility, filters)

## Method

- Heuristic checklist: `.codex/skills/vkc-ux-audit/references/heuristics.md`
- Severity scale: S1–S4 (S1 blocks release)

## Output format (required)

Create a short report with:

1) **Scope** (routes + devices + locale)
2) **Findings** (S1→S4 order)
   - `Issue`: 1 sentence
   - `Evidence`: route + steps to reproduce
   - `Impact`: conversion / trust / frequency
   - `Fix`: concrete change proposal
3) **Quick wins (24–48h)**
4) **Backlog items (structural fixes)**

