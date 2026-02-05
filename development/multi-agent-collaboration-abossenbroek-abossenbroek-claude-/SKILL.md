---
name: Multi-Agent Collaboration
description: >
  This skill should be used when designing agent coordination, implementing
  context handoffs, reducing context overhead, creating multi-agent workflows,
  optimizing agent communication, implementing progressive disclosure,
  selecting architectural patterns (hierarchical vs swarm), or debugging
  agent context issues. Provides SOTA patterns for multi-agent systems
  achieving 78%+ context reduction while maintaining analysis quality.
---

# Multi-Agent Collaboration

## Overview

State-of-the-art patterns for context-efficient multi-agent systems. These patterns enable complex agent workflows while minimizing token overhead through strategic context engineering.

## Research Foundation

- Google ADK: Context compilation pipelines and session management
- Anthropic: Multi-agent coordination and handoff protocols
- Progressive Disclosure: Agent-readable semantic interfaces
- LangGraph/CrewAI/AutoGen: Framework-specific orchestration patterns

## Pattern Selection Framework

| Pattern | Use When | Trade-offs |
|---------|----------|------------|
| **Hierarchical** | Clear decomposition, audit trails | Central bottleneck, sequential latency |
| **Swarm** | Parallel exploration, diverse perspectives | Coordination overhead, emergent behavior |
| **ReAct** | Dynamic adaptation, tool-heavy workflows | Myopic decisions, may meander |
| **Plan-Execute** | Clear sequence, predictability needed | Less adaptive, requires replanning |
| **Reflection** | Quality refinement, self-correction | Added latency, may reinforce errors |
| **Hybrid** | Multiple coordination needs | Implementation complexity |

For detailed YAML definitions and examples of each pattern, see `references/patterns.md`.

## The Four Laws of Context Management

### Law 1: Selective Projection

Pass only fields each agent needs, not full data structures.

```yaml
# BAD: Full snapshot everywhere
snapshot: {...20KB...}

# GOOD: Selective projection
context:
  mode: deep
  claims_analyzed: 15
  high_risk_count: 4
```

### Law 2: Tiered Context Fidelity

Define explicit tiers based on agent role:

| Tier | Description | Example Agent |
|------|-------------|---------------|
| FULL | Complete data | Initial analyzer |
| SELECTIVE | Relevant subset | Domain workers |
| FILTERED | Criteria-matched | Validators |
| MINIMAL | Mode + counts | Strategy/routing |
| METADATA | Scope stats only | Report synthesis |

### Law 3: Reference vs Embedding

For large data, pass reference instead of full structure:

```yaml
# Embedding (expensive)
raw_findings: [{...}, {...}, ...]  # 40+ items

# Reference (efficient)
findings_summary:
  total: 45
  by_severity: {CRITICAL: 3, HIGH: 12}
  # Agent fetches specific findings on-demand
```

### Law 4: Lazy Loading

Load data on-demand, not upfront:

```yaml
initial_context:
  scope: {item_count: 45}
  available_data:
    - name: findings
      fetch: "request by severity or ID"
```

For implementation details and patterns, see `references/context-engineering.md`.

## Standard Handoff Protocol

```yaml
handoff:
  from_agent: context-analyzer
  to_agent: attack-strategist
  context_level: MINIMAL

  payload:
    mode: deep
    analysis_summary:
      claim_count: 15
      high_risk_count: 4
      patterns: [pattern_1, pattern_2]

  expected_output:
    format: yaml
    schema: strategy_v1
```

## Severity-Based Batching

Reduce validation operations by routing based on priority:

```yaml
batching:
  CRITICAL: [all_validators]      # 4 agents
  HIGH: [checker, verifier]       # 2 agents
  MEDIUM: [checker]               # 1 agent
  LOW/INFO: []                    # Skip

# Result: 60-70% fewer operations
```

## Anti-Patterns to Avoid

1. **Snapshot Broadcasting** - Passing full context to every agent
2. **Defensive Over-inclusion** - "Maybe they need this" mentality
3. **Grounding Everything** - Validating low-priority items
4. **Embedding Large Lists** - Full arrays when counts suffice
5. **Repeated Context** - Same data passed multiple times in chain
6. **Verbose Outputs** - Over-explaining when concise suffices

## Progressive Disclosure for Agents

### Three-Level Loading

```yaml
level_1_always_loaded:
  - skill_name
  - skill_description
  tokens: ~100

level_2_on_trigger:
  - main_skill_body
  - core_patterns
  - quick_reference_tables
  tokens: ~2000

level_3_on_demand:
  - detailed_references
  - extended_examples
  - implementation_guides
  tokens: as_needed
```

## Guardrails and Validation

### Output Validation Pattern

```yaml
validation:
  hook: post_tool_use
  on_invalid:
    action: block_and_retry
    max_retries: 2
  on_valid:
    action: continue
```

### Context Tier Enforcement

Document what each agent does NOT receive:

```yaml
agent_context:
  receives:
    - analysis_summary
    - assigned_vectors

  not_provided:  # CRITICAL: Explicit exclusions
    - full_snapshot
    - other_agents_data
    - conversational_arc
```

## Metrics

Track these to validate optimization:

| Metric | Target |
|--------|--------|
| Total context passed | < 100KB |
| Redundancy ratio | < 0.1 |
| Validation efficiency | > 3:1 findings/operations |
| Tier compliance | 100% |

## Additional Resources

- `references/context-engineering.md` - Detailed context management patterns
- `references/patterns.md` - Architectural patterns with YAML definitions
- `references/examples.md` - Red-agent implementation examples
