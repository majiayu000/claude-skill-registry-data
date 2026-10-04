---
name: pr-batch-merge-validation
description: Use when several open pull requests are queued to land and the question is which of them can go in together. Triggers on stale branches behind `main`, "does this batch conflict?", a clean local merge that still reds the pipeline, a gate that only exists on `main`, and any plan to rebase a branch that already has review history.
---

# PR Batch Merge Validation

## Profile keys consumed

- `project.repo`
- `ci.workflows`
- `ci.required_checks`
- `make.pr_comments`
- `capabilities.publish_pr_comments`

Review-thread retrieval runs through the target mapped by `make.pr_comments`;
skip that step with a recorded note when the key maps to `null` or when
`capabilities.publish_pr_comments` is `false`, and read the threads with `gh`
against `project.repo` instead. `git` and `gh` may be invoked directly.

## Overview

A clean text merge is where batch validation starts, not where it ends. The defects that sink a
batch are semantic: a gate the base branch added that the branch's new files never registered with,
a rationale that a later fix inverted, a variable whose meaning changed underneath the branch. None
of them appear in a diff; all of them appear in a run of the merged tree.

## When to use

- Two or more branches are individually green and need an ordering, or a decision on which subset
  lands.
- A branch has been open long enough that the base branch grew new gates.
- The merge button is green but the intended merge result was never built anywhere.
- Deciding whether to merge the base branch in or to rebase.
- Not for: getting a single change green — that is the ordinary local gate run.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate
  CI target): yes — the gate workflows declared in `ci.workflows` trigger on `pull_request` to
  `main`, so a branch that heads no such pull request runs none of them; the target mapped by
  `make.pr_comments` reads the review threads.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — same `pull_request`
  to `main` triggers and the same review-thread target behind `make.pr_comments`.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  same `pull_request` to `main` triggers; it maps `make.pr_comments` to `null`, so read the threads
  with `gh` and record the substitution.

```bash # profile-example
# With a profile whose make.pr_comments maps to the `pr-comments` target:
make pr-comments PR=<n>
```

## Procedure

1. **Bring each branch up to date by merging, not rebasing.** A merge commit preserves the review
   history and the comment anchors; rewriting the branch breaks both.

   ```bash
   git switch <branch>
   git merge origin/main   # resolve text conflicts here
   git push
   ```

2. **Read what each branch actually adds.** The three-dot form compares against the merge base, so
   it shows the branch's own work and omits everything already on the base branch — which is what
   the merge itself evaluates.

   ```bash
   git diff --name-only origin/main...HEAD
   ```

3. **Let the merged tree run the gates.** Because the gate workflows in `ci.workflows` fire only on
   a pull request targeting the default branch, a branch stacked on another feature branch runs
   nothing at all. Re-target it, or accept that it is unvalidated. Confirm the set that ran against
   `ci.required_checks`.

4. **Triage the two failure classes differently.** A text conflict is blocked before any run. A
   semantic defect is green locally and red on the merged tree — that run is the source of truth.

5. **Intersect the file sets pairwise.** Two branches whose three-dot file lists do not overlap can
   land in either order. Overlapping ones can land only while neither merged tree is red.

6. **Re-test the triple.** Pairwise compatibility is not transitive: two compatible pairs sharing a
   branch still need the three-way result before the batch is called safe.

## Semantic defects to look for

- **Gate registration gaps** — the base branch added an allow-list, a coverage manifest, a policy
  file, or a route/target inventory, and the branch's new file must appear there. No conflict, red
  gate.
- **Inverted rationale** — a comment explaining why some code was unsafe is false once the base
  branch fixed the cause; a stale branch keeps obeying the retired reasoning.
- **Silently redefined switches** — the meaning of an environment or executor variable changed on
  the base branch, so branch code now runs under different defaults.
- **Unpinned fixtures** — a test fixture that mutates a real file drifts as that file changes on the
  base branch.
- **Latent defaults** — a default parameter that only misbehaves under a setting one container
  applies.

## Common mistakes

- Rebasing a reviewed branch onto the base branch — the history rewrite invalidates review threads
  and the checks keyed to the old commits.
- Treating a green local run as proof — local gates cannot see gates the base branch added.
- Using the two-dot diff to size a conflict — it includes work already merged and overstates the
  overlap.
- Declaring a triple safe from two green pairs — build the three-way result.
- Merging a branch whose merged tree is red because a red check "looks unrelated" — it is exactly
  where the semantic defects show up.
