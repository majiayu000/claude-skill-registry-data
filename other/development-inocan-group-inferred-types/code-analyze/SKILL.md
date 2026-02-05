---
name: code-analyze
description: Analyze codebase for patterns, issues, and improvements. Enforces analysis standards while incorporating user-specific requirements.
---

# Code Analyzer Skill

## What This Skill Does

Performs standardized code analysis with user context:
- Analyzes codebase structure and patterns
- Identifies technical debt and issues
- Suggests improvements and refactoring
- Enforces coding standards
- Generates actionable reports

## When Claude Should Use This

Use this skill when the user:
- Says "analyze the code" or "review the codebase"
- Wants to find bugs or issues
- Needs architecture review
- Mentions code quality or technical debt
- Requests security or performance analysis

## Analysis Workflow

### 1. Gather User Context
```
Ask the user:
1. Focus areas? (security, performance, architecture, all)
2. Specific concerns?
3. Depth of analysis? (quick scan, standard, deep dive)
4. Output format? (report, tasks, PR comments)
```

### 2. Standardized Analysis Process

#### Phase 1: Structure Analysis
```bash
# Map codebase structure
find . -type f -name "*.ts" -o -name "*.js" | head -20

# Count lines of code
cloc . --exclude-dir=node_modules,dist,out

# Identify entry points
grep -r "export.*function\|export.*class" --include="*.ts" | head -10
```

#### Phase 2: Pattern Detection
```bash
# Find potential issues
grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.ts"

# Identify deprecated patterns
grep -r "deprecated\|@deprecated" --include="*.ts"

# Find console.logs (potential debug code)
grep -r "console\." --include="*.ts" --exclude-dir=node_modules
```

#### Phase 3: Dependency Analysis
```bash
# Check for outdated packages
npm outdated

# Audit for vulnerabilities
npm audit

# Analyze bundle size
npm ls --depth=0
```

### 3. Automated Report Generation

Generate `analysis/ANALYSIS_[DATE].md`:
```markdown
# Code Analysis Report

## Summary
- **Date**: YYYY-MM-DD
- **Scope**: [User specified focus]
- **Health Score**: X/100

## Critical Issues
1. [Issue]: [Description]
   - File: [path:line]
   - Severity: High/Medium/Low
   - Fix: [Recommendation]

## Architecture Review
- **Patterns Found**: [List]
- **Anti-patterns**: [List]
- **Suggestions**: [List]

## Technical Debt
- **Total**: X hours estimated
- **Priority Items**: [List]

## Action Items
- [ ] Fix critical security issues
- [ ] Refactor deprecated patterns
- [ ] Update dependencies
```

### 4. Integration with Git Workflow

#### For Issues Found:
```bash
# Create issue branch
git checkout -b fix/[issue-name]

# For refactoring needs
git checkout -b refactor/[component-name]

# For security fixes
git checkout -b security/[vulnerability-name]
```

### 5. Enforcement Rules

#### Must Fix (Blocking):
- Security vulnerabilities (High/Critical)
- Breaking changes in dependencies
- Memory leaks
- Exposed secrets/credentials

#### Should Fix (Warning):
- Deprecated API usage
- Performance bottlenecks
- Code duplication > 50 lines
- Circular dependencies

#### Consider Fixing (Info):
- TODO/FIXME comments
- Missing documentation
- Complex functions (cyclomatic > 10)
- Long files (> 500 lines)

## Analysis Types

### 1. Security Analysis
```bash
# Check for secrets
grep -r "api[_-]key\|password\|secret\|token" --include="*.ts"

# Review authentication
grep -r "authenticate\|authorize\|jwt\|session" --include="*.ts"

# Check HTTPS usage
grep -r "http://" --include="*.ts"
```

### 2. Performance Analysis
```bash
# Find potential bottlenecks
grep -r "for.*for\|while.*while" --include="*.ts"

# Check for synchronous operations
grep -r "readFileSync\|execSync" --include="*.ts"

# Identify heavy operations
grep -r "sort\|filter.*map\|reduce" --include="*.ts"
```

### 3. Architecture Analysis
- Component coupling
- Layer violations
- Dependency cycles
- Interface segregation
- Single responsibility

## Output Actions

### 1. Create Fix Branches
For each critical issue:
```bash
git checkout -b fix/[issue-id]
echo "Fix plan" > fixes/[issue-id].md
```

### 2. Generate Tasks
Create `tasks/FIXES_[DATE].md`:
```markdown
## Critical Fixes Required

### HIGH Priority
- [ ] Fix SQL injection in [file:line]
- [ ] Remove hardcoded credentials in [file:line]

### MEDIUM Priority
- [ ] Refactor [component] to reduce complexity
- [ ] Update deprecated [package] usage

### LOW Priority
- [ ] Add missing documentation
- [ ] Clean up TODO comments
```

### 3. PR Templates
Generate `.github/PULL_REQUEST_TEMPLATE/fix.md`:
```markdown
## Fix for: [Issue ID]

### What was wrong?
[Description]

### How was it fixed?
[Approach]

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Security scan clean
```

## Integration with User Intent

The analyzer combines:
1. **User's specific concerns** (from prompt)
2. **Standardized checks** (always run)
3. **Codebase context** (patterns, history)
4. **Best practices** (industry standards)

Example:
- User: "Check our API for security issues"
- Analyzer: Runs standard checks + deep API security scan

## Protection Against Breaking Changes

### Allowed Fixes:
- Security patches that don't change interfaces
- Performance improvements with same behavior
- Bug fixes with tests
- Documentation updates

### Requires Approval:
- API changes
- Database schema changes
- Configuration changes
- Dependency major version updates

### Never Auto-Fix:
- Core business logic
- Authentication/Authorization
- Payment processing
- Data migrations

## Success Metrics

Analysis succeeds when:
- [ ] All critical issues identified
- [ ] Report generated with actionable items
- [ ] Fix branches created for issues
- [ ] Team understands findings
- [ ] Clear path to resolution