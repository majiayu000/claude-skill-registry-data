---
name: studio-context-brief
description: Use when an active KIT-managed Goal needs compact brief, working, or resume context projections from trusted structured state while preserving exact technical literals and durable handoff authority.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: workflow
    lifecycle_stage: operate
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: context/working.json
    required_evidence: [goal-manifest, reduced-state, projection-report]
    owner: HoaTV Studio
    reviewer: null
    maturity: experimental
    last_reviewed: 2026-09-04
    provenance:
      derived_from:
        repo: JuliusBrussee/caveman
        path: skills/caveman/SKILL.md
        commit: b4335705d436f5110386a1c39c6d8aed5002aeeb
        license: MIT
      patterns_from: [precision and compression principles only]
      copied_text: none
---
# Studio Context Brief

## Overview
Generate deterministic compact projections for an active KIT Goal from its trusted manifest, last-good reduced state, and evidence references. Compression removes repetition while retaining technical meaning; it is not arbitrary transcript summarization or a durable handoff.

## When to use
Use when the compact GUI, current agent, or a later session needs the `brief`, `working`, or `resume` projection for an active KIT-managed Goal.

## When NOT to use
Do not use to discover project facts, compress an arbitrary raw transcript by default, invent missing evidence, bypass projection caps, or replace `studio-handoff`. Route initial project discovery to `studio-project-intake` and durable cross-session transfer to `studio-handoff`.

## Required inputs and context discovery
Require an exact goal root containing a trusted Goal manifest and last-good reduced state. Consume structured scope, do-not-touch paths, current packet, next action, decisions, blockers, failures, changed files, evidence labels and references, and deduplicated completed history. Missing facts stay missing or are labeled `Unverified` or `BLOCKED`.

## Safety and risk level
Write only derived JSON and Markdown projections under the selected goal's `context/` directory. Never read arbitrary transcript input by default, shorten an exact technical literal, expose secrets or raw logs, cross the goal root, mutate Goal state, or grant handoff authority.

## Workflow
1. Resolve one active opted-in Goal and load its trusted manifest plus last-good reduced state; reject arbitrary raw transcript input.
   Completion criterion: source artifacts, goal ID, plan version, and required fact references are explicit; missing or invalid authority is `BLOCKED`.
2. Order facts by preservation priority: safety and ownership boundaries, negations and blockers; current packet and exact next action; paths, commands, symbols, numbers, units, decisive errors, artifacts, and evidence labels; then decisions, dependencies, and deduplicated completed history.
   Completion criterion: required facts retain exact spelling and source references before optional history is considered.
3. Generate all three projections: `brief` targets 150 tokens with hard cap 300, `working` targets 800 with hard cap 1,200, and `resume` targets 1,600 with hard cap 2,400.
   Completion criterion: each canonical projection contains exactly `schema_version`, `goal_id`, `projection`, `status`, `count_kind`, `count`, `target`, `hard_cap`, `text`, `required_fact_refs`, and `evidence_label`.
4. Measure with a supported runtime tokenizer when available. Otherwise use conservative UTF-8 byte fallback against the numeric hard cap, record `utf8_byte_fallback`, and label exact target-runtime token count `Unverified`.
   Completion criterion: no approximate measurement is represented as exact.
5. Remove filler, duplicate commentary, duplicate output, and superseded history without changing paths, commands, symbols, numbers, units, negations, or decisive error strings.
   Completion criterion: a required indivisible fact either appears exactly or remains referenced; silent shortening and semantic reversal are forbidden.
6. If required safety text or one indivisible exact literal cannot fit, emit projection status `BLOCKED`, empty `text`, complete `required_fact_refs`, and `evidence_label: BLOCKED`. Those existing fields mean the projection is not standalone context; do not add a second report artifact.
   Completion criterion: hard caps are never bypassed and overflow is never hidden by truncation.
7. Write JSON plus Markdown views for requested projections. Keep `studio-handoff` authoritative for durable transfer; a handoff may consume `resume` but must refresh Git state, files, commands, evidence labels, restore information, and reactivation prompt in normal prose.
   Completion criterion: each projection stays within the eleven-field canonical contract, and no compact projection is called an authoritative durable handoff.

## Evidence and output contract
Produce `context/brief.json`, `context/working.json`, and `context/resume.json` with matching Markdown views when all are requested. Each JSON projection uses only the eleven canonical fields above. `status: READY` with nonempty `text` is usable within its recorded measurement; `status: BLOCKED`, empty `text`, retained `required_fact_refs`, and `evidence_label: BLOCKED` means it must not be used as standalone context. Deterministic complete inputs may earn `PASS`; missing authority or indivisible overflow is `BLOCKED`. `studio-handoff` remains durable-transfer authority outside the projection schema.

## Handoff contract
The `resume` projection is optional input, not authority. `studio-handoff` must refresh repository state and preserve exact normal-prose transfer requirements before another session relies on it.

## Pitfalls and anti-rationalization
- “Shorter is better” never permits changed paths, commands, numbers, units, negations, or decisive errors.
- A byte fallback is not exact target-runtime token evidence.
- A referenced required fact does not make a `BLOCKED` projection standalone-safe.
- Compact context does not prove that a handoff is current.

## Verification checklist
- [ ] Inputs came from trusted structured Goal artifacts.
- [ ] Exact literals and safety priority were preserved.
- [ ] All requested projections report status, measurement, caps, text, required fact refs, and evidence label.
- [ ] Overflow is `BLOCKED`, not truncated or cap-bypassed.
- [ ] Standalone usability is derived only from existing status, text, required fact refs, and evidence label.
- [ ] `studio-handoff` remains durable-transfer authority.

## References and scripts
Load [commands and projection interpretation](references/commands.md) before execution. The standalone skill bundles `scripts/context_brief.py`, `schemas/studio-context-projection.schema.json`, and `schemas/studio-goal-state.schema.json`.
