---
name: extract-learnings
description: Use after completing a session to identify genuine learnings from mistakes, corrections, or rework - focuses only on patterns that were actually wrong, not things that worked correctly the first time
---

# Extract Learnings from Session

## Overview

Extract learnings identifies **actual mistakes** from completed work: where you were corrected, where you had to redo something, or where your initial approach was wrong.

**Core principle:** Extract only NEW learnings. Ignore things you got right. Focus on patterns that need to change.

## The Extraction Pattern

```
WHEN extracting learnings from a session:

1. IDENTIFY: What did you have to redo, fix, or change?
2. DISTINGUISH: Was this a correction or just normal iteration?
3. VERIFY: Did you make the same mistake multiple times?
4. EXTRACT: What's the underlying pattern to avoid?
5. DOCUMENT: State the learning as a future directive
```

## What Qualifies as a Learning

### ✅ Valid Learnings (Extract These)

Learnings come from **corrections** and **rework**:

- **Human corrected you**: "No, that's wrong - it should be X"
- **You misunderstood requirements**: Had to rewrite after clarification
- **Your code broke something**: Had to fix failures or regressions
- **You made the same mistake repeatedly**: Same error pattern appeared multiple times
- **You violated existing patterns**: Went against established conventions after being told
- **You over-engineered**: Added complexity that was explicitly rejected

### ❌ Not Valid Learnings (Skip These)

These are **normal work**, not mistakes:

- **Normal iteration**: "Let's also add Y" after X was done correctly
- **Requirements that evolved**: User changed their mind about what they wanted
- **Things you got right first time**: No correction needed = no learning needed
- **Expected clarifications**: Asking questions before implementing
- **Code that worked**: Even if later modified for new features
- **Design discussions**: Exploring options isn't the same as being wrong

## The Critical Question

For each potential learning, ask:

**"Was I corrected, or was this just normal work?"**

- Corrected → Extract learning
- Normal work → Skip it

## Extraction Process

### Step 1: Review the Session

Look through the conversation for:
- Direct corrections from human ("No, that's wrong...")
- Code you had to rewrite (not extend, but replace)
- Tests that failed due to your mistakes
- Patterns you repeated after being told not to

### Step 2: Identify the Pattern

For each correction, identify:
- What was wrong?
- Why was it wrong?
- What's the underlying pattern?

**Example:**
```
Correction: "Don't add gratitude - the CLAUDE.md explicitly says no thanks"
Pattern: Violated explicit written instructions
Learning: Always check CLAUDE.md before defaulting to conversational niceties
```

### Step 3: State as Directive

Express learnings as **future-facing rules**:

```
✅ "Check CLAUDE.md before using conversational phrases - it prohibits gratitude"
✅ "Verify API parameters against docs before implementation - don't assume"
✅ "Test edge cases before marking complete - caught multiple off-by-one errors"

❌ "The project uses React" (you knew this, not a learning)
❌ "User wanted dark mode" (requirement, not mistake)
❌ "Implemented authentication" (work done, not lesson learned)
```

## Common False Learnings to Avoid

### "Learned about the codebase structure"
**Why it's false:** Understanding codebase isn't a mistake correction
**When it IS a learning:** "Assumed files were in /lib but they're in /src - check actual structure first"

### "Learned the user prefers X style"
**Why it's false:** Learning preferences through normal discussion isn't a correction
**When it IS a learning:** "Kept using Y style after being told to use X - read style guide first"

### "Learned to ask clarifying questions"
**Why it's false:** Asking questions is normal, good practice
**When it IS a learning:** "Made assumptions about ambiguous requirement and had to rewrite - ask first when unclear"

### "Learned about new feature X"
**Why it's false:** Implementing new features is normal work
**When it IS a learning:** "Reimplemented X manually when library already provided it - check deps first"

## Template for Valid Learnings

```markdown
## Learning: [Brief title]

**What happened:** [Specific correction or rework]
**Why it was wrong:** [Root cause]
**Pattern to avoid:** [General principle]
**Future action:** [Specific directive]

**Example from session:**
[Actual instance where this occurred]
```

## Real Examples

### Valid Learning

```markdown
## Learning: Check CLAUDE.md before conversational defaults

**What happened:** Added "Thanks for the feedback" after code review; was corrected that CLAUDE.md explicitly prohibits gratitude expressions
**Why it was wrong:** Violated documented instructions in favor of conversational habits
**Pattern to avoid:** Defaulting to conversational niceties without checking project guidelines
**Future action:** Read CLAUDE.md before responding to feedback - verify communication style requirements

**Example from session:**
- Response: "Thanks for catching that!"
- Correction: "Don't say thanks - CLAUDE.md line 142"
- Had to edit response to remove gratitude
```

### Invalid "Learning" (Normal Work)

```markdown
❌ Learning: Project uses TypeScript

This is not a learning - this is basic context understanding.
No correction occurred. TypeScript was used correctly throughout.
```

### Valid Learning (Repeated Mistake)

```markdown
## Learning: Verify file paths exist before using Edit tool

**What happened:** Used Edit tool three times on files that didn't exist; each time errored and had to use Write instead
**Why it was wrong:** Edit requires file to exist first; should have checked with Read or List
**Pattern to avoid:** Assuming file exists without verification
**Future action:** Always Read file before using Edit, or verify with List if unsure

**Example from session:**
- Attempted: Edit on config/settings.json (doesn't exist)
- Error: "File not found"
- Had to: Write config/settings.json instead
- Repeated this pattern on 3 different files
```

## Anti-Pattern: The "Everything is a Learning" Trap

**Bad extraction:**
```
- Learned about the project structure ❌
- Learned user wants dark mode ❌
- Learned to implement authentication ❌
- Learned React hooks ❌
- Learned the API endpoints ❌
```

**Why this is bad:** None of these represent corrections. This is just documenting work done.

**Good extraction:**
```
- Assumed API was REST without checking; it's GraphQL - verify architecture before implementation ✅
- Implemented auth from scratch; project already had auth library - check dependencies first ✅
```

## Session Analysis Checklist

Before extracting learnings, verify:

- [ ] Did human explicitly correct you?
- [ ] Did you have to redo/rewrite (not just extend)?
- [ ] Did tests fail due to your mistake?
- [ ] Did you repeat the same error?
- [ ] Did you violate documented patterns?

If none of these apply → **No learnings to extract**

This is fine! Many sessions have zero learnings. Good work doesn't generate lessons.

## Output Format

When extracting learnings, provide:

1. **Session Summary:** Brief overview of what was accomplished
2. **Corrections Identified:** List of actual corrections/rework
3. **Learnings Extracted:** Only the items that meet criteria
4. **Confidence Assessment:** How sure you are these are genuine learnings vs. normal work

## The Bottom Line

**Extract corrections, not work done.**

If you got it right the first time → no learning.
If you had to fix it → extract the pattern.

Focus on what needs to change, ignore what worked.
