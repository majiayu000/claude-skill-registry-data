---
name: pr-prepare
description: "Prepare pull request descriptions for template changes. Activates on: prepare PR, create PR, pull request, ready for PR, draft PR, write PR"
---

# PR Preparation Skill

Automatically prepare pull request descriptions for template changes.

## Activation

This skill activates on keywords:
- "prepare PR", "prepare the PR", "prepare a PR"
- "create PR", "create pull request"
- "PR description", "pull request description"
- "ready for PR", "ready to PR"
- "draft PR", "write PR"

## Workflow

When activated, follow these steps:

### 1. Gather Context

Run these commands to understand the changes:

```bash
# Current state
git status

# Branch comparison
git log $(git merge-base HEAD main)..HEAD --oneline

# Files changed
git diff $(git merge-base HEAD main)..HEAD --stat
```

### 2. Analyze Template Changes

Identify:
- **Scope**: cookiecutter.json, hooks, template files, docs?
- **Purpose**: Why these changes were made
- **Impact**: Breaking changes for existing template users?
- **Testing**: Template generation tested?

### 3. Generate PR Description

Use this template format:

```markdown
## Summary

[1-3 sentences: what changed and why]

## Changes

- **[Component]**: [What changed and why]

## Scope

- [ ] `cookiecutter.json` (template variables)
- [ ] `hooks/` (generation hooks)
- [ ] `{{cookiecutter.project_slug}}/` (generated project files)
- [ ] Documentation

## Impact

- ✅ [Key benefit]
- ✅ No breaking changes to existing template users

## Testing

- [ ] Template generates with default options
- [ ] Template generates with features enabled
- [ ] Generated project passes `uv run pytest`

## Notes

[Optional: known issues, follow-up work]
```

### 4. Suggest PR Title

Follow conventional commits with template scopes:

| Scope | When to Use |
|-------|-------------|
| `feat(template):` | New template feature |
| `fix(hooks):` | Hook bug fix |
| `docs:` | Documentation |
| `chore(config):` | cookiecutter.json changes |
| `ci:` | Workflow changes |

### 5. Output

Present the complete PR description ready to copy-paste.

Remind the user:
- CodeRabbit will auto-fill summary
- Test template generation before pushing

## Example Output

**Suggested Title**: `feat(template): add CodeRabbit and Linear integrations`

**PR Description**:

```markdown
## Summary

Add CodeRabbit AI code reviews and Linear project management integration as optional features.

## Changes

- **cookiecutter.json**: New `include_coderabbit`, `include_linear`, `linear_team_key` variables
- **{{cookiecutter.project_slug}}/.coderabbit.yaml**: CodeRabbit configuration template
- **{{cookiecutter.project_slug}}/.github/PULL_REQUEST_TEMPLATE.md**: PR template with Linear support
- **hooks/post_gen_project.py**: Cleanup logic and success messages

## Scope

- [x] `cookiecutter.json` (template variables)
- [x] `hooks/` (generation hooks)
- [x] `{{cookiecutter.project_slug}}/` (generated project files)
- [x] Documentation

## Impact

- ✅ Projects can now use AI code reviews via CodeRabbit
- ✅ Linear integration for project management
- ✅ No breaking changes to existing template users

## Testing

- [x] Template generates with default options
- [x] Template generates with features enabled
- [x] Generated project structure validated

## Notes

CodeRabbit requires GitHub App installation after project creation.
```
