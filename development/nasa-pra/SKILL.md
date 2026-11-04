---
name: nasa-pra
description: "Knowledge base from the NASA Probabilistic Risk Assessment Procedures Guide (NASA/SP-2011-3421, 2nd ed.). Use for quantitative PRA of aerospace and safety-critical systems: the risk triplet and scenario logic stack (MLD, ESD, event trees, fault trees, minimal cut sets), Bayesian data collection and parameter estimation, aleatory/epistemic uncertainty modeling and common-cause failure (Alpha Factor, beta-factor, CCBE), human reliability analysis (THERP, CREAM, NARA, SPAR-H), context-based software risk (CSRM), physics-based and structural/phenomenological models (stress-strength, limit states, FORM/SORM, NASGRO, range safety), uncertainty propagation and importance measures (F-V, RAW, Birnbaum, DIM), and launch-abort modeling with worked PRA examples. This is the QUANTITATIVE engine beneath NASA's risk doctrine — for the qualitative RIDM/CRM decision framework use the nasa-risk pack. Thin on programme management, organisational risk governance, and non-aerospace regulatory contexts; aerospace-focused and anchored to the 2011 second edition."
---

<!-- argument-hint: [topic, method, or chapter number] -->

# NASA PRA Procedures Guide (NASA/SP-2011-3421, 2nd ed.)
**Source**: NASA (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill when you need to conduct or review quantitative Probabilistic Risk Assessment (PRA) of aerospace and safety-critical systems using the NASA PRA Procedures Guide (NASA/SP-2011-3421, 2nd ed.). It covers the risk triplet and scenario logic stack (MLD, ESD, event trees, fault trees, and minimal cut sets), Bayesian data collection and parameter estimation, aleatory and epistemic uncertainty modeling, common-cause failure treatment (Alpha Factor and beta-factor models), human reliability analysis methods (THERP, CREAM, NARA, and SPAR-H), context-based software risk modeling (CSRM), physics-based limit-state and structural models, and uncertainty propagation with importance measures. Use it when building or auditing a NASA-standard PRA model, when selecting HRA methods, or when quantifying launch-abort risk scenarios. For the qualitative RIDM and CRM decision framework, use the nasa-risk pack instead.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below; they are the working toolkit, not a summary.
- **With a topic** — ask about fault trees, Bayesian updating, common-cause failure, human error probabilities, software risk, stress-strength models, uncertainty propagation, importance measures, or launch abort; the relevant chapter is read on demand.
- **With a chapter** — ask for `ch03` (data + Bayesian estimation) or `ch08` (launch abort + worked examples).
- **Supporting files** — `glossary.md` (terms), `patterns.md` (named techniques with trade-offs), `cheatsheet.md` (selection tables, tells & smells).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## Core Frameworks & Mental Models

### The Risk Triplet (Kaplan & Garrick)
PRA represents risk as a set of triplets — **scenario, likelihood, consequence** — answering *what can go wrong, how likely is it, what are the consequences*, each with uncertainty made explicit. A single expected-value summary is rejected because prevention requires understanding the *elements* of each adverse scenario. A scenario's frequency is the initiating-event frequency times the conditional probability of reaching its end state.

### The Scenario Logic Stack
Risk is decomposed through a chain of graphical Boolean models:
- **Master Logic Diagram (MLD)** — deductively generates a comprehensive initiating-event list (terminating at *pinch points*), supported by FMEA reasoning.
- **Event Sequence Diagram (ESD)** — inductive, success-oriented flowchart, one per initiator, mapping paths to end states; communication-friendly, built first.
- **Event Tree (ET)** — the quantitative tree whose mutually exclusive paths are scenarios; the conventional "down" branch is failure.
- **Fault Tree (FT)** — deductive decomposition of a top event (the Boolean *complement* of a system success criterion) through AND/OR gates to basic events. Shared basic events across pivotal-event fault trees are how conditional dependencies are captured.
- **Minimal Cut Sets (MCSs)** — the irreducible joint-failure combinations; the target of Boolean reduction and the basis for quantification. Prevent every MCS, and prevent each MCS by defeating any one member.

### Two Layers of Uncertainty
**Aleatory** = irreducible stochastic variability of observables (the "model of the world"). **Epistemic** = reducible limit of knowledge about parameters and assumptions. They are kept separate. Epistemic uncertainty is moved by **Bayesian updating** (prior + likelihood → posterior) and propagated to the risk metric, typically by sampling. Results are a *fan of percentile curves*, not a single line — the width of the fan is the epistemic uncertainty.

### Bayesian Estimation as the Default Engine
Parameters (failure rates, demand probabilities, initiator frequencies, HEPs, software conditional probabilities) are estimated by fitting a prior and updating with evidence through a likelihood matched to the data-generating process: **Poisson** for time-based counts, **Binomial** for demand-based counts, **lognormal** for handbook/expert values. **Conjugate pairs** (Gamma–Poisson, Beta–Binomial) give closed-form posteriors; mismatches need numerical or MCMC solutions. Sequential updates compound (today's posterior is tomorrow's prior) and are order-independent.

### Dependence: Common-Cause Failure
Ignoring positive dependence underestimates risk. A CCF needs a **root cause** plus a **coupling factor** (shared design, hardware, function, people, procedures, location, environment). Treatment is two-phase: conservative qualitative + quantitative screening, then detailed analysis with **common-cause basic events (CCBEs)** expanded into the fault trees and parameters from the recommended **Alpha Factor** model (beta-factor and Basic Parameter are simpler precursors). The trick is to make the dependence an explicit basic event, after which ordinary independent-event math applies.

### Humans and Software as First-Class Contributors
**HRA** turns human-system interactions into basic events with **human error probabilities** and uncertainty bounds, via a five-step process and method selection (THERP, CREAM, NARA, SPAR-H; time-critical actions via a Time Response Curve). **Software risk is design risk** — compliant code responding wrongly to an unanticipated condition. The **Context-based Software Risk Model (CSRM)** splits software failure into unconditional/routine (failure-rate-quantifiable) and conditional/triggered (failure-on-demand-quantifiable) contributions, marks each recoverable or critical, and risk-informs testing.

### Physics-Governed Branch Points
Many branch outcomes are set by physics, not random failures. The unifying device is the **stress-strength formulation**: the probability that capability exceeds demand, both random variables, via a **limit-state function** (failure when g ≤ 0). Solve analytically for normal/lognormal cases, otherwise by Monte Carlo / LHS / AIS / FORM / SORM / AMV. Range-safety models (inert debris, blast, ray-focusing, plume) translate accidents into public consequence, judged by **Casualty Expectation** against EWR 127-1.

### Results, Importance, and the Safety Case
Uncertainty is propagated (LHS preferred over crude Monte Carlo) with a convergence procedure. **Importance measures** rank what drives the risk: F-V/RRW (where improvement pays off), Birnbaum (sensitivity), RAW (worst-case failure), DIM (parameters, additive). Because complex-system risk cannot be *proven*, credibility rests on completeness, scrutability, peer review, and a **Risk-Informed Safety Case** of evidence plus operating commitments.

### The Graded Approach
Match modeling depth to the stakes and life-cycle phase. Start parametric and coarse with honest uncertainty ranges; add fidelity only where existing models become insufficient or where uncertainty exposes a risk-driving design weakness. A coarse model with honest uncertainty beats a detailed one built on placeholder data.

## Chapter Index

| # | Title | Key content |
|---|---|---|
| [ch01](chapters/ch01-nasa-pra-foundations-risk-management-and-pra-framework.md) | Foundations — Risk Management and the PRA Framework | Risk triplet; RIDM/CRM context; scenario logic chain; minimal cut sets; aleatory vs. epistemic; RISC; graded approach |
| [ch02](chapters/ch02-nasa-pra-scenario-development-and-logic-modeling.md) | Scenario Development and Logic Modeling | MLD, ESD, event trees, fault trees; success criteria; initiating events; linking; tree-style selection; reduction to MCS |
| [ch03](chapters/ch03-nasa-pra-data-collection-and-bayesian-parameter-estimation.md) | Data Collection and Bayesian Parameter Estimation | Two-phase database process; failure taxonomy; priors/likelihoods/posteriors; conjugacy; sequential updating; population variability |
| [ch04](chapters/ch04-nasa-pra-uncertainty-modeling-and-common-cause-failures.md) | Uncertainty Modeling and Common Cause Failures | Model of the world; epistemic models; lognormal/gamma/beta; beta-factor, Basic Parameter, Alpha Factor; CCBE expansion; Impact Vector |
| [ch05](chapters/ch05-nasa-pra-human-reliability-and-software-risk-assessment.md) | Human Reliability and Software Risk Assessment | HRA five-step; THERP, CREAM, NARA, SPAR-H; HEP and PSFs; time-reliability; CSRM; DFM; software reliability growth |
| [ch06](chapters/ch06-nasa-pra-physical-structural-and-phenomenological-models.md) | Physical, Structural, and Phenomenological Models | Phenomenological modeling; stress-strength; range safety (LARA, blast, re-entry); MMOD; fire PRA; limit states; FORM/SORM; NASGRO/PFM |
| [ch07](chapters/ch07-nasa-pra-uncertainty-propagation-and-results-presentation.md) | Uncertainty Propagation and Results Presentation | Two-step propagation; crude Monte Carlo vs. LHS; convergence; epistemic dependency; importance measures; exceedance curves |
| [ch08](chapters/ch08-nasa-pra-launch-abort-modeling-and-worked-pra-examples.md) | Launch Abort Modeling and Worked PRA Examples | Abort assessment chain; manifestation/environment; triggers; blast P-I; GoldSim integration; Appendices A–E (Boolean algebra, hardware models, conjugate updating, worked PRAs) |

## Topic Index
- **Risk triplet** → ch01, ch02
- **Scenario development** → ch02
- **Initiating events** → ch02, ch08
- **Master Logic Diagram** → ch02, ch08
- **Event sequence diagram** → ch02, ch08
- **Event tree** → ch02, ch08
- **Fault tree** → ch01, ch02
- **Minimal cut sets** → ch02, ch08
- **Success criteria** → ch02, ch08
- **Linking** → ch02
- **Data collection** → ch03
- **Bayesian parameter estimation** → ch03
- **Prior and posterior** → ch03, ch04, ch08
- **Likelihood** → ch03, ch04
- **Conjugate priors** → ch03, ch04, ch08
- **Sequential updating** → ch03
- **Failure taxonomy** → ch03
- **Population variability** → ch03
- **Aleatory uncertainty** → ch04, ch07
- **Epistemic uncertainty** → ch04, ch07
- **Model of the world** → ch04
- **Lognormal distribution** → ch04, ch07
- **Common cause failure** → ch04
- **Alpha factor model** → ch04
- **Beta factor model** → ch04, ch08
- **Coupling factor** → ch04
- **Human reliability analysis** → ch05
- **Human error probability** → ch05
- **Performance shaping factors** → ch05
- **THERP** → ch05
- **CREAM** → ch05
- **SPAR-H** → ch05
- **Software risk** → ch05
- **CSRM** → ch05
- **Conditional software failure** → ch05
- **Phenomenological models** → ch06
- **Stress strength** → ch06
- **Limit state** → ch06
- **Range safety** → ch06
- **Casualty expectation** → ch06
- **MMOD** → ch06
- **Fire PRA** → ch06
- **NASGRO fracture mechanics** → ch06
- **FORM and SORM** → ch06
- **Uncertainty propagation** → ch07
- **Latin hypercube sampling** → ch07
- **Monte Carlo** → ch07, ch08
- **Convergence** → ch07
- **Epistemic dependency** → ch07
- **Importance measures** → ch07
- **Fussell-Vesely** → ch07
- **Risk achievement worth** → ch07
- **Birnbaum measure** → ch07
- **Differential importance measure** → ch07
- **Exceedance curve** → ch07
- **Launch abort** → ch08
- **Abort effectiveness** → ch08
- **Failure manifestation** → ch08
- **Warning time** → ch08
- **Blast overpressure** → ch08
- **Pressure impulse curve** → ch08
- **Structure function** → ch08
- **Worked PRA examples** → ch08

## Supporting Files
- [glossary.md](glossary.md) — ~50 terms with chapter references, from Aleatory Uncertainty to Warning Time
- [patterns.md](patterns.md) — 14 named patterns with When/How/Trade-offs, covering the scenario logic stack to importance-driven resource allocation
- [cheatsheet.md](cheatsheet.md) — PRA task flow, model-style and HRA-method selection tables, likelihood-matching, importance-measure guide, and tells & smells

---

## Scope & Limits
This skill covers the *Probabilistic Risk Assessment Procedures Guide for NASA Managers and Practitioners* (NASA/SP-2011-3421, Second Edition, December 2011), a US Government public-domain work. It is the **quantitative** counterpart to NASA's risk doctrine: it supplies the scenario logic, data-and-Bayesian estimation, uncertainty and dependence modeling, human and software risk, physics-based models, and abort modeling that put defensible, uncertainty-bearing numbers on risk. It is a *guide of recommended procedures*, not an exhaustive textbook, so individual methods (fault-tree construction, Bayesian inference, CCF) are pointed to companion references — the *Fault Tree Handbook with Aerospace Applications* (2002), *Bayesian Inference for NASA Risk and Reliability Analysis* (NASA/SP-2009-569), NUREG/CR-4780 (CCF), the *NASA System Safety Handbook* (NASA/SP-2010-580), and the *NASA Risk Management Handbook* (NASA/SP-2011-3422, the **nasa-risk** pack). It does **not** cover the qualitative RIDM/CRM decision and governance framework in depth (see nasa-risk), programme-management or organisational-risk requirements, or non-aerospace regulatory contexts; its examples are space-flight-centric (launch vehicles, crewed missions, range safety, lunar/planetary missions) and anchored to the 2011 second edition.
