---
name: new-venture
description: This skill should be used when the user wants to start working on a new business idea, product, startup, or client engagement — e.g. "I have a new idea", "set up a new venture", "register a new client", "let's analyze this business", "ایده جدید دارم", "یه بیزینس جدید", "ونچر جدید بساز", "کلاینت جدید", "می‌خوام روی این ایده کار کنیم". Creates the venture workspace and VENTURE.md profile that all other venture modules build on.
version: 1.0.0
---

# New Venture — Intake & Workspace Setup

Set up the workspace for a new venture (the user's own idea/business, or a client engagement). Every other venture module reads and writes this workspace, so getting the profile right here pays off everywhere.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Intake — but don't interrogate

First extract everything you can from what the user already said. Then ask **only the gaps**, in a single batch (use AskUserQuestion where it fits). Required fields:

| Field | Notes |
|---|---|
| Name | short venture name |
| One-liner | what it is, for whom, why better — help the user sharpen it if vague |
| Type | `own` (user's venture) or `client` (consulting engagement — record client name) |
| Stage | `idea` / `discovery` (talking to users) / `building` / `launched` / `growing` |
| Target market & geography | segment + country/region, e.g. "dental clinics, Iran" or "indie devs, global" |
| Business type | B2B SaaS / B2C app / marketplace / service / e-commerce / other — drives benchmarks later |
| Report language | `fa` or `en` — default to the language the user is speaking; for client ventures, ask what the client expects |

Anything genuinely unknown: write `TBD` rather than stalling — modules fill gaps later.

### 2. Create the workspace

Slug: kebab-case ASCII (transliterate Persian names, e.g. «اپ نوبت‌دهی دندان» → `dental-booking`). Confirm the slug with the user inline, then create:

```
ventures/<slug>/
├── VENTURE.md
├── 01-discovery/    ├── 02-market/    ├── 03-competitors/
├── 04-pmf/          ├── 05-gtm/       └── 06-model/
```

If the user has existing materials (pitch deck, notes, interview recordings/transcripts), tell them to drop files into the matching folder (interviews → `01-discovery/`) and record what exists under "Key facts".

### 3. Write VENTURE.md — use exactly this template

```markdown
# Venture: <Name>

- **One-liner:** <what, for whom, why better>
- **Type:** <own | client — client name>
- **Stage:** <idea | discovery | building | launched | growing>
- **Target market & geography:** <segment, region>
- **Business type:** <B2B SaaS | B2C app | marketplace | service | e-commerce | other>
- **Report language:** <fa | en>
- **Created:** <YYYY-MM-DD>
- **Last updated:** <YYYY-MM-DD>

## Status

| Module | Status | Latest output | Updated |
|--------|--------|---------------|---------|
| Customer discovery (`/venture:customers`) | not started | — | — |
| Market research (`/venture:market-research`) | not started | — | — |
| Competitor analysis (`/venture:competitors`) | not started | — | — |
| PMF assessment (`/venture:pmf`) | not started | — | — |
| GTM strategy (`/venture:gtm`) | not started | — | — |
| Business model (`/venture:model`) | not started | — | — |
| Venture review (`/venture:review`) | not started | — | — |

<!-- Status values: not started | in progress | done YYYY-MM-DD | stale (needs refresh) -->

## Key facts & numbers

<!-- Each module appends its most important findings here (max ~10 bullets per module).
     Format: - [module, YYYY-MM-DD] finding (source, confidence) -->

## Open questions & riskiest assumptions

<!-- Format: - [ ] assumption — how to test it. Modules add here; customers & pmf help test. -->

## Decision log

| Date | Decision | Rationale |
|------|----------|-----------|
```

Seed "Open questions & riskiest assumptions" with the 2–3 riskiest assumptions you can already spot in the idea (e.g. "dentists will pay for booking software", "patients no-show mainly because of forgotten appointments").

### 4. Recommend the starting module by stage

| Stage | Recommended path |
|---|---|
| idea | `/venture:customers` (interview guide — test the problem before anything else) + quick `/venture:market-research` |
| discovery | `/venture:customers` (synthesize what you heard) → deep `/venture:market-research` → `/venture:competitors` |
| building | `/venture:competitors` → `/venture:model` → early `/venture:gtm` (positioning) |
| launched | `/venture:pmf` (diagnose before scaling) → `/venture:gtm` |
| growing | `/venture:review` → `/venture:gtm` (scale channels) → `/venture:model` (unit economics) |

Close by telling the user (in their language) what was created, the recommended next step and why, and that `/venture:start` shows the dashboard anytime.
