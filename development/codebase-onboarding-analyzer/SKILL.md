---
name: codebase-onboarding-analyzer
description: Rapidly understand new codebases through automated analysis of structure, dependencies, architecture, complexity, and data flow. Use when exploring unfamiliar code, onboarding to projects, documenting legacy systems, or generating quick-start guides. Supports Python, JavaScript/TypeScript, Go, Rust, Java, and more.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Codebase Onboarding Analyzer


# Codebase Onboarding Analyzer

## Purpose

Understanding a new codebase is time-consuming and overwhelming. This Skill accelerates onboarding by automatically analyzing:

1. **Repository Structure** - Directory layout, file organization, module boundaries
2. **Dependency Mapping** - Internal dependencies, external packages, dependency graphs
3. **Code Complexity** - Cyclomatic complexity, cognitive complexity, maintainability metrics
4. **Architecture Extraction** - Design patterns, layer separation, component relationships
5. **Documentation Generation** - Auto-generate architectural docs, API references, diagrams
6. **Entry Point Identification** - Main functions, CLI commands, API endpoints, service initialization
7. **Data Flow Analysis** - Trace data movement, state management, side effects
8. **Quick-Start Guides** - Auto-generated setup and contribution guides
9. **Contributor Identification** - Git history analysis, ownership mapping
10. **Technology Stack Detection** - Languages, frameworks, tools, build systems


## When to Use This Skill

- Onboarding to a new project or team
- Understanding legacy codebases without documentation
- Technical due diligence (acquisitions, audits)
- Generating architecture documentation for existing systems
- Planning refactoring efforts
- Code review of large PRs
- Identifying technical debt hotspots
- Creating developer onboarding materials
- Reverse engineering application behavior
- Assessing codebase maintainability



## Quick Start: 5-Minute Codebase Overview

### 1. Quick Survey

Get high-level overview:

```bash
# Install analysis tools (optional)
pip install radon tokei
npm install -g madge

# Run quick survey
PROJECT_DIR=./my-project

# Count lines by language
tokei "$PROJECT_DIR"

# Show directory structure
tree -L 3 -d "$PROJECT_DIR"

# Find entry points
grep -r "if __name__ == '__main__':" "$PROJECT_DIR" --include="*.py"
grep -r "func main()" "$PROJECT_DIR" --include="*.go"
```

### 2. Dependency Analysis

Map dependencies:

```bash
# Python dependencies - Quick inline analysis
python -c "
import ast
from pathlib import Path

for py_file in Path('.').rglob('*.py'):
    with open(py_file) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                print(f'{py_file}: imports {alias.name}')
"

# JavaScript dependencies
npx madge --circular "$PROJECT_DIR"
npx madge --image graph.png "$PROJECT_DIR"
```

### 3. Complexity Check

Identify hotspots:

```bash
# Python complexity
radon cc "$PROJECT_DIR" -a -nb

# JavaScript complexity
npx complexity-report src/**/*.js
```

### 4. Find Entry Points

Discover how to run:

```bash
# Check for main files
find "$PROJECT_DIR" -name "main.py" -o -name "main.go" -o -name "index.js"

# Check for CLI commands
grep -r "@click.command" "$PROJECT_DIR" --include="*.py"

# Check for API endpoints
grep -r "@app.route" "$PROJECT_DIR" --include="*.py"
```

### 5. Git History Analysis

Understand evolution:

```bash
cd "$PROJECT_DIR"

# Top contributors
git shortlog -sn --all | head -10

# Most changed files (hotspots)
git log --format=format: --name-only | sort | uniq -c | sort -rg | head -20

# Recent activity
git log --since="30 days ago" --oneline | wc -l
```

## Core Analysis Capabilities

### Understanding Complexity Layers

Codebase analysis progresses through five layers:

```
┌─────────────────────────────────────────┐
│  Surface Layer                          │
│  ├── Languages & Frameworks             │
│  ├── Build System & Package Manager     │
│  └── Directory Structure                │
├─────────────────────────────────────────┤
│  Dependency Layer                       │
│  ├── External Dependencies              │
│  ├── Internal Module Dependencies       │
│  └── Dependency Graph & Cycles          │
├─────────────────────────────────────────┤
│  Architecture Layer                     │
│  ├── Design Patterns                    │
│  ├── Component Boundaries               │
│  ├── Layer Separation                   │
│  └── Service Interactions               │
├─────────────────────────────────────────┤
│  Code Quality Layer                     │
│  ├── Complexity Metrics                 │
│  ├── Code Smells                        │
│  ├── Test Coverage                      │
│  └── Technical Debt                     │
├─────────────────────────────────────────┤
│  Data Flow Layer                        │
│  ├── State Management                   │
│  ├── Data Transformations               │
│  ├── Side Effects                       │
│  └── API Contracts                      │
└─────────────────────────────────────────┘
```

**Analysis Strategy:** Start broad (surface), then go deep (data flow)

**See:** [KNOWLEDGE.md - Codebase Understanding](./KNOWLEDGE.md#codebase-understanding-layers)

### Complexity Metrics Reference

**Cyclomatic Complexity** - Number of independent paths
- 1-10: Simple, easy to test
- 11-20: Moderate complexity
- 21-50: High complexity, hard to test
- 50+: Very high, refactor recommended

**Cognitive Complexity** - How hard code is to understand
- Measures nested control flow
- Better predictor of maintainability

**Maintainability Index** - Combined metric (0-100)
- 85-100: Highly maintainable
- 65-85: Moderate maintainability
- 0-65: Difficult to maintain

**See:** [KNOWLEDGE.md - Complexity Metrics](./KNOWLEDGE.md#complexity-metrics)

## Analysis Patterns

### 1. Structure Analysis

Maps directory layout, identifies module boundaries, detects technology stack.

**See:** [PATTERNS.md - Pattern 1: Quick Codebase Survey](./PATTERNS.md#pattern-1-quick-codebase-survey)

### 2. Dependency Mapping

Analyzes internal module dependencies and external packages. Includes stdlib detection fix from PR #65.

**See:** [PATTERNS.md - Pattern 2: Dependency Analysis](./PATTERNS.md#pattern-2-dependency-analysis)

### 3. Complexity Analysis

Calculates cyclomatic complexity, maintainability index, cognitive complexity.

**See:** [PATTERNS.md - Pattern 3: Complexity Analysis](./PATTERNS.md#pattern-3-complexity-analysis)

### 4. Entry Point Discovery

Finds all ways to run and interact with the application.

**See:** [PATTERNS.md - Pattern 4: Entry Point Discovery](./PATTERNS.md#pattern-4-entry-point-discovery)

### 5. Architecture Documentation

Auto-generates comprehensive architecture docs.

**See:** [PATTERNS.md - Pattern 5: Architecture Documentation Generator](./PATTERNS.md#pattern-5-architecture-documentation-generator)

### 6. Git History Analysis

Analyzes repository history for insights.

**See:** [PATTERNS.md - Pattern 6: Git History Analysis](./PATTERNS.md#pattern-6-git-history-analysis)

## Complete Workflow

Full codebase analysis in 6 steps. See [EXAMPLES.md - Complete Onboarding Workflow](./EXAMPLES.md#complete-onboarding-workflow) for the complete all-in-one script.

## Top 3 Common Gotchas

1. **Generated Code Skews Metrics**
   - Build artifacts inflate complexity
   - **Solution:** Configure exclusion patterns
   - **See:** [GOTCHAS.md - Generated Code](./GOTCHAS.md#generated-code)

2. **Dynamic Language Import Challenges**
   - Python/JS dynamic imports hard to trace statically
   - **Solution:** Combine static and runtime analysis
   - **See:** [GOTCHAS.md - Dynamic Languages](./GOTCHAS.md#dynamic-languages)

3. **Circular Dependencies Detection**
   - Valid in some languages, smell in others
   - **Solution:** Visualize cycles, evaluate context
   - **See:** [GOTCHAS.md - Circular Dependencies](./GOTCHAS.md#circular-dependencies)

**Full list:** [GOTCHAS.md](./GOTCHAS.md)

## Language-Specific Tools

### Python
- **radon** - Complexity metrics
- **pydeps** - Dependency visualization
- **vulture** - Dead code detection
- **bandit** - Security scanning

### JavaScript/TypeScript
- **madge** - Dependency graphs
- **complexity-report** - Complexity analysis
- **dependency-cruiser** - Dependency validation

### Go
- **gocyclo** - Cyclomatic complexity
- **go-callvis** - Call graph visualization
- **godepgraph** - Dependency graphs

### Rust
- **cargo-modules** - Module structure
- **cargo-geiger** - Unsafe code detection
- **cargo-tree** - Dependency tree

**Complete reference:** [KNOWLEDGE.md - Code Analysis Tools](./KNOWLEDGE.md#code-analysis-tools)

## Best Practices

### DO's
1. **Start Broad, Then Deep** - Overview first, details second
2. **Automate Analysis** - Use scripts for consistency
3. **Focus on Entry Points** - Understand how to run first
4. **Use Visualization** - Graphs aid understanding
5. **Track Over Time** - Monitor complexity trends

### DON'Ts
1. **Don't Over-Analyze** - Paralysis by analysis is real
2. **Don't Analyze Generated Code** - Filter build artifacts
3. **Don't Trust Metrics Blindly** - Context matters
4. **Don't Skip Manual Review** - Talk to maintainers
5. **Don't Ignore Git History** - History reveals evolution

**Details:** [KNOWLEDGE.md - Best Practices](./KNOWLEDGE.md#best-practices)

## Additional Resources

### Detailed Documentation

- **[KNOWLEDGE.md](./KNOWLEDGE.md)** - Code analysis concepts, tools comparison
- **[PATTERNS.md](./PATTERNS.md)** - Complete implementation patterns with code
- **[EXAMPLES.md](./EXAMPLES.md)** - Real-world analysis examples
- **[GOTCHAS.md](./GOTCHAS.md)** - Troubleshooting guide
- **[REFERENCE.md](./REFERENCE.md)** - API documentation, configuration

### Related Skills

- **git-mastery-suite** - For Git history analysis techniques
- **security-scanning-suite** - For security-focused code analysis
- **architecture-evaluation-framework** - For architecture pattern identification
- **gap-analysis-framework** - For identifying missing capabilities

## Quick Reference Card

| Task | Command | Time |
|------|---------|------|
| **Quick survey** | `tokei . && tree -L 3` | 30s |
| **Find entry points** | `grep -r "if __name__" --include="*.py"` | 1m |
| **Dependency graph** | `python analyze_dependencies.py .` | 2m |
| **Complexity hotspots** | `radon cc . -a -nb` | 1m |
| **Git contributors** | `git shortlog -sn --all` | 30s |
| **Full analysis** | `./onboard-codebase.sh .` | 5-10m |
