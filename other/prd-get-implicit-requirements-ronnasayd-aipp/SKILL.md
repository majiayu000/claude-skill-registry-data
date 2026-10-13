---
name: prd-get-implicit-requirements
description: 'Extract implicit requirements from product requirement documents (PRDs), identify coverage gaps across 14 universal categories, and generate clarification questions for stakeholders. Use when user says "analyze PRD for gaps", "extract implicit requirements", "find missing requirements", "what''s not defined in our spec", "identify PRD holes", or "get clarification questions from PRD". Systematically covers: interface states, error handling, navigation, data persistence, network behavior, security, performance, platform behavior, content fallbacks, localization, accessibility, legal compliance, deployment, and observability.'
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

Finds what a PRD doesn't say, then turns those gaps into triaged, batched questions for stakeholders — not a rewrite of the PRD itself.

## Flow

| Phase                 | Action                                                                                                                                                | Output / Gate                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1. Structured Reading | Read full PRD, no notes yet. Identify product type, target platforms, external integrations, MVP scope. List covered domains + explicit out-of-scope. | Can describe product in 2 sentences + list main flows |
| 2. Gap Analysis       | Walk `references/gap-categories.md` — 14 categories, ask "does PRD define behavior for this?" per item                                                | Raw gap list tagged Critical/Important/Nice-to-have   |
| 3. Triage             | Apply triage table below before asking anything                                                                                                       | Filtered list: ask vs. auto-decide vs. defer          |
| 4. Elicitation        | Group into thematic rounds of 3-4 questions                                                                                                           | Rounds delivered to stakeholder                       |
| 5. Document           | Record each decision using `references/decision-entry-template.md`                                                                                    | PRD updated, decisions traceable                      |
| 6. Completion         | Run checklist below                                                                                                                                   | All critical gaps closed                              |

## Phase 3 — Triage table

| Condition                                 | Action                                   |
| ----------------------------------------- | ---------------------------------------- |
| Clear platform convention exists          | Document default, don't ask              |
| Decision affects architecture             | Ask before any implementation            |
| Decision blocks deployment/store approval | Highest priority, round 1                |
| Decision is purely visual/cosmetic        | Use best practice; ask only if uncertain |
| Explicitly out of MVP scope               | Record as deferred, don't ask            |

## Phase 4 — Elicitation rounds

- **Round 1:** Critical (security, legal, architecture blockers)
- **Round 2:** Core UX and main flows
- **Round 3:** Details (formats, fallbacks, edge cases)

Each question: one-line context (why it matters), 2-4 options with consequences (not just names), recommended option flagged when best practice exists.

## Phase 6 — Completion checklist

- [ ] Every critical gap has a documented decision
- [ ] No decision contradicts PRD's explicit scope
- [ ] Deferred decisions have a target version
- [ ] PRD revision date updated
- [ ] Dev team notified of additions

## Pocket Heuristics

- PRD defines **what** but not **what happens on failure** → gap.
- PRD defines a **feature** without empty/error/loading state → 3 gaps.
- Product targets a **specific platform**, PRD silent on native behaviors → integration gap.
- Product **collects data**, PRD silent on consent → legal gap.

## Reference files

- `references/gap-categories.md` — full 14-category question list for Phase 2 gap analysis
- `references/decision-entry-template.md` — Phase 5 decision entry format + insertion rules
