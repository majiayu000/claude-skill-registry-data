---
name: blast-radius-analysis
description: "Analyze the impact of code changes by mapping call graphs and identifying all direct and indirect dependencies. Use when users ask about blast radius analysis, code change impact, who calls a function, downstream dependencies, or risk assessment before refactoring. Traces call chains, identifies high-risk modules, and provides ranked impact analysis."
---

# Blast Radius Analysis

Analyze the potential impact of code changes before making them. Map out call graphs, identify dependencies, and assess risk.

## Core Workflow

When triggered by questions about code change impact, follow this systematic approach:

### 1. Locate the Target

First, find the target function/class in the codebase:

```bash
# Search for the function definition
grep -rn "def function_name" --include="*.py" --include="*.js" --include="*.ts"
# Or use Glob to find the file
```

### 2. Map the Call Graph

Use LSP tools to trace the complete call chain:

```python
# Get all incoming calls (who calls this function)
LSP(operation="incomingCalls", filePath="path/to/file", line=N, character=M)

# For each caller, recursively trace their incoming calls
# Build a complete tree of indirect dependencies
```

### 3. Categorize Impact Levels

Classify each affected module by risk:

**HIGH RISK (Critical)**:
- Public API functions
- Functions called by multiple unrelated modules
- Functions in hot paths or critical business logic
- Functions with complex state dependencies

**MEDIUM RISK**:
- Internal functions with moderate call chains
- Functions called by 2-3 other modules
- Functions with clear, isolated logic

**LOW RISK**:
- Leaf functions (no incoming calls beyond immediate parent)
- Private/internal methods with single caller
- Pure functions with no side effects

### 4. Output Format

Present results in this structure:

```
## Blast Radius Analysis: [Function Name]

**Location**: `file_path:line_number`

### Direct Callers (N)
1. `module/function` - Risk: [HIGH/MEDIUM/LOW]
   - Impact: [what breaks]

### Indirect Callers (N)
1. `module/A -> module/B -> target` - Risk: [HIGH/MEDIUM/LOW]
   - Impact: [cascading effect]

### Risk Ranking
🔴 Critical: [modules]
🟡 Moderate: [modules]
🟢 Safe: [modules]

### Recommendations
- [Specific guidance based on analysis]
```

## Advanced Patterns

For complex scenarios, see [ANALYSIS_PATTERNS.md](references/ANALYSIS_PATTERNS.md) for:
- Multi-file refactoring impact
- Breaking circular dependencies
- API contract changes

## Tool Selection Guide

- **LSP (preferred)**: For languages with LSP support (TS/JS, Python, Java, Go). Use `incomingCalls` and `outgoingCalls`.
- **Grep**: For languages without LSP or when LSP is unavailable. Search for function name patterns.
- **Grep + manual analysis**: For dynamic languages or when call sites are generated at runtime.

## Risk Assessment Methodology

See [METHODOLOGY.md](references/METHODOLOGY.md) for detailed criteria on:
- How to quantify risk levels
- Dependency depth vs. breadth tradeoffs
- Module coupling analysis
