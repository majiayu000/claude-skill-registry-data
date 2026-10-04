---
name: model
description: This skill should be used when the user asks about business models, unit economics, lean canvas, pricing math, CAC/LTV, break-even, or financial projections — e.g. "build a lean canvas", "calculate unit economics", "does the math work", "CAC LTV payback", "revenue projection", "مدل کسب‌وکار", "اقتصاد واحد", "بیزینس مدل", "حساب کن این بیزینس می‌صرفه یا نه", "پیش‌بینی درآمد". Produces a lean canvas, unit economics workbook, and scenario projections in the venture workspace.
version: 1.0.0
---

# Business Model — Lean Canvas & Unit Economics

Answer "how does this make money, and does the math survive contact with reality?" Two artifacts: the **Lean Canvas** (the whole model on one page) and the **unit economics workbook** (per-customer math + scenarios). All arithmetic shown, every input sourced or flagged as assumption.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Gather inputs — reuse before asking

Mine the workspace first: pricing & competitor price range (03-competitors, 05-gtm), market size & segment (02-market), willingness-to-pay evidence (01-discovery), churn/retention (04-pmf). Then ask the user only for what's missing: actual costs, current price, real CAC if any spend happened, capacity constraints (service businesses). Label every input: `measured / sourced / assumption`.

### 2. Lean Canvas

Copy `references/lean-canvas.md` to `06-model/lean-canvas-YYYY-MM-DD.md` and fill the copy — pull problem/segment from discovery, UVP from positioning if GTM ran, revenue/cost lines from this module's math. Canvas cells cite their source module. Unknowns stay visibly `TBD` (a canvas full of guesses presented as facts is worse than gaps).

### 3. Unit economics — the heart

Follow `references/unit-economics-guide.md` formulas. Compute per business type: ARPU, gross margin, CAC (per channel where possible), LTV (use a churn-based method, show it), **LTV:CAC**, **CAC payback months**, contribution margin per unit, break-even (customers and months). 

- Show every formula inline with its inputs: `LTV = 40 × 0.7 / 0.05 = $560` — re-derivable by the reader.
- **Scenario table — mandatory:** pessimistic / base / optimistic, varying the 2–3 weakest assumptions (usually churn, CAC, price). State which scenario the venture survives.
- **Sensitivity line:** the one variable that moves the result most → that's the number to validate next in the real world.

### 4. Projection (18 months, simple)

Monthly table: new customers (from GTM channel targets if set; otherwise a stated growth assumption), churned, active, MRR/revenue, costs (fixed + variable), net, cumulative cash. State the cash low-point and month of break-even — or "does not break even in 18mo under base case", plainly. Currency: local + hard-currency column when inflation is material (e.g. Iran — note inflation assumption explicitly).

For non-trivial math, write and run a small Python script in `06-model/` (so re-runs with new inputs are one command) and include its output table in the report.

### 5. Verdict & close

`06-model/business-model-YYYY-MM-DD.md` ends with: **does the model work?** (LTV:CAC ≥ 3 and payback ≤ 12mo as healthy defaults — adjust per type), what must be true for base case, the kill number ("if churn > X%, this never works"). Update VENTURE.md (status, key facts: LTV:CAC, payback, break-even month, kill number; new assumptions → riskiest list). Suggest next: weak economics from price → `/venture:gtm` pricing section; from churn → `/venture:pmf`; healthy → `/venture:review` or execute.

## Quality bar

- An assumption presented as a fact is the cardinal sin here — label and confidence-rate every input.
- Optimistic defaults are banned: early-stage churn is high, CAC rises with scale, conversion is worse than hoped. Base case must feel slightly uncomfortable.
- If the model only works in the optimistic scenario, the verdict is "doesn't work yet" — say it.
