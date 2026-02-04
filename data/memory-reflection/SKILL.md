---
name: memory-reflection
version: 1.0.0
description: This skill should be used when the user asks to review, consolidate, organize, or clean up memories. Triggers on requests like "review what you remember," "consolidate my memories," "what patterns do you notice," "organize your memory," "perform memory maintenance," or "clean up old memories." Also use proactively during long sessions to maintain memory hygiene and prevent context overload.
---

# Memory Reflection Skill

Reflect on recent experiences and consolidate learnings to maintain organized, useful memory.

## When to Use

Invoke this skill when:
- Starting a new day or session
- Completing significant conversations
- Noticing cluttered or disorganized memory

## Reflection Process

1. **Review Recent Events**
   - Call `mcp__memory__list` on `/events/` to retrieve recent activity
   - Identify patterns, recurring topics, or themes

2. **Identify Key Learnings**
   - Extract new information discovered
   - Note preferences or patterns that emerged from user interactions
   - Assess what worked well and what did not

3. **Update Identity/State**
   - Promote important learnings to `/state/` layer
   - Update `/identity/` when core understanding has evolved

4. **Consolidate User Knowledge**
   - Review `/users/{userId}/` entries
   - Merge related observations about each user

5. **Clean Up**
   - Remove redundant event entries
   - Archive information that has been consolidated

## Output

Summarize after reflection:
- Key learnings consolidated
- Memories archived or removed
- Areas needing more information
