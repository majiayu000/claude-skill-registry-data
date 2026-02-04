---
name: orca-architecture
description: This skill should be used when the user asks about "Orca architecture", "knowledge graph design", "MCP server structure", "nugget storage", "telemetry design", "Orca refactoring", or is planning changes to Orca components. Provides decision capture workflows, bounded exploration patterns, and architecture discussion guidance.
---

# Orca Architecture Guidance

## On Activation

Load current Orca context from the knowledge graph:

```
search_nugs cue="boot" projects=["orca"]
```

This returns system state, recent decisions, active traps, and architecture patterns relevant to starting work on Orca.

For deeper exploration during the session:
- `search_nugs cue="pre-edit" file="<path>"` - before modifying a file
- `search_nugs cue="post-error"` - after encountering failures
- `search_nugs projects=["orca"] k="choice" query="<topic>"` - specific decisions

**Do not rely on hardcoded facts.** The KG is the source of truth.

## Working Principles

### Before Proposing Changes

1. **Ask why it exists this way**
   - Don't assume you understand the constraints
   - Components often exist for non-obvious reasons

2. **Search for decisions**
   - Use `orca:search_nugs` with terms like "decision", "choice", "architecture"
   - Stale nuggets exist - verify against code when uncertain

3. **Surface your unknowns**
   - Say "I don't know why X" rather than guessing
   - Ask clarifying questions before diving deep

### During Exploration

4. **Bound your investigation**
   - Max 10 tool calls before summarizing
   - State what you're looking for before searching
   - Don't follow rabbit holes

5. **Distinguish state from decisions**
   - State: current implementation details (goes stale)
   - Decision: reasoning and constraints (ages better)

### When Proposing

6. **Multiple options with tradeoffs**
   - Never propose a single solution
   - State assumptions explicitly
   - Include "what could go wrong"

7. **Argue against yourself**
   - After proposing, identify weaknesses
   - Ask what the user cares about most

8. **Smallest validating step**
   - What's the minimum we could build to test the direction?
   - Prefer reversible over irreversible

### Capturing Decisions

9. **Create nuggets for decisions, not just state**
   - Include WHY, not just WHAT
   - Include alternatives considered
   - Include constraints that shaped the choice
   - Tag with `project:orca`

## Common Pitfalls

### Forensic Spirals
Taking 50+ steps exploring without progress. When you catch yourself:
- Stop immediately
- Summarize what you know
- Ask a specific question

### Confident Wrongness
Proposing to remove or change components without understanding their purpose. Always ask "why does this exist?" before proposing removal.

### State vs Decision Confusion
Creating nuggets that capture implementation details rather than reasoning leads to stale information that misleads future sessions.

## Commands

- `/orca-arch <topic>` - Start structured architecture discussion
- Use the `orca-explorer` agent for bounded codebase exploration
