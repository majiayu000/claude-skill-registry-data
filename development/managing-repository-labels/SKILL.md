---
name: Managing Repository Labels
description: Reviews existing repository issues, code structure, and domain to create or refresh a semantic label system with appropriate colors aligned to the repository's specific context and needs. Use for initial setup or periodic maintenance (every 6-12 months) when users mention "labels", "label organization", "repository cleanup", "label system", or when detecting labeling inconsistencies.
platforms: ["claude-code"]
status: stable
allowed-tools: ["Bash","gh","Glob","Grep","Read","Write"]
requires: ["gh CLI authenticated","repository write access"]
tags: ["github","labels","organization","maintenance","setup"]
---

# Managing Repository Labels

Analyze repository context and establish or refresh a semantic label system tailored to the project's domain and needs.

## What you should do

When invoked, help the user create or refresh their repository's label system by:

1. **Understanding the request** - Determine what's needed:
   - Initial setup for new repository
   - Periodic refresh (6-12 month cycle)
   - Standardization across organization
   - Migration from legacy labels

2. **Analyzing the repository** - Gather context:
   - Technology stack and project type
   - Existing issue patterns
   - Current label usage and gaps
   - Team terminology

3. **Designing the label system** - Create semantic labels:
   - Core categories (bug, enhancement, question)
   - Domain-specific labels (api, frontend, pipeline, etc.)
   - Apply semantic color philosophy
   - Ensure no redundancy or overlap

4. **Implementing changes** - Execute carefully:
   - Create new labels with proper colors
   - Migrate issues from old to new labels
   - Delete obsolete labels (after verification)
   - Audit and label unlabeled issues

5. **Documenting the system** - Create `.github/LABELS.md`:
   - Label categories and descriptions
   - Usage guidelines
   - Migration history

## When to use this skill

**Trigger phrases:**
- "Set up labels"
- "Organize our labels"
- "Label system is a mess"
- "Standardize labels"
- "Clean up labels"
- "Refresh label system"

**Proactive detection:**
- Many unlabeled issues detected
- Duplicate labels observed (e.g., `docs` and `documentation`)
- Inconsistent label usage
- Project scope has expanded
- Team mentions label confusion

**Scheduled maintenance:**
- Every 6-12 months for active repositories
- When merging multiple repositories
- After significant project evolution

## Analysis process

### 1. Analyze repository context

```bash
# Get repository information
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
REPO_DESCRIPTION=$(gh repo view --json description -q .description)

# List existing labels
gh label list --json name,description,color --limit 100

# Analyze recent issues for patterns
gh issue list --limit 50 --json title,body,labels --state all
```

**Look for:**
- Technology stack (languages, frameworks)
- Issue patterns (security, performance, bugs, features)
- Team terminology (what words do they use?)
- Missing label coverage (unlabeled issues)

### 2. Determine label categories

**Core categories** (most repositories need):
- **Nature**: bug, enhancement, question
- **Domain-specific**: Labels specific to project type (api, frontend, backend)
- **Quality**: testing, refactor, docs
- **Infrastructure**: ci, dependencies, config
- **Impact**: security, performance, accessibility

> **Important**: Do NOT create labels for status (todo/done), priority (high/low), value (essential/nice-to-have), or effort (heavy/light). These should be managed as custom fields in GitHub Projects V2, not labels.

**Repository-specific examples:**
- **API project**: endpoint, schema, authentication
- **Data project**: pipeline, validation, data-quality
- **UI project**: ux, accessibility, design-system
- **Library**: breaking-change, deprecation, api

## Color assignment

Use semantic color philosophy to communicate meaning visually. See [LABEL-COLORS.md](LABEL-COLORS.md) for complete reference.

### Quick reference

| Category | Hex Code | Use Case |
|----------|----------|----------|
| Critical (Red) | `FF3B30` | bug, breaking-change |
| High Priority (Orange) | `FF9500` | security, performance |
| Success (Green) | `34C759` | testing, quality |
| Enhancement (Light Green) | `30D158` | enhancement, feature-request |
| Refinement (Purple) | `AF52DE` | refactor, cleanup |
| Infrastructure (Cyan) | `00C7BE` | ci, deployment |
| Technical (Blue) | `007AFF` | dependencies, architecture |
| Routine (Gray) | `8E8E93` | docs, config |

### Color selection rules

1. **Darker shades = higher urgency** within same color family
2. **Never use pure red (`FF0000`)** - too alarming
3. **Limit to 2-3 shades per color family** - avoid confusion
4. **Test accessibility** - ensure WCAG AA contrast
5. **Match GitHub defaults** - `bug` uses `FF3B30`

## Implementation workflow

### Step 1: Create or update labels

```bash
# Create new labels
gh label create "bug" --description "Something isn't working" --color "FF3B30"

# Update existing labels
gh label edit "bug" --description "Something isn't working" --color "FF3B30"
```

### Step 2: Migrate issues

Before deleting obsolete labels, migrate issues:

```bash
# List issues with old label
OLD_LABEL="old-label-name"
NEW_LABEL="new-label-name"

ISSUES=$(gh issue list --label "$OLD_LABEL" --json number --jq '.[].number')

# Migrate each issue
for issue in $ISSUES; do
  echo "Migrating issue #$issue from $OLD_LABEL to $NEW_LABEL"
  gh issue edit $issue --remove-label "$OLD_LABEL" --add-label "$NEW_LABEL"
done
```

**Migration strategies:**
- **Direct replacement**: Old label → New label (1:1)
- **Split**: One old → Multiple new (e.g., `feature` → `enhancement` + domain)
- **Consolidate**: Multiple old → One new (e.g., `high-priority` + `critical` → `security`)
- **Drop**: Remove obsolete labels

### Step 3: Clean up obsolete labels

After migration, delete old labels:

```bash
# Verify label has no remaining issues
REMAINING=$(gh issue list --label "old-label" --json number --jq 'length')

if [ "$REMAINING" -eq 0 ]; then
  gh label delete "old-label"
  echo "Deleted obsolete label: old-label"
else
  echo "Warning: $REMAINING issues still use old-label"
fi
```

**Common labels to clean up:**
- **Status labels**: `todo`, `in-progress`, `done`, `backlog` (use Status custom field)
- **Priority labels**: `high-priority`, `low-priority`, `p0`, `p1` (use Value/Effort custom fields)
- **Value labels**: `essential`, `nice-to-have` (use Value custom field)
- **Effort labels**: `heavy`, `light`, `quick-win` (use Effort custom field)
- Duplicate labels (e.g., `documentation` and `docs`)
- Vague labels (e.g., `needs-work`, `help-wanted`)
- Legacy project-specific labels

### Step 4: Audit unlabeled issues

```bash
# Find unlabeled issues
gh issue list --label "" --limit 100 --json number,title

# Review and apply appropriate labels
for issue in $(gh issue list --label "" --json number --jq '.[].number' | head -20); do
  gh issue view $issue
  # gh issue edit $issue --add-label "appropriate-label"
done
```

### Step 5: Document the system

Create or update `.github/LABELS.md`:

```markdown
# Repository Labels

## Label Categories

### Critical Issues (Red-Orange)
- `bug` - Something isn't working
- `security` - Security-related issues
- `performance` - Performance improvements

### Quality (Green)
- `testing` - Test suite improvements
- `docs` - Documentation updates

### Infrastructure (Blue-Cyan)
- `ci` - Continuous integration
- `dependencies` - Dependency updates

## When to Use

**bug**: Broken functionality, errors, or unexpected behavior
**security**: Any security vulnerability or concern
**testing**: Test suite or testing infrastructure changes
**docs**: Documentation improvements

## Multiple Labels

Issues can have multiple labels:
- `bug` + `security`: Security vulnerability
- `enhancement` + `performance`: Performance-improving feature

## Migration History

### YYYY-MM-DD: Label system refresh
- **Reason**: [Initial setup | Periodic refresh | Project scope expansion]
- **Changes made**:
  - Migrated `feature` → `enhancement`
  - Consolidated `high-priority`, `urgent` → `security`
  - Deleted obsolete labels: `wontfix`, `invalid`
  - Added domain labels: `api`, `frontend`, `backend`
- **Issues affected**: XX issues migrated

**Maintenance schedule:**
- Review label system every 6-12 months
- Document each refresh with date and reason
- Update this file when label changes are made
```

## Quality gates

Before completing, verify:

- [ ] Labels cover all common issue types in repository
- [ ] Colors follow semantic color philosophy
- [ ] Descriptions are clear and actionable
- [ ] No redundant or overlapping labels
- [ ] All issues migrated from old to new labels
- [ ] Obsolete labels verified empty and deleted
- [ ] Documentation created in `.github/LABELS.md` with migration history
- [ ] Unlabeled issues reviewed and labeled appropriately

## Expected outcomes

- Consistent label system aligned to repository needs
- Semantic colors that communicate priority/type visually
- Clear documentation for contributors
- Existing issues properly categorized
- Foundation for better issue triage and project management
- Maintenance schedule established

## Repository type examples

### API/Backend project

- `api`, `endpoint`, `database`, `authentication`
- `bug`, `security`, `performance`
- `testing`, `docs`, `ci`

### Frontend project

- `ui`, `ux`, `accessibility`, `design-system`
- `bug`, `browser-compat`, `performance`
- `testing`, `docs`, `dependencies`

### Data/Pipeline project

- `pipeline`, `validation`, `data-quality`
- `bug`, `performance`, `config`
- `testing`, `docs`, `dependencies`

### Library/Framework

- `api`, `breaking-change`, `deprecation`
- `bug`, `enhancement`, `docs`
- `examples`, `testing`, `dependencies`

## Integration with other skills

**Works with:**
- **`gh-project-setup`** - Use during initial project setup
- **`git-issue-create`** - References label system for new issues
- **`gh-project-manage`** - Complements project field management

**Triggers from:**
- Repository onboarding workflows
- Project setup automation
- Issue creation detecting missing labels
- Team requesting better organization