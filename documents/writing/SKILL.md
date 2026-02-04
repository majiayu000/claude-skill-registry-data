---
name: writing
description: Clear, concise writing standards for documentation, comments, commit messages, and technical communication. Use when writing README files, documentation, PR descriptions, code comments, or any technical writing. Focuses on clarity, brevity, and active voice.
---

# Writing Guidelines

Standards for all written content: documentation, comments, commit messages, technical writing.

## Core Principles

### Be Concise
- Every word must earn its place
- Delete redundant words
- Cut the clutter
- Short sentences convey ideas clearly

### Active Voice
Prefer active voice over passive:
- ✅ "We fixed the bug"
- ❌ "The bug was fixed by us"

### One Idea Per Sentence
- Write short sentences
- Each sentence expresses one clear idea
- Complex ideas get multiple sentences

### Lead with Results
- Put the outcome first
- Make conclusions obvious
- Return early in explanations
- Don't bury the lead

## Naming in Writing

### Descriptive Names
- Code is reference, history, and functionality
- Names must be readable as a journal
- Be specific and concrete

### Avoid Vague Terms
Replace generic terms with specific ones:
- ❌ `data`, `item`, `list`, `component`
- ✅ `userPayment`, `users`, `paymentList`

### Remove Redundancy
- ✅ `users` (not `userList`)
- ✅ `payment` (not `userPaymentData`)

## Documentation Standards

### README Files
Structure:
1. What it does (one sentence)
2. Why it exists (one paragraph)
3. How to use it (clear steps)
4. Examples (if needed)

Keep it under 200 lines. Link to additional docs if needed.

### Code Comments

Comments are unnecessary 98% of the time:
- ❌ `// Loop through users`
- ✅ Extract to function: `filterActiveUsers()`

When comments are needed:
- Explain *why*, not *what*
- Explain business context or constraints
- Document surprising behavior or gotchas

### Commit Messages

Format:
```
<verb> <what> [<context>]
```

Examples:
- ✅ `Add user authentication`
- ✅ `Fix payment validation error`
- ✅ `Refactor database queries for performance`
- ❌ `Fixed stuff`
- ❌ `Updates`
- ❌ `Claude Code: Added feature`

Rules:
- Use imperative mood ("Add" not "Added")
- Be specific about what changed
- Include context if not obvious
- Never include "Claude Code" in messages

### PR Descriptions

Structure:
```
## What
[One sentence describing the change]

## Why
[One paragraph explaining motivation]

## Testing
[How this was tested]
```

Keep it scannable. Add details only if necessary.

## Technical Writing

### Headers
- Short, descriptive, sentence-case
- Make content scannable
- Use hierarchy properly (H1 → H2 → H3)

### Lists
- Use for related items only
- Keep items parallel in structure
- Prefer sentences in prose when possible

### Examples
- Show, don't just tell
- Use real code, not pseudocode
- Keep examples minimal and focused

## Writing Anti-Patterns

### Avoid
- Redundant words: "in order to" → "to"
- Weak verbs: "is able to" → "can"
- Passive voice: "was fixed by" → "fixed"
- Hedging: "might", "possibly", "perhaps" (when you know)
- Jargon without explanation
- Over-explaining obvious things

### Watch For
- Long sentences (>25 words)
- Dense paragraphs (>5 sentences)
- Nested clauses
- Ambiguous pronouns

## Specific Use Cases

### Error Messages
Format: `<What happened>. <What to do>.`

Examples:
- ✅ `User not found. Check the email address.`
- ✅ `Payment failed. Retry or contact support.`
- ❌ `An error occurred.`
- ❌ `Something went wrong.`

### API Documentation
Include:
1. Purpose (one sentence)
2. Parameters (with types)
3. Return value (with type)
4. Example usage
5. Error cases (if complex)

### Function/Variable Documentation
Use JSDoc/TSDoc only when necessary:
- Public APIs
- Complex algorithms
- Non-obvious behavior

Format:
```typescript
/**
 * Retry failed requests with exponential backoff.
 * Max 3 attempts, doubles delay each time.
 */
```

## Tone

### Technical Writing
- Professional but approachable
- Clear and direct
- Avoid humor in error messages
- Be helpful, not condescending

### Documentation
- Assume intelligence, not knowledge
- Explain context, not obvious things
- Guide, don't command

## Review Checklist

Before publishing writing:
- [ ] Lead with the result/conclusion
- [ ] Every sentence has one clear idea
- [ ] Active voice used throughout
- [ ] No redundant words
- [ ] Specific terms (no vague language)
- [ ] Short sentences (<25 words)
- [ ] Clear hierarchy (if using headers)
- [ ] Examples included (if needed)
- [ ] Scannable and skimmable
