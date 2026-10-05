---
name: assessment-scoring
description: This skill should be used when the user asks to "score a codebase", "rate code quality", "generate assessment score", "calculate weighted score", "final assessment", or when any code-auditor agent needs to produce a scoring summary. Provides the standardized scoring methodology for code assessment reports.
---

# Assessment Scoring Methodology

## Purpose

Provide a standardized, weighted scoring system for evaluating codebases across five dimensions: Code Quality, Performance, Security, Maintainability, and Testing.

## Scoring Categories

| Category | Weight | Focus Areas |
|----------|--------|-------------|
| Code Quality | 25% | Structure, complexity, standards, error handling |
| Performance | 25% | Algorithms, rendering, async, caching |
| Security | 20% | Vulnerabilities, auth, data protection, dependencies |
| Maintainability | 20% | Organization, documentation, coupling, tech debt |
| Testing | 10% | Coverage, quality, distribution, critical paths |

## Scoring Process

1. Each category receives a raw score from 0 to 10
2. Apply positive factors (good practices found) and negative factors (issues found)
3. Multiply each raw score by its weight percentage
4. Sum weighted scores for final composite score (0-10)

## Score Calculation Template

| Category | Score | Weight | Calculation | Weighted Score |
|----------|-------|--------|-------------|----------------|
| Code Quality | X/10 | 25% | X × 0.25 | X.XX |
| Performance | X/10 | 25% | X × 0.25 | X.XX |
| Security | X/10 | 20% | X × 0.20 | X.XX |
| Maintainability | X/10 | 20% | X × 0.20 | X.XX |
| Testing | X/10 | 10% | X × 0.10 | X.XX |
| **Total** | | 100% | | **X.XX/10** |

## Score Interpretation

| Range | Rating | Description |
|-------|--------|-------------|
| 0–2 | Critical | Immediate intervention required |
| 2–4 | Poor | Significant issues affecting development |
| 4–6 | Fair | Notable issues but manageable |
| 6–8 | Good | Minor issues, well-maintained |
| 8–10 | Excellent | Industry best practices |

## Remediation Roadmap Template

### Immediate Actions (Critical/Blocker)
- Fix all critical security vulnerabilities
- Address memory leaks and resource management issues
- Resolve blocking performance bottlenecks

### Short-term (1-4 weeks)
- Reduce code duplication below 5%
- Increase test coverage to 60%
- Refactor high-complexity methods

### Long-term (1-3 months)
- Achieve 80% test coverage
- Reduce technical debt to manageable levels
- Implement missing architectural patterns

## Additional Resources

### Reference Files

For detailed scoring criteria per category, consult:
- **`references/scoring-rubrics.md`**: Detailed positive/negative scoring factors per category
- **`references/interpretation-guide.md`**: In-depth interpretation guidance and recommendation templates
