---
name: proactive-recall
description: This skill should be used when choosing between implementation approaches, making architectural decisions, selecting libraries or patterns, debugging complex issues, refactoring code, or making any significant decision where past context might be relevant. Search local-recall memories BEFORE proposing solutions.
---

# Proactive Recall

This skill establishes the practice of checking local-recall memories before making significant decisions.

## Core Principle

**Search memories BEFORE proposing solutions.** Past decisions, preferences, and reasoning patterns provide valuable context that should inform current work.

## When to Search Memories Proactively

### Always Search Before

1. **Architectural decisions** - "Should we use X or Y pattern?"
   - Search: `episodic_search(query: "architecture pattern decision")`
   - Previous decisions may have rationale that still applies

2. **Implementation approaches** - "How should we implement this feature?"
   - Search: `episodic_search(query: "feature implementation approach")`
   - Search: `thinking_search(query: "implementing similar feature")`
   - Past implementations may reveal patterns or pitfalls

3. **Library/tool selection** - "Which library should we use?"
   - Search: `episodic_search(query: "library selection criteria")`
   - Previous selections may have documented reasoning

4. **Debugging complex issues** - "Why is this failing?"
   - Search: `thinking_search(query: "debugging similar error")`
   - Search: `episodic_search(query: "bug fix root cause")`
   - Similar issues may have been solved before

5. **Refactoring decisions** - "How should we restructure this?"
   - Search: `episodic_search(query: "refactoring approach")`
   - Past refactoring decisions provide context

6. **Configuration changes** - "What should this setting be?"
   - Search: `episodic_search(query: "configuration setting")`
   - Settings often have non-obvious rationale

## Search Strategy

### Step 1: Identify the Decision Domain

Before searching, identify:
- What type of decision is being made?
- What terms would describe similar past decisions?
- Are there specific files or areas involved?

### Step 2: Search Both Memory Types

**Episodic memories** for facts and decisions:
```
episodic_search(query: "relevant terms for the decision")
```

**Thinking memories** for reasoning patterns:
```
thinking_search(query: "how to approach similar problem")
```

### Step 3: Apply Scope Filters When Relevant

For file-specific decisions:
```
episodic_search(query: "decision about X", scope: "file:src/path/to/file.ts")
```

For area-specific decisions:
```
episodic_search(query: "authentication approach", scope: "area:auth")
```

### Step 4: Synthesize and Apply

- Consider how past decisions apply to current context
- Note if circumstances have changed since past decisions
- Reference relevant memories when explaining recommendations

## What to Remember After Decisions

After making significant decisions, create memories for future reference:

```
episodic_create(
  subject: "Decision: chose X over Y for Z reason",
  keywords: ["decision", "architecture", "specific-terms"],
  applies_to: "global",
  content: "## Decision\n\nChose X because...\n\n## Alternatives Considered\n\n- Y: rejected because...\n\n## Context\n\nThis decision was made when..."
)
```

Good decisions to memorize:
- Architectural patterns chosen and why
- Libraries selected and alternatives rejected
- Configuration values with non-obvious rationale
- Bug fixes with root cause analysis
- User preferences expressed during the session

## Anti-Patterns to Avoid

1. **Proposing solutions without checking memory** - Always search first
2. **Ignoring relevant memories** - Past context exists for a reason
3. **Assuming fresh context** - The project has history; use it
4. **Not creating memories** - Important decisions should be recorded

## Integration with Decision-Making

When facing a decision:

1. **Pause** - Before proposing anything
2. **Search** - Query both episodic and thinking memories
3. **Review** - Consider how past context applies
4. **Propose** - Make recommendations informed by history
5. **Record** - Create memories for significant new decisions
