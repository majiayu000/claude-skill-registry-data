---
name: claude-code-agent-patterns
description: Activate when creating or modifying Claude Code agents with proper architecture patterns, tool selection, and extended context integration
license: MIT
---

# Claude Code Agent Patterns

Guide for designing and implementing Claude Code agents with proven architectural patterns, optimal tool selection, and effective extended context integration.

## When to Use This Skill

Activate when:
- Creating new Claude Code agents
- Designing agent architecture and responsibilities
- Selecting appropriate tools for agents
- Integrating extended context with agents
- Implementing multi-agent coordination
- Troubleshooting agent behavior

## Core Architecture Patterns

### 1. Single-Purpose Specialist

**Use Case**: Agents focused on one specific domain or capability.

```yaml
---
name: security-scanner
description: "Specialized agent for identifying security vulnerabilities"
tools: [Read, Glob, Grep, Write]
model: sonnet
---
```

**Characteristics**:
- Clear, focused responsibility
- Deep domain expertise
- Optimized tool set
- Rich extended context

**Best For**: Analysis tasks, specialized assessments, domain-specific operations

### 2. Workflow Orchestrator

**Use Case**: Agents coordinating multiple tasks or other agents.

```yaml
---
name: ci-cd-orchestrator
description: "Coordinates complete CI/CD pipeline execution"
tools: [Task, Bash, Read, Write, TodoWrite]
model: opus
---
```

**Characteristics**:
- Manages complex multi-step processes
- Coordinates other agents via Task tool
- Handles error recovery and rollback
- Maintains process state

**Best For**: Complex workflows, multi-agent coordination, pipeline orchestration

### 3. Context-Aware Adapter

**Use Case**: Agents that adapt behavior based on project context.

```yaml
---
name: language-aware-formatter
description: "Code formatter adapting to project language and style"
tools: [Read, Glob, Bash, Write, Grep]
model: sonnet
---
```

**Characteristics**:
- Detects project characteristics automatically
- Adapts behavior based on context
- Supports multiple scenarios
- Maintains consistent interface

**Best For**: Multi-language tools, adaptive analysis, context-sensitive operations

### 4. Resource-Optimized Processor

**Use Case**: Agents handling large datasets or resource-intensive operations.

```yaml
---
name: large-codebase-analyzer
description: "Efficiently analyzes large codebases with incremental processing"
tools: [Read, Glob, Bash, Write, TodoWrite]
model: sonnet
---
```

**Characteristics**:
- Implements incremental processing
- Manages memory and resources
- Provides progress tracking
- Supports resumable operations

**Best For**: Large codebase analysis, batch processing, long-running operations

## Model Selection Guidelines

### Haiku
- Simple validation tasks
- File operations
- Basic path checking
- Quick utility operations

### Sonnet
- Complex reasoning and analysis
- Domain-specific expertise
- Code generation and modification
- Most specialist agents

### Opus
- Multi-agent coordination
- Workflow orchestration
- Complex decision-making
- High-stakes operations

## Tool Assignment Patterns

### Analysis-Focused
```yaml
tools: [Read, Glob, Grep, Write]
```
Information gathering and reporting

### Orchestration-Focused
```yaml
tools: [Task, Bash, TodoWrite]
```
Process coordination and execution

### Development-Focused
```yaml
tools: [Read, Edit, MultiEdit, Bash, Write]
```
Code modification and testing

### Web-Focused
```yaml
tools: [WebFetch, WebSearch, Read, Write]
```
External information retrieval

## Extended Context Architecture

### Hierarchical Knowledge Structure
```
extended_context/
├── domain-knowledge/
│   ├── core-concepts/
│   ├── best-practices/
│   └── common-patterns/
├── troubleshooting/
│   ├── common-issues/
│   └── resolution-guides/
└── reference-materials/
    └── tool-specifications/
```

### Cross-Referenced Context
```markdown
# In security-patterns.md
Related contexts:
- ../coding-standards/security-practices.md
- ../vulnerability-databases/known-issues.md
```

### Layered Context
1. **Core Layer**: Fundamental concepts
2. **Domain Layer**: Specific knowledge areas
3. **Application Layer**: Implementation guides
4. **Troubleshooting Layer**: Problem resolution

## Agent Communication Patterns

### Message Passing
```markdown
Context passed to next agent:
- operation-id: unique identifier
- previous-results: structured output
- user-context: original request
```

### Shared Context
```markdown
Shared context location: extended_context/shared/
- project-state.md
- user-preferences.md
- session-context.md
```

## Quality Assurance Patterns

### Self-Validation
```markdown
Validation steps:
1. Check output format compliance
2. Verify required information present
3. Validate against known constraints
4. Perform consistency checks
```

### Peer Review
```markdown
Review workflow:
1. Primary agent completes analysis
2. Review agent validates quality
3. Synthesis agent combines perspectives
4. Final output with confidence scores
```

## Anti-Patterns to Avoid

### Monolithic Agent
**Problem**: Single agent handling too many responsibilities
**Solution**: Split into focused specialist agents

### Tool Overload
**Problem**: Agent with too many tools
**Solution**: Assign minimal needed tool set

### Context Redundancy
**Problem**: Duplicate information across agents
**Solution**: Create shared context areas

### Coordination Chaos
**Problem**: Agents without clear communication
**Solution**: Implement structured coordination patterns

## Agent Template

```yaml
---
name: agent-name
description: "Clear, concise purpose statement"
model: sonnet  # or haiku/opus based on complexity
tools: [Read, Write, ...]
---

# Agent Name

## Purpose
[What this agent does and when to use it]

## Capabilities
- [Capability 1]
- [Capability 2]

## Extended Context Integration
References:
- extended_context/[category]/[file].md

## Input Requirements
- [Required input 1]
- [Required input 2]

## Output Format
[Expected output structure]

## Anti-Fabrication Requirements
- Base all outputs on actual analysis
- Execute validation tools before claims
- Mark uncertain information appropriately
```

## Key Principles

- **Single Responsibility**: One clear purpose per agent
- **Minimal Tools**: Only tools needed for the task
- **Rich Context**: Comprehensive extended context
- **Clear Communication**: Structured coordination patterns
- **Self-Validation**: Verify outputs before completion
- **Consistent Naming**: lowercase-hyphen format
