---
name: general-development
description: General software development practices including code review, testing strategies, and CI/CD integration. Use when implementing features, writing tests, setting up deployment pipelines, or conducting peer reviews.
license: MIT
metadata:
  author: devrecruit
  version: "1.0"
---

# General Development Skills

This skill provides best practices for core software development workflows including code reviews, testing, and continuous integration/deployment.

## Code Review Practices

### Purpose

Maintain code quality and knowledge sharing through effective peer reviews.

### Guidelines

1. **Review Process**

   - Review PRs within 24 hours when possible
   - Check for logic errors, edge cases, and code clarity
   - Verify tests are included for new functionality
   - Ensure documentation is updated when needed

2. **Providing Feedback**

   - Use constructive language and specific suggestions
   - Highlight what was done well, not just issues
   - Ask clarifying questions rather than making assumptions
   - Request changes only for critical issues; suggest improvements for non-blocking issues

3. **Checklist**
   - Code follows project style guide and conventions
   - Changes are properly tested
   - Documentation is complete
   - No hardcoded credentials or sensitive data
   - Performance implications considered
   - Dependencies are necessary and up-to-date

### Example

When reviewing a feature branch, check that:

- All tests pass
- Code coverage doesn't decrease
- No console.log statements remain
- Type safety is maintained

## Testing Strategies

### Purpose

Ensure application reliability and prevent regressions through comprehensive testing.

### Testing Levels

1. **Unit Tests**

   - Test individual functions and components in isolation
   - Use mocking for external dependencies
   - Aim for high coverage of business logic
   - Keep tests focused and readable

2. **Integration Tests**

   - Test component interactions and data flows
   - Verify API endpoints with realistic data
   - Test database operations and queries
   - Check error handling across components

3. **End-to-End Tests**
   - Test critical user journeys
   - Use browser automation for UI testing
   - Verify full workflow from input to output
   - Keep E2E tests lean and focused

### Best Practices

- Write tests alongside code during development
- Use descriptive test names that explain what is being tested
- Keep tests DRY while maintaining clarity
- Run tests locally before pushing
- Maintain test data fixtures

## CI/CD Integration

### Purpose

Automate code quality checks and deployment processes for faster, safer releases.

### Pipeline Stages

1. **Build Stage**

   - Compile/transpile code
   - Generate artifacts
   - Fail fast on compilation errors

2. **Test Stage**

   - Run unit and integration tests
   - Perform linting and code quality checks
   - Generate coverage reports
   - Fail on coverage thresholds

3. **Security Stage**

   - Scan dependencies for vulnerabilities
   - Check for secrets in code
   - Perform static analysis

4. **Deploy Stage**
   - Run E2E tests against staging
   - Deploy to staging environment
   - Run smoke tests
   - Deploy to production (with approvals if needed)

### Recommended Tools

- GitHub Actions for CI/CD orchestration
- ESLint for code linting
- Vitest/Jest for testing
- SonarQube for code quality metrics
- Dependabot for dependency updates

### Example Workflow

```yaml
- Trigger: Push to main or PR opened
- Build: Install dependencies, compile code
- Lint: Run ESLint, check formatting
- Test: Run unit and integration tests
- Security: Scan dependencies
- Deploy: Deploy to staging/production (with approvals)
```
