---
name: ss-multi-repo-workflow
description: Executes a requirement that spans multiple git repositories — plans once, then runs one repository-scoped coding unit per repository (each running ss-coding-workflow from that repo's real working root), batched by dependency order, and consolidates all resulting PRs into one cross-repo report. Use only when explicitly invoked or handed off from a single-repo workflow's multi-repo detection.
---

# Multi-Repo Workflow

Executes a requirement that spans **multiple git repositories**: plan once, then run one
**repository-scoped execution unit per repository** (each running `ss-coding-workflow` from that
repo's real working root), batched by dependency order, and finally consolidate all pull requests
into one cross-repo report.

**Why repository runners.** Every unit must start with the target repository as its real working
root so it loads that repo's own project instructions, specs, skills, and git state. Use a native
child runner only when the host can guarantee an independent absolute working directory, fresh
repository context, nested implementation/review delegation, observable lifecycle, and exact run
identity. Otherwise use a fresh headless process. Extra file access without repository-scoped
context is not sufficient.

```
Orchestrator (this session)
  ├── in repo-a: run ss-coding-workflow <plan-a>, autonomous, lite/full     ┐ batch 1 (parallel)
  ├── in repo-b: run ss-coding-workflow <plan-b>, autonomous, lite/full     ┘
  └── in repo-c: run ss-coding-workflow <plan-c>, autonomous, lite/full       batch 2 (after batch 1)
```

**Core principle: thin orchestration.** This skill never writes code or edits source/configuration
inside target repositories. Its only target-repository write is distributing the generated
sub-plan artifact before execution. Planning-stage work is delegated to other `ss-*` skills in
this session; execution-stage work is delegated to per-repo runners.

## When to Run

Only run this when the user explicitly asks for it, or a single-repo workflow hands off to it
after multi-repo detection (see `../ss-references/multi-repo-detection.md`). Do not auto-trigger it
for ordinary single-repo work.

## Inputs

- **Planning input**, one of:
  - a path to an existing master plan (see "Input Type Detection"), or
  - a requirement/PRD link, issue link, or plain-text requirement — triggers the planning stage
    first.
- **Delivery mode** — `full` (default) or `lite`, forwarded to every per-repo
  `ss-coding-workflow` invocation. See `ss-coding-workflow`'s "Delivery Mode" section; the choice
  is made once here and applied uniformly across repos.
- **Skip-gates** — skip the manual multi-repo execution gate.
- **Decide-autonomously** — resolve clarification questions without pausing; also forwarded to the
  planning-stage skills.
- **Runner adapter** — `auto` (default), `native child`, or `headless process`. `auto` selects a
  native child only when all readiness guarantees in this skill can be proven; otherwise it uses a
  headless process. Never treat mere access to another directory as repository-scoped context.
- **Allow unattended edits** (optional, default off) — authorize the selected runner's unattended
  edit mode in trusted environments only.

## Iron Rules

Violating any of these means stopping and explaining to the user:

1. **The orchestrator does no real work** — during planning, only call other `ss-*` skills. During
   execution, its sole target-repository write is copying each generated sub-plan to that repo's
   plan directory; otherwise it only launches/monitors runners and collects results. Never edit
   source, configuration, or any other project-owned file in a target repository.
2. **Repository runners do not own product decisions** — launch them in unattended mode. A native
   child may surface a needs-attention event, but this parent session owns every clarification and
   scope decision: before launch at the multi-repo gate or after an escalation.
3. **Batch order is a hard constraint** — repos in the same batch may run in parallel; batches run
   strictly in the master plan's dependency order. A consumer of an API never starts before its
   provider's batch completes.
4. **Distribute sub-plans before launching** — copy each repo's sub-plan into that repo first; a
   runner never reads plans across repositories.
5. **Verify every repository's result individually** — PR link, verdict, and task completion for
   each repo. A failed, timed-out, or blocked repo must never be hidden inside an aggregate
   report.
6. **Full-scope delivery — no unauthorized reduction** — every repository and every task
   completes, or is explicitly escalated. Never settle for "N of M repos done" unless the user
   explicitly approved dropping scope; record any such approval and repeat it in the final report.
7. **Never modify the internal behavior of orchestrated skills** — every runner uses stock
   `ss-coding-workflow`.
8. **Adapter readiness fails closed** — before launch, prove the selected adapter's cwd, context,
   nested-delegation, lifecycle, result, and exact-identity guarantees. If any guarantee is absent,
   stop or obtain explicit approval to select another adapter; never silently fall back mid-run.
9. **The security boundary is external** — run only on a trusted dev machine or container. A
   per-repo cwd/worktree is a change-isolation boundary, not a security sandbox; protection comes
   from feature branches, PR review, and branch protection.

## Input Type Detection

| Input | Detection | Handling |
|-------|-----------|----------|
| Master plan | `docs/plans/*-master.md`, header has a `**Repos:**` table with a valid per-repo Base SHA matching each sub-plan's `**BASE_SHA:**`; when it carries a Problem ID/investigation report, the complete troubleshooting repair-basis checks below also pass | Skip planning only after validation; an old or malformed troubleshooting plan set returns to `ss-plan` |
| Confirmed investigation report | Complete report has a matching `**Problem ID:**` and more than one `**Repositories Requiring Fix:**` entry | Treat its repository scope as authoritative; skip proposal and run `ss-plan` from the report |
| Requirement / PRD / issue | Anything else (link, text, non-master file) | Run the planning stage first, producing a master plan |
| Hand-off from a single-repo workflow | Invoked with identity-linked artifact paths and detection evidence | Probe artifacts, reuse only exact identity matches, continue from the first missing stage |

A troubleshooting master plan is valid only when its Problem ID and investigation-report path match
the report; `**Violated Invariant:**`, `**Owning Boundary:**`, and
`**Patch-Style Alternative Rejected:**` match the report's repair basis; every report repository has
one sub-plan; and every sub-plan contains a complete `Troubleshooting Repair Basis` with an
implementation-and-verification mapping for each applicable `**Affected Paths:**` entry. Validate
this before skipping planning and again before launch.

## Pre-flight Checks (execution stage)

Run before launching any repository runner. Any unmet check defaults to asking the user, not
terminating.

| Check | Trigger condition | Ask the user (default) | Autonomous default |
|-------|--------------------|-------------------------|---------------------|
| Repo paths valid | A repo entry's local path is missing, not a git repo, or its remote doesn't match | [give the correct path]/[clone it]/[remove this repo from scope, with explicit confirmation] | Abort and report — the orchestrator must never decide to drop a repository on its own |
| Plan baseline metadata valid | A master row lacks/resolves an invalid Base SHA, or it differs from that repo sub-plan's canonical `**BASE_SHA:**` | [rerun `ss-plan`]/[correct from verified planning evidence]/[abort] | Rerun `ss-plan`; each repository runner independently enforces relevant-drift freshness before dispatch |
| Troubleshooting repair basis valid | A Problem ID/investigation report is present but master metadata mismatches it, a report repository lacks a sub-plan, or any sub-plan lacks the complete design/invariant/owning-boundary/patch-rejection/affected-path matrix | [rerun `ss-plan` from the report]/[abort] | Rerun `ss-plan`; never execute or resume a patch-style plan set |
| Repo has project configuration | The target repo has no project-instructions file for AI agents | [set it up there first]/[continue without it, degraded] | Continue degraded; flag the repo in the final report |
| Clean working tree, fresh default branch | `git status` in that repo is non-empty, or its default branch is behind its remote | [stash/commit then continue]/[skip updating this repo] | Stash, then continue; flag in the report |
| Runner adapter ready | The selected adapter cannot prove real per-repo cwd, fresh project context/skills, nested delegation, terminal lifecycle, structured result capture, or exact resume identity | [repair readiness]/[explicitly choose another adapter]/[abort] | Abort and report; never silently fall back |
| PR-hosting CLI available in each repo | Neither `gh` nor `glab` works there | Same options as the other workflows | Continue with a verified local commit; report `delivery` as that commit and mark the PR pending for manual creation |

**Repository location convention:** the master plan's local-path column is authoritative. When
planning generates it, paths are probed as siblings of the current repo (`../<repo-name>`);
anything unresolvable is asked about, never guessed.

## Resume Detection

| Stage | Completion check | On hit |
|-------|-------------------|--------|
| Planning (proposal) | Hand-off provides a proposal explicitly linked to the current original-input identity | Reuse, skip; recency alone is insufficient |
| Planning (master plan) | Input/candidate explicitly links to the current identity and exact proposal/investigation report; a troubleshooting plan also passes the master/sub-plan repair-basis validation above | Reuse and skip planning only after validation; otherwise rerun `ss-plan` from the exact upstream artifact |
| Per-repo execution | The identity-matched branch has an open PR linked to its sub-plan, plus a valid identity-matched `---SS-RESULT---` block or reconstructable equivalent evidence satisfying every current SUCCESS invariant | Revalidate the structured evidence, then mark done and collect the PR link; an open PR alone is never completion |
| Per-repo partial | The identity-matched sub-plan has checked tasks and the adapter's exact execution identity is recorded | Resume that exact execution; never select an ambiguous "latest" session |

## Process

1. **Pre-flight and repo location.**
2. **Planning stage** *(only when the input is not a master plan)* — run in this session, since
   planning needs the global view and no process nesting is involved:
   1. For large requirements, draft a proposal with `ss-proposal` (with its own approval gate,
      skippable via skip-gates). The proposal's repo list feeds the master plan. Skip this step for
      a confirmed investigation report; that complete report is the design input.
   2. Run `ss-plan` — its scope check detects the multi-repo span and produces the **master plan
      plus per-repo sub-plans**. Shared API contract changes are handled inside the proposal/plan
      flow as usual (contract-first: provider repos land in earlier batches).
   3. If `ss-plan` does *not* produce a master plan: for an ordinary requirement, tell the user
      this is single-repo work and hand back to `ss-coding-workflow`/`ss-feature-workflow`; for a
      confirmed multi-repo investigation, fail closed and correct the plan because its verified
      repository scope cannot be downgraded.
3. **Gate: multi-repo execution confirmation** — default on; skip-gates bypasses it. Changing code
   in N repositories at once is a large blast radius, so show and pause for approval on:
   - the repository list with local paths and remotes;
   - batches and dependency order;
   - per-repo sub-plan task counts;
   - the number of parallel repository runners and the selected adapter/readiness evidence;
   - detection evidence, when arrived via hand-off.

   Options: **continue / adjust (edit the master plan, then re-show) / abort**.
4. **Distribute sub-plans** — copy each repo's sub-plan into that repo's plan directory, keeping a
   descriptive, slug-based filename. The plan travels with the repo's PR — reviewable and
   traceable. The master plan stays in the originating repo.
5. **Launch a batch** — for each repo in the current batch, start one runner with an absolute
   repository cwd, fresh repository context, stock `ss-coding-workflow`, the distributed sub-plan,
   and a captured exact execution identity. Defaults: **at most 3 concurrent repos per batch**
   (each runner may itself launch several implementer subagents — count the total against machine
   and API rate limits; split a larger batch into sub-batches), **per-repo timeout of 60 minutes**
   (both overridable by asking, or by the autonomous defaults). A process adapter captures its
   exit code, session ID, and per-repo log; a native child adapter captures its run/task ID,
   lifecycle state, and structured output.
6. **Monitor and collect** — require three signals together for every adapter: **terminal lifecycle
   state + valid normalized `---SS-RESULT---` block + timeout not exceeded**. A process exit code
   contributes to its terminal state but never replaces the result contract. Missing, malformed,
   contradictory, or non-terminal output counts as failure; preserve its log/lifecycle evidence.

   **Normalize and validate the result before trusting its status:**
   - require every shared field from `ss-coding-workflow`: status, exact persisted input identity,
     branch, delivery location, delivered commit ref, constrained review verdict, final
     test-verified ref, structured test
     evidence, task count, changed files, structured commands run, residual risks, and
     clean-worktree state;
   - parse every object/array field as valid JSON and reject unknown enum values or malformed
     7–64-character lowercase hexadecimal commit refs;
   - accept `SUCCESS` only when `input_identity` exactly matches the distributed sub-plan identity,
     review is `APPROVED`, all tasks are complete, delivery is present, `delivered_ref` is the
     commit at that delivery location, `test_verified_ref == delivered_ref`,
     the passed full-test command appears in both test evidence and commands run, changed files are
     non-empty, the worktree is clean, and no blocker is present;
   - require a blocker for `FAILED`/`BLOCKED`; prose outside the block never overrides missing or
     contradictory structured evidence.

   **Failure handling, per repo:**
   1. Read the adapter's terminal evidence; classify the cause.
   2. Auto-resumable (transient error, missing context the orchestrator can supply) → resume the
      recorded exact execution identity with a corrective instruction, at most twice. Never use an
      ambiguous "latest" or cwd-global continuation in parallel execution.
   3. Not auto-resolvable (blocked, root-cause ambiguity, permission denial) → **pause the
      workflow and escalate to the user** with that repo's log summary and the status of every
      other repo. Repos already running in the same batch keep going to completion — never kill
      healthy work.
   4. A repo the user decides to abandon must be recorded as an approved scope reduction and
      flagged in the final report.
7. **Repeat** for remaining batches once the current one fully succeeds (or the user accepts a
   partial result and unblocked later batches can proceed).
8. **Converge:**
   1. **Cross-link PRs** — for every PR created, update its description to list every sibling PR
      link plus a reference to the master plan.
   2. **Consolidated report:**

      ```markdown
      ## Multi-Repo Execution Report

      | Repo | Branch | PR | Review Verdict | Tests | Tasks |
      |---|---|---|---|---|---|
      | payment-service | feat/refund-6297 | https://github.com/example/payment-service/pull/456 | APPROVED | 18 passed @def456 | 3/3 |
      | order-service | feat/refund-6297 | https://github.com/example/order-service/pull/123 | APPROVED | 42 passed @abc123 | 5/5 |

      ## Needs Human Sign-off
      (collected from each runner's manual-verification checklist, grouped by repo)

      ## Suggested Merge Order
      1. payment-service #456 (API provider, batch 1)
      2. order-service #123 (batch 2)

      ## User-Approved Scope Reductions
      (none / listed one by one, quoting the user's own words)
      ```

## Repository Runner Contract

Each repository runner starts from the target repo's real working root and executes something
equivalent to:

```
Run ss-coding-workflow on docs/plans/<sub-plan-file> in mode=<full|lite>, deciding
autonomously, using branch <unified-branch-name>.
```

Requirements for every adapter:

- **Real absolute cwd and fresh repository context** — load the target repo's project instructions,
  specs, skills, and git state before executing the plan.
- **Unattended execution** — no child-owned product decisions. A native attention channel may ask
  the parent for help; a headless process must use closed/redirected stdin.
- **Nested delegation** — the runner must be able to execute `ss-coding-workflow`'s implementer and
  reviewer fanout without delegating back into another repository.
- **Explicit edit/network permissions** — grant only what implementation and PR delivery require,
  and only in a trusted environment.
- **Observable terminal lifecycle** — capture exit/lifecycle status and enough per-repo evidence to
  diagnose a failure.
- **Exact execution identity** — record the process session ID or native run/task ID at launch and
  use only that identity for resume.
- **Normalized structured result** — preserve the exact `---SS-RESULT---` contract emitted by
  `ss-coding-workflow`.

The unified branch name comes from the master plan; passing it explicitly to every runner is what
makes every repository use the same branch name.

**A note on isolation:** don't rely on a runner's own sandbox as a security boundary when agent
sessions are nested. Treat the trusted-machine/container boundary in Iron Rule 9 as the real
protection.

## Edge Cases & Error Handling

| Situation | Handling |
|-----------|----------|
| Input empty | Ask for a master plan path, PRD, or requirement |
| Master plan's repo table has only one row | Not multi-repo; hand back to `ss-coding-workflow` |
| `ss-plan` produced no master plan | Single-repo work; hand back |
| Repo path unresolvable and the user is unreachable (fully autonomous run) | Abort and report — never drop a repo autonomously |
| Unified branch name already exists in a repo with unrelated commits | Ask: reuse / new suffix / abort; autonomous default: create a suffixed branch and record it |
| Runner never reaches a terminal lifecycle state | Stop it at the timeout, treat it as failed, and preserve its log/lifecycle evidence |
| Partial batch success, escalation declined ("continue anyway") | Continue later batches only for repos that don't depend on the failed one; the failed repo and its dependents stay blocked and appear in the report |
| No PR-hosting CLI in a repo | That sub-repo still codes and records a verified local-commit delivery; report lists "PR pending, create manually" |

## Examples

```
Run ss-multi-repo-workflow on docs/plans/2026-07-03-refund-master.md
Run ss-multi-repo-workflow on https://your-tracker.example/issues/PROJ-6297, deciding autonomously
Run ss-multi-repo-workflow with "refund flow spanning the order and payment services", fully autonomous, using the available headless-process adapter
```
