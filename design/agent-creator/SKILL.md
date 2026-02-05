---
name: agent-creator
description: Expert guidance for creating effective Claude Code agents (subagents). Use when users want to create a new agent, update an existing agent, or learn agent design best practices. Covers agent architecture, prompt engineering, tool selection, model choice, and common pitfalls. Integrates with skill-creator when agent needs accompanying skills.
---

# Agent Creator

Expert guidance for creating effective Claude Code agents following best practices.

## About Agents

Agents are specialized subprocesses that handle complex tasks autonomously with **isolated context windows**. They extend Claude's capabilities by providing focused expertise, specific tool access, and appropriate model selection for different task types.

### Agents vs Skills

| Aspect | Agents | Skills |
|--------|--------|--------|
| **Context** | Isolated context window | Shared with main conversation |
| **Purpose** | Autonomous task execution | Procedural knowledge & guidance |
| **Model** | Can specify different model | Uses current model |
| **Tools** | Can restrict/expand tool access | Uses available tools |
| **Use when** | Task needs isolation, different capabilities, or parallel execution | Task benefits from guidance staying in current context |

**Choose agents when:**
- Task benefits from isolated context (clean slate)
- Different model is optimal (haiku for speed, opus for reasoning)
- Tool access should be restricted for security
- Tasks can run in parallel

**Choose skills when:**
- Knowledge should stay in current conversation
- Guidance benefits from seeing full context
- No special tool/model requirements

## Agent Architecture

### File Structure

Agents are Markdown files with YAML frontmatter stored in:
- **Project agents**: `.claude/agents/` (highest priority)
- **User agents**: `~/.claude/agents/` (all projects)

### Configuration Format

```yaml
---
name: agent-identifier          # Required: lowercase, hyphens only
description: When and why...    # Required: PRIMARY TRIGGER MECHANISM
tools: Tool1, Tool2, Tool3      # Optional: restrict/specify tools
model: sonnet                   # Optional: sonnet, opus, haiku
skills: skill1, skill2          # Optional: auto-load skills
color: blue                     # Optional: UI indicator
---

[Agent system prompt here - Markdown instructions]
```

### Configuration Fields

| Field | Required | Details |
|-------|----------|---------|
| `name` | Yes | Lowercase letters and hyphens only (e.g., `code-reviewer`) |
| `description` | Yes | **PRIMARY TRIGGERING MECHANISM** - determines when agent is invoked |
| `tools` | No | Comma-separated list; omit to inherit all tools |
| `model` | No | `haiku` (fast), `sonnet` (balanced), `opus` (reasoning) |
| `skills` | No | Skills to auto-load when agent invokes |
| `color` | No | UI color indicator |

## Core Principles

### 1. Single-Purpose Focus

Create focused, single-responsibility agents:
- One clear job per agent
- Better composability and predictability
- Easier to debug and maintain

### 2. Description is Everything

The `description` field is the **PRIMARY TRIGGERING MECHANISM**. Include:
- WHAT the agent does
- WHEN to use it (trigger scenarios)
- Specific examples in angle brackets

**Pattern:**
```yaml
description: [Role/capability]. MUST BE USED for [specific scenarios]. [Additional context]. Examples: "[trigger phrase 1]", "[trigger phrase 2]"
```

### 3. Minimal Viable Toolset

Grant only necessary tools:
- **Read-only agents**: Glob, Grep, Read, LS
- **Analysis agents**: Add WebFetch, WebSearch
- **Planning agents**: Add Write, Edit, TodoWrite
- **Implementation agents**: Add Bash, Task

**Performance impact:**
- 3-5 tools: ~2-5k tokens
- 7-8 tools: ~7-10k tokens
- 15+ tools: 15-25k tokens (avoid)

### 4. Appropriate Model Selection

- **Haiku**: Fast, lightweight tasks (exploration, simple analysis)
- **Sonnet**: Balanced tasks (orchestration, validation, general work)
- **Opus**: Complex reasoning (planning, architecture, research)

## Agent Creation Process

### Step 1: Define Purpose

Before creating, answer:
1. What specific problem does this agent solve?
2. When should Claude automatically invoke this agent?
3. What makes this different from existing agents?
4. Does this need isolation, or would a skill suffice?

### Step 2: Design Description

Write a comprehensive description:
1. Start with role/capability statement
2. Add "MUST BE USED" or "use PROACTIVELY" for strong triggers
3. Include specific scenarios and trigger phrases
4. Add examples using XML tags for complex scenarios

### Step 3: Select Tools

Determine minimum tools needed:
1. List all operations the agent must perform
2. Map operations to specific tools
3. Remove any tools not strictly necessary
4. Consider security implications

### Step 4: Choose Model

Select based on task complexity:
- Simple/fast tasks → `haiku`
- Standard tasks → `sonnet` or omit (default)
- Complex reasoning → `opus`

### Step 5: Write System Prompt

Structure the prompt body:

```markdown
# [Role Title]

[One-sentence mission statement]

## Core Principles
- [Principle 1]: [Brief explanation]
- [Principle 2]: [Brief explanation]

## Responsibilities / Methodology
1. [Step/responsibility 1]
2. [Step/responsibility 2]

## [Workflow/Process] (if multi-step)
### Step 1: [Name]
[Instructions]

## Quality Standards / Output Format
[Checklists, criteria, format requirements]

## Constraints (if critical)
- [What agent MUST NOT do]
- [Boundaries and limitations]
```

### Step 6: Define Boundaries

Add explicit boundaries if agent has limited scope:

```markdown
## YOUR ROLE ENDS HERE

**CRITICAL BOUNDARY**: You are strictly a [role]. Once you have [completed work]:
- Your work is COMPLETE
- DO NOT [prohibited action 1]
- DO NOT [prohibited action 2]
```

## Prompt Engineering Best Practices

### Use Imperative Form
- "Identify issues" not "You should identify"
- "Generate report" not "The report should be generated"

### Strong Emphasis Markers
- **MUST**, **NEVER**, **ALWAYS**, **CRITICAL** for non-negotiables
- Bold or capitalize critical constraints
- Use strategically, not everywhere

### Include Examples
- Good vs Bad examples (Use checkmarks/X marks)
- Concrete user scenarios
- Before/after for transformations

### Be Specific, Not Vague
- "Test min/max values, zero, negative" not "test edge cases"
- "Check for SQL injection, XSS, path traversal" not "check security"
- Include decision criteria and thresholds

## Common Pitfalls to Avoid

### Over-Engineering
- Creating 15+ tool agents with 30k token prompts
- One mega-agent instead of composable focused agents
- Adding features "just in case"

**Solution:** Start lightweight (<3k tokens, 3-5 tools), expand based on need

### Vague Descriptions
- "Helps with coding" - too generic
- Missing "when to use" information
- No concrete trigger examples

**Solution:** Specific triggers, scenarios, and examples

### Tool Overload
- Giving all tools "just in case"
- Read-only agents with Write/Bash access
- Security risk and performance hit

**Solution:** Minimal viable toolset per agent purpose

### Missing Boundaries
- Agent scope creeps during execution
- No clear "done" criteria
- Agent attempts tasks outside its role

**Solution:** Explicit "YOUR ROLE ENDS HERE" section for bounded agents

### Ignoring Token Budget
- Verbose explanations Claude already knows
- Repeated information
- Unnecessary examples

**Solution:** Challenge each paragraph - "Does this justify its token cost?"

## Integration with Skills

When an agent needs domain expertise, use skills:

```yaml
---
name: specialized-agent
skills: domain-skill, helper-skill
---
```

**When to create an accompanying skill:**
- Agent needs substantial domain knowledge
- Knowledge is reusable across multiple agents
- Information would bloat agent prompt

**Use the skill-creator skill** to create accompanying skills:
```
Invoke skill: skill-creator
```

## Quality Checklist

Before finalizing an agent:

- [ ] **Name**: Lowercase with hyphens, descriptive
- [ ] **Description**: Includes WHAT, WHEN, and examples
- [ ] **Tools**: Minimal viable set for the task
- [ ] **Model**: Appropriate for task complexity
- [ ] **Prompt**: Follows structure (role → principles → methodology → standards)
- [ ] **Boundaries**: Clear scope and "done" criteria (if bounded)
- [ ] **Token efficiency**: <5k words for most agents
- [ ] **Examples**: Concrete scenarios in description or prompt
- [ ] **No overlap**: Doesn't duplicate existing agent functionality

## Example: Well-Designed Agent

```yaml
---
name: code-reviewer
description: Expert code review specialist. MUST BE USED when reviewing pull requests, code changes, or architecture decisions. Focuses on security, performance, maintainability, and best practices. Examples: "Review this PR", "Check this implementation for issues", "Review the changes in feature branch"
tools: Glob, Grep, Read, LS, WebSearch
model: sonnet
color: yellow
---

# Code Review Specialist

You are an expert code reviewer focused on identifying issues that impact security, performance, and maintainability.

## Review Priorities

1. **Security**: Injection vulnerabilities, auth issues, data exposure
2. **Performance**: O(n²) operations, memory leaks, unnecessary computation
3. **Maintainability**: Code clarity, naming, separation of concerns
4. **Best Practices**: Framework conventions, error handling, testing

## Review Process

1. Understand the change context (what problem is being solved)
2. Review for security vulnerabilities first
3. Check performance implications
4. Assess code quality and maintainability
5. Verify test coverage

## Output Format

For each issue found:
- **Severity**: Critical/High/Medium/Low
- **Location**: file:line
- **Issue**: Clear description
- **Recommendation**: Specific fix suggestion

## YOUR ROLE ENDS HERE

You are strictly a reviewer. After completing review:
- Your work is COMPLETE
- DO NOT implement fixes
- DO NOT modify code
```

## Resources

- See `references/prompt-patterns.md` for advanced prompt engineering patterns
- Use `skill-creator` skill when agent needs accompanying skills
