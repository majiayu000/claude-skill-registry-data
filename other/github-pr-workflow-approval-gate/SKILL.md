---
name: github-pr-workflow-approval-gate
description: >-
  Use when a pull request will not merge although no check has failed, a workflow run sits in
  `action_required` or shows as waiting for approval, required checks never report at all after a
  push, or the checks page looks green while merge status stays pending. Also when sweeping
  approvals for runs across a repository after pushing to a PR branch.
---

# GitHub PR workflow approval gate

## Profile keys consumed

- `project.repo`
- `ci.required_checks`

## Overview

A repository can require manual approval before it runs workflows triggered by a pull request. Those
runs land in `action_required` and never execute, so the checks they would report simply do not
appear — the merge stays blocked by a required check that is missing rather than failing. Nothing on
the PR page says so plainly, which is what makes it a silent blocker.

## When to use

- Merge status is pending or blocked and no check is red.
- A required check named in `ci.required_checks` is listed as expected but has never reported on
  this head.
- Fresh commits were pushed to a PR branch and the runs need approving before triage is meaningful.
- Not for: a run that started and failed — that is a real failure, fix its cause.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — many required checks are `pull_request`-triggered, so an unapproved run withholds
  the check entirely; the sweep below is repository-agnostic.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — as described.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — as
  described.

## Procedure

1. Resolve the repository from the checkout so the commands work anywhere. It must agree with
   `project.repo`.

   ```bash
   REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
   ```

2. List the runs that are waiting, so you can see what is being withheld before approving anything.

   ```bash
   gh api --paginate "repos/$REPO/actions/runs?status=action_required&per_page=100" \
     --jq '.workflow_runs[] | {id, name, head_branch}'
   ```

3. Approve them.

   ```bash
   gh api --paginate "repos/$REPO/actions/runs?status=action_required&per_page=100" \
     --jq '.workflow_runs[].id' \
   | xargs -I {} gh api -X POST "repos/$REPO/actions/runs/{}/approve"
   ```

4. Re-read the check status once the runs have started, and only then judge merge readiness. A run
   approved a moment ago reports nothing yet, so an immediate re-check looks identical to the
   blocked state you just cleared.

## Why the state exists

The approval requirement is a repository or organisation security setting, not a property of the
workflow file — it exists so a pull request cannot make a repository's runners execute unreviewed
code. Read the approval as "has anyone looked at this diff", and approve only after you have. Do not
try to route around it by changing a workflow's trigger away from `pull_request`; that would remove
the check from the pull request, which is the opposite of what merge readiness needs.

## Common mistakes

- Reading the checks tab and concluding the pipeline is green when the run never started.
- Approving without looking at the branch and the diff first.
- Approving once and forgetting: every push to the branch creates new runs that queue in the same
  state, so sweep again after each significant push.
- Filtering the run list by workflow name and missing runs from workflows you did not expect to be
  triggered.
- Listing runs without the `status` query parameter and without `--paginate` — one unfiltered page
  holds only the most recent runs of every status, so a busy repository's waiting runs are dropped
  and the sweep reports a clean state it never checked.
