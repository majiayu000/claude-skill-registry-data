---
name: predictive-intelligence
description: Analyze tasks upfront before execution. Predict task category, identify key files, assess risk level, and detect high-consequence operations. Use proactively when any task description is provided to guide execution strategy.
allowed-tools: Read, Grep, Glob
---

# Predictive Intelligence

Apex2's prediction phase implemented as a Claude Code skill. This skill extracts critical task metadata before any execution begins.

## Instructions

When invoked (either explicitly or automatically by Claude), perform these sequential analyses:

### 1. Task Categorization
Analyze the task description to determine:
- **Primary category**: ML/DL, Web Development, Data Analysis, Security, System Admin, DevOps, etc.
- **Complexity level**: Simple, Medium, Complex
- **Estimated duration**: <5min, 5-30min, >30min
- **Risk profile**: Low (reversible), Medium (potentially disruptive), High (irreversible/dangerous)

### 2. Key File Identification
Extract specific file/folder mentions from the task:
- Explicit file names mentioned
- Implicit file patterns based on task type
- Critical configuration files
- Test files that may need updating

### 3. Risk Assessment
Identify potential high-consequence operations:
- `rm -rf` or destructive commands
- Database migrations or data deletion
- System configuration changes
- Network service modifications
- Security credential changes

### 4. Environment Requirements
Predict what needs to be present:
- Required packages/libraries
- Service dependencies
- File permissions needed
- Network access requirements

### 5. Execution Strategy Guidance
Based on analysis, provide strategic recommendations:
- Should proceed with direct execution?
- Need further exploration first?
- Requires multi-step approach?
- Should create backups first?
- Needs dry-run testing?

## Apex2 Integration Patterns

### For ML Tasks
- Flag that training runs can exceed 5 minutes
- Recommend parameter search before full runs
- Suggest validating dataset dimensions first
- Identify need for GPU resources

### For Security Tasks
- Emphasize irreversible nature of many operations
- Recommend exact sequence verification
- Suggest backup verification before destructive commands
- Flag privilege escalation needs

### For Web Development
- Identify framework conventions used
- Check for existing test coverage
- Note dependency management approach
- Flag potential deployment impacts

## Analysis Process

1. Read the task description carefully
2. Use Glob to identify relevant file patterns
3. Use Grep to search for related keywords in files
4. Use Read to examine key files discovered
5. Synthesize findings into structured prediction report

## Output Format

Provide a concise prediction report with:

```
Task Analysis:
  Category: [category]
  Complexity: [level]
  Duration: [estimate]
  Risk: [profile]

Key Files:
  - [file1]: [purpose]
  - [file2]: [purpose]

Risks Identified:
  - [risk1]: [mitigation]
  - [risk2]: [mitigation]

Recommended Strategy:
  1. [step1]
  2. [step2]
  3. [step3]

Environment Needs:
  - [requirement1]
  - [requirement2]
```

## When to Use

This skill is automatically useful when:
- Any new task is described
- Complex multi-step operations are planned
- Unfamiliar codebases or domains encountered
- High-stakes operations are contemplated
- Quick context is needed before diving in

The goal is to prevent wasted effort and ensure safe, efficient execution by understanding the full scope before beginning.
