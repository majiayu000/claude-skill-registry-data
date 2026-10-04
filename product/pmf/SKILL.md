---
name: pmf
description: This skill should be used when the user asks about product-market fit — measuring it, testing it, or diagnosing weak traction — e.g. "do we have PMF", "product-market fit check", "design a Sean Ellis survey", "users sign up but don't stick", "launched but growth is slow", "پروداکت مارکت فیت", "به PMF رسیدیم؟", "محصولم رو ساختم ولی نمی‌فروشه", "چرا کاربرا برنمی‌گردن". Produces a PMF measurement plan or a scored assessment with pivot/persevere recommendation.
version: 1.0.0
---

# PMF Assessment — Measure, Score, Decide

Answer the scariest question honestly: **does anyone need this enough?** Two jobs depending on what exists: design measurement (no data yet) or assess and decide (data exists). The output is a decision aid — strong/weak/no fit, *why*, and what to do about it.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Establish what data exists

Ask the user what they have (don't assume): user counts, retention by cohort, usage frequency, churn, NPS, Sean Ellis survey results, revenue/renewals, qualitative feedback, support logs. Also read `01-discovery/` and "Key facts" for prior signals.

- **Little/no data, or pre-launch** → **Mode A: design measurement.**
- **Real usage data** → **Mode B: assess.**

### 2A. Mode A — Design the measurement plan

Produce `04-pmf/pmf-measurement-plan-YYYY-MM-DD.md` containing:
- **Sean Ellis survey** customized to the product from `references/sean-ellis-survey.md` (translated to the users' language — survey language = customers' language, regardless of report language), with delivery and sampling instructions (who to ask: people who used the product ≥2× recently; minimum n≈30–40).
- **Instrumentation shortlist:** the 3–5 metrics worth tracking *for this business type* (from `references/signal-benchmarks.md`) and how to capture them cheaply.
- **Decision date:** when to come back and run Mode B.

Pre-launch with zero users → say plainly that PMF can't be measured yet and route to `/venture:customers` (problem validation comes first).

### 2B. Mode B — Assess

1. **Score the scorecard** — copy `references/pmf-scorecard.md` to `04-pmf/pmf-scorecard-YYYY-MM-DD.md` and fill the copy, using `references/signal-benchmarks.md` for thresholds *by business type* (B2B SaaS retention ≠ consumer app retention). Every cell: value, benchmark, verdict, confidence. Missing metric → "not measured" (that's signal too).
2. **Read the qualitative texture:** what do the most-retained users have in common (segment, use case)? Sean Ellis "very disappointed" users — who are they? Pull quotes.
3. **Stress-test before verdict — mandatory:** launch the **`venture:devils-advocate`** agent with the draft scorecard + your tentative verdict. Prompt it to attack: data quality, survivorship bias, vanity metrics, segment-mixing, wishful benchmarks. Address every objection in the report (accept, rebut with evidence, or downgrade confidence).
4. **Verdict & diagnosis** in `04-pmf/pmf-assessment-YYYY-MM-DD.md`:
   - **Strong fit** → protect it: identify the fit segment precisely, route to `/venture:gtm` to pour fuel.
   - **Weak/partial fit** → diagnose the gap with this ladder, in order (each step cheaper to fix than the next):
     ① wrong *segment* being acquired → retarget; ② right segment, wrong *value prop/messaging* → reposition; ③ right promise, product *under-delivers* → fix activation/core loop; ④ problem isn't painful enough → pivot territory.
     Recommend the specific experiment to confirm the diagnosis.
   - **No fit** → say it kindly but plainly; recommend pivot directions grounded in any positive signal found (who *did* retain?), or a structured stop. Route to `/venture:review` for the kill/pivot call.

### 3. Close the loop

Update VENTURE.md (Status, key facts: PMF score + verdict + fit segment; riskiest assumptions revised). If verdict is weak/none, mark GTM module `stale` if it exists — scaling plans built on weak PMF are invalid.

## Quality bar

- **Never inflate.** The user's hopes are not data. A kind, evidenced "not yet" saves them months.
- Benchmarks must match business type AND geography reality (emerging-market consumer benchmarks differ; note it).
- Retention curve flattening > any single number. NPS alone is never sufficient evidence.
