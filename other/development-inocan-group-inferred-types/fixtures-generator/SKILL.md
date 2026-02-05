---
name: fixtures-generator
description: Generates valid and invalid JSON fixtures for CommandDTO and DecisionDTO based on current contract schemas.
---

# Fixtures Generator Skill

## Purpose
Produces canonical test fixtures for contract validation and graph testing,
covering both valid and expected-invalid scenarios.

## Inputs
- Contract schemas in `contracts/schemas/command.schema.json` and `decision.schema.json`.

## Outputs
- Generated JSON fixtures written to appropriate `fixtures/` directories.

## Scenarios Covered
- Minimal valid commands.
- Ambiguous commands.
- Missing required fields.
- Invalid enum values and payload shapes.

## Definition of Done (DoD)
- Generated fixtures reflect current schema version.
- Invalid fixtures fail validation as expected.
- Fixtures are usable by contract-checker and graph-sanity.
