---
name: github-markdown-posting
description: Write issue comments, PR comments, PR bodies, and wiki content as markdown that renders cleanly in the GitHub interface. Use when agents post or update visible GitHub content so formatting stays readable and consistent for human reviewers.
---

# GitHub markdown posting

## Rule
All issue comments, PR comments, PR bodies, and wiki posts should be written as GitHub-flavored markdown that renders cleanly in the GitHub interface.

## Goals
- keep posts readable in GitHub's renderer
- use headings, bullets, quotes, code fences, and emphasis appropriately
- avoid malformed markdown or formatting that renders poorly
- make structured updates easy for human reviewers to scan

## Apply especially to
- issue clarifications
- PR descriptions and updates
- QA review comments
- assumption logs
- wiki pages and wiki updates

## Guidance
- prefer clear headings and bullet lists for structured updates
- use fenced code blocks for commands, logs, or code snippets
- use blockquotes consistently for agent identity headers
- avoid raw plaintext dumps when markdown structure would help readability
