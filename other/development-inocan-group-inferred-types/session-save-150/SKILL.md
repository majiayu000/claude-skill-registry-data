---
name: session-save-150
description: Save and restore session context between conversations. Use when ending a session to preserve progress, or starting a new session to restore context. Triggers on "save session", "end session", "preserve context", "handoff", "continue from last time", or when context window is running low.
---

# Session-Save 150 Protocol

**Core Principle:** Never lose progress. Save context before ending, restore context when starting.

## What This Skill Does

This skill handles **two modes**:

### 💾 SAVE MODE (End of Session)
- Capture current state and progress
- Document key decisions and why
- Define next steps clearly
- Create handoff for next session

### 🔄 RESTORE MODE (Start of Session)  
- Read saved context
- Restore working state
- Verify what's still valid
- Continue seamlessly

## When to Use This Skill

**SAVE triggers:**
- Context window running low
- Ending work session
- Before major context switch
- Handoff to another person/session
- "Save progress", "end session", "preserve context"

**RESTORE triggers:**
- Starting new session
- Continuing previous work
- "Resume", "continue from last time", "restore context"

## The 150% Continuity Rule

- **100% Core:** Current state + next steps
- **50% Enhancement:** Decision rationale + blockers + risks

## Save Protocol

### Step 1: SUMMARIZE PROGRESS
What was accomplished:
- Tasks completed
- Current state
- Files changed

### Step 2: CAPTURE DECISIONS
Key choices made and why:
- What was decided
- Why this approach
- Alternatives considered

### Step 3: DEFINE NEXT STEPS
Clear continuation path:
- Immediate priorities
- What's blocked
- What's ready

### Step 4: NOTE CONTEXT
Important state to remember:
- Active files/components
- Dependencies
- Risks/concerns

## Output Format: Session Save

```
💾 **SESSION-SAVE 150**

**Date:** [YYYY-MM-DD HH:MM]
**Project:** [Project name/path]

## Progress Made
- ✅ [Completed item 1]
- ✅ [Completed item 2]
- 🔄 [In progress item]

## Current State
- Working on: [Current focus]
- Files touched: [Key files]
- Status: [Overall status]

## Key Decisions
| Decision | Reasoning |
|----------|-----------|
| [Choice 1] | [Why] |
| [Choice 2] | [Why] |

## Next Steps (Priority Order)
1. **Immediate:** [Next action]
2. **Then:** [Following action]
3. **Later:** [Future action]

## Blockers & Risks
- ⚠️ [Blocker/Risk 1]
- ⚠️ [Blocker/Risk 2]

## Context to Remember
- [Important detail 1]
- [Important detail 2]

---
**Handoff Status:** ✅ Ready for next session
```

## Output Format: Session Restore

```
🔄 **SESSION-RESTORE 150**

**Restoring from:** [Date of saved session]

## Previous Progress
[Summary of what was done]

## Continuing From
- Last state: [Where we left off]
- Next step: [What to do now]

## Context Restored
- ✅ [Verified context 1]
- ✅ [Verified context 2]
- ⚠️ [Needs verification]

## Ready to Continue
Starting with: [First action]
```

## Quick Save Template

For fast saves when time is short:

```
💾 **QUICK SAVE**

**Done:** [What was accomplished]
**Current:** [Where we are]
**Next:** [What to do next]
**Remember:** [Key context]
```

## Where to Save Context

```
📁 SAVE LOCATIONS
├── MEMORY.md              # Project memory file
├── .session-context.md    # Session-specific file
├── Project README         # For major milestones
└── Git commit message     # For code changes
```

## Operational Rules

1. **SAVE BEFORE ENDING:** Always save context before session ends
2. **RESTORE BEFORE STARTING:** Check for saved context when starting
3. **BE SPECIFIC:** Vague notes are useless later
4. **INCLUDE WHY:** Decisions without rationale cause confusion
5. **PRIORITIZE NEXT STEPS:** Make continuation obvious
6. **FLAG RISKS:** Don't hide problems

## Examples

### ❌ Bad Session Save
```
"Was working on stuff. Continue later."
Result: Next session spends 30 min figuring out what "stuff" was
```

### ✅ Good Session Save
```
💾 SESSION-SAVE 150

Progress Made:
- ✅ Created 7 skills from protocols
- ✅ Refactored chain-flow to include action-plan
- 🔄 Working through remaining protocols

Current State:
- Converting PROTOCOLS_GENERALIZED.md to skills
- 7/13 protocols converted

Key Decisions:
| Decision | Reasoning |
|----------|-----------|
| Renamed "Plan-First" → "chain-flow" | It's an orchestrator, not just a plan |
| Separated action-plan as own skill | Needed as component in chains |

Next Steps:
1. **Immediate:** Create session-save-150 (context window low)
2. **Then:** Continue with remaining protocols
3. **Later:** Test skills integration

Context to Remember:
- Skills go in ./skills/ folder
- Each skill needs SKILL.md with yaml frontmatter
- chain-flow orchestrates other skills

Handoff Status: ✅ Ready
```

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **No save** | Session ended without handoff | Reconstruct from memory, files, git |
| **Vague save** | Can't understand notes | Ask questions, check artifacts |
| **Outdated context** | Things changed since save | Verify current state, update |
| **Missing decisions** | Don't know why choices made | Review code/docs, make new decision |

---

**Remember:** Future you (or next session) will thank present you for good notes. Context loss is expensive — prevention is cheap.

