---
name: context-analysis
description: Establish comprehensive understanding of project structure, architecture, dependencies, and current state before conducting detailed code review. Use as the.
---

# Code Review - Context Analysis

Establish comprehensive understanding of the project before conducting detailed code review. This skill is **Phase 1** of the 6-phase code review methodology.

## When to Use This Skill

Use this skill when you need to:

- Begin a comprehensive code review
- Onboard to an unfamiliar codebase
- Understand project architecture and design decisions
- Identify technical debt before detailed review
- Map dependencies and potential risks
- Plan follow-up review phases

**Trigger phrases**: "code review", "analyze codebase", "understand architecture", "project analysis", "technical due diligence", "codebase overview", "onboarding"

## Review Mode Detection

This skill supports two modes:

- **Full Codebase**: Analyze the entire project structure, architecture, and dependencies
- **Git Changes**: Scope analysis to current git changes and their surrounding context

## What This Skill Does

### Analysis Areas

1. **Repository Discovery**
   - Directory structure analysis
   - Key files identification
   - Documentation review

2. **Architecture Understanding**
   - Entry points identification
   - Design patterns recognition
   - Module dependency mapping

3. **Dependency Analysis**
   - External dependency listing
   - Security vulnerability scan
   - Outdated package detection

4. **Build & Deployment**
   - Build system review
   - CI/CD configuration
   - Environment setup

5. **Codebase Metrics**
   - Lines of code
   - Complexity metrics
   - Code duplication

## Instructions

### Step 1: Determine Review Mode

**Full Codebase Mode:**
```bash
# Get directory structure
tree -L 3 -I 'node_modules|venv|.venv|__pycache__|target|build'

# Identify key files
ls -la

# Read documentation
cat README.md
cat CONTRIBUTING.md
```

**Git Changes Mode (Preflight):**
```bash
# Scope the changes
git status -sb
git diff --stat
git diff

# Find related modules and usages
rg "function_name" --type-add 'src:*.{py,js,ts,java,go,cs,cpp}'
```

### Edge Case Handling

- **No changes detected**: Inform the user and ask if they want to review staged changes (`git diff --cached`) or a specific commit range
- **Large diff (>500 lines)**: Summarize changes by file first, then batch analysis by module or feature area
- **Mixed concerns**: Group findings by logical feature rather than file order

### Step 2: Architecture Analysis

1. **Identify Entry Points**
   - Look for main.py, index.js, Application.java
   - Find CLI entry points
   - Locate API endpoints

2. **Map Design Patterns**
   - MVC, layered architecture
   - Repository pattern
   - Factory, singleton patterns

3. **Trace Dependencies**
   - Internal module imports
   - External library usage

4. **Identify Critical Paths**
   - Authentication and authorization flows
   - Payment or financial operations
   - Data writes and mutations
   - Network boundaries and external API calls

### Step 3: Dependency Health Check

```bash
# Python
pip-audit
pip list --outdated

# JavaScript
npm audit
npm outdated

# Java
mvn versions:display-dependency-updates
```

### Step 4: Generate Context Report

Create a report with:
- Executive summary
- Project structure
- Architecture analysis
- Dependency health
- Key findings
- Review focus recommendations

## Output Template

```markdown
# Code Review Context Analysis Report

**Project**: [Name]
**Date**: [Date]
**Reviewer**: [Name]
**Mode**: [Full Codebase / Git Changes]

## Executive Summary
- **Project Purpose**: [Description]
- **Primary Language**: [Language]
- **Architecture Style**: [Pattern]

## Project Structure
[Directory tree]

## Key Components
- Entry Points: [List]
- Core Modules: [List]
- External Interfaces: [APIs, CLI]
- Critical Paths: [Auth, payments, data writes, network]

## Dependency Health
- Total Dependencies: [Count]
- Outdated: [Count]
- Vulnerabilities: [Count]

## Key Findings
### Strengths
1. [Finding]

### Concerns
1. [Finding]

## Recommendations for Review Focus
1. [Area] - [Reason]
```

## Quality Checklist

- [ ] Repository structure documented
- [ ] Entry points identified
- [ ] Architecture patterns recognized
- [ ] Dependencies analyzed
- [ ] Vulnerabilities checked
- [ ] Critical paths mapped
- [ ] Metrics collected
- [ ] Context report generated

## Related Skills

- `code-quality` - Code quality + SOLID + dead code review (Phase 2)
- `security-review` - Security analysis, 10-domain model (Phase 3)
- `performance-review` - Performance analysis (Phase 4)
- `testing-review` - Test assessment (Phase 5)
- `final-report` - Consolidated report with verdict (Phase 6)

---

**Version**: 2.0.0
**Last Updated**: February 2026
**Based on**: DevAI-Hub code review methodology + code-review-expert


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
