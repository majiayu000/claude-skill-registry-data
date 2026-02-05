---
name: code-agent-builder
description: Create well-structured subagents for Claude Code with specialized expertise, proper tool configurations, and effective system prompts. Use when building custom subagents for code review, debugging, testing, data analysis, codebase research, or domain-specific workflows.
---

# Code Agent Builder

Create specialized AI subagents for Claude Code that handle specific tasks with focused expertise and isolated context.

## What Are Subagents?

Subagents are specialized AI assistants that Claude Code delegates tasks to. Each subagent:
- Has a specific purpose and expertise area
- Operates in its own context window (separate from main conversation)
- Can be configured with specific tools
- Includes a custom system prompt guiding behavior
- Lives in `.claude/agents/` (project) or `~/.claude/agents/` (user-wide)

## When to Create a Subagent

Create subagents for:
- **Repetitive specialized tasks**: Code review, testing, debugging
- **Domain-specific work**: Database queries, API interactions, data analysis
- **Multi-step workflows**: Research → analysis → implementation
- **Context isolation**: Keep main conversation focused while delegating details
- **Tool restriction**: Limit powerful tools to specific subagent types

## Quick Start: Creating Your First Subagent

### Step 1: Choose a Template

Select a starting template from `assets/`:
- `template-code-reviewer.md` - Code quality and security review
- `template-debugger.md` - Error investigation and fixing
- `template-test-runner.md` - Automated testing workflows
- `template-codebase-researcher.md` - Architecture analysis and reverse engineering
- `template-data-analyst.md` - Statistical analysis and visualization

Or start from scratch using the structure in `references/subagent-best-practices.md`.

### Step 2: Customize the Configuration

Edit the YAML frontmatter:

```yaml
---
name: your-subagent-name           # lowercase-with-hyphens
description: Specific description   # When to use this subagent
tools: Read, Edit, Bash            # Optional: specific tools only
model: sonnet                      # Optional: sonnet/opus/haiku/inherit
---
```

**Description writing tips**:
- Be specific and action-oriented
- Include trigger phrases for automatic delegation
- Use "PROACTIVELY" or "MUST BE USED" for automatic invocation
- Example: "Security analyst. MUST BE USED when reviewing authentication or data handling."

**Tool selection**:
- Omit `tools:` to inherit all tools (flexible but less focused)
- List specific tools for focused behavior and security
- Common tools: Read, Edit, Write, Bash, Grep, Glob
- Use `/agents` command to see all available tools including MCP tools

**Model selection**:
- `sonnet`: Default, balanced speed and capability
- `opus`: Most capable, use for complex analysis  
- `haiku`: Fastest, use for simple tasks
- `'inherit'`: Match main conversation's model

### Step 3: Write the System Prompt

Follow this structure:

```markdown
You are a [role] specializing in [domain].

When invoked:
1. [First step - usually gather information]
2. [Second step - analysis or processing]
3. [Final step - output or recommendation]

[Specific guidance section]:
- [Key principle or rule]
- [Technique to apply]
- [Important pattern]

For each [output type], provide:
- [Required element 1]
- [Quality standard]
- [Format specification]

Focus on [core objective], not [anti-pattern to avoid].
```

See `references/subagent-best-practices.md` for detailed examples and patterns.

### Step 4: Save the Subagent

**For project-specific use**:
```bash
mkdir -p .claude/agents
mv your-subagent.md .claude/agents/
```

**For personal use across all projects**:
```bash
mkdir -p ~/.claude/agents
mv your-subagent.md ~/.claude/agents/
```

**Priority**: Project subagents override user-level subagents with the same name.

### Step 5: Test and Iterate

1. Invoke explicitly: `> Use the your-subagent-name subagent to [task]`
2. Test automatic delegation by describing tasks matching the description
3. Observe performance and adjust based on results
4. Refine the system prompt for better guidance
5. Adjust tool access if needed

## Subagent Design Patterns

### Pattern 1: Process-Driven (Sequential Workflows)

Best for: Debugging, testing, deployment
```markdown
When invoked:
1. Discovery/analysis step
2. Planning step  
3. Execution step
4. Verification step
```

### Pattern 2: Analysis-Driven (Quality Assessment)

Best for: Code review, architecture analysis, research
```markdown
Analysis checklist:
- Criterion 1
- Criterion 2
- Criterion 3

Feedback organized by:
- Critical issues
- Warnings
- Suggestions
```

### Pattern 3: Tool-Focused (API/System Integration)

Best for: Databases, cloud services, file formats
```markdown
When invoked:
1. Understand requirement
2. Use [specific tool/command]
3. Process/format results
4. Present findings
```

## Management with /agents Command

The `/agents` command provides an interactive interface:

```
/agents
```

Features:
- View all available subagents
- Create new subagents with guided setup
- Edit existing subagents
- Manage tool permissions with full tool list
- Delete custom subagents
- See priority when duplicates exist

**Recommended**: Use `/agents` for tool management - it shows all available tools including MCP server tools.

## Advanced Techniques

### Chaining Subagents

For complex workflows:
```
> Use code-analyzer to find issues, then optimizer to fix them
```
Claude coordinates the sequence automatically.

### Proactive Usage Triggers

Make subagents activate automatically:
- "Use proactively after [action]"
- "MUST BE USED when [condition]"  
- "Use immediately after [event]"

Example:
```yaml
description: Test runner. Use proactively after code changes to run tests and fix failures.
```

### Context Preservation Strategy

- Main conversation: High-level planning and coordination
- Subagents: Detailed execution and technical work
- Result: Longer overall sessions without context pollution

## Available Reference Materials

### Comprehensive Best Practices

See `references/subagent-best-practices.md` for:
- File format details and field specifications
- Writing effective descriptions and system prompts
- Tool selection strategies
- Model selection guidance
- Design patterns with detailed examples
- Anti-patterns to avoid
- Performance considerations
- Complete lifecycle management

### Ready-to-Use Templates

Available in `assets/`:

1. **template-code-reviewer.md**
   - Proactive code quality and security review
   - Tools: Read, Grep, Glob, Bash
   - Organizes feedback by priority

2. **template-debugger.md**
   - Root cause analysis for errors and failures
   - Tools: Read, Edit, Bash, Grep, Glob
   - Systematic debugging workflow

3. **template-test-runner.md**
   - Automated testing after code changes
   - Preserves test intent while fixing issues
   - Framework-agnostic approach

4. **template-codebase-researcher.md**
   - Architecture analysis and reverse engineering
   - Extracts algorithms and design patterns
   - Structured analysis output format

5. **template-data-analyst.md**
   - Statistical analysis and visualization
   - R and Python expertise
   - Publication-quality outputs

## Common Patterns for Specific Domains

### For Code Quality
```yaml
name: code-quality-enforcer
description: Style and quality enforcer. Use proactively before commits to ensure standards.
tools: Read, Bash, Grep
```

### For Git Operations  
```yaml
name: git-specialist
description: Git workflow expert. Use before commits, after conflicts, when investigating history.
tools: Bash, Read, Grep
```

### For Documentation
```yaml
name: doc-writer
description: Technical documentation specialist. Use after implementing features to generate docs.
tools: Read, Write, Grep, Glob
```

### For Security
```yaml
name: security-auditor  
description: Security analyst. MUST BE USED when reviewing auth, data handling, or API endpoints.
tools: Read, Grep, Glob
```

## Best Practices Summary

✅ **Do:**
- Start with templates and customize
- Write specific, action-oriented descriptions
- Use imperative instructions in system prompts
- Test with real tasks and iterate
- Limit tools to what's actually needed
- Include concrete examples and checklists
- Make subagents single-purpose

❌ **Don't:**
- Create generic, multi-purpose subagents
- Write vague descriptions like "helper for various tasks"
- Assume context from main conversation
- Give all subagents all tools
- Make system prompts overly abstract
- Try to handle too many responsibilities in one subagent

## Troubleshooting

**Subagent not triggering automatically?**
- Make description more specific and action-oriented
- Add trigger phrases: "use PROACTIVELY", "MUST BE USED"
- Test explicit invocation first: `> Use [name] subagent to [task]`

**Subagent lacking necessary context?**
- Update system prompt to be more self-contained
- Add explicit instructions for gathering context
- Include examples of how to discover needed information

**Subagent using wrong tools?**
- Review tool permissions in frontmatter
- Use `/agents` command to adjust tool access
- Consider if subagent needs more or fewer tools

**Multiple subagents with similar names?**
- Check priority: Project > CLI > User
- Use unique, descriptive names
- Delete or rename conflicting subagents with `/agents`

## Next Steps

1. **Pick a template** from `assets/` that matches your needs
2. **Customize** the configuration and system prompt  
3. **Save** to `.claude/agents/` or `~/.claude/agents/`
4. **Test** with explicit invocation
5. **Iterate** based on real-world performance
6. **Consult** `references/subagent-best-practices.md` for detailed guidance
