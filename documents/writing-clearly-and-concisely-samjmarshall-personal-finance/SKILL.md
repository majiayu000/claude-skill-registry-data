---
name: writing-clearly-and-concisely
description: Apply writing rules to ANY prose humans will read — documentation, commit messages, error messages, explanations, reports, or UI text. Makes your writing clearer, stronger, and more professional.
model: sonnet
effort: high
---

# Writing Clearly and Concisely

**Announce at start:** "I'm using the writing-clearly-and-concisely skill to improve this writing."

## Overview

William Strunk Jr.'s *The Elements of Style* (1918) teaches clear, concise writing.

**Core Principle**: ALL writing for humans is prose. Apply these rules to code comments, documentation, commit messages, error messages, UI text, and any explanation.

**WARNING:** `elements-of-style.md` consumes ~12,000 tokens. Read it only when writing or editing prose.

## When to Use This Skill

**Use this skill for ALL writing humans will read:**

### Code & Development
- Commit messages and PR descriptions
- Code comments explaining logic
- API documentation
- README files and guides
- Error messages and logging

### Technical Writing
- Architecture docs
- Design proposals
- Technical specifications
- Internal documentation
- External user guides

### Communication
- Reports and summaries
- Explanations to teammates
- UI copy and help text
- Email and messages
- Any written explanation

**If a human will read it, it's prose. Apply these rules.**

## Common Rationalizations (Don't Accept These)

| Excuse | Reality |
|--------|---------|
| "Write quickly" → skip editing | Clarity ALWAYS worth the time |
| "Just internal docs" | Internal docs need clarity MORE, not less |
| "Technical writing ≠ prose" | ALL writing for humans is prose |
| "Not formal prose" | Formality ≠ clarity; informal needs clarity too |
| "Clarity isn't critical here" | This is NEVER true. Clarity is always critical. |
| "Good enough for now" | Poor writing wastes readers' time forever |
| "Too simple to need editing" | Simple writing often has the most unnecessary words |

**When you hear these rationalizations, STOP and apply the rules anyway.**

## Limited Context Strategy

When context is tight:
1. Write your draft using judgment
2. Dispatch a subagent with your draft and `elements-of-style.md`
3. Have the subagent copyedit and return the revision

## All Rules (Quick Reference)

### Elementary Rules of Usage (Grammar/Punctuation)
1. Form possessive singular by adding 's
2. Use comma after each term in series except last
3. Enclose parenthetic expressions between commas
4. Comma before conjunction introducing co-ordinate clause
5. Don't join independent clauses by comma
6. Don't break sentences in two
7. Participial phrase at beginning refers to grammatical subject

### Elementary Principles of Composition
8. One paragraph per topic
9. Begin paragraph with topic sentence
10. **Use active voice**
11. **Put statements in positive form**
12. **Use definite, specific, concrete language**
13. **Omit needless words**
14. Avoid succession of loose sentences
15. Express co-ordinate ideas in similar form
16. **Keep related words together**
17. Keep to one tense in summaries
18. **Place emphatic words at end of sentence**

### Section V: Words and Expressions Commonly Misused
Alphabetical reference for usage questions

## Most Critical Rules (Apply These First)

### Rule 10: Use Active Voice

❌ "The bug was fixed by the team"
✅ "The team fixed the bug"

❌ "Errors are handled by the system"
✅ "The system handles errors"

### Rule 11: Put Statements in Positive Form

❌ "The feature is not very necessary"
✅ "The feature is unnecessary"

❌ "Did not remember"
✅ "Forgot"

### Rule 13: Omit Needless Words

❌ "In my opinion, I think that..."
✅ (just make the statement)

❌ "at this point in time"
✅ "now"

❌ "allows users to be able to"
✅ "lets users"

### Rule 12: Use Definite, Specific, Concrete Language

❌ "handled appropriately"
✅ "logged to stderr"

❌ "The system processes data"
✅ "The parser extracts JSON fields"

## Systematic Application Process

1. **Write** - Get ideas down first
2. **Review for passive voice** - Convert to active (Rule 10)
3. **Review for negative forms** - Convert to positive (Rule 11)
4. **Review for vague language** - Make specific (Rule 12)
5. **Cut ruthlessly** - Remove needless words (Rule 13)
6. **Check word order** - Keep related words together (Rule 16)

**Apply ALL rules systematically. Don't stop after "good enough."**

## Under Pressure

Time pressure or "quick docs" requests don't justify skipping these rules.

**Why:**
- Bad writing wastes EVERY reader's time
- Editing takes seconds; reading bad docs wastes minutes per person
- Multiply by number of readers → clarity is always worth it

**When told "write quickly":**
1. Write the draft
2. Apply rules (takes 30 seconds)
3. Deliver clear result

Don't ask permission to edit. Just do it.

## For Different Contexts

### Commit Messages
- Subject: Omit needless words, active voice, specific
- Body: One paragraph per topic, active voice, concrete language
- Example: ❌ "Added feature that allows users to be able to search"
- Example: ✅ "feat: add history search"

### Error Messages
- Active voice ("File exceeds limit" not "limit was exceeded")
- Specific ("File exceeds 10MB limit" not "file is too large")
- Positive form when possible
- Omit needless words

### Documentation
- Use active voice throughout
- Be specific: actual commands, actual values, actual behavior
- One topic per paragraph
- Cut relentlessly

### Code Comments
- Explain WHY, not WHAT (code shows what)
- Be specific about intent
- Active voice: "Handles edge case" not "Edge case is handled"
- Omit needless words: "// Cache for performance" not "// This variable stores a cache for performance reasons"

## Bottom Line

**Writing for humans? Read `elements-of-style.md` and apply the rules.**

**Low on tokens? Dispatch a subagent to copyedit with the guide.**

**Under pressure? Apply rules anyway. Clarity is always worth 30 seconds.**

**Don't accept rationalizations. All writing for humans deserves clarity.**
