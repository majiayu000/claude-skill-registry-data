---
name: review-code
description: >-
  Meticulous code and pull request review ladder using /recon and /debug-mantra to test out each
  fix and feature against live ground truth. Supports PR targets under review-PR / --pr <PR#>.
  Loops through /workhorse and /unstuck ladders to autonomously resolve reversible adaptations and
  pivots without stopping for operator permission, driving verified forward movement.
metadata:
  argument-hint: "[diff, branch, file, or --pr <PR#>]"
---

# /review-code (and /review-pr) — Meticulous Ground-Truth Code & PR Review Ladder

`/review-code` is an empirical code and pull request review discipline that treats every proposed
change as a claim requiring firsthand verification. Rather than passively reading a diff and commenting
on style or plausible appearance, `/review-code` actively maps the system's blast radius, tests
fixes and features against live execution, and uses autonomous problem-resolution ladders to drive
forward movement.

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
> 1. **Ingest target & map blast radius (Phase 1 /recon).** Ingest the diff or PR (`review-PR`), map callers, state mutations, contracts, failure paths, and audit adherence to centralized helpers and zero parallel subsystems (DRY).
> 2. **Meticulously test fixes & features (Phase 2 /debug-mantra).** Test every fix against root cause (falsify symptom patches; mutate guards to watch them fail) and verify feature acceptance criteria with measured ground truth and negative controls.
> 3. **Autonomous resolution & anti-hesitation (Phase 3 /workhorse + /unstuck).** If pivots or adaptations are needed, classify reversibility (`Easy`/`Costly`/`One-way door`): autonomously adapt and test `Easy` changes without operator round-trips; freeze cogs and execute foundational unblocking moves.
> 4. **Grade & synthesize verified findings (Phase 4).** Categorize findings (`[Blocker]`, `[Should]`, `[Nit]`, `[Pass]`) with exact `file:line` citations, emit the actionable checklist, and post or report PR verdict.
>
> **Overall Goal:** Every fix and feature verified against live behavior rather than plausible appearance, with reversible issues resolved autonomously and review conclusions grounded in runnable proof.

Then begin work. When `/review-code` (or `/review-pr`) is the active orchestrating skill, this recital
precedes subordinate skill invocations; subordinate skills ([`/recon`](../../1-hourly/recon/SKILL.md),
[`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md), etc.) are then loaded for their mechanics
without conflicting recitals.

---

## The 5-Phase Review Ladder

```text
Phase 0: Target Intake & Scope Resolution  ──► Local diff/branch vs GitHub PR (`review-PR`); isolate refs & context
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
                                               structured report, actionable checklist, and PR verdict / comment
```

---

## Phase 0: Target Intake & Scope Resolution

Resolve the exact target under review. Two primary entry modes are supported:

### Mode A: Local Code Review (`/review-code`)
Used for uncommitted working tree changes, staged diffs, branch diffs against upstream, or targeted files:
```bash
# Review uncommitted changes against HEAD
git diff HEAD

# Review current branch against development baseline
git diff origin/development...HEAD

# Stat changes to size the review blast radius
git diff --stat origin/development...HEAD
```

### Mode B: GitHub Pull Request Review (`review-PR` / `/review-code --pr <PR#>`)
Triggered via `review-PR`, `/review-pr <PR#>`, or `/review-code --pr <PR#>`:
```bash
# Inspect PR metadata, base branch, head branch, author, and description
gh pr view <PR#> --json number,title,body,baseRefName,headRefName,headRefOid,author,state

# Fetch the raw unified diff for the PR
gh pr diff <PR#>

# Inspect linked issues (Fixes #..., Closes #..., GH-...) and project documentation
grep -E "(Fixes|Closes|Resolves) #[0-9]+" <<< "$(gh pr view <PR#> --json body -q .body)"

# Check hosted CI check run statuses
gh pr checks <PR#>
```

**Scope Invariant:**
- Identify the target branch: ensure the PR targets the active WIP branch (`development`), not `main` (per orchestrator rails).
- Size the diff: a targeted bug fix should typically be focused (< 500 lines); large architectural diffs require all 5 recon lanes.

---

## Phase 1: Seam & Blast Radius Recon ([`/recon`](../../1-hourly/recon/SKILL.md))

A diff read in isolation is plausible fiction. Code review requires knowing what callers, state,
contracts, and failure modes are touched by the modification.

Run the five recon lanes across the touched symbols:

| Lane | Focus | Review Inquiry & Verification |
|---|---|---|
| **Lane A. Entry & Call Paths** | Callers & Dispatch | Trace callers of all modified functions. Did call signatures, parameter defaults, or return types change? Are callers in other modules updated? Check CLI shims, hook registries, plugin dispatch, and event handlers. |
| **Lane B. State & Data Flow** | Readers & Writers | What state is mutated? Verify the single-writer invariant. Are SQLite locks, file descriptors, transactions, or cache layers handled? Does this introduce competing write paths or dirty reads? |
| **Lane C. Contracts & Boundaries** | APIs & Protocols | Do changes alter public APIs, CLI flags, JSON schemas, environment variables, or error codes? Check consumers across sibling modules or external repositories. |
| **Lane D. Build, Failure & Tests** | Errors & Coverage | How does this code fail? Trace timeouts, process exits, broken pipes, signal handling (`SIGINT`/`SIGTERM`), and missing input files. What existing test suites cover this seam? |
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

**Graph & Source Lookup:**
- Prefer MCP graph tools (`search_graph`, `trace_path`, `get_code_snippet`) when available to locate callers and dependencies in one call.
- Fall back to targeted ripgrep / file inspection when MCP tools are unavailable.
- **The One Rule:** Every caller cited in the review must exist at `file:line`. Anything unread or unverified is recorded under **Unknowns**, never assumed safe.

---

## Phase 2: Meticulous Ground-Truth Testing ([`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md))

Verified beats plausible. Reviewers must not merely read code; they must test the behavior of
fixes and features against live reality.

### 1. Testing Fixes (Root Cause vs. Symptom-Fix Trap)

When reviewing a bug fix, apply the four debug mantras rigorously:

1. **Mantra 1 — Reproduce reliably:**
   - Verify there is an automated regression test reproducing the original defect.
   - If the regression test is missing, write one or require it before approving.
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
│                 │ - Adding missing negative tests  │                        │
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
  or bypassing established centralized helpers in favor of ad-hoc implementations.**
  *Requires resolution before merge/approval.*
- ⚠️ **`[Should]`**: Architectural gaps, missing test coverage / negative controls, non-optimal complexity,
  missing error logging, unhandled edge cases, **or non-DRY duplicate logic / redundant utility functions.**
  *Strongly recommended improvements.*
- 💡 **`[Nit]`**: Style, documentation, variable naming, minor comment cleanups. *Non-blocking suggestions.*
- ✅ **`[Pass]`**: Confirmed correct execution paths with firsthand citations, verified test results,
  and passing mutation checks.

### 2. Structured Review Report Schema

Every `/review-code` report follows this structure:

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

### 3. PR Actionability (`review-PR`)

When targeting a pull request:
- **Format:** Ensure the output is formatted as clean GitHub-flavored markdown.
- **Automated Posting:** Post the review comment to the PR via `gh pr comment <PR#> --body-file <report.md>`
  or submit formal review via `gh pr review <PR#> --comment / --request-changes / --approve`.
- **Linked Issue Checklists:** If the PR closes issues (`Fixes #123`), verify that all requirements
  in the linked issue or PDDA tracking document (`PROJECT/1-INBOX/` or `PROJECT/2-WORKING/`) are
  satisfied and reflected in the checklist.

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
