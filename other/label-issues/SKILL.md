---
name: label-issues
description: Label unlabeled GitHub issues with priority and type labels. Use when triaging issues, cleaning up the backlog, or when asked to label/triage issues.
disable-model-invocation: true
allowed-tools: Bash(gh *), AskUserQuestion
---

# Label GitHub Issues

Triage unlabeled issues by assigning priority and type labels with user confirmation.

## Workflow

### Step 1: Fetch context

Run these commands to get current state:

```bash
# Get unlabeled issues (no labels at all)
gh issue list --json number,title,body,labels --jq '.[] | select(.labels | length == 0)'

# Get available labels
gh label list
```

If no unlabeled issues exist, inform the user and stop.

### Step 2: Process each issue

For each unlabeled issue:

1. **Show the issue**:
   - Issue number and title
   - First 200 characters of body (if present)

2. **Suggest labels**:
   - **Priority** (exactly one): `priority: critical`, `priority: high`, `priority: medium`, or `priority: low`
   - **Type** (one or more): `bug`, `enhancement`, `documentation`, `question`, etc.

   Base suggestions on:
   - Title keywords (fix/bug/error → bug, add/feature/request → enhancement)
   - Body content and tone
   - Severity indicators

3. **Ask for confirmation** using AskUserQuestion:
   - Show your suggested labels
   - Let user approve, modify, or skip

4. **Apply labels** if approved:
   ```bash
   gh issue edit <number> --add-label "priority: medium" --add-label "enhancement"
   ```

5. **Move to next issue**

## Label Guidelines

| Priority | Use when |
|----------|----------|
| `priority: critical` | Blocks release, security issue, data loss |
| `priority: high` | Major bug, key feature request |
| `priority: medium` | Standard work item |
| `priority: low` | Nice to have, minor improvement |

## Example Interaction

```
Issue #42: "App crashes when clicking submit"
Body: "After filling the form, clicking submit causes the app to crash..."

Suggested labels:
- priority: high (crash = significant impact)
- bug (crash indicates defect)

Apply these labels? [Yes / Modify / Skip]
```
