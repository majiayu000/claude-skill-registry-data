---
name: refactoring-discovery
description: Discover refactoring opportunities by analyzing code for excessive responsibilities, tight coupling, low cohesion, and SOLID principle violations. Generate detailed reports with redesign proposals tailored to the project's architecture. Use when analyzing existing code modules for quality issues, before major refactoring, or to maintain code health. Performs module-by-module analysis on demand. (project, gitignored)
---

# Refactoring Discovery

## Overview

Systematically analyze TypeScript codebases to identify refactoring opportunities focusing on excessive responsibilities, tight coupling, low cohesion, and SOLID principle violations. Generate actionable reports with metrics-based evidence and concrete improvement proposals tailored to the project's scale and architecture.

## When to Use This Skill

Invoke this skill in the following scenarios:

1. **Periodic Code Quality Audits** - Regular (weekly/monthly) codebase health checks
2. **Pre-Feature Implementation Review** - Before adding new features, identify existing issues
3. **Root Cause Investigation** - When bugs suggest design problems
4. **Targeted Module Improvement** - Detailed analysis of specific problematic modules

## Core Capabilities

### 1. Flexible Scope Analysis

Analyze at different granularities based on your needs:

- **Project-wide**: Scan entire codebase for prioritized issue list
  ```
  "Analyze the entire project for refactoring opportunities"
  ```

- **Directory-specific**: Focus on particular modules
  ```
  "Analyze src/reporting/ for design issues"
  ```

- **File-specific**: Deep dive into individual files
  ```
  "Review src/runner/index.ts for refactoring needs"
  ```

### 2. Multiple Output Formats

Generate appropriate documentation for your workflow:

- **Markdown Report** (`assets/report-template.md`): Comprehensive analysis with metrics, priority ranking, and improvement recommendations
- **Refactoring Plan** (`assets/refactoring-plan-template.md`): Step-by-step execution plan with risk assessment and rollback strategy
- **Metrics Dashboard**: Numerical scores for complexity, coupling, and cohesion

### 3. Project-Appropriate Standards

Apply design standards that fit the project's scale and architecture:

- Reference `references/design-standards.md` for threshold values
- Avoid over-engineering small projects
- Respect YAGNI principle
- Consider project-specific patterns (e.g., pluggable architecture)

## Analysis Workflow

### Overview

The analysis follows a 7-step process with validation built in:

1. **Understand Context** - Gather project information
2. **Define Scope** - Clarify analysis boundaries
3. **Load Standards** - Apply appropriate thresholds
4. **Perform Analysis** - Multi-tool static analysis
5. **Prioritize Issues** - Calculate priority scores
6. **Validate & Re-scope** - Reduce false positives (Critical!)
7. **Generate Output** - Create appropriate deliverables

### Step 1: Understand the Context

Before analysis, gather project information:

1. **Read architecture documentation** if available
2. **Identify design patterns** (pluggable, layered, etc.)
3. **Note any project-specific standards** in CLAUDE.md or similar
4. **Understand the project scale** (library, framework, application)

### Step 2: Define Analysis Scope

Ask the user to clarify:
- Which files/directories to analyze
- Priority level (quick scan vs. deep analysis)
- Specific concerns (complexity, coupling, specific SOLID violations)

### Step 3: Load Design Standards

Read `references/design-standards.md` to understand thresholds:

- Cyclomatic complexity limits
- Coupling metrics (imports, fan-out)
- Cohesion metrics (LCOM4)
- LOC thresholds
- Responsibility count guidelines

### Step 4: Perform Static Analysis

Execute multi-tool analysis chain for comprehensive code quality assessment:

#### 4.1 Code Pattern Discovery (KIRI MCP)

Use KIRI for efficient codebase exploration:

```typescript
// Find high-complexity functions
mcp__kiri__context_bundle({
  goal: "complex functions high cyclomatic complexity nested conditionals switch statements"
})

// Find coupling issues
mcp__kiri__context_bundle({
  goal: "import statements concrete dependencies circular imports"
})

// Find change hotspots (combine with git analysis)
mcp__kiri__files_search({
  query: "frequently modified high churn"
})
```

#### 4.2 TypeScript AST Analysis (Recommended: ts-morph)

For precise metrics, use ts-morph or TypeScript Compiler API:

```typescript
import { Project } from 'ts-morph';

const project = new Project({ tsConfigFilePath: 'tsconfig.json' });

// Analyze complexity
sourceFile.getFunctions().forEach(fn => {
  const cc = calculateCyclomaticComplexity(fn);
  const cognitive = calculateCognitiveComplexity(fn);
  const loc = fn.getEndLineNumber() - fn.getStartLineNumber();
});

// Analyze type complexity
sourceFile.getTypeAliases().forEach(type => {
  const depth = getConditionalTypeDepth(type);
  const genericCount = type.getTypeParameters().length;
});

// Analyze decorators
sourceFile.getClasses().forEach(cls => {
  const decoratorDepth = cls.getDecorators().length;
});
```

#### 4.3 Dependency Analysis (depcruise / madge)

Detect architectural issues:

```bash
# Using depcruise to find circular dependencies
npx depcruise --config .dependency-cruiser.js src

# Using madge for visual dependency graph
npx madge --circular --extensions ts src/

# Generate instability metrics (Afferent/Efferent coupling)
npx depcruise --output-type metrics src
```

#### 4.4 Dead Code Detection (ts-prune / ts-unused-exports)

Find unused exports:

```bash
# Find unused exports
npx ts-prune

# Find unused dependencies
npx depcheck
```

#### 4.5 Git Change Analysis

Correlate code metrics with change history:

```bash
# Find change hotspots
git log --format=format: --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# Find co-changing files (change coupling)
git log --format=format: --name-only | awk '/^$/ { if (NR > 1) print ""; next } { print }' | sort | uniq -c

# Find files by churn rate
git log --all -M -C --name-only --format='format:' "$@" | sort | uniq -c | sort -rn
```

#### 4.6 Coverage Correlation

Cross-reference complexity with test coverage:

```bash
# Generate coverage report
npx vitest run --coverage

# Identify high-complexity, low-coverage files (high risk)
# Complexity > 10 AND Coverage < 80%
```

#### Evaluation Criteria by Tool

For each file/module, synthesize findings:

1. **Complexity** (ts-morph + ESLint):
   - Cyclomatic complexity per function
   - Cognitive complexity (preferred)
   - TypeScript-specific: conditional types, generics, decorators
   - Total complexity per file
   - Nesting depth

2. **Coupling** (depcruise + KIRI):
   - Import count (adjust for barrel imports)
   - Concrete type dependencies vs. interfaces
   - Circular dependencies
   - Instability metric (Afferent/Efferent)
   - Change coupling (git analysis)

3. **Cohesion** (ts-morph + manual review):
   - LCOM4 calculation
   - Related methods grouped together
   - Field usage patterns
   - Responsibility focus

4. **Dead Code** (ts-prune):
   - Unused exports
   - Unreachable code
   - Orphaned types

5. **Architecture** (depcruise):
   - Layer violations
   - Dependency rule compliance
   - Module boundaries

6. **SOLID Violations** (KIRI + patterns):
   - Reference `references/refactoring-patterns.md` for detection patterns
   - Look for common smells (God classes, switch statements, fat interfaces)

### Step 5: Prioritize Issues

Calculate priority score using **Impact × Ease of Fix × Risk Reduction**:

#### Priority Formula

**Priority Score = (Impact × Risk Reduction) / Effort**

Where:
- **Impact** (1-10): Maintainability effect, bug likelihood, team velocity impact
- **Risk Reduction** (1-10): How much this fixes reduces system risk
  - Consider: Bug history, change frequency, blast radius
- **Effort** (1-10): Time to fix, dependency complexity, test requirements

#### Priority Categories

- **🔴 Critical** (Score ≥ 50): Immediate action required
  - Circular dependencies
  - Architecture violations (layer violations)
  - High complexity + low coverage + bug history
  - Change hotspots with >20 modifications/month

- **🟡 Medium** (Score 20-49): Schedule in next 1-2 sprints
  - SOLID violations affecting extensibility
  - High coupling in stable modules (Instability > 0.8)
  - Dead code with >2 release cycles unused
  - Medium complexity + low coverage

- **🟢 Low** (Score < 20): Nice-to-have improvements
  - Minor style inconsistencies
  - Moderate complexity improvements
  - Documentation enhancements

#### Contextual Factors

Also consider:
1. **Bug correlation**: Files with past bugs get +20 to impact
2. **Change frequency**: High churn files get +15 to risk reduction
3. **Test coverage**: Coverage < 50% gets +10 to risk reduction
4. **Blast radius**: Core modules get +10 to impact
5. **Team knowledge**: Well-known areas get -5 to effort

### Step 6: Validate and Re-scope (Critical Step)

Before generating final output, validate findings to reduce false positives:

#### 6.1 Sample Validation

1. **Select representative samples**:
   - Top 3 critical issues
   - 5 random medium issues
   - 2 low-priority issues

2. **Manual review**:
   - Verify metrics are correctly calculated
   - Check if context justifies the violation
   - Confirm recommendations are actionable

3. **False positive identification**:
   - Framework patterns (e.g., NestJS decorators) flagged incorrectly
   - Test files with legitimate high complexity
   - Generated code or migrations
   - Barrel imports counted as high coupling

#### 6.2 Threshold Adjustment

If false positive rate > 20%:

1. **Re-calibrate thresholds**:
   - Use statistical normalization (median + 2σ)
   - Apply layer-specific thresholds
   - Exclude framework patterns

2. **Re-run analysis** with adjusted parameters

3. **Document adjustments** in report

#### 6.3 Stakeholder Confirmation

For critical findings, verify with:
- File authors (git blame)
- Recent contributors
- Domain experts

Quick validation questions:
- "This file has CC=25. Is this intentional?"
- "These modules co-change often. Is this expected?"
- "This code is unused. Safe to remove?"

#### 6.4 Evidence Collection

For each confirmed issue, collect:
- **Detection query** used (KIRI, git command, tool output)
- **Metric values** (before/after thresholds)
- **Code snippets** showing the issue
- **Tool screenshots** or output
- **Git history** if relevant

This evidence trail ensures report credibility and helps future audits.

### Step 7: Generate Appropriate Output

Based on user needs and validated findings, generate:

#### For Periodic Audits → Markdown Report

Use `assets/report-template.md`:
- Executive summary with health score
- Findings by priority
- Metrics summary tables
- Top 10 files requiring attention
- Recommended refactoring sequence

#### For Specific Module Improvement → Refactoring Plan

Use `assets/refactoring-plan-template.md`:
- Problem statement with root cause
- Goals and success criteria
- Step-by-step refactoring phases
- Testing strategy
- Risk assessment
- Metrics tracking (before/after)

#### For Quick Review → Summary Format

Concise list:
- File path and issue type
- Key metrics
- One-line recommendation

## Reference Materials

### Design Standards (`references/design-standards.md`)

Comprehensive thresholds for:
- Function/method complexity (CC ≤ 10)
- Class/module complexity (Total CC ≤ 50)
- Coupling metrics (≤ 8 imports, ≤ 4 concrete deps)
- Cohesion metrics (LCOM4 ≤ 0.2)
- LOC thresholds (functions ≤ 40, files ≤ 400)
- Responsibility count ("1 primary + 1 auxiliary max")

Load this file when performing analysis to apply consistent criteria.

### Refactoring Patterns (`references/refactoring-patterns.md`)

Detailed patterns for addressing:
- **SRP violations**: God classes → Extract responsibilities
- **OCP violations**: Switch statements → Strategy pattern
- **LSP violations**: Contract violations → Composition over inheritance
- **ISP violations**: Fat interfaces → Interface segregation
- **DIP violations**: Concrete dependencies → Dependency injection

Common code smells:
- Long methods → Extract method
- Long parameter lists → Parameter object
- Feature envy → Move method
- Primitive obsession → Value objects

Load this file when recommending specific refactoring techniques.

## Example Usage Scenarios

### Scenario 1: Periodic Quality Check

**User**: "Analyze the entire project for refactoring opportunities"

**Process**:
1. Read `references/design-standards.md`
2. Run multi-tool analysis:
   - KIRI for code pattern search
   - depcruise for dependency graph
   - ts-prune for dead code
   - Git analysis for change coupling
3. Calculate priority scores (Impact × Risk / Effort)
4. Sample-validate top findings (reduce false positives)
5. Generate Markdown report using `assets/report-template.md` with evidence
6. Include tool versions and statistical baseline

### Scenario 2: Bug Root Cause Investigation

**User**: "I found a bug in src/runner/index.ts - is there a design problem?"

**Process**:
1. Read `references/design-standards.md` and `references/refactoring-patterns.md`
2. Use ts-morph to analyze the specific file
3. Check complexity and coupling metrics
4. Run git blame and churn analysis
5. Identify root cause (e.g., SRP violation, high coupling)
6. Validate findings with file author
7. Generate refactoring plan using `assets/refactoring-plan-template.md` with evidence trail

### Scenario 3: Pre-Feature Review

**User**: "Before implementing the new feature, check src/adapters/ for issues"

**Process**:
1. Read design standards
2. Analyze all files in src/adapters/
3. Check for consistent patterns
4. Identify potential extension points
5. Generate medium-priority report focused on extension readiness

## Best Practices

### DO:
- ✅ Consider project scale and architecture
- ✅ Apply thresholds from `design-standards.md`
- ✅ Provide concrete code examples
- ✅ Prioritize by impact and effort
- ✅ Reference specific patterns from `refactoring-patterns.md`
- ✅ Use KIRI for efficient codebase search

### DON'T:
- ❌ Suggest over-engineering for small projects
- ❌ Apply enterprise patterns blindly
- ❌ Ignore project-specific architecture
- ❌ Recommend refactoring without clear benefit
- ❌ Forget YAGNI principle
- ❌ Propose changes that break existing tests

## Output Quality Standards

All reports should include:

1. **Metrics-based evidence**: Specific numbers (CC, LCOM4, LOC)
2. **File locations**: Exact paths and line numbers
3. **Concrete examples**: Code snippets showing issues
4. **Actionable recommendations**: Specific patterns to apply
5. **Priority ranking**: Clear indication of urgency
6. **Risk assessment**: Consider impact of changes

## Integration with Development Workflow

### With Code Reviews
- Run analysis before PR submission
- Include metrics in PR description
- Use findings to guide review focus

### With Sprint Planning
- Generate reports at sprint start
- Allocate refactoring time based on priorities
- Track metrics sprint-over-sprint

### With Codex Review
- After generating report, request Codex review
- Incorporate Codex suggestions
- Validate thresholds with Codex expertise

## Resources Summary

### References (Load into context as needed)
- `references/design-standards.md` - Metrics thresholds and project standards
- `references/refactoring-patterns.md` - SOLID violations and refactoring techniques

### Assets (Use in output generation)
- `assets/report-template.md` - Comprehensive Markdown report template
- `assets/refactoring-plan-template.md` - Step-by-step refactoring plan template

These resources ensure consistent, high-quality analysis tailored to your project's needs.
