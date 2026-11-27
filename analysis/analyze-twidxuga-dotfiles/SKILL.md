---
name: analyze
description: Deep codebase analysis with parallel agents for patterns, dependencies, and architectural insights
disable-model-invocation: true
user-invocable: true
argument-hint: "<target or question>"
---

# Codebase Analysis

Perform a comprehensive codebase analysis for: $ARGUMENTS

## Process

1. **Parallel Discovery** — Launch multiple Agent(subagent_type="Explore") in parallel to:
   - Map file structure and key entry points
   - Search for patterns, dependencies, and conventions
   - Identify architectural boundaries and data flow

2. **Deep Analysis** — Based on discovery results:
   - Trace dependency chains and coupling
   - Identify potential issues (circular deps, dead code, inconsistencies)
   - Map the architecture (components, layers, boundaries)

3. **Recommendations** — Provide:
   - Architectural insights and trade-offs
   - Potential improvements with impact assessment
   - Risks and technical debt observations

## Rules

- Use at least 3 parallel Explore agents for initial discovery
- Read key files directly rather than guessing their contents
- Provide concrete file:line references, not vague observations
- Focus on what was asked — don't analyze everything if a specific target was given
