---
description: "Answer **\"where did we leave off?\"** — a fast, read-only recap of a project's recent activity and current open state."
---

# /catchup

Answer **"where did we leave off?"** — a fast, read-only recap of a project's recent activity and current open state. Pulls recent commits, CI/deploy health, open PRs (with mergeability), open issues, local git state, and session memory into one scannable summary, ending with a single suggested next step.

Use this at the **start of a session** to re-orient. It is the recap layer: `/recon` explains *what a repo is*, `/start-working` decides *what to do next*, and `/catchup` reports *what just happened and what's open right now*. It never edits, commits, or merges.

## Arguments

- `$ARGUMENTS` - Optional configuration. Space-separated tokens:
  - First positional: repo slug override (`owner/name`). Defaults to the `origin` remote, then a configured fallback, then inference from the directory name.
  - `scope=all|issues|prs|recent` — Which sections to include (default: `all`).
  - `since=N` — Lookback window in days for commits and CI runs (default: 7).
  - `limit=N` — Max rows per list (default: 20).

Examples:
```
/catchup
/catchup scope=prs
/catchup owner/repo since=3
/catchup scope=issues limit=40
```

## Instructions

### 0. Resolve Target and Mode (gate)

Determine whether there's a local checkout, and which GitHub repo to query. Everything downstream branches on `MODE`.

```bash
# Is the current directory a git work tree?
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  MODE="local+github"
  R=$(git remote get-url origin 2>/dev/null | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')
else
  MODE="github-only"   # e.g. a control directory with .claude/ but no clone
  R=""
fi

# Fall back to a configured slug, then to the first positional arg.
R="${ARG_REPO:-$R}"
R="${R:-blamechris/skill-templates}"
```

If `R` is still empty (no remote, no fallback, no arg), try `gh repo list --limit 50` and match the directory name; if still ambiguous, ask the user for the slug rather than guessing.

State the resolved `R` and `MODE` to the user in one line before continuing. In `github-only` mode, the **Local git state** section is skipped (print "— skipped (no local clone)") — this graceful degradation is the point of the gate, never error out on a missing clone.

Parse `$ARGUMENTS` for `scope` (default `all`), `since` (default 7), and `limit` (default 20).

### 1. Recent Activity — commits + CI/deploy

Run these queries in parallel where possible.

```bash
# Recent commits on the default branch (works without a local clone)
gh api "repos/$R/commits" \
  --jq '.[] | "\(.commit.author.date[0:10])  \(.sha[0:7])  \(.commit.message | split("\n")[0])"' \
  | head -"$LIMIT"

# Recently merged PRs for "what shipped" context
gh pr list -R "$R" --state merged --limit 8 \
  --json number,title,mergedAt -q '.[] | "#\(.number)  \(.mergedAt[0:10])  \(.title)"'

# Latest CI run health
gh run list -R "$R" --limit 8

```

Summarize: what shipped recently, whether the latest default-branch run is green, and whether the most recent deploy succeeded. Call out any failing run on the default branch explicitly — that's the "something's on fire" signal.

### 2. Open PRs — with mergeability

```bash
gh pr list -R "$R" --state open --limit "$LIMIT"
```

For each open PR, pull the merge/CI rollup so stale or conflicting PRs are obvious. Loop over the **already-capped** list from above so `$PR` is defined and the number of `gh pr view` calls stays bounded by `$LIMIT` (no unbounded N+1 on repos with many open PRs):

```bash
for PR in $(gh pr list -R "$R" --state open --limit "$LIMIT" --json number -q '.[].number'); do
  gh pr view "$PR" -R "$R" \
    --json number,title,mergeable,mergeStateStatus,statusCheckRollup \
    -q '{num:("#"+(.number|tostring)), title:.title, mergeable:.mergeable, state:.mergeStateStatus,
         checks:([.statusCheckRollup[]?|.conclusion]|group_by(.)|map("\(.[0]):\(length)")|join(", "))}'
done
```

Flag each PR using `mergeStateStatus` + `statusCheckRollup`:

| Signal | Meaning |
|--------|---------|
| `BEHIND` | Branch is behind the base — needs a rebase/update before it can merge |
| `CONFLICTING` / `DIRTY` | Has merge conflicts — needs manual resolution |
| `FAILURE` in checks | CI is red — may resolve after a rebase, or needs a real fix |
| `CLEAN` + all `SUCCESS` | Ready to merge |

Note when several stale PRs predate a recent toolchain/dependency change on the default branch — their failures may simply be a missing rebase.

### 3. Open Issues — grouped

```bash
gh issue list -R "$R" --state open --limit "$LIMIT" \
  --json number,title,labels,updatedAt \
  -q '.[] | "#\(.number)  [\([.labels[].name]|join(", "))]  \(.title)"'
```

Group issues by the repo's label taxonomy so the list reads as themes, not a flat dump:

Use the existing `bug`, `enhancement`, `documentation`, and `from-review` labels; otherwise group by updated date.

Surface the count, the most recently updated items, and any `bug`/`critical`/`blocked` issues at the top. Do not read every issue body — this is a recap, not triage (`/start-working` does the deep prioritization).

### 4. Local Git State (`local+github` mode only)

Skip this entire section in `github-only` mode (print "— skipped (no local clone)").

```bash
git status -sb                       # current branch + ahead/behind + dirty files
git stash list                       # forgotten work-in-progress
git log --oneline @{u}..HEAD 2>/dev/null   # unpushed local commits, if upstream set
```

Report the current branch, ahead/behind vs upstream, count of uncommitted/staged files, and any stashes — these are the "you were mid-something" signals.

### 5. Context Layer — memory + repo-memory (best-effort)

Both sources are optional; skip silently if absent.

- **Auto-memory:** if a project/auto memory exists (e.g. `MEMORY.md` or a `memory/` dir), surface any `project`/`feedback` notes relevant to current work — these often record "why we left off here."
- **repo-memory MCP:** if the `repo-memory` server is enabled, call `get_changed_files` (and `get_project_map` for orientation) to show recently-touched areas. If the server is unavailable, skip without comment.

### 6. Report + Suggested Next Step

Print one scannable summary. Use tables for PRs and issues. Keep it tight.

```markdown
## Where you left off — {R}

**Mode:** {local+github | github-only}   **Window:** last {since}d

### Recent activity
{1-3 lines: what shipped, latest CI/deploy state — green or red}

### Open PRs ({N})
| PR | What | State |
|----|------|-------|
| #573 | androidx bump | BEHIND, CI failing |
| #557 | AGP 9.1.0 | CONFLICTING |

### Open issues ({N})
{grouped by label theme, 1 line per theme; flag any bug/blocked at top}

### Local state
{branch · ahead/behind · N uncommitted · M stashed   — or "skipped (no local clone)"}

### Suggested next step
{ONE concrete action, e.g. "Rebase the 3 BEHIND Dependabot PRs against the new toolchain — likely cheap green wins; handle the conflicting AGP PR separately."}
```

End on exactly one suggested next step. Do not write any file.

## Critical Rules

1. **Read-only** — `/catchup` never edits files, creates issues/PRs, commits, or merges. It does not merge or rebase anything; it only reports. The user decides what to act on.
2. **Graceful degradation** — every source is optional. No local clone → `github-only` mode (skip local git state). No `gh` auth, no deploy workflow, no memory, no repo-memory → skip that section and note it in the summary. Never fail the whole run on one missing source.
3. **Recap, not triage** — this is a fast orientation (target < 90 seconds). Don't read every issue body or trace code. For prioritized work selection use `/start-working`; for repo orientation use `/recon`.
4. **One next step** — end with a single concrete suggestion, not a menu. The user wanted "where did we leave off," not a backlog.
5. **No attribution** — never add any AI/agent attribution to output.
