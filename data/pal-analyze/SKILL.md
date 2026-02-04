---
name: pal-analyze
description: Comprehensive code analysis for architecture, performance, security, and quality using PAL MCP. Use when reviewing codebases, assessing technical decisions, or planning improvements. Triggers on analysis requests, architecture reviews, or code quality assessments.
---

# PAL Analyze - Code Analysis

Systematic code analysis covering architecture, performance, maintainability, and patterns.

## When to Use

- Understanding unfamiliar codebases
- Architectural review and assessment
- Performance analysis and optimization
- Code quality evaluation
- Pattern identification
- Technical debt assessment

## Quick Start

```python
# Start architecture analysis
result = mcp__pal__analyze(
    step="Analyzing authentication system architecture",
    step_number=1,
    total_steps=2,
    next_step_required=True,
    findings="Beginning architecture review",
    analysis_type="architecture",
    output_format="detailed",
    relevant_files=[
        "/app/auth/service.py",
        "/app/auth/middleware.py"
    ],
    confidence="exploring"
)
```

## Analysis Types

| Type | Focus |
|------|-------|
| `architecture` | System design, patterns, modularity |
| `performance` | Bottlenecks, optimization opportunities |
| `security` | Vulnerabilities, auth issues |
| `quality` | Code smells, maintainability |
| `general` | Comprehensive overview |

## Output Formats

| Format | Description |
|--------|-------------|
| `summary` | High-level overview |
| `detailed` | In-depth analysis |
| `actionable` | Prioritized recommendations |

## Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `step` | string | Analysis narrative |
| `step_number` | int | Current step |
| `total_steps` | int | Estimated total |
| `next_step_required` | bool | More analysis needed? |
| `findings` | string | Discoveries and insights |

## Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `analysis_type` | enum | architecture/performance/security/quality/general |
| `output_format` | enum | summary/detailed/actionable |
| `confidence` | enum | exploring → certain |
| `relevant_files` | list | Files under analysis |
| `files_checked` | list | All files examined |
| `issues_found` | list | Issues with severity |
| `continuation_id` | string | Continue session |
| `model` | string | Override model |

## Example: Performance Analysis

```python
mcp__pal__analyze(
    step="Identifying performance bottlenecks in data processing pipeline",
    step_number=1,
    total_steps=2,
    next_step_required=True,
    findings="Scanning for N+1 queries, inefficient loops, missing caching",
    analysis_type="performance",
    output_format="actionable",
    relevant_files=[
        "/app/services/data_processor.py",
        "/app/models/report.py"
    ],
    confidence="exploring"
)
```

## What to Document in Findings

Include both strengths and concerns:

- **Architecture**: Patterns used, coupling, cohesion
- **Performance**: Complexity, caching, query patterns
- **Security**: Auth flows, input validation, secrets
- **Quality**: Duplication, naming, test coverage

## Best Practices

1. **Be systematic** - Cover all relevant aspects
2. **Document strengths** - Not just problems
3. **Prioritize issues** - By severity and impact
4. **Consider context** - Team size, timeline, constraints
5. **Provide evidence** - Reference specific code
