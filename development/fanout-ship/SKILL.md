---
name: fanout-ship
version: 1.0.0
description: |
  Parallel multi-agent ship pattern. Decompose 1 parent task into N independent
  child tasks → spawn N background agents in isolated git worktrees → each opens
  PR targeting shared integration branch → smallest-first merge order with
  self-documenting rebase recipes → final PR integration → main.

  Collapses N×30min sequential work into ~30min wall-clock. Isolated blast
  radius (one agent crash ≠ kill others). Granular revert. Small review surface
  per PR. Background execution = no babysit.

  Trigger when user says: "fan out", "fanout", "split into N PRs", "parallel build",
  "parallel agents", "spawn N agents", "/fanout-ship", "ship in parallel", or
  pastes a parent issue + list of child tasks.

  Auto-trigger heuristic: task list ≥ 4 INDEPENDENT subtasks touching DISJOINT
  files, single repo, GitHub-hosted.
license: MIT
compatibility: claude-code
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - TaskCreate
  - TaskUpdate
---

# fanout-ship

## When to use

USE when ALL true:

- ≥4 child tasks
- Tasks touch DISJOINT files (no shared edits)
- Single GitHub repo
- `gh` CLI authenticated
- Clean working tree on base branch

SKIP when:

- Tasks share files (merge conflict storm)
- <4 tasks (overhead > benefit)
- Sequential dependencies (B needs A's output)
- No CI / no PR review process (just commit direct)

## Inputs required

1. **Repo path** — local clone, clean tree
2. **Base branch** — usually `main` / `mobile_main_dev` / `develop`
3. **Parent issue** — GitHub issue # (or create one)
4. **Child task list** — N items, each with:
   - `title` — short
   - `scope` — files/classes/methods to touch
   - `blast_radius` — int (line count est, method count, complexity 1-10)
   - `acceptance` — testable criteria

If user gives vague request → ASK for the task list before fanout.

## The 8-step recipe

### 1. Pre-flight

```bash
cd <repo>
gh auth status                    # must be logged in
git status                        # must be clean
git fetch origin
git checkout <base> && git pull
```

Abort on dirty tree or auth fail.

### 2. Create integration branch

```bash
INTEG="issue-${PARENT}-integration"
git checkout -b "$INTEG"
git push -u origin "$INTEG"
```

### 3. Create child issues (if not exist)

```bash
for task in tasks; do
  gh issue create \
    --title "Phase N: <ChildTitle>" \
    --body "Parent: #<PARENT>. Scope: ...\nAcceptance: ..." \
    --label "fanout"
done
```

Capture issue numbers → write to `tasks.json`.

### 4. Sort by blast radius ASCENDING

Smallest first = least rebase pain. Save canonical merge order.

### 5. Spawn N agents in ONE message

Use `Agent` tool with:

- `isolation: "worktree"` — isolated copy
- `run_in_background: true` — fire & forget
- `subagent_type: "general-purpose"` (or specialized)
- Self-contained prompt (see template below)

CRITICAL: all N `Agent` calls in single assistant message = true parallel.

### 6. Status polling

```bash
gh pr list --base "$INTEG" --json number,title,state,headRefName,mergeable
```

Format as table. Optional: wrap in `/loop 60s` for live refresh.

### 7. Merge in order

For each PR (smallest blast radius first):

```bash
gh pr checks <PR>            # CI green
gh pr merge <PR> --squash    # or --rebase
```

Remaining PRs auto-need rebase (recipe in their body).

### 8. Final PR

```bash
gh pr create \
  --base <base> \
  --head "$INTEG" \
  --title "Parent #<PARENT>: integrated N child PRs" \
  --body "Closes #<PARENT>. Merged: <list>"
```

Device-test integration branch BEFORE final merge.

## Agent prompt template

Each spawned agent gets THIS prompt (vars filled in):

```
You are implementing child task <N>/<TOTAL> of parent issue #<PARENT>.

REPO: <repo_url>
BASE: <base_branch>
TARGET: <integration_branch>
ISSUE: #<CHILD_ISSUE>

SCOPE:
<scope_description>

FILES TO TOUCH:
<file_list>

ACCEPTANCE:
<acceptance_criteria>

PROCEDURE:
1. Branch off <base_branch>: `git checkout -b feat/issue-<CHILD_ISSUE>-<slug>`
2. Implement scope. Touch only listed files.
3. Run tests: `<test_cmd>`
4. Commit: clear message referencing #<CHILD_ISSUE>
5. Push: `git push -u origin <branch>`
6. Open PR: `gh pr create --base <integration_branch> --title "..." --body "<see below>"`

PR BODY MUST INCLUDE:
## Position
<N> of <TOTAL> in merge order (blast radius: <BR>)

## Closes
#<CHILD_ISSUE>

## Rebase recipe (for later PRs in queue)
\`\`\`
git fetch origin
git rebase origin/<integration_branch>
git push --force-with-lease
\`\`\`

## Testing scenarios
- <scenario 1>
- <scenario 2>

## Files changed
<list>

CONSTRAINTS:
- Touch ONLY files in scope. No drift.
- No formatting churn outside touched lines.
- No dependency bumps unless required by scope.
- If blocked → comment on issue #<CHILD_ISSUE>, do NOT touch other PRs.

Report PR URL when done.
```

## Files

- `recipes/agent-prompt.md` — full agent prompt template (copy-fill)
- `recipes/decomposition-checklist.md` — how to split parent → children safely
- `templates/tasks.schema.json` — JSON schema for task list
- `scripts/preflight.sh` — verify gh + clean tree + base branch
- `scripts/create-integration-branch.sh` — branch + push
- `scripts/create-child-issues.sh` — bulk gh issue create from tasks.json
- `scripts/spawn-block.md` — copy-paste Agent call block (N invocations)
- `scripts/status-table.sh` — `gh pr list` → markdown table
- `scripts/merge-next.sh` — merge next-smallest PR + nudge rebase
- `references/blast-radius-heuristics.md` — how to estimate

## Decomposition checklist (read recipes/decomposition-checklist.md)

Before fanout, verify each child task:

- [ ] Files DISJOINT from siblings
- [ ] Acceptance testable independently
- [ ] No shared schema migration (or schema is FIRST + others depend)
- [ ] No shared config edit
- [ ] Independent test suite path

If shared schema → fan out AFTER schema lands solo.

## Cost model

- Wall clock: ~max(child_task_duration) instead of sum
- Anthropic tokens: ~N × solo cost (parallel = parallel spend)
- GitHub Actions: N × CI run
- Worktree disk: N × repo size

Break-even: N≥4 AND wall-clock-saved > $$ tokens-extra. Almost always wins for N≥6.

## Example uses

- `wp-rest-control-system` — 20 endpoints × 2 plugins = 40 fanout (batched 10s)
- `sm-dashboard` — 7 Supabase tables + 14 RLS = 21 parallel migrations
- `sites-expansion` — 140 WXR pages = batched fanout 10×14
- `github-100-repos` Tier S — 10 anchor scaffolds parallel
- `aeo-audit-tool` — 5 API integrations parallel

## Failure modes + fixes

| Failure                      | Cause                  | Fix                                                        |
| ---------------------------- | ---------------------- | ---------------------------------------------------------- |
| Merge conflicts every PR     | Files not disjoint     | Re-decompose. Pull conflict file into solo PR first.       |
| Agent opens PR to wrong base | Prompt missed `--base` | Explicit `--base <integration>` in prompt                  |
| Stale rebase storm           | Slow merge cadence     | Merge ≤2 PRs/day or batch-rebase weekly                    |
| One agent stuck              | API timeout / loop     | Kill via TaskStop → respawn                                |
| CI flake on rebased PR       | Cache stale            | Push empty commit `git commit --allow-empty -m "rerun ci"` |
| Auth fail mid-run            | gh token expired       | `gh auth refresh` then respawn failed agents               |

## Anti-patterns

- ❌ Spawning agents in separate messages (loses parallelism)
- ❌ Skipping integration branch (PRs target main = chaos)
- ❌ Merging biggest first (forces N-1 huge rebases)
- ❌ Letting agents pick their own scope (drift = conflict)
- ❌ Skipping preflight (dirty tree = corrupted worktrees)
- ❌ Using for tasks <4 children (overhead > benefit)
