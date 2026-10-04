---
name: feedback-improvement
description: Systematic workflow for capturing Claude failures and encoding fixes into memory or skills. Use when user says "you screwed up", "that didn't work", "you keep doing X wrong", "remember this for next time", "don't do that again", or after any Claude failure that should be prevented in future sessions.
---

# Feedback Improvement Workflow

Turn user observations about Claude failures into durable fixes.

## Core Principle

**User is validator, Claude is executor.** Claude cannot reliably self-diagnose. This workflow captures user observations as testable constraints.

## Workflow

### 1. Isolate Failure

Identify:
- **What happened** vs **what should have happened**
- **Pattern or one-off** - Recurring = encode fix, one-off = acknowledge only
- **Scope** - This session only, or permanent?

### 2. Diagnose Root Cause

| Category | Fix Type |
|----------|----------|
| Missing procedure | Add workflow |
| Skipped step | Add checkpoint/gate |
| Wrong assumption | Add "must verify" rule |
| Overconfidence | Add "when uncertain" guard |
| Ignored existing rule | Reinforce or clarify rule |

### 3. Choose Fix Location

**Memory edit** when:
- User-specific preference or fact
- Standing instruction for this user's projects

**Skill proposal** when:
- Reusable workflow for any user
- Multi-step process with validation logic

**Session-only** when:
- User says "just for now"
- Too context-specific to generalize

### 4. Execute Fix

#### Memory Edits

```
memory_user_edits command="view"
memory_user_edits command="add" control="For Python: MUST view entire file before str_replace"
memory_user_edits command="replace" line_number=3 replacement="Updated rule"
memory_user_edits command="remove" line_number=5
```

Write concise, actionable rules:
- ❌ "User doesn't like when imports break"
- ✅ "Never edit Python without viewing full file first"

#### Skill Proposals

Skills are **read-only** during conversations. Cannot modify directly.

1. Draft fix in `/home/claude/skill-fix-proposal.md`
2. Present to user with exact text to add/change
3. User uploads updated skill externally

Format:
```markdown
## Skill Fix Proposal
Target: /mnt/skills/user/[skill]/SKILL.md

### Add after [section]:
[exact text]
```

#### Session-Only

State explicitly: "For this session, I will [behavior]. This won't persist."

### 5. Validate

Confirm with user:
1. State fix in plain language
2. Describe when it triggers
3. Ask: "Does this capture what you want?"

## Fix Quality

- **Specific**: Exact behavior, not vague intention
- **Testable**: User can observe compliance
- **Minimal**: Fewest words that work
- **Non-contradictory**: No conflict with existing rules

## Anti-Patterns

Do not encode:
- Vague vibes ("be more careful")
- Rules that bypass safety checks
- Duplicates of existing rules
- Preferences that discourage honest feedback
