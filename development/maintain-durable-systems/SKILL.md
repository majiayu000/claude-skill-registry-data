---
name: maintain-durable-systems
description: Maintain, debug, design, refactor, or release software and configuration systems with search-first discovery, semantic DRY, architecture reuse, test-driven changes, safe lifecycle handling, cross-surface contracts, and verified time/memory/latency costs. Use when asked to "fix a regression", "design an API", "improve performance", "change installation or configuration", make a maintainer plan, or audit release readiness.
license: Apache-2.0
---

# Maintain Durable Systems

<purpose>

Make the smallest coherent change that solves the real workflow while preserving correctness,
recoverability, usability, compatibility, and resource efficiency.

</purpose>

<requirements>

## P0 operating contract

1. **DURABLE-REQ001-explore-before-change.** Search guidance, docs, source, tests, TODOs, history,
   prior work, and live behavior before judging the design. Verify exact source after structural
   discovery.
2. **DURABLE-REQ002-map-semantic-ownership.** Trace data flow and identify who owns parsing, normalization,
   defaults, precedence, validation, ordering, paging, presentation, persistence, lifecycle, and
   cleanup across every affected surface.
3. **DURABLE-REQ003-reuse-or-improve-architecture.** Start at the strongest existing seam.
   Support the existing architecture or better when evidence warrants; do not add a parallel
   facade, parser, config path, cache, or policy owner.
4. **DURABLE-REQ004-eliminate-semantic-duplication.** Apply DRY principles to duplicated meaning, not only similar
   text. Keep one authority for each co-loaded contract and let adapters translate syntax or
   deliberate surface policy. Preserve essential repetition when independently loaded skills,
   errors, or documents will not have the authoritative copy in view.
5. **DURABLE-REQ005-optimize-the-whole-outcome.** Improve or preserve correctness, task completion, ease of use,
   latency, throughput, peak and retained memory, allocation/copy volume, I/O, output size, cost,
   compatibility, maintainability, recovery, and user time together.
6. **DURABLE-REQ006-make-correct-use-easy.** Make the system easy to use correctly and hard to use incorrectly. Make it automatic and
   correct when safe intent is unambiguous, match users' existing mental models, solve problems for
   users, and provide the necessary context and guidance when it cannot solve a problem itself.
7. **DURABLE-REQ007-preserve-cross-surface-intent.** Keep shared semantics consistent across core APIs, language
   bindings, CLI, services/protocols, config, schemas, docs, and installed behavior. Name, justify,
   and test every deliberate difference caused by audience or transport.
8. **DURABLE-REQ008-protect-complexity-and-performance.** State present and worst-case runtime,
   memory, and latency bounds. Also inspect throughput, allocations, copies, I/O amplification,
   locks, concurrency, startup, output growth, failure cleanup, and cancellation.
9. **DURABLE-REQ009-verify-changes-test-first.** For behavior changes, reproduce the defect, add the
   smallest failing shared-layer test, confirm its reason, implement one coherent change, and cover
   every affected boundary with durable tests. For non-code work, define a failing acceptance check
   or concrete completion proof before editing.
10. **DURABLE-REQ010-plan-fine-grained-work.** Order tasks by dependency and give each a concrete
    outcome, evidence, implementation scope, verification, and honest completion, deferral, or
    external-action state.
11. **DURABLE-REQ011-preserve-user-state.** Protect source data, configuration, manual edits, unrelated work, and
    recovery paths. Mutate or remove only exact targets whose ownership and authority are proven.
12. **DURABLE-REQ012-automate-knowable-work.** Make safe, knowable work programmatic and
    automatic. Provide manual instructions only as an absolute last resort, with exact state,
    rationale, and an actionable next step.
13. **DURABLE-REQ013-preserve-the-useful-superset.** Consolidate files, commands,
    types, and workflows only when the result retains or improves every required capability. Prove
    current-to-target coverage before deleting or replacing anything.
14. **DURABLE-REQ014-make-long-work-resumable.** For long or multi-stage workflows, persist
   machine-readable state, reload it on rerun, support the whole workflow and meaningful
   individual stages, and recover cleanly after interruption or partial failure.
15. **DURABLE-REQ015-separate-questions-from-decisions.** Keep hypotheses, preferences,
    measurements, and decisions distinct. Use actual data and neutral comparisons until evidence
    justifies a recommendation.
16. **DURABLE-REQ016-keep-requirements-traceable.** For multi-surface or high-risk work, preserve
   each distinct requirement, correction, example, scope boundary, platform, format, and edge case
   in a compact requirement-to-plan-to-test matrix. Do not silently merge away a constraint merely
   because several messages discuss the same feature.
17. **DURABLE-REQ017-invalidate-dependent-work.** When evidence disproves an assumption or a
    plan step changes, identify every dependent decision, task, test, document, and completion claim;
    move affected work back to pending and reverify it rather than patching only the visible error.
18. **DURABLE-REQ018-scale-ceremony-to-risk.** Data safety, user intent, discover-before-change, and
    verification remain mandatory. Use matrices, premortems, benchmarks, multi-pass reviews, and
    multi-agent work only when affected surfaces, uncertainty, reversibility, or scale justify them.
    A small local change should take the fast path: find the owner, reproduce or specify the
    contract, make one tested change, run the focused gate, and report it.
19. **DURABLE-REQ019-reread-plans-after-resumption.** Read every active plan sequentially
    from start to finish again before editing. Then check everything done in the current session
    against the plan's requirements, dependency order, intentional differences, non-goals, tests,
    complexity bounds, and completion gates. A summary or targeted excerpt can restore orientation,
    but it is not a substitute for this end-to-end regression audit.

</requirements>

<workflow>

## Execution workflow

Choose artifact depth before starting. Use the fast path for one-owner, reversible, well-understood
changes with a focused test. Use the full workflow when behavior crosses surfaces, changes public
contracts or persisted state, has uncertain ownership, affects performance/security/lifecycle, or
is difficult to reverse. Escalate from the fast path as soon as evidence reveals those conditions.

### 1. Discover

- Read repository and environment guidance before acting.
- Use structural search for symbols, call paths, and ownership; use literal search for config,
  error text, docs, and incomplete index coverage.
- Inspect relevant history and prior sessions when the task depends on earlier decisions.
- After context compaction or session resumption, reread each active plan end-to-end and reconcile
  all current-session work against it before continuing.
- Reproduce external reports and installed-state claims. Separate requirements, measurements,
  hypotheses, and third-party assertions.
- Read surrounding turns before generalizing a remembered instruction. Deduplicate mirrors,
  delegation prompts, generated envelopes, copied AI output, and terminal-rendered repeats.

Do not design until the current behavior, desired behavior, affected surfaces, existing authority,
and actual failure are explicit.

### 2. Frame the contract

Write down:

- the user outcome and failure mode;
- stakeholders and whose workflow, data, time, or compatibility is affected;
- explicit in-scope and out-of-scope boundaries;
- measurable success criteria and the evidence that will close each one;
- invariants and invalid states;
- input, output, error, cancellation, and cleanup behavior;
- parameter names, types, units, ranges, defaults, precedence, and origins;
- parity expected across surfaces and each intentional difference;
- data ownership, migration, install, update, uninstall, and recovery states;
- current and target resource bounds.
- the zero/minimum-parameter common path, advanced modes, and progressive-disclosure boundary;
- persisted state, rerun, resume, stage selection, interruption, and cleanup behavior.

Prefer orthogonal, typed parameters over booleans or catch-all maps that create conflicting states.
Reject invalid combinations early with actionable errors. Keep retrieval, computation, and
presentation controls independent unless the product contract explicitly couples them.
Make the best common path work with zero or minimal configuration, automatically enable safe
capabilities when their prerequisites are known, and retain explicit advanced controls.

### 3. Select the mechanism

Generate only serious candidates. Compare them against correctness, architecture fit, semantic
ownership, UX, compatibility, lifecycle safety, complexity, observability, testability, and
rollback. Prefer the smallest composable mechanism that extends an existing authority.

Record the selected mechanism, material alternatives, why they lost, and any tradeoff that is not
Pareto-improving. Do not preserve weak alternatives as fake options.

Trace the selected mechanism's data and control flow from input through validation, ownership,
computation, persistence, presentation, errors, cleanup, and recovery. Cite current file paths,
symbols, observed error text, test commands, and primary sources where they make the plan
reproducible. Verify references against current source; label anything not directly checked.

Run a premortem before selection: assume the design failed, list the plausible causal paths, and
trace each through affected code, tests, scripts, docs, configuration, persisted state, and
integrations. Solve the root cause rather than adding a local guard around one symptom.

### 4. Change with TDD

1. Add a focused failing test at the lowest shared owner.
2. Confirm that it fails for the intended reason.
3. Implement one coherent change without unrelated cleanup.
4. Add adapter, serialization, docs/schema, lifecycle, and installed tests wherever affected.
5. Parameterize reusable fixtures and sweep meaningful edges, including empty, zero, one, maximum,
   invalid, interrupted, concurrent, stale, modified, and partial states.
6. Run focused checks before broader gates.

For multi-step implementation, make the task graph mirror causality: each TDD/reproduction task
precedes its implementation task, implementation dependencies are explicit, and final integration
verification depends on every affected surface. If a correction invalidates an earlier premise,
reset the dependent tasks and gates before continuing.

Use synthetic data and temporary roots for general tests. Never let ordinary tests mutate real user
configuration, indexes, sessions, credentials, or manually edited files.
Clean temporary servers, processes, files, and ports by default. Retain them only through an
existing explicit debug control.

### 5. Verify costs and behavior

Complete this table for each hot or scale-sensitive path:

| Criterion | Required statement |
| --- | --- |
| Time | Present and worst-case bound in named input symbols; indexed and fallback paths |
| Memory | Peak and retained bounds; what is materialized; behavior when a limit means all |
| Latency | Cold/warm distribution, startup, locks, network waits, and tail behavior |
| Throughput | Units per second and concurrency assumptions |
| Allocation/copy | Per-row/per-byte clones, serialization, buffering, and avoidable duplication |
| I/O | Files/rows/bytes scanned or written; amplification, fsync, cache, and mmap behavior |
| Output | Result membership versus presentation bytes; paging, streaming, and completeness metadata |
| Lifecycle | Cancellation, rollback, partial failure, cleanup, restart, and resource release |

A small result page does not prove bounded work. A timeout does not repair an inefficient algorithm.
A byte or row limit must name the problem it solves, remain observable, and never silently change
correctness. Compare the same dataset, build, environment, workload, and correctness digest before
and after performance-sensitive changes.

Put computational-complexity comments and docstrings beside the implementation that owns each hot
path. Define every input symbol and state time, peak-memory, retained-memory, I/O, and output-growth
bounds for indexed, fallback, zero/all, error, and cancellation paths where they differ. Keep those
comments synchronized with tests, benchmarks, public schemas, and user-facing documentation.

### 6. Cross-check every surface

Trace the shared contract through core/library APIs, language bindings, CLI, service or protocol
adapters, config, schemas, docs, examples, packaging, and installed behavior. Keep shared semantics
identical while retaining justified differences caused by audience or transport.

For each difference, document the rationale and test both parity and divergence. Keep errors,
nullability, enums, serialization, help, docstrings, and stubs aligned across language boundaries.
Exercise the zero-parameter workflow, every meaningful mode, individual stages, the full end-to-end
path, reruns, resumes, and automatic stage detection.

### 7. Dogfood and critically review

Exercise the real user workflow from a clean or minimally inherited environment. Separate config
discovery, executable resolution, process startup, protocol negotiation, permission, parsing,
retrieval, presentation, and harness failures.

Critically assess AI or reviewer responses because agents often go off the rails and make mistakes.
Check their assumptions, results quality, scope, source freshness, test integrity, and claimed
results directly. Correlated or mirrored reports are not independent votes. Record tool ambiguities
and dogfood failures in the appropriate private evidence log.

### 8. Preserve and hand off

Compare the final work against the original source and a fact inventory. Restore lost mechanisms,
edge cases, state taxonomies, test matrices, UX reasoning, and verification details before removing
duplication. Keep durable docs concise and keep raw evidence separate.

Report exact changed files, tests, measurements, unresolved risks, justified deferrals, and external
actions. Commit only coherent, reviewed, recoverable progress; do not claim release readiness until
the full clean-build and artifact gate passes.

Use current/target capability matrices when several surfaces or mechanisms change. Name what exists,
what remains, what is replaced, the justification, and the verification evidence so a maintainer
can make each decision without reconstructing the investigation.

Before declaring a plan implementation-ready, inventory its sections, goals, code references,
assumptions, dependencies, risks, deferrals, and external actions. Run iterative critique passes
until a complete pass finds no new material issue; stop when it converges rather than enforcing an
arbitrary number of alternatives, best-practice items, subagents, or repeated narration. Finish
with a requirement traceability sweep covering every named use case, edge case, language/platform,
file type/format, and user example.

</workflow>
