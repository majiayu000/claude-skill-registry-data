---
name: pr-writer
description: |
  This skill should be used when the user asks to "create a PR", "open a pull request",
  "write a PR description", "push and create PR", or needs to generate a best-in-class
  pull request description based on commits. Provides industry-standard PR description
  formatting following conventional commits, Microsoft Engineering Playbook, and
  HackerOne best practices.
---

# PR Writer Skill

Generate industry best-in-class pull request descriptions by analyzing commits and
producing clear, comprehensive, and reviewer-friendly PR content.

## Best Practices Sources

This skill synthesizes PR description best practices from:
- [Microsoft Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/pull-requests/)
- [HackerOne PR Guide](https://www.hackerone.com/blog/writing-great-pull-request-description)
- [Graphite PR Best Practices](https://graphite.com/guides/github-pr-description-best-practices)
- Conventional Commits specification

## PR Title Format

Follow the Conventional Commits format:

```
<type>[optional scope]: <concise description>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style/formatting (no logic change)
- `refactor` - Code refactoring (no feature/fix)
- `perf` - Performance improvement
- `test` - Adding/updating tests
- `chore` - Build process, dependencies, tooling
- `ci` - CI/CD changes
- `revert` - Reverting previous changes

**Examples:**
- `feat(auth): add OAuth2 login support`
- `fix(api): handle null response in user endpoint`
- `refactor(live-tutor): extract model connection classes`

## PR Description Template

```markdown
## Summary

<2-3 sentences explaining what changed at a high level>

## Motivation

<Why this change is needed - business goal or engineering improvement>

## Changes

<Bullet list of key changes, organized by area if multiple>

- Changed X to do Y
- Added Z for W
- Removed deprecated Q

## Testing

<How the changes were tested>

- [ ] Unit tests pass
- [ ] Manual testing performed
- [ ] E2E tests updated (if applicable)

## Screenshots

<For UI changes, include before/after screenshots>

## Breaking Changes

<If any, describe what breaks and migration path>

## Related Issues

<Link to tickets, issues, or related PRs>

Closes #123
Related to #456
```

## Writing Guidelines

### The "What" Section (Summary)
- Be explicit and concise - a few short sentences
- Describe changes at a high level, not implementation details
- Reference tickets AFTER explaining the change, not instead of

### The "Why" Section (Motivation)
- Articulate the business or engineering goal
- Explain the problem being solved
- The "why" is often more important than the "what"

### The "How" Section (Changes)
- Highlight significant design decisions
- Explain non-obvious implementation choices
- Help reviewers understand the approach

### Testing Section
- Document how the code was tested
- Include edge cases not covered and associated risks
- Provide steps for reviewers to verify

### Visual Evidence
- Screenshots for UI changes (before/after)
- CLI output for infrastructure changes
- Use collapsible sections for large outputs

## Commit Analysis Process

To generate a PR description from commits:

1. **Gather commit information**
   ```bash
   git log origin/develop..HEAD --oneline
   git diff origin/develop...HEAD --stat
   ```

2. **Analyze the changes**
   - Identify the primary type (feat, fix, refactor, etc.)
   - Determine the scope (module, feature area)
   - List all files changed and categorize by purpose

3. **Synthesize the summary**
   - Combine related commits into coherent narrative
   - Focus on the outcome, not the journey
   - Highlight the most significant changes

4. **Determine testing approach**
   - Check if tests were added/modified
   - Note any test commands that should be run
   - Flag areas needing manual verification

## Output Quality Checklist

Before finalizing a PR description, verify:

- [ ] Title follows conventional commits format
- [ ] Summary is 2-3 sentences, not a wall of text
- [ ] Motivation explains the "why", not just "what"
- [ ] Changes are organized and scannable (bullet points)
- [ ] Testing section is actionable
- [ ] No implementation details that belong in code comments
- [ ] Links to related issues are included
- [ ] Breaking changes are clearly called out

## Anti-Patterns to Avoid

- Generic titles like "Update code" or "Fix bug"
- Descriptions that just reference a ticket with no context
- Overly verbose descriptions (keep it conversational)
- Missing the "why" - jumping straight to "what"
- No testing information
- Burying breaking changes in the middle of text

## Adapting to PR Size

**Small PRs (1-3 files, simple fix):**
- Shorter summary (1-2 sentences)
- May skip "How" section
- Simple testing note

**Medium PRs (feature or refactor):**
- Full template
- Clear organization by area
- Comprehensive testing section

**Large PRs (major feature, architecture change):**
- Consider breaking into smaller PRs
- Detailed "How" section with design decisions
- May include architecture diagrams
- Highlight areas needing careful review
