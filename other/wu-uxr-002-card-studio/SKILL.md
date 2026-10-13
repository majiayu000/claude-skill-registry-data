---
name: wu-uxr-002-card-studio
description: Execute one slice of WU-UXR-002, the Card Studio UX remediation from the 2026-10-11 field study (bidi-safe text, truthful feedback, no lost cards, legible credits, mobile reachability, consistent publishing, send sheet, og previews, remix, Urdu UI, defaults, maker parity, ready-made tiles, gated mobile hierarchy). Use for any change to Card Studio, the WhatsApp/Instagram makers, /urdu-cards sharing or /s/ share pages while WU-UXR-002 is active. Tests first, one slice per branch, then stop.
---

# WU-UXR-002 — Card Studio UX Remediation

The canonical execution skill is:

`skills/wu-uxr-002-card-studio/SKILL.md`

Read that file in full before coding. Then follow its mandatory read order, gates and slice discipline.

## Sources

```text
specs/WU-UXR-002-card-studio-ux-remediation.md
specs/WU-UXR-002-IMPLEMENTATION-CHECKLIST.md
docs/audits/urdu-card-studio-ux-2026-10-11/   (findings CARD-UX-001…039, evidence, harness)
```

## Non-negotiable rules (summary)

- One slice per branch (`claude/wu-uxr-002<letter>-<slug>`). Stop after the slice.
- Write failing tests first. Register them in `scripts/run-contract-tests.js`, `playwright.config.js` and `.github/workflows/quality.yml`.
- Decision-line slices (H, L, M, N) and decision-gated slices (I: D-UX2-2, F homepage: D-UX2-3, O: D-UX2-1) need the decision recorded first. If it isn't, ask the user.
- Slice O (mobile hierarchy) requires production evidence. Never implement it speculatively.
- Every new string in English and natural Urdu. Run `npm run locale:generate` after HTML changes.
- Bump `sw.js` `CACHE_NAME` and its test pins when `APP_SHELL` files change.
- No user-uploaded images in remix payloads, no publishing without consent, content-free telemetry only.
- Keep `data-*` hooks stable, or update all specs and the audit harness together.
