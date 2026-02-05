---
name: letta-agent-designer
description: Guide for designing effective Letta agents. This skill should be used when users need help choosing agent architectures, designing memory blocks, selecting models, or planning tool configurations for their Letta agents.
license: MIT
---

# Letta Agent Designer

This skill guides the process of designing effective Letta agents with appropriate architectures, memory configurations, and tool setups.

## When to Use This Skill

Use this skill when users are:
- Starting a new Letta agent project and need architectural guidance
- Deciding between letta_v1_agent and memgpt_v2_agent architectures
- Designing memory block structure for their use case
- Selecting appropriate models for their agent's purpose
- Planning which tools to attach to their agent

## Agent Design Process

### 1. Architecture Selection

Consult `references/architectures.md` for detailed comparison. Quick guidance:

**Use letta_v1_agent when:**
- Building new agents (recommended default as of October 2025)
- Need compatibility with reasoning models (GPT-5, Claude 4.5 Sonnet)
- Want simpler system prompts and direct message generation

**Use memgpt_v2_agent when:**
- Maintaining legacy agents
- Require specific tool patterns not yet supported in v1

### 2. Memory Block Design

Memory blocks structure the agent's persistent context. Follow these patterns:

**Core blocks for all agents:**
- `persona`: Agent identity and behavioral guidelines
- `human`: User-specific information and preferences

**Add custom blocks based on use case:**
- Customer support: `company_policies`, `product_knowledge`
- Coding assistant: `project_context`, `coding_standards`
- Personal assistant: `schedule`, `preferences`, `contacts`

For detailed memory patterns, consult `references/memory-patterns.md`.

**Key principle:** Keep blocks focused and purpose-specific. Agents can cross-reference between blocks.

### 3. Model Selection

Match model capabilities to agent requirements:

**For production agents:**
- GPT-4o or Claude 4.5 Sonnet for complex reasoning
- GPT-4o-mini for cost-efficient general tasks
- Claude Haiku 4.5 for fast, lightweight operations

**Avoid for production:**
- Small Ollama models (<7B parameters) - poor tool calling
- Gemini older than 2.5 Pro - function calling reliability issues

See `references/model-recommendations.md` for detailed guidance.

### 4. Tool Configuration

**Start minimal:** Attach only tools the agent will actively use. Common starting points:

- **Memory tools** (memory_insert, memory_replace, memory_rethink): Core for most agents
- **File system tools**: Auto-attached when folders are connected
- **Custom tools**: For domain-specific operations (databases, APIs, etc.)

**Tool Rules:** Use to enforce sequencing when needed (e.g., "always call search before answer")

Consult `references/tool-patterns.md` for common configurations.

## Validation Questions

Before finalizing agent design, verify:

1. Does the architecture match the model's capabilities?
2. Are memory blocks granular enough for effective updates?
3. Is the model appropriate for the expected workload and latency requirements?
4. Are tools necessary and properly configured?

## Next Steps

After design validation:
1. Create agent via ADE or API
2. Test with representative queries
3. Iterate on memory block structure and system instructions
4. Monitor tool usage patterns for optimization
