---
name: concept2cure-design
description: The single source of truth for the Concept2Cure.RI UI. Use this skill whenever you're designing, mocking, reviewing, or implementing any Concept2Cure.RI surface. Visual language is Claude.ai-faithful (warm cream canvas + Claude orange + Styrene/Tiempos) re-skinned for biotech/pharma reviewer workflows.
user-invocable: true
---

## Authority

**This skill owns the Concept2Cure.RI UI.** Every pixel, token, copy rule and interaction in the product comes from here. The legacy UI under `client/src/concept2cure/` (ZenApp, AppsPage, industry dashboards, etc.) is being **gradually deleted and replaced** surface-by-surface, not refactored in place.

If you are Claude Code (or any agent) wiring these designs into the codebase:
- **Implement exactly what is shipped here.** Layout, spacing, copy, motion, color, density — match 1:1. Do not improvise.
- **Do not invent new patterns.** If a surface you need is not in this skill yet, stop and ask — that surface has not been designed.
- **When ambiguity exists, the token surface wins over the prototype, the prototype wins over the legacy codebase, and the legacy codebase wins over your intuition.** In that order.
- **Delete as you replace.** When you ship a new surface, remove the legacy route/page that it supersedes. Leave no orphaned UI paths.

Open questions or visual trade-offs go back to the designer of record (this skill). Do not resolve them unilaterally.

## Read order

Always consult, in this order:
1. `HANDOFF.md` — phase status + active implementation contract (which surfaces are live, which are in design, which are legacy-still-shipping).
2. `README.md` — voice, visual foundations, content rules, iconography, the 28-component registry.
3. `colors_and_type.css` — the canonical token surface. Claude.ai-exact OKLCH, shadcn semantic layer, raw Claude scales, licensed font stack with fallbacks. **Do not hard-code colors or font names in components — reference these tokens.**
4. `preview/` — specimen cards for every token category. The visual spec.
5. `ui_kits/` — the hi-fi React references. These are the **authoritative implementations** — copy their JSX structure, class names, and CSS rules into the product codebase wholesale.

## UI kits (current phase status)

- `ui_kits/home/` — **Phase 1 · READY FOR IMPLEMENTATION.** Front-door home screen. 15-item rail, domain switcher, time-of-day greeting, composer with suggestion pills, AnA proactive briefing card, dashboard, module launcher, recent activity, ⌘K command palette. This replaces the legacy `projects` / `mission-control` / `IndustryAwareApp` home.
- `ui_kits/ana_ri/` — **Reference · NOT READY FOR IMPLEMENTATION.** Chat-first shell. Informs the Projects detail surface (phase TBD).
- `ui_kits/ectd_coauthor/` — **Reference · NOT READY FOR IMPLEMENTATION.** 3-pane System-Aware Artifact workbench. Informs the Artifact surface (phase TBD).

## Non-negotiables

These come from `README.md` — every agent must enforce them without exception:

- **Sentence case everywhere.** Titles, headings, buttons, menu items. Never Title Case. Never ALL CAPS except 10px metadata labels.
- **No emoji. No exclamation marks. No cheerleading.** The system confirms, never celebrates.
- **Body = 13px**, max title = 18–24px. Never shout.
- **Claude orange (`#d97757`) is the only strong color.** Used sparingly — one focal point per screen.
- **200ms ease-out motion.** No bounce, no spring, no overshoot.
- **Lucide icons only.** Never mix icon systems.
- **Numbers over adjectives.** "Reviewed by 12 reviewers across 4 agencies" beats "comprehensively reviewed".
- **Every destructive action confirms calmly.** No "Are you sure?" panic modals.

## Working mode

- **Design requests** → surface a hi-fi HTML prototype under `ui_kits/` or a specimen under `preview/`. Register it as an asset.
- **Implementation requests (Claude Code)** → read the matching `ui_kits/*` directory, mirror its structure into the codebase under `client/src/concept2cure/` (or the v2 equivalent), and delete the legacy surface it replaces.
- **Ambiguity** → ask. Do not guess.
