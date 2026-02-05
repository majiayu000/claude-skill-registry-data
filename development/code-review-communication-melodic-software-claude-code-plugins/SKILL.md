---
name: code-review-communication
description: Frameworks for giving and receiving code review feedback effectively. Use for PR comments, review strategies, handling disagreements, and balancing thoroughness with kindness.
allowed-tools: Read, Glob, Grep
---

# Code Review Communication

This skill provides frameworks for effective code review communication - both giving feedback that lands well and receiving feedback without defensiveness.

## When to Use This Skill

- Writing a code review comment and want it to be clear and constructive
- Receiving feedback that feels harsh and need perspective
- Want to distinguish between blocking issues and minor suggestions
- Need to communicate code quality concerns without damaging relationships
- Preparing to review a junior developer's first PR

## Core Frameworks

### Conventional Comments

A labeling system that makes the intent of each comment crystal clear.

**Format:** `[label] (decoration): explanation`

**Labels:**

| Label | Meaning | Action Required |
| ----- | ------- | --------------- |
| `praise` | Highlight good work | None - encouragement |
| `nitpick` | Minor style/preference issue | Optional |
| `suggestion` | Improvement idea | Consider but not required |
| `issue` | Must be addressed | Required before merge |
| `question` | Need clarification | Response required |
| `thought` | Sharing perspective | None - FYI only |

**Decorations:**

- `(non-blocking)` - Explicitly optional
- `(blocking)` - Must be resolved
- `(if-minor)` - Only if the fix is trivial

**Examples:**

```text
praise: This error handling is really thorough - I like how you covered the edge cases.

nitpick (non-blocking): Consider using a more descriptive variable name than `x`.

suggestion: You could use `Object.entries()` here for cleaner iteration.

issue (blocking): This SQL query is vulnerable to injection. Use parameterized queries.

question: What's the expected behavior if the user cancels mid-operation?

thought: I've seen this pattern cause issues with concurrent requests in the past.
```

**Full reference:** `references/conventional-comments.md`

### Summary-Analysis-Suggestion Method

For larger reviews or when multiple comments are needed:

1. **Summary** - Start with what works (genuine positives)
2. **Analysis** - Identify specific areas needing attention
3. **Suggestion** - End with actionable recommendations

This prevents the "wall of criticism" effect that makes authors defensive.

### Separating Code from Coder

The most important principle: **criticize code, not people**.

| Instead of... | Say... |
| ------------- | ------ |
| "You wrote this wrong" | "This function could be simplified" |
| "You didn't think about X" | "There's an edge case here around X" |
| "Why did you do it this way?" | "What's the reasoning behind this approach?" |
| "You should know better" | "This is a common gotcha - here's the pattern" |

Use collaborative "we" language:

- "We should add a test for this"
- "How should we handle the null case?"
- "Let's think about the performance implications"

### Blocking vs Non-Blocking

**Blocking issues (must fix):**

- Security vulnerabilities
- Bugs that will cause production issues
- Breaking changes to public APIs
- Missing required tests for critical paths

**Non-blocking issues (nice to have):**

- Style preferences
- Alternative implementations
- Minor optimizations
- Documentation improvements

**Rule of thumb:** If you'd be comfortable if the author ignored this comment, it's non-blocking.

## Receiving Feedback

Receiving code review feedback well is equally important. See `references/receiving-feedback.md` for:

- Assuming good intent
- Separating ego from code
- Asking clarifying questions
- Handling disagreements professionally
- When to take discussions offline

## Related Resources

- `references/conventional-comments.md` - Full label taxonomy with examples
- `references/receiving-feedback.md` - Guide to receiving feedback gracefully
- `feedback-conversations` skill - For broader feedback (not just code)
- `/soft-skills:review-comment` command - Generate a well-structured review comment

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
