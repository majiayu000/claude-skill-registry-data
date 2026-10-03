---
name: review-retro
description: Mine past automated-review runs for recurring process and judgment failures, then propose fixes to the review setup as one evidence-cited PR. Use when running the review retrospective or tuning the PR reviewer.
allowed-tools: Bash(git *), Bash(gh *), Read, Edit, Write, Glob, Grep
model: opus
disable-model-invocation: true
---

# Review retro

You run the retrospective for the automated review setup (the learn stage of the review pipeline). The review pipeline reviews code; you review the pipeline. Your deliverable is not findings about code: it is improvements to the setup itself, grounded in past runs.

**Dormant until there is history.** The retro needs a window of real review runs and the human outcomes on them. Until the merged producer has reviewed a stretch of PRs, there is nothing to mine: say so and stop rather than inventing patterns from a handful of runs.

> **Setup:** the `ci/review-metrics` branch is produced by
> [`claude-code-review.yml`](../../../.github/workflows/claude-code-review.yml) (which runs
> `/pr-ci-review` with a `--json-schema` from [`tools/review`](../../../tools/review/) and
> appends each run's record). Until that workflow is enabled and has history, the retro
> degrades gracefully — it reports there is no history to mine and stops.

## Evidence

Three sources, all reachable through `gh` or `git`:

- **Run records.** Every CI review appends its `review-metrics` record to the `ci/review-metrics` orphan branch as `records/<run_id>.json` (read via `git fetch origin ci/review-metrics`; the branch holds the full history, so no artifact downloads are needed). Each record carries `process_issues` (self-reported process failures), `refuted_findings` with reasons (the validator's false-positive catches), the reviewer spawn shape (`reviewers_spawned` / `reviewers_skipped`), cost, and tokens. Not every record is a review: a run can fail before producing output (`is_error: true`, null findings). Tell those apart from a clean review that genuinely found nothing. A record's `schema_version` marks methodology boundaries; treat each side as its own population. A record with `review_mode: incremental` reviews only the delta since the prior review, so full and incremental runs are different populations too; never pool their durations, costs, or finding counts in one trend. From the version where the model stopped posting (the poster script owns the PR write), the claimed-versus-actual comment drift of older records has no counterpart and its disappearance is not a trend; what replaces it is anchoring loss, `comments_posted_actual` against the count of `important` findings: the gap is the importants that reached the author as a bullet in the review body rather than a thread on the code.
- **PR thread outcomes.** For each PR those runs reviewed, what humans did with the posted comments. A finding whose code was fixed or whose suggestion was applied earned its place; one dismissed, resolved with pushback, or retracted as a conceded challenge (via `address-review-comments`) is a false positive that survived validation. Mind the author when reading across a posting-identity change: a pipeline that switches which bot posts (e.g. from the CLI's login to `github-actions[bot]`) splits the comments across two logins, so a filter on either alone silently truncates the window to one side of the cutover.
- **Human-found misses.** On those same PRs, the review comments humans wrote that the automated review never raised. Each is an issue the pipeline could have caught and did not. Count a miss only against a PR the pipeline actually reviewed; a comment on a PR whose review never ran is an outage, not a coverage gap.

**Window**: from the last retro PR (title contains `[review-retro]`) included, to now.

**Memory**: the prior retro PRs are your ledger. A merged one is done; a closed-unmerged one was rejected, so do not re-propose its change unless the new window adds materially different evidence.

## Judgment

You are looking for patterns, not incidents; "recurring" is your call, with no numeric threshold. Wherever the evidence shows the pipeline misfiring — in its process, its judgment, or its coverage — trace the failure to the mechanism in the setup that produced it and propose the fix there: a reviewer brief or area in `pr-ci-review`, the consolidator's citation-first assignment, the validator, the workflow, or the schema. Never blunt a reviewer wholesale to make the numbers look better, and the review's philosophy (record-all / rank-by-display, precision over speculation, small inconsistencies compound) is not yours to rewrite.

## Act

Walk the user through what the evidence shows and what you propose to change, and let them steer before you write any diff. For what survives the discussion: branch off the trunk with `scripts/worktree-create.sh review-retro-<date>`, apply the changes, and open a PR (via the `pr-description` skill) with a title of the form `[review-retro] <short summary>`, whose description cites the evidence per change. Wait for the user's sign-off. If nothing recurring emerged, say so and stop: open no PR in that case.
