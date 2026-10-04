---
name: review-prs
description: "Use for \"check open PRs\", \"review PRs across my repos\", \"merge the dependabot PRs\", \"clean up PRs\". Scans every git repo under a directory, lists open PRs grouped into action bumps, dependency bumps, and everything else, and merges the groups you approve. Never merges a feature PR without a per-PR yes."
---

# Review PRs

Scan the repos on this machine, show what's open, merge what you approve. Built for the weekly pile of Dependabot PRs, where one yes should clear twenty of them.

## Config

Everything is overridable in the prompt. Defaults, in order of precedence:

1. Words in the prompt. "dir=~/work", "org=my-org", "exclude foo, bar".
2. `~/.config/squirrel/review-prs.json`, if it exists.
3. Built in: directory `~/code`, no org filter, no excludes.

The config file:

```json
{
  "dir": "~/code",
  "org": "my-org",
  "exclude": ["archived-thing", "*-plugin"]
}
```

Excludes are glob patterns on the repo name. Excluded repos never appear in output. Carry excludes through the whole session, don't re-ask.

## Steps

### 1. Scan

Run `scripts/scan.py` from this skill. Don't rewrite the scan by hand.

```bash
python3 scripts/scan.py [--dir DIR] [--org ORG] [--exclude PATTERN ...]
```

On Windows, where `python3` isn't a command, use `py -3`.

It walks every git checkout under the directory, keeps the ones whose origin is on GitHub and matches the org filter if one is set, skips excludes, and prints one line per open PR: `repo|#number|title|url|author`. Repos with nothing open are silent.

If `gh` isn't authenticated, stop and say so.

### 2. Group

Three groups, by title and author.

- **Action bumps.** Dependabot PRs bumping a GitHub Action. Title matches `bump <owner>/<action>` where the owner is a known action publisher: `actions`, `docker`, `aws-actions`, `github`, `ossf`, `pypa`, and the like. Low risk, safe in bulk.
- **Dependency bumps.** Any other Dependabot or Renovate PR. `bump <package> from X to Y`, `update <package> requirement`, `build(deps)`. Review before merging. A major version bump gets flagged in the table.
- **Everything else.** A person wrote it. The human decides each one.

### 3. Present

Three tables, repo, PR, title. Show `(none)` for an empty group. Then one question: which groups or which PRs to merge.

### 4. Merge

For each approved PR, in order:

1. If the branch is behind, `gh pr update-branch` and wait for checks. Dependabot doesn't always rebase on its own.
2. Merge with the method the repo allows. Squash if it's allowed, otherwise merge. Delete the branch.
3. Never pass `--admin` unless the human said to bypass protection for this run. Protection is there on purpose.

Track the result per PR and show a table: merged, already merged, conflict needs a person, failed with the reason. A conflict is never forced.

### 5. Re-check

Scan again with the same settings and show what's left.

## Never

- Merge a PR from the "everything else" group without a yes for that specific PR.
- Scan outside the configured directory or org.
- Bypass branch protection without being told to.
- Force a merge over a conflict.
