---
name: subagent-development
description: Central authority for Claude Code subagents (sub-agents). Covers agent file format, YAML frontmatter, tool access configuration, model selection (inherit, sonnet, haiku, opus), automatic delegation, agent lifecycle, resumption, command-line usage (/agents), Agent SDK programmatic agents, priority resolution, and built-in agents (Plan subagent). Assists with creating agents, configuring agent tools, understanding agent behavior, and troubleshooting agent issues. Delegates 100% to docs-management skill for official documentation.
allowed-tools: Read, Glob, Grep, Skill
---

# Subagents Meta Skill

> ## 🚨 MANDATORY: Invoke docs-management First
>
> **STOP - Before providing ANY response about subagents/agents:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**
>
> ### Verification Checkpoint
>
> Before responding, verify:
>
> - [ ] Did I invoke docs-management skill?
> - [ ] Did official documentation load?
> - [ ] Is my response based EXCLUSIVELY on official docs?
>
> If ANY checkbox is unchecked, STOP and invoke docs-management first.

## Overview

Central authority for Claude Code subagents (also called sub-agents). This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** subagents, sub-agents, agents, agent file, agent YAML, agent frontmatter, agent tools, agent model, automatic delegation, agent lifecycle, agent resumption, /agents command, programmatic agents, agent SDK, built-in agents, Plan subagent, agent configuration

**Use this skill when:**

- Creating new agent definition files
- Configuring agent tool access
- Selecting agent models (inherit, sonnet, haiku, opus)
- Understanding automatic vs explicit agent invocation
- Working with agent resumption and lifecycle
- Using the /agents CLI command
- Integrating agents with Agent SDK
- Understanding priority resolution (project > CLI > user)
- Working with built-in agents (Plan subagent)
- Troubleshooting agent behavior

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Core Concepts

| Topic | Keywords |
| --- | --- |
| Overview | "subagents", "sub-agents", "agent overview" |
| File Format | "agent file format", "agent YAML frontmatter", "agent file structure" |
| File Locations | "agent file locations", "agent directories", "where to put agents" |

### Configuration

| Topic | Keywords |
| --- | --- |
| YAML Frontmatter | "agent YAML frontmatter", "agent configuration", "agent metadata" |
| Tool Access | "agent tools", "agent tool access", "allowed-tools agents" |
| Model Selection | "agent model selection", "inherit model", "sonnet haiku opus agents" |
| Permission Mode | "permissionMode", "agent permission mode", "acceptEdits", "bypassPermissions" |
| Skills Field | "agent skills field", "skills auto-load", "agent skills configuration" |
| Color (Undocumented) | "agent color", "subagent color", "agent UI color" |

### Behavior

| Topic | Keywords |
| --- | --- |
| Automatic Delegation | "automatic delegation", "agent automatic invocation" |
| Explicit Invocation | "explicit agent invocation", "manual agent call" |
| Lifecycle | "agent lifecycle", "agent execution", "agent completion" |
| Resumption | "agent resumption", "resume agent", "continue agent", "agentId", "resumable agents" |
| Plugin Agents | "plugin agents", "plugin-provided agents", "plugin subagents" |
| Chaining Agents | "chaining subagents", "chain agents", "agent orchestration" |
| Performance | "agent performance", "context efficiency", "agent latency", "parallel agents" |

### CLI and SDK

| Topic | Keywords |
| --- | --- |
| CLI Usage | "/agents command", "agents CLI", "list agents" |
| Agent SDK | "Agent SDK subagents", "programmatic agents", "SDK agent creation" |
| Priority Resolution | "agent priority resolution", "project CLI user agents" |

### Built-in Agents

| Topic | Keywords |
| --- | --- |
| General-purpose | "general-purpose subagent", "general purpose agent", "default subagent" |
| Plan Subagent | "Plan subagent", "planning agent", "implementation planning" |
| Explore Subagent | "Explore subagent", "explore agent", "codebase exploration", "read-only agent" |
| Thoroughness Levels | "thoroughness levels", "quick medium thorough", "exploration depth" |

## Official YAML Frontmatter Reference

**Source:** `doc_id: code-claude-com-docs-en-sub-agents` section `#configuration-fields`

These are the officially documented YAML frontmatter fields for subagent definition files:

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | Natural language description of the subagent's purpose |
| `tools` | No | Comma-separated list of specific tools. If omitted, inherits all tools from main thread |
| `model` | No | Model alias (`sonnet`, `opus`, `haiku`) or `'inherit'` to use main conversation's model |
| `permissionMode` | No | Valid values: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated list of skill names to auto-load when subagent starts |

**Important:** The `color` property documented below is NOT in official Claude Code documentation.

## Color Property (Undocumented)

The `color` property is an undocumented feature that sets the UI color for subagents. It is NOT in official Claude Code documentation and may change without notice.

**Available Values:** red, blue, green, yellow, purple, orange, pink, cyan

**Placement:** Typically placed after `model` or at the bottom of YAML frontmatter.

**Example:**

```yaml
---
name: my-agent
description: Description of what this agent does
tools: Read, Grep, Glob
model: haiku
color: blue
---
```

**Warning:** As an undocumented feature, this property:

- May not work in all Claude Code versions
- May be removed or changed without notice
- Should not be relied upon for critical functionality

## Repository Color Standard

This repository uses a semantic color categorization for subagents to provide visual consistency:

### Category Assignments

| Category | Color | Purpose | Agents |
| --- | --- | --- | --- |
| **Documentation/Meta** | purple | Documentation, auditing, meta-skills | docs-researcher, docs-validator, skill-auditor |
| **Code Quality** | blue | Code analysis, review, debugging, testing | code-reviewer, codebase-analyst, debugger, test-generator |
| **Research** | green | Research, information gathering, web content | mcp-research, platform-docs-researcher, web-research |

### Reserved Colors (Future Use)

| Color | Reserved For |
| --- | --- |
| orange | Generation/Creation agents |
| red | Critical/Error handling agents |
| yellow | Warning/Attention agents |
| pink | User-facing/Communication agents |
| cyan | Utility agents |

### When to Assign Colors

When creating new agents for this repository:

1. **Identify the agent's primary purpose** (documentation, code quality, research, etc.)
2. **Match to existing category** if possible
3. **Use reserved colors** only for new categories that match the reserved purpose
4. **Document new categories** if creating a genuinely new type

## Quick Decision Tree

**What do you want to do?**

1. **Create a new agent** -> Query docs-management: "agent file format", "agent YAML frontmatter"
2. **Configure agent tools** -> Query docs-management: "agent tools", "allowed-tools agents"
3. **Select agent model** -> Query docs-management: "agent model selection", "inherit sonnet haiku opus"
4. **Configure permissionMode** -> Query docs-management: "permissionMode", "agent permission mode"
5. **Auto-load skills in agent** -> Query docs-management: "agent skills field", "skills auto-load"
6. **Understand automatic delegation** -> Query docs-management: "automatic delegation agents"
7. **Resume an agent (agentId)** -> Query docs-management: "agent resumption", "agentId", "resumable agents"
8. **Use /agents CLI** -> Query docs-management: "/agents command", "agents CLI"
9. **Programmatic agents (SDK)** -> Query docs-management: "Agent SDK subagents"
10. **Understand priority resolution** -> Query docs-management: "agent priority resolution"
11. **Work with General-purpose agent** -> Query docs-management: "general-purpose subagent"
12. **Work with Plan subagent** -> Query docs-management: "Plan subagent", "planning agent"
13. **Work with Explore subagent** -> Query docs-management: "Explore subagent", "thoroughness levels"
14. **Understand plugin agents** -> Query docs-management: "plugin agents", "plugin-provided agents"
15. **Chain multiple agents** -> Query docs-management: "chaining subagents", "agent orchestration"
16. **Optimize agent performance** -> Query docs-management: "agent performance", "parallel agents"
17. **Troubleshoot agent issues** -> Query docs-management: "agent troubleshooting" + specific issue keywords
18. **Add color to agent (undocumented)** -> See "Color Property (Undocumented)" section above
19. **Choose color for new agent** -> See "Repository Color Standard" section above

## Topic Coverage

### Agent Files

- File format and structure
- YAML frontmatter fields (name, description, tools, model)
- File locations (project, CLI, user directories)
- Naming conventions

### Tool Configuration

- Specifying allowed tools
- Tool access inheritance
- Restricting dangerous tools
- MCP tools in agents

### Model Selection

- Model options: inherit, sonnet, haiku, opus
- When to use each model
- Cost and performance considerations
- Inheritance from parent context

### Invocation Patterns

- Automatic delegation (description matching)
- Explicit invocation via Task tool
- Agent discovery and selection
- Priority resolution order

### Lifecycle Management

- Agent execution flow
- Context isolation
- Result reporting
- Error handling

### Resumption

- Resuming existing agents
- Context preservation
- When to resume vs create new
- Resume parameter usage

### CLI Integration

- /agents command
- Listing available agents
- Agent status and management
- CLI-defined agents

### Agent SDK Integration

- Programmatic agent creation
- SDK patterns for subagents
- Custom agent implementations
- Advanced agent workflows

### Default Agent Types

- **General-purpose subagent**: Complex multi-step tasks, autonomous execution
- **Plan subagent**: Implementation planning, architectural decisions
- **Explore subagent**: Codebase exploration, read-only research
- Thoroughness levels (quick, medium, very thorough) for Explore agent
- Default agent behaviors and when to use each
- Customizing built-in agent behavior

### Plugin Agents

- Plugin-provided agents
- Plugin agent discovery and usage
- Plugin agent configuration

### Performance Considerations

- Parallel agent execution
- Context efficiency and token usage
- Agent latency optimization
- When to use subagents vs direct tools

## Test Scenarios

These scenarios should activate this skill:

1. **Direct activation**: "Use the subagent-development skill to help me create an agent"
2. **Configuration question**: "How do I restrict tools for my subagent?"
3. **Built-in agent question**: "What is the Explore subagent and how do I use it?"
4. **Troubleshooting**: "My agent isn't being invoked automatically"
5. **SDK question**: "How do I define agents programmatically in the Agent SDK?"

## Related Skills

| Skill | Relationship |
| --- | --- |
| **docs-management** | Primary delegation target (100%) - all official documentation |
| **agent-sdk-development** | Agent SDK-specific guidance for programmatic agents |
| **skill-development** | Skills can be auto-loaded by agents via skills field |
| **current-date** | For audit timestamps and verification dates |

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "How do I create an agent?"

1. Invoke docs-management skill
2. Use keywords: "agent file format", "agent YAML frontmatter"
3. Load official documentation
4. Provide guidance based EXCLUSIVELY on official docs
```

### Multi-Topic Query Pattern

```text
User asks: "I want to create an agent with restricted tools that uses Haiku"

1. Invoke docs-management skill with multiple queries:
   - "agent file format", "agent YAML frontmatter"
   - "agent tools", "allowed-tools agents"
   - "agent model selection", "haiku agents"
2. Synthesize guidance from official documentation
```

### Troubleshooting Pattern

```text
User reports: "My agent isn't being invoked automatically"

1. Invoke docs-management skill
2. Use keywords: "automatic delegation agents", "agent description"
3. Check official docs for automatic invocation requirements
4. Guide user based on official troubleshooting steps
```

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Agent not found | "agent file locations", "agent directories" |
| Agent not auto-invoked | "automatic delegation", "agent description matching" |
| Wrong model used | "agent model selection", "inherit model" |
| Tools not available | "agent tools", "allowed-tools agents" |
| Resumption not working | "agent resumption", "resume agent" |
| Priority conflicts | "agent priority resolution", "project CLI user" |

## Repository-Specific Notes

This repository uses subagents for:

- **Explore agents**: Codebase exploration and research
- **Plan agents**: Implementation planning
- **General-purpose agents**: Complex multi-step tasks

When creating agents for this repository, follow patterns in `.claude/settings.json` and existing agent configurations.

## Related Guidance

For comprehensive subagent usage guidance beyond configuration:

- **When to use subagents**: See `.claude/memory/operational-rules.md` → "Agent Usage Principles"
- **Parallelization strategies**: See `.claude/memory/performance-quick-start.md` → "Strategy 1: Parallelization"
- **Context preservation patterns**: See `.claude/memory/operational-rules.md` → "Agent Communication Pattern"
- **Proactive delegation rule**: See `CLAUDE.md` Quick Reference → "PROACTIVE DELEGATION"

## Auditing Agents

This skill provides the validation criteria used by the `agent-auditor` agent for formal audits.

### Audit Resources

| Resource | Location | Purpose |
| --- | --- | --- |
| Validation Checklist | `references/validation-checklist.md` | Pre-creation verification checklist |
| Scoring Rubric | `references/validation-checklist.md#audit-scoring-rubric` | Formal audit scoring criteria |
| Undocumented Features | `references/undocumented-features.md` | Color, permissionMode, skills field details |

### Scoring Categories

| Category | Points | Key Criteria |
| --- | --- | --- |
| Name Field | 20 | Lowercase, hyphens, max 64 chars, no reserved words |
| Description Field | 25 | Third person, delegation triggers, when-to-use guidance |
| Tools Configuration | 20 | Appropriate restrictions, not over/under restricted |
| Model Selection | 15 | Appropriate for task complexity |
| Additional Fields | 20 | Color, skills, permissionMode correctly configured |

**Thresholds:** 85+ = PASS, 70-84 = PASS WITH WARNINGS, <70 = FAIL

### Related Agent

The `agent-auditor` agent (Haiku model) performs formal audits using this skill:

- Auto-loads this skill via `skills: subagent-development`
- Uses validation checklist and scoring rubric
- Checks both official and undocumented features
- Generates structured audit reports
- Invoked by `/audit-agents` command

### External Technology Validation

When auditing agents that use external technologies (scripts, packages, runtimes), the auditor MUST validate claims using MCP servers before flagging findings.

**Technologies Requiring MCP Validation:**

- .NET/C# scripts: Validate with microsoft-learn + perplexity
- Node.js/npm packages: Validate with context7 + perplexity
- Python scripts/packages: Validate with context7 + perplexity
- Shell scripts: Validate with perplexity
- Any version-specific claims: ALWAYS validate with perplexity

**Validation Rule:**

Never flag a technology usage as incorrect without first:

1. Querying appropriate MCP server(s) for current documentation
2. Verifying with perplexity for recent changes (especially .NET 10+)
3. Documenting MCP sources in the finding

**Stale Data Warning:**

- microsoft-learn can return cached/outdated documentation
- ALWAYS pair microsoft-learn with perplexity for version verification
- Trust perplexity for version numbers and recently-released features

## References

**Official Documentation (via docs-management skill):**

- Primary: "sub-agents" documentation
- Related: "Agent SDK", "Task tool", "model selection"

**Repository-Specific:**

- Agent configurations: `.claude/settings.json`
- Performance guidance: `.claude/memory/performance-quick-start.md`
- Operational rules: `.claude/memory/operational-rules.md` (Agent Usage Principles section)

## Version History

- **v1.2.0** (2025-11-27): Color property documentation
  - Added "Official YAML Frontmatter Reference" section with source reference to docs-management
  - Added "Color Property (Undocumented)" section documenting available colors
  - Added "Repository Color Standard" section with semantic color categories
  - Added color keyword to Configuration registry
  - Expanded Quick Decision Tree (19 entries, up from 17) with color entries
- **v1.1.0** (2025-11-27): Audit and enhancement
  - Added missing keyword registry entries (permissionMode, skills field, plugin agents, chaining, performance)
  - Expanded Built-in Agents section (General-purpose, Plan, Explore, thoroughness levels)
  - Added Test Scenarios section (5 scenarios)
  - Added Related Skills section
  - Expanded Quick Decision Tree (17 entries, up from 10)
  - Added Plugin Agents and Performance Considerations to Topic Coverage
  - Added Token Budget statement
- **v1.0.0** (2025-11-26): Initial release
  - Pure delegation architecture
  - Comprehensive keyword registry
  - Quick decision tree
  - Topic coverage for all subagent features
  - Troubleshooting quick reference

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
