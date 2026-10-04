---
name: competitors
description: This skill should be used when the user asks for competitor analysis, competitive landscape, battlecards, positioning maps, or "who else does this" — e.g. "analyze my competitors", "competitive analysis for X", "build a battlecard", "who are the alternatives", "تحلیل رقبا", "رقیب‌های این محصول کیان", "رقبا رو بررسی کن", "بتل‌کارت بساز", "مقایسه با رقبا". Produces competitor profiles, a comparison matrix, positioning map, and battlecards in the venture workspace.
version: 1.0.0
---

# Competitor Analysis — Landscape, Matrix & Battlecards

Map who competes for the same customer money/attention, find the exploitable gaps, and arm the user (or their client) with battlecards. The deliverable is **differentiation strategy**, not a competitor encyclopedia.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Discover the landscape

- Ask the user which competitors they already know (they always know some).
- Search for more — including **local-language** queries for local markets («نرم‌افزار نوبت‌دهی مطب» finds Iranian competitors that English queries never will).
- Crucially include **non-obvious competition**: indirect tools solving the same job differently, and the status quo (Excel, paper, a secretary, doing nothing). The status quo is usually the #1 competitor.
- Categorize: `direct` / `indirect` / `substitute (status quo)`.

### 2. Select targets with the user

Propose the full list, agree on **3–6 for deep profiling** (direct leaders + the most dangerous indirect). More than 6 dilutes quality.

### 3. Deep-dive — fan out scouts in parallel

Launch one **`venture:competitor-scout`** agent per selected competitor — **all in a single message (parallel Agent calls)**. Each prompt must include:
- competitor name + homepage (if known),
- the venture one-liner + target segment (so the scout assesses *relative* threat),
- the profile template path: `${CLAUDE_PLUGIN_ROOT}/skills/competitors/references/profile-template.md` (tell the scout to read and fill it),
- output destination: return the filled profile as the final message.

Save each returned profile to `ventures/<slug>/03-competitors/profiles/<competitor-slug>.md`. For substitutes/status quo, write a short profile yourself inline (no scout needed).

### 4. Synthesize

Write `ventures/<slug>/03-competitors/competitive-analysis-YYYY-MM-DD.md` in `report_language`:

1. **Landscape overview** — categorized list, one line each.
2. **Comparison matrix** — rows: competitors + *this venture*; columns: target segment, pricing, key features (3–5 that matter to the ICP), traction signal, primary channel, weakness.
3. **Positioning map** — pick the 2 axes that matter most to the buyer (e.g. price ↔ premium, generalist ↔ specialist); place everyone; **name the empty quadrant** and whether it's empty because it's gold or because it's a graveyard.
4. **SWOT for this venture** vs the field — grounded in matrix facts, not vibes.
5. **Where to win** — 2–3 differentiation opportunities with the evidence (gaps in matrix + complaints found in reviews), and what NOT to compete on.
6. **Battlecards** — for the top 2–3 threats, copy `references/battlecard-template.md` to `03-competitors/battlecard-<competitor>-YYYY-MM-DD.md` and fill each copy (essential for client/sales use).

### 5. Close the loop

- Update VENTURE.md: Status row → `done YYYY-MM-DD`; key facts (main threats, chosen differentiation angle, pricing range in market); add risky assumptions (e.g. "users will switch from X for feature Y" → test via `/venture:customers`).
- Suggest next: `/venture:gtm` (positioning builds directly on this) or `/venture:model` (market pricing now known).

## Quality bar

- Review mining beats feature lists: competitors' 1–2★ reviews are a map of unmet needs — quote them.
- Treat competitor marketing claims as claims, not facts; mark traction estimates with confidence.
- "This market has a strong default incumbent and no exploitable gap" is a valid, valuable conclusion — say it if true.
