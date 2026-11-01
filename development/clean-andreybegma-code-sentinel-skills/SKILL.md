---
name: cs-clean
description: Clean up what merged work leaves behind on a GitHub repository — remote and local branches of merged pull requests, worktrees still holding them, and issues those pull requests resolved but GitHub never closed (a `Closes #n` into a non-default base such as `develop` closes nothing). Shows the evidence for every item, asks before deleting (or runs with --auto), never touches unmerged work
argument-hint: "[--dry-run] [--auto] [--local] [--abandoned]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# Repository Cleanup

You remove what merged work leaves behind: branches whose pull request has
merged, the worktrees and local branches that still point at them, and the
issues those pull requests resolved. **Everything you delete has a merged pull
request or an ancestry check as its proof. Without proof, you report and leave
it.** Without `--auto`, nothing is deleted or closed before the person confirms
it.

## Arguments

`$ARGUMENTS`, any combination:

| Flag | Effect |
|---|---|
| *(none)* | Collect, classify, report, then ask which groups to apply |
| `--dry-run` | Collect, classify, report. Change nothing, ask nothing |
| `--auto` | Apply the *merged* groups (remote branches, local branches, worktrees, issues) without asking. Never the abandoned group. For CI and for `cs-orchestrator` runs |
| `--local` | Local branches and worktrees only — no remote deletions, no issue changes |
| `--abandoned` | Also offer the branches of pull requests that were **closed without merging** (unselected by default; ignored under `--auto`) |

## Configuration

`.code-analyzer-config.json` → `clean`, every key optional:

```json
{
  "clean": {
    "protectedBranches": ["main", "master", "develop", "staging", "production", "release/*", "hotfix/*"],
    "prLimit": 300,
    "closeIssues": true
  }
}
```

| Key | Default |
|---|---|
| `protectedBranches` | the list above; globs allowed. The default branch, `orchestrator.base`, and every branch GitHub reports as protected are always added |
| `prLimit` | how many of the most recent merged and closed pull requests to read |
| `closeIssues` | `false` leaves issues alone and cleans branches only |

## Step 0: Prerequisites

Run each as its own command:

```sh
gh auth status
git remote get-url origin
git fetch --prune origin
gh repo view --json nameWithOwner,defaultBranchRef -q '"\(.nameWithOwner) \(.defaultBranchRef.name)"'
gh api "repos/{owner}/{repo}/branches?protected=true&per_page=100" -q '.[].name'
```

If `gh` is not authenticated or `origin` is not a GitHub repository, stop and
say what is missing. Build the **protected set**: default branch,
`orchestrator.base` (if configured), GitHub-protected branches,
`clean.protectedBranches`. A protected branch is never a candidate.

## Step 1: Collect

```sh
gh pr list --state merged --limit <prLimit> --json number,title,headRefName,headRefOid,baseRefName,mergedAt,body,closingIssuesReferences,isCrossRepository
gh pr list --state closed --limit <prLimit> --json number,title,headRefName,headRefOid,mergedAt,isCrossRepository
gh pr list --state open --limit 200 --json number,headRefName,baseRefName,body
git for-each-ref refs/remotes/origin --format='%(refname:lstrip=3) %(objectname) %(committerdate:short)'
git for-each-ref refs/heads --format='%(refname:short) %(objectname) %(upstream:short) %(upstream:track)'
git worktree list --porcelain
git branch --show-current
tmux ls 2>/dev/null | grep '^cs-' || true
```

Ignore `origin/HEAD`. Pull requests from forks (`isCrossRepository: true`) have
no branch here; skip them for branch cleanup, but keep them for issues.

**Keep set**: every branch that is the head or the base of an open pull request,
the current branch, and the branch of every worktree whose `cs-*` tmux session
is live (an orchestrator slot at work).

## Step 2: Classify branches

For each branch, the first matching row decides.

### Remote branches (`origin/<b>`)

| Condition | Verdict |
|---|---|
| protected, or in the keep set | **keep** |
| a merged pull request has `headRefName == <b>`, and the branch tip equals its `headRefOid` or is an ancestor of it (`git merge-base --is-ancestor <tip> <headRefOid>`) | **merged** — cite the PR |
| a merged pull request has that head, but the branch has commits after it | **keep** — "N commits after #<pr> merged" |
| `git merge-base --is-ancestor origin/<b> origin/<default>` (or `origin/<base>`) | **merged** — "contained in `<default>`" |
| a pull request closed **without** merge has that head and the tip equals its `headRefOid` | **abandoned** — only offered with `--abandoned` |
| anything else | **stale / unknown** — report with last commit date, never delete |

When several pull requests share a head name, use the most recent one whose
`headRefOid` matches the tip.

### Local branches

| Condition | Verdict |
|---|---|
| protected, current branch, or in the keep set | **keep** |
| the remote branch of the same name classified **merged** above, and the local tip is that tip or an ancestor of it | **merged** |
| upstream is `[gone]` and the local tip equals or is an ancestor of a merged pull request's `headRefOid` | **merged** |
| tip is an ancestor of `origin/<default>` or `origin/<base>` | **merged** |
| upstream `[gone]` but none of the above | **unpushed work** — report the commits (`git log --oneline origin/<default>..<b>`), never delete |
| anything else | **keep** |

### Worktrees

A worktree whose branch is **merged** is a candidate only when
`git -C <path> status --porcelain` is empty and no live `cs-*` session holds it.
A dirty worktree is reported, never removed. The main worktree is never a
candidate.

## Step 3: Classify issues

Skip this step under `--local` or `closeIssues: false`.

For each merged pull request (not only those whose branch still exists — the
issue may be the only leftover), collect the issues it claims:

- `closingIssuesReferences[].number`;
- plus every same-repository reference in its body matching
  `(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s*:?\s+#(\d+)` — GitHub links
  these only for pull requests into the default branch, so the body is the
  reliable source for anything merged into `develop` or another base.
  `owner/repo#n` references to other repositories are ignored.

An issue is a **close candidate** when all hold:

1. `gh issue view <n> --json state,labels -q .state` is `OPEN`;
2. it was not reopened after that pull request's `mergedAt`:
   `gh api "repos/{owner}/{repo}/issues/<n>/events?per_page=100" -q '.[] | select(.event=="reopened") | .created_at'`
   has nothing later than `mergedAt` — a reopened issue is a person's decision;
3. no **open** pull request claims it too (same pattern over open pull request
   bodies) — the work is not finished;
4. it is not labelled `cs:needs-person`.

Each candidate cites the pull request and the base it merged into. Also list
closed issues that still carry `cs:in-flight` — the label is stale.

## Step 4: Report

```markdown
## Cleanup — <owner/repo> · default <default> · base <base>

### Remote branches of merged pull requests (<n>)
| Branch | Pull request | Merged into | Merged at |

### Local branches (<n>)
| Branch | Evidence |

### Worktrees (<n>)
| Path | Branch | Evidence |

### Issues resolved but still open (<n>)
| Issue | Title | Closed by | Into |

### Abandoned branches — closed without merge (<n>)        ← only with --abandoned
| Branch | Pull request | Closed at |

### Not touched
| Item | Why |                ← stale branches, unpushed work, dirty worktrees, reopened issues, issues with open PRs
```

Empty sections are omitted. If every group is empty, say the repository is
clean and stop. Under `--dry-run`, stop here.

## Step 5: Confirm

Skip under `--auto` (apply every non-abandoned group).

Use `AskUserQuestion` with `multiSelect: true`, one option per non-empty group,
labelled with its count:

- `Remote branches (<n>)` — description: "Delete branches of merged pull requests on origin"
- `Local branches and worktrees (<n>)` — description: "Remove clean worktrees and delete merged local branches"
- `Issues (<n>)` — description: "Close as completed with a comment naming the merged pull request; also remove stale cs:in-flight labels"
- `Abandoned branches (<n>)` — description: "Delete branches of pull requests closed without merge — not recommended unless you know they are dead"

Nothing selected means nothing changes; say so and stop.

## Step 6: Apply

In this order, so that git never refuses a branch a worktree still holds:

1. **Worktrees** — `git worktree remove <path>` (no `--force`), then
   `git worktree prune`.
2. **Local branches** — `git branch -D <b>`. `-D` is required because a squash
   or rebase merge leaves the local commits unreachable from the base; the
   merged pull request or the ancestry check from Step 2 is the proof.
3. **Remote branches** — `git push origin --delete <b1> <b2> …` in batches of
   up to 20. A branch already gone is not an error.
4. **Issues** — per issue:
   `gh issue close <n> --reason completed --comment "Resolved by #<pr>, merged into <base>. Closed by /cs-clean."`,
   then `gh issue edit <n> --remove-label cs:in-flight` if it carries it. For
   stale labels on closed issues, the label removal only.
5. `git fetch --prune origin`.

A failure is recorded and the rest continues.

## Step 7: Summary

```markdown
## Cleanup done

| Group | Done | Failed |
|---|---|---|

Failed:
- <item> — <error line>

Not touched: <n> items (see the report above).
```

## Never

- Delete a protected branch, the default branch, the orchestrator base, the
  current branch, or the head or base of an open pull request.
- Delete a branch with commits that no merged pull request and no ancestry
  check accounts for.
- Remove a dirty worktree, the main worktree, or one a live `cs-*` session
  holds; use `--force` anywhere.
- Close an issue no merged pull request claims, one reopened after the merge,
  or one an open pull request still claims.
- Delete abandoned branches under `--auto`.
- Touch tags, rewrite history, or push anything other than branch deletions.
