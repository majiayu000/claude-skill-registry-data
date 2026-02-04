---
name: sub-agent-creator
version: 0.2.1
description: Use PROACTIVELY when creating specialized Claude Code sub-agents for task delegation. Automates agent creation following Anthropic's official patterns with proper frontmatter, tool configuration, and system prompts. Generates domain-specific agents, proactive auto-triggering agents, and security-sensitive agents with limited tools. Not for modifying existing agents or general prompt engineering.
---

# Sub-Agent Creator

Automates creation of Claude Code sub-agents with proper configuration and proactive behavior.

## When to Use

**Trigger Phrases**:
- "create a sub-agent for [purpose]"
- "generate a new sub-agent"
- "set up a sub-agent to handle [task]"
- "make a proactive agent that [behavior]"

**Use Cases**:
- Domain-specific agents (code reviewer, debugger)
- Proactive agents that auto-trigger on patterns
- Security-sensitive agents with limited tools
- Team-shared project-level agents

## Workflow (6-Step Agent Creation Architect)

Follow this structured process for consistent, high-quality agents:

### Step 1: Extract Core Intent
Identify what the agent should accomplish:
- **Single responsibility**: What ONE thing does this agent do?
- **Trigger conditions**: When should Claude invoke this agent?
- **Success criteria**: How do we know the agent succeeded?

```markdown
Example:
- Intent: Review code for security vulnerabilities
- Trigger: Security-related requests, audit requests
- Success: Findings reported with confidence scores
```

### Step 2: Design Expert Persona
Define the expertise the agent embodies:
- **Domain expertise**: What knowledge domain? (security, testing, DevOps)
- **Perspective**: Cautious? Thorough? Fast? Pragmatic?
- **Communication style**: Terse? Educational? Actionable?

```markdown
Example:
- Persona: Senior security engineer with penetration testing background
- Perspective: Cautious, assumes hostile input
- Style: Concise findings with exploit paths
```

### Step 3: Architect Instructions
Structure capabilities and constraints:
- **PROHIBITED** operations first (what it CANNOT do)
- **ALLOWED** operations second (what it CAN do)
- **Output format** specification
- **Edge case handling**

```markdown
Structure order:
1. Prohibitions (safety rails)
2. Capabilities (what it does)
3. Output format (structured response)
4. Examples (when to use / when NOT)
```

### Step 4: Optimize for Token Efficiency
Reduce prompt size without losing clarity:
- Remove redundant phrases
- Use tables over prose where possible
- Consolidate similar concepts
- Target: <500 tokens for focused agents, <1000 for complex

### Step 5: Create Identifier
Generate the agent name:
- **Format**: lowercase, hyphenated, 2-4 words
- **Pattern**: `[domain]-[action]` or `[action]-[target]`
- **Examples**: `security-reviewer`, `test-generator`, `migration-validator`

### Step 6: Add Examples
Provide dual-example training:
```markdown
### When TO Use
<example>
user: "[request that should trigger]"
assistant: [Invokes agent]
<reasoning>Why this triggers</reasoning>
</example>

### When NOT to Use
<example>
user: "[request that should NOT trigger]"
assistant: [Does NOT invoke]
<reasoning>Why this doesn't trigger</reasoning>
</example>
```

---

## Quick Workflow (Simplified)

For straightforward agents, use this condensed process:

### Phase 1: Information Gathering
1. **Purpose**: What task/domain should agent specialize in?
2. **Name**: Auto-generate kebab-case from purpose
3. **Description**: Template: "Use PROACTIVELY to [action] when [condition]"
4. **Location**: Project (.claude/agents/) or User (~/.claude/agents/)

### Phase 2: Technical Configuration
1. **Model**: inherit (default), sonnet, opus, haiku
2. **Tools**: Read-only, Code ops, Execution, All, Custom
3. **System Prompt**: Role, approach, priorities, constraints

### Phase 3: File Generation
- Build YAML frontmatter
- Structure system prompt with templates
- Write to correct location

### Phase 4: Validation & Testing
- Validate YAML, tools, model
- Generate testing guidance
- List customization points

## Frontmatter Structure

```yaml
---
name: agent-name
version: 0.2.0
description: Use PROACTIVELY to [action] when [condition]
tools: Read, Grep, Glob  # Omit for all tools
model: sonnet             # Omit to inherit
---
```

### Version Tracking (Recommended)

*Pattern from: Claude Code version evolution*

Track changes to enable rollback and understand evolution:

```yaml
---
name: my-agent
version: 0.3.0
changelog:
  - "0.3.0: Added anti-pattern examples"
  - "0.2.0: Enhanced with dual-example pattern"
  - "0.1.0: Initial release"
---
```

**Versioning Guidelines**:
- **MAJOR** (1.0.0): Breaking changes to behavior or output
- **MINOR** (0.1.0): New features, enhanced capabilities
- **PATCH** (0.0.1): Bug fixes, documentation updates

Keep changelog in frontmatter for quick reference; detailed notes can go in separate CHANGELOG.md.

## Model Options

| Model | Use Case |
|-------|----------|
| inherit | Same as main conversation (default) |
| sonnet | Balanced performance |
| opus | Maximum capability |
| haiku | Fast/economical |

## Tool Access Patterns

| Pattern | Tools | Use Case |
|---------|-------|----------|
| Read-only | Read, Grep, Glob | Safe analysis |
| Code ops | Read, Edit, Write | Modifications |
| Execution | Bash | Running commands |
| All | * | Full access (cautious) |

## Installation Locations

| Location | Path | Use Case |
|----------|------|----------|
| Project | .claude/agents/ | Team-shared, versioned |
| User | ~/.claude/agents/ | Personal, all projects |

## Success Criteria

- [ ] Valid YAML frontmatter
- [ ] Agent file in correct location
- [ ] Description includes "PROACTIVELY"
- [ ] System prompt has role, approach, constraints
- [ ] Appropriate tool restrictions
- [ ] Clear testing instructions

## Security Best Practices

- Default to minimal tool access
- Require confirmation for "all tools"
- Validate tool list against available tools
- Warn about overly broad permissions

## Reference Materials

- `data/models.yaml` - Model options
- `data/tools.yaml` - Available tools
- `templates/agent-template.md` - Prompt structure
- `examples/` - Sample agents (code-reviewer, debugger)

## Testing Your Agent

### Manual Invocation
```
Use the [agent-name] sub-agent to [task]
```

### Proactive Trigger
Perform action matching the description to test auto-delegation.

### Debugging
```bash
# Check file
cat .claude/agents/[agent-name].md | head -10

# Verify location
ls .claude/agents/
```

---

**Version**: 0.1.0 | **Author**: Connor

**Docs**: https://docs.claude.com/en/docs/claude-code/sub-agents
