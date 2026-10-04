---
name: ss-troubleshooting-workflow
description: End-to-end defect fix — takes an issue link, alert ID, or problem description and orchestrates tier-adaptive root-cause investigation, human confirmation, branching, a fix plan, multi-agent coding with built-in review, and PR/commit delivery. Use only when the user explicitly asks for the full diagnose-to-delivery pipeline, not for diagnosis alone.
---

# Troubleshooting Workflow

Chains the existing `ss-*` skills into a single diagnose-fix-deliver flow:

```
ss-inspect → [Gate: root-cause confirmation] → ss-create-branch
→ ss-plan → ss-coding (built-in review) → review-acceptance loop → ss-create-pr
```

**Core principle: thin orchestration.** This skill never writes code or drafts a plan itself. It
calls the other skills in order, pauses at the gates below, passes each step's output to the
next, and reports progress.

> **Review is not run twice.** `ss-coding` already enforces a post-coding review
> internally and returns a verdict. This workflow never invokes `ss-code-review` separately —
> the review-acceptance loop below is driven entirely by that verdict.

Unlike `ss-feature-workflow`, the root-cause report from `ss-inspect` replaces the proposal, and
**root cause is confirmed before any branch is created** — worth fixing is established before
code is touched.

## When to Run

This is heavy, end-to-end orchestration: it runs a root-cause investigation, creates a branch,
spawns coding agents, runs reviews, and delivers the fix. Only run it when the user explicitly
asks for this skill or clearly wants the full diagnose-to-delivery pipeline. For a plain question
or a diagnosis-only request, do the work directly (or point to `ss-inspect` for diagnosis alone).

## Inputs

- **Problem source** — an issue link, alert ID, or plain-text problem description. If missing,
  ask for one.
- **Delivery mode** — `full` (default) or `lite`. See "Delivery Mode" below.
- **Investigation tier** — `auto` (default), `L0 Local`, `L1 Runtime`, or `L2 Systemic`, forwarded to `ss-inspect`. An explicit higher tier is honored; an explicit lower tier is only a hint and must be promoted when its evidence conditions or risk boundary fail.
- **Skip-gates** — proceed through the root-cause confirmation gate without pausing (not
  recommended — see Iron Rule 2).
- **Decide-autonomously** — resolve ambiguous choices without asking.
- **Worktree preference** — forwarded to `ss-create-branch`.

## Delivery Mode: full vs. lite

The quality gates — root-cause confirmation, TDD, multi-agent code review, verification — are
identical in both modes. Only the start and finish of the *fix* change:

| | `full` (default) | `lite` |
|---|---|---|
| Start | `ss-create-branch` cuts a fix branch (optionally a worktree) | Skipped — develop in place on the current branch |
| Finish | `ss-create-pr` opens a pull/merge request | Skipped — finish with a conventional-commits commit (push optional) and print a change summary |
| Cleanup | `ss-cleanup` removes the branch/worktree after merge | Not applicable |

Mode resolution: an explicit mode input wins; otherwise ask once at the start and use that answer
for the rest of the run. Never persist the choice to a project config file.

## Multi-Repo Routing

Cross-service defects — service A errors, root cause lives in service B, or the fix spans both —
are a frequent multi-repo case. This workflow checks at three points. Full rules in
`../ss-references/multi-repo-detection.md` (this table is a condensed copy; the reference file wins
on conflict).

| Level | Signal | Action |
|---|---|---|
| Deterministic | `ss-plan` produced a **master plan** (`*-master.md` with a `**Repos:**` table of more than one row), or a complete, confirmed root-cause report whose `**Repositories Requiring Fix:**` list has more than one entry | Hand off to `ss-multi-repo-workflow`; a confirmed report's repository scope cannot be downgraded later |
| Heuristic | The issue/alert description explicitly requires committing fixes in two or more services/repos | Ask, showing the evidence; autonomous mode hands off |
| Exclusions | Shared API-contract repo, spec/standards submodules, services merely mentioned as callers/context with no code change, multiple modules inside one repository | Not multi-repo signals |

**Judgment points:**

1. **Entrance, before pre-flight** — scan the issue/alert text for the heuristic signal. On a
   hit, ask (or decide autonomously) and hand off with the original input.
2. **Root-cause gate** — the most reliable point: by the end of the investigation, affected repos
   are part of the evidence chain. Once the user confirms a complete report whose repository list
   has more than one entry, hand off with that report as the planning input. Single-repo
   continuation is forbidden after confirmation.
3. **After build-plan** — a safety net for initially single-repo reports: if `ss-plan`'s scope
   check detects a cross-repo span and produces a master plan, hand off with it. If a previously
   confirmed multi-repo report reaches planning and the plan omits one of its repositories, stop
   and correct the plan instead of downgrading scope.

On hand-off: pass the original input, the root-cause report and any other artifacts, and the
active automation flags to `ss-multi-repo-workflow`; print one line explaining the hand-off and
terminate this workflow.

## Iron Rules

Violating any of these means stopping and explaining to the user:

1. **The orchestrator does no real work** — only call other `ss-*` skills; never edit source or
   draft plans directly.
2. **The root-cause-confirmation gate is on by default and critical** — a wrong root cause causes
   full rework, so a human must confirm it (skip-gates mode can bypass this, but it isn't
   recommended).
3. **Design understanding precedes repair design at every tier** — before `ss-inspect` may write a
   permanent repair proposal, it must explain the complete relevant design and implementation for
   the evidence-derived scope: responsibilities/ownership, end-to-end flow, dependencies,
   invariants, existing mechanisms, healthy analogs, and all affected paths. Tiering may shorten
   the account but never skip this gate or authorize a patch-style fix.
4. **Pre-flight checks ask, they don't abort** — apply the autonomous default only when deciding
   autonomously.
5. **No gate for review — run the loop instead** — see "Review-Acceptance Loop". There is also no
   gate before delivery.
6. **Resumable by identity, never recency alone** — reuse only artifacts explicitly linked to the
   current `**Problem ID:**` and their exact upstream artifact.
7. **Investigation completeness is non-skippable** — skip-gates may bypass the human pause, but it
   never permits anything below `Confidence: HIGH`, an unjustified investigation tier/evidence
   budget, unresolved promotion signals, material evidence gaps, an incomplete design-understanding
   gate, missing canonical `**Affected Paths:**`/`**Repositories Requiring Fix:**` bullet lists, or
   an incomplete repair and verification plan (including canonical `**Violated Invariant:**`,
   `**Owning Boundary:**`, and `**Patch-Style Alternative Rejected:**`) to proceed.
8. **Never relax safety guardrails** — automation flags only affect questions and approvals; they
   never bypass the hard rules built into the underlying skills.

## Pre-flight Checks

Run the source/delivery checks once on start. Evaluate branch/worktree readiness only after a complete report is confirmed, immediately before Step 4. Any unmet check defaults to asking the user, not terminating.

| Check | Trigger condition | Ask the user (default) | Autonomous default |
|-------|--------------------|-------------------------|---------------------|
| Problem source reachable | Input is a URL and no tool is configured to fetch it | [describe how to fetch it]/[switch to a text description]/[abort] | Cannot read the source → abort and report |
| PR-hosting CLI available | Neither `gh` nor `glab` is installed/authenticated | [install/authenticate then continue]/[continue but skip `ss-create-pr`]/[abort] | Continue; skip `ss-create-pr`, prompt to deliver manually |
| Branch/worktree identity (after confirmation) | A candidate branch/worktree exists but is not linked to the confirmed Problem ID, or full mode is still on the default branch | [reuse only with identity evidence]/[create the correct branch]/[abort] | Invoke `ss-create-branch` for the confirmed Problem ID; never mix with unrelated work |

> Whether the investigation needs environment/observability access is decided by `ss-inspect`
> itself — pure code analysis needs none of that.

## Resume Detection

| Step | Completion check | On hit |
|------|-------------------|--------|
| `ss-inspect` | A report's `**Problem ID:**` matches the current issue URL, alert ID, or stable fingerprint; its investigation tier, rationale, evidence budget, and promotions are recorded; confidence is HIGH with no material evidence gaps; the design-understanding gate is complete; canonical `**Violated Invariant:**`, `**Owning Boundary:**`, and `**Patch-Style Alternative Rejected:**` fields are present; and systemic-impact, repository, repair, and verification sections are complete | List matching complete reports and ask whether to reuse (autonomous mode reuses the newest matching one); never reuse a merely recent, under-scoped, or MEDIUM-confidence report |
| `ss-create-branch` | The current branch/worktree is explicitly linked to the same Problem ID (branch slug, issue-linked artifact, or recorded workflow metadata) | Reuse/switch only when identity matches; otherwise create the correct branch |
| `ss-plan` | A structured plan explicitly references the same Problem ID and exact investigation report; contains a complete `Troubleshooting Repair Basis` with matching canonical invariant/boundary/patch-rejection fields and revalidated responsibilities, flow, dependencies, existing mechanisms, and healthy analogs; and maps every `**Affected Paths:**`/`**Repositories Requiring Fix:**` entry to implementation and verification | Reuse, skip; otherwise rebuild it from the report — identity and path coverage alone are insufficient |
| `ss-coding` | Every task in that identity-matched, freshness-valid plan is checked; built-in review is `APPROVED`; full verification matches current HEAD; tree is clean | Skip coding; stale checkboxes or evidence from another plan/ref never count |
| `ss-create-pr` | An open PR is linked to the same Problem ID, branch, and plan, and complete SUCCESS evidence proves current APPROVED review, full verification, clean tree, and `test_verified_ref == delivered_ref` | Report the existing PR link and finish; identity or an open PR alone is insufficient |

## Process

1. **Pre-flight and resume.**
2. **`ss-inspect`** — produce a report-only investigation: derive a stable `**Problem ID:**`,
   classify the evidence/risk boundary as L0 Local, L1 Runtime, or L2 Systemic, and gather only the
   tier-required discriminative evidence while promoting immediately when scope or risk expands.
   Verify the root cause with at least two independent sources, scope understanding by potential
   blast radius, reconstruct the relevant design/invariants, populate the canonical
   `**Affected Paths:**` and `**Repositories Requiring Fix:**` bullet lists, and design the permanent
   repair plus verification. It must not edit code/configuration, mutate runtime state, apply
   mitigation, create a branch, or invoke coding.
3. **Design-understanding completeness check, then root-cause confirmation gate** — first require
   a justified tier and evidence budget with no unresolved promotion signal, `Confidence: HIGH`,
   no material evidence gaps, and a passed design-understanding gate covering responsibilities,
   ownership, end-to-end flow, dependencies, invariants, existing mechanisms, healthy analogs,
   affected paths, and explicit rejection of patch-style repair. Missing evidence or
   impact-scoped understanding always returns to investigation,
   even under skip-gates. Then show the complete conclusion and evidence; pause for **continue to
   fix / re-investigate / abort**. Skip-gates may bypass this human pause only after completeness
   passes. Cap re-investigation at 2 rounds; if the report is still incomplete, stop with the
   evidence gaps and do not offer "continue anyway." Once a complete report is confirmed, its
   repository list is authoritative: more than one entry hands off immediately to
   `ss-multi-repo-workflow` before any branch is created.
4. **`ss-create-branch`** *(full mode only)* — branch from the Problem ID, prefix defaulting to
   `fix/`. Forward the worktree preference. Record the identity linkage, branch name, and worktree
   path.
5. **`ss-plan`** — draft the fix plan from the exact investigation report (including any spec
   delta). The plan must restore the violated invariant at the correct ownership boundary, cover
   every `**Affected Paths:**` bullet, and include compatibility/migration, rollback,
   observability, and regression verification. If it produces a master plan, hand off to
   `ss-multi-repo-workflow` and stop. If it drops a repository from a confirmed report, correct the
   plan before continuing.
6. **`ss-coding`** — execute the fix plan. It already covers TDD and test
   verification, and enforces its own post-coding review before returning a verdict.
7. **Review-acceptance loop** — adjudicate findings and feed valid fixes or invalid-finding reasons
   back into `ss-coding` until its fresh built-in review returns literal `APPROVED`, or escalate.
8. **Delivery** *(full mode)* — call `ss-create-pr`, referencing the original issue in the PR
   description; report the link, plus a reminder that `ss-cleanup` removes the worktree and
   branch after merge. *(lite mode)* — commit with a conventional-commits message referencing the
   issue (push optional), then print a summary.

## Review-Acceptance Loop

After `ss-coding` returns its verdict, this workflow sets no gate and does not pause:

1. Read the verdict.
2. No unresolved findings (approved) → go to delivery.
3. Unresolved findings remain → judge each one: **valid** goes on the to-fix list; **invalid**
   (false positive, out of scope, by design, or suggestion-only) is recorded with a reason and
   left unfixed.
   - **Scope-reduction findings get no leniency**: a finding reporting unimplemented requirements,
     stubbed logic presented as complete, or scope silently deferred ("phase 2", "MVP",
     "simplified for now") must never be judged invalid as "by design" or "out of scope" unless
     the user explicitly approved that scope adjustment earlier — cite that approval.
4. All judged invalid → pass the complete adjudication record back to `ss-coding` and require a
   fresh built-in review of the current diff. Only literal `APPROVED` proceeds to delivery; if it
   cannot be obtained, escalate instead of rewriting the verdict.
5. Valid findings remain → call `ss-coding` again for just those findings → back to step 1.

**Convergence protection:**
- Cap workflow-level rounds at 3, independent of `ss-coding`'s internal rounds; if
  exceeded, escalate with the latest verdict plus the fixed/unresolved lists.
- Track recurrence at the workflow level: the same finding judged valid across 2 consecutive
  workflow rounds after being "fixed" is a stall — escalate.
- Record every "invalid" judgment and its reason. Never force a finding to "invalid" just to pass.

## Edge Cases & Error Handling

| Situation | Handling |
|-----------|----------|
| Input empty | Ask for an issue link, alert ID, or problem description |
| `ss-inspect` cannot pin down a root cause or complete the impact-scoped understanding | Stop before confirmation, explain the evidence gap, and do not force a fix |
| Diagnosis concludes "not a defect / expected behavior" | Report the conclusion, don't create a branch or fix, finish |
| Coding is blocked | Stop, escalate, preserve the scene |
| Review-acceptance loop exceeds max rounds | Escalate |
| No PR-hosting CLI, user chose "continue" | Stop before delivery, prompt to deliver manually |
| Worktree creation fails | `ss-create-branch` falls back to in-place development automatically; record and continue |
| User chooses "abort" at any step | Stop, report progress and artifact paths |

## Examples

```
Run ss-troubleshooting-workflow on https://your-tracker.example/issues/PROJ-7150
Run ss-troubleshooting-workflow with "staging: user login returns 500", deciding autonomously
Run ss-troubleshooting-workflow on ALERT-20260626-001 in lite mode
```
