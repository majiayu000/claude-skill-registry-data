---
name: pair-process-review
description: "Reviews a pull request through 6 sequential phases (5 review + optional merge with parent cascade) — validation, technical review, adoption compliance, completeness, decision — to decide whether it merges. Gate before judgment: a red mechanical gate caps the verdict, and the decision is published as the required `pair-review` check plus the synthesized PR state (to-be-reviewed / ready-to-merge / not-approved), so merge stays blocked until gates are green, the review is approved, and (at risk:red) a human approves explicitly. Not a quick build/test sanity check (use /pair-capability-verify-quality). Composes /pair-capability-classify, /pair-capability-verify-quality, /pair-capability-verify-done, /pair-capability-record-decision, /pair-capability-assess-debt, /pair-capability-assess-security (required), /pair-capability-verify-adoption, /pair-capability-assess-stack (optional)."
version: 0.5.0
author: Foomakers
---

# /pair-process-review — Code Review

Review a pull request through 6 sequential phases (5 review + 1 optional merge). Each phase composes atomic skills and follows the **check → skip → act → verify** pattern for idempotent re-invocation.

## Process Profile

<!-- process-step: id=review -->

Executable form of the **`review`** step. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill                   | Type       | Required | Phase | Purpose                                      |
| ----------------------- | ---------- | -------- | ----- | -------------------------------------------- |
| `/pair-capability-classify`             | Capability | Yes †    | 1     | Risk matrix from the diff (confirm-or-raise) |
| `/pair-capability-verify-quality`       | Capability | Yes      | 2     | Quality gate checking                        |
| `/pair-capability-verify-done`          | Capability | Yes      | 4     | Definition of Done checking                  |
| `/pair-capability-record-decision`      | Capability | Yes      | Any   | Record missing ADR (HALT condition)          |
| `/pair-capability-assess-debt`         | Capability | Yes      | 4     | Flag tech debt items                         |
| `/pair-capability-assess-security`      | Capability | Yes †    | 2     | Security posture verdict + findings (D22)    |
| `/pair-capability-assess-cost`          | Capability | Yes †    | 2     | Cost class verdict + signals (D22)           |
| `/pair-capability-assess-coupling`      | Capability | Yes †    | 2     | Architecture/coupling balance verdict (D22)  |
| `/pair-capability-verify-adoption`      | Capability | Optional | 3     | Full adoption compliance                     |
| `/pair-capability-assess-stack`         | Capability | Optional | 3     | Tech-stack resolution                        |
| `/pair-capability-execute-manual-tests` | Capability | Optional | 6     | Post-merge release validation (manual tests) |

† **Required _when installed_.** `/pair-capability-classify`, `/pair-capability-assess-security`, `/pair-capability-assess-cost` and `/pair-capability-assess-coupling` carry Required = Yes because `/pair-process-review` composes them by default — but all **degrade gracefully**: `/pair-process-review` **warns and continues** when the skill is absent (`/pair-capability-classify` → Step 1.5 Skip; `/pair-capability-assess-security` → Step 2.4; `/pair-capability-assess-cost` → Step 2.5; `/pair-capability-assess-coupling` → Step 2.6; each also under Graceful Degradation), the affected section reading **not assessed**, never HALTing on their absence. "Required" here means _composed by default_, not _a hard prerequisite_, so the flag never contradicts the graceful-skip steps.

## Arguments

| Argument     | Required | Description                                                                                                                                                                                                                                          |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$pr`        | Yes      | PR number or URL to review                                                                                                                                                                                                                           |
| `$story`     | No       | Story ID for requirements validation. If omitted, extracted from PR description.                                                                                                                                                                     |
| `$dispatched` | No       | `true` when this run was **dispatched** (spawned by `/pair-capability-publish-pr`'s caller, an automation loop, a CI job) rather than invoked by a human in an interactive session. Default `false`. Sets the **non-interactive contract** below. Never merges (Phase 6 is unreachable). |

### The non-interactive (dispatched) contract

Two steps of this flow ask a human a question: Step 1.4 ("Proceed with review?") and Step 5.5 ("Merge now or let the author merge?"). In a **dispatched** run there is nobody to answer, so guessing is not an option in either direction — stalling wastes the run, and self-answering Step 5.5 would let the reviewing agent merge its own APPROVED verdict. With `$dispatched: true` (or whenever the run has no interactive human — e.g. the invocation prompt is a bare `/pair-process-review $pr=<n>` from another agent):

- **Step 1.4** — do **not** ask. Emit the same READY block as output and continue directly to Step 1.5.
- **Step 5.5** — do **not** ask, and never self-answer "Merge now". The outcome is always option 2 (**author/human merges**): produce the report and stop after Phase 5.
- **A dispatched run never reaches Phase 6**: it does not merge, does not cascade, does not delete a branch, even on APPROVED with `merge_allowed` true. The human merge gate is the point of the flow ([pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md): "a human still performs the merge; pair never auto-merges"). The dispatch instruction says so explicitly, and this contract holds even if it does not.

Everything else (phases 1–5, the verdict, the `pair-review` publication, the state synthesis) is identical to an interactive run.

## Session State

Maintain throughout the review:

```text
CODE REVIEW STATE:
├── PR: [#PR-NUMBER: Title]
├── Phase: [1-validation | 2-technical | 3-adoption | 4-completeness | 5-decision | 6-merge]
├── Story: [#ID: Title]
├── Review Type: [feature | bug | refactor | docs | config]
├── Issues: [critical: N | major: N | minor: N]
├── Debt Items: [N flagged]
└── Decision: [pending | APPROVED | CHANGES-REQUESTED | TECH-DEBT]
```

## Phase 1: PR Validation (BLOCKING)

### Step 1.1: Load PR Context

1. **Check**: Is the PR already loaded in this session?
2. **Skip**: If yes, confirm PR number and move to Step 1.2.
3. **Act**: Read the PR from the **code host** — a PR/process-review operation, so it reads `code-host`, not `pm-tool` (resolution + routing table: see [way-of-working / PM-tool + code-host resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md); absent `code-host` ⇒ same tool as the PM tool):
   - PR metadata (author, branch, target, status)
   - Changed files and diff
   - PR description and linked story
4. **Verify**: PR loaded and open. If not → **HALT**.

### Step 1.2: Load Story Context

1. **Check**: Is the story already loaded?
2. **Skip**: If yes, move to Step 1.3.
3. **Act**: Extract the story ID from the PR description (the `Refs: <issue-id>` cross-link when the tools are split) or the `$story` argument. Read the story from the **PM tool** — an item read, so it reads `pm-tool`:
   - Acceptance criteria
   - Task breakdown and completion claims
   - Epic context
4. **Verify**: Story loaded with AC. If story not found, warn and proceed with PR-only review.

### Step 1.2b: Sync Deploy Notes on Re-Review (T-2, TT-388, AC2)

1. **Check**: Does the loaded PR body carry a **Deploy Config Declaration** section with at least one non-default field, **or** does the linked PM item already carry a `## Deploy Notes` block? (The pr-template resolves override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md); KB default [here](../../../.pair/knowledge/guidelines/collaboration/templates/pr-template.md).)
2. **Skip**: Neither holds — the PR declares no deploy impact and the item has no block to clear → nothing to do, move to Step 1.3. Note the asymmetry with the PR-side check alone: an existing block must still be reconciled even when the PR now declares nothing, or a reverted declaration would survive as stale state.
3. **Act**: Run the same **upsert-or-delete** `/pair-capability-publish-pr` performs in its Phase 4 step 3 — same heading match (by text, at any level; section ends at the first heading of equal or higher level), same `_Esempio:_`-discarding field parse, same render, same outcomes: replace an existing `## Deploy Notes`, insert one, or **remove** it when the PR's declaration went back to all-defaults — and the same **provenance scoping**: only a block whose `_Fonte:_` names this PR is ever replaced or removed; one written by another PR (or by hand) is kept and reported. Every other section of the item is left untouched. One algorithm, two call sites: this step exists because the author's fix-loop ("Author addresses findings, then re-invokes `/pair-process-review`" — Step 5.5) can push a section change straight to the branch without ever re-invoking `/pair-capability-publish-pr`; a re-review is the next guaranteed point this skill reads the PR body, so it is the natural place to catch a drifted section — whether the fix **added** a new env var or **removed** one.
4. **Verify**: The linked PM item's `## Deploy Notes` reflects the current PR body — present and current, or absent when the PR declares no deploy impact — or the sync failure is reported. Non-blocking — never HALTs the review, and never re-runs a full `/pair-capability-classify`/`/pair-capability-verify-quality` pass just for this.

### Step 1.3: Classify Review Type

1. **Check**: Can the review type be determined from PR labels or story type?
2. **Act**: Classify as `feature`, `bug`, `refactor`, `docs`, or `config` based on:
   - PR labels and title prefix
   - Story type
   - Changed file patterns (e.g., only .md files → docs)
3. **Verify**: Review type set. Determines which validation steps apply.

### Step 1.4: Confirm with Reviewer

Present analysis:

```text
REVIEW READY:
├── PR: [#NUMBER: Title]
├── Author: [name]
├── Story: [#ID: Title | N/A]
├── Type: [feature | bug | refactor | docs | config]
├── Files Changed: [N files, +X/-Y lines]
└── AC: [N criteria to validate]
```

Ask: _"Proceed with review?"_ — **only in an interactive run**. A **dispatched** run (`$dispatched: true`, or no human in the loop) emits this block and continues to Step 1.5 without asking; it never stalls waiting for an answer that cannot come (see the non-interactive contract above).

### Step 1.5: Classification (risk matrix from the diff)

1. **Check**: Has `/pair-capability-classify` already run with `$context: review` on the current PR head commit?
2. **Skip**: If already run — reuse the matrix + tier, move to Phase 2. If `/pair-capability-classify` is not installed → warn (`/pair-capability-classify not installed — no review-time risk matrix`) and move to Phase 2.
3. **Act**: Compose `/pair-capability-classify` with `$context: review` against the PR diff. It applies the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) to the diff footprint, reads the story's refinement-time tier, and produces the review matrix as a **floor** — it confirms or **raises** the tier, and **never lowers** it (D17). The Security relevance and Coupling balance dimensions are reconciled in Phase 2 (Steps 2.4 and 2.6) as `/pair-capability-assess-security` / `/pair-capability-assess-coupling` verdicts land — raise-only.
4. **Verify**: The review matrix + `risk:*` tier are recorded on the **PR description** (matrix as 1 line + `<details>`, D22; tags applied only when a `## Tag Projection` is declared). This PR-description matrix is the **live, editable** copy — if Phase 2 raises Security relevance or Coupling balance, `/pair-process-review` updates it **in place** (Step 2.4), it is not re-emitted by `/pair-capability-classify`. (Phase 5 additionally embeds a point-in-time **snapshot** of this matrix in the Verdict block of the review report; that copy belongs to the **append-only** native review body and is **never** edited in place — a post-submission raise surfaces in the next fresh review, see Step 5.3 / idempotency #5. So "in place" applies only to the editable PR description, not the review body.) A raise to `risk:red` is carried into the Step 5.2 decision. `/pair-capability-classify` HALTs only if the quality model doc (#221) is absent.

## Phase 2: Technical Review

### Step 2.1: Quality Gates

**The gate is the first filter** (R5.4, [pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md)): mechanical checks run before judgment, and a red gate **caps** the outcome of this review.

1. **Check**: Has `/pair-capability-verify-quality` already run on the current PR head commit?
2. **Skip**: If all gates passing on current commit — record results, move to Step 2.2.
3. **Act**: Compose `/pair-capability-verify-quality` with `$scope = all`.
4. **Verify**: Record quality gate results. Failures become review findings (do not HALT — /pair-process-review reports them) **and cap the decision**: with any gate red the review can **never** reach APPROVED / TECH-DEBT and the Step 5.4 synthesis can **never** yield `ready-to-merge` — the judgment review does not override a mechanical failure. Continue the review (the findings are still useful to the author) but carry `Gates: red` into Step 5.2.

### Step 2.2: Code Quality Assessment

1. **Check**: Have code quality issues already been identified in this session?
2. **Skip**: If already assessed — move to Step 2.3.
3. **Act**: Review changed files against:
   - [Design Rules](../../../.pair/knowledge/guidelines/code-design/design-principles/design-rules.md) — do/don't patterns (DR-1, DR-2, ...). A diff **clearly** matching a rule's recognition criteria is a **violation** — cite the rule ID (e.g. "DR-1 — God Module") in the finding, not a generic "improve structure" comment. A **partial or ambiguous** match is a **suggestion**, not a violation — do not count it toward the review decision.
   - [Code design guidelines](../../../.pair/knowledge/guidelines/code-design/README.md) — readability, maintainability, naming
   - [Technical standards](../../../.pair/knowledge/guidelines/technical-standards/README.md) — patterns, conventions
   - Review type-specific concerns (e.g., behavior preservation for refactors, regression tests for bugs)
4. **Verify**: Issues catalogued by severity (critical / major / minor), with rule ID referenced where a Design Rule applies.

### Step 2.3: Architecture & ADR Compliance

1. **Check**: Does the PR introduce new technical decisions (libraries, patterns, technologies)?
2. **Skip**: If no new decisions detected — move to Step 2.4.
3. **Act**: For each new decision, verify:
   - ADR exists in `adoption/tech/adr/`
   - [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) updated
   - Version consistency across workspaces
4. **Verify**: All decisions documented. **Missing ADR → HALT**:
   - Compose `/pair-capability-record-decision` with `$type = architectural` and `$topic` describing the gap.
   - Set review status to CHANGES-REQUESTED until ADR is created.
   - Resume review after ADR is added.

### Step 2.4: Security Assessment

1. **Check**: Has `/pair-capability-assess-security` already run with `$mode: review` on the current PR head commit?
2. **Skip**: If already run — reuse the verdict + findings, move to Step 2.5.
3. **Act**: Compose `/pair-capability-assess-security` with `$mode: review` against the PR diff. It resolves the rule set (KB global + per-service + per-web-app + adoption project rules) and returns a 1-line verdict + collapsed findings, each tagged **introduced** or **pre-existing**. The verdict feeds the five verdict-first Security sections of the review body — **input validation, output handling, authentication, authorization, introduced vulnerabilities** (Step 5.1, per the [code-review-template](../../../.pair/knowledge/guidelines/collaboration/templates/code-review-template.md)).
4. **Verify**: Verdict + findings recorded — feeds the Security sections (Step 5.1) and the **Security relevance** dimension of the Step 1.5 classification matrix (`/pair-capability-classify` folds this verdict in **raise-only** — it may raise the tier, never lower it). **PR-description re-render**: when the verdict raises Security relevance (or the Coupling verdict raises Coupling balance), `/pair-process-review` updates the already-written Step 1.5 **PR-description** matrix **in place** — re-rendering the affected `<details>` row and the 1-line `risk:*` tier so the PR **description** reflects the final, raised tier (the append-only review body is never edited in place — Step 5.3); `/pair-capability-classify` is **not** re-invoked (its Phase-1 run stands, and a raise-only edit needs no recompute). **Tag re-apply**: when a `## Tag Projection` is declared (e.g. `Active: risk`), this in-place Phase-2-originated raise **also re-applies the projected chromatic tag on the PR** — swapping the stale label for the raised tier (e.g. `risk:yellow` → `risk:red`) via the same §5 projection `/pair-capability-classify` uses in its Step 5, applied here by `/pair-process-review` on the raise-only edit — so the PR label matches the raised body tier (AC3); when no projection is declared, only the body matrix is updated and no label is touched. If any **introduced** finding is red → flag explicitly: this is the AC4 signal that drives the CHANGES-REQUESTED decision in Step 5.2. Does not itself HALT — `/pair-capability-assess-security` has no merge authority, this skill's own decision step does.
5. **Degrade**: `/pair-capability-assess-security` not installed → the five Security sections read **not assessed** (never dropped); a manual security read of the diff is still expected.

### Step 2.5: Cost Assessment

1. **Check**: Has `/pair-capability-assess-cost` already run against the current PR head commit?
2. **Skip**: If already run — reuse the class + signals, move to Step 2.6.
3. **Act**: Compose `/pair-capability-assess-cost` against the PR diff. It resolves the cost-signal catalog from the project's stack/architecture/infrastructure adoption and returns the `cost:green|yellow|orange|red` class as a 1-line verdict + collapsed signals table (D22). This is a genuine re-assessment of the diff — never a restatement of the story's refinement-time `cost:*` tag.
4. **Verify**: Class + signals recorded — feed the **Cost** section of the review body (Step 5.1, 1 line + `<details>`). The `cost:*` class is carried as its own dimension of the matrix (never folded into the risk `max`). A **red** cost class surfaces the **blocking human sign-off** requirement in the Verdict area (Step 5.1) and is carried into the Step 5.2 decision. Tag re-apply on the PR follows the same rule as Step 2.4 when `cost` is in the declared `## Tag Projection`. Does not itself HALT — `/pair-capability-assess-cost` has no merge authority.
5. **Degrade**: `/pair-capability-assess-cost` not installed → the Cost section reads **not assessed** (never dropped).

### Step 2.6: Architecture (Coupling) Assessment

1. **Check**: Is `/pair-capability-assess-coupling` installed?
2. **Skip**: If not installed → the **Architecture (Coupling)** section reads **not assessed** explicitly; move to Phase 3.
3. **Act**: Compose `/pair-capability-assess-coupling` with `$scope: diff`. It returns a 1-line balance verdict on the integrations the diff touches (integration strength, socio-technical distance, volatility) + collapsed findings (D22).
4. **Verify**: Verdict + findings recorded — feed the **Architecture (Coupling)** section of the review body (Step 5.1) and the **Coupling balance** dimension of the Step 1.5 matrix (`/pair-capability-classify` folds it in **raise-only**, same in-place body re-render + tag re-apply rule as Step 2.4). Does not itself HALT.

## Phase 3: Adoption Compliance

This phase uses a **4-level graceful degradation cascade** depending on which optional skills are installed:

| Level | /pair-capability-verify-adoption | /pair-capability-assess-stack | Behavior                                                   |
| ----- | ---------------- | ------------- | ---------------------------------------------------------- |
| 1     | Installed        | Installed     | Full adoption compliance + automatic tech-stack resolution |
| 2     | Installed        | Not installed | Full compliance detection, manual stack resolution         |
| 3     | Not installed    | Installed     | Inline tech-stack check only + automatic resolution        |
| 4     | Not installed    | Not installed | Warn developer for manual verification                     |

### Step 3.1: Determine Degradation Level

1. **Check**: Is `/pair-capability-verify-adoption` installed? Is `/pair-capability-assess-stack` installed?
2. **Act**: Set the degradation level (1–4) based on availability.
3. **Verify**: Level set. Proceed with the corresponding behavior.

### Step 3.2: Run Adoption Check

Run the procedure for the level determined in Step 3.1 — see [degradation-levels.md](./degradation-levels.md) for the exact steps of each of the 4 levels.

### Step 3.3: Verify Adoption Results

1. **Check**: Are there unresolved non-conformities?
2. **Skip**: If all resolved or Level 4 (warned) — move to Phase 4.
3. **Act**: Unresolved tech-stack items become review findings. Unresolved architectural gaps are HALT conditions.
4. **Verify**: All items resolved or catalogued as findings.

## Phase 4: Completeness Check

### Step 4.1: Definition of Done

1. **Check**: Has `/pair-capability-verify-done` already run in this session?
2. **Skip**: If already run on current commit — reuse results, move to Step 4.2.
3. **Act**: Compose `/pair-capability-verify-done` with `$scope = all` and `$story` (if available).
4. **Verify**: Record DoD results. Failing criteria become review findings. HALT conditions (missing ADR) propagate.

### Step 4.2: Tech Debt Assessment

1. **Check**: Has `/pair-capability-assess-debt` already run in this session?
2. **Skip**: If already run — reuse results, move to Phase 5.
3. **Act**: Compose `/pair-capability-assess-debt` with `$scope = all`. `/pair-capability-assess-debt` is **output-only** — it returns a report and creates nothing.
4. **Act**: Report the debt items in the review output (Tech Debt section). Debt introduced by the PR is **surfaced, not blocked**: it does **not** HALT the review and **never** blocks the PR. Do **not** auto-create a tech-debt issue.
5. **Act**: If a debt item is worth scheduling, note it as a recommendation for **deliberate** promotion after review via `/pair-capability-write-issue` (with the `tech-debt` label) — a manual, selective act, never automatic.
6. **Verify**: Debt items recorded in the report. High-severity items may inform the review verdict (TECH-DEBT: approve + track separately) but never force CHANGES-REQUESTED on debt grounds alone.

## Phase 5: Review Decision

### Step 5.1: Compile Review Report

1. **Act**: Compile all findings into a **verdict-first** review body following the [code-review-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/code-review-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)). The body is ordered so verdict, tier and cost class read in **~30 seconds** (D22, R6.6):
   - **Verdict** (top): classification tags (`risk:<tier>` · `cost:<class>`) + the decision + a 1-line reason + PR/author/story metadata. Include the **`Classification changed:`** drift note **only** when the review-time tier/cost differs from the story's refinement-time classification — it fires **upward only** (e.g. `risk:yellow` → `risk:red`, raise-only per quality-model §3.2 / D17); a review that would lower a dimension records the reduction as a finding in the collapsed details, never as a silent downgrade. A **red** cost class states the **blocking human sign-off** requirement here.
   - **Assessments** (each a 1-line verdict + `<details>`, "not assessed" when the capability is absent):
     - **Security — input validation, output handling, authentication, authorization, introduced vulnerabilities** (five verdicts from `/pair-capability-assess-security`, Step 2.4)
     - **Cost** — `cost:*` class + signals (from `/pair-capability-assess-cost`, Step 2.5)
     - **Architecture (Coupling)** — balance verdict (from `/pair-capability-assess-coupling`, Step 2.6; "not assessed" when the skill is absent)
   - **Details** (collapsed): findings by severity + positive feedback (Phase 2); functionality / AC coverage; testing & quality gates (from /pair-capability-verify-quality); adoption compliance with degradation level (Phase 3); tech debt (from /pair-capability-assess-debt); documentation (from /pair-capability-verify-done).

### Step 5.2: Make Review Decision

Based on compiled findings:

| Decision              | Condition                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------- |
| **APPROVED**          | No critical or major issues. All AC met. Quality gates pass (a red gate caps the decision — Step 2.1). |
| **CHANGES-REQUESTED** | Critical issues found, missing ADRs, any **introduced** red security finding from `/pair-capability-assess-security` (AC4), failing tests, AC not met. A **red** `cost:*` class does not itself block — it surfaces a **blocking human sign-off** requirement in the Verdict (the human, not the skill, gates on cost). |
| **TECH-DEBT**         | Only minor issues or debt items. Approve current PR, track debt separately.               |

### Step 5.3: Submit Review

The compiled report **is the body of the native review on the code host** — the verdict is the review action; there is **no separate PR comment** (decision Q5, AC2).

The review is submitted on the **code host only** (where it gates the merge). It is **never mirrored** onto the PM tool: the board reaches the outcome through the linked PR reference, so no review state is duplicated. See the [routing table](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md).

1. **Act**: Submit the native review on the code host (for GitHub, per [github-implementation.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/github-implementation.md); another host's implementation guide supplies the equivalent commands), passing the compiled verdict-first report as the review **body**:
   - **APPROVED / TECH-DEBT**: `event = APPROVE`.
   - **CHANGES-REQUESTED**: `event = REQUEST_CHANGES`.
   - MCP-first: `pull_request_review_write` with `method = create`, the report as `body`, and the appropriate `event`.
   - CLI fallback: `gh pr review <number> --approve|--request-changes --body-file <report>`.
   - **Self-authored PR** (solo/self-review): GitHub rejects `APPROVE` / `REQUEST_CHANGES` on your own PR. Submit the same verdict-first report with `event = COMMENT` (`gh pr review <number> --comment --body-file <report>`) — the verdict token (APPROVED / CHANGES-REQUESTED / TECH-DEBT) still leads the body, so the decision and full report are recorded, never lost. See Graceful Degradation.
2. **Act**: On re-review, submit a **fresh** native review — both documented paths append (MCP `create`; `gh pr review` CLI), neither edits a submitted body. GitHub's latest-review-governs semantics mean the newest review carries the verdict while earlier reviews stay as visible history, so re-invocation is safe without editing in place (idempotency).
3. **Verify**: The native review is submitted with the verdict-first body — no separate review-comment artifact exists.

### Step 5.4: Publish the `pair-review` Check & Synthesize the PR State (AC3, AC4, AC5)

The verdict is judgment; the **merge block is mechanical**. This step turns the verdict into the required check and the PR state — see [pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md) for the model and [github-implementation.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/github-implementation.md) § PR state flow for the host commands. Nothing here re-derives criteria: the tier comes from the PR's `risk:*` label via `resolve_tier` and the per-tier requirements come from [quality-model.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) §4 (**no classification criteria in this flow — D18**).

1. **Check**: Does the current head commit already carry a `pair-review` check whose conclusion matches this verdict, and a matching `pr-state:*` label?
2. **Skip**: If yes — nothing to publish, move to Step 5.5 (idempotent re-invocation).
3. **Act — publish the check**: source the shipped [`pr-state.sh`](../../../.pair/knowledge/assets/pr-state.sh) and map the verdict with `review_check_conclusion` (`approved`/`tech-debt` ⇒ `success`, `changes-requested` ⇒ `failure`, anything else ⇒ `pending`). Publish `pair-review` on the **head commit** with that conclusion, through the mechanism the host guide prescribes for an ordinary agent token — on GitHub a **commit status** (the Checks API is writable only by a GitHub App). A `pending` result is never published as resolved — the required check stays unsatisfied so the merge stays blocked. If publication is **refused** (missing scope, no status API), report `pair-review: NOT PUBLISHED — advisory` and continue: the verdict still lives in the native review, but never claim a merge is blocked when it is not.
4. **Act — resolve the requirements for the tier**: read the tier from the PR labels (`resolve_tier`, tags only, **untagged/malformed ⇒ 🔴 fail-safe**), then read that tier's row from quality-model §4 through its `Argument > Adoption > KB default` cascade: reviewer count, SLA, **checklist depth** — `standard` vs `extended` as [quality-model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) §4 defines it (there is no separate extended-checklist artifact: `extended` is the same code-review template with **no section skipped**, "not applicable" written out rather than omitted) — and whether **explicit approval** is required. Record them in the review output; never invent or hardcode a threshold here. At 🔴, state the explicit-approval requirement in the Verdict block so the human reading the PR knows what is still missing (D10).
5. **Act — synthesize the state**: `resolve_pr_state <gates> <verdict> <tier> <explicit-approval>` — `gates` from Step 2.1, `explicit-approval` = a **non-author human** approval recorded on the current head (the pair review itself never counts; on a single-maintainer repo 🔴 therefore needs a second human account — see pr-states.md). Apply the resulting `pr-state:to-be-reviewed` / `pr-state:ready-to-merge` / `pr-state:not-approved` label, removing any other `pr-state:*` label (exactly one at a time); the labels are provisioned once per repository and if absent this step is **non-blocking** (degradation below). A red gate or a 🔴 tier without explicit approval yields `to-be-reviewed`, never `ready-to-merge` (AC2, AC4).
6. **Verify**: The head commit carries the `pair-review` check (or the publication failure is reported), the PR carries exactly one `pr-state:*` label matching the synthesis (or its absence is reported), and the tier requirements are recorded in the output. The label is a **view** — enforcement is the required checks (R5.7); this skill never edits branch protection and never bypasses a check.

### Step 5.5: Determine Next Action

1. **Check**: What was the review decision?
2. **Skip**: If CHANGES-REQUESTED → output review report and stop. Author addresses findings, then re-invokes `/pair-process-review`.
3. **Act — dispatched run**: if this run is **dispatched** (non-interactive — see the contract in Arguments), do **not** ask and do **not** self-answer: the outcome is option 2 below (the human merges). Output the report and stop. A self-answered "Merge now" here would let the reviewing agent merge on its own verdict, which is exactly what the human merge gate forbids.
4. **Act — interactive run**: If APPROVED or TECH-DEBT → ask reviewer:

   > PR approved. Merge now or let the author merge?
   > 1. **Merge now** — proceed to Phase 6
   > 2. **Author merges** — stop here, author re-invokes `/pair-process-implement` Phase 4

   Either route enforces the **same** precondition before merging (`merge_allowed` on the re-synthesized state — Step 6.0 here, Step 4.1 there), so routing to the author never skips the 🔴 explicit-approval requirement.

5. **Verify**: If a human explicitly selected "Merge now" → proceed to Phase 6. Otherwise (including every dispatched run) → output and stop.

## Phase 6: Merge & Close (APPROVED only, optional)

Only reached when a **human reviewer** picked "Merge now" in Step 5.5 of an **interactive** run — a dispatched run stops at Phase 5 by contract (Arguments § non-interactive) — see [merge-and-cascade.md](./merge-and-cascade.md) for the merge-precondition (Step 6.0: `merge_allowed` on the synthesized PR state — HALT unless `ready-to-merge`), merge-strategy, merge-commit, merge, parent-cascade, branch-cleanup, and post-merge-manual-test steps (Steps 6.1–6.6) plus the completion output.

## Output Format

At review decision (Phase 5):

```text
REVIEW COMPLETE:
├── PR:         [#NUMBER: Title]
├── Story:      [#ID: Title | N/A]
├── Decision:   [APPROVED | CHANGES-REQUESTED | TECH-DEBT]
├── Issues:     [critical: N | major: N | minor: N]
├── Security:   [green | yellow | red — N findings, N introduced | not assessed]
├── Cost:       [green | yellow | orange | red | not assessed]
├── Coupling:   [green | yellow | red | not assessed — skill absent]
├── Quality:    [PASS | FAIL — N gates]
├── DoD:        [N/N criteria met]
├── Adoption:   [Level N — summary]
├── Debt:       [N items flagged]
├── Review:     [Submitted as native review body — no separate comment]
├── Check:      [pair-review → success | failure | pending (blocks merge)]
├── Tier req.:  [🟢/🟡/🔴 — N reviewer(s) / SLA / standard|extended checklist / explicit approval: required-and-present | required-and-MISSING | n-a]
└── PR state:   [pr-state:to-be-reviewed | pr-state:ready-to-merge | pr-state:not-approved]
```

At merge (Phase 6): see [merge-and-cascade.md](./merge-and-cascade.md).

## HALT Conditions

Review stops immediately when:

- **PR not found or not open** (Phase 1)
- **Missing ADR for new technical decision** (Phase 2, Step 2.3) — compose `/pair-capability-record-decision`, then resume
- **Unresolved architectural non-conformity** (Phase 3) — must be addressed before decision
- **PR state is not `ready-to-merge`** (Phase 6) — `merge_allowed` fails: gates red, review not approved, or a 🔴 PR without explicit human approval. Report which condition is unmet and stop; never bypass a required check.

On HALT: report the blocker, compose the resolution skill if available, wait for developer.

## Idempotent Re-invocation

See [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). Re-invoking `/pair-process-review` on a partially reviewed PR is safe — per-phase:

1. **PR context**: detects already-loaded PR, skips re-loading.
2. **Deploy Notes sync** (Step 1.2b): an upsert-or-delete — re-running it against an unchanged Deploy Config Declaration section is a no-op write, never a duplicate `## Deploy Notes` block; against a reverted (all-defaults) section it removes the stale block once, then is a no-op.
3. **Phases**: checks which phases completed (via session state or PR review comments). Resumes from first incomplete phase.
4. **Skill compositions**: /pair-capability-verify-quality, /pair-capability-verify-done, /pair-capability-assess-security results cached in session. Not re-run if already passing/current on current commit.
5. **New commits**: if PR updated since last check, re-validates affected phases only.
6. **Review report**: re-review appends a fresh native review (MCP `create` / `gh pr review`); GitHub's latest-review-governs semantics make the newest one carry the verdict while prior reviews remain as history. The report is always the review body, never a separate comment — so no duplicate comment artifact is created.
7. **PR state & check** (Step 5.4): re-publishing is a no-op when the head commit already carries a `pair-review` check matching the verdict and the `pr-state:*` label already matches the synthesis. A **new head commit** (including a force-push) has no check of its own, so the review re-runs on it and the merge stays blocked meanwhile. A tier raised between runs re-synthesizes on the new tier — raise-only, so a re-run never loosens a requirement.
8. **Merge**: detects already-merged PR. Skips Phase 6 if already merged. Resumes parent cascade if merge succeeded but status updates are incomplete.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (optional skill not installed → degrade, never HALT; PM tool not accessible → ask the reviewer directly) for the standard scenarios. Additional cases:

- **/capability-verify-adoption not installed**: Falls back to inline dependency checking against [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md). Warning logged. See degradation cascade (Phase 3).
- **/capability-assess-stack not installed**: Unlisted dependencies flagged as warnings for manual verification. Does NOT HALT.
- **/capability-assess-debt not available**: Skip debt assessment, note in report.
- **/capability-assess-security not installed**: Skip Step 2.4. The five Security sections (input validation, output handling, authentication, authorization, introduced vulnerabilities) read **not assessed** — never dropped. Does NOT HALT; a manual security read of the diff is still expected per [how-to-11](../../../.pair/knowledge/how-to/09-how-to-code-review.md).
- **/capability-assess-cost not installed**: Skip Step 2.5. The Cost section reads **not assessed**. Does NOT HALT.
- **/capability-assess-coupling not installed**: Skip Step 2.6. The Architecture (Coupling) section reads **not assessed**. Does NOT HALT.
- **Self-authored PR (self-review)**: GitHub blocks `APPROVE` / `REQUEST_CHANGES` on your own PR, so the native verdict action is rejected for solo authors. Fall back to `event = COMMENT` (`gh pr review <number> --comment --body-file <report>`), keeping the verdict token at the head of the body — the full verdict-first report is still recorded as a review, so nothing is lost (unlike a rejected APPROVE/REQUEST_CHANGES). Does NOT HALT.
- **Story not found**: Review proceeds with PR-only validation (no AC check). Phase 6 skips parent cascade.
- **Code review template not found**: **HALT** — cannot produce review without template (a required dependency, not optional).
- **PM tool not accessible**: the PR-side work (review, merge) still runs on the code host; the PM-side writes (issue close, parent cascade) are reported as not done rather than guessed. In a single-tool project this is the same tool, so the merge falls back to CLI only.
- **Code host declared but unreachable/unauthenticated**: **HALT** with a setup pointer before any review is submitted — there is nothing to review against. PM-side reads already done are not rolled back.
- **Merge fails** (conflicts, branch protection): Report the failure, ask reviewer to resolve. Do not force-push or bypass protections.
- **Code host has no check-run/required-check API**: publish the `pr-state:*` label only, report `enforcement: advisory — host manual setup required` (see [pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md) degraded mode), and do NOT claim the merge is blocked. Does NOT HALT.
- **`pair-review` publication refused** (Step 5.4 — token lacks the status scope, host rejects the write): report `pair-review: NOT PUBLISHED — advisory` with the host error; the verdict stays in the native review and the state is still synthesized. Enforcement is advisory until publication works — never asserted otherwise. Does NOT HALT.
- **`pr-state:*` label absent / no label API** (Step 5.4): report `pr-state label: not applied` — **non-blocking**, the required checks remain the authority. Does NOT HALT and does not block Phase 6's `merge_allowed` evaluation, which reads the synthesized state, not the label.
- **🔴 PR on a single-maintainer repository, with `Review enforcement: enabled`**: the non-author human approval is unobtainable (GitHub rejects a self-approval), so the state stays `to-be-reviewed` and Phase 6 HALTs. **With enforcement `disabled` — the default — nothing HALTs**: report the tier, the verdict and the synthesized state, say that the 🔴 approval requirement is advisory here, and stop there. A default that blocks is how a single-maintainer repository becomes unmergeable. Report it as a repository constraint — a second human account is required, or `pair-explicit-approval` must deliberately not be a required context there (pr-states.md edge cases). Never self-approve to unblock.
- **/capability-execute-manual-tests not installed**: Skip Step 6.6. Log "Manual test validation skipped — skill not installed." Does NOT block merge.
- **Deploy Notes sync fails or the PM item is unreachable** (Step 1.2b): warn and continue the review — never HALTs. Retried on the next re-invocation (idempotent).
- **No manual test suite**: Skip Step 6.6. Log "No manual test suite found." Does NOT block merge.

## Notes

- This skill **reads code, submits the native review (verdict = the review action), publishes the required `pair-review` check + the `pr-state:*` label, reconciles the PM item's `## Deploy Notes` section with the PR's Deploy Config Declaration — writing, updating or removing it (Step 1.2b, T-2, TT-388) — and optionally merges PRs** — it does not modify source code and posts no separate review comment (AC2).
- **Gate ≠ review** ([pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md)): the mechanical gate is the first filter (Step 2.1) and the judgment verdict never overrides it; the merge block itself is the required check, not this skill's opinion. The `pr-state:*` label is a view — enforcement lives in branch protection (R5.7), which this skill never edits or bypasses.
- **Per-tier requirements are read, never invented** — reviewer count, SLA, checklist depth, and the 🔴 explicit-approval requirement come from [quality-model.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) §4 through its `Argument > Adoption > KB default` cascade (D10). The tier comes from the PR's `risk:*` label (`resolve_tier`, tags only, untagged ⇒ 🔴 fail-safe): **this flow contains no classification criteria** (D18).
- Review phases are sequential — each phase builds on findings from prior phases.
- The reviewer can stop between phases; re-invoke to resume (see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md)).
- Output follows [code-review-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/code-review-template.md) — the template defines structure, /pair-process-review fills it with findings.
- HALT on missing ADR is inherited from [how-to-11](../../../.pair/knowledge/how-to/09-how-to-code-review.md) — this is a business rule, not a skill limitation.
- **Parent cascade is best-effort** — if sub-issue queries fail, the skill reports which updates need manual attention.
