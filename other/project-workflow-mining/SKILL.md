---
name: project-workflow-mining
description: "Extracts repeatable input-to-output workflows from repository examples, tests, scripts, documentation, and configuration."
---

# Project Workflow Mining

## Purpose

Extracts repeatable input-to-output workflows from repository examples, tests, scripts, documentation, and configuration.

## When to use

Create skills based on how people use a repository rather than count-inflating file-by-file wrappers.

## Required inputs

Capability map, examples, tests, documented commands, scripts/config, and nearby catalog entries.

## Workflow

1. Collect candidate workflows from examples, docs, CI, tests, build scripts, configuration templates, migrations, and troubleshooting notes.
2. Describe each workflow by goal, inputs, prerequisites, decision points, actions, output, validation, and recovery.
3. Group fragments that achieve one user goal; split only when inputs, decisions, or deliverables materially differ.
4. Attach source evidence to every candidate and mark missing prerequisites or assumptions.
5. Discard candidates that merely restate docs, list options, or duplicate a neighboring skill without an independent result.

## Validation checklist

Each retained workflow produces a concrete artifact and a validation approach; title-only variants are rejected.
- [ ] Source revision, paths, and authorized scope are recorded.
- [ ] Every material claim has a source reference or explicit uncertainty label.
- [ ] At least one neighboring/negative case has been checked.
- [ ] Validation describes what actually ran and does not treat a plan as a pass.

## Required output

Ranked workflow cards with evidence, input/output contract, prerequisites, validation method, and merge/split notes.

## Boundaries and failure handling

Do not recommend destructive scripts against production merely because an example contains them. State side effects and seek authorization before execution.
If source access, evidence, permissions, or provenance is insufficient, stop and return blockers rather than inventing details. Preserve originals and seek human review for ambiguous licensing or semantic boundaries.

## Trigger examples

- **Positive:** Mine tests, examples, and commands into distinct workflows that users can actually follow.
- **Negative:** Create one skill per file or heading, regardless of whether each is a complete task.
