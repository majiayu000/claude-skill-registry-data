---
name: nasa-ms-7009
description: "Knowledge base from NASA-STD-7009B (Standard for Models and Simulations) with implementation depth from NASA-HDBK-7009B. Use for M&S criticality and programmatics, development evidence and capability assessment, verification/validation domains, uncertainty and sensitivity, use-phase results assessment, risk-informed decision reporting, and handbook life-cycle products. Covers STD-7009B (2024-03-05) + HDBK-7009B (2026-02-03) synthesized notes only; does not replace program-specific TA direction, NPR 7150.2 software requirements detail, or full PRA methodology."
---

<!-- argument-hint: [topic, facet, or chapter number] -->

# NASA Standard for Models and Simulations (7009B + Handbook)
**Source**: NASA-STD-7009B (2024-03-05) with NASA-HDBK-7009B (2026-02-03) (US Government work, public domain) | **Chapters**: 7

## When to use
Reach for this pack when establishing or reviewing credibility of models and simulations that inform NASA (or NASA-like) critical decisions — criticality/intended use, M&S life-cycle planning, development pedigree and permissible uses, V&V domains, uncertainty/sensitivity, use-phase appropriateness, results assessment, and decision-maker reporting with mandatory warnings and risk acceptance.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about criticality, capability assessment, V&V domains, uncertainty, permissible use, results reporting, or handbook phases.
- **With a chapter** — ask for `ch01` through `ch07`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Two-document stack
- **STD-7009B**: Mandatory M&S requirements (shalls) across programmatics, development, and use/reporting.
- **HDBK-7009B**: Implementation handbook — life-cycle phases, compliance interpretation, model/AI pedigree context, PM/Technical Authority roles.

### Three-phase requirement spine
1. **Programmatics** — intended use, criticality, plan, metrics, acceptance criteria, reviews, defects.
2. **Development** — RWS/pedigree, CM of data/software, units, assumptions, math, limits, permissible uses, capability assessment, guidance; plus V&V and development uncertainty.
3. **Use and reporting** — proposed use, appropriateness, inputs, setup, envelope control, messages, results assessment, risk, decision reporting.

### Dual credibility assessments
| Assessment | Primary phase | Role |
|------------|---------------|------|
| M&S capability | Development / release | How strong is the M&S product? |
| M&S results | Use / analysis | How credible is this analysis outcome? |

### Use chain
Intended use → (develop) permissible uses + V&V domains → (operate) proposed use + appropriateness assessment.

### Reporting control
Decision briefings carry warnings, uncertainty+method, assessment outcomes vs thresholds, reviews, qualifications, records, and risk-acceptance rationale — not plots alone.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-ms-scope-criticality-programmatics.md) | Scope, Criticality, Programmatics | Intended use, criticality, plan, metrics, acceptance, reviews, defects |
| [ch02](chapters/ch02-ms-development-evidence-capability.md) | Development Evidence and Capability | Pedigree, assumptions, limits, permissible uses, capability assessment, guidance |
| [ch03](chapters/ch03-ms-verification-validation.md) | Verification and Validation | Verify/validate shalls and domains of V&V |
| [ch04](chapters/ch04-ms-uncertainty-sensitivity.md) | Uncertainty and Sensitivity | Referent/model/use uncertainty; sensitivity records |
| [ch05](chapters/ch05-ms-use-results-assessment.md) | Use and Results Assessment | Proposed use, inputs, setup, envelope, messages, results assessment |
| [ch06](chapters/ch06-ms-risk-and-decision-reporting.md) | Risk and Decision Reporting | Analysis risk, mandatory warnings, report contents, acceptance |
| [ch07](chapters/ch07-hdbk-lifecycle-implementation.md) | Handbook Life-Cycle Depth | Phases, compliance, pedigree/AI, 7150.2 link, TA roles |

## Topic Index
- **Acceptance criteria / thresholds** → ch01, ch06
- **AI / ML models as M&S** → ch02, ch07
- **Assumptions and abstractions** → ch02, ch06
- **Capability assessment** → ch02, ch06, ch07
- **Criticality assessment** → ch01
- **Decision-maker warnings** → ch06
- **Defect / problem tracking** → ch01, ch06
- **Domain of validation** → ch03, ch05
- **Domain of verification** → ch03, ch05
- **Input pedigree** → ch05
- **Intended use** → ch01
- **Life-cycle phases (handbook)** → ch07
- **Permissible uses** → ch02, ch05
- **Proposed use / appropriateness** → ch05
- **Results assessment** → ch05, ch06
- **Risk acceptance for M&S analysis** → ch06
- **Sensitivity analysis** → ch04, ch05
- **Technical Authority / PM roles** → ch01, ch07
- **Uncertainty characterization** → ch04, ch06
- **Units and coordinate frames** → ch02
- **Verification** → ch03
- **Validation** → ch03

## Supporting Files
- [glossary.md](glossary.md) — M&S credibility terms with chapter references
- [patterns.md](patterns.md) — implementation patterns (When/How/Trade-offs)
- [cheatsheet.md](cheatsheet.md) — spine, report must-haves, tells and smells

---

## Scope & Limits
This pack covers NASA-STD-7009B (approved 2024-03-05) together with NASA-HDBK-7009B (2026-02-03) as synthesized reference notes from a two-PDF extraction (metadata pages 88 + 175 = **263** source_pages). It does **not** reproduce the full requirements compliance matrix verbatim, replace delegated Technical Authority direction, fully detail NPR 7150.2 software engineering requirements, or teach end-to-end probabilistic risk assessment methods (see nasa-pra / nasa-risk). US Government public domain work. No source-material download link is published.
