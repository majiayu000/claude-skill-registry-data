---
name: nasa-system-safety
description: "Knowledge base from NASA System Safety Handbook Volume 2 (NASA/SP-2014-612). Use for risk-informed safety cases (RISC), integrated safety analysis (ISA), adequate safety concepts, safety objectives and requirements, acquirer/provider roles, graded safety analysis, claims-evidence-argument structure, SSMP development, and RISC evaluation. Does not cover nuclear or chemical safety domains, occupational health regulations, or NASA-specific programmatic requirements beyond system safety."
---

<!-- argument-hint: [topic, process, chapter number, or keyword such as RISC / ISA / ASARP / SCI / graded approach] -->

# NASA System Safety Handbook Volume 2 (NASA/SP-2014-612)
**Source**: NASA Office of Safety and Mission Assurance (US Government work, public domain) | **Chapters**: 7

## When to use
Use this skill when working on safety cases, system safety analysis, risk-informed decision making, or safety requirements for aerospace or safety-critical engineering programmes. It is the primary reference for structuring a RISC, scoping an ISA, setting safety thresholds and goals, understanding Acquirer/Provider roles, or evaluating an existing safety case. This skill covers the NASA implementation of the safety case paradigm; it is applicable to other safety-critical domains by analogy but is grounded in NASA aerospace practice.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about RISC development, ISA scoping, ASARP, SCI designation, safety thresholds, assurance deficits, graded approach, SSMP content, or RISC evaluation; I read the relevant chapter.
- **With a chapter** — ask for `ch01` through `ch07`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### 1. The Two-Principle Framework for Adequate Safety
A system is adequately safe if and only if it **simultaneously**:
1. **Meets or exceeds the minimum tolerable level of safety performance** — a probabilistic floor set by the Acquirer, expressed as a maximum acceptable total loss probability (threshold for first operations; goal for mature operations).
2. **Is ASARP** — further safety improvement would require intolerable sacrifice in cost, schedule, or technical performance.

Both conditions must hold throughout all life-cycle phases. Meeting the minimum alone is insufficient; ASARP without meeting the minimum is insufficient.

### 2. The Acquirer / Provider Split
| Role | Responsibility | Primary Output |
|---|---|---|
| **Acquirer** | Safety assurance: set requirements, evaluate RISC, accept safety risk | Safety requirements; RISC Evaluation Report; risk acceptance decision |
| **Provider** | Safety ensurance: achieve adequate safety through design/operation; build the RISC | SSMP; ISA; RISC Report |

When a Provider sub-tasks another organisation, the Provider becomes Acquirer for that sub-relationship.

### 3. The Risk-Informed Safety Case (RISC) Structure
```
Top Claim: System is adequately safe
  └── Intermediate Claim 1 (meets minimum tolerable level)
        └── Intermediate Claim 1.1
              ├── Base Claim A  [Direct Evidence + Supporting Evidence → Assurance Deficit Score 1-5]
              └── Base Claim B  [Direct Evidence + Supporting Evidence → Assurance Deficit Score 1-5]
  └── Intermediate Claim 2 (system is ASARP)
        └── Base Claim C  [...]
```
- **Direct evidence**: quantitative (PRA results, failure rates, test data, anomaly rates, best-practice adherence).
- **Supporting evidence**: qualitative (personnel qualifications, V&V of tools, documentation quality, safety culture, external review quality).
- **Assurance deficit score**: 1 (very low deficit, ~95–100% confidence) → 5 (very high deficit, ~0–35% confidence). Set by Acquirer based on mission criticality.

### 4. Safety Performance Margin and Requirement Derivation
```
Safety Threshold (total loss probability including UU risks)
  - Safety Performance Margin (estimated from historical SPF)
  = Analytic Requirement for Known Risks (what the ISA/PRA must demonstrate)

Safety Performance Factor (SPF) = Total actual loss prob ÷ Known-risk modelled loss prob
  (derived from historical programmes; values of ~5 have been observed for early development)

Initial analytic requirement = Safety Threshold ÷ SPF
Mature analytic requirement  = Safety Goal ÷ SPF_mature
  (trajectory follows exponential burndown over ~125 flights)
```

### 5. Graded ISA / RISC Approach
| Project Priority | Trigger | Required Analysis |
|---|---|---|
| Priority 1 | Human spaceflight; White House approval; planetary protection; strategic; >$1B | Full PRA + qualitative system safety analysis |
| Priority 2 | $250M–$1B life-cycle cost | Qualitative analysis + PRA where appropriate |
| Priority 3 | <$250M life-cycle cost | Qualitative analysis only |

Apply finer-grained grading within any mission: highest-criticality scenarios → deepest analysis.

### 6. The Three-Phase Staged RISC Evaluation
1. **Acceptance Review** — completeness and protocol compliance check; gate before substantive review.
2. **Qualitative Scope/Methods Review (Surveying)** — methods, coverage, ASARP, evidentiary strength; Evaluator forms independent view.
3. **Quantitative Evaluation (Auditing)** — spot-check calculations, sensitivity studies, simplified independent models for critical claims.

Output: **RISC Evaluation Report** with summary and detailed findings; overall rating of Acceptable or Unacceptable.

### 7. Assurance Deficit → CRM Integration
Assurance deficits identified in the RISC convert directly into CRM risk statements (per NPR 8000.4A) with assigned owners, tracked under the same Continuous Risk Management process as all other programme risks. The RISC and CRM process are the same management loop, not parallel activities.

### 8. Key Decision Rules
- RISC is **not** the basis for the risk acceptance decision — it informs the decision but does not bind the decision maker.
- Safety requirement tailoring is mandatory, not optional — blanket levy of all historical requirements without ASARP review is explicitly identified as sub-optimal.
- SCI designation must be top-down from ISA, not bottom-up from FMEA only — management practices, interfaces, and organisational factors are SCIs.
- Confirmation bias is the primary threat to RISC validity — the RISC must include both failure scenario analysis (deductive) and safety argument (inductive).

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-introduction.md) | Introduction | Volume 2 scope; 5 rationales; 8 principal themes; RISC as organising concept; graded approach; UU risk primacy |
| [ch02](chapters/ch02-key-concepts.md) | Key Concepts | Adequate safety two-principle framework; Acquirer/Provider roles; safety assurance vs ensurance; safety threshold/goal; ASARP; RISC definition; UU risk taxonomy |
| [ch03](chapters/ch03-system-safety-framework-overview.md) | System Safety Framework Overview | Four-element framework; ISA as central engine; SCI designation; allocated/derived requirements; tailoring; Acquirer-Provider interaction tables; life-cycle perspective |
| [ch04](chapters/ch04-safety-objectives-requirements.md) | Safety Objectives and Requirements (Acquirer) | Safety performance margin derivation; SPF; KMO sub-cases; burndown profile; deterministic requirements; ASARP tailoring; verification procedures; SSRA |
| [ch05](chapters/ch05-system-safety-ensurance-activities.md) | System Safety Ensurance (Provider) | SSMP (42-element); graded ISA (Priority 1/2/3); M&S CAS; assurance deficit management; SCI top-down identification; ASARP trade analysis; precursor analysis |
| [ch06](chapters/ch06-risc-development.md) | RISC Development (Provider) | Claims tree structure; intermediate/base claims; direct/supporting evidence; assurance deficit scoring; GSN; graded RISC approach; RISC Report structure; living document lifecycle |
| [ch07](chapters/ch07-risc-evaluation.md) | RISC Evaluation (Acquirer) | Staged evaluation (acceptance/surveying/auditing); Evaluation Team independence; assurance deficit × importance matrix; confidence aggregation methods; VOI analysis; RISC Evaluation Report |

## Topic Index
- **Adequate safety / adequately safe** → ch02, ch03
- **ASARP** → ch02, ch03, ch04, ch05
- **Assurance deficits** → ch05, ch06, ch07
- **Claims tree / claims-evidence-argument** → ch06, ch07
- **Confirmation bias** → ch02, ch06
- **Continuous Risk Management (CRM)** → ch05, ch07
- **Graded approach** → ch01, ch05, ch06
- **Integrated Safety Analysis (ISA)** → ch03, ch05
- **Key Decision Points (KDPs)** → ch02, ch03
- **Key Mission Objectives (KMOs)** → ch04
- **Minimum tolerable safety level / safety threshold / safety goal** → ch02, ch03, ch04
- **RISC development** → ch06
- **RISC evaluation** → ch07
- **RISC Report** → ch06
- **Safety-Critical Items (SCIs)** → ch03, ch05
- **Safety performance margin / SPF** → ch03, ch04
- **SSMP (System Safety Management Plan)** → ch05
- **SSRA (System Safety Requirements Analysis)** → ch03, ch04, ch05
- **UU risks (unknown/underappreciated)** → ch02, ch03, ch04
- **Value-of-Information (VOI)** → ch07
- **Verification procedures** → ch04

## Supporting Files
- [glossary.md](glossary.md) — ~50 defined terms with chapter references, alphabetical order.
- [patterns.md](patterns.md) — 13 reusable patterns with When-to-use, How, and Trade-offs sections.
- [cheatsheet.md](cheatsheet.md) — Decision rules, quick-reference RISC component table, and tells-and-smells for common failure modes.

---

## Scope & Limits
This knowledge pack covers the full content of NASA/SP-2014-612 (Volume 2), which provides implementation guidance for systems engineering-integrated system safety at NASA: objectives/requirements, integrated safety analysis, RISC development, and RISC evaluation. It does not cover: Volume 1 conceptual foundations in depth; domain-specific standards (nuclear, chemical, occupational health); NASA-specific programmatic requirements not related to system safety; or non-aerospace applications (though the RISC framework is applicable by analogy). All content is US Government work in the public domain; no licence restrictions apply.
