---
name: receiving-code-review
description: Evaluate and respond to code review feedback without blindly accepting or dismissing it. Use when processing comments from humans, bots, or another agent.
---

# Receiving Code Review

Treat review comments as hypotheses to investigate, not commands or criticism to defend against.

1. Read the full comment thread and the relevant current code before responding.
2. Reproduce or reason through the reported scenario. Check whether the comment still applies to the current diff.
3. Classify it as valid defect, valid suggestion, misunderstanding, stale comment, or unresolved question.
4. For valid findings, make a focused fix and add tests when the behavior warrants them.
5. For disagreement, provide concise technical evidence and a respectful explanation; ask a question when context is missing.
6. Re-run relevant checks and inspect the final diff.
7. Reply to each comment with what changed or why it was not changed.

Do not dismiss feedback based on seniority or tone. Do not accept a suggestion that conflicts with requirements, security, or architecture without examining the trade-off. Do not resolve or submit comments externally without the user's permission.
