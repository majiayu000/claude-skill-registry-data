---
name: pr
description: Push the current jj bookmark, open a draft GitHub PR, link it to ClickUp, and move the task to in review.
user-invocable: true
allowed-tools: Bash
---

Open a GitHub pull request for the current branch.

## Steps

1. **Push the current bookmark** — find the bookmark name with `jj log -r @ --no-graph -T 'bookmarks'`, then push:
   ```bash
   jj git push --bookmark <bookmark>
   ```

2. **Ask for a ClickUp task ID** if one wasn't provided in the `/pr` invocation (e.g. `/pr abc123`). ClickUp IDs are alphanumeric strings. Never use a URL — reference as `CU-<id>` in the PR body.

3. **Draft the PR** — gather context in parallel:
   - `jj log -r 'trunk()..@' --no-graph -T 'description ++ "\n"'` — commits on this branch
   - `jj diff --git -r 'trunk()..@'` — diff vs main

   Terse format per repo convention:
   - **Title**: ≤70 chars, present tense, no period
   - **Body**:
     ```
     One sentence stating the problem (≤25 words).

     One sentence summarizing the fix.

     CU-<task-id>
     ```

4. **Create the PR** — always draft, always explicit `--head` and `--base` (jj leaves git in detached HEAD). Use the bookmark name for `--head` — GitHub's API requires a branch name, not a commit SHA:
   ```bash
   gh pr create --draft --head <bookmark> --base main --title "..." --body "..."
   ```

5. **Complete the ClickUp workflow** — after the PR URL is returned, run in parallel using the ClickUp MCP tools:
   - Set the "Github Link" custom field (id: `57902a6b-7f34-4be2-b94f-74901dae59a1`) to the PR URL via `clickup_update_task`
   - Move the task status to `in review` via `clickup_update_task`

6. **Report** — output the PR URL and confirm the ClickUp task was updated.
