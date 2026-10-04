---
name: qa
description: Use when reporting bugs, doing QA, or filing GitHub issues conversationally
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [testing, qa, bugs, github, issues]
---

# Qa

Run an interactive QA session. The user describes problems they're encountering. You clarify, explore the codebase for context, and file GitHub issues that are durable, user-focused, and use the project's domain language.

## For each issue the user raises

### 1. Listen and lightly clarify
Let the user describe the problem in their own words. Ask at most 2-3 short clarifying questions focused on:
- What they expected vs what actually happened
- Steps to reproduce (if not obvious)
- Whether it's consistent or intermittent

Do NOT over-interview. If the description is clear enough to file, move on.

### 2. Explore the codebase in the background
While talking to the user, understand the relevant area to:
- Learn the domain language used in that area
- Understand what the feature is supposed to do
- Identify the user-facing behavior boundary

### 3. Assess scope: single issue or breakdown?
Break down when the fix spans multiple independent areas or there are clearly separable concerns.

### 4. File the issue(s)
Write issues that describe the problem from the user's perspective, not implementation details.

## Common Pitfalls

- **Over-interviewing the user**: Asking too many clarifying questions wastes user time. Limit to 2-3 questions. If the description is clear enough, file the issue.
- **Including implementation details in issues**: Issues should describe user-facing behavior, not internal file paths or line numbers. Keep the focus on what is broken from the user's perspective.
- **Not breaking down compound issues**: A single report that spans multiple independent areas should be split into separate issues for parallel work.

## Code Examples

```bash
# QA Session Workflow
# 1. User reports: "The form doesn't validate on submit"
# 2. Explore the codebase to understand form handling
# 3. File a GitHub issue:

## Summary
Form validation does not trigger on submit button click

## Expected behavior
Invalid fields show error messages and red border on submit

## Actual behavior
Form submits successfully with invalid/empty data

## Steps to reproduce
1. Navigate to /settings/profile
2. Leave required field "email" empty
3. Click "Save Changes"
4. Observe: form submits without validation feedback
```

## Verification Checklist

- [ ] User described the problem in their own words
- [ ] At most 2-3 clarifying questions asked
- [ ] Codebase explored for domain context
- [ ] Compound issues broken into separate issues
- [ ] Issues filed without implementation details
