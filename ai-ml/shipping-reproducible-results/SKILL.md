---
name: shipping-reproducible-results
description: Package completed data analysis and ML work so an independent recipient can reproduce the claimed results, verify artifact lineage, and operate the handoff within its stated scope. Use when finalizing a project, study, model package, or review bundle; not for deploying to a live system.
---

# Shipping Reproducible Results

Ship an evidence-bearing result, not merely code that once ran. The package must connect the approved question to immutable inputs, an executable workflow, generated outputs, validation evidence, and an explicit handoff boundary.

## Freeze the result contract

Before packaging, record:

- the approved question, population, unit of analysis, time window, and exclusions;
- the exact claims and acceptance criteria being delivered;
- which outputs are authoritative and which are exploratory;
- the source snapshot or retrieval contract, including access limitations;
- the intended execution environment and supported operating scope.

Do not silently expand a validated result from a sample to a population, from retrospective analysis to prospective use, or from one environment to another.

## Build the provenance chain

Make each authoritative output traceable through:

```text
source identity -> immutable snapshot or query -> transformation -> configuration
-> code revision -> environment -> model artifact -> evaluation -> published output
```

Record content hashes for immutable local artifacts and durable identifiers for remote sources. Preserve raw inputs when permitted; otherwise preserve the exact query, retrieval time, schema, row counts, access requirements, and a safe fixture sufficient to test the pipeline.

Separate source data, intermediate artifacts, final outputs, caches, and human edits. Never require a recipient to guess which file is canonical.

## Make execution deterministic enough to audit

Provide one documented entry point from a clean state. Pin direct dependencies and runtime versions; record relevant system libraries and hardware. Seed every controllable source of randomness and document remaining nondeterminism rather than promising bitwise equality when the stack cannot provide it.

Packaging does not authorize restricted-data access, material compute, credential use, external transfer, or publication. Verify the relevant authority before those actions. When execution is not authorized or available, prepare the reproducible contract and label the unexecuted stages instead of running them.

Define acceptable reproduction precisely:

- exact hashes for deterministic artifacts;
- numeric tolerances for floating-point outputs;
- statistical or ranking tolerances for nondeterministic training;
- invariant schemas, row counts, and decision outcomes where values may vary.

Fail loudly on missing inputs, schema drift, stale caches, or incompatible artifacts.

## Prove the full path

Run from the documented clean entry point without relying on notebook state, shell history, undeclared credentials, or files outside the package. Verify every material claim with evidence of matching scope.

A green unit test is not proof of complete reproduction. The completion matrix must distinguish:

- environment creation;
- input acquisition or verification;
- preprocessing and feature generation;
- model loading or training;
- evaluation and independent validation;
- report or artifact generation;
- comparison with the authoritative expected outputs.

If a full rerun is impossible because data, compute, or credentials are unavailable, ship the maximum verifiable subset and mark the unexecuted stages as unproven. Do not call the package fully reproducible.

## Handoff to a named owner

Document how to run, verify, interpret, update, and safely retire the result. Include known limitations, prohibited uses, external dependencies, expected costs, credential ownership, failure signals, and escalation contacts. Preserve rejected hypotheses and failed experiments when they affect future maintenance or interpretation.

Use [assets/reproduction-handoff.md](assets/reproduction-handoff.md) as the release document and [assets/run-manifest.yaml](assets/run-manifest.yaml) as a machine-readable starting point. For verification levels, lineage requirements, and clean-room acceptance rules, read [references/reproduction-contract.md](references/reproduction-contract.md).

## Release gate

Release only when the package contains no secrets, unintended or unauthorized private data, machine-specific absolute paths, undeclared dependencies, or ambiguous canonical artifacts. Keep approved restricted artifacts in their authorized secure location and publish only permitted references or sanitized fixtures. External sharing and public release require separate authority. The final status must be one of:

- **reproduced:** an independent clean run met the declared acceptance criteria;
- **ready for independent reproduction:** the complete package and entry point are prepared, but an independent clean run has not yet been performed;
- **replayable with constraints:** the executable path is present but named stages require unavailable access or resources;
- **archival evidence only:** outputs and provenance are preserved, but the computation cannot currently be rerun.

State the status prominently. Never upgrade it based on intent or partial checks.
