---
name: techdebt
description: Find and fix duplicated or overcomplicated code
argument-hint: "[file, directory, or leave blank for recent changes]"
---

Analyze $ARGUMENTS for technical debt. Focus on two things only:

## 1. Duplicated Code
- Near-identical functions or blocks (3+ lines repeated)
- Copy-pasted logic with minor variations
- Similar patterns that could share a helper

**Fix by:** Extracting shared logic into well-named functions. Don't over-abstract—if it's only used twice, duplication might be fine.

## 2. Overcomplicated Code
- Functions longer than ~30 lines
- Deeply nested conditionals (3+ levels)
- Clever one-liners that are hard to read
- God functions doing too many things

**Fix by:** Breaking into smaller functions with clear names. Prefer boring, obvious code over clever code.

## Process
1. Scan the target (or git diff if no target given)
2. List what you find: `[DUP]` or `[COMPLEX]` with file:line
3. Ask before fixing, or fix all if user says "fix"
4. Make minimal changes—don't refactor unrelated code

## Don't
- Add abstractions for single-use code
- Create utils files for one helper
- Change working code just because it's "not ideal"
