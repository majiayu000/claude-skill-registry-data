---
name: e1006-types
description: "Use when classify technical requirements for a space system under ECSS-E-ST-10C §6.2.1–6.2.13: assign each requirement to one of twelve requirement types (functional, mission, interface, environmental, operational, human factor, ILS, physical, PA-induced, configuration, design, verification), confirm every requirement belongs to exactly one type, and flag requirement statements that cannot be assigned without additional information. Trigger: ecss, e-st-10-system-scope, requirement-types, functional, mission, interface, environmental, operational, physical, PA-induced, configuration, design, verification."
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
  tags: [ecss, e-st-10-system-scope, requirement-types, functional, mission, interface, environmental, operational, physical, PA-induced, configuration, design, verification]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Requirement Types (space-systems/ecss/e1006-types)

Use when the task is to assign each technical requirement for a space
system to one of the twelve requirement types defined in ECSS-E-ST-10C
§6.2.1–6.2.13, verify that every requirement belongs to exactly one type,
and flag statements that cannot be type-assigned without further
clarification from the originating engineer.

## Domain quick reference

ECSS-E-ST-10C §6.2 defines a mutually exclusive, exhaustive taxonomy of
twelve requirement types. Every technical requirement in a system
specification must be assignable to exactly one of these types:

- **Functional** (§6.2.2): Specifies what the system shall do — the
  capabilities, transformations, and behaviors it must perform.
- **Mission** (§6.2.3): Derived from mission objectives — orbit
  parameters, design lifetime, coverage, and revisit time.
- **Interface** (§6.2.4): Governs the boundary between the system and
  external entities — mechanical, electrical, data-bus, and RF interfaces.
- **Environmental** (§6.2.5): Imposed by the natural or induced
  environment — thermal extremes, radiation dose, vibration and acoustic
  loads, EMC, and shock.
- **Operational** (§6.2.6): Defines how the system is operated —
  operating modes, command sequences, and ground-support timelines.
- **Human factor** (§6.2.7): Governs human-system interaction —
  ergonomics, HMI design, alarm management, and operator training.
- **ILS** (§6.2.8): Integrated Logistic Support — maintainability,
  mean time to repair, spare-parts provisioning, and supportability.
- **Physical** (§6.2.9): Tangible system properties — mass budget,
  dimensional envelope, volume, center of mass, and power draw.
- **PA-induced** (§6.2.10): Derived from the Product Assurance programme
  — reliability targets, safety, EEE-parts derating, and FMEA/FMECA.
- **Configuration** (§6.2.11): Configuration identification, baselining,
  and change-control obligations.
- **Design** (§6.2.12): Constraints on the design solution — material
  selections, manufacturing processes, and standards-compliance mandates.
- **Verification** (§6.2.13): Specifies how the system will be verified —
  test methods, qualification and acceptance test obligations, and
  inspection criteria.

## Workflow

1. Collect every technical requirement from the applicable specification
   document. Number each requirement with its originating identifier.
2. Read the requirement text and determine the primary subject: what the
   system must DO (→ functional), what the MISSION context demands
   (→ mission), what the BOUNDARY to an external system looks like
   (→ interface), what the ENVIRONMENT imposes (→ environmental), how
   the system is OPERATED (→ operational), what a HUMAN user needs
   (→ human factor), what LOGISTIC support must enable (→ ILS), what
   tangible PHYSICAL property is constrained (→ physical), what the PA
   PROGRAMME mandates (→ PA-induced), how CONFIGURATION is controlled
   (→ configuration), what DESIGN solution is constrained (→ design),
   or how the requirement will be VERIFIED (→ verification).
3. Assign exactly one type label. If the requirement text covers two
   types simultaneously, split it into two requirements before assigning.
   Do not assign multiple types to a single requirement statement.
4. For each requirement where the primary subject is ambiguous, flag the
   requirement as needing clarification from the originating engineer.
   Record the candidate types and the reason for the ambiguity.
5. Compile a type-assignment table: requirement ID, requirement text,
   assigned type, rationale. Requirements that remain without an
   assigned type after step 4 are listed separately as unresolved.
6. Review the table for completeness: confirm no requirement is
   missing a type entry, and that every assigned type is one of the
   twelve defined in §6.2.2–§6.2.13.

## Pitfalls

- Assigning "functional" as a catch-all for any unresolved requirement —
  functional type is reserved for statements about what the system must
  DO, not for requirements whose type has not yet been determined.
- Confusing environmental type with design type — an environmental
  requirement states what the system must survive; a design requirement
  states how the solution must be constructed. A radiation-hardened
  material mandate is a design requirement; a total-ionising-dose
  target is an environmental requirement.
- Conflating verification type with test descriptions — a verification
  requirement states that a property must be verified and by what method;
  a test procedure document is the artifact that executes that
  verification and is not itself a requirement type.
- Assigning two types to a single requirement statement — the standard
  requires each statement to be categorized to exactly one type. A
  statement that blends function with physical constraint must be
  separated into two discrete requirements before type assignment.
- Leaving PA-induced requirements implicit — requirements derived from
  the PA programme (reliability, safety, parts) must be explicitly
  captured in the specification as PA-induced type, not folded into
  functional or design requirements.

## Behavior contract (gate 3)

The type-assignment, alias-normalisation, auto-scoring, error-path, and
batch-categorization logic is exercised by the gate 3 contract test:
scripts/test_e1006_types.py against scripts/e1006_types_logic.py
(stdlib unittest, offline, 40+ assertions). Run:
python3 scripts/test_e1006_types.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
