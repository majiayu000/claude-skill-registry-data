---
name: e1002-levels
description: "Use when a product tree needs its verification levels defined and every requirement needs a verification level assigned before verification planning under ECSS-E-ST-10-02C: build the equipment/subsystem/element/segment/system hierarchy, assign each requirement to the level of the component(s) it is allocated to, and check whether a level is ready to close out. Trigger: verification level, verification levels, equipment subsystem element segment system, product tree, common ancestor, level closure, level close-out, E-ST-10-02, ecss, e-st-10c."
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
  tags: [ecss, e-st-10-02c, verification-level, product-tree, requirements-engineering]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification Levels (space-systems/ecss/e1002-levels)

Use when the task is defining the verification-level hierarchy of a
product tree and assigning every requirement to a level under
ECSS-E-ST-10-02C, ahead of verification-method selection
(E-ST-10-02 clause 5.2.2) and stage planning (E-ST-10-02 clause 5.2.4).

## Domain quick reference

- ECSS-E-ST-10-02C clause 5.2.3 organises verification bottom-up along
  the product tree into five levels: equipment, subsystem, element,
  segment, system. Each component in the product tree sits at exactly
  one level and integrates into a parent component at a higher level.
- A requirement allocated to a single component is verified at that
  component's level (see the sibling e10-req-allocation leaf for how a
  requirement reaches a component in the first place).
- A requirement that spans more than one component -- an interface or
  emergent-behaviour requirement -- is verified at the lowest level
  where those components are first integrated together: the closest
  common ancestor in the product tree, not each component's own level.
- Verification proceeds bottom-up: a level is not ready to close out
  while any requirement assigned to it, or to a level beneath it, is
  still unverified.

## Workflow

1. Model the product tree: every component with its verification level
   and its parent component (the root, typically system-level, has no
   parent). Validate the tree -- no unknown level, no missing parent,
   and every parent strictly above its child in the hierarchy -- before
   assigning requirements.
2. For each requirement, record the component(s) it is allocated to. A
   single component gives that component's level directly.
3. For an interface or emergent-behaviour requirement spanning two or
   more components, walk each component's ancestry up to the root and
   take the closest ancestor common to all of them; that ancestor's
   level is the requirement's verification level.
4. Build the level matrix: one level per requirement id, and confirm no
   requirement id from the input set is missing -- every requirement
   needs a level, not a sample.
5. Before reporting a level ready to close out, confirm every
   requirement assigned to that level or to any level beneath it in the
   equipment-to-system hierarchy has already been verified; list any
   that have not as the blockers.
6. Hand the level matrix to method selection (E-ST-10-02 clause 5.2.2,
   the sibling e10-req-verif-methods leaf) and to the Verification Plan
   / VCD (E-ST-10-02 clause 5.2.8).

## Pitfalls

- Assigning an interface requirement to one of its component's own
  levels instead of the level where the components are actually
  integrated together -- it under-states how far the system has to be
  assembled before compliance is observable.
- Treating a product tree as valid without checking that every parent
  sits strictly above its child -- a flat or inverted tree silently
  breaks every level assignment computed from it.
- Declaring a level closed while a requirement at a lower level is
  still open, breaking the bottom-up verification sequence.
- Dropping requirements from the level matrix -- an incomplete matrix
  fails the "every requirement gets a level" mandate even if the
  requirements present are assigned correctly.

## Behavior contract (gate 3)

The level-hierarchy, product-tree validation, level-assignment, and
level-closure logic is exercised by the gate 3 contract test:
scripts/test_e1002_levels.py against scripts/e1002_levels_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1002_levels.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
