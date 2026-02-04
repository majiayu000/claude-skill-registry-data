---
name: pr-author-reviewer
description: Raise PR quality with templates, checklists, and security reviews
version: 1.0.0
tags: [pr, code-review, quality, security]
---

# PR Author and Reviewer Skill

## Purpose
Ensure consistent, high-quality pull requests with templates and automated checks.

## Process
1. Load PR template from references/pr_template.md
2. Run security checklist from references/security_review.md
3. Lint commit messages
4. Generate PR description
5. Log decision rationales to memory

## Scripts
- `lint_commit_msgs.py`: Validate commit message format
- `generate_pr.py`: Create PR from template

## Output
- Formatted PR description
- Security checklist results
- Commit message validation

*PR Author and Reviewer v1.0.0*
