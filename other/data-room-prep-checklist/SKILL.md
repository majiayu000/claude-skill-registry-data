---
name: data-room-prep-checklist
description: "Generate a stage-specific data room checklist, folder structure, and investor gap list from your round context. Use when preparing for due diligence or getting investor-ready. Triggers: 'data room checklist', 'prepare data room', 'чек-лист дата рума', 'подготовка data room'."
version: 1.0.0
---

# Data Room Prep Checklist

This skill generates a targeted due-diligence preparation package for founders raising a pre-seed, seed, or Series A round. Provide your round stage and business model — receive a prioritized checklist, a recommended folder structure, and a gap list of what's likely missing and what investors will ask next. No CRM or integrations required; works entirely from pasted context.

**Input:**
- Round stage (pre-seed / seed / Series A / Series B+)
- Business model type (SaaS / marketplace / hardware / services / other)
- Optional: investor type (VC / angel / strategic / family office); pasted existing data room contents

**Output:**
- Single markdown document with three sections: Due Diligence Checklist, Recommended Folder Structure, Gap List

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Parse Round Context

1. Check if the message contains any business context (company description, product, industry, stage, model, or funding goal). If the message contains ONLY a trigger phrase with no additional context whatsoever, respond immediately: "Укажи стадию раунда и тип бизнеса, чтобы я собрал адресный чек-лист. / Share your round stage and business model so I can generate a targeted checklist." Do not proceed to generate a checklist.

2. Read the user's message for round stage and business model:
   - Accepted stages: pre-seed, seed, Series A, Series B+
   - Accepted models: SaaS, marketplace, hardware / deep-tech, services, e-commerce, other
   - If stage is missing: default to seed-level checklist; prepend bilingual note: "Stage not specified — using seed-level defaults. / Стадия не указана — используется шаблон seed."
   - If business model is missing: default to SaaS; prepend note: "Business model not specified — using SaaS defaults."

2. Check for optional context:
   - **Investor type** (VC / angel / strategic / family office) — adjusts checklist formality and item set
   - **Pasted existing data room contents** — triggers delta mode (see Step 2b)

### Step 2: Generate Due Diligence Checklist

1. Build a 6-category checklist tailored to stage and model. Assign each item one priority label:
   - **[Must-have]** — deal-breaker if absent; investor will pause DD without it
   - **[Expected]** — investor will ask; have it ready before formal due diligence starts
   - **[Nice-to-have]** — accelerates process; may not be required at early stages

   **Categories:**

   - **Legal & Corporate:** Certificate of Incorporation, cap table (fully diluted), shareholders agreement, IP assignment agreements (all founders), option pool / ESOP schedule, board consent resolutions for equity grants, regulatory licenses (if applicable)
   - **Financials:** 3-year financial model (P&L, cash flow, balance sheet), MRR/ARR monthly breakdown (last 12 months), bank statements (last 3–6 months), burn rate and runway summary, audited or CPA-reviewed financials (Series A+)
   - **Product & Technology:** Product demo or screenshots, technical architecture overview, IP ownership confirmations, security practices summary
   - **Team:** Founder bios / LinkedIn profiles, org chart, employment agreements, equity vesting schedules
   - **Commercial & GTM:** Customer list (anonymized is fine), signed contracts or LOIs, pipeline summary, key metrics dashboard (churn, NPS, CAC/LTV, activation rate)
   - **Cap Table & Funding History:** Fully diluted cap table with post-money projection, SAFE / convertible note summary if applicable, prior round terms, option pool breakdown

2. Adjust depth and items by stage:
   - **Pre-seed:** lighter legal (incorporation + IP assignments focus), no audited financials, team section critical, 6–12 month runway model
   - **Seed:** full legal foundation, 12–18 month financial model, 2–3 reference customers, signed customer contracts
   - **Series A:** CPA-reviewed or audited financials, trailing-12-month cohort data, board consent resolutions, full cap table
   - **Series B+:** expand financials (audited), ARR bridge, cohort retention table, complete legal diligence package

3. Adjust for investor type:
   - **Angel / family office:** lighter legal formality; heavier weight on team section and vision
   - **Strategic:** add partnership terms, IP licensing section, integration roadmap document
   - **VC:** full standard package per stage

**Step 2b — Delta mode (if user pasts existing contents):**
- Compare pasted list against the generated checklist
- Produce a delta summary:
  - ✓ Covered
  - ✗ Missing
  - ⚠ Partial (exists but may be incomplete, e.g., "cap table present but may not include latest options")

### Step 3: Generate Recommended Folder Structure

1. Produce an indented hierarchy of top-level and sub-folders (6 main folders matching checklist categories)
2. Adjust for business model: hardware/deep-tech adds `/IP & Patents` and `/Manufacturing & Regulatory`
3. Format as a fenced code block — copy-paste ready for Google Drive, Notion, Dropbox, or similar

### Step 4: Generate Gap List

1. **"What you're likely missing"** — list 3–5 items commonly absent at the stated stage:
   - Pre-seed: signed co-founder agreements, IP assignments from all founders, corporate formation docs
   - Seed: board consent resolutions for prior equity grants, reference customer list with contact info, signed NDA template for DD
   - Series A: audited or CPA-reviewed financials, trailing-12-month cohort data, fully diluted cap table with post-money projection

2. **"What the investor will ask next"** — list 2–4 predictable follow-up questions:
   - "Show me monthly MRR for the last 12 (or 24) months"
   - "Who are your 3 reference customers and can we speak with them?"
   - "What's your current burn and runway?"
   - "Do you have signed IP assignments from all founders?"

3. Close with a **Next step** line: one concrete first action for the founder.

### Step 5: Format Output

1. Assemble all three sections into a single markdown document
2. Open with a header that summarizes the round context used (stage, model, investor type)
3. If a checklist sub-category has no relevant items (e.g., manufacturing on a pure SaaS company), omit it with a note: "(Not applicable for [model])"
4. Translate all section headers, priority labels, and checklist items into the user's language; folder structure stays in Latin characters regardless of language

---

## Output Format

```markdown
# Data Room Checklist — [Stage] Round · [Business Model]
> For: [investor type] | [bilingual stage-note if defaulted]

---

## Due Diligence Checklist

### Legal & Corporate
- [ ] **[Must-have]** Certificate of Incorporation / Articles of Association
- [ ] **[Must-have]** Cap table (fully diluted, current)
- [ ] **[Expected]** Shareholders agreement
- [ ] **[Expected]** IP assignment agreements (all founders)
- [ ] **[Nice-to-have]** Option pool / ESOP schedule

### Financials
- [ ] **[Must-have]** 3-year financial model (P&L, cash flow, balance sheet)
- [ ] **[Must-have]** MRR/ARR breakdown — last 12 months (monthly)
- [ ] **[Expected]** Bank statements — last 3–6 months
- [ ] **[Expected]** Burn rate and runway summary (current)
- [ ] **[Nice-to-have]** CPA-reviewed or audited financials

[... remaining categories ...]

---

## Recommended Folder Structure

```
/Data Room — [Company Name] — [Round]
  /01 Legal & Corporate
    /Incorporation Documents
    /Shareholder Agreements
    /IP Assignments
    /Option Pool & ESOP
  /02 Financials
    /Historical P&L
    /Financial Model
    /Bank Statements
  /03 Product & Technology
  /04 Team
  /05 Commercial
  /06 Cap Table & Funding History
```

---

## Gap List

### What You're Likely Missing ([Stage])
1. [Item 1 — e.g., "Signed IP assignment agreements from all founders"]
2. [Item 2 — e.g., "Board consent resolutions for prior equity grants"]
3. [Item 3 — e.g., "Reference customer list with contact permission"]

### What the Investor Will Ask Next
1. [Question 1 — e.g., "Show me monthly MRR for the last 12 months"]
2. [Question 2 — e.g., "Who are your 3 reference customers?"]

---

**Next step:** [Concrete first action — e.g., "Send this folder structure to your lawyer and confirm all legal documents are countersigned originals, not drafts."]
```

**Russian output** uses Russian section headers:
- Чек-лист due diligence → Юридическое и корпоративное / Финансы / Продукт и технологии / Команда / Коммерческое и GTM / Кэп-тейбл и история привлечений
- Priority labels: **[Должен быть]** / **[Ожидается]** / **[Желательно]**
- Folder path names remain in Latin characters (standard practice in Russian startups)

---

## Edge Cases

1. **Stage not specified:** Default to seed-level; prepend bilingual note (see Step 1)
2. **Hardware / deep-tech:** Add categories: IP Portfolio & Patents, Manufacturing Agreements, Regulatory Approvals (CE / FCC / FDA); note at top: "Hardware due diligence includes additional IP and regulatory items."
3. **Existing data room pasted by user:** Activate delta mode (Step 2b); output ✓/✗/⚠ comparison
4. **Non-VC investor (angel / family office / strategic):** Adjust item set and formality per investor type (Step 2, point 3)
5. **Series B+ stage:** Expand financials section; add audited statements, ARR bridge, cohort retention table; prepend note: "Series B+ requires deeper financial disclosure — additional items added."

---

## Negative Cases

- **Empty input — no stage, no context:** Respond: "Укажи стадию раунда и тип бизнеса, чтобы я собрал адресный чек-лист. / Share your round stage and business model so I can generate a targeted checklist."
- **User asks to review a term sheet or analyze legal documents (investor/reviewer side):** Respond: "Этот скилл помогает основателю подготовить data room, но не анализирует юридические документы. Для правового анализа обратись к юристу. / This skill helps founders prepare a data room, not review legal terms. Consult a lawyer for legal analysis."
- **User asks to evaluate investors or write a pitch deck:** Respond: "Этот скилл создаёт чек-лист документов для due diligence, а не оценивает инвесторов и не пишет питч. / This skill prepares due-diligence documents — not investor evaluation or pitch writing."
