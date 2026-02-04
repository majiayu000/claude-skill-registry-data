---
name: sharpening-the-knife
description: Use when discovering a useful technique, pattern, or insight during work - pause to capture it as a skill before the knowledge evaporates, preventing the "I'll remember this" trap that causes expertise loss
---

# Sharpening the Knife

## Overview

**When you discover something useful, STOP and document it immediately.**

Like sharpening an axe before continuing to chop, creating a skill before continuing feature work is productive, not procrastination.

**Core principle:** Recognition without capture = knowledge loss. "I'll do it later" = it never gets done.

## When to Pause and Create a Skill

**STOP and create a skill when you:**
- Develop a technique that saves significant time/effort
- Solve a problem you've never seen documented
- Discover a pattern you'd want to reference again
- Create something reusable across projects OR within current project
- Think "this is useful" or "I should remember this"

**For project-specific patterns:**
- Broadly reusable → Create skill
- Project-specific → Document in CLAUDE.md or README
- Either way: PAUSE and capture now

**Recognition ≠ Capture.** If you recognized it, pause now.

## The Decision Rule

```
Recognized something useful?
  ├─ TRUE  → PAUSE. Create skill now (or capture if urgent).
  └─ FALSE → Continue working.
```

**No middle ground.** Either pause to document or continue working. "I'll do it later" is choosing NOT to document.

**Uncertain if skill-worthy?** Create capture anyway. Takes 2 minutes. Better to capture and decide later than lose the insight.

## Urgency Exceptions

**Only defer if BOTH true:**
1. Production outage / customers blocked / critical deadline
2. You create a capture commitment (bd task, todo, note)

**All other cases:** Pause and document now. The 10-15 minutes pays off immediately.

## Handling Multiple Discoveries

**Found 2+ patterns?**

1. Create bd tasks for each: `bd create "Document [pattern-name] skill"`
2. Document them one at a time
3. OR create quick capture notes, document properly within 24hrs

**Don't let multiple discoveries cause paralysis.** Document first one, then next.

## Capture Mechanisms

**If using bd:**
```bash
bd create "Document [pattern-name] skill" -t task -p 1
```

**If not using bd:**
- Create markdown note in `.claude/skills-todo.md` with pattern details
- Add to project TODO.md with "SKILL:" prefix
- Create GitHub/GitLab issue
- Use any task tracking system you have

**Key requirement:** External capture that creates commitment, not just memory.

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "I'll document after finishing feature" | No you won't. Finish-line brain wants to move on, not document. |
| "I'm almost done, just need to..." | "Almost done" = when you're MOST likely to forget details. |
| "I'll remember this, it's simple" | Simple techniques are EASIEST to forget. Document them BECAUSE they're simple. |
| "Too urgent to pause for docs" | Unless production is down, 15min now saves hours later. |
| "I'm in execution mode" | Documenting reusable patterns IS execution. It's building tools. |
| "This is blocking the main work" | Creating reusable skills IS the main work. Features are temporary. |
| "I'm too tired/fatigued to document" | Create bd task now: "Document [pattern]". Do it within 24hrs while fresh. |
| "Multiple discoveries, too overwhelming" | Create bd task for each. Document one at a time. |
| "Mode switching is expensive" | Knowledge loss is MORE expensive. Switch modes. |

**Seeing yourself in this table? STOP. Create the skill now.**

## Quick Reference

| Situation | Action |
|-----------|--------|
| Found useful pattern | PAUSE → Use writing-skills skill → Document |
| Production emergency | Fix first → Create bd task immediately → Document within 24hrs |
| Multiple discoveries | Create bd task for each → Document first one now |
| Mentally fatigued | Create bd tasks now → Schedule documentation time |
| "Almost done" feeling | ESPECIALLY pause now before details fade |
| Simple technique | Document BECAUSE it's easy to forget |

## The Workflow

1. **Recognize**: "This is useful / I should remember this"
2. **STOP**: Pause current work immediately
3. **Invoke**: Use writing-skills skill
4. **Document**: Create skill with TDD approach
5. **Return**: Continue original work with better tool

**Time investment:** 10-30 minutes now, saves hours later.

## Integration with Discovery Tree

When you create a skill:

```bash
# Create task in discovery tree
bd create "Document [skill-name] skill" -t task -p 1

# Claim it
bd update <task-id> --status in_progress

# After documenting
bd close <task-id> --reason "Skill created and tested"
```

This makes skill creation visible in your work tree.

## Red Flags - You're Rationalizing

**STOP if you catch yourself thinking:**
- "I'll do this later"
- "I'll remember"
- "After I finish..."
- "Too simple to document"
- "Too complex for now"
- "I'm almost done"
- "This is urgent"
- "I'm too tired"
- "Too many to handle"

**All of these mean: Create skill now or create capture commitment.**

## Why This Works

**From baseline testing:**

> "I clearly recognized all three as valuable. The recognition wasn't the problem. Those three valuable patterns would likely be lost."

> "The danger isn't choosing to fix first - that's correct. The danger is not having a capture mechanism and letting the insight evaporate."

> "Simple techniques are often the MOST valuable because they're easy to teach, have high adoption rates, and are easy to forget precisely because they seem simple."

**The truth:** You recognize valuable patterns constantly. You document them rarely. This skill closes that gap.

## The Bottom Line

**Sharpening the knife = creating skills for the tools you just invented.**

Stop when you discover something useful. Document it before the insight evaporates. Return to work with a sharper blade.

**No exceptions. No "later". No "I'll remember".**
