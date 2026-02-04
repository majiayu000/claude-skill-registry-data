---
name: file-issue
description: File a bug report or feature request to a project's GitHub repository
group: github
keywords: [github, issues, bug report, feature request, bug, feature, filing issues]
version: 1.0.0
author: docent
---

# File Issue Runbook

This runbook files bug reports, feature requests, questions, or documentation issues to a project's GitHub repository using the `gh` CLI.

## Purpose

Standardize issue creation with proper formatting, required information, and appropriate labels. Works with any project configured in `.docent/config.yaml`.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- Project configured in `.docent/config.yaml` with repository information
- Network connectivity to GitHub

## Variables

This runbook accepts the following variables:

- **project**: Which project to file against (default: current project)
- **type**: bug | feature | question | documentation
- **title**: Issue title (required)
- **description**: Issue body (required)

Additional type-specific variables:

**For bugs:**

- **actual_behavior**: What's happening now
- **expected_behavior**: What should happen
- **reproduction_steps**: How to reproduce the bug

**For features:**

- **use_case**: Why this feature is needed
- **suggested_solution**: Proposed implementation (optional)

**For documentation:**

- **location**: Where documentation is unclear/missing
- **suggestion**: Proposed improvement

## Procedure

### Step 1: Resolve Project Repository

**Action:** Determine which GitHub repository to file against

**From `.docent/config.yaml`:**

```yaml
projects:
  docent:
    repo: tnez/docent
  my-app:
    repo: user/my-app
```

**Resolution logic:**

1. If `project` variable provided → use that project's repo
2. If `project = "current"` or not provided → detect from git remote
3. If no config and no git remote → error (cannot determine repo)

**Commands:**

```bash
# Get current repo from git remote
git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/'

# Validate repo exists
gh repo view <owner/repo> --json name
```

**Validation:**

- Repository identifier is in `owner/repo` format
- Repository exists and is accessible
- User has permission to create issues

---

### Step 2: Format Issue Based on Type

**Action:** Generate appropriate issue template based on type

#### Bug Report Format

```markdown
## Description

{{description}}

## Current Behavior

{{actual_behavior}}

## Expected Behavior

{{expected_behavior}}

## Steps to Reproduce

{{reproduction_steps}}

## Environment

- OS: {{os}}
- Version: {{version}}

---

Filed via [docent](https://github.com/tnez/docent)
```

#### Feature Request Format

```markdown
## Feature Description

{{description}}

## Use Case

{{use_case}}

## Suggested Solution

{{suggested_solution}}

---

Filed via [docent](https://github.com/tnez/docent)
```

#### Question Format

```markdown
## Question

{{description}}

---

Filed via [docent](https://github.com/tnez/docent)
```

#### Documentation Issue Format

```markdown
## Documentation Issue

{{description}}

## Location

{{location}}

## Suggested Improvement

{{suggestion}}

---

Filed via [docent](https://github.com/tnez/docent)
```

---

### Step 3: Add Appropriate Labels

**Action:** Determine labels based on issue type

**Label mapping:**

- bug → `bug`
- feature → `enhancement`, `feature-request`
- question → `question`
- documentation → `documentation`

**Additional labels** (if detectable):

- Project area (e.g., `mcp`, `templates`, `documentation`)
- Priority (e.g., `priority: high` if certain keywords present)

**Commands:**

```bash
# Check available labels for repository
gh label list --repo <owner/repo>
```

---

### Step 4: Create GitHub Issue

**Action:** File the issue using `gh issue create`

**Commands:**

```bash
# Create issue with body from file
gh issue create \
  --repo <owner/repo> \
  --title "<title>" \
  --body "<formatted body>" \
  --label "<labels>"

# Example for bug:
gh issue create \
  --repo tnez/docent \
  --title "Bootstrap fails with permission error" \
  --body "$(cat issue-body.md)" \
  --label "bug"
```

**Validation:**

- Issue created successfully
- Issue number returned
- Issue URL accessible

---

### Step 5: Report Success

**Action:** Provide confirmation with issue link

**Success Message:**

```
✅ Issue filed successfully!

Issue #123: <title>
URL: https://github.com/<owner/repo>/issues/123

The issue has been created with:
  - Type: <type>
  - Labels: <labels>
  - Status: Open

You can view and track the issue at the URL above.
```

**Additional actions:**

- Copy issue URL to clipboard (if supported)
- Optionally log to `.docent/journals/` for tracking

---

## Examples

### Example 1: File Bug in Docent

**Invocation:**

```
/docent:act file issue in docent: bootstrap fails on Windows with permission error

(Agent interprets and extracts):
- project: docent
- type: bug
- title: "Bootstrap fails on Windows with permission error"
- description: "When running bootstrap on Windows, permission denied error occurs"
```

**Generated issue:**

- Repo: tnez/docent
- Title: "Bootstrap fails on Windows with permission error"
- Labels: bug
- Body: Formatted bug report

---

### Example 2: Feature Request for Current Project

**Invocation:**

```
/docent:act file feature request: add dark mode support

(Agent interprets):
- project: current (detected from git remote)
- type: feature
- title: "Add dark mode support"
- use_case: Better UX for users working at night
```

**Generated issue:**

- Repo: user/my-app (from git remote)
- Title: "Add dark mode support"
- Labels: enhancement, feature-request
- Body: Formatted feature request

---

### Example 3: Documentation Issue

**Invocation:**

```
/docent:act file documentation issue for docent: getting started guide is outdated

(Agent interprets):
- project: docent
- type: documentation
- title: "Getting started guide is outdated"
- location: docs/guides/getting-started.md
```

**Generated issue:**

- Repo: tnez/docent
- Title: "Getting started guide is outdated"
- Labels: documentation
- Body: Formatted documentation issue

---

## Error Handling

### gh CLI Not Authenticated

**Symptoms:** `gh issue create` fails with authentication error

**Fix:**

```bash
# Authenticate with GitHub
gh auth login

# Follow prompts to authenticate
```

**Validation:** `gh auth status` shows authenticated

---

### Repository Not Found

**Symptoms:** Cannot find repository from config or git remote

**Fix:**

1. Check `.docent/config.yaml` has correct repo
2. Verify git remote: `git remote get-url origin`
3. Provide explicit project parameter

---

### Permission Denied

**Symptoms:** Cannot create issues in repository

**Fix:**

- Verify you have access to the repository
- Check repository settings allow issue creation
- Use `gh auth refresh` to update permissions

---

### Network Error

**Symptoms:** Cannot reach GitHub

**Fix:**

- Check internet connectivity
- Verify GitHub status: https://www.githubstatus.com
- Retry after connectivity restored

---

## Configuration

Add projects to `.docent/config.yaml`:

```yaml
projects:
  docent:
    repo: tnez/docent
    default_labels:
      - via-docent

  my-app:
    repo: user/my-app
    default_labels:
      - automated

  work-project:
    repo: company/project
    default_labels:
      - from-docent
      - needs-triage
```

**Options:**

- `repo`: GitHub repository in owner/repo format (required)
- `default_labels`: Labels to add to all issues (optional)

---

## Validation

After filing issue:

- Issue exists at provided URL
- Issue has correct title and body
- Labels are applied correctly
- Issue is searchable in GitHub

---

## Notes

- Issues are filed with attribution: "Filed via docent"
- Attribution helps track which issues came from docent for analytics
- Users can edit issues after filing via GitHub UI
- Issue URLs are permanent (even if issue is closed/deleted)
- Consider logging filed issues to journal for personal tracking

---

## Advanced Usage

### Batch Issue Filing

File multiple related issues:

```
/docent:act file issues for planned features:
1. Add export functionality
2. Implement search
3. Create user dashboard
```

Agent can interpret and file 3 separate feature requests

### Issue Templates

Projects can define custom templates in `.docent/templates/issue-*.md` that override default formats

### Auto-labeling

Configure intelligent labeling based on content:

```yaml
projects:
  my-app:
    repo: user/my-app
    auto_labels:
      - pattern: "auth|login|password"
        labels: ["area: auth"]
      - pattern: "slow|performance|speed"
        labels: ["performance"]
```

---

## Related Runbooks

- `health-check` - Find issues to file before they become bugs
- `code-review` - Review changes before filing improvement issues
