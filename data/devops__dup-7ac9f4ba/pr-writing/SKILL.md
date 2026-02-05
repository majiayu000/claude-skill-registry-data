---
name: pr-writing
description: Best practices for writing clear, effective pull request descriptions. Use when creating PRs to ensure they communicate changes effectively to reviewers.
---

# PR Writing Skill

Guidelines for writing pull request descriptions that help reviewers understand and approve changes quickly.

## PR Title Format

```
#<issue-number> <type>: <concise description>
```

Always prefix the PR title with the GitHub issue number to enable easy cross-referencing.

### Types
| Type | Use For |
|------|---------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `chore` | Build, tooling, dependencies |
| `perf` | Performance improvement |
| `style` | Formatting, whitespace (no logic change) |

### Good Titles
```
#42 feat: Add user registration endpoint
#187 fix: Prevent duplicate form submissions
#23 refactor: Extract authentication logic into service
#91 docs: Add API documentation for user endpoints
```

### Bad Titles
```
Update code                    # Too vague, no issue number
Fixed the bug                  # Which bug? No issue number
WIP                           # Not ready for review
feat: Add login               # Missing issue number prefix
```

## PR Body Structure

```markdown
## Summary
[1-3 sentences explaining WHAT changed and WHY]

Closes #<issue-number>

## Changes
- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI changes)
[Before/after screenshots or GIFs]

## Notes for Reviewers
[Optional: Areas to focus on, known limitations, questions]
```

## Writing the Summary

### Focus on WHY, not just WHAT

**Bad:**
> Added a new function called validateEmail and updated the user model.

**Good:**
> Adds email validation to prevent invalid emails from being stored, which was causing delivery failures in the notification system.

### Be Specific About Impact

**Bad:**
> Fixed authentication bug.

**Good:**
> Fixes session timeout not being respected when "Remember Me" is checked, which was causing users to be logged out after 30 minutes regardless of their preference.

### Keep It Scannable

Reviewers often skim. Front-load the important information:

**Bad:**
> After investigating the issue that was reported last week about the dashboard loading slowly, I discovered that we were making redundant API calls. This PR addresses that by implementing caching.

**Good:**
> Reduces dashboard load time by 60% by caching API responses. The redundant calls were causing 3-second delays on each page load.

## Describing Changes

### Be Specific and Organized

Group related changes:

```markdown
## Changes

### API
- Add `POST /api/users/register` endpoint
- Add request validation middleware
- Add rate limiting (10 requests/minute)

### Database
- Add `email_verified` column to users table
- Add index on `email` column

### Tests
- Add unit tests for registration validation
- Add integration tests for registration flow
```

### Explain Non-Obvious Changes

```markdown
## Changes
- Increase connection pool size from 10 to 25
  - Load testing showed connection exhaustion under peak traffic
- Add retry logic to external API calls
  - The payment provider has occasional 503s that resolve on retry
```

## Linking to Issues

Always link the related issue:

```markdown
Closes #123
```

Or for partial work:

```markdown
Related to #123
Part of #123
```

## Highlighting Review Focus

Help reviewers prioritize their attention:

```markdown
## Notes for Reviewers

**Please focus on:**
- The caching invalidation logic in `src/cache/manager.ts` - I'm unsure if this handles all edge cases
- The error handling in the new endpoint

**You can skim:**
- The test files follow existing patterns
- The migration is straightforward
```

## Screenshots and Visuals

For UI changes, always include:

```markdown
## Screenshots

### Before
[screenshot]

### After
[screenshot]
```

For complex flows, use GIFs or numbered screenshots:

```markdown
## User Flow

1. User clicks "Register"
   [screenshot 1]

2. Validation errors shown inline
   [screenshot 2]

3. Success state with redirect
   [screenshot 3]
```

## Breaking Changes

Clearly call out breaking changes:

```markdown
## ⚠️ Breaking Changes

- `getUserById()` now returns `null` instead of throwing when user not found
- The `/api/v1/users` endpoint is deprecated, use `/api/v2/users`

### Migration Guide
1. Update all `try/catch` blocks around `getUserById()` to null checks
2. Update API clients to use v2 endpoint
```

## Draft PRs

Use draft PRs for:
- Work in progress needing early feedback
- Architectural decisions to discuss
- Proof of concepts

```markdown
## 🚧 Draft PR

This is a draft to get early feedback on the approach.

**Questions:**
1. Should we use Redis or in-memory caching?
2. Is this the right place for this logic?

**Not yet complete:**
- [ ] Error handling
- [ ] Tests
- [ ] Documentation
```

## Checklist Before Submitting

Before marking ready for review:

- [ ] Title follows `#<issue> type: description` format
- [ ] Summary explains what AND why
- [ ] Issue is linked with `Closes #X`
- [ ] Changes are listed specifically
- [ ] Tests are included and passing
- [ ] Screenshots added for UI changes
- [ ] Breaking changes are highlighted
- [ ] Self-reviewed the diff for obvious issues
- [ ] Branch is synced with main (no merge conflicts)

## PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| Small | < 100 | < 30 min | Ideal |
| Medium | 100-300 | 30-60 min | Acceptable |
| Large | 300-500 | 1-2 hours | Consider splitting |
| XL | > 500 | Hours | Split if possible |

If a PR is large, explain why:
```markdown
## Note on PR Size

This PR is larger than usual because it includes a database migration
that requires updating all affected queries atomically. Splitting would
leave the codebase in a broken state.
```
