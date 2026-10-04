---
name: review
description: This skill should be used when the user wants an honest overall assessment of a venture — a board-style review, go/no-go decision, kill-pivot-persevere call, investment-readiness check, or periodic check-in — e.g. "review my whole venture", "should I continue with this", "be brutally honest about this business", "monthly business review", "is this worth pursuing", "کل بیزینس رو نقد کن", "بی‌رحمانه بررسی کن", "ادامه بدم یا نه", "جلسه هیئت مدیره", "ارزیابی کلی ونچر". Produces a cross-module scorecard with a kill/pivot/persevere/double-down recommendation and updates the decision log.
version: 1.0.0
---

# Venture Review — The Board Meeting

Step back from module-level work and answer the only question that matters: **is this venture working, and what's the highest-leverage next move?** Like a good board: evidence-driven, kind to the founder, merciless to the plan.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Read the whole venture

Everything: VENTURE.md, all module reports (latest dated file per module), decision log, open assumptions. Plus ask the user: **what changed since the last review?** (new numbers, customer events, money/runway, morale — runway and energy are real variables; ask, respectfully).

### 2. Cross-module scorecard

| Dimension | Source | Grade (A–F) | Evidence | Freshness |
|---|---|---|---|---|
| Problem & demand validation | 01-discovery | | | |
| Market attractiveness | 02-market | | | |
| Competitive position | 03-competitors | | | |
| Product-market fit | 04-pmf | | | |
| GTM execution & traction | 05-gtm + user data | | | |
| Economics viability | 06-model | | | |

Rules: a grade needs evidence from the files — no evidence, grade is `?` (and that's a finding: "we don't know X" is a top risk). Mark **stale** anything >90 days old or invalidated by newer findings (e.g. model built on a price GTM later changed) and set those modules `stale` in VENTURE.md.

### 3. Coherence check (the cross-module value — modules can each pass while the whole fails)

- Does the GTM target segment = the segment discovery/PMF found actually loves it?
- Does pricing in the model = pricing in GTM = willingness-to-pay in discovery?
- Does SOM support the model's growth assumption?
- Did any module's "riskiest assumption" get quietly forgotten? List the still-untested ones with age.

### 4. Adversarial pass — mandatory

Launch **`venture:devils-advocate`** with: venture one-liner, the scorecard + your tentative recommendation, paths to the 2–3 most load-bearing reports, and "what decision rides on this" (continue/kill/raise/invest more time). Integrate: address every critical objection — accept (changes the recommendation), rebut (with evidence, cited), or downgrade confidence visibly.

### 5. Verdict

`<slug>/venture-review-YYYY-MM-DD.md` (in `report_language`):

1. **State of the venture** — one honest paragraph.
2. **Scorecard** (above) + coherence findings.
3. **Top 3 risks**, ranked, each with cheapest mitigation/test.
4. **Recommendation — pick one, commit:**
   - **Double-down** — evidence of working engine; name what to pour fuel on and what to stop doing (focus = stopping things).
   - **Persevere** — on track, no step-change; name the milestone and date for next review.
   - **Pivot** — core assumption broke but an asset is real (a retaining segment, a channel that converts, a team skill); name 1–2 concrete pivot directions *grounded in the strongest evidence found*, and the module sequence to validate them.
   - **Kill** — kindly, plainly, with the evidence; what was learned, what's salvageable (relationships, code, audience). A clean kill is a win, not a failure — say that and mean it.
5. **Next 30 days** — 3–5 actions max, each mapped to a module or real-world task.
6. **For client ventures:** add a client-facing executive summary (1 page, diplomatic but unspun).

### 6. Close the loop

Append the recommendation + rationale to VENTURE.md Decision log (date, decision, rationale — one row). Update statuses/staleness. Set the next review trigger ("after 30 days or when <metric/event>").

## Quality bar

- The recommendation must be falsifiable: "persevere IF X by DATE" — never "keep going and see".
- Sunk cost is not evidence; "we've worked on it 8 months" appears nowhere in the reasoning.
- Respect the human: deliver hard verdicts with care, but never soften them into ambiguity — ambiguity steals months.
