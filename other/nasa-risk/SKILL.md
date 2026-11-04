---
name: nasa-risk
description: "Knowledge pack synthesized from NASA Risk Management Handbook, Version 2.0 (November 2024; NASA/SP-20240014019 Part 1, NASA/SP-20240014326 Part 2): RIDM, CRM, and risk leadership. SCOPE LIMITS: single-source (the two November 2024 volumes); domain PRA methods (fault trees, event trees, Bayesian inference) are not this pack, see nasa-pra (NASA/SP-2011-3421); NPR 8000.4, NPD 1000.0, NPR 7120.5, and NPR 8715.3 named, not quoted; reconstructed reference notes, not NASA guidance, and no NASA endorsement."
---

<!-- argument-hint: [topic, process, or chapter number] -->

# NASA Risk Management Handbook, Version 2.0

**Source:** US Government work, public domain (17 U.S.C. 105): NASA Risk Management Handbook, Version 2.0 (November 2024), NASA/SP-20240014019 (Part 1) and NASA/SP-20240014326 (Part 2). Terms and vetting: [LICENSE](LICENSE).

## When to use

Use this skill for questions about NASA risk-informed decision making (RIDM), continuous risk management (CRM), and risk leadership: setting risk posture and tolerances, running an Analysis of Alternatives, writing or reviewing a Risk Management Plan, classifying risks against tolerances, or selecting risk responses. It does not cover domain PRA methods (fault trees, event trees, Bayesian inference); those stay in `nasa-pra`.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to use this skill

- **With no arguments**, read Core Frameworks below.
- **For a topic**, use the Topic Index, then read the linked chapter.
- **For a life-cycle question** (which process at which stage), use the Chapter Index.
- **For a term**, use [glossary.md](glossary.md).
- **For a decision rule** (steps, statement formats, classification logic), use [cheatsheet.md](cheatsheet.md).
- **For a leadership or graded-approach move**, use [patterns.md](patterns.md).

## Core Frameworks & Mental Models

### Objectives-Driven Risk Management (ODRM)

Risk is the potential for shortfalls against explicitly established objectives; objectives flow down from NASA strategic goals through programs, projects, and institutions, and risk postures flow down in tandem. Aggregate risk to each objective, not a list of items, is the thing assessed and judged. Analysis and classification are separate steps: objective distributions first, tolerance comparison second, displays (stoplight, 3x3, 5x5) anchored to markers and tolerances last.

### Risk Leadership

Leaders define and communicate objectives and posture, translate posture into per-objective Risk Tolerance Levels, empower managers inside those limits, and keep risk information flowing up, down, and sideways. Desired outcomes: risk balanced against benefit and opportunity, low process burden, decision velocity. Decision robustness is the standard: enough evidence and uncertainty characterization that the choice is insensitive to credible perturbations.

### RIDM: three parts, six steps

Part 1: identify objectives and performance measures from stakeholder expectations (fundamental-objectives hierarchy, natural/constructed/proxy measures), then identify alternatives (compile broad, prune with a trade tree on feasibility and dominance). Part 2: run one integrated risk analysis per alternative (shared parameters, correlations, U/U margins, graded rigor) and develop the Technical Basis for Deliberation. Part 3: deliberate (risk tolerances, risk-normalized performance targets set sequentially, contenders pared) and select, accepting and documenting the selected alternative's risks in a Risk-Informed Selection Report. Three modes: Activity-Planning, Activity-Rebaseline (exception-driven, inside the selected alternative), Activity-Execution (inside CRM Plan, choosing among risk responses).

### CRM: five steps plus communicate-and-document

Identify (validated risk and opportunity statements, taxonomies, leading indicators), Analyze (RSDs; probabilistic or heuristic paths; IRTL classification; aggregate integration; risk drivers), Plan (six dispositions: Accept, Mitigate, Watch, Research, Elevate, Close; options combined into response alternatives), Track (implementation and effectiveness observables), Control (evaluate tracking, correct or re-plan), with Communicate and Document running through all of it. Burn-down schedules turn posture into milestone commitments; the relational risk database is process memory.

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-introduction-and-scope.md) | Introduction and scope | Purpose, policy alignment (NPR 8000.4, NPD 1000.0), what is new in Version 2.0, roles and reading roadmaps |
| [ch02](chapters/ch02-objectives-driven-framework.md) | Objectives-driven framework | Objectives flow-down, risk types, opportunity, risk leadership steps, posture and RTLs, graded approach, RIDM-CRM integration modes, life-cycle reviews |
| [ch03](chapters/ch03-risk-models-and-posture.md) | Risk models, analysis, and decision concepts | Aggregate risk, triplets, RSDs, U/U risk and leading indicators, hostile-agent scenarios, PMKs, RTLs and coloring, IRTL heuristic, anchored matrices |
| [ch04](chapters/ch04-risk-informed-decision-making.md) | Risk-Informed Decision Making | Six steps, objectives hierarchy, trade trees, integrated analysis, TBfD, deliberation and RPTs, RISR, activity classes and tailoring |
| [ch05](chapters/ch05-continuous-risk-management.md) | Continuous Risk Management | Initialization and RMP inputs, identify/analyze/plan/track/control, six dispositions, burn-down, risk database, communicate-and-document |
| [ch06](chapters/ch06-organizational-integration.md) | Organizational integration | Life-cycle RIDM-CRM continuity, LCR evaluation, cross-cutting risk Types A and B, CORCP/CORHP, RMP contents and coordination |
| [ch07](chapters/ch07-application-examples.md) | Application examples | Process selection, worked Activity-Planning RIDM, worked CRM executions (project and center), probabilistic vs. heuristic |

## Topic Index

- **RIDM (Risk-Informed Decision Making)** → ch04, ch07
- **RIDM steps / Analysis of Alternatives** → ch04
- **CRM (Continuous Risk Management)** → ch05, ch07
- **CRM steps and dispositions** → ch05
- **Risk leadership** → ch01, ch02, ch06
- **Graded approach / activity classes** → ch02, ch04, ch05
- **Risk posture and risk tolerances (RTL, IRTL)** → ch02, ch03, ch07
- **Aggregate risk and aggregation** → ch01, ch02, ch03
- **Performance measures, markers, and constraints** → ch03, ch04
- **Objectives hierarchy / objectives flow-down** → ch02, ch04, ch07
- **Individual risk scenarios / risk statements** → ch03, ch05, ch07
- **U/U risk and leading indicators** → ch03, ch07
- **Security risks (cybersecurity, physical security)** → ch01, ch03
- **Opportunity management** → ch02, ch05, ch07
- **Risk Scenario Diagrams (RSDs)** → ch03, ch05, ch07
- **Risk Management Plan (RMP)** → ch05, ch06
- **Cross-cutting risk and organizational protocols** → ch02, ch06
- **Life-cycle reviews and burn-down** → ch02, ch05, ch06
- **Risk database and communication** → ch05, ch06
- **Risk-Informed Selection Report / TBfD** → ch04, ch07
- **Part 2 examples (process selection, worked RIDM and CRM)** → ch07
- **NPR 8000.4 alignment (named, not quoted)** → ch01, ch02

## Supporting Files

- [glossary.md](glossary.md) — definitions chapter and acronym list of Version 2.0, alphabetical, chapter-tagged.
- [cheatsheet.md](cheatsheet.md) — RIDM six steps, CRM five steps plus communicate-and-document, statement formats, dispositions, classification rules, warning signs.
- [patterns.md](patterns.md) — twelve risk-leadership and graded-approach moves with when/how/trade-offs.

---

## Scope & Limits

Covers NASA Risk Management Handbook Version 2.0 only (both volumes, November 2024), vetted on 2026-10-28; content is reconstructed, synthesized reference notes, not official NASA guidance, with no NASA endorsement. Domain PRA methods (fault trees, event trees, Bayesian inference) are out of scope: use the `nasa-pra` pack (NASA/SP-2011-3421). NPR 8000.4, NPD 1000.0, NPR 7120.5, and NPR 8715.3 are named as the policy the handbook aligns to and are never quoted or rebuilt. The handbook targets NASA programme and project contexts; adapting it to other industries or regulatory regimes is the reader's job.
