---
name: refine-issue
description: Refining issues with technical context and structured details. Use when expanding a brief bug, feature, or refactor description into a detailed issue suitable for developers and AI agents.
---

# Issue Refinement

Expand brief issue descriptions into structured issues for developers and AI agents.

## Issue Types

| Type | When to Use | Guide |
|------|-------------|-------|
| Bug | Something is broken | `bug.md` |
| Feature | New capability | `feature.md` |
| Refactor | Internal improvement, no behavior change | `refactor.md` |

## Workflow

1. Identify type and read the corresponding guide
2. Gather context from code and related issues
3. Draft refinement following the type-specific structure
4. Output for user approval before updating the issue

## Output Structure

All issues share this skeleton. Type guides add sections in between.

```markdown
## Summary

One to two sentences.

[Type-specific sections from guide]

## Context

### Related Code

Files that need changes or inform the work.

### Related Issues

Links to related issues, prior attempts, upstream work.
```

## Style

- **Direct** - Facts, not hedging
- **Specific** - Name the function, file, behavior
- **Concise** - Every sentence adds information
- **Link to code** - Permalinks for GitHub (`https://github.com/{owner}/{repo}/blob/{sha}/path#L10-L20`), file paths elsewhere (`path/to/file:10-20`)

## Issue Trackers

Fetch with `get_issue`, output refinement for review, update only after approval.

- Linear: `mcp__linear__get_issue`, `mcp__linear__update_issue`
- GitHub: `mcp__github__get_issue`, `mcp__github__update_issue`
