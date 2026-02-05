---
name: code-quality-pipeline
description: "Systematic code quality improvement workflow combining smart-reviewer and test-generator MCP tools with Pareto 80/20 auto-fixes, severity-based review, and comprehensive test generation. Use when p..."
---

# Code Quality Workflow for @j0kz/mcp-agents

Systematic approach to improving code quality using smart-reviewer and test-generator MCP tools.

## When to Use This Workflow

- **Before creating pull request** - Pre-PR quality gate
- **After significant refactoring** - Verify no regressions
- **During codebase audits** - Systematic quality improvement
- **When CI/CD quality checks fail** - Fix issues systematically
- **Adding new features** - Ensure quality from start

## 5-Step Quality Pattern

```
1. Initial Assessment → Identify files needing review
2. Smart Review → Categorize issues (critical/moderate/minor)
3. Auto-Fix (Pareto 80/20) → Apply safe fixes automatically
4. Generate Tests → Cover untested code
5. Re-Review → Verify improvements
```

## Quick Start

### For Changed Files (Pre-PR)
```bash
# Get changed files
git diff --name-only main...HEAD | grep -E '\.(ts|js)$'
```

### Batch Review
```javascript
Tool: batch_review
Input: {
  "filePaths": ["file1.ts", "file2.ts"],
  "config": { "severity": "strict" }
}
```

### Apply Auto-Fixes
```javascript
Tool: apply_auto_fixes
Input: {
  "filePath": "src/module.ts",
  "safeOnly": true  // Always true for automation
}
```

### Generate Tests
```javascript
Tool: write_test_file
Input: {
  "sourceFile": "src/module.ts",
  "config": {
    "framework": "vitest",
    "coverage": 80
  }
}
```

## Severity Configuration

| Level | Use For | What It Flags |
|-------|---------|---------------|
| **strict** | Production, APIs, Security | ALL vulnerabilities, type violations, complexity >50 |
| **moderate** | Standard development, PRs | Critical issues, complexity >70, major gaps |
| **lenient** | Prototypes, experiments | Only severe issues, breaking errors |

**For detailed severity configuration:**
```bash
cat .claude/skills/code-quality-pipeline/references/severity-config-guide.md
```

## Auto-Fix with Pareto Principle

**Key Insight:** 20% of fixes resolve 80% of issues

### Safe Auto-Fixes (Apply Automatically)
- Formatting & indentation
- Import organization
- Unused code removal
- Simple type fixes
- Naming consistency

### Manual Fixes (Review Required)
- Logic changes
- Refactoring suggestions
- Architecture improvements
- Complex type inference

**For complete auto-fix patterns:**
```bash
cat .claude/skills/code-quality-pipeline/references/auto-fix-patterns.md
```

## Test Generation

### Configuration
```javascript
{
  "framework": "vitest",      // Standard for @j0kz
  "includeEdgeCases": true,   // Boundary conditions
  "includeErrorCases": true,  // Error paths
  "coverage": 80              // Target percentage
}
```

### What Gets Generated
- Unit tests for functions
- Edge cases (null, empty, boundaries)
- Error handling tests
- Async operation tests
- Mock setups

**For test generation details:**
```bash
cat .claude/skills/code-quality-pipeline/references/test-generation-guide.md
```

## Common Patterns

### Pattern 1: Fast Pre-Commit
```
Time: 1-2 minutes
1. Review staged files (moderate)
2. Apply safe auto-fixes
3. Run tests
```

### Pattern 2: Comprehensive Pre-PR
```
Time: 5-15 minutes
1. Review all changes (strict)
2. Auto-fix safe issues
3. Manual fix critical issues
4. Generate missing tests
5. Verify coverage >75%
```

### Pattern 3: Legacy Code Improvement
```
Time: 30-60 minutes
1. Review with moderate severity
2. Apply all safe fixes
3. Fix critical issues manually
4. Generate test suite
5. Re-review for verification
```

**For complete workflow examples:**
```bash
cat .claude/skills/code-quality-pipeline/references/complete-workflow-examples.md
```

## Expected Outcomes

### After Auto-Fix (Safe Only)
```
Issues: -73% average reduction
Formatting: 100% consistent
Imports: 100% organized
Dead code: 100% removed
```

### After Full Pipeline
```
Critical issues: 0
Complexity: <50
Coverage: >75%
Maintainability: >80
```

## Issue Priority Guide

### Critical (Fix Before Merge)
- Security vulnerabilities
- Type safety violations
- Resource leaks
- Null/undefined errors

### Moderate (Fix If Time)
- High complexity (>70)
- Missing documentation
- Performance issues
- Duplicate code

### Minor (Future Cleanup)
- Style preferences
- Micro-optimizations
- Comment improvements

## Integration with Other Tools

### With orchestrator-mcp
```javascript
Tool: run_workflow
Input: {
  "workflow": "pre-merge",
  "params": { "files": ["..."] }
}
```

### With modular-refactoring
After quality pipeline, if complexity >50:
- Apply modular-refactoring-pattern
- Split files >300 LOC
- Extract to helpers/utils

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Too many issues" | Use auto-fix for 80% reduction |
| "Tests failing" | Check if bugs found (good!) or mocks needed |
| "Auto-fix broke code" | Restore from .backup/, use safeOnly=true |
| "Inconsistent results" | Check severity level appropriateness |

## Quick Commands

```bash
# After quality improvements
npm test                         # Run tests
npm run test:coverage            # Check coverage
npm run update:test-count        # Update badges
git diff                         # Review changes
```

## Related Skills

- **mcp-workflow-composition:** Orchestrate multiple tools
- **modular-refactoring-pattern:** Reduce complexity
- **testing-patterns-vitest:** Deep testing guidance

## Scripts Available

Check the `scripts/` directory for automation:
```bash
ls .claude/skills/code-quality-pipeline/scripts/
```

---

**For project standards:** `.claude/skills/project-standardization/SKILL.md`
**For workflow orchestration:** `.claude/skills/mcp-workflow-composition/SKILL.md`