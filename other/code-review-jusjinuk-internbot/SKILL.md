---
name: code-review
description: Explain and review code. Use when code is shared in conversation or a review is requested.
---

# Code Explanation & Review

## When to use

- User pastes code in the conversation
- User asks "what does this do?", "review this", "is this correct?"
- User shares a file path or GitHub link for review

## Workflow

1. **Identify context**: language, framework, what part of a system this is
2. **Read the code carefully** before commenting — understand intent first
3. **Explain at the right level**: match the user's apparent expertise
   - For "what does this do?" — explain the high-level purpose and flow
   - For "review this" — focus on issues and improvements

## What to look for

### Correctness
- Logic errors, off-by-one, wrong comparisons
- Missing error handling for operations that can fail (I/O, network, parsing)
- Race conditions in async/concurrent code
- Incorrect types or unchecked type assertions

### Performance (only flag if impactful)
- O(n²) or worse in hot paths (loops within loops on large data)
- Repeated computation that should be cached
- Synchronous I/O blocking the event loop
- N+1 query patterns

### Security (always flag)
- SQL injection, command injection, XSS
- Hardcoded secrets or credentials
- Missing input validation at system boundaries

### Style (mention briefly, don't belabor)
- Naming that obscures intent
- Overly complex logic that could be simplified
- Dead code or unused imports

## Formatting for Slack

- Lead with a one-sentence summary: "This is a [description]. It [does X]."
- Group issues by severity — bugs first, then performance, then style
- For each issue: quote the problematic line, explain why it's wrong, show the fix
- Keep it concise — 3-5 observations is better than 15 nitpicks
- If the code is good, say so — don't manufacture issues
