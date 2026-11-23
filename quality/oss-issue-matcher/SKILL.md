---
name: oss-issue-matcher
description: "Use when the user wants to find an open-source issue or project to contribute to, a good first issue, or help picking a repo whose maintainers will actually review and merge outside pull requests (for example 'find me a first open-source contribution', 'good first issues for Rust', 'is this repo worth contributing to')."
---

# OSS Issue Matcher

## Overview

Most "good first issue" lists rank by label, not by whether anyone will answer your pull request. This skill scores each candidate repo on how it has actually treated outside PRs, then picks issues only from repos that pass. Every number comes from `scripts/repo_pulse.py`, never from memory. Everything is read-only: do not comment on issues, claim them, fork or open PRs.

## Setup

Run `gh auth status`. If gh is missing or not logged in, stop and tell the user to run `! gh auth login`.

Take the user's language or stack, skills, hours per week and goal (learn, résumé, fix a tool they use). If no language or skill was given, ask that one question; otherwise state your defaults in one line and proceed.

## Process

1. **Find candidates.** Run two searches, `--label "good first issue"` and `--label "help wanted"`:
   `gh search issues --label "good first issue" --state open --no-assignee --archived=false --language <lang> --sort updated --limit 100 --json repository,number,title,updatedAt --jq '.[] | [.repository.nameWithOwner, .number, .title, .updatedAt] | @tsv'`
   Count the issues per repo. Keep up to 12 repos, ranked by how many matching issues they have (a maintainer who keeps labelling issues is active), then by the most recent update. Prefer repos with 2 or more issues; a repo with one auto-generated-looking issue is usually too new to score. Add repos the user names.
2. **Score the repos.** Run `python scripts/repo_pulse.py owner/a owner/b ...` (the script sits next to this file). It reads the last 100 PRs and reports, for outside contributors only: merge rate, median hours to a maintainer's first reply (over the PRs that got one), the share of PRs left unanswered, days since the last commit, and a grade.
3. **Cut.** Drop `avoid` and `archived` repos and say why in one line. Keep `responsive` first, `slow` second. `insufficient-data` is unscored: include it only if the user wants it, labeled so. A repo entry with `error` could not be read; list it as unchecked.
4. **Check each issue** in the surviving repos (at most 3 per repo):
   - `gh issue view N --repo R --json assignees,labels,comments,createdAt,updatedAt,body`: unassigned, and no comment in the last 30 days saying "I'll take this" or "working on this". If the issue is under 7 days old, say the claim check only covers that short time and that sibling issues created in the same minute are probably a batch.
   - `gh pr list --repo R --state open --search "N"`: no open PR already references it.
   - A maintainer has confirmed it is wanted (a maintainer comment, or the label applied by one).
   - The repo's CONTRIBUTING file, read for a required issue-first step, CLA, DCO or test rules.
   - Scope fits the user's hours and skills.
5. **Report** the best 3 issues.

## Grades

| Grade | Rule (heuristic, in the script) |
|---|---|
| `responsive` | at most 20% of outside PRs unanswered, median first reply within 72h, at least 50% of closed PRs merged, commit in the last 90 days |
| `slow` | answers outside PRs, but slowly or selectively; read the numbers |
| `avoid` | 50% or more unanswered, or under 20% merged, or no commit for a year |
| `insufficient-data` | fewer than 8 outside PRs old enough to judge |

When the numbers pull apart (a fast median reply but many unanswered PRs), say the repo answers some PRs quickly and ignores most, and do not smooth it into one impression. A PR counts as unanswered only if it is closed unmerged or has waited over 14 days with no human maintainer reply (a merge counts as an answer, drafts are skipped, bots do not count). `avoid` is about outside PRs, not the project's quality: some projects close unsolicited PRs unless an issue was agreed first. Say so when the cause is visible in CONTRIBUTING.

## Report format

For each issue: repo, link, one line on what to change, the repo's numbers (grade, merge rate, median hours to first reply, unanswered share), why it fits the user's hours and skills, claim status (unassigned, no open PR, maintainer-confirmed), and the first step. Then a short **Rejected** list with the reason for each repo or issue. Then what you could not check.

If nothing passes, say so and name the closest repo and why it failed. Do not pad the list.

## Limits to state

- The score covers the last 100 PRs. Long threads can hide a maintainer's late reply, so very slow answers are under-counted.
- Small or new repos get `insufficient-data`, not a grade.
- A maintainer whose organisation membership is private shows up as an outside contributor, which flatters a repo's merge rate.
- Stars, issue counts and labels are not evidence of responsiveness. Do not use them to rank.

## Common Mistakes

- Ranking by label or stars instead of the script's numbers.
- Recommending an issue without checking for an open PR or a recent claim.
- Judging a repo by merged PRs alone: ignored and closed PRs are the point.
- Calling a `slow` repo bad. It may still suit a patient first-time contributor with a high merge rate.
- Commenting to claim the issue for the user. The user does that.
