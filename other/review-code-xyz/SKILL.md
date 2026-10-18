---
name: review-code-xyz
description: >-
  Meticulous local code review ladder (uncommitted changes, a branch, or files) using /recon and
  /debug-mantra to test each fix and feature against live ground truth, then /workhorse and
  /unstuck to resolve reversible issues without stopping for operator permission. Reviewing a
  GitHub PR? Use review-pr-xyz (validates the PR's claims first, report-only). Multi-model panel
  review? Use review-xyz.
metadata:
  argument-hint: "[diff, branch, or file]"
---

# /review-code-xyz — Meticulous Ground-Truth Local Code Review Ladder

`/review-code-xyz` is an empirical code review discipline that treats every proposed change as a
claim requiring firsthand verification. Rather than passively reading a diff and commenting
on style or plausible appearance, `/review-code-xyz` actively maps the system's blast radius, tests
fixes and features against live execution, and uses autonomous problem-resolution ladders to drive
forward movement.

**Which review skill:** local diff or branch → this skill. A GitHub PR →
[`review-pr-xyz`](../review-pr-xyz/SKILL.md), which validates the PR's claims first, reuses this
skill's Phase 1, 2 and 4 definitions, and only reports (it never pushes fixes). A multi-model
reviewer panel → [`review-xyz`](../review-xyz/SKILL.md).

It coordinates four specialized disciplines into a cohesive review workflow:
1. **[`/recon`](../../1-hourly/recon/SKILL.md)**: Seam and blast-radius mapping across callers, data
   flows, public contracts, and operational failure paths before forming an opinion.
2. **[`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md)**: Meticulous ground-truth testing.
   Falsifies symptom-fix patches, executes mutation tests to watch assertions go red, and verifies
   feature acceptance criteria with negative controls and measured evidence.
3. **[`/workhorse`](../workhorse/SKILL.md)**: Governed defect resolution ladder. Triages review
   findings into an atomic priority queue (`[Blocker]`, `[Should]`, `[Nit]`, `[Pass]`) and enforces
   least-mechanism architecture ([`/ponytail`](../../1-hourly/ponytail/SKILL.md)), governance compliance,
   and preservation invariants.
4. **[`/unstuck`](../../1-hourly/unstuck/SKILL.md)**: Autonomous forward movement and anti-hesitation
   engine. Classifies adaptations on the Reversibility Scale (`Easy` vs `Costly` vs `One-way door`):
   **autonomously adapts and tests `Easy` reversible pivots without stopping to prompt the operator**,
   freezes cogs, and applies foundational unblocking moves.

---

## Recite this — verbatim, as the first thing in your first response

> **Review-Code Discipline:**
> 1. **Ingest target & map blast radius (Phase 1 /recon).** Ingest the local diff or branch, map callers, state mutations, contracts, failure paths, and audit adherence to centralized helpers and zero parallel subsystems (DRY).
> 2. **Meticulously test fixes & features (Phase 2 /debug-mantra).** Test every fix against root cause (falsify symptom patches; mutate guards to watch them fail) and verify feature acceptance criteria with measured ground truth and negative controls.
> 3. **Autonomous resolution & anti-hesitation (Phase 3 /workhorse + /unstuck).** If pivots or adaptations are needed, classify reversibility (`Easy`/`Costly`/`One-way door`): autonomously adapt and test `Easy` changes without operator round-trips; freeze cogs and execute foundational unblocking moves.
> 4. **Grade & synthesize verified findings (Phase 4).** Categorize findings (`[Blocker]`, `[Should]`, `[Nit]`, `[Pass]`) with exact `file:line` citations, emit the actionable checklist, and deliver the verdict twice: post the report to the GitHub PR/issue via `gh` **and** render it on-screen with the verified comment URL. Never one without the other.
>
> **Overall Goal:** Every fix and feature verified against live behavior rather than plausible appearance, with reversible issues resolved autonomously and review conclusions grounded in runnable proof.

Then begin work. When `/review-code-xyz` is the active orchestrating skill, this recital
precedes subordinate skill invocations; subordinate skills ([`/recon`](../../1-hourly/recon/SKILL.md),
[`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md), etc.) are then loaded for their mechanics
without conflicting recitals.

---

## The 5-Phase Review Ladder

```text
Phase 0: Target Intake & Scope Resolution  ──► Local diff, branch or files; isolate refs & context (PRs → review-pr-xyz)
                 │
                 ▼
Phase 1: Seam & Blast Radius Recon (/recon)──► Map callers (Lane A), state (Lane B), contracts (Lane C), tests (Lane D), DRY (Lane E)
                 │
                 ▼
Phase 2: Meticulous Ground-Truth Testing   ──► Fixes: Repro -> trace fail path -> mutate-to-red (falsify)
         (/debug-mantra)                   ──► Features: Measured ground truth -> falsify criteria -> negative controls
                 │
                 ▼
Phase 3: Autonomous Pivot & Resolution     ──► Classify reversibility: Easy (autonomous forward move) vs Costly vs One-way
         (/workhorse + /unstuck)           ──► Self-invoke /unstuck on hesitation tripwires; apply /ponytail root-cause fix
                 │
                 ▼
Phase 4: Graded Findings & PR Actionability──► [Blocker] / [Should] / [Nit] / [Pass] with mandatory file:line citations;
                                               report posted to the GH PR/issue AND rendered on-screen with the verified comment URL
```

---

## Phase 0: Target Intake & Scope Resolution

Resolve the exact target under review: uncommitted working tree changes, staged diffs, branch diffs
against upstream, or targeted files.
```bash
# Review uncommitted changes against HEAD
git diff HEAD

# Review current branch against development baseline
git diff origin/development...HEAD

# Stat changes to size the review blast radius
git diff --stat origin/development...HEAD
```

**Asked to review a GitHub PR?** Stop and hand off to [`review-pr-xyz`](../review-pr-xyz/SKILL.md).
PR review lives there because it adds a claim-validation phase this ladder does not run, and it is
report-only.

**Scope Invariant:**
- Identify the base: the branch should target the active WIP branch (`development`), not `main` (per orchestrator rails).
- Size the diff: a targeted bug fix should typically be focused (< 500 lines); large architectural diffs require all 5 recon lanes.

---

## Phase 1: Seam & Blast Radius Recon ([`/recon`](../../1-hourly/recon/SKILL.md))

A diff read in isolation is plausible fiction. Code review requires knowing what callers, state,
contracts, and failure modes are touched by the modification.

Run the five recon lanes across the touched symbols:

| Lane | Focus | Review Inquiry & Verification |
|---|---|---|
| **Lane A. Entry & Call Paths** | Callers & Dispatch | Trace callers of all modified functions. Did call signatures, parameter defaults, or return types change? Are callers in other modules updated? Check CLI shims, hook registries, plugin dispatch, and event handlers. |
| **Lane B. State & Data Flow** | Readers & Writers | What state is mutated? Verify the single-writer invariant. Are SQLite locks, file descriptors, transactions, or cache layers handled? Does this introduce competing write paths or dirty reads? **Step N+1:** verify whether an active reader, background reconciler, or UI consumer exists for any state or status being written. |
| **Lane C. Contracts & Boundaries** | APIs & Protocols | Do changes alter public APIs, CLI flags, JSON schemas, environment variables, or error codes? Check consumers across sibling modules or external repositories. **Step N+1:** verify whether arguments passed into engines/solvers act as constraints or generators to prevent entity duplication. |
| **Lane D. Build, Failure & Tests** | Errors & Coverage | How does this code fail? Trace timeouts, process exits, broken pipes, signal handling (`SIGINT`/`SIGTERM`), and missing input files. What existing test suites cover this seam? **Step N+1:** simulate temporal retry and lease recovery on failure to prevent infinite stuck retry loops. |
| **Lane E. Centralized Helpers & DRY** | Helpers & Anti-Reinvention | Does this change reinvent functionality that already exists in centralized helpers (e.g. `utils/py/`, canonical CLI shims, standard libraries)? Does it construct a parallel subsystem instead of extending existing modules (violating `GUIDING-PRINCIPLES.md` North Star)? Check for copy-pasted blocks or duplicate helper definitions across the diff. |

### Lane E: Centralized Helpers & Anti-Redundancy (DRY) Audit

The North Star (`GUIDING-PRINCIPLES.md`) requires: *durable, reversible, DRY; extend what exists rather than forking a parallel system.*
A diff that works but reinvents existing wheels introduces long-term tech debt, bugs, performance overhead, and maintenance drag.

Reviewers must audit three anti-redundancy checks:
1. **Centralized Helper Adherence:**
   - Did the diff implement custom logic (e.g. subprocess execution, lock management, path/root resolution, JSON parsing, git mutation guards, or date formatting) where a canonical helper already exists in `utils/py/`, `src/`, or shared runtime modules?
   - Bypassing an established helper in favor of an ad-hoc inline solution is a `[Blocker]`.
2. **Parallel Subsystem / Reinvention Trap:**
   - Does the change build parallel shadow machinery instead of extending established subsystems (e.g. custom telemetry logging instead of `.tick` events, custom runner loops instead of the existing driver)?
   - Standing up a parallel subsystem is an architectural violation and a mandatory `[Blocker]`.
3. **Intra-Diff & Cross-Module Duplication (DRY):**
   - Are there duplicated helper functions or copy-pasted logic across multiple files in the PR?
   - Code duplication that can be extracted cleanly into an existing shared utility is a `[Should]`.

### Step N+1 Downstream Verification

Code review must never stop at the local mutation site. Reviewing only lines changed inside the diff is the primary source of plausible-sounding approval on broken architecture: approving `status = SENDING` without checking whether a background polling worker actually selects and advances it, approving an unhandled `raise` without checking whether a distributed lease manager enters an infinite recovery retry loop, or approving passing arguments into a solver without checking whether the callee treats them as constraints or generators.

Reviewers must enforce the Step N+1 verification invariants defined in [`recon`](../../1-hourly/recon/SKILL.md#step-35--step-n1-downstream-verification-default-vs-deep):

#### 1. Invariant Review Classification (Mandatory on Every Seam)
Reviewers must trace past transparent delegation (forwarding helpers, retry decorators) to the first logical downstream boundary:
- **Consumer Behavior & Progress (Lane B):** Verify at `file:line` that deployed consumers not only exist, but actually select the newly written state/value and advance it toward a terminal state or bounded timeout/recovery path (a UI badge or display-only reader alone does not prove progress). Introducing a stranded or unadvancing non-terminal state without a progress owner is a `[Blocker]`. Justified terminal/audit-only writes must be noted as such.
- **The Retry Hop (Lane D):** Verify at `file:line` how the enclosing caller and temporal retry mechanism behave when an exception is raised or claim held. Introducing an infinite stuck retry loop (e.g. continuous unresolvable retries without backoff/dead-letter) is a `[Blocker]`.
- **Parameter Role Contract (Lane C):** Verify at `file:line` whether arguments passed into existing engines/solvers act as constraints (filtering) or generators (creating candidates). Passing entities under the assumption of constraint when the callee acts as a generator creates duplicate entities and is a `[Blocker]`.
- **Rollout Coexistence & Rollback (Lane C):** When persisted formats, status values, or external contracts change, verify backward/forward coexistence across versions and rollback feasibility per SWE migration policy. Introducing breaking schema/state without a stated coexistence or rollback boundary is a `[Blocker]`.

#### 2. Deep Mode Review (`/review-code-xyz --deep`)
When review is invoked with `--deep` or for complex cross-service architectural changes, expand review to transitive call chains ($N+2, N+3$), programmatic dataset validation (e.g. running verification scripts over JSON/CSV catalogs), and distributed failure matrices (worker crash / clock skew). Reserve deep mode for broader transitive analysis, not for finishing an ordinary check hidden behind one wrapper.

**Evidence Standard:**
- Every consumer, caller, and callee cited in the review must exist at `file:line`.
- Anything unread, unverified, or cut off by budget is recorded under **Unknowns**, never assumed safe.

---

## Phase 2: Meticulous Ground-Truth Testing ([`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md))

Verified beats plausible. Reviewers must not merely read code; they must test the behavior of
fixes and features against live reality.

### 1. Testing Fixes (Root Cause vs. Symptom-Fix Trap)

When reviewing a bug fix, apply the four debug mantras rigorously:

1. **Mantra 1 — Reproduce reliably:**
   - Verify there is an automated regression test reproducing the original defect.
   - If the regression test is missing, write one or require it before approving, unless the repo
     forbids new tests (XYZ-forge: `AGENTS.md` *No new tests*, GH-831). There, require the existing suite that
     covers it, or a recorded manual repro.
2. **Mantra 2 — Trace the fail path:**
   - Trace from the crash or incorrect output back to the root cause origin.
   - **The Symptom-Fix Trap:** Actively scrutinize whether the fix merely patches symptoms at the
     crash site (e.g. adding `try/except: pass`, defaulting a `None`, coercing types, adding loose
     regexes, or using `|| true`) while leaving the corrupt state producer intact upstream.
     *The crash site is where the invariant was checked; the bug is where it was broken.*
     A fix that masks the crash without preventing the bad state is a `[Blocker]`.
3. **Mantra 3 — Falsify the fix (The Mutation Test):**
   - **"A check that cannot fail is not a check."**
   - Mutate the fix in a disposable environment:
     - Invert the condition (`if not valid` → `if valid`).
     - Comment out the guard or remove the correction.
     - Transpose arguments or return dummy values.
   - Run the test suite: **Did the test turn RED?**
   - If the test still passes when the fix is broken, the test is decorative and reports confidence
     it never earned. This is a mandatory `[Blocker]`.
   - In a repo that forbids new tests (XYZ-forge: `AGENTS.md` *No new tests*, GH-831), where no existing suite
     covers the fix, a manual red control recorded under `TESTS-RESULTS/` satisfies this mantra. It mutates
     the fix and records the failing result.
4. **Mantra 4 — Cross-reference breadcrumbs:**
   - Walk recent `CHANGELOG.md` entries and git history. Does this fix repeat a previously failed
     pattern or reopen a settled architectural decision?

### 2. Testing Features (Acceptance Criteria & Boundary Invariants)

When reviewing a new feature or enhancement:

1. **Measured Ground Truth at Review Time:**
   - Execute the feature's entry points directly. Do not rely on claimed execution logs.
   - Verify outputs, return codes, and side-effects match specifications.
2. **Falsify Acceptance Criteria:**
   - **"An empty input passes every check."** Verify that empty strings, missing files, or zero-byte
     inputs fail loudly rather than passing vacuously through unhandled command substitutions or
     permissive wildcards.
   - Size-check extracted artifacts before asserting correctness over them.
3. **Negative Controls & Boundary Stress:**
   - Test invalid CLI arguments, malformed configuration files, and nonexistent paths.
   - Test concurrency and lock contention (e.g. parallel runs of `./validate.sh` or concurrent database access).
   - Test idempotency: does running the feature twice in succession produce identical, safe results without duplicate records or side effects?

---

## Phase 3: Autonomous Pivot & Resolution Loop ([`/workhorse`](../workhorse/SKILL.md) + [`/unstuck`](../../1-hourly/unstuck/SKILL.md))

When review or ground-truth testing surfaces failures, gaps, or necessary adaptations, the agent
must avoid constant round-trips to the operator for routine adjustments.

### 1. The Reversibility Decision Matrix

Classify every necessary adaptation or pivot on the repository's shared scale:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       REVERSIBILITY CLASSIFICATION                          │
├─────────────────┬──────────────────────────────────┬────────────────────────┤
│ Classification  │ Scope & Characteristics          │ Action & Protocol      │
├─────────────────┼──────────────────────────────────┼────────────────────────┤
│ EASY            │ - Local test assertion fixes     │ AUTONOMOUSLY EXECUTE   │
│                 │ - Edge-case input handling       │ - Do NOT ask operator  │
│                 │ - Defensive parameter checks     │ - Implement & test     │
│                 │ - Fixing a typo or broken regex  │ - Record in ledger     │
│                 │ - /ponytail least-mechanism diff │ - Drive forward move   │
│                 │ - Negative tests, if repo allows │                        │
├─────────────────┼──────────────────────────────────┼────────────────────────┤
│ COSTLY          │ - Re-architecting shared schema  │ PREPARE ROLLBACK & ASK │
│                 │ - Breaking public API contracts  │ - Formulate 2 options  │
│                 │ - Introducing new dependencies   │ - Prove rollback path  │
│                 │ - Major coordination changes     │ - Await confirmation   │
├─────────────────┼──────────────────────────────────┼────────────────────────┤
│ ONE-WAY DOOR    │ - External resource deletion     │ HARD STOP & CONFIRM    │
│                 │ - Publishing secrets / tokens    │ - Name permanent loss  │
│                 │ - Destructive database drops     │ - Require operator OK  │
│                 │ - Upstream force-pushes          │                        │
└─────────────────┴──────────────────────────────────┴────────────────────────┘
```

**Autonomous Action Rail:**
If a change is classified **`Easy`** and directly resolves a review blocker or test failure to allow
forward movement, **execute the adaptation immediately**. Do not stop, narrate hesitation, or prompt
the operator for permission. Document the pivot cleanly in the final report.

### 2. The Unstuck Anti-Hesitation Engine ([`/unstuck`](../../1-hourly/unstuck/SKILL.md))

Self-invoke the [`/unstuck`](../../1-hourly/unstuck/SKILL.md) interrupt when encountering any of the
four autonomous tripwires:
1. **Two-Turn No-Milestone Tripwire:** Catching yourself asking "Should I test X?" or "Would you like
   me to review Y?" across two turns without advancing the review. *Stop asking; execute the test.*
2. **Tool Exit Code Inertia:** A test or command fails during review verification (e.g. exit code 1 or 2),
   and the agent halts or asks what to do. *Trace the failure with `/debug-mantra`, apply the `Easy`
   foundational fix, and re-run.*
3. **Passive Narration Detection:** Typing phrases like "Waiting for...", "Now I will see...", or "Let
   me know how to proceed" while an in-flight review is pending. *Freeze the cogs and act.*
4. **False Completion Detection:** About to report "LGTM" or "Approved" when acceptance tests were
   skipped, unmutated, or unverified. *Reject completion until evidence is collected.*

**The Five Unstuck Rungs during Review:**
- *Rung 1: Freeze the cogs.* Do not invent new review frameworks, extra wrappers, or meta-analysis.
- *Rung 2: Re-anchor the finish line.* State the observable deliverable: "Verified review report with
  runnable test receipts emitted."
- *Rung 3: Test the blocker.* Is the finding a genuine goal blocker, required correctness/safety,
  or merely polish/cog? (Park polish; queue blockers).
- *Rung 4: Choose one foundational action.* Apply the **No Bandages / No Painkillers Law**: do not
  silence type checks (`@ts-ignore`, `# noqa`), suppress asserts, or bypass gates. Apply the cleanest
  foundational fix.
- *Rung 5: Act once, verify movement, and re-drive.* Execute the move, check that the milestone
  advanced, and resume.

### 3. The Workhorse Defect Resolution Ladder ([`/workhorse`](../workhorse/SKILL.md))

When the review process requires remediating discovered defects:
- **Rung 0: Triage:** Deconstruct all issues into an atomic priority queue (`[Blocker]` → `[Should]` → `[Nit]`).
- **Rung 1: Ground Truth:** Capture raw repros and trace fail paths.
- **Rung 2: Least Mechanism ([`/ponytail`](../../1-hourly/ponytail/SKILL.md)):** Use the standard library
  first, extend existing modules, and produce the shortest working diff. Zero code sprawl.
- **Rung 3: Governance Gate:** Check compliance with `AGENTS.md`, `SOP.md`, `GUIDING-PRINCIPLES.md`,
  and frozen twin guards (`test/gh308-frozen-twin-guard.sh`).
- **Rung 5: Preservation Gate:** Prove preservation invariants before applying any destructive edit.
- **Rung 6: Semantic Verification:** Re-run test suites and verify observable outputs.

---

## Phase 4: Graded Findings & PR Actionability

Structure review findings into four standard citation-backed categories. Every finding must cite
exact `file:line` or symbol references.

### 1. Finding Categories

- 🛑 **`[Blocker]`**: Correctness defects, regressions, security/credential leaks, data loss hazards,
  untested error states, symptom patches hiding root causes, tests that pass on broken code,
  **reinventing a parallel subsystem when an established canonical mechanism exists (North Star violation),
  bypassing established centralized helpers in favor of ad-hoc implementations, or Step N+1 downstream defects
  (orphaned state machines without active readers/pollers, infinite stuck retry loops on failure, or parameter
  generator/constraint inversions producing duplicate entities).**
  *Requires resolution before merge/approval.*
- ⚠️ **`[Should]`**: Architectural gaps, missing test coverage / negative controls, non-optimal complexity,
  missing error logging, unhandled edge cases, **or non-DRY duplicate logic / redundant utility functions.**
  *Strongly recommended improvements.* In a repo that forbids new tests (XYZ-forge: `AGENTS.md` *No new tests*, GH-831), a
  missing-coverage finding asks for an existing suite or a recorded manual check, and a new test file in
  the diff is itself a `[Should]`.
- 💡 **`[Nit]`**: Style, documentation, variable naming, minor comment cleanups. *Non-blocking suggestions.*
- ✅ **`[Pass]`**: Confirmed correct execution paths with firsthand citations, verified test results,
  and passing mutation checks.

### 2. Structured Review Report Schema

Every `/review-code-xyz` report follows this structure:

```markdown
## 🛡️ Code Review Report: <Target / PR Title>

**Verdict:** `Approved` | `Changes Requested` | `Comment`
**Target:** `<Branch / Commit / PR #>` | **Diff Size:** `N lines (+A / -B)`
**Review Mode:** `Ground-Truth Verified (/recon + /debug-mantra)`

| Category | Count | Status |
|:---|:---:|:---|
| 🛑 `[Blocker]` | 0 | All clear |
| ⚠️ `[Should]`  | 1 | Action recommended |
| 💡 `[Nit]`     | 2 | Optional polish |
| ✅ `[Pass]`    | 8 | Verified firsthand |

---

### 🗺️ Recon Map & Blast Radius
- **Entry Points & Callers:** `src/entry.py:42`, `utils/cli.py:105` (all callers verified).
- **State & Data Invariants:** Single-writer verified; SQLite lock budget respected.
- **Contracts & Boundaries:** Public API backward-compatible; no breaking schema drift.
- **Centralized Helpers & DRY:** Canonical helpers used; zero parallel subsystems or reinvention detected.
- **Step N+1 Downstream Verification:**
  - Consumer Hop: Active reader/poller verified at `src/worker.py:110` (no orphaned state).
  - Retry Hop: Next-cycle recovery verified at `src/scheduler.py:75` (no infinite stuck retry loop).
  - Parameter Role: Verified argument acts as constraint (no entity duplication).

---

### 🔬 Meticulous Testing & Verification Evidence
- **Ground Truth Repro:** Verified regression test `test/gh123_regression.py` fails without fix.
- **Mutation Falsification:** Mutated guard at `src/core.py:88`; verified test went **RED** (exit code 1).
- **Negative Controls:** Tested empty input and invalid flags; verified appropriate errors.
- **Reversible Adaptations Executed:** [Detail any `Easy` autonomous fixes applied during review].

---

### 📋 Detailed Findings & Actionable Checklist

#### 🛑 Blockers
- [ ] `src/auth.py:112` — Token comparison uses non-constant-time equality. `[Blocker]`
- [ ] `src/utils.py:45` — Reinvented git lock parsing instead of calling centralized helper `utils/py/rtl.py`. `[Blocker]`

#### ⚠️ Should Address
- [ ] `src/worker.py:45` — Missing negative control test for timeout event. `[Should]`

#### 💡 Nits & Minor Polish
- [ ] `src/utils.py:15` — Clarify docstring regarding return type. `[Nit]`

#### ✅ Verified Passes
- `src/core.py:88` — Thread-safe atomic update verified with concurrent worker test. `[Pass]`
```

### 3. Verdict Delivery: Post to GitHub AND Render On-Screen (mandatory — both, every run)

The review ships twice from the same bytes: once into the chat session, once into the GitHub target.
Posting is not an alternative to the on-screen report, is not optional, and is not gated on operator
approval — a review comment is reversible (it can be edited or deleted), so it is pre-authorized
here. Never pause to ask.

1. **Resolve the target before writing the report.** Resolve the branch's open PR with
   `gh pr view --json number,url -q .number`, or use an explicit `--issue <N>` if given. If neither
   resolves, that is the only sanctioned skip — state `NO GH TARGET — report on-screen only` on
   screen and stop there. Nothing else may skip the post. Post to the PR only
   when the reviewed bytes are its pushed head (`git status --porcelain` empty and `HEAD` equal to
   `gh pr view --json headRefOid`). Otherwise the comment would describe code the PR does not
   contain: report on-screen and state `NOT POSTED: local diff differs from the PR head`.
2. **Write the report to a file first.** Emit the full Phase 4 report as clean GitHub-flavored
   markdown to `temp/review-<PR#|issue#>-<YYYYMMDD-HHMM>.md` (create `temp/` if missing; never the
   repo root). If the repo does not already ignore `temp/` (`git check-ignore -q temp/x`), add
   `temp/` to `.git/info/exclude` first so the report can never be committed. The on-screen report and the posted comment must carry the same content.
3. **Post it without asking, with `--body-file`** (never `--body` — shell quoting silently mangles
   multi-line markdown):
   - PR target: `gh pr comment <PR#> --body-file <report.md>`
   - Issue target: `gh issue comment <N> --body-file <report.md>`
   Do not default to `gh pr review --request-changes` / `--approve`: branch protection may reject
   self-approval and a requested-changes gate blocks the merge; a plain comment always succeeds.
4. **Verify the post landed.** `gh pr comment` prints the comment URL on success — capture it. If no
   URL was captured, re-check via `gh pr view <PR#> --json comments` (an issue target:
   `gh issue view <N> --json comments`) and confirm the report's
   heading line is present. An uncaptured URL is an unverified post.
5. **Render on-screen and close the loop.** Print the full report in the chat session, then the
   verification line `Posted: <comment-url>`. If posting failed, print the full report, the exact
   `gh` error, and `NOT POSTED: <reason>` — a failed post is reported, never silently skipped.

- **Linked Issue Checklists:** If the PR closes issues (`Fixes #123`), verify that all requirements
  in the linked issue or PDDA tracking document (`PROJECT/1-INBOX/` or `PROJECT/2-WORKING/`) are
  satisfied and reflected in the checklist before posting.

---

## Operating Rules & Safety Rails

1. **Lead with the line that survives skimming:** State the verdict, critical blocker count, and
   reversibility assessment in the very first sentence.
2. **Verified beats plausible:** Do not praise code or declare it "clean" without running tests,
   inspecting raw artifacts, or tracing execution paths. An unverified claim is an unknown.
3. **A check that cannot fail is not a check:** Always verify that assertions actually guard what they
   claim by witnessing them fail under mutation.
4. **An empty input passes every check:** Guard against vacuous passes by asserting extracted data
   volume and non-empty artifacts before evaluating results.
5. **Throwaway Full-Clone Isolation (GH-564 rail):** Never run mutation-heavy gates or destructive test
   suites in a primary clone whose state matters or in a linked worktree. Use a disposable full clone
   in `/tmp/` when running suites that touch git remotes, configs, or refs.
6. **Preserve working tree state (GH-527 rail):** Never use `git reset --hard`, `git checkout -- <path>`,
   or tree-wide `git stash` to clean up review experiments.
7. **Frozen Bash twins (GH-308 rail):** Ensure no modifications are made to legacy `.sh` twins under
   `utils/` or `relay-automation/`; all Tier-A runtime logic lives in Python under `utils/py/`.
8. **Builder/Orchestrator Role Split (GH-221 rail):** Claude is the orchestrator and reviewer.
   Autonomous adaptations are restricted to `Easy` reversible fixes and review assertions; do not
   drive headless full-system marathon builds without authorized builder lanes.
9. **The verdict ships twice (pre-authorized):** posting the Phase 4 report to the GitHub PR/issue
   is reversible and pre-authorized — do not pause for operator approval, and do not end a review
   with the report only on-screen when a GitHub target exists. The one sanctioned skip is
   `NO GH TARGET`, stated on screen.
