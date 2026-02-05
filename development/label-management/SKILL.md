---
name: label-management
description: Manage GitHub labels - create, edit, delete, apply labels, and organize with color coding using gh CLI
---
# GitHub Label Management Skill

This skill provides operations for managing repository labels, including creating, editing, deleting labels, and applying them to issues and pull requests for better organization and triage.

## Available Operations

### 1. Create Label
Create new labels with custom names, descriptions, and colors.

### 2. List Labels
View all labels in a repository.

### 3. Edit Label
Update label properties (name, color, description).

### 4. Delete Label
Remove labels from a repository.

### 5. Clone Labels
Copy labels from one repository to another.

### 6. Apply Labels to Issues/PRs
Add labels to issues and pull requests.

### 7. Remove Labels
Remove labels from issues and pull requests.

## Usage Examples

### Create Label

**Create basic label:**
```bash
gh label create bug --repo owner/repo-name \
  --description "Something isn't working" \
  --color d73a4a
```

**Create multiple labels:**
```bash
gh label create enhancement --repo owner/repo-name --description "New feature or request" --color a2eeef
gh label create documentation --repo owner/repo-name --description "Improvements or additions to documentation" --color 0075ca
gh label create "good first issue" --repo owner/repo-name --description "Good for newcomers" --color 7057ff
```

**Create with default color:**
```bash
gh label create "needs triage" --repo owner/repo-name --description "Needs initial review"
```

**Using API:**
```bash
gh api repos/owner/repo-name/labels \
  -f name="security" \
  -f description="Security related issues" \
  -f color="d93f0b"
```

### List Labels

**List all labels:**
```bash
gh label list --repo owner/repo-name
```

**Limit results:**
```bash
gh label list --repo owner/repo-name --limit 100
```

**Search labels:**
```bash
gh label list --repo owner/repo-name --search "bug"
```

**Order by name:**
```bash
gh label list --repo owner/repo-name --order asc
```

**JSON output:**
```bash
gh label list --repo owner/repo-name --json name,description,color
```

**Using API:**
```bash
gh api repos/owner/repo-name/labels --jq '.[] | {name, description, color}'
```

### Edit Label

**Update label name:**
```bash
gh label edit bug --repo owner/repo-name --name "bug-report"
```

**Update color:**
```bash
gh label edit bug --repo owner/repo-name --color ff0000
```

**Update description:**
```bash
gh label edit bug --repo owner/repo-name --description "Critical bug requiring immediate attention"
```

**Update multiple properties:**
```bash
gh label edit enhancement --repo owner/repo-name \
  --name feature \
  --description "New feature request" \
  --color 00ff00
```

**Using API:**
```bash
gh api repos/owner/repo-name/labels/bug \
  -X PATCH \
  -f new_name="critical-bug" \
  -f color="ff0000" \
  -f description="Critical issues"
```

### Delete Label

**Delete single label:**
```bash
gh label delete bug --repo owner/repo-name
```

**Delete with confirmation:**
```bash
gh label delete bug --repo owner/repo-name --yes
```

**Delete multiple labels:**
```bash
for label in "wontfix" "duplicate" "invalid"; do
  gh label delete "$label" --repo owner/repo-name --yes
done
```

**Using API:**
```bash
gh api repos/owner/repo-name/labels/wontfix -X DELETE
```

### Clone Labels

**Copy labels from another repository:**
```bash
# Get labels from source repo
gh label list --repo source-owner/source-repo --json name,description,color > labels.json

# Create labels in target repo
cat labels.json | jq -r '.[] | "\(.name)|\(.description)|\(.color)"' | \
  while IFS='|' read name desc color; do
    gh label create "$name" --repo owner/repo-name --description "$desc" --color "$color" 2>/dev/null || true
  done
```

**Clone from template repository:**
```bash
# Script to clone labels
SOURCE_REPO="template-owner/template-repo"
TARGET_REPO="owner/new-repo"

gh api repos/$SOURCE_REPO/labels --jq '.[]' | \
  jq -c '{name, description, color}' | \
  while read label; do
    gh api repos/$TARGET_REPO/labels \
      -f name="$(echo $label | jq -r '.name')" \
      -f description="$(echo $label | jq -r '.description')" \
      -f color="$(echo $label | jq -r '.color')"
  done
```

### Apply Labels to Issues/PRs

**Add label to issue:**
```bash
gh issue edit 123 --repo owner/repo-name --add-label "bug"
```

**Add multiple labels:**
```bash
gh issue edit 123 --repo owner/repo-name --add-label "bug,critical,needs-review"
```

**Add label to PR:**
```bash
gh pr edit 456 --repo owner/repo-name --add-label "enhancement"
```

**Using API:**
```bash
gh api repos/owner/repo-name/issues/123/labels \
  -f 'labels[]=bug' \
  -f 'labels[]=critical'
```

### Remove Labels

**Remove label from issue:**
```bash
gh issue edit 123 --repo owner/repo-name --remove-label "bug"
```

**Remove multiple labels:**
```bash
gh issue edit 123 --repo owner/repo-name --remove-label "bug,wontfix"
```

**Remove all labels:**
```bash
# Get all labels on issue
LABELS=$(gh issue view 123 --repo owner/repo-name --json labels --jq '.labels[].name' | tr '\n' ',')
gh issue edit 123 --repo owner/repo-name --remove-label "$LABELS"
```

**Using API:**
```bash
# Remove specific label
gh api repos/owner/repo-name/issues/123/labels/bug -X DELETE

# Remove all labels
gh api repos/owner/repo-name/issues/123/labels -X DELETE
```

## Common Patterns

### Standard Label Set

```bash
REPO="owner/repo-name"

# Issue Types
gh label create "bug" --repo $REPO --description "Something isn't working" --color "d73a4a"
gh label create "enhancement" --repo $REPO --description "New feature or request" --color "a2eeef"
gh label create "documentation" --repo $REPO --description "Improvements or additions to documentation" --color "0075ca"
gh label create "question" --repo $REPO --description "Further information is requested" --color "d876e3"

# Priority
gh label create "priority: high" --repo $REPO --description "High priority" --color "ff0000"
gh label create "priority: medium" --repo $REPO --description "Medium priority" --color "ffaa00"
gh label create "priority: low" --repo $REPO --description "Low priority" --color "00ff00"

# Status
gh label create "status: in progress" --repo $REPO --description "Work in progress" --color "fbca04"
gh label create "status: blocked" --repo $REPO --description "Blocked by dependencies" --color "b60205"
gh label create "status: needs review" --repo $REPO --description "Needs code review" --color "0e8a16"

# Community
gh label create "good first issue" --repo $REPO --description "Good for newcomers" --color "7057ff"
gh label create "help wanted" --repo $REPO --description "Extra attention is needed" --color "008672"
```

### Issue Triage Workflow

```bash
REPO="owner/repo-name"

# 1. List untriaged issues
gh issue list --repo $REPO --label "needs-triage" --state open

# 2. Review issue
gh issue view 123 --repo $REPO

# 3. Apply appropriate labels
gh issue edit 123 --repo $REPO \
  --add-label "bug,priority: high" \
  --remove-label "needs-triage"

# 4. Assign to team member
gh issue edit 123 --repo $REPO --add-assignee developer1
```

### Bulk Label Operations

```bash
REPO="owner/repo-name"

# Add label to multiple issues
for issue in 101 102 103 104 105; do
  gh issue edit $issue --repo $REPO --add-label "sprint-3"
done

# Remove stale label from closed issues
gh issue list --repo $REPO --state closed --label "stale" --json number --jq '.[].number' | \
  while read issue; do
    gh issue edit $issue --repo $REPO --remove-label "stale"
  done
```

### Label Cleanup

```bash
REPO="owner/repo-name"

# Find unused labels
ALL_LABELS=$(gh label list --repo $REPO --json name --jq '.[].name')

for label in $ALL_LABELS; do
  # Count issues with label
  COUNT=$(gh issue list --repo $REPO --label "$label" --state all --limit 1000 --json number --jq '. | length')

  if [ "$COUNT" -eq 0 ]; then
    echo "Unused label: $label"
    # Optionally delete
    # gh label delete "$label" --repo $REPO --yes
  fi
done
```

### Rename Label Across Issues

```bash
REPO="owner/repo-name"
OLD_LABEL="bug"
NEW_LABEL="defect"

# 1. Create new label
gh label create "$NEW_LABEL" --repo $REPO --description "Software defect" --color "d73a4a"

# 2. Find all issues with old label
gh issue list --repo $REPO --label "$OLD_LABEL" --state all --limit 1000 --json number --jq '.[].number' | \
  while read issue; do
    # Add new label
    gh issue edit $issue --repo $REPO --add-label "$NEW_LABEL"
    # Remove old label
    gh issue edit $issue --repo $REPO --remove-label "$OLD_LABEL"
  done

# 3. Delete old label
gh label delete "$OLD_LABEL" --repo $REPO --yes
```

### Color-Coded Categories

```bash
REPO="owner/repo-name"

# Type labels (Red shades)
gh label create "type: bug" --repo $REPO --color "d73a4a"
gh label create "type: feature" --repo $REPO --color "ff6b6b"
gh label create "type: refactor" --repo $REPO --color "ee5a6f"

# Area labels (Blue shades)
gh label create "area: frontend" --repo $REPO --color "0052cc"
gh label create "area: backend" --repo $REPO --color "0e8a16"
gh label create "area: database" --repo $REPO --color "1d76db"

# Effort labels (Green shades)
gh label create "effort: small" --repo $REPO --color "c2e0c6"
gh label create "effort: medium" --repo $REPO --color "7bcf8e"
gh label create "effort: large" --repo $REPO --color "0e8a16"
```

## Advanced Usage

### Label Analytics

**Count issues by label:**
```bash
gh label list --repo owner/repo-name --json name --jq '.[].name' | \
  while read label; do
    count=$(gh issue list --repo owner/repo-name --label "$label" --state all --json number --jq '. | length')
    echo "$label: $count"
  done | sort -t: -k2 -nr
```

**Most used labels:**
```bash
gh api repos/owner/repo-name/labels --jq '.[] | "\(.name)|\(.color)"' | \
  while IFS='|' read name color; do
    count=$(gh issue list --repo owner/repo-name --label "$name" --state all --limit 1000 --json number --jq '. | length')
    echo "$count|$name|$color"
  done | sort -t'|' -k1 -nr | head -10
```

### Label Templates

**Bug report labels:**
```bash
#!/bin/bash
REPO=$1

gh label create "severity: critical" --repo $REPO --color "b60205"
gh label create "severity: high" --repo $REPO --color "d93f0b"
gh label create "severity: medium" --repo $REPO --color "ff9800"
gh label create "severity: low" --repo $REPO --color "ffeb3b"

gh label create "status: confirmed" --repo $REPO --color "0e8a16"
gh label create "status: in progress" --repo $REPO --color "fbca04"
gh label create "status: fixed" --repo $REPO --color "00ff00"
```

**Project management labels:**
```bash
#!/bin/bash
REPO=$1

# Sprints
gh label create "sprint-1" --repo $REPO --color "bfd4f2"
gh label create "sprint-2" --repo $REPO --color "c5def5"
gh label create "sprint-3" --repo $REPO --color "d4e6f1"

# Milestones
gh label create "milestone: v1.0" --repo $REPO --color "0052cc"
gh label create "milestone: v2.0" --repo $REPO --color "1d76db"

# Dependencies
gh label create "dependencies" --repo $REPO --color "0366d6"
gh label create "blocked" --repo $REPO --color "b60205"
```

### Sync Labels Across Organization

```bash
#!/bin/bash
ORG="my-org"
TEMPLATE_REPO="my-org/template"

# Get all repos in org
gh api orgs/$ORG/repos --paginate --jq '.[].name' | \
  while read repo; do
    echo "Syncing labels for $ORG/$repo"

    # Get template labels
    gh api repos/$TEMPLATE_REPO/labels --jq '.[]' | \
      jq -c '{name, description, color}' | \
      while read label; do
        NAME=$(echo $label | jq -r '.name')
        DESC=$(echo $label | jq -r '.description')
        COLOR=$(echo $label | jq -r '.color')

        # Create or update label
        gh api repos/$ORG/$repo/labels \
          -f name="$NAME" \
          -f description="$DESC" \
          -f color="$COLOR" 2>/dev/null || \
        gh api repos/$ORG/$repo/labels/"$NAME" \
          -X PATCH \
          -f description="$DESC" \
          -f color="$COLOR"
      done
  done
```

### Auto-Label Based on File Changes

```bash
# In a PR workflow
REPO="owner/repo-name"
PR_NUMBER=123

# Get changed files
FILES=$(gh pr view $PR_NUMBER --repo $REPO --json files --jq '.files[].path')

# Auto-apply labels based on paths
if echo "$FILES" | grep -q "^frontend/"; then
  gh pr edit $PR_NUMBER --repo $REPO --add-label "area: frontend"
fi

if echo "$FILES" | grep -q "^backend/"; then
  gh pr edit $PR_NUMBER --repo $REPO --add-label "area: backend"
fi

if echo "$FILES" | grep -q "\.test\."; then
  gh pr edit $PR_NUMBER --repo $REPO --add-label "tests"
fi

if echo "$FILES" | grep -q "\.md$"; then
  gh pr edit $PR_NUMBER --repo $REPO --add-label "documentation"
fi
```

## Error Handling

### Label Already Exists
```bash
# Check if label exists
gh label list --repo owner/repo-name --search "bug" --json name --jq '.[].name' | grep -q "^bug$" && echo "Exists" || echo "Does not exist"

# Create or update
gh label create "bug" --repo owner/repo-name --color "d73a4a" 2>&1 | grep -q "already exists" && \
  gh label edit "bug" --repo owner/repo-name --color "d73a4a"
```

### Label Not Found
```bash
# Verify label exists before editing
if gh label list --repo owner/repo-name --search "bug" --json name --jq '.[].name' | grep -q "^bug$"; then
  gh label edit "bug" --repo owner/repo-name --color "ff0000"
else
  echo "Label 'bug' not found"
fi
```

### Invalid Color Code
```bash
# Validate hex color (6 characters, no #)
COLOR="d73a4a"
if [[ $COLOR =~ ^[0-9a-fA-F]{6}$ ]]; then
  gh label create "bug" --repo owner/repo-name --color "$COLOR"
else
  echo "Invalid color code: $COLOR"
fi
```

## Best Practices

1. **Use consistent naming**: Adopt a naming convention (e.g., "type: bug", "priority: high")
2. **Limit label count**: Too many labels reduce effectiveness (aim for 15-30)
3. **Use color coding**: Group related labels with similar colors
4. **Document labels**: Use descriptions to explain when to use each label
5. **Regular cleanup**: Remove unused labels periodically
6. **Template across repos**: Use consistent labels across organization
7. **Combine labels**: Use multiple labels for detailed categorization
8. **Avoid redundancy**: Don't create overlapping labels
9. **Make discoverable**: Use clear, searchable names
10. **Review usage**: Analyze which labels are actually being used

## Common Label Categories

### Issue Types
- bug, enhancement, documentation, question, feature

### Priority
- priority: critical, priority: high, priority: medium, priority: low

### Status
- status: in progress, status: blocked, status: needs review, status: ready

### Area/Component
- area: frontend, area: backend, area: api, area: database, area: ui

### Effort/Size
- size: xs, size: s, size: m, size: l, size: xl

### Community
- good first issue, help wanted, hacktoberfest, beginner-friendly

## Integration with Other Skills

- Use `issue-management` to apply labels during issue creation
- Use `pull-request-management` to label PRs automatically
- Use `workflow-management` to auto-label based on CI/CD results
- Use `project-management` to organize by labels in project boards

## References

- [GitHub CLI Label Documentation](https://cli.github.com/manual/gh_label)
- [GitHub Labels Guide](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [Label Best Practices](https://medium.com/@dave_lunny/sane-github-labels-c5d2e6004b63)
- [GitHub Labels API](https://docs.github.com/en/rest/issues/labels)
