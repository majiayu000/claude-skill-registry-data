---
name: ci-suite-audit
description: >-
  Audit registered CI test suites and recommend retention, split, nightly,
  quarantine, or turn-off verdicts based on runtime receipts, failure history,
  touch-set overlap, and prose/junk assertion analysis. Use when an operator asks
  to "audit test suites", "curate CI tests", "find slow tests", "identify redundant tests",
  "review test retention", "evaluate test gate health", or prepare the full-suite audit.
---

# ci-suite-audit — Test Suite Curation & Retention Triage Playbook

A structured, evidence-governed method for evaluating and curating test suites in large CI registries.
It inspects runtime performance, defect and flake history, touch-set overlap, sibling coverage, and
assertion quality (prose and junk checks) to classify test suites into actionable, defensible verdicts.

## Purpose & Mission
The audit exists to reverse test registry expansion (#853: 207 → 419 in 41 days; the GH-854 CI stabilization objective) by proposing KEEP, NIGHTLY, MERGE, QUARANTINE, or TURN-OFF (TURN-OFF means unregister and add to `EXEMPT` or unpin from registry). The skill aggressively curates dead, redundant, prose-only, flake-prone, and unbacked test suites back down to a fast, reliable, regression-focused gate while fiercely protecting verified regression guards. Reports must explicitly state the total count and share of suites proposed to leave the PR gate.

The skill serves as the canonical curation method for full-suite audits (GH-854, GH-862).

---

## Operating Rules & Core Constraints

1. **Manual Invocation Only:** The skill is invoked by an operator for occasional audits (e.g. quarterly sweeps or after major CI churn windows). It is not automated, not scheduled, not wired into CI workflows, and does not run on pull requests.
2. **Text-Only Skill:** Contains instructions and documentation only. No executable scripts live in the skill directory or under `utils/`, `scripts/`, or `bin/`. Any one-off extraction or scoring code needed during an audit belongs in that run's evidence directory (`TESTS-RESULTS/<date>+GH-<n>/`). Scoring code and input tables (failure records, coverage maps, duplicate contracts) must derive every field from saved source artifacts. Hand-typed tables keyed by suite name and name-based verdict branches are forbidden. Code from a previous run may be reused only if it meets the same rule.
3. **Target Branch Requirement:** Run against `development` or the active stabilization staging branch such as `staging/stabilize-2026-10`; record the full 40-character target tip SHA. Another ref requires the operator to name it and the report to explain why. Never audit `main`, which retains obsolete pre-freeze suites and stale registries.
4. **Proposes Verdicts; Humans Decide:** The skill generates structured recommendations with citations and confidence ratings. It **never** directly edits `validate.sh`, `test/`, `utils/ci-route.sh`, or GitHub Actions workflows, never deletes files, and never opens pull requests. Changes to the registry or test files must be reviewed and approved by an operator per verdict class.
5. **Restricted GitHub Writes:** The skill's only permitted GitHub write operations are creating/updating its own dedicated report issue and appending per-turn decision comments on that issue (see *Report Issue & Per-turn Comments*). It never modifies or comments on any other issue or PR.
6. **Freeze & No New Tests Compliance (GH-831):** The skill respects repository test freezes. It introduces no new gate machinery, no new runner scripts, and no new test arrays (`NIGHTLY_TESTS` stays out of tree; candidates remain in `TESTS`). Quarantined suites use the existing unregister-and-exempt mechanism in `test/gh306-registry-bidirectional.sh`.
7. **No Keep-by-Default (Honest Metrics):** Anything not measured is `UNKNOWN`; nothing is estimated silently. There is no default verdict. A row gets `KEEP` only when D2 has an observed execution denominator $N > 0$ for that suite and D3/D5 produced outputs for it. Otherwise the verdict is `INVESTIGATE` and every unmeasured field is `UNKNOWN`. A suite must earn `KEEP` through verified regression catching, unique core contract guarding, or confirmed passing behavioral execution.
8. **Multi-Source Failure Signals:** Collect four sources in a stated window: (1) hosted full-registry job logs, (2) issues labelled `ci`, `stability`, or `bug` that name an exact suite, (3) `fix:`/`hotfix:` commits touching `test/`, and (4) committed receipts with a failing `event:"suite"` record. Record the searched N and window for each source. Only executed runs contribute to a suite's `k of N` denominator; issues and commits provide attribution, not extra runs. Uncommitted local logs are leads, not auditable failure counts.
9. **Exact Entity Matching:** Known flakes, defects, and tracking umbrellas must be matched by exact suite filename or canonical mapping. Loose prefix matching (e.g. `gh492` matching `gh492-roadmap-state-sweep.sh` instead of `gh492-idle-kill.sh`) is strictly prohibited.
10. **Log Evidence Preservation:** Save each downloaded or extracted workflow log, run summary, or receipt into the evidence folder (`TESTS-RESULTS/<date>+GH-<n>/`) the first time it is read.

---

## Pre-Flight Calibration Step (Mandatory Gate)

Before scoring any suites in the active registry, the skill **must** execute a pre-flight calibration test against the 8 known bad suites turned off by operator decision #831 (their files remain on disk):
- `gh578-ci-optimize-skill.sh`
- `gh778-review-code-skill.sh`
- `gh798-status-skill.sh`
- `gh779-radar-ci-health.sh`
- `gh781-wam-radar-seed.sh`
- `gh615-start-task-reinforce.sh`
- `gh616-start-task-commensurate-envelope.sh`
- `gh617-relay-xyz-commensurate-review.sh`

### Calibration Criteria:
1. **At least 7 of the 8 suites** must evaluate as `TURN-OFF` or `MERGE` under the skill's detector rules.
2. `gh798-status-skill.sh` must be classified as a wording-only/prose suite (`TURN-OFF`).
3. **Hard Stop:** If the calibration step fails (fewer than 7 turn-offs or `gh798` not classified as wording-only/TURN-OFF), the audit run is declared **INVALID** and must immediately halt without publishing or acting on any verdicts.
4. Score calibration rows with the same saved inputs and scoring pass as target rows; save them as `calibration.tsv` and generate the report table from that file. Check the calibration verdicts before publishing any target verdict. A separate hand-assigned calibration table cannot pass this gate.

---

## Unit & Data Access Modes

### Unit of Analysis
The unit of curation is **one entry in the `TESTS=(...)` array in `validate.sh`**.
- Anything the suite executes via `bash`, `python3`, `node`, or binary invocation belongs to its unit (e.g. `gh436-merge-cleanup.sh` running `gh436-merge-cleanup.py`).
- Sourced libraries (`test/_setup.sh`, `test/lib/*.sh`) provide shared fixture and containment context.
- Count the non-empty `TESTS` entries directly from `validate.sh`; do not compare only with `validate.sh --list`, which reads the same registry. Require the operator's expected count, stop on disagreement, and assert `TESTS ∩ EXEMPT = ∅`. Record `EXEMPT` separately, including the #831 eight, and score those eight only in calibration. Print the full target SHA and the SHA/date of the newest commit that changed `validate.sh`'s registry. Subdirectory suites may have their own pins and need no `EXEMPT` entry.
- **Subdirectory Suites:** Note that `test/gh306-registry-bidirectional.sh` `EXEMPT` only governs top-level `test/*.sh` files. Subdirectory suites (e.g. `synthetic/*`) that are turned off come out of `TESTS` and their own registry pin (`test/gh141-synthetic-registry.sh`), not into gh306 `EXEMPT`.

### Access Modes

1. **In-Checkout Mode (Preferred):**
   - The operator invokes the skill inside an active, clean repository checkout on the target branch (e.g. `development` or staging branch).
   - The skill does not pull or clone automatically.
   - Uses local disk tools (`rg`, file inspections, committed receipts) to inspect full source, helpers, and test definitions across all registered suites.
2. **Connector-Only Mode (Fallback):**
   - Used when operating without a local workspace clone, reading registry files, receipts, and workflow logs via the GitHub connector.
   - Full source reads are prioritized for: every non-KEEP candidate, the top 10 heavy suites by runtime, every `#853` isolation member, and every suite with a failure in the analysis window.
   - Suites evaluated solely from run logs or labels are `INVESTIGATE` (`LOW`) until their source is read. They cannot earn `KEEP` or a concrete removal verdict from those signals alone.

### Data Limitations & Disclosures
Every audit report must explicitly disclose data boundaries:
- **Committed Receipts:** Committed validation receipts represent passing (`green`) runs by construction; they provide accurate runtime distributions but no failure signal.
- **Hosted CI Logs:** Historical failure logs are extracted from hosted `validate.sh` summary `failed:` blocks. Log retention is subject to GitHub Actions artifact windows (typically 14–90 days).
- **Local Gate Receipts:** Local gate runs (`validation.jsonl`, `ci-local.sh` logs) supply historical failure signals not captured in hosted runs.
- **Label Coverage:** Some test runs or shims may produce partial test label manifests. Record the measured labeled count; unlabeled suites are `UNKNOWN` for label-based heuristics.
- **Unmeasured Signals:** Any signal, log, or receipt not directly observed or parsed is recorded as `UNKNOWN`; it is never estimated silently.

---

## Inputs

| Signal | Source | Collection Rule |
|---|---|---|
| **Registry** | `validate.sh` `TESTS`, gh306 `EXEMPT` | Independently count non-empty `TESTS` entries and compare with the operator's expected count; assert disjointness with `EXEMPT`. Record full target and newest registry-change SHAs. |
| **Current Tier** | `utils/ci-route.sh` registry mapping | Record Small (tier 1/2), Medium, or Large-only for each suite. |
| **Runtime** | `TESTS-RESULTS/.../validation.jsonl` (`event:"suite"`, `duration_ms`) | Compute median duration across at least 3 green full-gate receipts. Record runner host architecture. |
| **Failure Tally** | Hosted full-registry logs and committed failing suite receipts | Record each suite's executed `k of N` per run source, window, and run/receipt IDs. Mark unexecuted suites `UNKNOWN`; never report "never failed". Deduplicate the same run across sources. |
| **Failure Attribution** | Label-discovered issues and `fix:`/`hotfix:` commits touching `test/` | Record each source's searched N and window, then cite the exact issue or commit for each suite match. These are not run denominators. |
| **Failure Cause** | PRs/issues linked to failures; #853 tracking list | Classify failure mechanisms using the Failure Taxonomy. |
| **Labels & Hints** | `PASS:` / `ok -` output in full run logs | Extract sub-check counts and keyword hints for overlap and prose checks. |
| **Source Code** | Suite file, executed scripts, sourced helpers | Full source read required for every non-KEEP recommendation. |

### Known Flake Candidates to Seed
When initializing an audit, seed known non-deterministic candidates identified in prior windows:
- `gh610-claude-subscription.sh` (intermittent across PR runs)
- `gh123-lock-progress-bound.sh` (timing and progress bounds)
- `registry-lock-concurrency.sh` (intermittent contention / race)
- Discover every active #853 and #812 member by exact filename from the saved issue bodies, including `agent-chorus-bridge.sh`, `gh492-idle-kill.sh`, `gh620-skills-army-mini-sync.sh`, `gh777-inventory-ratchet.sh`, `gh674-merge-cleanup-hosted-lookup.sh`, and `gh436-merge-cleanup.sh`. Name every discovered member, its issue, and its class in the report; unmeasured classes stay `UNKNOWN`.

---

## Detectors (D1–D9)

### D1: Runtime Profiling & Heavy Suite Leverage
- Measure median execution time in seconds, global runtime rank, and share of the median full gate. Use at least 3 green full-registry receipts whose registry matches the target count; list each receipt path and full tested SHA. Compute one median full-gate runtime denominator from those receipts and use `med_s / denominator` for every `pct_gate` field in the TSV and summary. If fewer than 3 qualify, runtime and gate-share fields are `UNKNOWN`; never hardcode runtime figures.
- **Heavy Suite:** Rank ≤ 10 or consuming ≥ 1.0% of the total gate runtime.
- **High-Leverage Heavy Suites:** Special priority is given to measured heavy suites, including `gh251-validate-pytest-skip.sh`, `gh436-merge-cleanup.sh`, `gh549-work-events.sh`, and `marathon-drive.sh` when their current rank qualifies. Investigate whether nested executions can be bounded, faster siblings exist, or candidate status for NIGHTLY applies.
- Recompute rankings from fresh receipts after any suite trimming PR.
- *Role:* Runtime breaks ties and nominates NIGHTLY candidates. **Runtime alone never justifies turning off a test.**

### D2: Failure History & Defect Attribution
- Classify all observed failures across the audit window using the Failure Taxonomy.
- Same-commit / same-SHA divergence (passing on one run, failing on another) serves as primary evidence of non-determinism (`flake`).
- Bind each run to the commit it actually tested. A hosted `wave-reconcile` run qualifies an integrated snapshot named in its log (`Qualifying N landing(s) in integrated snapshot <sha>`); its `headSha` is the workflow's ref (a PR run's is the PR head) and must not be used. When the tested commit cannot be established, count the result but mark its SHA attribution `unknown`; it is not flake evidence.
- Report each source separately: hosted and committed local receipts get per-suite executed `k of N` and run IDs; labelled issues and fix commits get searched N, date window, exact suite mapping, and source IDs. Show counts of suites with at least one observed failure and suites with no failure data. No matching issue or commit is evidence of zero failures.

### D3: Touch-Set Overlap & Duplicate Analysis
- For each suite, statically analyze:
  1. Binaries and scripts executed (`bash <x>`, `python3 utils/py/<y>`, `bin/tick <verb>`, `node <z>`).
  2. Library files sourced (`test/_setup.sh`, `test/lib/*.sh`).
  3. Repository paths read or grepped.
  4. Repository paths written or modified.
- Two suites overlap when their **invoked target entry points overlap**.
- Text similarity (e.g. 5-token shingle Jaccard ≥ 0.6) or label similarity is a secondary tiebreaker only after touch-sets overlap. Filename similarity (e.g. `gh155-phase3` vs `gh155-phase5`) is not overlap if distinct subsystems are invoked.
- When two suites share identical target entry points and duplicate contract assertions, nominate the redundant suite for `MERGE`.
- Generate duplicate candidates from saved, computed touch sets. Do not seed a hand-typed list of duplicate suite pairs.

### D4: Sibling Coverage
- A suite is **covered** when a named sibling suite tests the same target entry points with an equal or superset set of behavioral assertions.
- *Example:* `synthetic/synthetic-pi-model-unset.sh` is covered by `test/pi-turn.sh` (which asserts exit code 5, clean working tree, no commit, and uninvoked model binary).

### D5: Prose & Non-Core Text Check
- Count assertions that inspect documentation and markdown files (`*.md`, `SKILL.md`, `docs/*`, `README`, `ROUTER.md`, `AGENTS.md`) versus assertions that execute codebase scripts/binaries and verify behavioral contracts.
- Executing code counts only when an assertion checks that code's behaviour. Running a script and then grepping a doc does not count.
- Exclude generated fixture files or runtime-emitted docs created inside a test sandbox (e.g. asserting `ESCALATION.md` was created by an agent turn is behavioral).
- **Prose Ratio:** `(doc-grep assertions) / (total assertions)`.
  - **Ratio ≥ 0.6 or Pure Skill/Doc Text (GH-831):** Candidate for `TURN-OFF` if the suite merely asserts wording, markdown structure, or non-core skill text rather than runtime harness behavior. A suite at ≥ 0.6 that still has behavioral assertions no sibling covers (D4) is `SPLIT`, not `TURN-OFF`; name those assertions.
  - **Ratio 0.2–0.6 (Mixed):** Candidate for `SPLIT` (keep behavioral checks; drop/move pure wording assertions).
  - **Ratio < 0.2 (Behavioral):** Retain on gate.

### D6: Junk Pattern Detection
Inspect individual assertions for anti-patterns:
- **Exact String Fragility:** Asserting exact prose strings that break on innocuous copy-edits but pass on broken logic.
- **Duplicate Contract Calls:** Repeating identical CLI invocations and flag checks across multiple independent suites without novel assertions.
- **Stub Implementing Assertion:** A test stub (e.g. mock `gh` or `git`) hardcodes the exact string the test subsequently asserts.
- **Private Call-Shape Checks:** Asserting internal Python function names or private helper argument lists instead of public CLI behavior.
- **Vacuous Negative Controls:** Assertions that mutate a local copy or test fixture and grep the copy without exercising the actual code path (e.g. `gh798` controls 8a/8b).

### D7: Can-It-Fail Verification
- Before asserting that a test suite cannot fail, trace all sourced helpers and error traps.
- A suite sourcing `_setup.sh` that calls `fail()` on error will exit 1 on failure even if the file concludes with `exit 0`.

### D8: Fixed-at-HEAD Verification
- For every historical flake or failure, check whether a remediating commit already landed on the active branch (e.g. `gh649` resolved by `pwd -P` canonical path resolution).
- If fixed at HEAD, classify as `fixed-flake`; cite the fixing commit and apply the ordinary KEEP evidence rule. Do not quarantine solely for a fixed historical failure.

### D9: Four-Question Gate (OpenClaw)
For every evaluated suite:
1. *What contract or behavior does it protect?* (CLI verb, concurrency invariant, data integrity, routing).
2. *What credible regression makes it fail?* (State the failure scenario).
3. *Why doesn't existing coverage catch it?* (Identify the unique boundary).
4. *Does it require a test-only seam in production code?* (Reject artificial test-only hooks).
- *Verdict Effect:* A suite with no clear answer to Q1 or Q2 is a candidate for `TURN-OFF` or `MERGE` (it guards no identified behavior or failure mode). A suite with answers to Q1 and Q2 but no answer to Q3 is a candidate for `MERGE` into its covering sibling.

---

## Failure Taxonomy

| Class | Evidence Required | Verdict Effect |
|---|---|---|
| `regression-caught` | Failure directly caught a real bug, confirmed by a subsequent product code fix (e.g. `gh436` in #812 caught by `0ae3452a`/#794; `gh496` caught race in #813/#818). | **Protected.** Stays on the PR gate regardless of runtime. |
| `coupling` | Failure caused by unrelated inventory changes, doc rewordings, or count shifts. | If coupling is to prose/wording, run D5: at ratio ≥ 0.6 candidate for **TURN-OFF**. For fragile D6 assertions on core code, **KEEP-FIX** requires a cited assigned fix; otherwise **INVESTIGATE**. |
| `flake` | Same commit passed in another run; or error log cites timing bound/port race. | An ongoing unfixed flake blocking CI is **QUARANTINE** without an assigned fix, or **KEEP-FIX** with a cited assigned open fix. Historical divergence without recent red or an established fix is **INVESTIGATE**. |
| `host` | Failure caused by runner environment (macOS vs Linux paths, `/tmp` contention, host Python). | **KEEP-FIX** with a cited assigned open fix; otherwise **INVESTIGATE** or **QUARANTINE** under the flake rule. The #853 umbrella alone is attribution, not assignment. |
| `fixed-flake` | Cause of failure was resolved by a landed commit at HEAD (D8). | Eligible for **KEEP** if the ordinary evidence bar is met. Cite fixing commit; do not quarantine solely for the fixed failure. |
| `unattributed` | Unexplained timeout or missing summary log. | `INVESTIGATE` if this is the only failure class; include the failure in the radar share. |

---

## Verdicts, Decision Rules & Guardrails

| Verdict | Definition & Rule | Proposed Action (Requires Approval) |
|---|---|---|
| **KEEP** | Meets retention bar, catches regressions, or uniquely guards a core contract with passing behavioral receipts. | Retain in `validate.sh` `TESTS`. |
| **KEEP-FIX** | Retained suite with an active, assigned fix issue or PR open in the current window (requires its citation; an umbrella alone does not assign the fix). | Retain in `TESTS`; link the assigned fix. |
| **NIGHTLY** (candidate) | Heavy suite with a faster PR-time sibling covering its full target set (see NIGHTLY Rule). | Listed as candidate for future scheduled runs (#859). Remains in `TESTS`. |
| **QUARANTINE** | Flaky suite blocking CI with no fix landed at HEAD and no active fix lane assigned. | Move from `TESTS` to `test/gh306-registry-bidirectional.sh` `EXEMPT` with `quarantine: <issue>` reason. Keep file on disk. If multiple suites share root cause, recommend `whack-a-mole`. |
| **SPLIT** | Mixed suite (D5 prose ratio 0.2–0.6, or ≥ 0.6 with uncovered behavioral assertions) combining behavioral checks with prose greps. | Propose splitting: retain executable contract checks; drop or move wording greps. |
| **MERGE** | Redundant suite whose unique assertions are folded into a named keeper suite. | Propose folding assertions into keeper after red control; then turn off. |
| **TURN-OFF** | Obsolete suite (target removed), pure prose/skill-text suite (GH-831), or fully covered sibling with no unique assertions. | Remove from `TESTS`; add top-level suites to gh306 `EXEMPT` with reason, or remove subdirectory suites from their own registry pin (name that pin in `restore`). Keep the file on disk. |
| **INVESTIGATE** / **UNKNOWN** | Insufficient telemetry or unmeasured metrics. | Retain in `TESTS` pending further telemetry; never default to KEEP. |

### Tier-Based Flake Rule (#802/#853)
A flaky suite in an active tier (the Small or Medium membership mapped by `utils/ci-route.sh`, including `SUBSYSTEM_TESTS_small`) receives `KEEP-FIX` only with a cited, assigned open fix issue or PR. Without one, an ongoing flake blocking CI is `QUARANTINE` under the ordinary rule. Historical same-SHA divergence with no recent red and no established fix is `INVESTIGATE`, not automatic KEEP or QUARANTINE. Outside those tiers, apply the same evidence rules rather than turning a suite off on membership alone.

### The Retention Bar
The retention bar applies only after D3/D4 show that no other suite on the PR gate covers the same entry point. A covered suite is a `MERGE` or `TURN-OFF` candidate whatever category it falls in. When no covering sibling exists, a suite is eligible for **KEEP** under rule 7 if it independently guards:
- Package installation, bootstrapping, or migration logic.
- Concurrency, file locks, or driver lock invariants.
- Security, credential containment, or network egress boundaries.
- CLI contracts (exit codes, standard flags, stdout/stderr protocols).
- Data integrity, database schemas, or ledger transactions (`releases.db`, `tick`).
- Gate routing or CI test selection contracts (`ci-route.sh`, `gh308`).
- Source inspection when it is the only independent guard of a user-facing configuration key or path per D4.

*Mantra:* **Static or slow is not a reason to delete; but redundant, dead, or unmeasured is never a reason to keep.**

### Sibling Deduplication Precedence
**Sibling coverage and deduplication take precedence over the retention bar.** Even if a suite tests a retention-bar contract, if another faster suite already guards that exact contract with equal or superset assertions (D4), the redundant duplicate is nominated for `MERGE` or `TURN-OFF`.

### The NIGHTLY Rule
A heavy suite $H$ is a candidate for NIGHTLY only when **all four conditions hold**:
1. $H$ is heavy (D1: rank ≤ 10 or ≥ 1.0% gate time) and has **no** `regression-caught` failures in the audit window or issue history.
2. A named sibling suite $S$ remains on the PR gate, and $S$'s invoked target scripts/binaries are a **superset** of $H$'s invoked targets (D3). Static reads, greps, and written files do not count toward superset target invocations; only invoked target scripts/binaries count.
3. $S$ is significantly faster (median duration of $S \le 20\%$ of $H$) and has no open flakes.
4. If $H$ guards a retention-bar contract, $S$ must guard that same contract.

*PR Gate Yield Note:* Candidates remain in `TESTS` today (#859 is pending), so a NIGHTLY verdict takes nothing off the PR gate until scheduled runner machinery lands. Reports must explicitly track the count of suites proposed to leave the PR gate separately.
*Fallback:* If no sibling qualifies, the suite stays on the PR gate; apply the ordinary KEEP evidence rule. Insufficient evidence yields `INVESTIGATE`, never automatic KEEP.

### Core Guardrails
- **`0 of N runs` is never a reason to turn off or demote a test.**
- **A `regression-caught` suite is never proposed for NIGHTLY, QUARANTINE, or TURN-OFF.** (e.g. `gh436-merge-cleanup.sh` caught the #812 regression; it remains on the PR gate).
- **An active #853 member is never turned off.** It can be `KEEP-FIX`, `QUARANTINE`, or `INVESTIGATE` under the evidence rules.
- **Subdirectory Suites:** Note that `test/gh306-registry-bidirectional.sh` `EXEMPT` only governs top-level `test/*.sh` files. Subdirectory suites (e.g. `synthetic/*`) that are turned off come out of `TESTS` and their own registry pin (`test/gh141-synthetic-registry.sh`), not into gh306 `EXEMPT`.
- **Check Pinned Suites:** Before proposing `TURN-OFF`, verify whether other suites assert the entry in `TESTS` (e.g. `gh35-test-tiers.sh`, `gh365-driver-lane-registry.sh`, `gh141-synthetic-registry.sh`, `ci-workflow.sh`, `gh379-canary-uses-validate.sh`, or release manifest suites).
- **No Unbacked Merges:** If a proposed survivor for `MERGE` or `SPLIT` does not exist, mark the row as `parked: no survivor` rather than creating new suites under the freeze.
- **High Confidence Required:** QUARANTINE, TURN-OFF, MERGE, SPLIT, and NIGHTLY require full source inspection and `HIGH` or `MED` confidence. `INVESTIGATE` has no confidence floor.
- **Observation Window:** Approved turn-offs are moved to `EXEMPT` (or removed from registry pin) for an observation window before anyone considers deleting a file (at least 14 days).

---

## 8-Point Acceptance Test for Audit Runs

Every completed audit run must pass this 8-point acceptance check before findings or report issues are accepted:

1. **Calibration Passed:** Calibration against the 8 suites turned off by #831 passed (at least 7 of 8 scored `TURN-OFF`/`MERGE`, and `gh798` scored wording-only/`TURN-OFF`).
2. **Target Branch Pinned:** Audit was executed strictly on `development` or active stabilization staging branch (not `main`).
3. **Honest Metrics:** All unmeasured suites, missing durations, or unobserved failure signals are recorded as `UNKNOWN` or `INVESTIGATE`, with zero keep-by-default fallbacks.
4. **Multi-Source Failures:** Record the searched N and window for hosted runs, labelled issues, fix commits, and committed failing receipts; keep run denominators separate from attribution counts.
5. **Seeded Flakes Investigated:** `gh610`, `gh123`, and `registry-lock-concurrency` show historical same-SHA divergence but no recent red since 2026-09-25. Classify them `INVESTIGATE` until a fix or continuing failure is established; do not infer `KEEP` from subsequent green runs. An ongoing unfixed flake blocking CI is `QUARANTINE`, or `KEEP-FIX` with a cited assigned open fix.
6. **Heavy Suites Profiled:** High-leverage heavy suites (including `gh251`, `gh436`, `gh549`, `marathon-drive`) are analyzed for nested runners and faster siblings.
7. **Redundant Suites Merged:** Duplicate suites with overlapping touch sets receive `MERGE` recommendations naming a surviving keeper.
8. **Sibling Skills Triggered:** Sibling skill recommendations (`radar` for trunk-red clusters, `whack-a-mole` for shared root causes) fire accurately based on objective criteria.

---

## Output Format

The audit produces a machine-readable tab-separated values (TSV) dataset and a markdown summary, saved to the evidence directory:
`TESTS-RESULTS/<date>+GH-<issue>/ci-suite-audit.tsv`

### TSV Columns
```text
suite	tier_now	med_s	rank	pct_gate	fails (k of N)	fail_class	issues	touch_set	overlap_with	covered_by	prose_ratio	junk_flags	pins	gate_q1_q3	verdict	proposed_action	evidence	confidence	source_read	restore
```

- `evidence`: Cites `file:line`, job run ID, or GitHub issue/PR number.
- `confidence`: `HIGH` requires source read and measured failure data; green receipts alone give at most `MED`. `LOW` means material fields remain unmeasured; `UNKNOWN` means confidence cannot be assessed.
- `restore`: Shell command to restore or un-exempt the suite if needed.
- Copy full 40-character SHAs from git or API output for commit links and report metadata; never reconstruct them. A short SHA is acceptable only in the issue title and dedupe marker.

### Summary Markdown Layout
The summary report includes:
1. **Audit Metadata:** Run date, full target and newest registry-change SHAs, ref/branch, expected and observed registry counts, analysis mode (in-checkout vs connector), each source's N/window/IDs, qualifying full-receipt paths and tested SHAs, and the one computed full-gate runtime denominator in seconds (or `UNKNOWN`). Count suites with at least one observed failure and suites with no failure data.
2. **Pre-Flight Calibration Results Table:** Results for the 8 #831 calibration suites (`gh578`, `gh778`, `gh798`, `gh779`, `gh781`, `gh615`, `gh616`, `gh617`) with prose ratios, verdicts, and pass assertion (≥7/8 turn-offs, `gh798` wording-only classified).
3. **Detector Coverage Table (D1–D9):** Evaluated counts vs the measured registry total for every detector, or count marked UNKNOWN.
4. **Verdict Breakdown Table:** Tally of suites per verdict class (including INVESTIGATE and UNKNOWN) and count/percentage of suites proposed to leave the PR gate (QUARANTINE + TURN-OFF + MERGE).
5. **D3 Shared Entry-Point Clusters Table:** Entry points invoked by $\ge 3$ suites, listing overlapping suites, overlap details, and nominated MERGE candidate or retention reason.
6. **Heavy Suites & NIGHTLY Evaluation Table:** Top heavy suites by runtime, evaluating the 4 NIGHTLY conditions (1: heavy & no regression-caught, 2: superset sibling on PR gate, 3: sibling duration $\le 20\%$, 4: sibling guards retention contract), nearest sibling, sibling median duration, and candidate verdict.
7. **SPLIT Ratio Band Verification Table:** Verification that every SPLIT candidate's prose ratio falls within the 0.20–0.60 range, or is ≥ 0.60 with its uncovered behavioral assertions named (D5).
8. **Actionable Proposals Table:** Itemized list of all non-KEEP candidates with suite name, tier, median duration, failure history, proposed action, evidence/citations, and mandatory `confidence` column.
9. **Diagnostic & Remediation Reminders:** Measured sibling skill trigger formulas (`radar` share $(unattributed + coupling)/red\_runs \ge 25\%$; `whack-a-mole` cluster $\ge 3$ parallel-load/host races in #853).

---

## Report Issue & Per-turn Comments

### Report Issue Creation & Deduplication
- **Title Format:** `ci-suite-audit: <audit date> report @ <registry SHA>` (e.g. `ci-suite-audit: 2026-10-08 report @ <short staging SHA>`).
- **Deduplication Marker:** The report issue body begins with an HTML comment marker:
  `<!-- ci-suite-audit:<registry-sha>:<audit-date> -->`
- **Dedupe First:** Before opening a new issue, look for an existing report in this order:
  1. **The local record.** When the skill creates a report issue, it writes the number and marker to `TESTS-RESULTS/<date>+GH-<issue>/report-issue.txt`. A re-run first reads that file: it is the only check that is consistent immediately after creation.
  2. **A direct listing,** matched locally on the marker: `gh issue list --state open --label ci --limit 200 --json number,title,body`. Do **not** use `--search`.

  Both GitHub reads are eventually consistent. The #862 practice runs opened duplicates when re-running 3 s after creation: first through search (#871/#872), then through listing (#873/#874). The local record closes that window, and a later session's listing covers re-runs minutes or days apart.
  - *Match found (same SHA or audit date):* Update the existing issue body and post a comment with the delta. **Never open a duplicate issue.**
  - *Multiple open matches:* Stop and request operator clarification.
  - *Closed match:* Open a new issue referencing the previous closed report.
- **Labels:** Apply `ci` and `stability`, plus `ci-suite-audit` if that label exists in the repository. **Never apply the `radar` label.**
- **GitHub Size Limit (65,536 chars):** If the full report exceeds GitHub's issue body limit, place the summary, verdict counts, non-KEEP rows, and reminders in the issue body. Post the full per-suite TSV/table across sequentially numbered issue comments (`table part k of n`).
- **Posting Fallback:** Attempt issue creation via GitHub CLI (`gh issue create`). If CLI is unavailable or unauthorized, create via GitHub connector tools. If running offline or without GitHub write permissions, write the formatted report to the evidence directory (`TESTS-RESULTS/<date>+GH-<issue>/ISSUE.md`) and alert the operator.

### Per-Turn Comments
- In interactive audit sessions, after each turn where a decision is reached, post **one** structured comment detailing:
  - Verdicts accepted, rejected, or overridden by the operator.
  - Follow-up issues filed (only with explicit operator authorization).
  - Open questions resolved.
- **Post Only on Changes:** Turns without decisions or changes generate no comment ("no change" comments are prohibited).
- Conclude each comment with the remaining open items. When all items are resolved, propose closing the issue. Close only upon operator confirmation.

### Safety & Redaction
- Redact all access tokens, API keys, secret variables, and environment values.
- Strip local machine paths, replacing them with repository-relative paths (`skills/...`, `test/...`).

---

## Related Skills

The skill recommends sibling skills for broader coordination; it never invokes them autonomously.

- **[radar](../../3-weekly/radar/SKILL.md):** The **diagnostic** sibling. Recommends running radar when CI failures reflect wider SDLC or process drift rather than isolated test defects:
  - *Trigger:* $\ge 25\%$ of red runs in the window are `unattributed` or `coupling`, or a trunk-red cluster appears (e.g. `gh436` and `gh674` red together across multiple runs, as in #812).
- **[whack-a-mole](../../3-weekly/whack-a-mole/SKILL.md):** The **remediation** sibling. Recommends running whack-a-mole when recurring test failures share a single root cause:
  - *Trigger:* $\ge 3$ suites fail due to the same underlying mechanism (e.g. shared runner port race or `/tmp` collision). If an existing umbrella covers the pattern (such as #853 for test isolation), cross-reference that issue instead of opening a new one.
- **[ci-optimize](../ci-optimize/SKILL.md):** Pipeline architecture cross-link (unit: entire CI/CD pipeline; `ci-suite-audit` unit: one test suite).

### Sibling Reminder Block
Every audit report and issue concludes with a status block:

```markdown
## Sibling Skill Recommendations
- **radar:** [trigger met: <evidence> | not triggered]
- **whack-a-mole:** [trigger met: <evidence (points to #853 if covered)> | not triggered]
```

---

## Proposed Authoring Gate (Proposal for Operators)

> **For operator decision. Not active by default.** Adapted from OpenClaw (MIT).
> Under the repository test freeze, no new test files may be added. When modifying or extending existing suites, apply this 4-question gate to every new assertion:

1. **What behavior or contract does this assertion protect?** (Name the CLI verb, schema constraint, or isolation boundary).
2. **What credible regression makes this assertion fail?** (Witness the failure under mutation or record a red control).
3. **Why don't existing assertions catch it?** (Check existing suites with `rg` before adding duplicate assertions).
4. **Does it rely on artificial test-only hooks in production code?** (Avoid adding flags or exports solely for testing).

---

## Sources

Upstream credits, MIT license texts, and copyright notices are documented in [`NOTICE`](NOTICE).
