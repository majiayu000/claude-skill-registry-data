---
name: feature-branch
description: Create a feature branch from an Azure DevOps ticket. Fetches ticket title, slugifies, creates `feature/<id>-<slug>`, and optionally transitions ticket to Active. Trigger when user says "feature branch", "create branch", "/dev-azdo:feature-branch", or provides a ticket id/URL to start work on.
---

# Feature Branch

Create `feature/<ticket-id>-<slug>` from an Azure DevOps work item.

## Input Detection

Take the ticket from the request.

| Form                                  | Meaning                                     |
| ------------------------------------- | ------------------------------------------- |
| empty                                 | look in recent context for ticket; else ask |
| numeric (`12345`)                     | ticket id, fetch title for slug             |
| URL containing `_workitems/edit/<id>` | extract id, fetch title                     |
| `<id> <slug-override>`                | use override slug, skip title fetch         |

## Workflow

### 1. Resolve ticket + slug

#### empty

Scan recent conversation for work item id + title (e.g. prior triage output). Else ask user.

#### id / URL

```bash
az boards work-item show --id <id> --query '{id:id, title:fields."System.Title"}' -o json
```

Slugify title: lowercase, strip special chars, spaces→hyphens, 3–5 words max.

#### `<id> <override>`

Use override directly. Slugify same rules.

### 2. Pre-flight

```bash
git status --short
```

If dirty, warn and ask: stash or abort.

```bash
git branch --show-current
```

Resolve the default branch as described in `${CLAUDE_PLUGIN_ROOT}/references/conventions.md`.
The new branch starts from the current HEAD. If the current branch is not the default branch,
name it and ask whether stacking the new branch on it is intended. On no, stop and let the user
switch first. Skip the question when `feature/<id>-<slug>` already exists, since step 3 only
switches to it.

### 3. Create branch

```bash
git checkout -b feature/<id>-<slug>
```

If branch already exists → switch to it instead, inform user.

### 4. Optional: transition ticket → Active

Prompt: "Transition ticket #<id> to Active? (y/N)"

Default: **No**.

If yes → invoke the `ticket` skill with `state <id> active`.

### 5. Confirm

Print created branch name + ticket transition status.

## Notes

- Branch and ticket transition are intentionally separate. `feature-branch` only offers the transition.
- Later state changes are offered by `dev-azdo:pr` (Code Review after `create`, the next state after `complete`) and go through the `ticket` skill.
