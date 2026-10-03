---
name: investigate-codebase
description: >-
  Build an evidence-backed working model of an existing codebase. Use when you
  must orient in a large or unfamiliar repository; explain architecture or a
  subsystem; trace a request, runtime, control, or data flow for a concrete
  question or bug; analyze a branch, commit, diff, or pull request for behavioral
  impact and blast radius; or assess AI-generated or changed code against
  requirements, contracts, invariants, tests, and runtime evidence. Default to
  read-only investigation. Do not trigger only because a coding task touches an
  existing repository; use when understanding or verification is the requested
  outcome or a substantial prerequisite.
---

# Investigate Codebase

## Objective

Build the minimum sufficient, falsifiable model needed to answer the user's
question. Prefer a thin vertical slice over an exhaustive repository summary.
Optimize for human understanding and verification, not the amount of code read.

## Operating contract

- Read all applicable repository and agent instruction files before inspecting
  implementation, including nested per-directory files under whichever convention
  the repository uses (for example `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md`).
- Default to read-only investigation. Do not edit files, install dependencies,
  switch branches, reset state, or alter durable resources unless the user
  requested that action.
- Preserve unrelated and dirty worktree changes. Separate committed changes from
  local modifications before drawing conclusions.
- Record the repository revision. For change analysis, resolve and record the
  exact base and head revisions rather than silently guessing.
- Treat README files, architecture documents, comments, and PR descriptions as
  intent evidence that must be reconciled with implementation and behavior.
- Start narrow. Expand scope only when a dependency, contract, contradiction, or
  unresolved hypothesis requires it.
- Prefer version-control history, manifests, exact symbol references, fast
  repository-wide text search (`rg`, `grep`, or the equivalent available in the
  environment), language-native tooling, tests, and runtime observation. Use
  semantic or embedding search only to locate candidate code, never as behavioral
  proof.
- Use whatever file-reading, search, and command-execution capabilities the host
  environment provides. If a capability required by a check is unavailable, record
  the check as `UNKNOWN` with the reason rather than substituting a weaker claim.
- Ask before checks that may use production credentials, access external systems,
  mutate durable state, incur meaningful cost, or take substantial time.
- Never equate passing tests, high coverage, or clean static analysis with proof
  of complete correctness.

## Select the investigation

Choose one primary mode and read its guide completely:

- `ORIENT`: Map a large or unfamiliar repository. Read
  [orient-large-codebase.md](references/orient-large-codebase.md).
- `TRACE`: Explain a concrete runtime, control, or data flow. Read
  [trace-runtime-flow.md](references/trace-runtime-flow.md).
- `IMPACT`: Analyze a PR, branch, commit, or diff. Read
  [analyze-pr-impact.md](references/analyze-pr-impact.md).
- `VERIFY`: Assess generated or changed code. Read
  [verify-generated-code.md](references/verify-generated-code.md).

Combine modes only when necessary, such as `IMPACT + VERIFY`. Read only the
guides required for the selected modes.

Choose a depth:

- `scan`: Find landmarks and a likely path; keep uncertainty explicit.
- `working`: Produce an evidence-backed explanation and focused checks. Use by default.
- `audit`: Broaden risk and verification coverage when explicitly requested or
  warranted by the change's consequences.

State the selected mode, depth, scope, revision, assumptions, and important
environment limits in the result.

## Investigation loop

### 1. Anchor the target

- Identify the repository root, applicable instructions, working-tree state,
  revision, build system, and relevant runtime configuration.
- For a PR or branch, resolve the actual comparison base from PR metadata or the
  merge base. Keep unrelated local changes out of the comparison.
- Exclude generated, vendored, fixture, snapshot, lockfile, and formatting noise
  from semantic analysis unless one of them changes behavior or contracts.

### 2. Frame falsifiable questions

- Rewrite the request as observable questions: given which input and preconditions,
  what output, state change, side effect, or failure should occur?
- Identify available correctness oracles: explicit requirements, acceptance
  criteria, public contracts, schemas, stable prior behavior, domain invariants,
  reference implementations, or production observations.
- If no independent oracle exists, state which consistency claims can be assessed
  and which intent claims cannot be established.

### 3. Build the minimum map

- Locate only the relevant manifests, boundaries, entry points, public contracts,
  configuration, persistence, external effects, and tests.
- Describe components by runtime or domain responsibility rather than by directory.
- Mark dynamic dispatch, dependency injection, reflection, generated code, plugins,
  queues, and callbacks as unresolved edges until supported by evidence.

### 4. Trace a thin vertical slice

Follow the smallest path that can answer the question:

`input boundary -> parsing/auth -> orchestration -> domain decisions -> state or external effect -> output/error/telemetry`

Track control flow, data-shape changes, state ownership, feature flags, async
boundaries, retries, serialization, errors, and observable side effects when relevant.

### 5. Maintain an evidence ledger

For each material claim, record:

| Claim | Evidence status | Revision + path/symbol or command | Result or limitation |
|---|---|---|---|

Use these labels:

- `SOURCE`: Directly supported by implementation, configuration, schema, or diff.
- `RUNTIME`: Observed through an executed command, test, log, trace, or reproducer.
- `INFERRED`: Reasoned from evidence but not directly observed.
- `UNKNOWN`: Missing code, environment, specification, oracle, or access.
- `CONTRADICTED`: A counterexample or conflicting source disproves the claim.

Prefer `revision + file + symbol`; use line numbers as secondary anchors because
they drift. Include exact commands and outcomes for runtime evidence. Never label a
statically inferred call path as an observed runtime trace.

### 6. Challenge the model

- Turn the model into predictions that could be false.
- Search for contradictory call sites, tests, schemas, configuration, history,
  and runtime behavior.
- Consider empty and boundary inputs, permissions, ordering, retries, idempotency,
  concurrency, partial failure, compatibility, migration, rollback, and external
  boundary behavior according to risk.
- Ask which unchanged behavior must remain invariant, not only what changed.

### 7. Verify economically

Choose the cheapest check capable of falsifying each important claim:

1. Source, type, schema, and configuration inspection
2. Typecheck, lint, compile, or static analysis
3. Focused unit or component test
4. Integration or end-to-end path
5. Base/head differential, property, metamorphic, adversarial, or mutation check
6. Runtime trace or production-like observation

Prefer focused checks tied to a hypothesis over an untargeted full suite. Distinguish
pre-existing failures, regressions, flaky outcomes, skipped checks, timeouts, and
environment mismatches. Do not hide checks that could not run.

### 8. Synthesize for human use

Answer the question before presenting supporting detail. Use progressive disclosure:

- `30 seconds`: Direct answer, primary path, and largest uncertainty.
- `5 minutes`: Minimal model, contracts or invariants, behavior delta, and risks.
- `Audit`: Evidence ledger, commands, results, contradictions, and unknowns.

Limit the first map to roughly five to seven meaningful components and one to three
representative flows. Provide a five-to-twelve-file reading route in causal or
dependency order, with one reason per file. If the user is learning, finish with
two or three prediction questions that test whether the model transfers.

## Report contract

Return the sections relevant to the selected mode:

1. Direct answer
2. Scope, mode, depth, revision, and base/head when applicable
3. Minimal architecture or execution-flow model
4. Contracts and invariants
5. Evidence ledger
6. Behavioral impact or correctness matrix
7. Risks, contradictions, assumptions, and unknowns
8. Recommended reading route
9. Smallest next verification steps
10. Prediction questions when learning is part of the goal

Use a diagram only when it materially clarifies at least three boundaries, branches,
or state transitions. Do not produce a full repository tree as a substitute for a model.

Phrase correctness conclusions conditionally, for example:

> At revision X in environment Y, evidence supports behavior Z for scenarios A
> and B. Scenario C and external dependency D remain unverified.

Do not output an uncalibrated correctness percentage.

## Completion criteria

Stop when:

- the target question has a supported answer;
- the relevant entry, decisions, state ownership, side effects, and failure path
  are accounted for to the requested depth;
- every material claim has evidence or is explicitly marked unknown;
- verification results and limitations are reproducible; and
- further exploration is unlikely to change the answer materially.

Do not continue exploring merely to appear exhaustive.
