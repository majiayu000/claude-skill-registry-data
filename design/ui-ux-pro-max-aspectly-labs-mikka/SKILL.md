---
name: ui-ux-pro-max
description: "Mikka's adapted UI/UX Pro Max checklist for accessibility, touch, layouts, feedback, performance and interface quality. Use when reviewing or refining official Mikka Web, Desktop or iOS UI; always respect existing paid components and design decisions."
---

# UI/UX Pro Max — Mikka edition

Upstream: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), pinned in [project skill provenance](../README.md). This locally adapted text replaces upstream executable search-tool steps. Mikka intentionally did **not** vendor the Python `scripts/search.py` or CSV `data/` directory: **never attempt to invoke them**.

For full UX guidance, read the already installed:
- [quick-reference.md](references/quick-reference.md) — category rules and rationales.
- [pro-rules.md](references/pro-rules.md) — concrete touch, motion, navigation, responsive and accessibility checklist.

For a project audit, start with [mikka-ux-quality-audit](../mikka-ux-quality-audit/SKILL.md). For capability/button gaps, use [mikka-action-coverage](../mikka-action-coverage/SKILL.md); visual heuristics cannot prove a backend command is available to users.

## Mikka adaptation

1. Read `AGENTS.md`, `docs/design/README.md`, `docs/design/rules.md`, `docs/design/components.md`, the current official UI and accepted Figma. Do not synthesize a new global style, font palette or framework. Existing components own density and visual behavior.
2. Prioritize accessibility and touch/keyboard operability, honest system-status feedback, forms and error recovery, narrow layout, navigation and meaningful motion. Evaluate technical quality only after the underlying user job and operation path are correct.
3. BoardUI Pro/affectUI/beUI Pro are as-shipped; their component internals, visuals, fonts and tokens are **not** subject to upstream prescriptions. Only permitted data/text and owner-controlled adapters may change.
4. The official interface is the private hosted renderer linked with Mikka's public business contracts. Do not audit or design a second Community UI, and do not treat Expo Web as physical iOS proof.
5. Every finding must attach source-pair SHA, actual entry route, screenshot/DOM/user action, observable failure, severity, existing component to reuse, and regression/owner. Distinguish hypotheses from verified defects. Existing accepted rules and user decisions supersede generic upstream guidelines.
6. Use `mikka-browser-qa`, existing targeted test owners and local production-build screenshots to verify. Do not add general browser tests to CI or new polling.

This skill provides design intelligence and review constraints; it is not a browser, runtime action-coverage checker or release authority.
