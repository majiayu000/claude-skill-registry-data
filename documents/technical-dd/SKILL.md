---
name: technical-dd
description: "Generate investment-grade Technical Due Diligence reports for The Studio (Utopia Capital). Use this skill whenever the user mentions technical due diligence, TDD, tech DD, technical assessment, technical evaluation of a company, or wants to assess whether a startup's technology works, is well-built, can scale, and what the technical risks are. Also trigger when the user uploads company materials (pitch decks, technical docs, corporate profiles) and asks for a due diligence analysis, technical review, or investment assessment focused on technology. This skill produces branded .docx reports suitable for sharing with co-investors or the company itself. Even if the user just says 'run DD on this company' or 'assess this startup' or 'review these materials', use this skill — it's the standard workflow for technical evaluation at The Studio."
---

# Technical Due Diligence Report Generator

## What This Skill Does

Generates a comprehensive Technical Due Diligence report from uploaded company materials. The output is a professionally formatted, branded .docx document that can be shared with investment committees, co-investors on NRL, or the company itself.

This is a **Technical DD** — it answers: does the tech work, is it well-built, can it scale, what are the technical risks? Commercial and financial DD (unit economics, competitive landscape, valuation, partnerships) is handled separately by the deal team in an Investment Memo.

## Important Context

These reports replace what would typically cost ~$70K from an external TDD provider. The quality bar is high: every claim must be evidence-rated, every risk must be specific (not generic), and the analysis must withstand scrutiny from partners who will poke holes.

---

## Step 1: Gather Inputs

Before generating anything, collect the required context from the user.

### Required Information
Ask the user for these if not already provided:

1. **Company name** and one-line description
2. **Stage and raise**: e.g. "Pre-Series A, raising $2.5M at $22.5M pre-money"
3. **Your relationship to the deal**: lead, co-investor, co-build candidate, advisory
4. **Any specific technical hypotheses or concerns**: e.g. "We think their AI claims are weak" or "We're worried about scalability"

### Required Materials (upload)
At minimum, the user should provide:
- **Pitch Deck** (PDF or slides)
- **Corporate Profile or One-Pager**
- **Any technical documentation**: architecture diagrams, API docs, product demos, sales engineering decks

### Optional but Strongly Encouraged
Prompt the user for these — they significantly improve depth:
- **Sector maps or context documents**: industry primers, market landscapes, competitive intelligence that helps Claude understand the domain deeply
- Technical blog posts, whitepapers, published research from the company
- Previous DD reports or investor memos
- Customer contracts or LOIs
- Patent filings or IP disclosures

### Optional
- Brand assets if not using default Studio branding (logo file, accent color, font)

If the user hasn't provided enough materials, say so explicitly. Don't generate a thin report — tell them what's missing and what it would unlock.

---

## Step 2: Analyze Materials

Before writing, do a thorough pass through all uploaded materials. Build a working mental model of:

1. **What the company claims** — extract every technical claim from marketing materials, pitch deck, and corporate profile
2. **What evidence exists** — match each claim against concrete evidence (architecture diagrams, customer deployments, metrics, third-party validation)
3. **What's missing** — identify critical gaps in the materials provided
4. **Domain context** — if sector maps or context docs were provided, use them to calibrate your assessment against industry norms and competitive reality

This analysis phase is critical. The value of the TDD is in the gap between claims and evidence.

---

## Step 3: Generate the Report

Read `references/report-structure.md` for the detailed section-by-section specification. The report follows this architecture:

### Report Sections

| # | Section | Focus |
|---|---------|-------|
| 1 | Cover Page | Branded cover with company name, report title, date, classification |
| 2 | Technical Summary | Key technical findings, materials disclaimer, critical metrics — no investment recommendation language |
| 3 | Company Overview | Founding, product suite, timeline, customer base — kept brief, context-setting only |
| 4 | Technical Architecture Assessment | Stack with evidence ratings, infrastructure, architecture patterns, deployment model |
| 5 | AI/ML Capabilities Assessment | Deep-dive: real ML vs. rules-based? Model performance? Training data? Drift monitoring? |
| 6 | Code Quality & Engineering Practices | CI/CD, testing, code review, documentation, DevOps maturity |
| 7 | Security & Compliance | Data handling, encryption, certifications, regulatory posture, vulnerability management |
| 8 | Scalability Assessment | Current load, scaling architecture, bottlenecks, cost of scaling |
| 9 | Technical Debt & Maintenance | Legacy systems, upgrade cycles, dependency risks, refactoring needs |
| 10 | Technical Team Assessment | Team composition, depth, gaps (missing CTO?), hiring velocity, capability vs. claims |
| 11 | Technical Moat & IP | Patents, trade secrets, proprietary data, time-to-replicate, defensibility |
| 12 | Roadmap Feasibility | Timeline vs. team vs. funding, execution risk, dependency chains |
| 13 | Technical Risk Register | Critical/High/Medium/Low with specific descriptions — never generic |
| 14 | Evidence Quality Audit | Every major technical claim rated against the evidence hierarchy |
| 15 | What Must Be True | Technical assumptions for the investment thesis, with evidence status and concrete tests |
| 16 | Dispositive Technical Questions | 10-15 questions with GREEN/RED flags to resolve critical unknowns |

### Key Principles

**Evidence hierarchy** — read `references/evidence-framework.md` for the shared framework. Rate every technical claim as SUPPORTED / PARTIAL / CLAIMED / UNSUPPORTED.

**Specificity over generics** — "Competitive vulnerability" is generic. "SITA has 100x resources and already claims full CDM stakeholder coverage" is specific. Name the threat. This applies especially to the Risk Register.

**What Must Be True and Dispositive Questions are always company-specific.** Generate them from the materials — never use a generic template. These sections resolve the specific unknowns surfaced by your analysis, not boilerplate DD questions.

**Intellectual honesty** — if you don't have data, say so. Don't extrapolate. Mark gaps explicitly. The materials disclaimer in the Technical Summary should list exactly what was and wasn't provided.

**Tone**: direct, analytical, investor-grade. No hedging ("it could potentially be argued..."). Acknowledge genuine strengths before flagging weaknesses — accurate assessment, not prosecution.

---

## Step 4: Format as .docx

Read `references/formatting-guide.md` for the full formatting specification. Read `assets/utopia-branding.md` for default branding.

Use the docx skill (`/mnt/skills/public/docx/SKILL.md`) to generate the final document. Key formatting requirements:

- Branded cover page with The Studio logo and company name
- Headers: "CONFIDENTIAL | [Company] Technical DD | [Date]"
- Footers: "The Studio — Utopia Capital | Page X"
- Tables with branded header rows (accent color)
- Callout boxes with colored left borders for critical findings
- Alternating row shading for readability
- Page breaks between major sections
- Evidence ratings color-coded in tables (green for SUPPORTED, amber for PARTIAL, orange for CLAIMED, red for UNSUPPORTED)

---

## Step 5: Review and Iterate

After delivering the first draft, tell the user:
- Which sections are thinnest due to limited materials
- What additional inputs would strengthen specific sections
- Offer to deepen any section they want to push on

If the user provides additional materials or context, regenerate the affected sections — don't start from scratch.

---

## What This Skill Does NOT Cover

These are separate workstreams. If relevant, flag in the report that they're needed:

- **Commercial DD**: unit economics, competitive landscape, valuation, partnership economics — this goes in the Investment Memo (separate skill)
- **Legal DD**: contracts, IP assignments, corporate governance
- **Financial model auditing**: revenue projections, burn rate scenarios
- **Background checks** on founders
- **Customer reference calls** (though the TDD should specify which calls to make)
- **Hands-on code review or security audit** (though the TDD flags when these are needed and what to look for)
