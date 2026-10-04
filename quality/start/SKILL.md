---
name: start
description: This skill should be used when the user wants the business suite dashboard, guidance on where to start or what to do next — e.g. "/venture:start", "business dashboard", "what's the next step for my venture", "how do I use the venture suite", "از کجا شروع کنم", "داشبورد بیزینسم رو نشون بده", "قدم بعدی چیه", "راهنمای استفاده", "وضعیت ونچرهام". Acts as the orchestrator and living manual for all venture modules.
version: 1.0.0
---

# Biz Start — Dashboard, Router & Living Manual

The front door of the venture suite. Show where every venture stands, recommend the next move, and teach the suite interactively. Keep it conversational — short dashboard first, detail on demand. **Never dump the full manual unprompted.**

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Workflow

### 1. Scan

Read every `ventures/*/VENTURE.md` (only these files — not whole folders). No `ventures/` directory or empty → skip to step 4 (first-time welcome).

### 2. Dashboard

Show a compact table in the user's language:

| Venture | Stage | Done | Stale/open | Suggested next step |
|---|---|---|---|---|

- "Done" = modules with `done` status; "Stale" = stale modules or unchecked riskiest assumptions.
- Flag ventures untouched for 30+ days.
- One venture only → skip the table, give a short narrative status instead.

### 3. Route

Recommend the next module per venture using stage + status + open assumptions:

1. Riskiest assumptions unvalidated & no discovery done → `/venture:customers`
2. No market sizing → `/venture:market-research` (quick mode for `idea` stage, deep otherwise)
3. Market done, competitors missing → `/venture:competitors`
4. Stage `launched`+ and no PMF check → `/venture:pmf`
5. PMF weak → `/venture:customers` + `/venture:pmf` gap diagnosis (do NOT push GTM scaling on weak PMF)
6. PMF strong / stage `building`+ → `/venture:gtm`, then `/venture:model`
7. Everything done or 3+ modules done → `/venture:review` (board-style check)

Ask which venture/module to run, then proceed as that module instructs.

### 4. First-time welcome (no ventures yet)

Briefly (in the user's language): the suite tracks each idea/business/client as a *venture* folder; modules write reports into it and build on each other. Then ask where they are and route:

| "Where are you?" | Route |
|---|---|
| فقط یه ایده دارم / just an idea | `/venture:new-venture` → then customers + quick market research |
| با مشتری‌ها حرف زدم، می‌خوام جدی بررسی کنم / validated interest | new-venture → deep market research + competitors |
| دارم می‌سازم / building | new-venture → competitors + business model |
| لانچ کردم ولی رشد کنده / launched, slow growth | new-venture → **pmf first** (diagnose before pushing growth) |
| می‌خوام برای کلاینت گزارش آماده کنم / client deliverable | new-venture (type: client) → whichever module matches the deliverable |

### 5. Manual on demand

If asked "how does X work / این چیکار می‌کنه":

| Module | One-liner | Example prompt (fa) |
|---|---|---|
| `/venture:new-venture` | register a venture, create workspace | «یه ایده جدید دارم: ...» |
| `/venture:market-research` | TAM/SAM/SOM sizing, trends, segments | «بازار این محصول چقدره؟» |
| `/venture:competitors` | competitor matrix, SWOT, battlecards | «رقبای این محصول رو تحلیل کن» |
| `/venture:customers` | Mom Test interviews, personas, synthesis | «گاید مصاحبه با مشتری بساز» |
| `/venture:pmf` | Sean Ellis test, PMF scorecard, pivot/persevere | «ببین به PMF رسیدیم یا نه» |
| `/venture:gtm` | positioning, channels, pricing, launch plan | «استراتژی ورود به بازار بچین» |
| `/venture:model` | Lean Canvas, CAC/LTV, projections | «اقتصاد واحد این بیزینس رو حساب کن» |
| `/venture:review` | board-style review of everything, kill/pivot/persevere | «کل ونچر رو بی‌رحمانه نقد کن» |

Recommended journey: **customers → market-research → competitors → model → gtm → (launch) → pmf → review** — but modules run standalone in any order; each warns when a prerequisite would sharpen its output.

For the full Persian manual, read and summarize relevant sections of `${CLAUDE_PLUGIN_ROOT}/PLAYBOOK.fa.md` (point the user to it for self-reading too).

## Rules

- This module never produces analysis itself — it routes. Don't half-run market research here; hand off to the module.
- Recommendations must come from VENTURE.md state, not generic advice. Quote the user's own open assumptions back at them when routing.
- Sequencing discipline: discovery/validation before scaling moves. Push back (kindly) when a user with weak validation asks to jump to GTM.
