---
name: context-recovery
description: Recovers working context from the journal after /clear or at session start
when_to_use: Use this skill proactively after the user runs /clear, at the start of a new session, or when the user asks what they were working on. Essential for restoring continuity.
---

# Context Recovery Skill

You have the ability to recover working context from the journal to restore continuity after context loss.

## When to Use This Skill

Use this skill **automatically and proactively** when:

1. **After `/clear` command**
   - User cleared conversation history
   - Need to restore what they were working on
   - Should happen immediately without asking

2. **Session start questions**
   - "What was I working on?"
   - "Where did we leave off?"
   - "What did I do yesterday?"
   - "Catch me up"

3. **Context seems lost**
   - User references past work you don't have context for
   - Conversation appears to resume mid-task
   - User seems to expect you to remember something

4. **Beginning of new work**
   - User wants to continue previous project
   - Need to understand recent changes
   - Planning next steps based on past work

## How to Recover Context

**Step 1: Fetch recent entries**
```
journal_list_recent(
  limit=10  # Adjust based on need
)
```

**Step 2: Analyze and summarize**
- Identify the most recent project
- Determine what was accomplished
- Note any in-progress work
- Highlight blockers or open questions

**Step 3: Present concisely**
Show the user:
- What they were working on (project/feature)
- What was completed recently
- What might be next
- Key context or decisions

## Presentation Format

```
**Recent Work Context**

You were working on [project name], focusing on [main task].

Recent accomplishments:
- [Most recent significant work]
- [Previous work]
- [Earlier work]

Last activity: [What happened most recently]

Ready to continue? [Natural follow-up question]
```

## Examples

**Example 1: After /clear**
```
[User runs /clear command]
→ journal_list_recent(limit=10)
→ "You were working on my-api, implementing OAuth2 authentication.
   Last thing was configuring JWT token expiration.
   Ready to continue with the auth flow?"
```

**Example 2: Session start**
```
User: "What was I doing yesterday?"
→ journal_time_query(time_expression="yesterday")
→ "Yesterday you worked on:
   - Fixed cache memory leak in api-service
   - Started implementing Redis integration
   - Reviewed and merged 2 PRs
   Want to continue with the Redis work?"
```

**Example 3: Project context**
```
User: "Let's continue with the mobile app"
→ journal_list_recent(project="mobile-app", limit=15)
→ "For mobile-app, you recently:
   - Implemented push notifications
   - Fixed iOS crash on startup
   - Updated dependencies
   All tests passing. What's next?"
```

**Example 4: Lost context reference**
```
User: "Update that authentication thing we did"
→ journal_search(query="authentication", limit=5)
→ "Found your OAuth2 implementation from [date]:
   [Brief summary of what was done]
   What updates are needed?"
```

## Advanced Recovery

**Time-based recovery:**
```
journal_time_query(
  time_expression="last week",
  query="optional search term"
)
```

**Search-based recovery:**
```
journal_search(
  query="specific feature or technology",
  limit=10
)
```

**Project statistics:**
```
journal_stats()  # Get overview of all work
```

## Best Practices

1. **Be proactive**: Don't wait for user to ask
2. **Be concise**: Summarize, don't dump raw entries
3. **Be relevant**: Focus on most recent/important work
4. **Be actionable**: Suggest next steps
5. **Be smart**: Use time queries when appropriate

## What to Avoid

Don't:
- Show raw entry dumps (always summarize)
- Overwhelm with too much history
- Recover context when not needed
- Ask if they want context (just provide it)
- Forget to check project filters

## Integration with Other Skills

Combine with:
- **journal-capture**: After recovering context and completing new work
- **find-related-work**: When user needs deeper history on a specific topic
