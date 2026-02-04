---
name: Pain Point Manager
description: Automatically capture, update, and manage development pain points. Use when user mentions friction, blockers, workarounds, or wants to track development obstacles.
allowed-tools: Read, Write, Edit, Grep
---

# Pain Point Manager Skill

## Purpose
Automatically manage the pain points tracking system by capturing new pain points, updating existing ones, archiving resolved items, and extracting patterns.

## Auto-Activation Triggers
This skill activates when the user:
- Mentions "pain point", "friction", "blocker", "workaround"
- Says "that was frustrating" or similar sentiment
- Describes manual workarounds or repetitive tasks
- Mentions "we should fix this" or "this is annoying"
- Asks to add/update pain points
- Requests weekly pain point review

## Core Operations

### 1. Capture New Pain Point
**Trigger phrases:**
- "This is a pain point"
- "Add this to pain points"
- "This keeps causing issues"

**Workflow:**
1. Read `.claude/pain-points/active-pain-points.md`
2. Determine next available PAIN-ID
3. Gather context automatically (file paths, frequency, impact)
4. Classify priority:
   - **Critical**: "blocking", "can't deploy", "broken"
   - **High**: "daily", "multiple times", "significant delay"
   - **Medium**: "weekly", "annoying", "workaround exists"
   - **Low**: "occasionally", "nice to have"
5. Add new entry with complete metadata
6. Confirm capture with ID reference

**Template:**
```markdown
### [PAIN-XXXX] Brief action-oriented description
- **Impact**: Specific scope
- **Frequency**: Daily/Weekly/Occasional
- **First Noted**: YYYY-MM-DD
- **Context**: File paths, scenarios
- **Workaround**: Current approach
- **Potential Solution**: Ideas if discussed
```

### 2. Update Existing Pain Point
**Update Types:**
- Frequency increase
- Priority change
- Status change (resolved)
- Context addition
- Solution progress

### 3. Weekly Review Workflow
**Steps:**
1. Load active pain points
2. Check recent work for friction mentions
3. Update frequency counts
4. Generate focus areas
5. Recommend top 2-3 priorities

**Review Output:**
```markdown
## Weekly Pain Point Review - YYYY-MM-DD

### Current State
- **Total Pain Points**: X
- **New This Week**: X
- **Resolved This Week**: X

### Focus Areas
**Quick Wins** (High Impact, Low Effort):
1. [PAIN-XXXX]: Description

**Strategic Investments** (High Impact, High Effort):
1. [PAIN-XXXX]: Description

### Next Steps
1. Approve focus areas
2. Create tasks for priorities
3. Next review: YYYY-MM-DD
```

### 4. Archive Resolved Items
- Items >30 days old in "Recently Resolved" move to archive
- Generate archival summary with resolution details
- Track biggest wins and common themes

## Priority Scoring

Calculate: (Impact x Frequency) + Urgency Modifier

**Impact Score (1-10):**
- 10: All deployments/team blocked
- 7-9: Major feature or multiple people affected
- 4-6: Single feature or occasional impact
- 1-3: Individual developer, specific scenario

**Frequency Score (1-10):**
- 10: Multiple times per day
- 7-9: Daily
- 4-6: Weekly
- 1-3: Monthly or less

**Auto-Prioritization:**
- Score 15+: Critical
- Score 10-14: High
- Score 5-9: Medium
- Score <5: Low

## Best Practices

### 1. Be Proactive
Listen for friction language and offer to capture without being asked.

### 2. Be Specific
Don't accept "deployment is slow" - require measurable details.

### 3. Keep It Current
Weekly reviews, monthly archival, quarterly pattern analysis.

### 4. Link Evidence
File paths, task IDs, commits that show the pain.

### 5. Focus on Actionability
Every pain point needs clear description, measurable impact, and potential solution path.

## Integration

### With Git Commits
Reference in commit messages: `"Fix: [description] (PAIN-XXXX)"`

### With Memory System
- Episodic memory feeds discovery
- Pain point patterns update procedural memory

## Skill Metadata

**Version:** 1.0.0
**Category:** Development Experience & Quality
**Maintenance**: Weekly active use, Monthly archival
