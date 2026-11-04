---
name: dod-rio
description: "Knowledge base from the DoD Risk, Issue, and Opportunity (RIO) Management Guide for Defense Acquisition Programs (OUSD R&E, Sep 2023 incl. Change 2.2). Use for the defense-acquisition mechanics of program risk management: the RIO definitions (risk/issue/opportunity), the five-step risk process (plan-identify-analyze-mitigate-monitor), 1-5 likelihood/consequence scoring and the 5x5 risk matrix, the four mitigation options (accept/avoid/transfer/control), burn-down plans, issue management (probability=1), opportunity management toward should-cost, cross-program/interface risk, tailoring RIO to the six AAF acquisition pathways (UCA/MTA/MCA/Software/DBS/Services), specialized methods (RMF, MBCRA/Cyber Table Top, Agile metrics, FMECA, ITRA/DTRAM), and institutionalizing RIO via the PRMP, boards (RMB/JRMB/ROMB/RWG), tools, tiered roles, and WBS/IMP/IMS/EVM/TPM integration. This is the DoD-acquisition complement to nasa-risk (general CRM/RIDM theory) and dau-se-guidebook (the SE process frame). Does NOT teach general risk theory from scratch, and defers specialized risk regimes (system safety/ESOH, HSI, detailed cyber/RMF, spectrum) to their own DoD instructions and the relevant packs."
---

<!-- argument-hint: [RIO definition, five-step process, likelihood/consequence scoring, risk matrix, mitigation option, burn-down, issue, opportunity, cross-program, AAF pathway, RMF/cyber/ITRA, PRMP/board/role, chapter number] -->

# DoD Risk, Issue, and Opportunity (RIO) Management Guide
**Source**: OUSD R&E (US Government work, public domain; Distribution A) | **Chapters**: 8

## When to use
Use this skill to run **program risk, issue, and opportunity management on a U.S. defense acquisition program**: defining and scoring risks, choosing and burning down mitigations, managing realized issues, hunting opportunities toward should-cost, containing cross-program interface risk, tailoring the whole effort to the chosen Adaptive Acquisition Framework (AAF) pathway, layering in specialized risk methods, and institutionalizing it all through the program's plan, boards, tools, roles, and cost/schedule/technical artifacts. This is the DoD-acquisition rendering of risk management — the program-office mechanics that sit on top of the general continuous-risk-management theory in `nasa-risk` and inside the SE process frame in `dau-se-guidebook`.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the three RIO objects, the five-step process, likelihood/consequence scoring and the matrix, the four mitigation options, and the institutional machinery.
- **With a topic** — ask about a scoring rule (consequence = max-of-three, unmitigated), a mitigation option (accept/avoid/transfer/control), a burn-down plan, issue or opportunity management, cross-program tripwires, an AAF pathway (UCA/MTA/MCA/Software/DBS/Services), or a specialized method (RMF, Cyber Table Top, ITRA/DTRAM, FMECA).
- **With a chapter** — `ch02` (identify + analyze + scoring), `ch03` (mitigate/monitor/issues), `ch04` (opportunity + cross-program), `ch05`/`ch06` (RIO by AAF pathway), `ch08` (PRMP/boards/roles/tool integration).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One discipline, three faces, two complements.** Risk, issue, and opportunity are managed as **one family** with a shared register and shared boards. The guide is *guidance, not mandate* — recommended practice for AAF programs, used with DoDI 5000.02, not a mandatory checklist. Read it **with** `nasa-risk` (the general method) and `dau-se-guidebook` (the SE process), which it specializes rather than replaces.

## Core Frameworks & Mental Models

### The three RIO objects (the diagnostic lens)

The guide reduces the whole domain to three diagnostic questions, each a distinct managed object tied to the **cost / schedule / performance** baseline:

- **Risk** — *what can go wrong?* A possible future event/condition that could harm objectives; characterized by **likelihood AND consequence**.
- **Issue** — *what has gone, or will certainly go, wrong?* A realized or near-certain negative event (likelihood = 5 / probability = 1); characterized by **consequence only**.
- **Opportunity** — *what can be improved?* A potential future benefit; the **upside mirror** of risk, the engine for reaching **should-cost** (vs. merely staying inside will-cost).

The central stance: **the worth of risk management comes from a PM who thinks critically and grows a risk-aware culture**, not from satisfying policy. **Plans over process** — the individual mitigation plans (the output) matter more than the machinery; drop any step that doesn't add value, and never "shoot the messenger."

### The five-step risk process

```
Plan → Identify → Analyze → Mitigate → Monitor
       └────────── continuous Communication & Feedback ──────────┘
```
The same steps apply across **every life-cycle phase and every AAF pathway**; only the detail of each action changes. The **PM owns** it (jointly led with the LSE); it is **multidisciplinary** (SE, T&E, EVM, production, QA, logistics) and runs **top-down and bottom-up** at once.

### Scoring: 1–5 ordinal, max-of-three, unmitigated

- **Likelihood** 1–5 against probability bands (Table 2-2); **consequence** 1–5 against tailored criteria (Table 2-1, anchored to the MCA pathway).
- **Consequence = the maximum** of cost/schedule/performance impact — never an average — assessed **as if fully realized with no further mitigation**, using **fully burdened costs**. A **KPP/APB threshold breach forces Level 5**.
- **No fractional scores** (2.4 is invalid). Government and contractor use a **common framework** so disagreements are visible and comparable, not forced into consensus.
- The **5×5 risk matrix** maps likelihood × max-consequence to **Low (green)/Moderate (yellow)/High (red)**. **Risk level ≠ priority** — also weigh cost-effectiveness, time frame, inter-risk relationships, and **EMV/ROI**, but **always rank KPP-threatening risks high**. Model **aggregate** exposure with **Monte Carlo SRA/CRA**.
- The **risk register** (built early) is the single source of truth; risk/issue/opportunity registers may be combined.

### The four mitigation options

Every controlled risk gets **Accept · Avoid · Transfer · Control** (or a hybrid):

| Option | Essence | Watch-out |
|---|---|---|
| **Accept** | Bear it but keep tracking (Watch Item) | Pre-identify resources if realized; acceptance ≠ ignoring |
| **Avoid** | Alternate path / defer / substitute mature tech | Defer only if system would ship without it |
| **Transfer** | Reassign (MOA/MOU) | Hardest; **never fully removes Government exposure** |
| **Control** | Drive likelihood/consequence down | Default; must be **real** reduction, not relabeled baseline work |

A **burn-down plan** (six steps) makes a Control plan trackable: sequence → make objective/measurable → assign planned L/C → date → load into **IMS** → chart level vs. time. Required for all high/moderate and selected low risks. **Meetings don't burn down risk — results do.** Front-load high-**consequence** risks.

### Issues and opportunities (the mirrors)

- **Issue management** mirrors the risk loop but drops the likelihood axis (probability = 1): score consequence, assign an RMB owner, plan a **corrective action / POA&M with an EAC** in the IMS, re-assess for spawned risks. Options are mainly **Ignore** (after a business case) or **Control**.
- **Opportunity management** is the proactive twin: a six-activity loop (plan → identify → analyze [business case] → decide → monitor → feedback), with options **Pursue / Defer / Reevaluate / Reject**. Spending effort **raises** the likelihood of a good event (the inverted lever). Aggregate small wins; reject short-term-gain/long-term-loss candidates.

### Cross-program / interface risk

When a system depends on hardware/software/schedules owned by **other programs**, the **interfaces** are a primary risk source owned by no one. Contain with a **designated technical authority**, **MOAs carrying cost/schedule/performance tripwires**, an **ICWG**, **ICDs/IRSs**, synchronized schedules, an integration plan, and giver–receiver deliverables tracked in the IMS. **Escalate early** up PM → PEO → SAE → DAE; refer requirements disputes to the **CSB**. Reconcile **SWAP-C** across the seam.

### RIO is tailored to the AAF pathway

There is **no single DoD risk process** — the pathway pre-sets the risk posture, and tailoring is fine adjustment:
- **UCA** (<2 yr, DoDI 5000.81) — accepts deficiencies for speed; ends in a disposition analysis.
- **MTA** (2–5 yr, DoDI 5000.80) — fails early and descopes; op demo ≥1 yr before completion.
- **MCA** (milestone-driven, DoDI 5000.85) — front-loads hard decisions, picks the entry milestone by where risk lives, burns down Technology/Engineering/Integration risk in **TMRR** while money is cheap, and gates with **SETRs** (ASR/SRR/SFR/PDR → CDR/TRR/SVR/FCA/PRR → OTRR/IOT&E/PCA) plus TRA/MRA/SRA.
- **Software** (DoDI 5000.87) — automation/continuous-test/cyber **up front**; MVP→MVCR; User Agreement; technical-debt tracking.
- **DBS** (DoDI 5000.75) — fit a commercial product to re-engineered processes via **fit-gap**; ATP gates.
- **Services** (DoDI 5000.74) — **the requirement is the risk**; seven steps, ARRT→PWS/QASP, CPARS.

Contract type follows the risk profile — **risk is never fully transferred to industry** (the Government still needs the product).

### Specialized methods feed the enterprise register

Each is a **sensor** for a risk class the general process won't surface; **funnel each back into one register** with a common consequence language (roll micro-risks up, decompose macro-risks down): **RMF** (DoDI 8510.01; 7 steps; tiered per NIST SP 800-39), **MBCRA / Cyber Table Top** (DoDI 5000.89; mission-framed cyber), **Agile metrics** (Size/Time/Effort/Defects), **FMECA** on the digital model (DoDI 5000.88), **ITRA/DTRAM** (8 risk areas × 7 factors), and **S&T/program protection** (DoDI 5000.83).

### Institutionalization

RIO becomes durable machinery: the **PRMP** (written at formulation, refreshed at life-cycle events); **boards** — PM-chaired **RMB**, **JRMB** for mutual Government–contractor risk, **ROMB** when it also handles opportunities, chartered **RWGs**; an early, SEP-documented **tool** (Project Recon / Active Risk Manager / Risk Exchange); **tiered roles** with the non-negotiable rule that **every risk has an owner**; and **traceability** into **WBS** (MIL-STD-881F), **IMP/IMS**, **EVM** (EIA-748), and **TPMs** (DoDI 5000.02, kept SMART). A mitigation not tied to a funded work package and a schedule activity is **aspiration, not management**.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-dod-rio-foundations.md) | RIO Foundations | Purpose/scope; risk vs. issue vs. opportunity definitions; guidance-not-mandate; PM ownership; plans-over-process; deferred specialized regimes |
| [ch02](chapters/ch02-dod-rio-risk-identification-analysis.md) | Risk: Plan, Identify, Analyze | Five-step process; PRMP/SEP; risk categories (Technical/Programmatic/Business); risk statement; 1–5 scoring; risk matrix; register; EMV; aggregate/Monte Carlo |
| [ch03](chapters/ch03-dod-rio-mitigation-monitoring-issues.md) | Mitigation, Monitoring & Issues | Four options (accept/avoid/transfer/control); six-step burn-down; monitoring against EVM/IMS/TPM; issue management (probability = 1) |
| [ch04](chapters/ch04-dod-rio-opportunity-cross-program.md) | Opportunity & Cross-Program | Opportunity loop and should-cost; opportunity register; RMB/ROMB; interface risk; MOAs/tripwires; ICWG; SWAP-C; escalation chain |
| [ch05](chapters/ch05-dod-rio-aaf-pathways-hardware.md) | RIO by AAF Pathway (UCA/MTA/MCA) | Pathway as pre-set risk dial; MCA entry-by-risk; SETR gates; TRA/MRA/SRA; framing assumptions; contract type; disposition analysis |
| [ch06](chapters/ch06-dod-rio-aaf-pathways-software-services.md) | RIO by AAF Pathway (Software/DBS/Services) | Software pipeline/MVP→MVCR/User Agreement; DBS fit-gap and ATP gates; Services seven steps/ARRT/QASP/CPARS |
| [ch07](chapters/ch07-dod-rio-additional-methods.md) | Additional Methods | RMF (7 steps, NIST 800-39 tiers); MBCRA/Cyber Table Top; Agile metrics (Size/Time/Effort/Defects); Digital Engineering/FMECA; ITRA/DTRAM; S&T protection |
| [ch08](chapters/ch08-dod-rio-process-roles-se-tools.md) | Process, Roles & SE/PM Tools | PRMP outline; RMB/JRMB/ROMB/RWG; Service tools; tiered roles; WBS/IMP/IMS/EVM/TPM integration; SRA/CRA/PRA; DCMA 14-point; UAV-jammer example |

## Topic Index

- **AAF pathways (selecting/tailoring)** → ch05, ch06, cheatsheet
- **Aggregate / compounding risk (Monte Carlo)** → ch02, ch08
- **Burn-down plan / chart** → ch03, ch08, cheatsheet
- **Business / External risk** → ch02
- **Consequence (max-of-three, unmitigated, fully burdened)** → ch02, cheatsheet
- **Contract type as a risk instrument** → ch05, ch08
- **Cross-program / interface risk; MOAs; tripwires; ICWG; SWAP-C** → ch04
- **Cyber Table Top (CTT) / MBCRA** → ch07, ch06
- **DCMA 14-point schedule metrics / schedule health** → ch08
- **Digital Engineering / FMECA** → ch07
- **DTRAM (8 areas × 7 factors) / ITRA** → ch07
- **EMV / ROI prioritization** → ch02
- **Escalation chain (PM→PEO→SAE→DAE) / CSB** → ch04
- **Framing assumptions** → ch05
- **Issue management (probability = 1; Ignore/Control; POA&M/EAC)** → ch03
- **Likelihood (1–5 bands)** → ch02
- **Mitigation options (accept/avoid/transfer/control)** → ch03, cheatsheet
- **Monitoring (EVM/IMS/TPM, trend matrix)** → ch03, ch08
- **Opportunity management / should-cost vs. will-cost** → ch04, cheatsheet
- **PRMP (plan, outline, refresh triggers)** → ch01, ch02, ch08
- **Risk vs. issue vs. opportunity (definitions)** → ch01, cheatsheet
- **Risk categories (Technical/Programmatic/Business)** → ch02
- **Risk matrix (5×5) → Low/Moderate/High** → ch02, cheatsheet
- **Risk register (single source of truth, combined)** → ch02, ch08
- **Risk statement (event+consequence+cause; if–then)** → ch02
- **RMB / JRMB / ROMB / RWG (boards & working groups)** → ch02, ch03, ch08
- **RMF (7 steps; Assess Only; NIST SP 800-39 tiers)** → ch07
- **Roles (Executive/Management/Working; every risk has an owner)** → ch08
- **SETRs (ASR/SRR/SFR/PDR/CDR/TRR/SVR/FCA/PRR/OTRR/PCA)** → ch05
- **Software pathway (MVP→MVCR, User Agreement, technical debt)** → ch06
- **SRA / CRA / PRA (indicators, not verdicts)** → ch08, ch02
- **Tailoring (drop steps that don't add value)** → ch01, ch05
- **Tools (Project Recon / Active Risk Manager / Risk Exchange)** → ch08
- **TRA / MRA (readiness assessments)** → ch05
- **WBS / IMP / IMS / EVM / TPM integration** → ch08

## Supporting Files

- [glossary.md](glossary.md) — RIO terms (boards, scores, pathways, tools, methods), alphabetical, with chapter references
- [patterns.md](patterns.md) — 11 reusable techniques (write a risk statement, score, classify, pick a mitigation, build a burn-down, manage issues/opportunities, contain cross-program risk, tailor to pathway, funnel specialized methods, institutionalize) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the three RIO objects, scoring rules, mitigation/issue/opportunity options, AAF pathway → posture table, specialized-methods table, institutionalization, and tells & smells

---

## Scope & Limits

**Covers**: program risk, issue, and opportunity management for U.S. defense acquisition programs per the DoD RIO Management Guide (Sep 2023, incl. Change 2.2) — the RIO definitions; the tailorable five-step risk process; 1–5 likelihood/consequence scoring, the 5×5 matrix, EMV/ROI, and aggregate Monte Carlo analysis; the four mitigation options and the six-step burn-down; issue management (probability = 1); opportunity management toward should-cost; cross-program/interface risk; RIO tailoring across all six AAF pathways; the specialized methods (RMF, MBCRA/CTT, Agile metrics, DE/FMECA, ITRA/DTRAM, S&T protection) as risk sensors; and institutionalization via the PRMP, boards, tools, tiered roles, and WBS/IMP/IMS/EVM/TPM integration.

**Does not cover in depth** (deferred by the source to its own authorities): general risk theory and continuous-risk-management method built from scratch (use `nasa-risk`); the broader SE process model RIO sits inside (use `dau-se-guidebook`); system safety / ESOH and hazard analysis (DoDI 5000.88, MIL-STD-882 — see `mil-std-882` / system-safety packs); Human Systems Integration (DoDI 5000.95 — see `nasa-hsi`); the full cybersecurity RMF control workflow and SP 800-53 catalog (DoDI 8510.01 / NIST — see `nist-800-37`, `nist-sse`); electromagnetic spectrum/E3 (DoDI 4650.01 / 3222.03); Technology Readiness Assessment depth (see `gao-tra`); and modular-open-systems detail (see `dod-mosa`). It is **guidance, not mandatory policy**, and is thin on worked numeric examples beyond the single Appendix-D UAV-jammer walkthrough.

**Jurisdiction**: U.S. DoD work, public domain (Distribution A — approved for public release, distribution unlimited). Recommended guidance for AAF acquisition programs; used alongside DoDI 5000.02 and Military Department direction.

**Source version**: DoD Risk, Issue, and Opportunity Management Guide for Defense Acquisition Programs, OUSD R&E, September 2023, Incorporating Change 2.2 (December 2023).
