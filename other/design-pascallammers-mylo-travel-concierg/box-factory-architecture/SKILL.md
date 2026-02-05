---
name: box-factory-architecture
description: Guidance for using Claude Code component architecture and choosing between agents, skills, commands, and hooks. Helps decide which component type fits a use case, understand delegation and isolation, debug cross-component issues, and design cohesive plugin architectures. Use when choosing component types, designing plugins with multiple components, debugging delegation failures, asking about component interaction patterns, or creating Box Factory-compliant components.
---

# Box Factory Architecture

This meta-skill teaches the Claude Code component and ecosystem architecture - how components interact, when to use each type, and how to design cohesive multi-component solutions. **This applies to both Main Claude (choosing what to create) and sub-agents (understanding their role).**

## Fundamentals

Four foundational principles underpin all Claude Code component design:

### Isolation Model

Components operate independently, and have limited access to the user or each other.  

These are our RULES (based on spec & best practices):

- Only Main Claude has user access
- Sub-agents:
  - CANNOT: ask the user questions, see conversation history, reference Skill files by name
  - CAN: use tools, load skills, reference Skill content by subject
- Skills:
  - CANNOT: reference any other component (single exception: Box Factory skills can reference Box Factory Architecture as a prerequisite)
  - CAN: Provide information and instruction
- Commands:
  - CANNOT: execute logic, access user directly
  - CAN: trigger Sub-agents, reference Skills

### Return-Based Delegation  

Sub-agents return complete results. No mid-execution interaction - agent must have everything upfront.

### Progressive Disclosure

Load knowledge only when relevant (this preserves context and saves tokens). Use Skills tosolve selective context loading.

### Knowledge Delta Filter

Document only what Claude doesn't know. Skip base knowledge; include user-specific delta.

**Design test:** If your sub-agent needs to ask questions mid-execution, redesign the delegation pattern.

**Deep dive:** [Core Architectural Concepts](./principles/core-architecture.md) - Diagrams, design implications, common misconceptions. **Traverse when:** debugging delegation issues, need to understand WHY architecture works this way. **Skip when:** table above answers your question.

**Deep dive:** [Knowledge Delta Filter](./principles/knowledge-delta-filter.md) - Decision framework for content inclusion, examples across component types. **Traverse when:** writing any component content, reviewing for bloat, unsure what to include/exclude. **Skip when:** already know the delta principle, content is clearly user-specific.

## Instructions

1. Select a workflow based on your needs from [Workflow Selection](#workflow-selection)

**Claude Code changes rapidly and is post-training knowledge.** Fetch the [official documentation](#claude-code-official-documentation) when designing components to ensure current specifications.

## Workflow Selection

| If you need to...                                                   | Go to...                                                                                   |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Choose a component type (skill vs agent vs command vs hook)         | [Which Component Should I Choose](#which-component-should-i-choose)                        |
| Debug delegation issues (agent not receiving data, calls failing)   | [Component Communication](#component-communication-and-delegation)                         |
| Design multi-component workflows (command→agent→skill chains)       | [Design Patterns](#design-patterns-in-claude-code-components)                              |
| Understand isolation model (why agents can't ask questions)         | [Fundamentals](#fundamentals)                                                              |
| See reference implementations (complete plugin ecosystems)          | [Example Ecosystems](#example-component-ecosystems)                                        |
| Determine file paths for new components (project vs user vs plugin) | [Component Paths](./components/component-paths.md)                                         |
| Write documentation for components (skills, agents, READMEs)        | [Building Blocks](#building-blocks)                                                        |
| Get oriented / unsure where to start                                | [Fundamentals](#fundamentals) then [Component Selection](#which-component-should-i-choose) |

## Design Patterns in Claude Code Components

Most common patterns used in multi-component workflows:

| Pattern                                     | Workflow                                  |
| ------------------------------------------- | ----------------------------------------- |
| Simple series of steps or tool call         | `User` -> `Command`                       |
| Complex agent flow triggered by command     | `User` -> `Command` -> `Agent`            |
| Complex agent flow backed by knowledge base | `User` -> `Command` -> `Agent` -> `Skill` |

**Deep dive:** [Interaction Patterns](./components/interaction-patterns.md) - 5 detailed patterns (Command→Agent, Agent→Skill, nested delegation, Hook+Agent, shared skills), scope anti-patterns. **Traverse when:** designing multi-component workflow, debugging component interactions, need pattern examples. **Skip when:** simple single-component task, workflow table covers your use case.

## Component Communication and Delegation

Quick reference for what each component can do:

| Component                | Can                                    | Cannot                                    |
| ------------------------ | -------------------------------------- | ----------------------------------------- |
| Main Claude              | Ask user questions, delegate to agents | N/A (full access)                         |
| Sub-agent (aka subagent) | Use tools, load skills, return results | Ask questions, see conversation history   |
| Command                  | Trigger agents, expand to prompts      | Execute logic directly, access user       |
| Skill                    | Provide guidance when loaded           | Execute code, call tools, trigger actions |
| Hook                     | Run scripts, block/modify tool calls   | Ask questions, use judgment               |
| MCP Server               | Provide custom tools                   | Access conversation, trigger unprompted   |

**Deep dive:** [Component Communication & Delegation](./components/communication-and-delegation.md) - CAN/CANNOT lists for each component type with examples and edge cases. **Traverse when:** need detailed interaction rules, debugging "why can't my agent do X". **Skip when:** table above answers the question.

## Which Component Should I Choose

Users can customize Claude Code using components broken into roughly three categories.

### Components used by Claude

| Component Type | When to Use                                       | Avoid When (use instead)                              |
| -------------- | ------------------------------------------------- | ----------------------------------------------------- |
| `Sub-agent`    | Complex logic, autonomous delegation              | Guidance only (Skill), simple repeatable (Command)    |
| `Skill`        | Substantial interpretive guidance across contexts | Doing work (Agent), brief context \<20 lines (Memory) |
| `Command`      | Simple repeatable actions, explicit user control  | Complex logic (Agent), knowledge only (Skill)         |
| `Memory`       | Project knowledge, behavior shaping               | Substantial guidance (Skill), enforcement (Hook)      |
| `MCP server`   | Custom tool integrations, specialized transports  | Standard tools suffice (use built-in tools)           |

### Components for the UX of the User

| Component Type | When to Use                                 | Avoid When (use instead)                        |
| -------------- | ------------------------------------------- | ----------------------------------------------- |
| `Hook`         | Guaranteed enforcement, simple rules        | Judgment calls (Agent), guidance (Skill)        |
| `Status Line`  | Custom session metadata display             | Enforcement needed (Hook), any Claude action    |
| `Output Style` | Custom response formats, structured outputs | Logic changes (Agent/Skill), enforcement (Hook) |

### Distribution Wrappers for Components

| Component Type | When to Use                            | Avoid When (use instead)                  |
| -------------- | -------------------------------------- | ----------------------------------------- |
| `Plugin`       | Bundling multiple components for reuse | Single-project use (project components)   |
| `Marketplace`  | Discovering and sharing plugins        | Private/internal plugins (direct install) |

**Deep dive:** [Choosing the Right Component](./components/choosing-the-right-component.md) - Full decision framework with KEY CHARACTERISTIC, CHOOSE IF, DO NOT CHOOSE IF, and Example User Requests for each component. **Traverse when:** ambiguous component choice, need to map user intent phrases to component type, edge cases not covered by summary. **Skip when:** summary tables clearly answer the question.

## Building Blocks

Reusable documentation patterns that apply across all component types:

| Pattern                                                           | Purpose                                                    |
| ----------------------------------------------------------------- | ---------------------------------------------------------- |
| [Navigation Tables](./building-blocks/navigation-tables.md)       | Routing tables for progressive discovery                   |
| [Decision Frameworks](./building-blocks/decision-frameworks.md)   | Structured formats for documenting choices between options |
| [Reference Sections](./building-blocks/reference-sections.md)     | At-a-glance content design for the happy path              |
| [Deep Dive Links](./building-blocks/deep-dive-links.md)           | Cross-reference format with traverse/skip guidance         |
| [Quality Checklist](./building-blocks/quality-checklist.md)       | Checkbox validation at end of documents                    |
| [Anti-Pattern Catalog](./building-blocks/anti-pattern-catalog.md) | Structure for documenting common mistakes                  |

Use these patterns when writing documentation for any component type (skills, agents, commands, READMEs).

## Claude Code Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when designing components to ensure current specifications:

- <https://code.claude.com/docs/en/sub-agents> - Agent architecture and isolation model
- <https://code.claude.com/docs/en/slash-commands> - Command structure and triggering
- <https://code.claude.com/docs/en/hooks> - Hook lifecycle and execution
- <https://code.claude.com/docs/en/plugins> - Plugin packaging and distribution
- <https://code.claude.com/docs/en/mcp> - MCP server configuration and transports
- <https://code.claude.com/docs/en/memory> - CLAUDE.md, rules, and project memory
- <https://code.claude.com/docs/en/skills> - Skill definition and loading

## Example Component Ecosystems

A very simple ecosystem:

```markdown
CLAUDE.md    # Basic project memory.  Indicates to use code-reviewer agent when reviewing code.
commands/review-code.md    # Command that triggers code review by delegating to code-reviewer agent.
agents/code-reviewer.md    # Code review agent, looks up guidelines from skill.
skills/code-review-guidelines.md    # Skill with guidance on code review best practices.
```

**Deep dive:** [Example Component Ecosystems](./examples/example-component-ecosystems.md) - 3 complete ecosystems (Testing, Documentation, Code Quality) with architecture diagrams and interaction flows. **Traverse when:** need reference implementation, learning multi-component patterns, planning similar ecosystem. **Skip when:** understanding single component, simple use case.

## Anti-Patterns

Common architecture mistakes. See linked design skills for detailed guidance.

| Pitfall                    | Symptom                                              | Fix                                                              | Details                                                 |
| -------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| User interaction in agents | Agent prompt contains "ask the user", "confirm with" | Remove - agents are isolated, return complete results            | [sub-agent-design](../sub-agent-design/SKILL.md)        |
| Wrong granularity          | Agent for simple task, skill for 10-line guidance    | Match complexity: Command < Agent < Skill based on scope         | [Component Selection](#which-component-should-i-choose) |
| Missing tool permissions   | Agent fails silently or can't complete task          | Add required tools (esp. Skill tool if loading skills)           | [sub-agent-design](../sub-agent-design/SKILL.md)        |
| Vague agent descriptions   | Main Claude doesn't delegate when it should          | Use strong triggers: "MUST BE USED when...", "ALWAYS use for..." | [sub-agent-design](../sub-agent-design/SKILL.md)        |
| Over-engineering           | Plugin for single-project use                        | Use project-level components until reuse is proven               | [plugin-design](../plugin-design/SKILL.md)              |

## Quality Checklist

Before finalizing component architecture:

**Fundamentals:**

- [ ] Agents have no user interaction language ("ask", "confirm", "clarify")
- [ ] Agents return complete results (not partial or interactive)
- [ ] Progressive disclosure applied (skills for substantial guidance, memory for brief)

**Component Selection:**

- [ ] Component type matches task complexity (see [Which Component Should I Choose](#which-component-should-i-choose))
- [ ] "Avoid When" conditions checked for each component

**Tool Permissions:**

- [ ] Agent tools match responsibilities (Read-only for reviewers, Write for creators)
- [ ] Skill tool included if agent loads skills
- [ ] Task tool included if agent delegates to sub-agents
