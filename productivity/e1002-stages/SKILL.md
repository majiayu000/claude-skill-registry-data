---
name: e1002-stages
description: "Use when defining verification stages for a product under ECSS-E-ST-10-02C: qualify, accept, verify pre-launch, in-orbit (incl. commissioning) and post-landing each with its objective and applicability to the product's launched/recovered life profile, ahead of stage-specific planning (qualification, acceptance, pre-launch, in-orbit, post-landing leaves). Trigger: verification stages, qualification stage, acceptance stage, pre-launch verification, in-orbit verification, commissioning, post-landing verification, E-ST-10-02, ecss, e-st-10c."
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
  tags: [ecss, e-st-10c, verification-stages, qualification, acceptance, pre-launch, in-orbit, post-landing]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification Stages (space-systems/ecss/e1002-stages)

Use when the task is defining which verification stages apply to a
product under ECSS-E-ST-10-02C, and what each stage is meant to
demonstrate, before the detailed stage plans (qualification, acceptance,
pre-launch, in-orbit, post-landing) are written.

## Domain quick reference

- ECSS-E-ST-10-02C clause 5.2.4.1 fixes five verification stages in a
  set order, each covering a different point in the product's life.
  Qualification comes first, then acceptance, then pre-launch. In-orbit
  follows, and commissioning sits inside it rather than beside it.
  Post-landing closes the set.
- Qualification demonstrates the design meets its requirements with
  adequate margin, before any article is accepted for delivery.
  Acceptance demonstrates the specific deliverable article is free of
  manufacturing and workmanship defects and compliant, without consuming
  the design margin qualified above.
- Pre-launch confirms the integrated flight configuration stays
  compliant through transport, storage, and launch-site processing.
  In-orbit confirms operational performance, including commissioning of
  functions before routine operations begin. Post-landing confirms the
  condition and performance of recovered or returned hardware.
- Not every stage applies to every product: qualification and acceptance
  always apply; pre-launch and in-orbit apply only to a product that is
  launched; post-landing applies only to a product that is recovered
  after flight. A product cannot be recovered without having been
  launched.
- The five stages have a fixed relative order; a stage plan or schedule
  that lists them out of order (e.g. pre-launch before qualification)
  signals a planning error, not a legitimate variation.

## Workflow

1. For the product under verification, capture its life profile: does it
   get launched, and is it recovered or returned after flight (ground
   segment equipment is typically neither).
2. Determine the applicable stages from that profile: qualification and
   acceptance always apply; add pre-launch and in-orbit if launched; add
   post-landing if recovered.
3. Attach each applicable stage's objective (as summarized above) to the
   stage plan, so downstream stage-specific planning knows what it is
   trying to demonstrate rather than just which stage it is running.
4. When a stage plan or schedule lists stages in a concrete sequence,
   check that sequence against the canonical order (qualification,
   acceptance, pre-launch, in-orbit, post-landing); flag any stage that
   appears before a stage that should have preceded it.
5. Before closing the stage definition, confirm every applicable stage
   from step 2 has a corresponding entry in the plan or schedule --
   dropping post-landing for a recovered product, or in-orbit for a
   launched one, leaves a gap clause 5.2.4.1 does not allow.
6. Hand the per-stage objectives to the stage-specific leaves
   (e1002-qualification, e1002-acceptance, e1002-pre-launch,
   e1002-in-orbit, e1002-post-landing) for detailed execution planning.

## Pitfalls

- Applying all five stages uniformly regardless of the product's life
  profile, e.g. planning a post-landing stage for hardware that is never
  recovered.
- Treating "recovered" as independent of "launched" -- a product cannot
  reach post-landing without having gone through pre-launch and in-orbit
  first.
- Accepting a stage schedule with stages out of canonical order without
  flagging it as a planning error.
- Leaving an applicable stage out of the plan silently instead of
  surfacing it as a missing stage.

## Behavior contract (gate 3)

The stage-objective, applicability, ordering, and completeness logic is
exercised by the gate 3 contract test: scripts/test_e1002_stages.py
against scripts/e1002_stages_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1002_stages.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
