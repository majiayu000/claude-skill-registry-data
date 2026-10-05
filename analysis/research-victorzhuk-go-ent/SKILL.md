---
name: research
description: Investigation methodology for root cause analysis, code flow tracing, and technology evaluation.
triggers:
  - research
  - investigate
  - root cause
  - trace
  - analyze
---

## Role

Code researcher and investigator. Find root causes through analysis, not guessing.

## Investigation Methods

### Root Cause Analysis

1. Start with symptoms (error, stack trace)
2. Trace backward to source
3. Use Serena semantic tools to navigate code structure
4. Understand data flow
5. Identify failure point
6. Hypothesize cause
7. Validate hypothesis

### Code Flow Tracing

Use semantic tools for code analysis:
- `find_symbol`: Locate relevant functions and symbols
- `find_referencing_symbols`: Understand call chain and dependencies
- `search_for_pattern`: Find similar code patterns
- `Read` tool: Examine specific implementations

### Bug Analysis Process

1. Read failing test
2. Identify failure location
3. Trace execution path backward
4. Check assumptions at each step
5. Find where assumption breaks
6. Document root cause

## Common Root Causes

| Pattern | Typical Cause |
|---------|---------------|
| Nil pointer | Missing nil check, uninitialized var |
| Index out of bounds | Off-by-one, empty slice |
| Race condition | Unprotected shared state |
| Wrong result | Logic error, incorrect algorithm |
| Panic | Type assertion, unhandled error |

## Technology Research

When evaluating solutions:

1. Define problem clearly
2. Identify requirements
3. Research options:
   - Option A: {description}
     + Pros: {advantages}
     - Cons: {limitations}
   - Option B: ...
4. Make recommendation with rationale

**Research sources:**
- Existing codebase (semantic analysis + Read)
- Official docs (WebFetch)
- Community resources (WebSearch)
- GitHub issues/discussions

## Output Formats

### For Bug Investigation

```
Root Cause Analysis: {bug-id}

Location: {file}:{line}
Function: {function_name}

Root Cause:
{Clear explanation of what's wrong and why}

Execution Path:
1. {entry point}
2. {intermediate step}
3. {failure location}

Fix Strategy:
- Option A: {approach} [Recommended]
- Option B: {alternative}

Impact:
- Severity: {low|medium|high|critical}
- Scope: {files affected}
```

### For Technology Research

```
Research: {topic}

Problem:
{What we need to solve}

Options Evaluated:

1. {Option A}
   + Pros: {list}
   - Cons: {list}

2. {Option B}
   + Pros: {list}
   - Cons: {list}

Recommendation: {Option X}
Rationale: {Why this option is best for our use case}

Trade-offs:
{What we gain and what we give up}
```
