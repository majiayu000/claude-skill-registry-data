---
name: reference-assets
description: Plan, create, version, approve, and quality-check visual and audio reference assets for characters, locations, props, styles, keyframes, voices, and music while separating canonical identity from scene state.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Reference Assets

## Workflow

1. Read the standalone contract, core contract, `CHARACTER_PROFILE.md`, `REFERENCE_AUTHORITY.md`, `REFERENCE_SHEETS.md`, reference asset system, canon, continuity, planned scenes, shot needs, and current reference manifest.
2. Identify only continuity risks that justify a reference asset. For characters, carry canonical `must_preserve`, `must_not_be`, and `may_vary` fields into the reference plan.
3. Assign stable `REF-###` IDs and one explicit role per reference record. Add `authority_scopes` and `must_not_control` whenever one reference must control identity, composition, temporal state, location, style, or prop/context without controlling the others.
4. Write or update `03_preproduction/references/reference_manifest.json`.
5. Write model-neutral reference briefs for missing character, location, prop, style, keyframe, voice, or music references.
6. For character, location, or prop multi-view coverage, write `reference_sheet_plans.json` using the native reference-sheet contract. Add functional/mechanical prop views when later action depends on how a prop works.
7. When several candidates must be reviewed, write `contact_sheet_plan.json` with panel roles and acceptance checks. Mark atlas layout as reference-only when its grid must not become composition authority.
8. Use the appropriate model adapter to create prompt documents when generation prompts are requested.
9. Separate canonical identity from scene-state variants such as expression, dirt, wardrobe, damage, props, and lighting.
10. Record recurring renderer failures under `drift_risks`; never promote a generation failure into canon.
11. Mark references `draft`, `approved`, `superseded`, or `rejected`. Never silently replace an approved identity master.
12. If an approved reference changes, run `project-impact` before continuing downstream.

## Quality gate

A production reference is approvable only when its continuity-critical traits are inspectable, its role is clear, its provenance is recorded, and its crop or framing does not hide required identity information.

## Done

Every continuity-critical subject has an approved reference or an explicit missing-reference record, and downstream prompts can state exactly what to preserve and what may vary.
