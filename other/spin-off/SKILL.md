---
description: "Delegate a task to a separate Claude Code session, optionally with its own worktree and Jira ticket. Use when asked to 'spin off', 'spin off a task', 'spin this off', 'delegate to another session', or 'send this to a new worktree'."
user-invocable: true
---

# Spin Off Task

Delegate a task to a new Claude Code session. Can optionally create a Jira ticket and/or git worktree, or just launch a bare session.

## Arguments

Accepts a free-form description of the task to spin off. May include:

- A Jira ticket ID (e.g., `TICKET-1234`) to skip ticket creation
- A project key + description to create a new ticket (e.g., "RETIRE: migrate legacy auth tokens")
- An indication that no ticket or worktree is needed (e.g., "no worktree needed", "no ticket")
- Just a task description if no ticket is needed

## Process

### Step 1: Gather inputs

Parse the user's request to determine:

- **Ticket ID** -- if the request contains a Jira ticket pattern (`[A-Z]+-[0-9]+`), use it directly
- **Ticket creation** -- if the user wants a new ticket, gather: project key, summary, description, issue type (default: Task)
- **Lightweight mode** -- if the user says no ticket/worktree is needed, skip Steps 2-4 and go straight to Step 5
- **Task prompt** -- the instructions to send to the new Claude session
- **Repo** -- which repo to create the worktree in (default: current repo's main working tree)

If any required info is missing, ask the user. The task prompt is required -- this is what the new Claude session will work on.

**Lightweight mode:** If the user explicitly says no worktree or ticket is needed, skip Steps 2-4 entirely. Go straight to Step 5 using the current repo's main working tree as the `--cwd`, and derive a short descriptive workspace name from the task (e.g., `app/review-pr-59826`).

### Step 2: Resolve or create Jira ticket

Follow `../../references/jira-workflow.md`.

After this step you will have `TICKET_ID`, `TICKET_URL`, and `TICKET_SUMMARY`.

### Step 3: Resolve repo path

Determine the main repo working tree path (resolving through worktrees if needed):

```bash
main_git_dir=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)
repo_path=$(dirname "$main_git_dir")
```

If the user specified a different repo, use that path instead. Verify the path exists and is a git repository.

Detect the default branch for branching:

```bash
git -C "$repo_path" remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'
```

### Step 4: Create worktree

Resolve the minions path by following `../../references/minions-path.md`. After this step you will have `minions_path`.

Then create the worktree:

```bash
{minions_path}/scripts/worktree/create {repo_path} {TICKET-OR-BRANCH} --skip-dev-db --skip-test-db --base {default_branch}
```

This handles fetching from origin, creating/reusing the branch, placing the worktree at `~/worktrees/{project_name}/{branch_name}`, and running bootstrap.

If the script reports the worktree already exists, that's fine -- it reuses it.

Capture the worktree path. The convention is `~/worktrees/{project_name}/{branch_name}` where `project_name` is the basename of the repo (e.g., `app`).

If the script fails, report the error and stop.

### Step 5: Create cmux workspace

```bash
cmux new-workspace --cwd {worktree_path} --command claude
```

Capture the workspace reference from stdout. The output format is `OK workspace:N` -- extract the `workspace:N` part.

Rename following the minions convention:

```bash
cmux rename-workspace --workspace {workspace_ref} "{project_name}/{branch_name}"
```

Where `project_name` is the repo basename (e.g., `app`) and `branch_name` is the ticket/branch name.

### Step 6: Wait for Claude to be ready

Loop up to 15 times, sleeping 2 seconds between attempts:

```bash
cmux read-screen --workspace {workspace_ref}
```

On each read, check the screen output:

- **Trust prompt** (screen contains "Quick safety check" or "trust this folder" or the workspace trust dialog): send `cmux send-key --workspace {workspace_ref} Enter` to accept
- **Claude ready** (screen contains `❯` (the Unicode prompt character), "How can I help", or the welcome message): proceed to Step 7
- **Still loading**: sleep 2 seconds and try again

**Important:** Claude's input prompt uses the Unicode character `❯` (U+276F, HEAVY RIGHT-POINTING ANGLE QUOTATION MARK), not a plain `>`. When grepping the screen output, use `❯` or match on other reliable indicators like "Claude Code" combined with the presence of the status bar line (containing "tokens" or "Opus").

If Claude doesn't become ready after 30 seconds, report the issue and tell the user to check the workspace manually. Do not block indefinitely.

### Step 7: Send the task

Send the task in plan mode. Use two separate sends to ensure plan mode activates before the prompt arrives:

```bash
cmux send --workspace {workspace_ref} "/plan"
cmux send-key --workspace {workspace_ref} Enter
```

Sleep 3 seconds for plan mode to activate, then send the task description **via a tempfile** to avoid shell-interpretation issues with quotes and metacharacters in the prompt:

```bash
prompt_file="$(mktemp -t spin-off-prompt.XXXXXX)"
trap 'rm -f "$prompt_file"' EXIT
# Write the task description with Write tool, NOT shell heredoc, to keep
# escaping out of the equation entirely.
cmux send --workspace {workspace_ref} -- "$(cat "$prompt_file")"
cmux send-key --workspace {workspace_ref} Enter
```

Only fall back to inline `cmux send --workspace {workspace_ref} "{task_description}"` if the prompt is short and provably free of quotes / `$` / backticks / backslashes.

### Step 8: Report

Print a summary:

```
Spun off to workspace "{project_name}/{branch_name}":
- Ticket: {TICKET_KEY} ({ticket_url})
- Worktree: {worktree_path}
- Task sent in plan mode
```

If no ticket was created, omit the ticket line.

## Examples

```
/spin-off TICKET-1234 -- Investigate the tenant-not-set error in chat analytics and write a fix with tests
/spin-off RETIRE: migrate legacy auth tokens -- Move the old token format to the new encrypted scheme
/spin-off Fix the flaky test in spec/models/user_spec.rb line 42
/spin-off Review PR #59826, no worktree or ticket needed
```
