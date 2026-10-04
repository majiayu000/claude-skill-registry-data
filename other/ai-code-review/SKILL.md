---
name: ai-code-review
description: "AI-powered code review with security scanning, performance analysis, and best practices checking. Supports multiple languages and frameworks."
triggers:
  - "review code"
  - "code review"
  - "检查代码"
  - "代码审查"
  - "security scan"
---

# AI Code Review

Intelligent code review with security, performance, and quality analysis.

## Features

- 🔒 **Security Scanning** — OWASP Top 10, CVE detection
- ⚡ **Performance Analysis** — Bottleneck detection
- 📏 **Best Practices** — Language-specific patterns
- 🧪 **Test Coverage** — Missing test detection
- 📝 **Documentation** — JSDoc/docstring completeness

## Usage

### Review Pull Request

```bash
# Review current PR
hermes review pr

# Review specific PR
hermes review pr --number 123

# Review with custom rules
hermes review pr --rules security,performance
```

### Review Files

```bash
# Review single file
hermes review file src/auth.ts

# Review directory
hermes review dir src/

# Review with severity filter
hermes review dir src/ --severity high,critical
```

### Review Modes

```bash
# Quick review (fast, basic checks)
hermes review --mode quick

# Deep review (thorough, all checks)
hermes review --mode deep

# Security-focused review
hermes review --mode security
```

## Analysis Categories

### Security

| Check | Description | Severity |
|-------|-------------|----------|
| SQL Injection | Raw SQL queries | Critical |
| XSS | Unescaped output | High |
| CSRF | Missing tokens | High |
| Secrets | Hardcoded credentials | Critical |
| Dependencies | Vulnerable packages | High |

### Performance

| Check | Description | Impact |
|-------|-------------|--------|
| N+1 Queries | Database loops | High |
| Memory Leaks | Unclosed resources | Medium |
| Bundle Size | Large imports | Medium |
| Caching | Missing cache | Low |

### Quality

| Check | Description | Category |
|-------|-------------|----------|
| Complexity | High cyclomatic complexity | Maintainability |
| Duplication | Code duplication | Maintainability |
| Naming | Poor variable names | Readability |
| Documentation | Missing docs | Documentation |

## Output Format

```markdown
## Code Review Report

### Summary
- Files reviewed: 15
- Issues found: 8
- Critical: 2 | High: 3 | Medium: 2 | Low: 1

### Critical Issues

#### 1. SQL Injection in `user.ts:45`
```typescript
// ❌ Vulnerable
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Fixed
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### Suggestions

#### Performance: Cache API response in `api.ts:23`
Consider adding Redis cache for frequently accessed data.
```

## Configuration

```yaml
# .hermes-review.yml
rules:
  security:
    enabled: true
    severity: [critical, high]
  
  performance:
    enabled: true
    thresholds:
      complexity: 10
      function_length: 50
  
  quality:
    enabled: true
    require_docs: true

ignore:
  - "**/test/**"
  - "**/node_modules/**"
  - "**/*.test.ts"
```

## Integration

### GitHub Actions

```yaml
- uses: clowlove/hermes-review@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    rules: security,performance
    comment: true
```

### Pre-commit Hook

```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: hermes-review
        name: AI Code Review
        entry: hermes review file
        language: system
        files: \.(ts|js|py)$
```

## Pitfalls

1. **False Positives** — AI may flag valid patterns, review manually
2. **Context Missing** — AI may not understand business logic
3. **Performance** — Deep review takes longer, use quick mode for CI
4. **Privacy** — Code is sent to AI provider, check company policy
