---
name: claude-code-command-patterns
description: Activate when creating or modifying Claude Code slash commands with proper frontmatter, Task invocation patterns, and TodoWrite integration
license: MIT
---

# Claude Code Command Patterns

Guide for creating and modifying Claude Code slash commands with proper structure, parallel execution patterns, and agent coordination.

## When to Use This Skill

Activate when:
- Creating new Claude Code slash commands
- Modifying existing command structure
- Implementing parallel Task invocations
- Adding TodoWrite progress tracking
- Coordinating multiple agents from commands
- Debugging command-to-agent integration

## Command Structure

### Required Frontmatter
```yaml
---
description: "Command purpose in clear, concise terms"
argument-hint: "[input-type] [optional-params]"
---
```

### Command Body Template
```markdown
I am a [command purpose] that [brief description]. My task is to:

1. Setup todo tracking for the workflow
2. Invoke specialized agents using parallel Task calls
3. Read and validate outputs from expected files
4. Create comprehensive report with findings

## Implementation

I will use TodoWrite to track progress, then make parallel Task calls:
- Task with subagent_type: "agent-name-1" - pass the [argument] for [purpose]
- Task with subagent_type: "agent-name-2" - pass the [argument] for [purpose]

Then read outputs, validate them, and create complete report.
```

## Required Elements

### 1. TodoWrite First
Always setup todo tracking before Task calls:
```markdown
I will use TodoWrite to track progress...
```

### 2. Parallel Task Calls
Explicitly state parallel execution:
```markdown
...then make parallel Task calls:
- Task with subagent_type: "agent-a" - ...
- Task with subagent_type: "agent-b" - ...
```

### 3. Argument Passing
Pass meaningful context to each agent:
```markdown
- Task with subagent_type: "analyzer" - pass the project_path argument [PATH] for analysis
```

### 4. Output Validation
Read and validate actual outputs:
```markdown
Then read outputs from [files], validate them, and create complete report.
```

## Execution Patterns

### Parallel Execution
When tasks are independent:
```markdown
make parallel Task calls:
- Task with subagent_type: "agent-1" - ...
- Task with subagent_type: "agent-2" - ...
- Task with subagent_type: "agent-3" - ...
```

### Sequential Execution
When tasks have dependencies:
```markdown
First, use Task with subagent_type: "discovery-agent" to analyze project.
Then, use Task with subagent_type: "plan-agent" with discovery results.
Finally, use Task with subagent_type: "task-agent" with plan output.
```

### Conditional Execution
When execution depends on results:
```markdown
First check if [condition] exists using Read tool.
If present, skip to validation phase.
If not, execute discovery workflow.
```

## Argument Extraction Pattern

Commands should document argument extraction for agents:
```markdown
## Argument Extraction Instructions

When invoking agents, use explicit argument passing:
- "pass the project_path argument [PATH] for [purpose]"
- "pass the changes-description argument '[DESC]' for [purpose]"

Agents extract these values from their task prompts.
```

## Anti-Patterns to Avoid

### Never Use
- Coordinator agents that call other agents (commands coordinate directly)
- Sequential execution when parallel is possible
- Missing TodoWrite progress tracking
- Generic arguments without context
- Assuming outputs without Read/validation
- Incorrect subagent_type references

### Incorrect
```markdown
# WRONG: Missing TodoWrite
I will invoke agents directly...

# WRONG: No argument passing
- Task with subagent_type: "analyzer"

# WRONG: Sequential when parallel works
First run agent-1, then agent-2, then agent-3...
```

### Correct
```markdown
# RIGHT: TodoWrite first
I will use TodoWrite to track progress, then...

# RIGHT: Explicit argument passing
- Task with subagent_type: "analyzer" - pass the project_path argument ./src for code analysis

# RIGHT: Parallel execution
...make parallel Task calls:
- Task with subagent_type: "agent-1" - ...
- Task with subagent_type: "agent-2" - ...
```

## Complete Example

```markdown
---
description: "Analyze project security posture and generate comprehensive report"
argument-hint: "[project-path]"
---

I am a security analysis coordinator that evaluates project security across multiple dimensions. My task is to:

1. Setup todo tracking for the security workflow
2. Invoke security agents using parallel Task calls
3. Read and validate outputs from security reports
4. Create comprehensive security assessment

## Implementation

I will use TodoWrite to track progress, then make parallel Task calls:
- Task with subagent_type: "vulnerability-assessment-specialist" - pass the project_path argument for vulnerability scanning
- Task with subagent_type: "security-architecture-analyst" - pass the project_path argument for architecture review
- Task with subagent_type: "security-threat-modeler" - pass the project_path argument for STRIDE analysis

Then read outputs from security reports, validate findings, and create consolidated assessment.
```

## Naming Conventions

- **Commands**: lowercase-hyphen (e.g., `security-review.md`)
- **Agents**: lowercase-hyphen (e.g., `security-threat-modeler.md`)
- **subagent_type**: Must match agent filename without `.md`

## Key Principles

- Commands coordinate agents directly (no intermediate coordinators)
- Use TodoWrite for progress tracking
- Prefer parallel execution when tasks are independent
- Pass explicit arguments with clear purposes
- Validate outputs before creating final reports
- Use consistent lowercase-hyphen naming
