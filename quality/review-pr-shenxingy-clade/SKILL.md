---
name: review-pr
description: Review an exact PR head in isolation using trusted-base instructions and execution evidence
when_to_use: "review PR, code review pull request, PR feedback, validate candidate"
argument-hint: '[PR_NUMBER_OR_URL]'
user_invocable: true
---

# Review PR

Review one exact pull-request candidate in an isolated checkout. Resolve trusted
base instructions before executing head code, run repository-required evidence,
bind findings to base/head SHAs, and never count the author's own review as an
independent approval.
