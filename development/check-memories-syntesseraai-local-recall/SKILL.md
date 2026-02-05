---
name: check-memories
description: This skill should be used when the user asks "how did we solve this before", "what was the decision about X", "have we done this before", "what do you remember about", "check your memory", or when searching for past context, previous decisions, or historical information about the project.
---

# Check Memories

This skill provides guidance for searching local-recall memories to find relevant historical context.

## When to Use

Invoke this skill when:
- The user explicitly asks about past decisions or previous work
- The user asks "do you remember" or "have we discussed"
- Searching for historical context about a specific topic
- Looking up previous architectural decisions
- Finding past bug fixes or solutions

## How to Search Memories

### Episodic Memories

Episodic memories contain facts, decisions, and observations from past sessions:
- Architectural decisions and rationale
- Bug fixes and their root causes
- User preferences and conventions
- Configuration changes and why they were made
- Project-specific knowledge

Use the `episodic_search` tool with a natural language query:

```
episodic_search(query: "authentication implementation decision")
```

### Thinking Memories

Thinking memories contain reasoning patterns - how problems were analyzed and solved:
- Debugging approaches that worked
- Decision-making processes
- Analysis patterns for similar problems

Use the `thinking_search` tool:

```
thinking_search(query: "debugging race condition in async code")
```

## Search Strategy

1. **Start broad, then narrow**: Begin with general terms, refine based on results
2. **Use domain terms**: Include specific technical terms from the codebase
3. **Check both memory types**: Episodic for facts, thinking for reasoning patterns
4. **Consider scope filters**: Use `scope: "file:path/to/file"` for file-specific memories

## Interpreting Results

- **Similarity scores**: Higher is better (0.0-1.0 scale)
- **Recency**: More recent memories may be more relevant for evolving decisions
- **Keywords**: Check if memory keywords match the query context
- **Scope**: `global` memories apply everywhere; `file:` or `area:` scoped memories are context-specific

## Creating New Memories

When learning something important that should be remembered:

```
episodic_create(
  subject: "Brief description of the memory",
  keywords: ["relevant", "searchable", "terms"],
  applies_to: "global",  // or "file:path" or "area:name"
  content: "Detailed content in markdown"
)
```

Good candidates for new memories:
- Decisions with rationale that may be questioned later
- Non-obvious configurations and why they exist
- User preferences that should persist
- Bug fixes with root cause analysis
