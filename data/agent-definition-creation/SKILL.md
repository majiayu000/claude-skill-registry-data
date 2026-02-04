---
name: agent-definition-creation
description: >
  Use this skill when creating or refining Claude Code sub-agent definitions. Helps design specialized
  AI assistants with proper YAML frontmatter, system prompts, tool access, and example-driven descriptions.
  Automatically invoked when user requests "create an agent", "design a sub-agent", "make a specialist",
  or mentions agent development. Ensures agents follow Anthropic best practices with focused responsibilities,
  discovery-optimized descriptions, and proper tool restrictions.
allowed-tools: Read, Write, Edit, Grep, Glob, mcp__Conventions__search_conventions, mcp__Conventions__get_convention
---

# Agent Definition Creation Skill

This skill helps create production-ready Claude Code sub-agent definitions following Anthropic's official specifications and best practices.

## Core Principles

### 1. Single Responsibility
Each agent should have ONE clear purpose. Avoid creating multipurpose agents that try to do everything.

**Good**: `postgres-expert` - PostgreSQL database management and optimization
**Bad**: `database-expert` - All databases (too broad)

### 2. Discovery-Optimized Descriptions
The `description` field is critical for Claude to discover when to use your agent. Include:
- **What**: Clear statement of capabilities
- **When**: Specific scenarios that trigger usage
- **Examples**: Concrete usage patterns with user/assistant dialogue
- **Trigger terms**: Keywords users might mention

### 3. Tool Restriction Strategy
Grant only necessary tools following principle of least privilege:
- **Omit `tools` field**: Inherits all tools from main conversation (use for general-purpose agents)
- **Specify tools list**: Grant specific tools (use for focused/security-sensitive agents)

### 4. Model Selection
Choose the right model for the task:
- **`sonnet`**: Default choice for most agents (balanced performance/cost)
- **`opus`**: Complex reasoning, architecture decisions, critical tasks
- **`haiku`**: Simple, repetitive tasks with clear patterns
- **`inherit`**: Match parent conversation's model

## Agent Structure

```yaml
---
name: agent-identifier
description: >
  Primary description with capabilities and use cases.

  Examples:
  <example>
  Context: Situation description
  user: "User request example"
  assistant: "I'll use the agent-name to handle this task."
  <commentary>
  Explanation of why this agent is appropriate.
  </commentary>
  </example>

  <example>
  Context: Another scenario
  user: "Different request pattern"
  assistant: "Let me use the agent-name for this."
  <commentary>
  Another use case explanation.
  </commentary>
  </example>

tools: Tool1, Tool2, Tool3  # Optional - omit to inherit all tools
model: sonnet               # Optional - sonnet, opus, haiku, or inherit
color: "#hexcolor"          # Optional - UI color coding
---

System prompt content starts here.

You are a [role description] specializing in [domain].

## Core Responsibilities
- List key responsibilities
- Be specific and actionable
- Include success criteria

## Approach
- Describe methodology
- Include examples
- Reference best practices

## Constraints
- Limitations and boundaries
- Security considerations
- Performance requirements
```

## File Naming & Location

**Project-level** (shared with team):
- Location: `.claude/agents/`
- Format: `agent-name.md`
- Example: `.claude/agents/postgres-expert.md`

**User-level** (personal, cross-project):
- Location: `~/.claude/agents/`
- Format: `agent-name.md`
- Example: `~/.claude/agents/custom-reviewer.md`

**Naming conventions**:
- Use lowercase letters and hyphens only
- Be descriptive but concise
- Avoid generic names like "helper" or "assistant"

## Required Fields

### name
Unique identifier using lowercase alphanumeric characters and hyphens.

```yaml
name: fastapi-expert        # Good
name: FastAPI Expert        # Bad - no spaces or capitals
name: expert                # Bad - too generic
```

### description
Natural language explanation with examples. This is THE MOST IMPORTANT FIELD.

**Structure**:
1. **Primary statement**: What the agent does (1-2 sentences)
2. **Use cases**: Specific scenarios (bullet points or prose)
3. **Examples**: 2-4 concrete user/assistant dialogues with commentary
4. **Trigger terms**: Keywords for discovery

**Example**:
```yaml
description: >
  Expert in PostgreSQL database management, optimization, and architecture. Specializes in
  query performance tuning, schema design, replication, and PostgreSQL 16+ advanced features.
  Use PROACTIVELY for database optimization, slow queries, or schema design tasks.

  Examples:
  <example>
  Context: User needs query optimization
  user: "My PostgreSQL queries are slow"
  assistant: "I'll use the postgres-expert agent to analyze and optimize your queries."
  <commentary>
  Query performance is a core competency, so this agent is appropriate.
  </commentary>
  </example>
```

## Optional Fields

### tools
Comma-separated list of allowed tools. Omit to inherit all tools from main conversation.

**When to restrict**:
- Security-sensitive agents (limit file access, bash execution)
- Focused agents that only need specific capabilities
- Agents that should not modify code (Read, Grep, Glob only)

**Common tool sets**:
```yaml
# Read-only analysis
tools: Read, Grep, Glob, Bash(git :*)

# Code modification
tools: Read, Write, Edit, MultiEdit, Grep, Glob

# Research and planning
tools: Read, Grep, Glob, WebFetch, WebSearch

# Full-stack development
tools: Read, Write, Edit, MultiEdit, Bash, Grep, Glob, WebSearch
```

### model
Specify model for this agent. Options: `sonnet`, `opus`, `haiku`, `inherit`

```yaml
model: sonnet    # Default - balanced performance
model: opus      # Complex reasoning, architecture
model: haiku     # Simple, fast tasks
model: inherit   # Match parent conversation
```

### color
Hex color for UI identification (optional, cosmetic).

```yaml
color: "#d79921"    # Yellow
color: "#458588"    # Blue
color: "#cc241d"    # Red
```

## System Prompt Best Practices

### 1. Role Definition
Start with a clear role statement:

```markdown
You are an expert PostgreSQL database administrator and architect specializing in
performance optimization, schema design, and high-availability configurations.
```

### 2. Responsibilities Section
List concrete, actionable responsibilities:

```markdown
## Core Responsibilities

### Query Optimization
- Analyze EXPLAIN plans and execution statistics
- Recommend index strategies for slow queries
- Identify and fix N+1 query problems
- Optimize JOIN operations and subqueries

### Schema Design
- Design normalized schemas following 3NF principles
- Implement efficient indexing strategies
- Set up row-level security (RLS) for multi-tenancy
- Create database migrations with zero downtime
```

### 3. Approach Section
Describe methodology with examples:

```markdown
## Approach

When optimizing queries:
1. Request the slow query and current execution plan
2. Analyze EXPLAIN ANALYZE output for bottlenecks
3. Recommend specific index additions or query rewrites
4. Provide before/after performance metrics
5. Explain the reasoning behind each optimization
```

### 4. Examples & Code Snippets
Include working examples:

```markdown
## Example: Index Optimization

For a slow query like:
\`\`\`sql
SELECT users.*, orders.total
FROM users
JOIN orders ON users.id = orders.user_id
WHERE orders.created_at > NOW() - INTERVAL '30 days';
\`\`\`

Recommend:
\`\`\`sql
CREATE INDEX idx_orders_created_user
ON orders(created_at, user_id)
INCLUDE (total);
\`\`\`
```

### 5. Constraints & Boundaries
Define what the agent should NOT do:

```markdown
## Constraints

- Never recommend dropping production indexes without analyzing dependencies
- Always suggest testing schema changes in staging first
- Do not execute destructive operations without explicit confirmation
- Require EXPLAIN ANALYZE output before optimization recommendations
```

## Agent Archetypes

### Research/Analysis Agents
**Characteristics**:
- Read-only tool access (Read, Grep, Glob)
- Focus on investigation and reporting
- No code modification

**Example**: Code reviewer, security auditor, documentation analyzer

### Development Agents
**Characteristics**:
- Full editing tools (Read, Write, Edit, MultiEdit)
- Language/framework-specific expertise
- Can run tests and builds

**Example**: Python expert, React specialist, FastAPI architect

### Infrastructure Agents
**Characteristics**:
- Bash access for system commands
- Docker, cloud CLI tools
- Configuration file manipulation

**Example**: Docker engineer, Terraform specialist, K8s expert

### Orchestration Agents
**Characteristics**:
- Task delegation capabilities
- High-level planning
- Multi-agent coordination

**Example**: Project planner, workflow coordinator

## Testing Your Agent

After creating an agent definition:

1. **Test discovery**: Ask natural language questions that should trigger the agent
   ```
   User: "Help me optimize my PostgreSQL query"
   Expected: Claude invokes postgres-expert agent
   ```

2. **Verify tool access**: Ensure the agent can access specified tools

3. **Check boundaries**: Confirm the agent stays within its defined scope

4. **Review examples**: Ensure example scenarios accurately represent usage

## Common Mistakes to Avoid

❌ **Too broad scope**
```yaml
name: backend-expert
description: Expert in all backend technologies
```

✅ **Focused scope**
```yaml
name: fastapi-expert
description: Expert in FastAPI async Python API development
```

❌ **Generic description**
```yaml
description: Helps with database tasks
```

✅ **Specific description with examples**
```yaml
description: >
  PostgreSQL expert for query optimization, schema design, and replication.
  Use for slow queries, database architecture, or production scaling.

  Examples: [concrete user/assistant dialogues]
```

❌ **No tool restrictions when needed**
```yaml
# Security audit agent with full write access - dangerous!
tools: # Inherits all tools including Edit, Write, Bash
```

✅ **Appropriate tool restrictions**
```yaml
# Security audit agent - read-only access
tools: Read, Grep, Glob, Bash(git :*)
```

❌ **Missing examples in description**
```yaml
description: Expert in React development
```

✅ **Examples included**
```yaml
description: >
  Expert in React development...

  Examples:
  <example>
  Context: User needs component optimization
  user: "My dashboard re-renders too often"
  assistant: "I'll use the react-expert to profile and optimize rendering."
  <commentary>Performance optimization is a core competency.</commentary>
  </example>
```

## Advanced Features

### Resumable Agents
Each agent execution gets a unique `agentId`. You can resume previous agent conversations:

```
User: "Resume agent execution abc123 and continue the analysis"
```

Transcripts are stored separately and can be continued with full context.

### Proactive Usage
Include phrases in description to encourage automatic invocation:
- "Use PROACTIVELY when..."
- "MUST BE USED for..."
- "Automatically invoke for..."

### CLI Configuration
Dynamic agent creation without files:

```bash
claude --agents '{"name": "temp-agent", "description": "...", "tools": "Read,Grep"}'
```

## Resources

Reference the examples directory for:
- Complete agent definitions across different domains
- Real-world system prompts with proven effectiveness
- Tool restriction patterns for various use cases
- Discovery-optimized description templates

---

**Next Steps**: After creating an agent definition, test it with natural language queries to verify Claude discovers and invokes it appropriately. Refine the description based on actual usage patterns.
