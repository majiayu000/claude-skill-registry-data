---
name: market-research
description: This skill should be used when the user asks for market research, market sizing, TAM/SAM/SOM, market trends, industry analysis, or market segmentation — e.g. "how big is this market", "do market research for my idea", "size the market", "industry trends for X", "مارکت ریسرچ کن", "بازار این محصول چقدره", "تحقیق بازار", "تحلیل بازار", "سایز بازار رو دربیار". Produces a cited, confidence-rated market research report in the venture workspace.
version: 1.0.0
---

# Market Research — Sizing, Trends & Segments

Produce decision-grade market research: how big is the opportunity, how is it changing, which segment to enter first. Numbers must be **traceable** (cited) and **honest** (confidence-rated) — a wrong TAM quietly poisons every later module.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Scope (with the user, briefly)

From VENTURE.md + one quick exchange, pin down:
- **Market definition** — the job being done, not the product category ("appointment no-show reduction for clinics", not "SaaS").
- **Geography** — local market vs global changes sources and method entirely.
- **Mode** — `quick` (~10 min scan: top-line size, 3–5 trends, segment list) or `deep` (full report). Default: quick for `idea` stage, deep otherwise. State which mode you're running.

### 2. Research

Consult `references/data-sources.md` for where to look and `references/sizing-guide.md` for method. Core rules:

- **Local markets → local language.** For Iran search in Persian (آمار, گزارش بازار, مرکز آمار ایران, cafebazaar/digikala data); for Turkey in Turkish; etc. English-only search badly undercounts local markets.
- **Triangulate:** any number that matters needs ≥2 independent sources, or gets `confidence: low` explicitly.
- **Recency:** prefer data ≤2 years old; note the year next to every figure.

**Quick mode:** run 5–10 targeted WebSearch/WebFetch rounds inline yourself.

**Deep mode:** decompose into 3–5 research questions (e.g. ① market size & growth, ② segments & buyer behavior, ③ trends/drivers/regulation, ④ analogous markets & benchmarks) and fan out **`venture:market-researcher` agents in parallel — one question each, single message, multiple Agent calls**. In each agent prompt include: the venture one-liner, market definition, geography, the specific question, and expected output format (findings + citations + confidence). Synthesize results yourself afterward.

### 3. Size the market — both directions, show the math

Follow `references/sizing-guide.md`:
- **Top-down:** industry reports → TAM → filter to SAM → realistic share → SOM.
- **Bottom-up (more credible, always include):** (number of target customers) × (reachable %) × (realistic price). Build each factor from cited data.
- The two methods will disagree — **explain why**, present a range, and state which number you'd bet on.
- Every formula appears in the report with its inputs, so the user (or their client) can re-derive it.

### 4. Write the report

Fill a copy of `references/report-template.md`, saved as `ventures/<slug>/02-market/market-research-YYYY-MM-DD.md` (quick mode → `market-scan-YYYY-MM-DD.md`, abbreviated sections). Write in `report_language`. Re-runs create a new dated file — never overwrite history.

### 5. Close the loop

- Update VENTURE.md: Status row → `done YYYY-MM-DD`; append ≤10 key facts (SOM range, growth rate, top trend, chosen entry segment...); add new risky assumptions discovered.
- Suggest next: usually `/venture:competitors` (the sizing surfaced who's competing) or `/venture:customers` if buyer behavior data was thin.

## Quality bar

- A skeptical investor should find zero unsourced numbers.
- "No reliable data found — proxy used: X (low confidence)" is a *good* sentence; an invented number is a firing offense.
- Recommend an **entry segment** explicitly — research that ends without a "so what" is decoration.
