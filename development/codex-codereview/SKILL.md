---
name: codex-codereview
description: Use for code review and quality feedback from Codex. Triggers on "codex review code", "codex code review", "have codex review this", "get codex feedback on code".
---

# Codex Code Review Skill

Comprehensive code review with Codex (gpt-5.2).

## When to Use

- Reviewing code before commit
- Getting feedback on implementation
- Checking for security issues
- Verifying best practices
- Architecture review

## Reasoning Level

**high** (thorough but efficient review)

## Execution

1. Identify code to review:
   - Specific files mentioned by user
   - Staged changes (`git diff --staged`)
   - Recent changes (`git diff`)
2. Gather context about the codebase patterns
3. Formulate a review prompt:
   ```
   Review this code thoroughly.

   Code:
   <code to review>

   Context:
   <any relevant context about patterns/conventions>

   Please review for:
   1. Bugs and logic errors
   2. Security vulnerabilities
   3. Performance issues
   4. Code quality and readability
   5. Best practices adherence
   6. Edge cases
   ```
4. Run: `codex exec -c model_reasoning_effort="high" "<prompt>"`
5. Return structured review feedback

## Response Format

```
**Codex Code Review:**

**Summary:**
[Overall assessment]

**Issues Found:**
- 🔴 Critical: [if any]
- 🟡 Warning: [if any]
- 🔵 Suggestion: [if any]

**Detailed Feedback:**
[Line-by-line or section-by-section feedback]

**Recommendations:**
[Specific improvements]

**Session ID:** [id]
```
