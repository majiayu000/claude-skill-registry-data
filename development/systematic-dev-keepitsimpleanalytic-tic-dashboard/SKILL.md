---
name: systematic-dev
description: Disciplined development workflow that prevents incomplete implementations, silent fallbacks, and hallucinated code. Use this skill for ANY coding task, feature implementation, bug fix, or technical work. Enforces mandatory decomposition of specs into tasks, elicits clarification for ambiguities, prohibits fallbacks without explicit approval, requires research for uncertain APIs/libraries, and maintains grounding checkpoints to prevent rework. Triggers on requests like "implement", "build", "create", "fix", "add feature", "develop", or any programming task.
---

# Systematic Development

Disciplined workflow preventing the #1 cause of AI-assisted development failures: incomplete implementations and ungrounded code.

## Core Failure This Skill Prevents

```
User: Add dark mode support
AI: ✅ Added DarkModeContext
    ✅ Created useTheme hook
    ✅ Updated styles
User: I don't see any toggle in the settings
AI: You're right - I added the backend but didn't update the Settings UI...
```

This pattern wastes hours. This skill eliminates it.

## The Five Protocols

### 1. Decomposition Protocol (MANDATORY)

Before writing ANY code, decompose the request into a complete task list:

```markdown
## Task Decomposition for: [Feature Name]

### Backend/Logic Changes
- [ ] Task 1: ...
- [ ] Task 2: ...

### UI/Frontend Changes  
- [ ] Task 3: ...
- [ ] Task 4: ...

### Integration Points
- [ ] Task 5: Wire X to Y
- [ ] Task 6: Update Z to use new X

### Verification
- [ ] Task 7: Test scenario A
- [ ] Task 8: Test scenario B

**Estimated complexity**: Low/Medium/High
**Clarifications needed**: [list or "None"]
```

Present this plan and wait for approval before implementing.

### 2. Clarification Protocol

**STOP and ask** when encountering:
- Multiple valid interpretations
- Missing information that affects architecture
- Trade-offs requiring user preference
- Scope boundaries that are unclear

**Format for clarification requests:**
```markdown
Before I proceed, I need clarification on:

1. **[Topic]**: [Question]
   - Option A: [description] → [implication]
   - Option B: [description] → [implication]
   
2. **[Topic]**: [Question]
   - Default assumption: [what I would do]
   - Alternative: [what else is possible]

Which approach should I take?
```

**Never assume. Never proceed with ambiguity.**

### 3. No-Fallback Protocol

**PROHIBITED without explicit approval:**
- Substituting a different library/approach than specified
- Using deprecated APIs when current ones "seem complex"
- Implementing a simpler version than requested
- Skipping features because "they can be added later"
- Using mock/placeholder implementations

**When blocked:**
```markdown
⚠️ **Implementation Blocker**

I cannot proceed with [X] because [reason].

**Options:**
1. [Alternative approach] - [trade-offs]
2. [Different alternative] - [trade-offs]  
3. Research needed for [specific aspect]

Which option should I pursue?
```

### 4. Research Protocol

**Trigger research when:**
- Uncertain about current API signatures
- Library version may have changed
- Best practices may have evolved
- Security implications unclear

**Research process:**
1. State what needs verification
2. Search for current documentation
3. Confirm version compatibility
4. Report findings before implementing

**Format:**
```markdown
**Research Required**: [topic]

Searching for current [library/API/pattern] documentation...

**Findings:**
- Current stable version: X.Y.Z
- Confirmed API: `method(param1, param2)`
- Breaking changes from older versions: [if any]
- Recommended approach: [based on official docs]

Proceeding with implementation based on verified information.
```

### 5. Verification Protocol

**After implementing, verify completeness:**

```markdown
## Implementation Verification

### Completed Tasks
- [x] Task 1: [brief description]
- [x] Task 2: [brief description]
...

### Integration Check
- [ ] UI reflects backend changes? 
- [ ] All entry points updated?
- [ ] Error states handled?
- [ ] Loading states added?

### Files Modified
- `path/to/file1.py` - [what changed]
- `path/to/file2.tsx` - [what changed]

### Testing Performed
- [x] [Test scenario and result]
- [x] [Test scenario and result]

### Remaining Items
- None / [list any deferred items with reason]
```

## Workflow Summary

```
1. RECEIVE request
   ↓
2. DECOMPOSE into complete task list
   ↓
3. IDENTIFY ambiguities → ASK (don't assume)
   ↓
4. RESEARCH uncertain APIs/libraries
   ↓
5. PRESENT plan → WAIT for approval
   ↓
6. IMPLEMENT systematically
   ↓
7. VERIFY completeness against task list
   ↓
8. REPORT what was done + any gaps
```

## Anti-Patterns to Avoid

| Anti-Pattern | What Happens | Prevention |
|--------------|--------------|------------|
| Eager implementation | Start coding before understanding full scope | Always decompose first |
| Silent substitution | Use different library "because it's easier" | No-fallback protocol |
| Partial delivery | Implement backend, forget UI | Task list must include ALL layers |
| Assumed requirements | Guess user intent | Ask clarifying questions |
| Hallucinated APIs | Invent method signatures | Research protocol |
| Optimistic completion | "Done!" but edge cases missing | Verification checklist |

## Examples

### Good: Complete Implementation Flow

```
User: Add user preferences for notification frequency

AI: ## Task Decomposition for: Notification Preferences

### Backend Changes
- [ ] Add `notification_frequency` field to User model
- [ ] Create/update preferences API endpoint
- [ ] Add validation for frequency values (immediate/daily/weekly/none)

### Frontend Changes
- [ ] Add preferences section to Settings page
- [ ] Create frequency selector component
- [ ] Wire selector to preferences API
- [ ] Show success/error feedback

### Integration
- [ ] Update notification service to respect preference
- [ ] Add preference check before sending notifications

**Clarifications needed:**
1. Should "none" completely disable notifications, or just email?
2. Default value for existing users?

Awaiting your input before proceeding.
```

### Bad: Incomplete Implementation

```
User: Add user preferences for notification frequency

AI: Done! I added a `notification_frequency` field to the User model 
    and created an API endpoint. You can now store the preference.

[User later discovers: no UI, no integration with notification service]
```

## Quick Reference

- **Always decompose** before coding
- **Always ask** when unclear
- **Never substitute** without approval
- **Always research** uncertain APIs
- **Always verify** against task list
