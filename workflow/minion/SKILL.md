---
description: "Hand a task off to the automated minions implement pipeline (plan→implement→PR). Use when asked to 'spin off a minion', 'send to minion', 'implement with minion', or 'minion TICKET-ID'."
user-invocable: true
---

# Minion: Automated Implement Pipeline

Hand a Jira ticket off to the minions implement pipeline, which autonomously plans, implements, and opens a PR — no human steering required.

## Arguments

Accepts a Jira ticket ID or enough information to create one:

- A ticket ID (e.g., `TICKET-1234`) to use an existing ticket
- A project key + description to create a new ticket (e.g., "RETIRE: migrate legacy auth tokens")

No task prompt is needed — the Jira ticket is the task.

## Process

### Step 1: Gather inputs

Parse the user's request to determine:

- **Ticket ID** -- if the request contains a Jira ticket pattern (`[A-Z]+-[0-9]+`), use it directly
- **Ticket creation** -- if the user wants a new ticket, gather: project key, summary, description, issue type (default: Task)
- **Repo** -- which repo to run the pipeline against (default: current repo's main working tree)

If any required info is missing, ask the user.

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

### Step 4: Resolve minions path

Follow `../../references/minions-path.md`.

After this step you will have `minions_path`.

### Step 5: Pull latest minions

The minions repo updates frequently; pull before running:

```bash
git -C "{minions_path}" pull origin main
```

If this fails, warn the user and ask whether to proceed anyway.

### Step 6: Launch implement script in cmux workspace

The implement script must run in the minions repo, not the target repo:

```bash
cmux new-workspace --cwd "{minions_path}" --command "scripts/minions/implement {repo_path} {TICKET_URL}"
```

Capture the workspace reference from stdout. The output format is `OK workspace:N` -- extract the `workspace:N` part.

### Step 7: Rename workspace

```bash
cmux rename-workspace --workspace {workspace_ref} "{repo_basename}/{TICKET_ID}"
```

Where `repo_basename` is the basename of the target repo (e.g., `app` for `~/work/guideline/app`).

### Step 8: Report

```
Handed off to minions pipeline:
- Ticket: {TICKET_ID} ({TICKET_URL})
- Workspace: {repo_basename}/{TICKET_ID}
```

The pipeline runs autonomously — no further action needed.

## Examples

```
/minion TICKET-1234
/minion TICKET: migrate legacy auth tokens -- Move the old token format to the new encrypted scheme
minion TICKET-1234
spin off a minion for TICKET-1234
implement with minion TICKET-1234
```
