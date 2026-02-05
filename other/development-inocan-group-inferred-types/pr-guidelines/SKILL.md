---
name: pr-guidelines
description: Pull request best practices distilled from Graphite and GitHub guides. Use when creating pull requests in conjunction with the graphite-workflow skill to ensure they follow size guidelines, include proper context, and facilitate efficient reviews. Covers PR stacking, description templates, reviewer assignment, and team metrics.
user_invocable: true
---

# Pull Request Best Practices

## Overview

This skill provides distilled best practices for creating effective pull requests. Smaller, well-structured PRs lead to faster reviews, fewer bugs, and more efficient collaboration.

**Key insight:** Teams with ~50 line PR averages ship 40% more code than teams with 200+ line PRs.

## When to Use This Skill

Use this guidance when:
- Creating a new pull request
- Reviewing a pull request for structure and completeness
- Planning a large feature that needs to be split into multiple PRs
- Establishing team PR guidelines and metrics

## PR Size Guidelines

| Metric | Ideal | Acceptable | Flag for Review |
|--------|-------|------------|-----------------|
| Lines changed | ~50 | < 200 | > 500 |
| Files affected | 1-3 | < 10 | > 10 |
| Scope | Single task | Related changes | Multiple unrelated features |

**Keep PRs atomic** - Each PR should accomplish one clear goal and be mergeable independently.

### Break Down Tasks Early

During planning, if a feature will require hundreds of lines or touch many files, break it down:

**Example: User authentication**
- PR 1: Backend API logic
- PR 2: User interface components
- PR 3: Refactoring and test updates

Each change addresses one piece and keeps PRs digestible.

## Before Submitting

Run through this checklist:

- [ ] **Self-review**: Run through changes and trim unnecessary code
- [ ] **Build and test**: Catch obvious errors before others see them
- [ ] **Check scope**: Ensure you're only addressing one task
- [ ] **Verify size**: Under 200 lines is ideal

### Ask Yourself

- Are there unrelated changes that should be split?
- Have I kept the focus on a single task?
- Can I add explanations to help reviewers understand context?

## PR Description Template

```markdown
## Summary

<!-- Brief description of what this PR does -->

## Related Issues

<!-- Link to related issues: Fixes #123, Closes #456 -->

## Type of Change

<!-- Mark the appropriate option with an "x" -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Data addition (film, developer, or recipe entries)

## Changes Made

<!-- List the key changes in this PR -->

-
-
-

## Testing

<!-- Describe how you tested your changes -->

- [ ] I have run `bun run test` and all checks pass
- [ ] I have added tests that prove my fix/feature works
- [ ] I have tested manually in the development environment

## Checklist

- [ ] My code follows the project's code style
- [ ] I have formatted my code with `bun run format`
- [ ] I have made corresponding changes to documentation (if applicable)
- [ ] My changes generate no new warnings
- [ ] I have checked that there are no circular dependencies between packages

## Screenshots

<!-- If applicable, add screenshots to demonstrate the change -->

## Additional Notes

<!-- Any additional context or information for reviewers -->

```

### Breaking Changes

Explicitly call out:
- API changes affecting downstream consumers
- Database migrations requiring coordination
- Configuration changes
- Compatibility considerations

### Provide Context for Reviewers

- Write clear titles and descriptions
- Link to tracking issues or previous conversations
- Share the type of feedback needed (quick look vs. deeper critique)
- For multi-file PRs, guide reviewers on where to start
- Include before/after screenshots for UI changes

## PR Stacking

For large features, use stacked PRs to maintain reviewability:

```
main <- PR 1: Core infrastructure/base changes
     <- PR 2: Feature components building on base
     <- PR 3: Integration/UI changes
```

Each PR in the stack should remain independently reviewable (< 200 lines).

**Benefits:**
- Establish core infrastructure first
- Subsequent PRs build on those changes
- Parallel progress without blocking
- Easier to pinpoint and assign reviewers by domain

## Assigning Reviewers

Thoughtfully assign based on expertise:

| Change Type | Reviewer |
|-------------|----------|
| Core infrastructure | Senior engineers/DevOps |
| UI updates | UX designers + frontend engineers |
| Security changes | Security team (auth/crypto/access) |
| Domain logic | Owners of affected components |

Small PRs make precise reviewer assignments easier.

## When PRs Must Be Large

If a large PR is unavoidable:

- **Communicate early**: Notify the team a large PR is coming
- **Label it**: Use tags like `large` or `needs extended review`
- **Provide detailed breakdown**: Bullet points for each major change
- **Consider PR stacking**: Keep each PR under 200 lines while maintaining dependencies

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Feature creep - bundling unrelated changes | One task per PR, use stacking |
| Context vacuum - sparse descriptions | Use template, link to issues |
| Review bottlenecks - waiting on one person | Add multiple reviewers with domain expertise |
| Unintentional dependencies - breaking other features | Consider downstream impacts, note breaking changes |
| Knowledge silos - narrow technical review | Include diverse perspectives (UX, security, ops) |

## Automation

Let tools catch shallow issues so humans can focus on logic and architecture:

- **Linting and formatting** (run before PR)
- **Type checking**
- **Unit tests**
- **Security scans** (dependency review, code scanning)

**Commands:**

```bash
# Run verification before considering done
bun run test
```

## Team Metrics to Track

Monitor these to identify workflow bottlenecks:

- **Time to first review** - Target: < 1 business day
- **Time from publish to merge** - Identify where delays occur
- **PR size distribution** - Keep averages low
- **Bugs caught in review** - Quality signal

### Security Review Checklist

Before submitting, check for security issues:

- Review the dependency diff for vulnerable dependencies
- Check the GitHub Advisory Database for context
- Resolve failing security checks (dependency review, code scanning)
- Use GitHub Copilot Autofix for security vulnerability suggestions

## Handling Review Feedback

- **Respond to every comment** - Even if just "acknowledged"
- **Clarify feedback type needed** - Quick sanity check or thorough review?
- **Real-time collaboration** - For complex context, consider pair programming
- **Ask questions** - Frame reviews as conversations, not approvals

## Continuous Improvement

### Start Tracking the Numbers

- Monitor review turnaround time
- Track bugs caught in review
- Schedule regular retrospectives
- Survey developers on what works and what's frustrating

### Encourage Controlled Experimentation

- Try variations in review cadence
- Experiment with PR communication modes
- Test new tooling integrations
- Start small, then roll out widely

### Promote Knowledge Sharing

- Make time for informal code reviews
- Run training workshops on PR best practices
- Celebrate proactive collaboration publicly
