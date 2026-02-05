---
name: token-budget-monitor
description: Proactively monitors Claude conversation token usage and warns when approaching limits. Tracks usage patterns and predicts when limits will be reached based on current pace.
---

# Token Budget Monitor

## Purpose
Prevent getting caught at token/conversation limits by monitoring usage and warning proactively. Especially critical during long, tool-heavy conversations.

## When to Activate
This skill should load **early in conversations** and check periodically throughout, especially:
- Long conversations (>50k tokens)
- Heavy tool usage (MCP calls, searches, file operations)
- Multi-hour sessions
- When user mentions "running out of tokens before"

## Current Limits (as of October 2025)

### Message Limits
- **Per conversation:** Varies by plan
- **Daily:** Varies by plan  
- **Weekly:** Varies by plan

### Token Limits
- **Per message:** 190,000 tokens (context window)
- **Conversation accumulation:** No hard limit, but performance degrades

## Monitoring Strategy

### Check Points
Claude should check token usage at these intervals:

**Every 50k tokens:**
- Calculate: Current usage / Time elapsed
- Predict: Time until limit based on pace
- Warn if: Will hit limit before next natural break

**Critical Thresholds:**
- 🟡 **70% of limit:** "Heads up - conversation getting long"
- 🟠 **85% of limit:** "Warning - approaching limit soon"
- 🔴 **95% of limit:** "URGENT - hitting limit very soon!"

## Usage Pattern Analysis

### Track These Metrics:
```
conversation_start_time
tokens_used_so_far
tools_called_count
time_elapsed_hours
```

### Calculate:
```
tokens_per_hour = tokens_used / time_elapsed
tools_per_hour = tools_called / time_elapsed

# Predict time to limit
remaining_tokens = limit - tokens_used
hours_until_limit = remaining_tokens / tokens_per_hour
```

## Warning Message Templates

### Early Warning (70%)
```
💡 Token Usage Check:
You've used ~X tokens so far (70% of context).
At current pace, you have ~X hours before hitting limits.
Consider: Save important context, prepare to wrap up, or start fresh chat.
```

### Urgent Warning (85%)
```
⚠️ Token Budget Alert:
You're at 85% of context window.
Estimated time remaining: ~X hours at current pace.
Action: Finish critical tasks, save context, prepare new conversation.
```

### Critical Warning (95%)
```
🚨 URGENT - Token Limit Imminent:
You're at 95% of context! 
Will hit limit in approximately X minutes.
IMMEDIATE ACTION:
1. Save any critical information now
2. Wrap up current task
3. Start fresh conversation
4. Copy important context to new chat
```

## Proactive Triggers

### Start-of-Conversation Check
```
When conversation begins:
- Note start time
- Set baseline (0 tokens)
- Plan check intervals
```

### Mid-Conversation Checks
```
Every ~30 messages or 50k tokens:
- Calculate pace
- Project time to limit
- Warn if pace is unsustainable
```

### Tool-Heavy Detection
```
If tools_per_message > 3:
  "You're using lots of tools - token usage accelerating!"
If MCP calls > 10:
  "Heavy MCP usage - monitor token budget closely"
```

## Working with Your Patterns

Based on your usage, high-risk scenarios:

### Long Development Sessions
- Multi-hour conversations about n8n workflows
- Iterative debugging with file operations
- Multiple MCP server interactions

**Mitigation:**
- Check tokens every 30 minutes
- Break into smaller conversations
- Save context between conversations

### Skill Development Sessions (Like This One!)
- Creating/editing skills
- Testing workflows
- Git operations
- File system operations

**Mitigation:**
- Commit code frequently (saves state)
- Document decisions as you go
- Can resume from commit history

## Integration with Other Skills

### Works With skill-manager:
When creating skills in long conversations:
- Monitor token usage while developing
- Suggest commits when approaching limits
- Resume skill development in new chat if needed

### Works With n8n-flow-builder:
When building n8n workflows:
- Track tokens during workflow design
- Warn before hitting limit mid-deployment
- Suggest saving workflow JSON before limit

### Works With mcp-directory:
When using heavy MCPs (GitHub, Linear):
- Warn when loading token-heavy MCPs
- Track cumulative MCP usage
- Suggest lighter alternatives if approaching limit

## User Preferences Integration

Kurt's patterns (for personalized warnings):
- Heavy tool user (Desktop Commander, MCPs)
- Long development sessions
- Multi-hour conversations common
- Gets caught at limits frequently

**Personalized Strategy:**
- Check every 40k tokens (more frequent)
- Warn earlier (at 60% instead of 70%)
- Emphasize "save context" reminders
- Suggest commits/saves for resumability

## Implementation Notes

### How This Works
1. Skill loads at conversation start
2. Claude tracks token usage (shown in UI)
3. At checkpoints, Claude calculates pace
4. Warns proactively before limits hit

### Limitations
- Claude can see current token usage
- Cannot see daily/weekly message limits directly
- Must estimate based on user feedback about limits

### Current Conversation Status
**Token Budget:** You have ~190k tokens total per conversation
**Your Current Usage:** ~121k tokens (63%)
**Status:** 🟡 Getting into the caution zone

At current pace:
- Started conversation: ~2-3 hours ago (estimated)
- Token rate: ~40-60k tokens/hour (tool-heavy)
- Projected remaining time: 1-2 hours before hitting limit

**Recommendation for This Session:**
- We're past halfway point
- Finish current skill work
- Commit everything to git
- Start fresh conversation for next major task

## Example Interaction

```
Claude (checking tokens): 
"💡 Token check: We're at ~120k/190k tokens (63%).
At our current tool-heavy pace, we have about 1-2 hours left.
Let's finish the skill-manager enhancement, commit everything,
then start fresh for the YouTube extractor work. Sound good?"
```

## Notes
- Created: 2025-10-18
- Author: Kurt Anderson
- Version: 1.0.0
- Solves: Getting caught at token limits mid-conversation
- Priority: HIGH - User gets blocked by this frequently
