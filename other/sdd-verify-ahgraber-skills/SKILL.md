---
name: sdd-verify
description: |-
  Use when verifying that an implementation matches a change's SDD artifacts. Triggers: "verify", "check implementation", "did I implement everything", "verify the change", "is implementation complete", "check conformance".
---

# SDD Verify

Verify that the implementation satisfies the contracts stated in the change's specs.
Produces a structured report across **six** dimensions (Completeness, Scope, Contract, Coverage, Coherence, Conformance) with three severity levels.

Specs are contracts — property statements about observable state (see `references/sdd-spec-formats.md` § 1).
Scenarios are evidence that samples those contracts, not the contracts themselves (§ 1.5).
`sdd-verify` checks evidence: it confirms that the cited tests and outputs demonstrate each contract claim and cover the claim's input space.
It does not formally prove universal properties — strong claims supported by thin evidence are a risk flag, not a failure.
It does not search for defects beyond the cited evidence.
That search has no stopping point inside verify, so re-runs on unchanged code would keep finding new defects.
Defect search belongs to `code-review` and `security-scan`, which verify offers at the end of every run (Phase 9).

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

Write the report and its findings in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## When to Use

- After completing some or all tasks — check coverage and correctness
- Before running `sdd-sync` — confirm implementation matches the change before syncing specs

## When Not to Use

- No active change exists (`.specs/changes/<name>/` is missing) — the skill is change-scoped; use `sdd-derive` to retrofit specs from existing code instead
- Schema-only validation with no spec context — run the project's schema generation directly and diff
- During implementation itself — use `sdd-apply` to drive work; verify after

## Invocation Notice

- Tell the user when this skill is running: `sdd-verify`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Soft Gate

Before starting, check `.specs/changes/<name>/tasks.md`:

- If `tasks.md` is missing, warn: "No `tasks.md` for this change — completeness check will be skipped."
  Offer to proceed anyway.
- If `tasks.md` exists but no tasks are marked complete, warn: "No completed tasks yet — verify output will be limited."
  Offer to proceed anyway.

## Verification Dimensions

| Dimension        | Question                                           | What to check                                                                                                                                                            |
| ---------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Completeness** | Is everything done?                                | All tasks checked off, all delta spec requirements implemented                                                                                                           |
| **Scope**        | Is everything in scope, and no more?               | Every meaningful code change traces to a requirement; every requirement and change traces up to a user story; no unspecified behavior and no value-less over-engineering |
| **Contract**     | Does the implementation satisfy the spec contract? | Cited evidence demonstrates each requirement's scenarios and covers the input space of the claim stated in the text                                                      |
| **Coverage**     | Do scenarios meaningfully sample the contract?     | Scenarios span happy path, boundaries, and plausible failure modes — not trivially-passing cases                                                                         |
| **Coherence**    | Does it follow the design?                         | Implementation follows decisions in `design.md`                                                                                                                          |
| **Conformance**  | Do schemas match the specs?                        | Generated schema diff confirms spec requirements are reflected in the schema                                                                                             |

## Severity Levels

| Level          | Meaning                                                              | Action required            |
| -------------- | -------------------------------------------------------------------- | -------------------------- |
| **CRITICAL**   | Implementation contradicts a requirement or design decision          | Must fix before proceeding |
| **WARNING**    | Implementation partially meets a requirement or deviates from design | Should address             |
| **SUGGESTION** | Minor improvement opportunity                                        | Optional                   |

Severity is not the same thing as sync gating.
A finding can keep its original severity and still be non-blocking when the user explicitly authorizes that exception and it is recorded per `references/sdd-change-formats.md`.

## Evidence Rules

Evidence classification (VERIFIED / TESTED / INSPECTED / WAIVED), the SHALL/INSPECTED → CRITICAL sufficiency rule, the waiver format and provenance check, and the citation format are defined in `references/evidence-rules.md`.
**Read that file before Phase 4** — both the orchestrator and any subagents need it.

In summary:

- **VERIFIED** — externally observable artifact you can re-inspect after the run (response body, schema file, captured output).
- **TESTED** — named, passing automated test from this verify run's suite.
- **INSPECTED** — no execution evidence; static reading only.
- **WAIVED** — `design.md` § Verification Waivers entry with checkable manual evidence.

Hard rule: **SHALL at INSPECTED → CRITICAL** unless waived.
Static reading is never sufficient for a SHALL.

Verification overrides are separate from waivers:

- **Waiver** — evidence exception for a requirement with manual evidence.
- **Override** — audit-tracked permission to proceed despite a known blocking finding or gate outcome.

Overrides never change severity; they only affect blocking status.
Use them to preserve decision continuity, not to erase or reclassify findings.

## Parallel Subagent Path

Phases 4–6 (Evidence, Contract, Coverage) SHALL be evaluated against the parallel-subagent gate before Phase 3 begins.
Single-agent execution is permitted only when the gate routes you there — it is not the default.

The gate evaluation runs as a required step within Phase 2.
The full availability gate, granularity proposal, model resolution, dispatch protocol, and synthesis steps live in `references/parallel-subagent-path.md`.

## Process

### Phase 1: Load Artifacts

Read all available artifacts (graceful degradation — proceed with what exists):

- `.specs/changes/<name>/tasks.md` — task completion status
- `.specs/changes/<name>/proposal.md` — user stories, scope, and any `## Resolved Questions`
- `.specs/changes/<name>/design.md` — design decisions and any `## Spec Changes` / `## Verification Waivers` / `## Verification Overrides` (if exists)
- `.specs/changes/<name>/specs/` — delta specs (if exist)
- `.specs/specs/` — baseline specs for full context

### Phase 2: Run Test Suite and Capture Results

Run the project's full test suite before any other checks.
Verification claims rest on observed behavior, so a green suite is the baseline evidence that the implementation actually works.

1. **Discover the test command** by checking, in order:

   - Project contributor docs: `CONTRIBUTING.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`.
   - Build manifests: `Makefile` targets, `package.json` `scripts.test`, `pyproject.toml` `[tool.pytest.ini_options]` or `[tool.poetry.scripts]`, `tox.ini`, `noxfile.py`, `Cargo.toml`.
   - CI config: `.github/workflows/*test*.yml`, `.gitlab-ci.yml`.
   - If still ambiguous, ask the user once and remember the answer for the rest of the run.

2. **Run the full suite with per-test-ID output** — do not narrow to changed files or a single test path.
   Subagents confirm citations by searching the log for individual test names, so the output must show each test's pass/fail status by name.
   Common flags: `pytest -v`, `jest --verbose`, `go test -v`, `nox -- -v`.
   For machine-readable output use `pytest --junit-xml=<path>` and point subagents at the XML.
   If the runner cannot produce per-test-ID output, treat all requirements as INSPECTED and note this as a WARNING.
   Capture the output to `.specs/changes/<name>/.verify/test-output.log`.
   `.verify/` is transient run scratch — the first time you create it, write a `.gitignore` containing a single `*` into the directory so the whole thing stays out of git and out of the archive (see the router's **Directory Convention**).

3. **If any tests fail or error**, flag each failure as CRITICAL in the report and **stop the verify run by default** — do not proceed to later phases.
   A failing suite invalidates Contract, Coverage, and Coherence conclusions, and there is no reliable way to localize "affected area" without a test→requirement map.
   Re-run after fixes.

   If the user explicitly says they already know about the failing suite and wants to proceed anyway, continue only in a **failing-suite override** mode:

   - Keep every test failure at its original severity in the report.
   - Record that the remaining phases are diagnostic only, not a clean verification pass.
   - Before recommending `sdd-sync`, record the exception per `references/sdd-change-formats.md` and ensure `tasks.md` contains an unchecked remediation task.
   - Never conclude "all applicable dimensions verified" or otherwise present the run as fully passing.
   - The parallel-subagent gate step handles whether subagent dispatch is allowed under override; do not decide that here.

4. **If the project has no runnable test suite**, note this as a WARNING and continue — every requirement will land at INSPECTED at best.

5. **Do not modify, skip, or `xfail` tests to make the suite pass** — that is itself a CRITICAL finding.

#### Evaluate Parallel-Subagent Gate

You SHALL run this gate after Phase 2 and before Phase 3.
Single-agent execution is allowed only when the gate routes you there.

Checklist — do all four:

1. **Read** `references/parallel-subagent-path.md` § 1 (Availability Gate) and § 2 (Granularity).

2. **Count** delta spec requirements across all in-scope capabilities.

3. **Apply** the gate table in § 1 (first match wins) to determine the path.

4. **Announce** the outcome to the user using this template, then wait for confirmation if parallel:

   ```text
   Parallel gate: <N> requirements across <K> capabilities.
   Path: <single-agent | parallel> — <reason from gate table row>.
   <If parallel:> Proposing <P> subagents at <per-capability | per-requirement> granularity. Confirm or override.
   ```

If the gate sends you to single-agent, proceed to Phase 3 yourself.
If the gate sends you to parallel, wait for user confirmation, then resolve model and dispatch per `references/parallel-subagent-path.md` §§ 3–4.
These dispatch and gating rules are purpose-built for SDD verification and take precedence over any general subagent skill (e.g. `subagent-patterns`) when verifying an SDD change.

**Failing-suite override and the gate.**
The gate table in `references/parallel-subagent-path.md` § 1 already partitions failing-suite states (rows 2 and 3): parallel dispatch is allowed under override only when the dispatch inputs explicitly carry the override state and the known overridden blockers; otherwise the gate routes to single-agent.
Apply that table — do not improvise a separate decision here.

**Audit rule.**
If no gate-outcome announcement appears in the run, the gate was not evaluated and the next phase must not begin.

### Phase 3: Generate Schema Snapshot (if schemas configured)

If `.specs/.sdd/schema-config.yaml` exists, regenerate "after" snapshots **now**, before evidence classification, so the schema diff is available as VERIFIED evidence in Phase 4.

1. Generate snapshots into `.specs/changes/<name>/schemas/after/`.
2. Compute the before→after diff and store the diff path for Phase 4 and Phase 7 to consume.

If no schema config exists, skip silently.
Phase 7 is where the diff is interpreted against the spec; this phase only produces the artifact.

### Phase 4: Check Completeness and Evidence

This is the first per-requirement phase — eligible for subagent dispatch (see `references/parallel-subagent-path.md`).

1. Count checked tasks vs. total tasks in `tasks.md`.
2. For each delta spec requirement, verify a corresponding implementation exists in the codebase.
   Flag missing implementations as CRITICAL (SHALL) or WARNING (SHOULD/MAY).
3. For each implemented requirement, identify and **cite** the strongest available evidence per `references/evidence-rules.md` §§ 1, 3, 5:
   - **VERIFIED** — name the integration/e2e test that ran in Phase 2 with its captured output, the schema diff from Phase 3, or the captured command output.
   - **TESTED** — name the unit-level test from Phase 2 that exercises the requirement.
   - **INSPECTED** — record this only when no executable evidence exists.
4. Apply the **Evidence sufficiency rule** (`evidence-rules.md` § 2):
   - SHALL at INSPECTED → CRITICAL, unless waived in `design.md` (then WAIVED, subject to the provenance check in § 4).
   - SHOULD at INSPECTED → WARNING.
   - MAY at INSPECTED → no automatic finding.
5. If a citation cannot be resolved (named test does not exist in the captured Phase 2 output, output path is missing, schema diff is empty when one was expected), the requirement falls back to INSPECTED.

If Phase 2 is in failing-suite override mode, passing tests from that run may still be cited for requirement-local evidence, but the report must state that the overall suite is failing and that downstream conclusions are advisory.

The output of this phase is a per-requirement evidence table that drives Phase 5 and the final report.
On the parallel path, the orchestrator assembles this table from subagent findings during synthesis.

#### Enumerate Write-Sites (orchestrator only)

Cross-cutting search work — runs at the orchestrator regardless of single-agent vs. parallel path.
Subagents do not enumerate write-sites; they consume the enumeration as a dispatch input.

For each **ADDED or MODIFIED universal SHALL** in scope, produce a list of **contract-relevant write-sites** — code locations that produce or modify the value the SHALL is over.
See `references/sdd-change-formats.md` § 3.1 for the definition and heuristic.

Procedure:

1. Identify the contract-asserted value(s) named in the requirement (a persisted field, a response shape, an emitted event, etc.).
2. Search the codebase for every code location that writes or modifies that value — use Grep, the structural graph if available (e.g., `code-review-graph` `query_graph_tool`), or repeated reads.
3. **Scope rule.**
   For ADDED requirements, every located write-site is in scope (all are new behavior).
   For MODIFIED requirements, in scope is the union of (a) write-sites touched by the change diff and (b) pre-existing write-sites the modified contract now applies to — even if the change diff didn't touch them.
   Untouched legacy code is exactly where this rule earns its keep; do not narrow enumeration to the diff.
4. Filter out non-contract-relevant locations per the heuristic (internal helpers that don't produce contract-asserted state, pure transformations consumed by exactly one canonical writer, instrumentation-only calls).
5. Record the enumeration as `requirement → [write-site path:line, …]`.

The enumeration is the orchestrator's responsibility because:

- It is cross-cutting (often spans files outside the change diff for MODIFIED).
- It needs full tooling (Grep, graph search, repeated reads) that the per-requirement subagent context shouldn't carry.
- Centralizing avoids subagents re-running the same search and improvising scope.

The enumeration feeds Phase 5 step 4 directly, and on the parallel path it is passed verbatim to subagents in the dispatch prompt under **Implementation write-sites in scope**.

If a SHALL is not universal (narrow shape, no input-space partitions) skip enumeration — single-site requirements don't need this check.

#### Check Scope (Unspecified Changes)

This is the inverse of Phase 4 (Completeness): for each meaningful code change, check whether a delta spec requirement covers it.
It runs at the orchestrator regardless of single-agent vs. parallel path — subagents do not run this phase.

1. **Get the code diff** for this change:

   - Run `git diff <base-branch>...HEAD` (or `git diff HEAD~1..HEAD` if a single commit), capturing meaningful changes only.
   - If no git context is available, enumerate all files touched by the change from `tasks.md` references or the user.

2. **Identify meaningful changes** — changes that alter observable behavior:

   - New functions, methods, classes, endpoints, or public APIs.
   - Modified control flow, conditionals, or return values.
   - Removed or renamed public interfaces.
   - Schema or data model changes not already caught by Phase 3.
   - Skip: formatting-only edits, comment edits, variable renames with no behavioral effect, and test file changes (test coverage is a separate concern).

3. **Classify each meaningful change** into one of three categories:

   - **In scope** — a delta spec requirement explicitly covers the behavior the change introduces or modifies.
   - **Related** — no delta spec requirement covers it, but it touches behavior governed by a baseline spec requirement; the change is adjacent to the spec'd work but wasn't pulled into scope.
   - **Unspecified** — no spec coverage at all, neither delta nor baseline; the change introduces or modifies behavior the spec system has no record of.

4. **Flag related and unspecified changes by severity**:

   - **CRITICAL**: unspecified change introduces or modifies a public API, external contract, or persisted schema.
   - **WARNING**: related change (silently modifies baseline-governed behavior without a delta requirement) or unspecified change that alters internal logic, control flow, or error handling.
   - **SUGGESTION**: related or unspecified minor defensive change, refactor, or cleanup that is low-risk.

   In-scope changes require no finding — omit them from the report.

5. Record the scope map — which changes are covered and by which requirement — so Phase 9 can include it in the report.
   A change that is fully covered need not be mentioned; only unspecified changes appear in the report.

6. If no git diff is available and file enumeration is also impossible, note this as a WARNING and skip the scope check.

#### Check Value Alignment (story ceiling)

This is the value-side of the scope check.
SDD's other dimensions confirm _contract_ conformance but never _value_ conformance, so over-engineering that satisfies a contract no user needs passes silently.
This check is the counterweight.
It runs at the orchestrator, is change-diff-scoped (never baseline-wide), and its findings are **WARNING** by default — advisory, non-blocking.

Graceful degradation: if `.specs/changes/<name>/proposal.md` has no `## User Stories` section, or `.specs/NORTH-STAR.md` is absent, note this in the report and skip the check — there is no value referent to check against.

1. Read the proposal's user stories and `.specs/NORTH-STAR.md`.
2. **Orphan requirements.**
   For each in-scope delta requirement, check for a `Serves:` backlink to a declared story.
   A requirement that serves no story is suspected over-engineering — flag **WARNING: requirement `<name>` serves no user story (possible gold-plating) — confirm it advances product value or cut it.**
3. **Orphan implementation.**
   For each meaningful code change the scope check classified _unspecified_, additionally note when it also traces to no story — the implementation-side of the same smell.
4. **Story laddering.**
   Check that each declared story ladders to the product north star.
   A story with no connection to `NORTH-STAR.md` is drift from product intent — flag **WARNING: story `<slug>` does not ladder to the north star.**

These are WARNING-level findings, not gates: a requirement may legitimately serve product value diffusely (shared infrastructure), so the finding prompts a confirmation rather than blocking.

#### Check MODIFIED Delta Integrity (pre-sync safety)

`sdd-sync` replaces each MODIFIED requirement wholesale, so any baseline scenario or sub-clause the delta block omits is silently deleted at sync.
This check is the gate that catches that loss before sync; it runs at the orchestrator regardless of single-agent vs. parallel path.

For each MODIFIED requirement in the delta specs:

1. Load the matching baseline requirement from `.specs/specs/<capability>/spec.md` (same capability directory, same requirement name).
2. Compare the baseline's scenarios and sub-clauses against the MODIFIED delta block.
3. If the delta omits a baseline scenario or sub-clause **and** the change does not deliberately remove it (no rationale in `design.md`), flag **WARNING: MODIFIED `<name>` delta drops baseline scenario `<scenario>` — `sdd-sync` will delete it from the baseline.**
   **Restore the full post-change requirement (`references/sdd-spec-formats.md` § 4) or document the removal in `design.md`.**

A delta requirement with no matching baseline requirement is ADDED or RENAMED, not MODIFIED — out of scope for this check.

For a deterministic backstop on the **scenario** part of this check, run `scripts/check_modified_completeness.py <specs-root> --change <name>` — scoped to the change under verification, matching the `sdd-sync` guard so an unrelated active change cannot fail this one.
Omit `--change` to scan every active change, e.g. as a repo-wide pre-commit/CI gate that runs without an agent.
It compares scenario names only and exits non-zero when the MODIFIED delta drops a baseline scenario; sub-clause and body-text loss (step 2) still needs a human read.
Intentional drops are marked with a `<!-- modified-removes: ScenarioName -->` comment in the delta block.

#### Check Spec Changes (spec-drift check)

Specs may change during implementation only with the record `references/sdd-change-formats.md` § 5 requires.
This check finds spec edits that lack that record.
It runs at the orchestrator.

Run the spec-drift check in § 5.5: diff the delta specs from the proposal commit to the working tree, and classify each hunk as a scenario change or a requirement change.

- A scenario change with no `design.md` § Spec Changes entry, or with `Approved by user: pending` → **CRITICAL: scenario change `<capability>: <scenario>` has no recorded user approval.**
- A requirement change with no `design.md` Decision entry or no dated Resolved Questions line → **CRITICAL: requirement change `<capability>: <requirement>` was not approved by the user.**
- A scenario change that narrows what its requirement guarantees but is recorded only as a scenario change → **CRITICAL: `<capability>: <scenario>` narrows its requirement and needs approval as a requirement change.**
- A requirement change that narrows its requirement, whose Decision entry does not state the behavior the narrowing gives up (`references/sdd-change-formats.md` § 5.2) → **CRITICAL: `<capability>: <requirement>` narrows its requirement without stating the behavior it gives up.**
- A § Spec Changes entry whose rationale is only that the code behaves this way → **WARNING: `<capability>: <scenario>` is supported only by the code it describes.**
- A hunk whose only change replaces one internal method, symbol, or span name with another → **WARNING: `<capability>: <requirement>` pins a call path; state the outcome instead (`references/sdd-spec-formats.md` § 1.4).**

If no proposal commit exists, flag **WARNING: no proposal commit; the spec-drift check could not run** and do not report a clean pass.

### Phase 5: Check Contract Satisfaction

Skip requirements flagged as missing in Phase 4.
For each requirement at TESTED or VERIFIED tier, confirm the cited evidence actually demonstrates the contract claim — do not just trust the test name.
INSPECTED-tier requirements are not contract-checked here; their tier already determined the finding in Phase 4.

If Phase 2 is in failing-suite override mode, Contract findings are still useful for triage, but they do not clear the change for release or sync.

For each implemented requirement at TESTED or VERIFIED:

1. Read the requirement text — this is the **contract claim** (`references/sdd-spec-formats.md` § 1).
2. Read the delta spec scenarios — concrete **evidence** sampling the claim.
3. Inspect the cited test or output to verify each scenario holds in the executed evidence (not just in the source code).
4. **For universal SHALL claims** (ADDED or MODIFIED), use the write-site enumeration produced in Phase 4.
   For each enumerated write-site, check the test execution log for at least one cited test that exercises the contract _through that site_ — not just through the canonical path.
   If a write-site has no covering test in the log, flag **CRITICAL: partition-incomplete evidence — write-site `<path:line>` for SHALL `<name>` has no test coverage.**
   A passing test on one path is not evidence for a deduplication shortcut, retry branch, or composition step that writes the same value.
5. **Check that the evidence covers the claim's input space.**
   For each universal SHALL, compare the inputs the claim quantifies over with the inputs the cited evidence exercises: the write-sites from step 4, the partitions (`references/sdd-spec-formats.md` § 1.6), and generated evidence (§ 1.7).
   For example, a requirement that says "for any query satisfying C, the system SHALL return no relevant results" is not demonstrated by tests that use only the scenario queries.
   When § 1.7 says the claim needs generated evidence and the evidence is example tests only, flag **WARNING: `<name>` quantifies over `<input space>`, but its evidence samples only `<what the tests exercise>` — add a property or differential test, or use the `formal-verification` skill.**
   Read only the cited evidence, the enumerated write-sites, and the code they exercise.
   Do not construct new inputs, write probe scripts, or list edges to probe; that is defect search, and the Phase 9 review handoff owns it.
6. Flag deviations as CRITICAL (the evidence or code read in this phase contradicts the requirement or a scenario, or a write-site lacks evidence) or WARNING (partially meets the requirement, or the evidence does not cover the claim's input space).

### Phase 6: Check Scenario Coverage

For each requirement, assess whether its scenarios meaningfully sample the contract claim.
This is a coverage heuristic, not a formal check — it guards against requirements whose scenarios are too thin to catch a plausible failure.

If Phase 2 is in failing-suite override mode, label Coverage conclusions as provisional because the suite is already known red.

Coverage smells to flag as WARNING:

- **Happy-path only** — every scenario describes a well-formed, success-bound case.
  Missing boundary or adversarial cases.
- **No precondition variation** — all scenarios share essentially the same GIVEN.
  Fails to exercise different parts of the input space.
- **Scenarios restate the requirement** — the scenario adds no information beyond the requirement text.
  No independent test value.
- **Universal claim, single scenario** — the requirement states a property over a class of inputs ("for any X", "whenever Y"), but only one scenario is provided _and_ the partition heuristic does not flag any positive signal.
  This is a quantitative concern: the input space may be uniform but the sample size is one.
- **Partition-incomplete coverage** — apply the partition heuristic in `references/sdd-spec-formats.md` § 1.6.
  When a positive signal fires (lifecycle states, identity/equivalence, multi-source composition, derived-pair invariant) but scenarios cover only some partitions of the input space, flag this distinct from "single scenario."
  This is a qualitative concern: the input space partitions into named arms and only some are sampled.
  Example: a SHALL with identity/equivalence semantics whose only scenario covers `(novel input)` and never `(equivalent-to-existing input)` — partition-incomplete, even if multiple scenarios are present.

Flag as SUGGESTION (not WARNING) if the requirement is genuinely narrow and a single scenario is adequate (e.g., "the response Content-Type SHALL be `application/json`").

### Phase 7: Check Conformance (if schemas configured)

If Phase 3 produced a schema diff:

1. **Schema-vs-schema diff** (before → after) — what was added, modified, removed?
   Does this align with `schemas/expected.md` (if present)?
2. **Schema-vs-spec cross-check**:
   - ADDED requirements describing API or data shapes: does the schema confirm the change?
     Flag as CRITICAL if missing.
   - REMOVED requirements: is the corresponding schema element actually gone?
     Flag as WARNING if still present.
   - MODIFIED requirements: does the schema change match the new behavior?
3. **Drift detection** — schema changes with no corresponding spec requirement: flag as WARNING ("Schema shows new `<field/endpoint>` — not covered by any requirement").
4. **Authored schema check** — if the repo contains a committed authored schema (e.g., a hand-maintained `openapi.yaml`), diff it against the newly generated snapshot.
   Flag genuine divergences as WARNING; tolerate documented additions (e.g., vendor extensions, computed fields) noted in `design.md`.

If `schemas/expected.md` exists but Phase 3 was skipped (no `schema-config.yaml`), note this in the report — the user expected schema tracking but it was not configured.

### Phase 8: Check Coherence

If `design.md` exists:

1. For each decision in `design.md`, verify the implementation follows it via static reading.
2. Flag deviations as CRITICAL (contradicts an explicit decision) or WARNING (diverges without documentation).

If Phase 2 is in failing-suite override mode, Coherence findings remain worth reporting, but they do not outweigh the CRITICAL failing-suite status.

Coherence findings are static reads by design — `design.md` records HOW choices, not external contracts, so the evidence-tier rule does not apply here.
A decision either is or is not reflected in code; if the decision needs runtime confirmation, it should have been promoted to a spec requirement.

### Phase 9: Produce Report

The report is a derived snapshot, not a committed artifact.
Present it in chat.
If you persist it, write it to `.specs/changes/<name>/.verify/report.md` — the transient, self-gitignored zone created in Phase 2 — never the change root, where it would be committed and travel into the archive as if it were a source of truth.
A committed report goes stale the moment code or specs move.
Its durable consequences do not live in the report: waivers and overrides are recorded in `design.md`, and remediation tasks in `tasks.md` (both committed).
The report only echoes them.

Before writing the Summary, classify blocking status:

- Any finding or gate outcome the skill says "must fix before proceeding," "stop," or "blocked" is **blocking** by default.
- A blocking finding or gate outcome becomes **non-blocking for sync** only when a matching override is recorded per `references/sdd-change-formats.md`.
- Chat-only instructions are not sufficient once the report is finalized; the override must be written into the change artifacts.

For each entry in `design.md § Verification Overrides`, carry the audit record into the report:

- Echo the finding, stage, reason, constraints, follow-up task, approved-by value, and recorded value.
- If this verify run is proceeding under an override, the Summary must make that intervention explicit so later stages can recover the decision context without rereading the whole conversation.

```markdown
# Verification Report: {Change Name}

**Date:** {date} **Tasks:** {N}/{M} complete

## Evidence

| Requirement | Level (SHALL/SHOULD/MAY) | Tier (VERIFIED/TESTED/INSPECTED/WAIVED) | Citation                                   |
| ----------- | ------------------------ | --------------------------------------- | ------------------------------------------ |
| {name}      | SHALL                    | TESTED                                  | `tests/path::test_name`                    |
| {name}      | SHALL                    | WAIVED                                  | design.md § Verification Waivers → {ref}   |
| {name}      | SHOULD                   | INSPECTED                               | (no executable evidence — flagged WARNING) |

## CRITICAL

- {Description of issue} — {file:line or area}

## WARNING

- {Description of issue}

## SUGGESTION

- {Description of improvement}

## WAIVED

- {Requirement} — manual evidence: {reference} (per design.md § Verification Waivers; provenance: {predates change | added during implementation | added after verify failure})

## OVERRIDES

- {blocking finding or gate outcome} — stage: {stage}; reason: {reason}; constraints: {constraints}; follow-up: {tasks.md task text}; approved by: {approved by}; recorded: {recorded}

## SCOPE

- {Change description} — {file:line} · {related | unspecified} (CRITICAL/WARNING/SUGGESTION)

## CONFORMANCE

- [x] {What schema confirmed} — {requirement name}
- [ ] {What schema did not confirm} — {requirement name} (CRITICAL/WARNING)

## Summary

{1-2 sentences on overall status and recommended next step}
```

Omit empty sections (e.g., omit CONFORMANCE if no schema config exists; omit WAIVED if no waivers apply).

If Phase 2 proceeded under a failing-suite override, the Summary must say so explicitly and recommend fixing or isolating the failing tests before treating the verify run as complete.
If any blocking findings are overridden for sync, the Summary must say that the run is not a clean pass and that `sdd-sync` is permitted only under the recorded overrides.

If no issues found:

```text
All applicable dimensions verified:
- [x] Completeness
- [x] Scope
- [x] Contract
- [x] Coverage
- [x] Coherence (if design.md exists)
- [x] Spec changes — every spec edit since the proposal commit has its recorded user approval
- [x] Conformance (if schema-config.yaml exists)
- [x] Evidence — every SHALL at TESTED or VERIFIED (or WAIVED with checkable manual evidence)

Ready for `sdd-sync`.
```

Only include checklist items for dimensions that actually applied — match what's in the report.

If the run has no remaining blockers but does include overrides, do not use the clean-pass template above.
State instead that verification found issues the user explicitly chose not to let block sync, and that remediation remains open in `tasks.md`.

#### Offer the Review Handoff

Verify checks evidence; it does not search for defects.
After the report, on every run, offer `code-review` in one line.
When the change touches a security boundary, also offer `security-scan`.
A change touches a security boundary when it parses or classifies untrusted input, makes an authorization, sandbox, or policy decision, or handles secrets or credentials.

For each skill you offer, state what you will pass to it:

- The change's delta specs and `design.md` as the source of truth (for `code-review`, through `build_review_packet.py --include`).
- The universal SHALL claims this run flagged because their evidence does not cover their input space, as the areas to examine first.

Run neither skill without the user's approval.
If the user declines, end the run.
A clean verify report states that the evidence covers the claims; do not present it as a finding that the code has no defects.

## Graceful Degradation

| Missing artifact                  | Behavior                                                                  |
| --------------------------------- | ------------------------------------------------------------------------- |
| `tasks.md`                        | Skip completeness check, warn before proceeding                           |
| `design.md`                       | Skip coherence check and waiver lookups, note in report                   |
| Delta specs                       | Skip contract and coverage checks, note in report                         |
| `schema-config.yaml`              | Skip Phase 3 snapshot and Phase 7 conformance check, note in report       |
| `schemas/expected.md`             | Skip expected-vs-actual diff within conformance; run drift detection only |
| No git diff available             | Skip scope check (Phase 4 step), flag as WARNING, note in report          |
| No user stories / `NORTH-STAR.md` | Skip value-alignment check (Phase 4 step), note in report                 |
| No proposal commit                | Skip spec-drift check (Phase 4 step), flag as WARNING, no clean pass      |

"Warn before proceeding" means a conversational message to the user.
"Note in report" means adding a note inside the verification report itself.

## Common Mistakes

- Skipping the full test suite, narrowing to changed files only, or trusting a prior local run instead of executing it now — verification rests on observed behavior, so the suite must run as part of this skill.
- Not capturing test output to disk in Phase 2 — without the captured log, evidence citations have nothing to point at.
- Treating SUGGESTION-level issues as blockers, or treating coverage smells as CRITICAL.
- Skipping graceful degradation — running verify is valid even with incomplete artifacts.
- Not reading baseline specs for full behavioral context.
- Checking only that scenarios pass, not whether the evidence covers the claim's input space (`references/sdd-spec-formats.md` § 1.5 — scenarios are evidence, not definition).
- Searching for defects beyond the cited evidence: constructing inputs, writing probe scripts, or adding edges to probe or prior-run findings to subagent prompts.
  That search has no stopping point, and each run's coverage then depends on what the orchestrator wrote, so re-runs on unchanged code keep finding new defects and verify never converges.
  Report thin evidence as a WARNING and offer the review handoff (Phase 9) instead.
- Skipping write-site enumeration (the orchestrator step within Phase 4) for ADDED or MODIFIED universal SHALL claims — a passing test on the canonical path is not evidence for a deduplication shortcut, retry branch, or composition step that writes the same contract-asserted value.
- Narrowing write-site enumeration to the change diff for MODIFIED requirements — pre-existing legacy write-sites the modified contract now applies to are exactly the ones least likely to appear in the diff, and they need coverage too.
- Pushing write-site enumeration into subagents — subagents operate per-requirement; cross-cutting search is orchestrator work and belongs in Phase 4's enumeration step.
  Subagents consume the enumeration as a dispatch input.
- Treating partition-incomplete coverage as identical to "single scenario."
  They are distinct: one is a quantitative concern (sample size of one), the other is qualitative (named partitions exist, only some are sampled).
- Marking a requirement VERIFIED or TESTED without a checkable citation, or accepting a waiver without checkable manual evidence — both fall back to INSPECTED / CRITICAL per `evidence-rules.md`.
- Skipping the waiver provenance check (`evidence-rules.md` § 4) — waivers added in the same branch as the implementation, especially after a failed verify, need to be surfaced.
- Recording an override in `design.md` but failing to carry its context into the OVERRIDES section or Summary, which breaks the audit trail for later verify/sync work.
- Persisting the verification report into the committed change directory (or anywhere but `.verify/`) — it is a derived snapshot that goes stale the moment code or specs move; write it only to the transient, self-gitignored `.verify/`, and rely on `design.md`/`tasks.md` for the durable record.
- Treating an override as a severity downgrade, or honoring a chat-only override without recording it in `design.md` and `tasks.md`.
- Proceeding to Phase 3 without evaluating the parallel-subagent gate (the required step within Phase 2) — the gate is mandatory; if no gate-outcome announcement appears in the run, you skipped it.
  Single-agent execution is a gate result, not a default.
- On the parallel path: re-running per-requirement phases on the orchestrator, mixing granularities, dispatching above the concurrency cap, or silently defaulting the model — see `references/parallel-subagent-path.md` § 6.
- Skipping the scope check (the step within Phase 4) — completeness alone is not sufficient; the inverse direction (code → spec) is equally important and catches scope creep and accidental behavioral side-effects.
- Skipping the value-alignment check (the step within Phase 4) — without it, verify confirms contract conformance but never catches value-less over-engineering, the gold-plating this dimension exists to flag.
- Treating an orphan-requirement finding (serves no story) as CRITICAL — it is a WARNING by default; a requirement may serve product value diffusely, so the finding prompts confirmation, not a block.
- Running the scope check only against the delta specs without also checking baseline specs — a change that silently modifies behavior already covered by a baseline requirement is still unspecified for this change.
- Skipping the MODIFIED delta-integrity check (the orchestrator step within Phase 4) — `sdd-sync` replaces MODIFIED requirements wholesale, so a delta block that drops a baseline scenario causes silent contract deletion at sync; verify is the gate that catches it first.
- Classifying test file changes or formatting-only edits as meaningful changes in the scope check step — the scope check targets behavioral changes, not every diff hunk.
- Skipping the spec-drift check (the orchestrator step within Phase 4), or accepting a spec edit because its rationale sounds reasonable when the user approval line is missing.
- Reporting a clean pass when no proposal commit exists — the spec-drift check did not run, so spec edits made during implementation are unchecked.

## References

- `references/evidence-rules.md` — tiers, sufficiency rule, waivers, provenance check, citation format
- `references/parallel-subagent-path.md` — availability gate, granularity, dispatch, synthesis
- `references/verify-subagent.md` — canonical job description for subagents on the parallel path
- `references/sdd-spec-formats.md` — contract shapes (§ 1.1), scenarios as evidence (§ 1.5), partition heuristic (§ 1.6), claims that need generated evidence (§ 1.7)
- `references/sdd-change-formats.md` — task format (§ 3) and contract-relevant write-site definition (§ 3.1)
- `references/sdd-schema.md` — schema evidence annotations (§ 1) and lifecycle policy (§ 4)
- `scripts/check_modified_completeness.py` — deterministic dropped-scenario check (scenario names only, not body sub-clauses); exits non-zero on dropped baseline scenarios, wireable as a pre-commit/CI gate
