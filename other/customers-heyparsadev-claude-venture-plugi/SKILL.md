---
name: customers
description: This skill should be used when the user wants customer discovery work — interview guides, problem validation, personas, jobs-to-be-done, or synthesizing interview/survey feedback — e.g. "make a customer interview guide", "how do I validate this problem", "build personas", "analyze my interview notes", "synthesize user feedback", "گاید مصاحبه با مشتری", "اعتبارسنجی مشکل", "پرسونا بساز", "مصاحبه‌هام رو تحلیل کن", "با مشتری چی بپرسم". Produces interview guides, ICP hypotheses, and evidence-ranked synthesis in the venture workspace.
version: 1.0.0
---

# Customer Discovery — Interviews, Personas, Synthesis

The cheapest way to avoid building something nobody wants: talk to people *correctly* and read the evidence honestly. Two jobs: **prepare** (guides, ICP hypothesis, who to talk to) and **synthesize** (turn raw notes into ranked, quoted insights).

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Mode A — Prepare (before/while talking to people)

### 1. ICP hypothesis

From VENTURE.md + riskiest assumptions, draft: who exactly has this problem worst (segment + situational trigger), where to find 10 of them this week (specific: which Telegram groups, associations, LinkedIn filters, physical locations), and what would disqualify someone as a target. Save as `01-discovery/icp-hypothesis-YYYY-MM-DD.md`.

### 2. Interview guide — Mom Test rules enforced

Build from `references/interview-guide-template.md` + `references/mom-test-rules.md`. Non-negotiables:
- Questions about **their life, past behavior and current workarounds** — never about your idea or hypotheticals ("would you use/pay...?" is banned).
- Target the riskiest assumptions from VENTURE.md — each assumption maps to ≥1 question.
- **Interview language = customers' language.** Write the guide in it (Persian guide for Iranian customers), regardless of report language.
- Include: intro script, 8–12 core questions with follow-up probes, closing asks (referral to 2 more people; permission to follow up), and a per-interview note template (so notes arrive synthesizable).

Save as `01-discovery/interview-guide-YYYY-MM-DD.md`. Coach briefly: 15–20 min per interview, record or note verbatim quotes, aim for 10–15 interviews before synthesizing, log each note file into `01-discovery/interviews/`.

## Mode B — Synthesize (notes/survey data exist)

### 1. Ingest

Read everything in `01-discovery/interviews/` (+ any survey exports, support logs, review dumps the user points to). Note n and how participants were sourced — selection bias goes in the report.

### 2. Extract & rank

Follow `references/synthesis-template.md`:
- **Pains** ranked by `frequency × severity` — severity shown by *behavior* (paying for workarounds, spending hours, past attempts to solve), not politeness. Verbatim quotes attached (anonymized: "P4, clinic owner").
- **Current solutions & what they cost** (money/time) — this is willingness-to-pay evidence.
- **Segments that emerged** (who feels it worst — often ≠ the ICP hypothesis; say so when it diverges).
- **Personas / JTBD:** only as many as the data supports (usually 1–2 from 10–15 interviews). Format: "When <situation>, I want <motivation>, so I can <outcome>" + hire/fire criteria for solutions.
- **Disconfirming evidence — mandatory section:** who *didn't* care, which assumptions cracked. If everyone loved everything, suspect the questions (or the sample) and say so.

### 3. Verdict on assumptions

For each riskiest assumption in VENTURE.md: `validated / refuted / still unknown` + the evidence line. Update VENTURE.md accordingly (check off, revise, or add new ones discovered).

Save as `01-discovery/synthesis-YYYY-MM-DD.md` in `report_language` (quotes stay bilingual: original + translation).

## Close the loop

Update VENTURE.md (status, key facts: top pain + quote, emergent segment, willingness-to-pay evidence). Suggest next: assumptions validated → `/venture:market-research` (size it) or `/venture:model`; refuted → reframe with `/venture:start`; product live → feed into `/venture:pmf`.

## Quality bar

- Compliments are not data. "I'd definitely use this" without past-behavior evidence = polite rejection — count it as nothing.
- n and sampling method appear in every synthesis; 5 friendly interviews ≠ validation, and the report says so.
- Insights without verbatim quotes don't ship.
