---
name: code-review
description: How to review code; a pull request, feature branch, local changes etc.
---

When asked to review code, whether a PR on GitHub or some local changes, provide feedback on:

- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security concerns
- Test coverage

Use the repository's CLAUDE.md for guidance on style and conventions.
For comments, changelog entries, and PR bodies, review against the standard in
[`.claude/skills/prose-pass/SKILL.md`](../prose-pass/SKILL.md) — read it as
criteria; do not invoke it, since it edits files and a review may have nothing
checked out.
If you encounter terms that should be added to the glossary, invoke the glossary
skill using: Skill tool with skill="glossary"
Be constructive and helpful in your feedback.
