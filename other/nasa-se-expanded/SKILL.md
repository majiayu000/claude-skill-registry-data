---
name: nasa-se-expanded
description: "Knowledge base from the Expanded Guidance for NASA Systems Engineering (NASA/SP-2016-6105-SUPPL, Volume 1, March 2016) — the practitioner-depth supplement to the NASA SE Handbook. Use for the load-bearing mechanics the handbook compresses: the SE Engine's per-phase cadence and the iterative-vs-recursive distinction, the AS9100 crosswalk, life-cycle tailoring vs. customization and the Compliance Matrix, the recursive system-design consistency loop (ConOps vs. Operations Concept, requirement flow/type/ownership, successive refinement), product realization (verify/qualify/accept/certify cardinality, protoflight, 'test the way we fly' coverage, two-form transition), and the crosscutting technical-management procedures (six-step scheduling, cost-estimating method selection, JCL, interface document family, RIDM/CRM, CM baselines, EVM arithmetic, MOE/MOP/KPP/TPM, the three required leading indicators, and the decision-analysis method catalog). This is the DEPTH layer — it deliberately does NOT restate the base definitions; pair it with the nasa-se-handbook pack. Scope: NASA space-flight SE practice (Vol 1 Practices); thin on the Vol 2 process-appendix detail, on non-NASA/commercial life cycles, and on software-engineering methodology."
---

<!-- argument-hint: [SE engine, tailoring/customization, ConOps, requirements ownership, verification/validation/qualification/certification, integration, transition, scheduling, cost estimating, JCL, interface (IRD/ICD/IDD), risk (RIDM/CRM), CM baselines, EVM, MOE/MOP/KPP/TPM, leading indicators, decision analysis, AHP/Borda/MAUT, or a chapter number] -->

# Expanded Guidance for NASA Systems Engineering (NASA/SP-2016-6105-SUPPL, Vol 1, March 2016)
**Source**: NASA — US Government work, public domain | **Chapters**: 6 | **Role**: depth supplement to `nasa-se-handbook`

## When to use
Use this skill when you need practitioner-depth mechanics that the NASA SE Handbook compresses into brief statements. It is the right pack for questions about the SE Engine's per-phase cadence and the iterative-vs-recursive distinction, life-cycle tailoring vs. customization and the Compliance Matrix, the recursive system-design consistency loop (ConOps vs. Operations Concept, requirement flow/type/ownership, successive refinement), product realization cardinality (verify/qualify/accept/certify, protoflight, end-to-end coverage), and crosscutting technical-management procedures such as six-step scheduling, cost-estimating method selection, the JCL scatterplot, the interface document family (IRD/ICD/IDD), RIDM/CRM, CM baselines, EVM arithmetic, the MOE/MOP/KPP/TPM hierarchy, required leading indicators, and the decision-analysis method catalog. Pair it with the nasa-se-handbook pack, which supplies the base survey-level definitions this supplement assumes.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
This pack is the **expanded-guidance depth layer** over the base `nasa-se-handbook`. It assumes you already know the standard definitions (the 17 processes, ConOps, MOEs, the V&V split, PBS/WBS, the risk triplet) and instead supplies the *operating mechanics* — the procedures, the cardinality patterns, the decision trees, and the named pitfalls the handbook compresses to a sentence. For survey-level orientation, read the handbook pack first; come here for "how does this actually run, and what goes wrong."

- **Without arguments** — load the core frameworks below for the SE Engine cadence, the tailoring machinery, the system-design loop, the realization cardinality clocks, and the crosscutting-management toolkit.
- **With a topic** — ask about a specific mechanic: "iterative vs. recursive", "tailoring vs. customization", "ConOps vs. Operations Concept", "verify/qualify/accept/certify", "protoflight", "six-step scheduling", "JCL scatterplot", "IRD vs. ICD vs. IDD", "RIDM vs. CRM", "the four CM baselines", "EVM SPI/CPI", "MOE/MOP/KPP/TPM", "the three required leading indicators", "AHP vs. Borda vs. MAUT".
- **With a chapter** — ask for `ch01` (SE engine fundamentals), `ch02` (life cycle & tailoring), `ch03` (system design processes), `ch04` (product realization), `ch05` (planning/requirements/interface/risk management), `ch06` (CM/data/assessment/decision analysis).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The SE Engine read correctly (NPR 7123.1)
The 17 processes sit in three sets — **system design** (4), **product realization** (5), **technical management** (8). The load-bearing reading the handbook blurs: processes **10–17 are crosscutting *tools*** for executing 1–9, not the next sequential steps. The engine is a **template you stamp onto every product** in the hierarchy — each tier "resets to process 1" and runs its own full pass with stakeholders inherited from above. Re-run cadence is specific: development processes (1–9) fire **five engine cycles** (Pre-Phase A → D); management processes (10–17) fire **seven** (Pre-Phase A → F). **Phases C and D are split** so design (left side) runs in C and realization (right side) in D. **Implementation fires only at the bottom tier**; every higher pass is **Integration**, and integration-level V&V is non-negotiable because parts passing does not imply the whole passes.

### Iterative vs. recursive (precise defined terms)
**Iterate** = re-run a process on the **same** product to fix a discrepancy. **Recurse** = re-apply the processes to design the **next lower** layer, realize the **next upper** layer, or advance a **life-cycle phase**. Iterate to *fix*; recurse to *descend, ascend, or advance*. The **SE/PP&C overlap** is structural: the systems engineer supplies technical truth and cost/schedule *realism*; Project Planning & Control imposes programmatic constraints. The **AS9100 crosswalk** (Table 2.1-1) maps the 17 processes onto the aerospace quality standard — the bridge for any AS9100-certified Center or contractor.

### The life cycle as a tailoring substrate
The phases/KDPs are a **scaffold right-sized per project**, not a fixed pipeline. **Tailoring** seeks relief from a "shall" (consistent with objectives, allowable risk, constraints) and produces **deviations/waivers** logged in the **Compliance Matrix** (Appendix H.1/OCE for Center-wide, H.2/Center Director for program/project). **Customization** reshapes *how* you meet a requirement and needs **no** waiver. Anchor relief in a risk class (NPR 8705.4) and the eight tailoring characteristics; check the governing PM directive (7120.5/.7/.8, 7150.2) separately. The **SE Product Maturity table** is a Preliminary→Baseline→Update ratchet; `**` cells mark required products per review. The **budget cycle (PPBE)** is a planned *disturbance* — an implicit fiscal gate often slipping past Oct 1 into a continuing resolution — not an SE process.

### The recursive system-design loop
The four design processes are **one consistency clamp**, not a pipeline: a strawman architecture, its ConOps, and the derived requirements are forced into mutual agreement and validated against three questions (works as expected? achievable in budget/schedule? delivers the funded functionality?). Stop refining a branch when it would convince an independent review team the design is feasible — a **resolution** criterion. Distinguish **ConOps** (early, technical-team) from **Operations Concept** (later, flight/ground reasonableness). Route every requirement by **flow, type, and ownership** — programmatic requirements (and waivers) belong to the program/project; technical requirements to the Technical Authority. **Successive refinement**: each turn's allocated/derived requirements become the next level's high-level requirements. Space-asset protection is **survivability engineering** (threat × susceptibility = vulnerability), not security paperwork.

### Product realization — the cardinality clocks
Verification = "built right" (traces to requirements). Validation = "right thing built" (traces to the ConOps). Keep them apart, then exploit overlap where one rig answers both. Sort by clock: **verify / qualify / certify once per design; accept once per unit** — and **certification is an audit of evidence, not a test**. **Protoflight** qualifies on the flight unit itself (reduced margin) instead of dedicated qual hardware. **"Test the way we fly"** is a coverage discipline: prioritized fault-space without combinatorial blowup, skeleton-first with stubs/simulators, a **fresh-eyes operator**, regression after every fix, an authenticated environment, external-interface scope. **Integration engineers interactions, not assemblies** (mechanical/fluid/thermal/electrical/data/logical/human flows), from concept through de-integration. **Transition has two forms** — up (to the next integration level) or out (to the operational user) — and drives packaging, handling, storage, training, and enabling-product handoff. Reused-product **pedigree does not transfer**.

### Crosscutting technical management — the procedures
**Planning** reconciles the team's bottom-up estimate against the project's top-down allocation; build network schedules in **six steps** (negotiate external dependencies, write every basis of estimate, integrate to find the project critical path, resource-level, reserve float). Match **cost-estimating method to maturity** (parametric → analogous → grassroots); read the **JCL** off a cost-vs-schedule Monte Carlo scatterplot (required at KDP C above $250M). **50–70% of life-cycle cost is committed at architecture selection, ~90% by preliminary design.** Assess every requirement change with three tools (performance margins, evaluators list, risk/threats list). **Interface documents**: IRD ("shall", bilateral) → ICD (design solution) or IDD (one-sided), wrapped by an ICP, changed via PIRN/IRN. **Risk = RIDM + CRM**, built from initiating events. **CM**: four baselines map one-to-one to gates (**Functional→SDR, Allocated→PDR, Product→CDR, As-Deployed→ORR**) and rides on **SAE/EIA-649-2** (5 functions, 37 principles); CM needs a CR+CCB, **Technical Data Management** needs only managed change authority. **EVM** measures "the system that produces the system" — earned value (BCWP) is the pivot; planned-vs-actual is spending only. Keep the **MOE/MOP/KPP/TPM** hierarchy straight (customer vs. supplier viewpoint), report the **three required leading indicators** (mass margin, power margin, RFA/RID/action-item burndown) for maturity *and* stability, and pick decision-analysis tools from the catalog (trade studies, cost-benefit, influence diagrams, decision trees, **AHP**, **Borda counting**, **utility/MAUT**) scaling rigour to consequence.

---

## Chapter Index

| # | Section (source) | Key content |
|---|---|---|
| [ch01](chapters/ch01-nasa-se-expanded-fundamentals-and-se-engine.md) | Fundamentals & SE Engine (§2.0–2.3) | SE as a way of thinking (Rechtin/two-cultures lineage); SE Engine as three sets with 10–17 as crosscutting tools; the SE/PP&C overlap; iterative vs. recursive (precise defined terms); per-phase engine cadence (5 / 7 cycles, C/D split); AS9100 crosswalk; PBS & tracking icon; the STS worked example read as engineering-judgment |
| [ch02](chapters/ch02-nasa-se-expanded-life-cycle-and-tailoring.md) | Life Cycle & Tailoring (§3.0–3.11) | Formulation/Implementation phases, KDPs & liens; governing-document routing (7120.5/.7/.8, 7150.2); SE Product Maturity ratchet; tailoring vs. customization; the Compliance Matrix (H.1/H.2); risk-class anchor (8705.4); Type A–F scaling; ABC; descope options; SEMP baseline timing; the PPBE budget cycle as a planned disturbance |
| [ch03](chapters/ch03-nasa-se-expanded-system-design-processes.md) | System Design Processes (§4.1–4.4) | The recursive consistency loop; ConOps vs. Operations Concept; survivability model (threat × susceptibility = vulnerability) & the PPP; requirement flow/type/ownership & metadata; standards order of authority; FFBD/N²/TLA; doctrine of successive refinement; objective function & trade space; KDRs; threshold vs. baseline; deterministic vs. risk-informed safety; specialty-engineering integration |
| [ch04](chapters/ch04-nasa-se-expanded-product-realization.md) | Product Realization (§5.1–5.5) | Verify/qualify/accept/certify cardinality (once-per-design vs. once-per-unit); certification-as-audit; protoflight; "test the way we fly" coverage mechanics; integration as the engineering of interactions; de-integration & disposal; discrepancy triage; reused-product pedigree; M&S validation failure modes; two-form transition & site survey; enabling-product handoff |
| [ch05](chapters/ch05-nasa-se-expanded-crosscutting-planning-requirements-interface-risk.md) | Planning / Requirements / Interface / Risk Mgmt (§6.1–6.4) | Technical Planning Strategy & team skill-mix; six-step network schedule; workflow-diagram formats; cost-estimating method selection; life-cycle-cost integration & double-counting trap; JCL scatterplot; WBS failure modes & EVM work/planning packages; the 50–70–90 cost lock-in; requirements change-impact toolset; interface document family & IWG; risk scenario/initiating-event structure; RIDM↔CRM |
| [ch06](chapters/ch06-nasa-se-expanded-crosscutting-cm-data-assessment-decision.md) | CM / Data / Assessment / Decision Analysis (§6.5–6.8) | SAE/EIA-649-2 (5 functions, 37 principles); the four baselines→review gates; CCB & change classification; CSA; CM-vs-DM governance line; SBU & ITAR data protection; the technical review system & SRB; EVM arithmetic (BCWS/BCWP/ACWP, SPI/CPI, EAC/VAC); MOE/MOP/KPP/TPM hierarchy; the three required leading indicators; decision-analysis method catalog (AHP, Borda, MAUT) |

## Topic Index

- **SE Engine / 17 processes / crosscutting tools** → ch01
- **Iterative vs. recursive** → ch01
- **SE and Project Planning Control overlap (PP&C)** → ch01
- **AS9100 crosswalk** → ch01
- **Product Breakdown Structure (PBS)** → ch01, ch05
- **Phase cadence / engine cycles / C-D split** → ch01
- **Life cycle phases / Formulation and Implementation** → ch02
- **Key Decision Point (KDP) / liens** → ch02, ch06
- **Tailoring vs. customization** → ch02
- **Compliance Matrix** → ch02
- **Agency Baseline Commitment (ABC) / descope options** → ch02
- **SEMP baseline timing** → ch02, ch05
- **Budget cycle / PPBE** → ch02
- **Recursive system design loop / consistency clamp** → ch03
- **Concept of Operations vs Operations Concept** → ch03
- **Survivability / threat susceptibility vulnerability** → ch03
- **Requirement flow, type, and ownership** → ch03
- **Standards order of authority** → ch03
- **Functional analysis FFBD N2 timeline** → ch03
- **Successive refinement / objective function / trade space** → ch03
- **Key Driving Requirement (KDR)** → ch03
- **Threshold vs baseline performance** → ch03
- **Deterministic vs risk-informed safety requirement** → ch03
- **Product realization / right side of the engine** → ch04
- **Verification qualification acceptance certification cardinality** → ch04
- **Protoflight** → ch04
- **Test the way we fly / end-to-end coverage** → ch04
- **Integration as engineering of interactions** → ch04
- **De-integration / disposal** → ch04
- **Discrepancy triage** → ch04
- **Reused product pedigree / heritage** → ch03, ch04
- **Two-form product transition / site survey** → ch04
- **Technical planning strategy / team skill mix** → ch05
- **Six-step network schedule** → ch05
- **Cost estimating method selection (parametric analogous grassroots)** → ch05
- **Joint Confidence Level (JCL)** → ch05
- **WBS failure modes / work and planning packages** → ch05
- **50-70-90 cost lock-in** → ch05
- **Requirements change-impact toolset** → ch05
- **Interface documents IRD ICD IDD ICP** → ch05
- **Risk scenario / initiating event** → ch05
- **RIDM and CRM** → ch05
- **Configuration Management baselines / SAE EIA 649** → ch06
- **Configuration Control Board (CCB) / change classification** → ch06
- **Configuration Status Accounting (CSA)** → ch06
- **CM versus Technical Data Management** → ch06
- **SBU and ITAR data protection** → ch06
- **Technical review system / Standing Review Board (SRB)** → ch06
- **Earned Value Management arithmetic (BCWP SPI CPI)** → ch06
- **MOE MOP KPP TPM hierarchy** → ch06
- **Three required leading indicators (mass power margin burndown)** → ch06
- **Decision analysis method catalog (AHP Borda MAUT trade studies)** → ch06

## Supporting Files

- [glossary.md](glossary.md) — key expanded-guidance terms (engine, tailoring/customization, baselines, V&V cardinality, EVM, MOE/MOP/KPP/TPM, RIDM/CRM, interface documents, decision-analysis methods), alphabetical, with chapter references.
- [patterns.md](patterns.md) — 14 practitioner patterns (stamp-the-engine, iterate-vs-recurse, tailor-vs-customize, the consistency clamp, requirement routing, hold-V&V-apart, engineer-interactions, the coverage discipline, six-step scheduling, method-to-maturity estimating, change-impact assessment, RIDM+CRM, leading indicators, decision-board scoping), each with When / How / Trade-offs.
- [cheatsheet.md](cheatsheet.md) — decision rules, the engine/review/baseline tables, EVM arithmetic, the technical-measure hierarchy, the interface-document picker, the decision-analysis method menu, and tells & smells.

---

## Scope & Limits

**Covers**: the practitioner-depth supplement to the NASA SE process — the SE Engine's structure and per-phase cadence, the iterative/recursive distinction, the AS9100 crosswalk; life-cycle tailoring vs. customization and the Compliance Matrix governance; the recursive system-design consistency loop (ConOps/Operations-Concept, requirement flow/type/ownership, successive refinement, survivability engineering); product realization (verify/qualify/accept/certify cardinality, protoflight, end-to-end coverage, two-form transition); and the eight crosscutting technical-management processes' operating procedures (six-step scheduling, cost-estimating method selection, JCL, WBS/EVM, interface document family, RIDM/CRM, CM baselines and standards, EVM arithmetic, the MOE/MOP/KPP/TPM hierarchy, the three required leading indicators, and the decision-analysis method catalog).

**Does not cover (by design — it is the depth layer)**: the base survey-level definitions and process input/activity/output tables — those live in the **`nasa-se-handbook`** pack, which this supplement assumes and deliberately does not restate. **Read the two packs together.**

**Thin or absent**: the Volume 2 detailed process-appendix material (entrance/exit criteria checklists, full templates, worked appendices) — this pack is built from **Volume 1 (Systems Engineering Practices)**; the binding "shall" statements (they live in **NPR 7123.1**, with program/project management requirements in **NPR 7120.5/.7/.8** and software in **NPR 7150.2** — this is *guidance*, not the NPR); detailed cost-model construction and contracting/FAR detail; software-engineering methodology; and **non-NASA, commercial, or non-space-flight life cycles** (the framing is NASA space-flight practice). For the wider SE canon and ISO/IEC/IEEE 15288 lineage see the `sebok` pack.

**Source version**: NASA/SP-2016-6105-SUPPL (March 2016), *Expanded Guidance for NASA Systems Engineering* — **Volume 1**, subtitled *Systems Engineering Practices* (~383 source pages). A NASA work in the US Government public domain.
