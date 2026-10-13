---
name: managing-design-briefs
description: >
  Brief-before-generation system with locked design tokens and anti-slop enforcement
  for Loxihart and FlashFusion brand profiles. Use this skill whenever someone asks to
  build, spec, audit, or generate any UI — component, dashboard, panel, landing page,
  browser extension, artifact, or design system. Also activates on: design brief,
  design tokens, anti-slop, v0, AI Studio, generator prompt, token drift, visual
  direction, color system, typography system, FlashFusion UI, Loxihart tool, Stitch pipeline,
  "does this pass the gates", "brief before generation", or any request that touches
  how something looks or is styled. If a UI is involved, use this skill first — even
  for small components. Do NOT use for pure backend work, data analysis, or
  non-visual deliverables (route those to doc/pptx/ROI skills).
metadata:
  version: "5.1.0"
---

# Managing Design Briefs

Brief-before-generation with locked tokens, anti-slop gates, and adversarial critic.
Two brand profiles (Loxihart, FlashFusion) share one workflow — tokens and aesthetic direction differ.

## Evals

**Should trigger:**
1. "I'm about to build a dashboard panel — let's start"
2. "Does this design pass the anti-slop gates?"
3. "Define the tokens before I generate this in v0"

**Should NOT trigger:**
1. "Build the React component directly, skip the brief" — only acceptable when design direction is already fully specified; otherwise the brief is mandatory first (this skill owns that gate)
2. "Write pure backend logic with no UI component" — no visual deliverable → route to a backend/build skill (e.g. kyle-vibe-coding)

---

## Hard Rules

1. **Brief before generation. Always. No exceptions.** If no brief exists — stop, create one, wait for confirmation.
2. **Profile confirmed before tokens load.** Never mix profiles mid-session.
3. **All 7 anti-slop gates pass before any output.** No partial passes. Fix or stop.
4. **Adversarial critic runs on every brief before generation.** Not optional for STANDARD/FULL scope.

---

## Quick-Start Decision Tree

```
Request arrives
  │
  ├─ Confirm profile first ─────────────────────────────────────────────
  │   ├─ Loxihart      (enterprise tool, internal dashboard, MSP context)
  │   └─ FlashFusion (product UI, landing page, artifact, app.ff.co)
  │
  ↓ (profile confirmed)
  │
  ├─ New brief needed ──────────────── workflows/brief-creation.md
  ├─ Audit existing brief ─────────── workflows/anti-slop-gates.md → gap list
  ├─ Adversarial critic pass ──────── workflows/adversarial-critic.md
  ├─ Extract generator prompt ──────── templates/generator-prompt-template.md
  ├─ Token drift check ────────────── workflows/token-drift-audit.md
  │                                   (or run scripts/token-drift-check.py)
  ├─ Update locked tokens ─────────── Edit references/[profile]-tokens.md
  │                                   Note version + reason
  ├─ Multi-session / 3+ screens ────── references/advanced.md
  └─ Sales / doc / SPIKE ──────────── Not UI → redirect
```

---

## Profile Summary (Locked Tokens in references/)

Load only the active profile — never both.

| Profile | Token file | Aesthetic |
|---|---|---|
| Loxihart | `references/Loxihart-tokens.md` | Flat void surface, electric violet, Space Grotesk + Inter, flat cards, dense enterprise |
| FlashFusion | `references/FlashFusion-tokens.md` | Void-dark #0B0B14, blur(12px) glass cards, Instrument Serif + Geist, violet/magenta/cyan |

**Cross-profile contamination is a hard failure.** See each token file's isolation section.

---

## Workflow Routing

| Task | Where to go |
|---|---|
| Creating a new brief | `workflows/brief-creation.md` |
| Running anti-slop gates | `workflows/anti-slop-gates.md` |
| Adversarial critic review | `workflows/adversarial-critic.md` |
| Checking output for token drift | `workflows/token-drift-audit.md` or `scripts/token-drift-check.py` |
| Filling the brief template | `templates/brief-template.md` |
| Building the generator prompt | `templates/generator-prompt-template.md` |
| OKLCH / multi-session patterns | `references/advanced.md` |

---

## Scope Gate

- **LITE** (single component, one-shot): gates 1–7 + brief template. Skip adversarial critic.
- **STANDARD** (multi-component, dashboard, page): full workflow + adversarial critic.
- **FULL** (design system, multi-session, pipeline): full workflow + adversarial critic + dual-file pattern from `references/advanced.md`.
