---
name: code-review-guidelines
description: When asynchronously reviewing peer code before merging into the main branch.
version: 2.0.0
category: code-quality
tags: [code-quality, review, team]
skill_type: review
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1600
dangerous: false
requires_review: false
security_level: safe
dependencies: []
triggers: [code review, pr review, pull request, merge request]
permissions:
  filesystem: { read: true, write: false }
  network: { outbound: false }
  shell: { execute: false }
input_requirements: [pull request code changes, test coverage, architecture context]
output_contract: [constructive feedback, clear blockers vs suggestions, documented concerns]
failure_conditions: [personality-driven feedback, no context provided, blocking on style]
last_updated: 2026-05-15
---

# Code Review Guidelines

## Purpose
Code review catches bugs, ensures maintainability, and builds team knowledge. This skill provides a structured, objective, empathetic framework for reviewing code without causing friction. The goal is to improve the codebase while growing the team.

## When to use
- Evaluating a Pull Request or Merge Request
- Providing constructive feedback to peers
- Ensuring code quality and architectural standards are met
- Building new team members' skills through feedback

## When NOT to use
- Nitpicking personal coding style (use linters/formatters)
- Blocking on subjective preferences
- Reviewing without understanding context

## Inputs required
- Pull request with code changes
- PR description explaining the why
- Linked ticket with context
- Test coverage (unit/integration tests)

## Workflow
1. **Understand the Goal**: Read the PR description and linked ticket FIRST. Understand WHY the change exists before reading code.
2. **Review Architecture**: Check structural integrity and design. Does it fit the codebase? Are new dependencies justified? Is it the right abstraction level?
3. **Review Logic**: Check for correct error handling, edge cases, off-by-one errors, and security implications.
4. **Check Tests**: Verify new logic is covered by unit/integration tests that test actual behavior (not just code coverage).
5. **Consider Performance**: Check for obvious performance issues (N+1 queries, memory leaks, synchronous blocking in async code).
6. **Provide Feedback**: Leave comments that explain the WHY. Differentiate between blocking requests and suggestions (use "Nit:" or "Note:").
7. **Be Constructive**: Phrase feedback as questions when possible ("Have you considered...?"). Assume positive intent.

## Rules
- MUST assume positive intent; critique the code, not the author
- MUST automate style and formatting checks via Linters/Formatters (do NOT argue over spacing in PR)
- MUST approve immediately if code improves the codebase, even if not perfect
- MUST provide context and links when referring to standards or patterns
- MUST distinguish between blocking requests and optional suggestions
- MUST NOT block on personal coding style preferences
- MUST NOT require unrelated changes (keep scope focused)

## Anti-patterns
- **Gatekeeping**: Blocking PRs over personal style preferences or "I would have done it differently"
- **Rubber Stamping**: Approving large PRs without reading or thinking
- **Scope Creep**: Asking the author to fix unrelated legacy code nearby
- **Vague Comments**: "This is bad" or "Improve this" without explanation
- **Late Requests**: Requesting major architectural changes after code is already implemented
- **Tone Issues**: Comments that feel dismissive or condescending

## Failure conditions
- PR blocked without clear explanation
- Security or correctness issue missed
- No tests for new logic
- Feedback based on personal preference, not code quality
- Author feels disrespected or attacked

## Validation checklist
- [ ] PR description explains the why (not just what)
- [ ] Tests cover new logic
- [ ] No obvious performance issues
- [ ] Error handling is correct
- [ ] Edge cases are considered
- [ ] Security implications reviewed (if applicable)
- [ ] Code follows established patterns in the codebase
- [ ] Dependencies are justified
- [ ] Comments explain complex logic
- [ ] No scope creep (focused on this change)

## Output format
- **Feedback structure**: Problem + context + suggestion
- **Tone**: Constructive, curious, respectful
- **Clarity**: Blocking requests vs. optional suggestions clearly marked
- **Actionability**: Comments are specific and actionable
- **Decision**: Clear approval, changes requested, or comment

## Security considerations
- Security issues MUST be flagged as blocking
- SQL injection, XSS, authentication bypasses MUST be caught
- Secrets/credentials MUST NEVER be committed (catch before merge)
- Permission checks MUST be enforced
- Data exposure MUST be reviewed

## Agent execution notes
- Agent MAY: Leave constructive feedback, ask clarifying questions, suggest improvements
- Agent MUST NEVER: Block on style/preference, be dismissive, miss security issues, approve without reading
- Agent MUST ASK: When context is missing, when architectural impact is unclear
- Agent MUST VALIDATE: Tests are present, no security holes, code improves codebase

## Example

**❌ Anti-pattern (Vague, dismissive, scope creep):**
```
"This code is bad"
"Why are you doing it this way?"
"Also, can you fix the bug in the file next to this?"
"Blocked - needs improvement"
"LGTM" (without reading)
```

**✅ Correct pattern (Constructive, specific, respectful):**
```
✅ Good catch on the edge case - this prevents the race condition we had in production.

💭 Question: In the validateEmail function, what happens if the email service is down?
   Have you considered adding a timeout or fallback behavior?

🔒 Security: Double-check that user input is sanitized before the database query.

📝 Nit: This comment could be clearer - what does "process the thing" mean?

✅ The test coverage looks good. I especially like the edge case tests.

🚀 Approved! This is a clear improvement to the codebase. Nice work.
```
