---
name: tw-codebase-doctrine
description: Compile deep repository evidence into artifact-bound correctness doctrine — authority/law/proof maps, owned invariants, failure archaeology, and the strongest durable destination for each piece of knowledge, plus an optional minimal repository-specific skill portfolio. Use when the user wants both deep codebase understanding AND durable doctrine, knowledge routing, or repo-specific skill recommendations. Research discoverable facts before asking. Read-only. Not for quick onboarding, one isolated invariant, ordinary implementation, generic review, or direct skill creation.
---

# Codebase Doctrine

## Mission

Determine what future maintainers and coding agents must **know, decide, reject, and prove** to change a repository safely.

```text
authorized intent
-> named search questions
-> artifact-bound evidence
-> closed claim graph
-> current/target authorities, laws, invariants, boundaries, failures, proof
-> strongest knowledge destinations
-> zero or one root skill plus zero to five focused skill candidates
```

The doctrine is a canonical synthesis for one pinned repository and intent state. It is never stronger than current code, executable proof, or explicit user authority.

## Activation boundary

Use only when the request contains **both** deep repository understanding **and** durable correctness doctrine, knowledge routing, authority/proof maps, or repo-specific skill recommendations.

Do not use for: quick onboarding or architecture fingerprinting (use `tw-codebase-archaeology`); one feature, bug trace, or isolated invariant (use `tw-invariant-ace`); ordinary implementation or generic review; skill brainstorming without repository evidence; or direct skill creation. This skill is **read-only** — persistence and skill creation require separate explicit authorization.

## Modes

| Mode | Purpose | Terminal artifact |
|---|---|---|
| `survey` | Provisional map + exact next questions | Codebase Survey |
| `doctrine` | Complete baseline workflow | Codebase Doctrine |
| `deep` | Baseline plus adaptive specialists | Doctrine + specialist receipts |
| `refresh` | Revalidate an existing doctrine at a new state | Doctrine Delta + resulting Doctrine |
| `portfolio` | Reevaluate knowledge destinations and skill candidacy | Portfolio |
| `audit` | Compare current guidance and skills against doctrine | Doctrine Audit |

Pick exactly one. Do not force a full doctrine into survey, portfolio, audit, or delta work.

## Phase 0 — intent before doctrine

Before asking intent questions, inspect enough to distinguish discoverable facts from user-owned choices: repository guidance and existing skills; manifests and build/test/release roots; major subsystems and cross-cutting flows; deployment/distribution shape; visible correctness, compatibility, security, performance, and operational priorities.

Then clarify **only material user-owned choices** (ask directly, or hand to a clarifying-questions pass): target boundary, consumers, current-state vs target-state posture, desired products, correctness priorities, non-goals, proof bar, compatibility/migration posture, persistence. Do **not** ask for repository facts, laws, implementation design, or skill-file content — discover those.

Record an intent capsule: target, consumers, posture, products, priorities, non-goals, proof bar, a primary correctness question, a primary risk, explicitly-sourced user invariant hypotheses (if any), and assumptions/deferrals. The capsule does **not** declare repository-derived laws before research.

## Artifact state

Pin and bind all evidence to one state: `repository_root`, `repository_name`, `branch`, `head`, `dirty_state`, `scope`, `intent_id`, `captured_at`. Re-pin before closure; reject stale evidence after a relevant head, diff, scope, or intent change.

## Evidence discipline

Always separate: `fact | inference | recommendation | open-question | current-observed-law | documented-intent | explicit-user-target | proposed-law | contradicted-or-retired`. Treat absent evidence as uncertainty, not permission.

## Workflow

### 1. Fingerprint the repository
Repository kind, languages, build/test systems, deployment shape, dependency direction, subsystems, public-contract roots, entrypoints, local dialect. Architecture is a hypothesis backed by responsibilities and dependency direction, not directory names.

### 2. Build the system map
Trace representative flows: `input/trigger -> parsing/routing -> orchestration -> domain transition -> persistence/integration -> output/effect`. Record external boundaries, persistence/config roots, feedback loops, and delays.

### 3. Map authority and state
For important state and evidence, identify who may create, mutate, validate, certify, publish, transfer, consume, retire, and roll back it. Prioritize write paths, transitions, certificates, transactions, and rollback over readers or names.

### 4. Extract the behavioral model
Use the smallest correctness vocabulary that explains carriers, operations, observations, state classes, transitions, laws, non-laws, forbidden states, and projections. Do not turn incidental current behavior into doctrine.

### 5. Extract current and target laws
Every law records: doctrine status and normative authority; owner; accepted observations and counterexamples; current evidence and (when applicable) target authority; gap statement; proof obligations and proof surfaces. Never merge an observed law and a proposed repair law into one unlabelled row.

### 6. Extract owned invariants and boundaries
An invariant requires: owner, source of truth, initialization, preserving transitions, violating counterexamples, enforcement boundary, exception owner, proof. A boundary requires: accepted/rejected inputs, authority before/after, transferred state or evidence, proof.

### 7. Failure archaeology
Normalize local wounds into recurring law, authority, representation, boundary, or proof-shape failures. A negative route may be suspected, witnessed, canonical, or retired — only a current canonical projection may create a durable route exclusion.

### 8. Map proof
Distinguish proof design, executed current proof, historical proof, and manual/reviewer proof. Executed current proof records command, exit code, result reference, toolchain, target, artifact state, and verification time.

### 9. Resolve contradictions
Do not average incompatible claims. Resolve them, or preserve the contradiction, the stronger evidence, residual uncertainty, and materiality.

### 10. Route durable knowledge
Every durable active claim gets exactly one primary destination — prefer the strongest enforceable one:
```text
code | type_or_representation | test_or_property | static_tool_or_linter | CI_gate
| repository_guidance (AGENTS.md/CLAUDE.md) | ADR_or_reference | negative_ledger
| repository_root_skill | focused_skill | retain_in_doctrine | reject
```

### 11. Optional skill portfolio
Shape: zero or one root repository skill, plus zero to five focused skills. No skill is required. Each candidate is an evidence-bearing decision, not a self-attested boolean; new candidates normally end as `recommended_for_trial`, with `accepted` reserved for empirical use evidence.

### 12. Test saturation
Stop when more search is unlikely to change a material decision: every required lane covered, no open route-changing search, no unresolved material contradiction, every durable active claim routed. Never claim exhaustive understanding.

## Adaptive specialists (deep mode)

Only for unresolved route-changing questions, never just because mode is `deep`. Suggested waves: (1) cartographer + authority/state mapper; (2) behavioral-law miner / failure-forensics / proof mapper on identified surfaces; (3) portfolio skeptic after draft routing; (4) saturation auditor after the complete draft. Spawn read-only workers with your harness's parallel-agent mechanism (Claude Code Task / Codex custom agents); each gets a scoped assignment and returns one evidence-bearing packet; reject stale, wrong-scope, or out-of-authority material; synthesize yourself.

## Persistence and handoff

Default output is conversational. Persist only when requested, to `.codebase-doctrine/doctrine.yaml` (local-exclude by default unless the user wants versioned doctrine). This skill recommends skills; it does not create them. After explicit authorization, hand a doctrine-bound skill brief to a skill-authoring pass.

## Hard rules

- Read-only. Research discoverable facts before asking.
- No material doctrine without a locked intent capsule.
- No repository-derived invariant locked as user intent; no silent intent drift.
- Every durable active claim has exactly one primary route.
- Writes and transitions outrank reads for authority.
- No law without status, authority, counterexample, evidence, and proof posture.
- No invariant without owner, initialization, transitions, boundary, counterexample, and proof.
- No persistence or skill creation without explicit authorization.
- Never claim exhaustive understanding.
