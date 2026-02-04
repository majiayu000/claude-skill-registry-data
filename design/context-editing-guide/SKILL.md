---
name: context_editing_guide
description: Managing context window, token optimization, summarization strategies for long conversations.
---

# Context Editing Skill

## When to Use
- Questions about managing long conversations
- Token cost concerns
- "Context window filling up"
- "Claude forgets earlier messages"
- "How to handle 20+ turn conversations"
- Summarization and compression strategies

## Key Feature: Context Editing

Context Editing lets you intelligently manage what stays in Claude's context window.

### Core Capabilities
1. **Summarization**: Compress older turns while preserving meaning
2. **Fact Extraction**: Pull out key facts to persistent storage
3. **Selective Retention**: Keep important messages verbatim
4. **Dynamic Management**: Adjust context based on conversation flow

### Recommended Pattern for Long Conversations

```
Turns 1-5:    Keep verbatim (recent context)
Turns 6-15:   Summarize (compressed context)
Persistent:   Extracted facts (always present)
```

### Token Savings
- Typical reduction: 60-70% for conversations over 20 turns
- Better user experience: Claude "remembers" key facts
- Cost savings scale with conversation length

## Response Guidelines

1. **Identify the problem**: Long conversations? Token costs? Lost context?
2. **Explain the pattern**: Verbatim + Summarized + Persistent
3. **Give specific numbers**: 60-70% savings, turn thresholds
4. **Offer to dive deeper**: Architecture details if they want
