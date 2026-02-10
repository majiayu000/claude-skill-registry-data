---
name: plot-approve
description: >-
  Merge an approved plan and fan out into implementation branches.
  Part of the Plot workflow. Use on /plot-approve.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git and gh CLI.
---

# Plot: Approve Plan

Merge an approved plan and fan out into implementation branches.

**Input:** `$ARGUMENTS` is the `<slug>` of an existing idea.

Example: `/plot-approve sse-backpressure`

## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Archive directory:** docs/archive/

### 1. Parse Input

If `$ARGUMENTS` is empty or missing:
- List open plan PRs: `gh pr list --json number,title,headRefName --jq '.[] | select(.headRefName | startswith("idea/"))'`
- If exactly one exists, propose: "Found plan `<slug>`. Approve it?"
- If multiple exist, list them and ask which one to approve
- If none exist, explain: "No open plan PRs found. Create one first with `/plot-idea <slug>: <title>`."

Extract `slug` from `$ARGUMENTS` (trimmed, lowercase, hyphens only).

### 2. Determine Plan PR State

Run the helper to get plan PR state:

```bash
../plot/scripts/plot-pr-state.sh <slug>
```

Handle each case:

- **Plan PR is a draft**: Error — "Plan is still a draft. Mark it ready for review first: `gh pr ready <number>`"
- **Plan PR is open and non-draft (ready for review)**: Proceed to merge it (step 3)
- **Plan PR is already merged**: That's the approval signal — skip merge, proceed directly to creating impl branches (step 4)
- **Plan PR is closed (not merged)**: Error — "Plan PR is closed. Reopen it or create a new one."
- **No PR found**: Error — "No PR found for branch `idea/<slug>`. Run `/plot-idea <slug>: <title>` first."

### 3. Merge Plan PR (if open and non-draft)

```bash
gh pr merge <number> --squash --delete-branch
```

This lands `docs/plans/<slug>.md` on main and deletes the `idea/<slug>` branch.

### 4. Read and Parse Plan

Pull main to get the (just-merged or previously-merged) plan:

```bash
git checkout main
git pull origin main
```

Read `docs/plans/<slug>.md` and parse the `## Branches` section. Expected format:

```markdown
- `type/name` — description
```

Each line must have a backtick-quoted branch name (e.g. `feature/sse-backpressure`) and a description after the `—` dash.

- If no branches are listed (or section is empty/only has the template comment), error: "No branches listed in the plan. Add branches to the `## Branches` section before approving."
- Validate each branch name starts with a known prefix: `feature/`, `bug/`, `docs/`, `infra/`

### 5. Create Implementation Branches and PRs

Collect approval metadata:

```bash
APPROVED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
APPROVED_BY=$(gh api user --jq '.login')
```

For **each branch** in the parsed list:

```bash
git checkout -b <type>/<name> origin/main
```

**Update `docs/plans/<slug>.md` on the branch** to reflect the approval:

1. Change `**Phase:** Draft` → `**Phase:** Approved`
2. Insert an `## Approval` section immediately after the `## Status` block:

```markdown
## Approval

- **Approved:** <APPROVED_AT>
- **Approved by:** <APPROVED_BY>
- **Assignee:** <APPROVED_BY>
```

This provides the initial commit needed for PR creation (no empty commits).

```bash
git add docs/plans/<slug>.md
git commit -m "plot: approve <slug>"
git push -u origin <type>/<name>

gh pr create \
  --draft \
  --assignee @me \
  --title "<description>" \
  --body "$(cat <<'EOF'
## Plan

Part of [<slug>](../blob/main/docs/plans/<slug>.md).

---
*Created with `/plot-approve`*
EOF
)"
```

Read the `## Plot Config` section from `CLAUDE.md` for the project board name. If configured:

```bash
gh pr edit <number> --add-project "<project board name>"
```

Collect all created PR numbers and URLs.

### 6. Update Plan File on Main

After all branches are created, update `docs/plans/<slug>.md` on main to link the implementation PRs.

In the `## Branches` section, append ` → #<number>` to each branch line:

```markdown
- `feature/sse-backpressure` — Handle disconnects → #12
- `bug/sse-memory-leak` — Fix connection leak → #13
```

```bash
git checkout main
git add docs/plans/<slug>.md
git commit -m "plot: link implementation PRs for <slug>"
git push
```

### 7. Summary

Print:
- Plan merged: PR #<plan-number> (or "already merged" if it was pre-merged)
- Implementation PRs created:
  - `type/name` → PR #<number> (URL)
  - `type/name` → PR #<number> (URL)
- Next step: check out a branch and start implementing
