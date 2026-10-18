---
name: review-pr-xyz
description: >-
  Ground-truth GitHub pull request review that first confirms the PR's claims and the request
  behind it are valid (the bug is real, the issue asks for this, it has not already landed), then
  maps blast radius with /recon and tests every fix and feature with /debug-mantra. Report-only:
  posts graded findings to the PR and renders them on-screen; never pushes, approves or merges.
  Trigger on /review-pr-xyz <PR#>, "review PR #N", or "review this pull request". Local diff or
  branch? Use review-code-xyz. Multi-model panel review? Use review-xyz.
metadata:
  argument-hint: "<PR# or PR URL> [--deep]"
---

# /review-pr-xyz — Claim-Validated Ground-Truth PR Review

A pull request is a bundle of claims: *this bug exists*, *this change fixes it*, *the linked issue
asks for this*, *tests pass*, *no behavior change outside X*. A review that only reads the diff
checks whether the code matches the description and never asks whether the description is true.
A PR can implement its description perfectly and still be wrong to merge.

`/review-pr-xyz` checks the claims first, then reviews the code against what is actually true. It
reuses the ladder of [`review-code-xyz`](../review-code-xyz/SKILL.md) (Phase 1 recon lanes, Phase 2
ground-truth testing, Phase 4 grading and delivery) by reference. Those definitions live there
once and are not copied here.

**Which review skill:** a GitHub PR → this skill. A local diff or branch →
[`review-code-xyz`](../review-code-xyz/SKILL.md) (which also fixes reversible issues). A multi-model
reviewer panel → [`review-xyz`](../review-xyz/SKILL.md).

---

## Recite this — verbatim, as the first thing in your first response

> **Review-PR Discipline:**
> 1. **Ingest the PR (Phase 0).** Metadata, head SHA, diff, linked issues, CI, and a disposable full clone at the PR head.
> 2. **Validate the claims before the code (Phase 1).** List every claim the PR and its linked issue make; verify each against live ground truth — reproduce the bug on the base, read the issue, check it has not already landed. An invalid core claim ends the review early.
> 3. **Map the blast radius (Phase 2 /recon).** Run the review-code-xyz recon lanes, including Step N+1 and the DRY audit.
> 4. **Test fixes and features (Phase 3 /debug-mantra).** Run review-code-xyz's Phase 2 ground-truth tests in the disposable clone: mutate to red, negative controls, measured outputs.
> 5. **Report, never fix (Phase 4).** Grade findings with `file:line` citations, post to the PR with `--body-file`, verify the comment URL, and render the same report on-screen. Never push, approve, or merge.
>
> **Overall Goal:** A verdict on whether the PR should merge, grounded in verified claims and runnable proof, delivered without touching the author's branch.

Then begin work. Subordinate skills ([`/recon`](../../1-hourly/recon/SKILL.md),
[`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md)) are loaded for their mechanics without
their own recitals.

---

## The Ladder

```text
Phase 0: PR Intake & Isolation        ──► gh metadata, head SHA, diff, linked issues, CI; disposable full clone
                 │
                 ▼
Phase 1: Claim Validation             ──► every claim → Valid / Invalid / Unverifiable, with evidence
                 │                        invalid core claim → skip to Phase 4 (Changes Requested)
                 ▼
Phase 2: Blast Radius (/recon)        ──► review-code-xyz Phase 1: Lanes A–E + Step N+1
                 │
                 ▼
Phase 3: Ground Truth (/debug-mantra) ──► review-code-xyz Phase 2: repro → trace → mutate-to-red; features → negative controls
                 │
                 ▼
Phase 4: Graded Report (report-only)  ──► review-code-xyz Phase 4 schema + a Claim Validation section; post + render
```

---

## Phase 0: PR Intake & Isolation

```bash
# Metadata, including the exact head SHA the review is about
gh pr view <PR#> --json number,title,body,baseRefName,headRefName,headRefOid,author,state,isDraft,url

# The diff and its size
gh pr diff <PR#>
gh pr view <PR#> --json additions,deletions,changedFiles

# Linked issues: closing keywords in the body plus GH-<n> mentions in title, body and commits
gh pr view <PR#> --json closingIssuesReferences,commits

# Hosted CI state
gh pr checks <PR#>
```

**Isolation (required before running anything):** clone the repository fresh into a throwaway
directory under `$TMPDIR` and check out the PR head there (`gh pr checkout <PR#>` inside that
clone). Every reproduction, mutation and test run in Phases 1–3 happens in that clone. Never run
them in the operator's primary clone or a linked worktree (GH-564 rail), and never push from it.

**Scope invariants:**
- The PR should target `development`, not `main`. A PR to `main` that is not a promotion is a
  `[Blocker]`.
- Record `headRefOid`. If the head moves during the review, say so in the report and review the
  SHA you actually tested.
- A draft PR is reviewed the same way; say "draft" in the verdict line.

---

## Phase 1: Claim Validation

Extract every claim from the PR title, body, commit messages and each linked issue, then verify
each one against ground truth, not against the diff. Start from the claim the PR's value rests on
(the **core claim**).

| Claim type | Example | How to verify |
|---|---|---|
| **Defect claim** | "X crashes when Y" | Reproduce it on the **base** branch in the disposable clone ([`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md) Mantra 1). Not reproducible on base → the fix has nothing to fix. |
| **Request claim** | "Implements #123" | Read the issue itself: does it ask for this, at this scope? Check the issue's state and any later comments that changed the ask. A PR solving a different problem than its issue is Invalid. |
| **Novelty claim** | (implicit in every PR) | Check the change has not already landed: `git log origin/<base> --oneline -S '<key symbol>'`, related merged PRs (`gh pr list --state merged --search '<terms>'`), and the repo's roadmap or ledger. Already landed → duplicate. |
| **Evidence claim** | "Tests pass", "verified locally", "CI green" | Re-run the named suite in the clone, or read the actual check run (`gh pr checks`). A claimed run you cannot reproduce or find is Unverifiable, not Valid. |
| **Scope claim** | "Docs only", "no behavior change", "refactor" | Check the diff: does it touch runtime code, defaults, schemas, flags or error codes? Any behavior change under a no-behavior-change claim is a `[Blocker]`. |
| **Root-cause claim** | "The cause was Z" | Trace it ([`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md) Mantra 2). A fix at the crash site while the bad state comes from upstream is the Symptom-Fix Trap. |

Give every claim one verdict:
- **Valid**: verified firsthand, evidence cited (command + result, or `file:line`).
- **Invalid**: contradicted by evidence. Cite the evidence.
- **Unverifiable**: cannot be checked here (needs credentials, hardware, production data). It goes
  under **Unknowns** in the report and is never treated as Valid.

**Early exit:** if the core claim is Invalid (the bug does not reproduce on the base, the issue asks
for something else, or the change already landed), skip Phases 2–3. Go straight to Phase 4 with
verdict `Changes Requested`, the claim evidence as `[Blocker]` findings, and a one-line note that
the code was not reviewed in depth because the premise failed. An invalid secondary claim (for
example an overstated "tests pass") does not end the review; it becomes a finding.

---

## Phase 2: Blast Radius ([`/recon`](../../1-hourly/recon/SKILL.md))

Run [`review-code-xyz`](../review-code-xyz/SKILL.md) **Phase 1 — Seam & Blast Radius Recon** across
the PR's touched symbols: Lanes A–E (callers, state and data flow, contracts, failure and tests,
centralized helpers and DRY) and the Step N+1 downstream checks. Its evidence standard applies:
every caller, consumer and callee cited exists at `file:line`; anything unread goes under
**Unknowns**.

Use the Phase 1 results to focus this: a validated defect claim tells you which fail path the
recon must cover; a scope claim tells you which contracts must be unchanged.

---

## Phase 3: Ground Truth ([`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md))

Run [`review-code-xyz`](../review-code-xyz/SKILL.md) **Phase 2 — Meticulous Ground-Truth Testing**
in the disposable clone:
- **Fixes:** the repro from Phase 1 now passes at the PR head; the regression check fails when the
  fix is mutated (*a check that cannot fail is not a check*); the fix sits where the invariant
  breaks, not where it was noticed.
- **Features:** run the entry points directly; falsify the acceptance criteria (*an empty input
  passes every check*); negative controls, idempotency, and concurrency where relevant.

Mutations are experiments: make them in the disposable clone, record the result, discard them.
None of them is committed or pushed.

---

## Phase 4: Graded Report (report-only)

Grade with the [`review-code-xyz`](../review-code-xyz/SKILL.md) **Phase 4** categories (`[Blocker]`,
`[Should]`, `[Nit]`, `[Pass]`) and report schema, with two changes:

1. Add a **Claim Validation** section directly under the summary table:

   ```markdown
   ### 🧾 Claim Validation
   | Claim | Source | Verdict | Evidence |
   |:---|:---|:---:|:---|
   | "X crashes when Y" (core) | PR body | Valid | Reproduced on base `abc1234`: exit 1, `KeyError: 'y'` |
   | Implements #123 | PR body | Valid | #123 asks for exactly this scope |
   | "Tests pass" | PR body | Unverifiable | Suite needs a staging token; not re-run |
   ```

2. Replace "Reversible Adaptations Executed" with **Suggested Fixes**: concrete, `file:line`-anchored
   changes for the author. Nothing is applied.

Header line: `**Review Mode:** Claim-Validated Ground Truth (/recon + /debug-mantra), report-only`
and `**Head reviewed:** <headRefOid>`.

**Delivery** follows [`review-code-xyz`](../review-code-xyz/SKILL.md) Phase 4 "Verdict Delivery",
posting to this PR: write the report to `temp/review-<PR#>-<YYYYMMDD-HHMM>.md` (kept out of git),
post with `gh pr comment <PR#> --body-file <file>` without asking (a comment is reversible and
pre-authorized), capture and verify the comment URL, then render the same report on-screen followed
by `Posted: <url>`. A failed post prints the report, the exact `gh` error, and `NOT POSTED: <reason>`.

---

## Operating Rules & Safety Rails

1. **Lead with the verdict.** First sentence: verdict, blocker count, and whether the core claim held.
2. **Claims before code.** Never start Phase 2 until every claim has a verdict.
3. **Report-only.** Never commit to, push to, force-push, rebase or edit the PR branch. Never
   `gh pr review --approve` or `--request-changes`, never `gh pr merge`, never close the PR or its
   issues. The only write is the review comment.
4. **Disposable clone for everything that runs.** Reproductions, mutations and suites run in a
   throwaway full clone; the operator's clones are read-only to this skill (GH-564, GH-527 rails).
5. **Verified beats plausible.** "LGTM" without runnable evidence is not a verdict. An unverified
   claim is an Unknown.
6. **Respect repo test policy.** In a repo that forbids new tests (XYZ-forge: `AGENTS.md` *No new
   tests*, GH-831), ask for an existing suite or a recorded manual check rather than a new test
   file, and treat a new test file in the diff as a `[Should]`.
7. **The verdict ships twice.** Posted to the PR and rendered on-screen, from the same file.
