---
name: creating-subagents
description: Expert knowledge on creating Claude Code subagents. Use when designing or creating subagent .md files, understanding subagent structure, tool restrictions, or model selection.
allowed-tools: Read, Grep, Glob
---

# Creating Subagents

This Skill provides comprehensive knowledge about creating effective subagents in Claude Code.

## What Are Subagents?

Subagents are specialized AI assistants that Claude Code can delegate tasks to. Each subagent:
- Has a specific purpose and expertise area
- Uses its own context window separate from the main conversation
- Can be configured with specific tools it's allowed to use
- Includes a custom system prompt that guides its behavior

**Critical Insight - The Primary Value**: While specialization is important, the **primary value** of subagents is **token context isolation**. Subagents allow the main conversation to delegate "token-heavy" or "noisy" tasks (like extensive research, analyzing large codebases, or processing logs) to a separate context window. This keeps the main orchestrator's context clean and focused, enabling much longer-running and more complex workflows.

Think of subagents as allowing the main agent to "go on side quests" without polluting its main context with unnecessary details.

## Mental Model: Orchestrator and Specialists

The most effective way to think about subagents is as a distributed team:

**Main Conversation = Project Manager / Orchestrator**
- Stays "token-light" - focuses on coordination, not execution
- Delegates clearly defined tasks to specialists
- Aggregates results from subagents
- Makes high-level decisions
- Writes the "final report" to the user

**Subagents = Specialists**
- Handle specific, token-intensive tasks
- Work in isolated context windows (their own "side quests")
- Return structured results to the orchestrator
- Examples: code reviewer, research analyst, test runner, database engineer

**The Token Budget Strategy**:
- Main thread has limited context window
- Many tasks are "token-heavy" (large file analysis, extensive research)
- Executing these in main thread "pollutes" the orchestrator's context
- Subagents solve this by isolating the noise
- Result: Main thread can handle much longer, more complex workflows

## File Structure

**Location**: `.claude/agents/{name}.md`

**Format**:
```yaml
---
name: agent-name
description: When to invoke this agent
tools: Read, Write, Edit  # Optional
model: sonnet             # Optional
---

# System Prompt

Agent's instructions, approach, and constraints.
```

## Creating and Managing Subagents

### The /agents Command (Recommended)

The `/agents` command is now the **preferred way** to create and manage subagents (as of October 2025).

**Why Use /agents:**
- Interactive guided creation with prompts
- Lists all available tools including MCP server tools
- Easier to discover which tools to grant
- Quick prototyping without manual YAML editing

**Usage:**
```
/agents create    # Interactive creation
/agents list      # Show all subagents
/agents edit      # Modify existing subagent
/agents delete    # Remove subagent
```

**Manual File Editing:**
You can still manually create `.claude/agents/{name}.md` files for:
- Version control (git tracking)
- Templating and automation
- Fine-grained control

Both approaches create the same .md files - choose based on your workflow.

## YAML Frontmatter Fields

### Required Fields

**name** (string)
- Unique identifier for the subagent
- Use lowercase letters and hyphens only
- Examples: `code-reviewer`, `test-runner`, `backend-engineer`
- ❌ Avoid: Spaces, underscores, capitals

**description** (string)
- Natural language description of the subagent's purpose
- Must include when/why to invoke the agent
- Should contain keywords users would mention
- Used by Claude to decide when to delegate tasks

### Optional Fields

**tools** (comma-separated string)
- Specific tools this subagent can use
- If omitted, inherits all tools from main thread
- Examples: `Read, Write, Edit, Bash, Grep, Glob`
- Use principle of least privilege

**model** (string)
- AI model for this subagent to use
- Options: `sonnet`, `opus`, `haiku`, `inherit`
- `inherit` - Use same model as main conversation
- If omitted, uses default subagent model (sonnet)

## Writing Effective Descriptions

The description is **critical** for automatic invocation. Claude reads descriptions to decide which subagent to use.

### Good Descriptions

```yaml
# Specific + Proactive Trigger
description: Expert code reviewer. Use PROACTIVELY after code changes to review quality, security, and maintainability.

# Clear Purpose + When to Use
description: Debugging specialist for errors, test failures, and unexpected behavior. Use when encountering any issues or when tests fail.

# Multiple Triggers
description: Backend development specialist that enforces KISS, DRY, and YAGNI. Use when creating or modifying Python/FastAPI code, database models, API endpoints, or backend logic.
```

### Bad Descriptions

```yaml
# Too vague
description: Helps with code

# Missing trigger
description: Reviews code for quality

# No "when to use"
description: Testing expert
```

### Key Elements

1. **Role** - What kind of expert is this?
2. **Purpose** - What specific tasks?
3. **Triggers** - When should Claude invoke it?
4. **Keywords** - Terms users would mention

### Proactive Invocation

Add these phrases to encourage automatic invocation:
- "Use PROACTIVELY"
- "MUST BE USED"
- "Use immediately after"
- "Use automatically when"

Example:
```yaml
description: Test coverage guardian. Use PROACTIVELY to remind about tests when code changes are made. MUST BE USED when implementing new features.
```

## System Prompt Structure

The system prompt (Markdown content after frontmatter) defines the subagent's behavior.

### Essential Sections

```markdown
# Agent Name

Brief overview of role and capabilities.

## Your Role

What this agent does and its expertise.

## When Invoked

Specific situations that trigger this agent.

## Your Process

Step-by-step workflow:
1. First action
2. Second action
3. Final action

## Output Format (CRITICAL)

**Why Structured Output Matters**:
Your output must be machine-readable so the orchestrator can parse and aggregate results.

Return results in JSON format:
{
  "summary": "Brief overview of findings",
  "issues": [
    {"severity": "high", "location": "file.py:42", "description": "...", "suggestion": "..."}
  ],
  "recommendations": ["...", "..."],
  "metrics": {"files_reviewed": 5, "issues_found": 3}
}

This structured format makes your output reliable and actionable for the orchestrator.

## Best Practices

Guidelines and principles to follow.

## Red Flags

What to watch for or challenge.
```

**Key Addition: Output Format**
The most important best practice for subagents is defining a **structured output format** (typically JSON). This ensures:
- Orchestrator can reliably parse subagent results
- Results can be aggregated across multiple subagent calls
- No ambiguity in how to interpret the output
- Enables automated decision-making based on subagent output

For detailed examples of subagents with structured output, see [examples.md](examples.md).

### Quick Example: Structured Output

```yaml
---
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Code Reviewer

## Your Process
1. Run `git diff` to see changes
2. Review systematically (readability, quality, security)
3. Return results as JSON

## Output Format

```json
{
  "summary": "Reviewed 3 files with 2 critical issues",
  "files_reviewed": ["src/auth.py", "src/api.py"],
  "critical_issues": [{"file": "...", "issue": "...", "recommendation": "..."}],
  "warnings": [...],
  "suggestions": [...]
}
```
```

**See [examples.md](examples.md) for the complete code reviewer example with full checklists and detailed output format.**

## Tool Restrictions

Use the `tools` field to limit what the subagent can do (principle of least privilege).

### Quick Reference

```yaml
# Read-only (analysis, review)
tools: Read, Grep, Glob

# Limited write (code generation)
tools: Read, Write, Edit, Grep, Glob

# Selective bash (specific commands only)
tools: Read, Bash(git:*), Bash(pytest:*)

# Full access (omit tools field)
# Inherits all tools from main conversation
```

**See [reference.md](reference.md) for detailed tool restriction patterns, security best practices, and when to use each type.**

## Model Selection

Choose the right model based on task complexity and requirements.

### Quick Reference

```yaml
model: haiku    # Fast, cheap (simple tasks, file search)
model: sonnet   # Balanced (default, most tasks)
model: opus     # Powerful (critical decisions, security)
model: inherit  # Match main conversation
```

**Decision Tree**:
- Simple/pattern-based → haiku
- Mission-critical/security → opus
- Default choice → sonnet

**See [reference.md](reference.md) for detailed model characteristics, use cases, and cost/speed trade-offs.**

## Common Patterns

Four main subagent patterns have emerged as most effective:

1. **Task-Specific** - Single focused task (test-runner, file-analyzer)
2. **Domain-Specific** - Expert in technology (database-engineer, api-designer)
3. **Principle-Enforcing** - Enforce guidelines (backend-engineer with KISS/DRY/YAGNI)
4. **Workflow Orchestrators** - Multi-step processes (deployment-engineer)

**See [examples.md](examples.md) for complete implementations of all four patterns with full system prompts.**

## Subagent Communication

Subagents can work with Skills and other subagents:

### Invoking Skills
```markdown
## Your Process
1. **Invoke the `code-style-guide` Skill** for language-specific patterns
2. Apply recommendations
```

### Delegating to Other Subagents
```markdown
## When to Delegate
- Test failures → `test-runner` subagent
- Deployment → `deployment-engineer` subagent
```

**See [communication.md](communication.md) for delegation patterns, testing strategies, and debugging communication issues.**

## Best Practices

1. **Single Responsibility** - One clear purpose (not "general-helper")
2. **Clear Triggers** - Specific keywords in description ("Use PROACTIVELY when...")
3. **Appropriate Tools** - Least privilege (read-only for reviewers, write for generators)
4. **Focused Prompts** - Under 300 lines, use Skills for complex knowledge
5. **Structured Output** - Define JSON format for orchestrator parsing
6. **TodoWrite Tracking** - Include task tracking in system prompt

## Common Pitfalls

**Too Generic**: `description: "Helps with coding"` → Add specific triggers
**Too Restrictive**: `tools: Read` only → Add Grep, Glob for useful analysis
**Missing Triggers**: No "Use when..." → Add explicit activation criteria
**Bloated Prompts**: 500+ lines → Use Skills for detailed knowledge

## Validation Checklist

Before finalizing a subagent:

- [ ] Name uses lowercase and hyphens only
- [ ] Description includes "when to use"
- [ ] Description contains trigger keywords
- [ ] Tools follow least privilege principle
- [ ] Model choice is appropriate
- [ ] System prompt has clear structure
- [ ] Process/workflow is defined
- [ ] Examples or checklists included
- [ ] No conflicts with existing subagents

## Summary

**Essential Elements**:
1. Focused responsibility (one job, done well)
2. Clear description with triggers
3. Appropriate tool restrictions
4. Structured system prompt
5. Defined workflow/process

**Success Criteria**:
- Automatically invoked at right time
- Has necessary tools to complete tasks
- System prompt provides clear guidance
- Integrates well with other subagents
