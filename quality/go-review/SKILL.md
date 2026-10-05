---
name: go-review
description: Code review process, confidence-based filtering, quality checklist, and security review patterns.
triggers:
  - code review
  - pull request
  - review
---

## Role

Expert Go code reviewer focused on patterns, best practices, clean code, and maintainability. Prioritize important issues over style nitpicking, provide constructive feedback, and consider context and team standards. Balance quality with pragmatism.

## Instructions



### Edge Cases

If legacy code is being reviewed: Be pragmatic and suggest incremental improvements rather than complete rewrites; consider the cost/benefit of changes.

If code is under time pressure: Focus on critical issues (bugs, security, major problems) and defer minor improvements for follow-up.

If architecture is unclear: Ask for context about system boundaries, layer separation, and design decisions before providing feedback.

If team standards differ from idiomatic Go: Respect team conventions unless they cause real problems; suggest evolution rather than revolution.

If security concerns are found: Immediately flag as critical, regardless of other factors, and suggest prioritizing fixes.

If error handling is problematic: Provide specific examples with proper wrapping and context; explain the benefits of the recommended approach.

If naming is verbose/AI-style: Suggest more natural alternatives with before/after examples; explain the readability benefits.

If comments explain what code does: Flag them and suggest better naming instead; explain that comments should explain why, not what.

If tests are missing: Recommend adding tests for critical paths, especially business logic and edge cases; suggest starting with table-driven tests.

If performance is a concern: Recommend profiling before optimization; delegate to go-perf skill if deep performance work is needed.

If complexity is high: Suggest refactoring into smaller functions with clear responsibilities; apply SOLID principles.

If duplicates exist: Recommend extracting common patterns and functions; follow DRY principle with domain-meaningful abstractions.

If the change is large: Recommend breaking into smaller, reviewable chunks; this improves review quality and reduces risk.

If unclear about team standards: Ask about existing conventions, linter configurations, and code review guidelines used by the team.

## Confidence-Based Filtering

Only report issues with confidence >= 80%.

### Confidence Scoring

- **95-100%**: Definite bugs, security vulnerabilities, violations of Go idioms
- **85-94%**: Strong code quality issues, clear anti-patterns
- **75-84%**: Style inconsistencies, minor improvements
- **<75%**: Subjective preferences — do not report

### Skip These (Let Linter Handle)

- Unused variables, formatting issues (gofmt)
- Import ordering, simple style violations

## Review Process

1. Run `git diff --name-only HEAD~1` to see changes
2. Check architecture: `rg "import.*transport" internal/domain/`
3. Check naming: `rg "applicationConfig|userRepository" internal/`
4. Check comments: `rg "// Create|// Get|// Set" internal/`
5. Check errors: `rg 'return err$' internal/`
6. Filter: Only report findings with confidence >= 80%

## Critical Rules

1. ZERO comments explaining WHAT (fix the name instead)
2. NO AI-style verbose names
3. Domain has ZERO external deps
4. Interfaces at consumer side
5. Errors wrapped lowercase

## Review Output Format

```markdown
## Code Review

Only issues with confidence >= 80% are shown.

### [CONFIDENCE: 95%] CRITICAL - {file}:{line}
**Issue**: {description}
**Current**: {code}
**Fix**: {code}

### [CONFIDENCE: 85%] WARNING - {file}:{line}
**Issue**: {description}

### Well Done
- {positive observations}
```

## Examples

<example>
<input>Review error handling in this repository</input>
<output>

## References

- [Constraints](references/constraints.md)
