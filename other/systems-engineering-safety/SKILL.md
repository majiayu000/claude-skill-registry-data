---
name: systems-engineering-safety
description: "Use when a task concerns aircraft or system-level engineering and safety assurance: guide the router to the systems-engineering-safety pack, covering ARP4754A systems-planning, requirements-traceability, requirements-allocation, verification-planning, and validation, ARP4761A safety-assessment, fta-fmea, common-cause-analysis, particular-risk-analysis, operating-support-hazard-analysis, and markov-analysis, and MBSE systems-engineering, sysml-modeling, state-machine, n2-diagram, and trade-study-analysis. This pack is the systems-level spine above item-level software and hardware assurance. Trigger: systems engineering, systems safety, ARP4754A, ARP4761A, safety assessment, fault tree, FMEA, common cause, particular risk, rotor burst, traceability, validation, allocation, verification planning, O&SHA, state machine, reachability, MBSE, SysML, N2 diagram, interface matrix, FDAL, IDAL, FHA, PSSA, SSA, trade study, Pugh matrix, Markov analysis, availability, MTTF."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: arp4754a
    reference-only: true
  - id: arp4761a
    reference-only: true
gated: false
domain: systems-engineering-safety
pack: systems-engineering-safety
compatibility: "agentskills.io SKILL.md; router/entry point for the systems-engineering-safety domain pack"
metadata:
  domain: systems-engineering-safety
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Systems engineering and safety domain pack (router)

Route here when the task is aircraft or system-level engineering,
safety assessment, or model-based systems engineering.

## Domain

Systems engineering and safety: development planning and development
assurance (ARP4754A), requirements traceability and validation, the
safety assessment process (ARP4761A) with fault tree and FMEA
analyses, common cause analysis, particular risk analysis, and
model-based systems engineering (SysML, digital thread).

Revision note: ARP4754B (2023) supersedes ARP4754A; this pack keys to
ARP4754A as the certification-baseline revision (FAA AC 20-174 cites A);
see standards-map.yaml arp4754a.revision_decision.

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| systems-engineering-safety/arp4754a/systems-planning | ARP4754A systems planning | FDAL/IDAL allocation, certification and development plans |
| systems-engineering-safety/arp4754a/requirements-traceability | ARP4754A requirements traceability | SRATS to HLR to LLR to code to tests, closure matrix |
| systems-engineering-safety/arp4754a/requirements-allocation | ARP4754A requirements allocation | allocation to items and functions, allocation coverage, unallocated requirements, double allocation |
| systems-engineering-safety/arp4754a/validation | ARP4754A validation | validation methods, requirements confirmation, validation scenarios |
| systems-engineering-safety/arp4761a/safety-assessment | ARP4761A safety assessment | FHA/PSSA/SSA sequence, analysis set selection |
| systems-engineering-safety/arp4761a/functional-hazard-assessment | ARP4761A functional hazard assessment | failure conditions, severity rating, probability targets, FHA worksheet, A-FHA, S-FHA |
| systems-engineering-safety/arp4761a/fta-fmea | FTA and FMEA | fault trees, minimal cut sets, failure modes, common cause |
| systems-engineering-safety/arp4761a/common-cause-analysis | Common cause analysis | common mode failures, zonal analysis, separation, independence |
| systems-engineering-safety/arp4761a/zonal-safety-analysis | ARP4761A zonal safety analysis | zone identification, zonal hazard severity, separation, containment, zonal hazard checklist, ZSA report |
| systems-engineering-safety/arp4761a/particular-risk-analysis | Particular risk analysis | single-event risks, rotor burst, bird strike, conditional probability, containment |
| systems-engineering-safety/arp4761a/operating-support-hazard-analysis | O&SHA | operating and support hazard analysis, maintenance hazards, ground operations, hazard register, risk index |
| systems-engineering-safety/mbse/systems-engineering | MBSE systems engineering | SysML modeling, function allocation, traceability closure |
| systems-engineering-safety/mbse/sysml-modeling | SysML modeling | diagram kinds, BDD/IBD, requirement and parametric diagrams, viewpoints, governance |
| systems-engineering-safety/mbse/state-machine | State machine modeling | SysML state machines, states, transitions, guards, events, reachability, firing trace |
| systems-engineering-safety/mbse/trade-study-analysis | Trade study analysis | trade study, decision criteria, weighted scoring, Pugh matrix, sensitivity analysis, alternative selection |
| systems-engineering-safety/arp4761a/markov-analysis | Markov analysis | Markov chain, state probability, transition rate, failure rate, repair rate, availability, MTTF, k-out-of-n |
| systems-engineering-safety/arp4754a/verification-planning | ARP4754A verification planning | verification methods, test/analysis/demonstration/inspection, verification coverage, derived requirements |
| systems-engineering-safety/mbse/n2-diagram | N2 interface diagram | N2 diagram, interface matrix, data links, interface count, missing interfaces |
| systems-engineering-safety/mbse/requirements-modeling | SysML requirements modeling | requirement stereotype, requirements diagram, derive/satisfy/verify links, status roll-up, vague term screening, verifiability |
| systems-engineering-safety/arp4754a/derived-requirements | ARP4754A derived requirements | derived requirement, derivation rationale, design decision source, implementation constraint, interface resolution, traceability path |
| systems-engineering-safety/arp4754a/development-assurance-levels | Development assurance levels | FDAL, IDAL, failure condition severity, DAL assignment A-E, independence |
| systems-engineering-safety/arp4761a/failure-rate-estimation | Failure rate estimation | failure rate, test hours, zero-failure demonstration, chi-square bound, confidence level |
| systems-engineering-safety/requirements/requirements-elicitation | Requirements elicitation | stakeholder needs, operational scenario, requirements baseline, atomicity, verifiability, weasel words, elicitation log |
| systems-engineering-safety/certification/certification-basis | Certification basis | certification basis, type certificate, supplemental type certificate, TSO, special conditions, FAR applicability, CS-25, certification program, means of compliance, regulatory path |
| systems-engineering-safety/arp4761a/preliminary-system-safety-assessment | Preliminary system safety assessment | PSSA, preliminary system safety assessment, safety requirements, FDAL, IDAL, allocation, architecture |
| systems-engineering-safety/arp4754a/systems-configuration-management | Configuration Management | configuration management, baseline, change control, change request, impact analysis, major change, minor change, safety critical requirement, certification data, interfaces, configuration item, change history, traceability closure. |
| systems-engineering-safety/arp4761a/reliability-block-diagram | Reliability block diagram | reliability block diagram, RBD, series parallel reliability, k-out-of-n, standby redundancy, MTBF |
| systems-engineering-safety/certification/means-of-compliance | Means of compliance | means of compliance, MOC-1, MOC-2, MOC-3, MOC-6, compliance matrix, certification item, coverage score |
| systems-engineering-safety/certification/equivalent-level-of-safety | Equivalent level of safety | ELOS finding, deviation from literal compliance, regulation intent, compensating measure, safety margin, equivalent safety finding |
| systems-engineering-safety/certification/mmel-development | MMEL development | master minimum equipment list, MMEL, dispatch with inoperative equipment, interval category, O procedure, M maintenance flag, relief verdict |
| systems-engineering-safety/continued-airworthiness/in-service-safety-assessment | In-service safety assessment | in-service safety assessment, service difficulty report, continued airworthiness, field event rate, observed versus predicted rate, single event rule, service bulletin, airworthiness directive request |
| systems-engineering-safety/safety-case/goal-structuring-notation | Goal structuring notation | goal structuring notation, GSN, safety argument, safety case, claim decomposition, solution node, away goal, argument validation, support coverage |
| systems-engineering-safety/continued-airworthiness/msg3-maintenance-analysis | MSG-3 maintenance analysis | MSG-3, maintenance steering group, scheduled maintenance task selection, hidden failure, evident failure, task category, interval determination, maintenance program development |
| systems-engineering-safety/continued-airworthiness/ica-cmr-ali-classification | ICA/CMR/ALI classification | airworthiness limitation items, ALI, certification maintenance requirements, CMR, airworthiness limitations section, ALS coverage, life-limited part, instructions for continued airworthiness |
| systems-engineering-safety/continued-airworthiness/airworthiness-directive-compliance | AD compliance | airworthiness directive compliance, directive applicability, affected model and serial range, compliance time remaining, grace band, open due overdue fleet report, directive effectivity |
| systems-engineering-safety/continued-airworthiness/type-certificate-data-sheet | Type certificate data sheet | type certificate data sheet, TCDS, type design record, approved model list, category airspeed limits, weight block validation, revision diff |
| systems-engineering-safety/arp4761a/fault-tree-importance-measures | Fault tree importance measures | fault tree importance measures, Birnbaum importance, Fussell-Vesely importance, risk achievement worth, risk reduction worth, basic event ranking, top event sensitivity |
| systems-engineering-safety/arp4761a/failure-mode-criticality | Failure mode criticality | failure mode criticality, FMECA criticality number, mode ratio, failure effect probability, item criticality, rate based ranking |
| systems-engineering-safety/arp4761a/beta-factor-analysis | Beta factor analysis | beta factor analysis, common cause fraction, CCF probability, common cause model, redundant channel common cause |
| systems-engineering-safety/arp4761a/fault-tree-uncertainty-analysis | Fault tree uncertainty analysis | fault tree uncertainty, lognormal error factor, lognormal confidence band, exceedance probability, uncertainty variance share |
| systems-engineering-safety/arp4761a/ssa-closure | SSA closure | ssa closure, system safety assessment close-out, closure gate, predicted probability margin, requirement closure |
| systems-engineering-safety/arp4761a/fmes-coverage-analysis | FMES coverage analysis | FMES coverage, FMEA to FHA coverage, uncovered failure condition, orphan row, coverage score |
| systems-engineering-safety/arp4761a/event-tree-analysis | Event tree analysis | event tree analysis, initiating event, mitigating function, branch path enumeration, end state frequency, dominant sequence |
| systems-engineering-safety/arp4761a/reliability-growth-analysis | Reliability growth analysis | reliability growth analysis, Duane growth slope, Crow-AMSAA shape beta, current MTBF, projected MTBF, growth verdict |
| systems-engineering-safety/arp4761a/maintainability-prediction | Maintainability prediction | maintainability prediction, failure rate weighted MTTR, mean time to repair, lognormal repair time percentile, t95 repair time |
| systems-engineering-safety/arp4761a/fault-tree-quantification | Fault tree quantification | top-event probability from minimal cut sets, rare-event approximation, min-cut upper bound, cut-set truncation |
| systems-engineering-safety/arp4761a/reliability-allocation | Reliability allocation | failure-rate and MTBF budget flow-down, equal-split and complexity-weighted apportionment, series-sum closure |

## Routing guidance

- Development assurance and planning questions route to the ARP4754A
  systems-planning sub-skill.
- Traceability and closure questions route to the ARP4754A
  requirements-traceability sub-skill; allocating requirements to
  items and functions, all- Configuration management questions route to the arp4754a configuration-management sub-skill.
ocation coverage, and unallocated
  requirements route to the requirements-allocation sub-skill;
  validation methods and confirmation questions route to the
  validation sub-skill.
- Safety assessment questions (severity, FHA/PSSA/SSA, analysis set)
  route to the ARP4761A safety-assessment sub-skill.
- Functional hazard assessment questions (failure condition
  identification, severity rating into the five categories, probability
  target mapping, FHA worksheet rows, A-FHA, S-FHA) route to the
  ARP4761A functional-hazard-assessment sub-skill; the FHA/PSSA/SSA
  sequence and analysis set selection stay with the safety-assessment
  sub-skill.
- Fault tree, FMEA, and cut-set questions route to the fta-fmea
  sub-skill; common mode and zonal independence questions route to
  the common-cause-analysis sub-skill.
- Single-event hazard questions (rotor burst, bird strike, tire
  burst, fire, conditional probability, containment) route to the
  particular-risk-analysis sub-skill.
- Zonal safety analysis questions (zone identification, zonal hazard
  severity classification, separation and containment verdicts, zonal
  hazard checklist completeness, ZSA report) route to the
  zonal-safety-analysis sub-skill; common mode failures and analysis
  set completeness questions route to the common-cause-analysis
  sub-skill.
- Operating and support hazard questions (maintenance tasks, ground
  operations, hazard register, risk index, acceptability) route to
  the operating-support-hazard-analysis sub-skill.
- Modeling and digital-thread questions route to the MBSE
  sub-skills: system-level engineering to systems-engineering,
  diagram-specific modeling to sysml-modeling, and state machines
  with transitions, guards, events, and reachability to
  state-machine.
- Trade study and alternative-selection questions (decision criteria
  weights, Pugh matrix, sensitivity analysis) route to the
  trade-study-analysis sub-skill.
- Item-level software or hardware questions route to the avionics pack.

- Markov chain, availability, MTTF, and transition rate questions route to the ARP4761A markov-analysis sub-skill.
- Verification method, verification coverage, and derived-requirement verification questions route to the ARP4754A verification-planning sub-skill.
- N2 diagram and interface matrix questions route to the MBSE n2-diagram sub-skill.
- SysML requirement modeling questions (requirement stereotype attributes, derive/satisfy/verify links, status roll-up, vague term screening, verifiability, atomicity) route to the MBSE requirements-modeling sub-skill.
- Derived requirement classification, derivation rationale, design decision and implementation constraint sources, and derived-requirement traceability questions route to the ARP4754A derived-requirements sub-skill.
- FDAL and IDAL assignment, failure condition severity to DAL mapping, and independence questions route to the ARP4754A development-assurance-levels sub-skill.
- Failure-rate estimation and demonstration from test or service data, zero-failure testing, and chi-square confidence bounds route to the ARP4761A failure-rate-estimation sub-skill.
- Stakeholder needs capture, operational scenarios, elicitation log, and requirement statement quality (atomicity, verifiability, weasel words) questions route to the requirements requirements-elicitation sub-skill.
- Certification regulation applicability, special condition determination, and TC, STC, and TSO path selection route to the certification certification-basis sub-skill.
- PSSA derivation of safety requirements from FHA outcomes, FDAL/IDAL allocation, and quantitative safety target allocation across the architecture routes to the arp4761a preliminary-system-safety-assessment sub-skill.
- MSG-3 scheduled maintenance task selection and hidden-failure exposure questions route to the continued-airworthiness msg3-maintenance-analysis sub-skill.
- top-event probability from minimal cut sets, rare-event approximation, min-cut upper bound, cut-set truncation questions route to the arp4761a fault-tree-quantification sub-skill.
- failure-rate and MTBF budget flow-down, equal-split and complexity-weighted apportionment, series-sum closure questions route to the arp4761a reliability-allocation sub-skill.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- RBD series parallel and redundancy reliability questions route to the arp4761a reliability-block-diagram sub-skill.
- Per-certification-item means-of-compliance assignment and matrix coverage questions route to the certification means-of-compliance sub-skill.
- Equivalent-level-of-safety questions (deviation from literal compliance with a regulation, compensating measures, safety margin to the rule intent) route to the certification equivalent-level-of-safety sub-skill.
- MMEL proposal questions (master minimum equipment list, dispatch with an item inoperative, interval category, O and M flags) route to the certification mmel-development sub-skill.
- In-service and continued-airworthiness questions (service difficulty reports, field event rate versus the SSA prediction, service bulletin or AD request) route to the continued-airworthiness in-service-safety-assessment sub-skill.
- GSN safety argument questions (claim decomposition, strategy and solution evidence nodes, away-goal justification, support coverage) route to the safety-case goal-structuring-notation sub-skill.
- Airworthiness-limitation and certification-maintenance-requirement questions (ALI/CMR classification, ALS coverage, life-limited part interval compliance) route to the continued-airworthiness ica-cmr-ali-classification sub-skill.

- AD compliance questions (directive applicability by affected model and serial range, compliance-time remaining in flight cycles, flight hours or calendar months, open due overdue status against the grace band, fleet compliance report) route to the continued-airworthiness airworthiness-directive-compliance sub-skill.
- Type-certificate-data-sheet questions (TCDS section compilation, weight block and category airspeed-limit validation, revision diff for TC amendment or STC review) route to the continued-airworthiness type-certificate-data-sheet sub-skill.
- Fault-tree basic-event ranking questions (Birnbaum and Fussell-Vesely importance, risk-achievement-worth and risk-reduction-worth from the minimal cut sets, dominance thresholds) route to the arp4761a fault-tree-importance-measures sub-skill.
- Rate-based failure-mode criticality questions (FMECA criticality number from the mode ratio and the failure-effect probability over an operating time, item criticality ranking for maintenance and redesign prioritization) route to the arp4761a failure-mode-criticality sub-skill.
- Common-cause quantification questions (beta-factor rate split into the independent and the shared common-cause fraction, dual-channel CCF probability, enhancement over the independence-only assumption) route to the arp4761a beta-factor-analysis sub-skill.

- Fault-tree uncertainty questions (lognormal error-factor propagation to a probability band around the top event, exceedance against a target, per-event uncertainty variance shares) route to the arp4761a fault-tree-uncertainty-analysis sub-skill.

- System safety assessment close-out questions (post-implementation verdict rollup by severity, meet-versus-target margins, open-condition and open-requirement lists, closure gate) route to the arp4761a ssa-closure sub-skill.

- FMES coverage questions (FMEA-row to FHA-failure-condition coverage, uncovered failure conditions, orphan FMEA rows, coverage score) route to the arp4761a fmes-coverage-analysis sub-skill.

- Event-tree questions (forward branching from an initiating event through mitigating-function successes and failures, end-state frequency rollup, dominant-sequence screening against severity targets) route to the arp4761a event-tree-analysis sub-skill.
- Reliability-growth questions (Duane log-log growth slope, Crow-AMSAA power-law process shape by MLE, improving or degrading verdict, current and projected MTBF) route to the arp4761a reliability-growth-analysis sub-skill.
- Maintainability-prediction questions (failure-rate-weighted MTTR rollup, lognormal repair-time t50 and t95 percentiles, verdict against a maximum-repair-time requirement) route to the arp4761a maintainability-prediction sub-skill.
