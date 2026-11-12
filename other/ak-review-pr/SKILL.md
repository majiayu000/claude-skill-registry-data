---
name: ak-review-pr
description: "Review GitHub PRs for correctness, regressions and security; fix, reply and merge modes authorize those steps."
when_to_use: "Invoke for PR numbers or URLs, to fix findings, post the review back to GitHub or merge when ready and watch CI."
category: workflow
keywords: [pr, pull request, review, github, gh, fix, reply, merge, ci, anti-slop, ai-slop, multi-pr, graphql, rest, cloud-environment]
argument-hint: "<PR number or URL> [<PR number or URL> ...] [--fix] [--reply] [--merge] [--advice] [--ultra]"
allowed-tools:
  - Bash(gh pr view *)
  - Bash(gh pr diff *)
  - Bash(gh pr checks *)
  - Bash(gh pr review *)
  - Bash(gh pr comment *)
  - Bash(gh pr merge *)
  - Bash(gh pr list *)
  - Bash(gh run view *)
  - Bash(gh run list *)
  - Bash(gh run watch *)
  - Bash(sleep *)
  - Bash(gh api *)
  - Bash(gh auth status *)
  - Bash(source *)
  - Bash(. *)
  - Bash(command *)
  - Bash(git log *)
  - Bash(git fetch *)
  - Bash(git diff *)
  - Bash(git status *)
  - Bash(git branch *)
  - Bash(git rev-parse *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(git push *)
  - Bash(date *)
  - Read
  - Edit
  - MultiEdit
  - Write
  - Glob
  - Grep
  - Task
metadata:
  author: agentkit
  version: "2.6.1"
---

# Review Pull Request

Review PR(s) `$ARGUMENTS` in this repository.

## Modes

- **Review-only** (default): review the PR(s) and print findings to chat. Do not edit, commit, or push.
- **Fix loop** (`--fix`): review, fix all actionable findings, commit+push, then re-review. Repeat until no actionable findings remain.
- **Reply** (`--reply`): after the review (or after the fix loop converges), post the review back to the PR via `gh pr review`.
- **Merge** (`--merge`): after all other modes complete, if the PR is ready to merge, activate `ak-git merge-pr` to merge it, watch post-merge CI until green, and verify follow-up before stopping.
- **Advice** (`--advice`): run under `kongming` advisory supervision (see Advisory supervision).
- **Ultra** (`--ultra`): run each PR's initial review as a best-of-5 verifier pass (see Ultra Verifier Mode).

Flags compose: `review-pr 123 --fix --reply` runs the fix loop and posts the final re-review at the end. `review-pr 123 --fix --reply --merge` additionally merges once the loop converges on Approve. `--advice` layers on top of any combination. Flag order does not matter.

## Multi-PR mode

`$ARGUMENTS` may name multiple PRs at once (e.g. `123 456 https://github.com/o/r/pull/789`). Every non-flag token is one PR reference. Accepted forms per token: bare number (`123`), `#123`, or a full PR URL. Tokens may be whitespace- or comma-separated.

Execution is **sequential per PR**. For each PR ref in `PR_REFS`, run the full flow (Instructions → Fix loop → Reply → Merge → Advice checkpoints) end-to-end before moving to the next. This keeps verdicts, commits, replies, and merge results deterministic and easy to attribute in the final report.

Fail-fast is off by default — a fatal error on one PR (e.g. PR not found, GraphQL+REST both denied, merge-readiness rejected) records the failure in the per-PR summary and continues with the next PR. Only stop the whole run when an unrecoverable environment failure occurs (`gh` not installed, no auth at all).

Single-PR invocations continue to behave exactly as before; `PR_REFS` just contains one element.

## GitHub API compatibility

Some hosted environments (notably Claude Cloud Environment) block the GitHub
GraphQL API at the egress proxy, so `gh pr view`, `gh pr diff`, `gh pr checks`
and `gh pr list` all fail with HTTP 403. Load
`references/gh-api-compatibility.md` before the first per-PR bash block: it owns
the `references/gh-api-helpers.sh` loader you must source, the adaptive helper
functions (`_ak_probe_gh_api`, `_ak_split_pr`, `_ak_pr_meta`, `_ak_pr_diff`,
`_ak_pr_files`, `_ak_pr_checks`, `_ak_pr_body`, `_ak_pr_review`,
`_ak_pr_comment`), and the two write-op caveats — auto-merge enable is
GraphQL-only, and self-PR approve returns 422 on both paths.
## Argument parsing

Strip mode flags, then tokenize the remainder into `PR_REFS`:

```
!`ARGS_STRIPPED="$(printf '%s' "$ARGUMENTS" | sed -E 's/[[:space:]]*--(fix|reply|merge|advice|ultra)([[:space:]]+|$)/ /g; s/,/ /g; s/^[[:space:]]+//; s/[[:space:]]+$//')" && PR_REFS="$ARGS_STRIPPED" && PR_COUNT="$(printf '%s\n' "$PR_REFS" | awk '{print NF}')" && printf 'PR_REFS=%s\nPR_COUNT=%s\n' "$PR_REFS" "$PR_COUNT"`
```

Detect flags (the substring match below is intentional — flags may appear in any order):

- `--fix` present → fix-loop mode active
- `--reply` present → reply mode active
- `--merge` present → merge mode active
- `--advice` present → advisory supervision active
- `--ultra` present → ultra verifier mode active for each PR's initial review

Within the Instructions loop, `PR_REF` is the current iteration's ref; the singular name is preserved so this section's examples and the rest of the doc read the same in both single- and multi-PR modes.

## Advanced modes

Load `references/advanced-review-modes.md` only for `--advice` or `--ultra`. It owns all
per-PR checkpoints and candidate/verifier behavior.

## Review execution

Read `references/review-workflow.md` for per-PR context, diff inspection and finding format.
Use `references/gh-api-compatibility.md` when resolving API access. Reuse findings/checks
only for unchanged head SHA, inputs and environment; verify current head before reply/merge.
Review-only never posts, edits or merges.

## Fix loop mode (`--fix`)

Load `references/mode-fix.md` when `$ARGUMENTS` contains `--fix`. It owns the
decision to fix, the per-finding fix rules, the commit and push contract, and the
re-review loop.
## Reply mode (`--reply`)

Load `references/mode-reply.md` when `$ARGUMENTS` contains `--reply`. It owns the
pre-flight checks, the review body format, the verdict-to-`gh` flag mapping, the
self-PR `COMMENT` fallback, composition with `--fix`, and idempotency.
## Merge mode (`--merge`)

Load `references/mode-merge.md` when `$ARGUMENTS` contains `--merge`. It owns the
merge-readiness gate, the `ak-git merge-pr` handoff, post-merge CI watching, and
failure handling.
## Final output

After every PR has completed its flow, report to the chat:

### Per-PR table

| PR | Verdict | Iterations | Commits | Reply | Merge | CI |
|----|---------|------------|---------|-------|-------|----|
| `<PR_REF>` | Approve / Request changes / Comment | N (if `--fix`) | list of SHAs (if `--fix`) | posted / fell-back / printed-locally (if `--reply`) | merged / not-ready(reason) / blocked (if `--merge`) | green / red / pending / n/a |

### Aggregate

- Total PRs processed and totals per verdict
- Environment: `AK_GH_REST=<0|1>` (native GraphQL vs REST fallback) and how many PRs actually hit the REST path
- Advisory summary if `--advice` ran: number of `kongming` checkpoints that fired across all PRs, whether each PR's MANDATORY post-CI-green comment was posted / skipped (with reason), and any advice-flagged risks that shaped verdicts or fix scope
- Remaining findings or blockers per PR
- Unresolved questions, if any

## Optional finding-triage experiment

After candidate discovery, explicitly opted-in experiments may follow
[semantic triage](references/semantic-triage.md). Ordinary review remains unchanged.
