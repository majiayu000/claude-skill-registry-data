---
name: communication-guidelines
description: Use when starting work - guidelines for asking questions and commit policies
---

# Communication Guidelines

Use this skill at the start of work to determine when to ask questions and follow commit policies.

## Checklist

### When to Ask Clarifying Questions
Ask questions for:
- [ ] **Ambiguous requests** - Multiple valid interpretations exist
  - Example: "optimize this" → Ask: speed, memory, or readability?
  - Example: "improve the API" → Ask: performance, interface design, or error handling?
- [ ] **Complex features** - Significant design decisions required
  - Example: "add authentication" → Ask: JWT, OAuth, session-based? Token duration?
  - Example: "add caching" → Ask: in-memory, Redis, file-based? TTL duration?
- [ ] **Missing context** - Information needed to implement correctly
  - Example: "fix the bug" → Ask: which bug? What's the expected behavior?

### When to Skip Questions
Proceed directly for:
- [ ] **Trivial commands** - Clear, single-step operations
  - Examples: "run tests", "format code", "check types"
- [ ] **Well-defined tasks** - All necessary information provided
  - Examples: "add logging to generate_image()", "fix type error in service.py:42"
- [ ] **Standard operations** - Following established patterns
  - Examples: "create a test for this function", "add error handling here"

### Commit and Amend Policies
- [ ] **Never create commits without explicit permission**
  - Wait for user to say "commit this" or "create a commit"
  - Don't assume completion means commit
- [ ] **Never amend commits without explicit permission**
  - Don't use `git commit --amend` unless user requests it
  - Respect commit history
- [ ] **Ask before creating pull requests**
  - Don't automatically create PRs after completing work
  - Wait for user to request PR creation

### Decision-Making Framework

**Before asking a question, check:**
1. Is this information necessary to proceed? (If no → proceed with reasonable defaults)
2. Are there multiple valid approaches with different trade-offs? (If yes → ask)
3. Could my assumption cause significant rework if wrong? (If yes → ask)
4. Is this a trivial/standard operation? (If yes → proceed)

**Examples:**

❌ **Don't ask:** "Should I use tabs or spaces?" (Project has ruff.toml configuration)
✅ **Do ask:** "Should I use JWT tokens or session cookies for authentication?" (Major architectural decision)

❌ **Don't ask:** "Should I run the tests?" (Standard verification step)
✅ **Do ask:** "Should I mock the GPU or use a real device for this test?" (Testing strategy decision)

### Communication Style
- [ ] Be concise and direct
- [ ] Focus on technical clarity over politeness
- [ ] Provide options when asking questions
- [ ] Explain trade-offs when recommending approaches
