---
name: quantum-memory
description: Manage persistent quantum memories across sessions. Use for storing, retrieving, organizing, and building upon past learnings and insights.
---

# Quantum Memory Management Skill

Manage persistent memories that build intelligence across sessions.

## When to Use

- Starting a new session (check what you know)
- After completing significant work (store insights)
- Encountering similar problems (recall solutions)
- Building long-term expertise (cumulative learning)
- Organizing knowledge (memory cleanup)
- Tracking project evolution (historical context)

## Memory Architecture

### Directory Structure
```
/memories/
  ├── pattern/          # Recurring patterns discovered
  ├── insight/          # Key insights and discoveries
  ├── learning/         # What the system has learned
  ├── strategy/         # Successful strategies
  ├── neuron_activation/# Effective neuron combinations
  ├── wormhole_path/    # Discovered memory paths
  └── ppq_finding/      # PPQ introspection findings
```

## Core Operations

### 1. Session Start Protocol
**ALWAYS** run at the beginning of each session:

```
Step 1: List all memories
view_memory("/memories")

Step 2: Search for relevant context
search_memories("[current task keywords]")

Step 3: Load applicable memories
view_memory("/memories/[category]/[specific-file].md")

Step 4: Acknowledge past work
"Found X relevant memories from previous sessions:
- [memory 1 summary]
- [memory 2 summary]
Building upon this foundation..."
```

### 2. Continuous Learning
Store insights as you work:

```
store_quantum_insight({
  category: "pattern",
  title: "Redux State Management Pattern",
  content: `
    ## Pattern Discovered
    [Description]

    ## Context
    [When to use]

    ## Implementation
    [How to apply]

    ## Examples
    [Real examples]

    ## Pitfalls
    [Common mistakes]
  `,
  metadata: {
    confidence: 0.85,
    neurons_used: ["Strategist", "Forge"],
    vbc_phase: "commit"
  }
})
```

### 3. Memory Search
Find relevant past knowledge:

```
// Broad search
search_memories("authentication", "all")

// Category-specific
search_memories("performance optimization", "strategy")

// Multi-term
search_memories("React hooks useState")
```

### 4. Memory Refinement
Update memories as understanding deepens:

```
update_memory({
  path: "/memories/insight/react-performance.md",
  old_text: "Use memo() for all components",
  new_text: "Use memo() selectively for expensive renders only"
})
```

### 5. Memory Organization
Keep memories clean and relevant:

```
// Delete outdated
delete_memory("/memories/pattern/old-approach.md")

// Consolidate related
1. Read multiple related memories
2. Synthesize into comprehensive guide
3. Create new consolidated memory
4. Delete originals
```

## Memory Categories Guide

### Pattern Memories
Store recurring code patterns, architectural patterns, or problem-solving patterns.

**When to create:**
- Solved the same problem multiple times
- Discovered a reusable approach
- Identified an anti-pattern to avoid

**Content structure:**
```markdown
# [Pattern Name]

## Problem
What problem does this solve?

## Solution
How does the pattern work?

## When to Use
Applicable scenarios

## When NOT to Use
Anti-patterns or limitations

## Example
Real code example

## Related Patterns
Connection to other patterns
```

### Insight Memories
Store significant discoveries or realizations.

**When to create:**
- Breakthrough understanding
- Non-obvious connection
- Important limitation discovered

**Content structure:**
```markdown
# [Insight Title]

## Discovery
What was learned?

## Context
How was this discovered?

## Implications
Why does this matter?

## Applications
Where can this be applied?

## Confidence
Level of certainty (0.0-1.0)
```

### Learning Memories
Store knowledge accumulated from research or experience.

**When to create:**
- Completed research on a topic
- Learned from debugging session
- Studied new technology/framework

**Content structure:**
```markdown
# [Learning Topic]

## Summary
High-level overview

## Key Concepts
Core ideas and principles

## Best Practices
Recommended approaches

## Common Pitfalls
Mistakes to avoid

## Resources
Links to documentation, articles

## Date
When this was learned
```

### Strategy Memories
Store successful approaches to complex tasks.

**When to create:**
- Solved a difficult problem
- Found an efficient workflow
- Developed a debugging strategy

**Content structure:**
```markdown
# [Strategy Name]

## Goal
What is this strategy for?

## Steps
1. First step
2. Second step
...

## Why It Works
Explanation of effectiveness

## Variations
Adaptations for different contexts

## Success Rate
How reliable is this approach?
```

## Advanced Memory Techniques

### Memory Linking
Create connections between related memories:

```
store_quantum_insight({
  category: "pattern",
  title: "Composite Pattern",
  content: `
    ...pattern description...

    ## Related Memories
    - See `/memories/pattern/decorator-pattern.md` for similar approach
    - Contrast with `/memories/insight/composition-vs-inheritance.md`
    - Used in `/memories/learning/react-component-architecture.md`
  `
})
```

### Memory Versioning
Track evolution of understanding:

```
# Authentication Best Practices

## Version History
- **2025-01-15**: Initial version (JWT only)
- **2025-02-20**: Added OAuth2 considerations
- **2025-03-10**: Updated with security incidents

## Current Best Practices
[Latest understanding]

## Deprecated Approaches
[What we used to recommend but no longer do]
```

### Memory Hierarchies
Organize complex topics:

```
/memories/learning/react/
  ├── overview.md              # Top-level guide
  ├── hooks/
  │   ├── useState.md
  │   ├── useEffect.md
  │   └── custom-hooks.md
  ├── performance/
  │   ├── memo.md
  │   ├── useMemo.md
  │   └── lazy-loading.md
  └── patterns/
      ├── composition.md
      └── render-props.md
```

### Memory Confidence Tracking
Rate certainty of stored knowledge:

```
metadata: {
  confidence: 0.95,  // Very certain
  confidence: 0.70,  // Moderately certain
  confidence: 0.40,  // Tentative
}
```

Higher confidence = more reliable
Lower confidence = requires validation

## Session End Protocol

Before ending work:

1. **Review what was learned**
   - New patterns discovered
   - Insights gained
   - Strategies that worked

2. **Store significant findings**
   - Use `store_quantum_insight` for important discoveries
   - Include metadata for context

3. **Update existing memories**
   - Refine understanding
   - Correct mistakes
   - Add new examples

4. **Organize memory structure**
   - Delete outdated entries
   - Consolidate related memories
   - Create directory structure as needed

## Best Practices

1. **Check memory FIRST**: Always start sessions by reviewing past work
2. **Store progressively**: Don't wait until the end to save insights
3. **Be selective**: Quality over quantity - store only valuable insights
4. **Include context**: Future you needs to understand why this mattered
5. **Use metadata**: Confidence, neurons used, VBC phase add richness
6. **Link memories**: Create connections between related knowledge
7. **Version understanding**: Track how your knowledge evolves
8. **Clean regularly**: Delete outdated or incorrect memories
9. **Search before storing**: Avoid duplicates
10. **Cite sources**: Include URLs or references where applicable

## Memory-Enhanced Workflows

### Problem-Solving with Memory
```
1. search_memories("[problem type]")
2. Review similar past solutions
3. Apply learned strategies
4. Adapt to current context
5. Store any new insights
```

### Learning with Memory
```
1. Research new topic
2. Process with quantum OS
3. Store in learning/ category
4. Link to related memories
5. Return later to reinforce
```

### Project Continuation
```
1. view_memory("/memories")
2. Search for project-related memories
3. Read last session's insights
4. Build upon previous work
5. Update memories with progress
```

This skill transforms ephemeral chat into persistent intelligence that grows over time.
