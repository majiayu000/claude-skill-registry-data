---
name: gh-issue-lifecycle
description: GitHub issue state machine and code integration patterns. Covers state transitions (needs-triage → accepted → in-progress → completed), branch naming (feat/123-desc), PR linking (Closes #123), close reasons (duplicate/won't fix/invalid/stale), and bulk operations.
---

# Issue Lifecycle

State machine for GitHub issues and how they connect to code.

## State Diagram

```
                    ┌─────────────────┐
                    │  needs-triage   │ ← New issue created
                    └────────┬────────┘
                             │ triage
                    ┌────────▼────────┐
        ┌───────────│    accepted     │ ← In backlog
        │           └────────┬────────┘
        │                    │ start work
        │           ┌────────▼────────┐
        │    ┌──────│  in-progress    │ ← Active development
        │    │      └────────┬────────┘
        │    │               │ PR merged
        │    │      ┌────────▼────────┐
        │    │      │    completed    │ ← Issue resolved
        │    │      └─────────────────┘
        │    │
        │    │ blocked
        │    │      ┌─────────────────┐
        │    └─────►│     blocked     │ ← Waiting on dependency
        │           └─────────────────┘
        │
        │ needs-info
        │           ┌─────────────────┐
        └──────────►│   needs-info    │ ← Waiting for clarification
                    └─────────────────┘
```

## State Definitions

### Open States

| State | Label | Meaning |
|-------|-------|---------|
| New | `needs-triage` | Just created, not reviewed |
| Clarification | `needs-info` | Waiting on reporter |
| Backlog | `accepted` | Triaged, waiting for work |
| Active | `in-progress` | Someone is working on it |
| Blocked | `blocked` | Can't proceed |

### Closed States

| State | Reason | Comment |
|-------|--------|---------|
| Completed | Fixed/implemented | Via PR or manual |
| Duplicate | Same as another | "Duplicate of #N" |
| Won't Fix | Out of scope | Explain why |
| Invalid | Not a real issue | Cannot reproduce |
| Stale | No activity | Auto-closed after warning |

## Linking Issues to Code

### Branch Naming

When starting work on issue `#123`:

```
feat/123-short-description    # feature
fix/123-short-description     # bug fix
chore/123-short-description   # maintenance
docs/123-short-description    # documentation
i18n/locale-code              # internationalization (e.g., i18n/zh-CN, i18n/ja-JP)
i18n/123-locale-code          # i18n with issue (e.g., i18n/42-es-MX)
```

Examples:
- `feat/42-add-dark-mode`
- `fix/123-login-timeout`
- `chore/99-update-deps`
- `i18n/zh-CN` - Chinese (Simplified) translations
- `i18n/42-ja-JP` - Japanese translations for issue #42

### PR Title

Include issue number in PR title:

```
feat: add dark mode (#42)
fix: resolve login timeout (#123)
chore: update dependencies (#99)
```

### PR Description

Use closing keywords in PR body:

| Keyword | Effect |
|---------|--------|
| `Closes #123` | Auto-closes when merged |
| `Fixes #123` | Same as Closes |
| `Resolves #123` | Same as Closes |

Example PR description:
```markdown
## Summary
Add dark mode toggle to settings page.

Closes #42

## Changes
- Add theme context
- Create toggle component
- Update color variables
```

### Linking Without Closing

Reference issues without auto-close:

```
Related to #45
See also #67
Depends on #89
```

## Manual Close Reasons

When closing without PR, always comment:

### Duplicate
```bash
gh issue close 123 --comment "Duplicate of #456"
```

### Won't Fix
```bash
gh issue close 123 --comment "Closing as won't fix: [reason]"
```

### Invalid / Cannot Reproduce
```bash
gh issue close 123 --comment "Cannot reproduce with provided steps. Please reopen with more details if issue persists."
```

### Stale
```bash
gh issue close 123 --comment "Closing due to inactivity. Please reopen if still relevant."
```

## Stale Issue Handling

### Detection

Issues with no activity for N days (typically 90):

```bash
# Find stale issues
gh issue list --search "updated:<$(date -v-90d +%Y-%m-%d)"
```

### Warning Process

1. Add `stale` label
2. Comment:
   ```
   This issue has been inactive for 90 days.
   It will be closed in 30 days if there's no further activity.
   Please comment if this is still relevant.
   ```
3. Close after 30 more days if no response

### Automation (GitHub Action)

```yaml
name: Stale Issues
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue has been inactive for 90 days.'
          days-before-stale: 90
          days-before-close: 30
          stale-issue-label: 'stale'
```

## Bulk Operations

### Close Multiple Issues

```bash
# Close all issues with label
gh issue list --label "stale" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closing stale issue"
```

### Relabel Issues

```bash
# Add label to all issues matching query
gh issue list --search "is:open label:bug" --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "needs-review"
```

### Transfer Issues

```bash
# Move issue to another repo
gh issue transfer 123 owner/other-repo
```

## Workflow Commands

### Start Work on Issue

```bash
# Create branch from issue
gh issue develop 123 --checkout

# Or manually
git checkout -b fix/123-description main
gh issue edit 123 --add-label "in-progress"
```

### Complete Issue via PR

```bash
# Create PR that closes issue
gh pr create --title "fix: resolve issue (#123)" --body "Closes #123"
```

### Mark as Blocked

```bash
gh issue edit 123 \
  --remove-label "in-progress" \
  --add-label "blocked"
gh issue comment 123 --body "Blocked on #456"
```

## Integration with Other Components

### Full Issue Workflow
1. **Create**: Use **gh-issue-templates** to format issue
2. **Triage**: Use **gh-issue-triage** to add type/priority labels
3. **Start Work**: Use this skill's branch naming patterns (feat/123-desc)
4. **Link to Code**: Reference issue in PR using `Closes #123`
5. **Close**: Use **gh-wrangler** agent with this skill's close patterns
6. **Cleanup**: PR merge auto-closes issue via GitHub

### State Transitions
This skill defines how issues move through states:
- `needs-triage` → Initial state (set by **gh-issue-templates**)
- `accepted` → After triage (applied by **gh-wrangler** using **gh-issue-triage**)
- `in-progress` → Work started (manual or via branch creation)
- `blocked` → Can't proceed (set manually with comment)
- Closed → Via PR merge or manual close

### Branch and PR Integration
When starting work on an issue:
```bash
# Branch naming from this skill
git checkout -b feat/123-description

# PR creation with linking
gh pr create --title "feat: description (#123)" --body "Closes #123"
```

## Related

- Skill: `gh-issue-templates` - Creating well-formatted issues
- Skill: `gh-issue-triage` - Labeling and prioritization
- Agent: `gh-wrangler` - Interactive lifecycle management
