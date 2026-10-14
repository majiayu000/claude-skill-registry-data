---
name: e1011-params
description: "Use when identify and map the interrelated HFE parameters that characterise a human-machine system under ECSS-E-ST-10-11C §4.2.1.1–4.2.1.2: categorize each parameter into the standard parameter set (performance, workload, situation awareness, human error, training, environment, interface, communication), trace interrelationships among parameter categories, assess completeness of the parameter set against required categories, and verify that every defined system phase carries at least one parameter assignment. Trigger: ecss, e-st-10-system-scope, hfe-parameters, human-machine-system, workload, situation-awareness, human-error, parameter-completeness."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-10-system-scope, hfe-parameters, human-machine-system, workload, situation-awareness, human-error, parameter-completeness]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Human Factors Engineering — HFE Parameter Set (space-systems/ecss/e1011-params)

Use when the task is to identify the interrelated HFE parameters for a
human-machine system under ECSS-E-ST-10-11C §4.2.1.1–4.2.1.2 — categorizing
each parameter into the standard set, tracing interrelationships, checking
completeness against required categories, and verifying coverage across all
system phases.

## Domain quick reference

- ECSS-E-ST-10-11C §4.2.1.2 defines a standard parameter set that covers
  every HFE concern a human-machine system must address: **performance**
  (task accuracy and throughput), **workload** (mental and physical load on
  the operator), **situation awareness** (the operator's comprehension of
  system state), **human error** (error probability and error type),
  **training** (crew preparation requirements), **environment** (physical
  conditions such as noise, lighting, vibration), **interface**
  (human-machine interface characteristics including displays and controls),
  and **communication** (crew-to-crew and crew-to-ground exchange parameters).
  Each parameter under assessment is categorized into exactly one of these
  eight categories before its interrelationships are traced.
- §4.2.1.1 establishes that parameters are not independent: workload
  interacts with both performance and human error; situation awareness
  interacts with both performance and human error; training influences
  human error and performance; environment influences workload;
  interface influences workload; and communication influences situation
  awareness. These pairwise interrelationships must be made explicit so
  that a change in one parameter propagates to all partners in the assessment.
- The four **required** categories are performance, workload, situation
  awareness, and human error. A parameter set missing any of these
  categories is incomplete regardless of how many optional categories
  are present.
- Parameter coverage must extend to every defined system phase (e.g.
  nominal operations, contingency, maintenance). A phase with no
  parameter assigned is not characterized.

## Workflow

1. Inventory every candidate HFE parameter for the system under assessment.
   For each parameter record its name, the raw type label from the input
   artefact, and the system phase(s) it belongs to.
2. Categorize each parameter: map the raw type label to one of the eight
   standard categories. Reject any label that does not match a category or
   a recognized synonym with an explicit finding; do not silently drop or
   default-categorize it.
3. Trace interrelationships: for every pair of categories that are both
   represented in the parameter set, check whether a known interrelationship
   applies (workload↔performance, workload↔human_error,
   situation_awareness↔human_error, situation_awareness↔performance,
   environment↔workload, interface↔workload, training↔human_error,
   training↔performance, communication↔situation_awareness). Record each
   active pair. Flag any parameter whose category has no active interrelationship
   partner in the set (it is isolated from the web of HFE concerns).
4. Check completeness: verify that the four required categories —
   performance, workload, situation awareness, human error — each have at
   least one parameter assigned. Issue a finding for every required category
   that is absent.
5. Check phase coverage: for every defined system phase, verify that at
   least one parameter is assigned. Issue a finding for every phase with
   no parameter. Also flag any parameter that carries no phase assignment.
6. Aggregate findings: the parameter-set characterization is complete only
   when the finding list from steps 2–5 is empty.

## Pitfalls

- Accepting an unrecognized parameter type without raising a finding and
  then counting the parameter as contributing to completeness — an
  uncategorizable parameter cannot satisfy a required category.
- Treating an isolated parameter (one whose category has no interrelated
  partner present) as fully characterized — the interrelationship web is
  part of the characterization, not a cosmetic annotation.
- Reading "required categories covered" as equivalent to "parameter set
  complete" — phase coverage is a separate completeness dimension; a set
  with all four required categories but a system phase with no parameters
  is still incomplete.
- Collapsing all synonyms silently without recording the mapping — if a
  raw label was resolved via a synonym, record the resolution so the
  reviewer can validate it against the source artefact.

## Behavior contract (gate 3)

The parameter-categorization, interrelationship-mapping, completeness-check,
and phase-coverage logic is exercised by the gate 3 contract test:
scripts/test_e1011_params.py against scripts/e1011_params_logic.py
(stdlib unittest, offline). Run:

    python3 scripts/test_e1011_params.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
