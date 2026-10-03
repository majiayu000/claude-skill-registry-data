---
name: code-review
description: Conduct effective code reviews that improve code quality, share knowledge, and maintain team standards. Focus on constructive feedback and learning.
triggers:
- /code review
- /review code
---

# Code Review Best Practices

This skill guides you through conducting effective code reviews that improve code quality, share knowledge, and maintain team standards.

## When to use this skill

Use this skill when you need to:
- Review pull requests from team members
- Establish code review processes
- Provide constructive feedback on code
- Learn from reviewing others' code
- Maintain code quality standards

## Prerequisites

- Understanding of the codebase and architecture
- Knowledge of team coding standards
- Familiarity with the feature being implemented
- Time to provide thorough, thoughtful review

## Guidelines

### Review Principles

**Purpose of Code Review**
- Catch bugs and issues early
- Share knowledge across the team
- Maintain coding standards
- Improve overall code quality
- Mentor junior developers

**Reviewer Mindset**
- Assume positive intent
- Ask questions rather than dictate
- Explain the "why" behind suggestions
- Distinguish between required changes and suggestions
- Acknowledge good code and clever solutions

### Review Checklist

**Code Quality**
- [ ] Code follows SOLID principles
- [ ] Functions are small and focused
- [ ] Variable names are descriptive
- [ ] Error handling is appropriate
- [ ] Edge cases are considered
- [ ] No obvious bugs or logic errors

**Security**
- [ ] No hardcoded secrets or credentials
- [ ] Input validation is present
- [ ] SQL injection risks are mitigated
- [ ] Authentication/authorization is correct
- [ ] Sensitive data is handled properly

**Performance**
- [ ] No obvious performance bottlenecks
- [ ] Database queries are optimized
- [ ] Unnecessary computations are avoided
- [ ] Resource usage is reasonable
- [ ] Caching is used appropriately

**Maintainability**
- [ ] Code is readable and well-commented
- [ ] Documentation is updated
- [ ] Tests are included and passing
- [ ] No code duplication (DRY principle)
- [ ] Complexity is appropriate

### Review Process

**Before Reviewing**
1. Understand the context (ticket, requirements)
2. Check if tests are included
3. Verify CI/CD checks pass
4. Review commit messages for clarity

**During Review**
1. Read through the entire change first
2. Understand the "what" and "why"
3. Look for patterns, not just individual lines
4. Use inline comments for specific issues
5. Use summary comments for general feedback

**Comment Categories**
```
[MUST]  - Must be fixed before merging
[SHOULD] - Should be fixed, but can be addressed later
[NIT]    - Minor suggestion, author's choice
[QUESTION] - Seeking clarification
[PRAISE] - Good work worth highlighting
```

### Providing Feedback

**Constructive Comments**
```
❌ "This is wrong."
✅ "Consider using a switch statement here for better readability 
    as the number of conditions grows."

❌ "Fix this."
✅ "This function is getting quite long. Could we extract the 
    validation logic into a separate function?"
```

**Tone Guidelines**
- Be respectful and professional
- Focus on the code, not the person
- Explain reasoning behind suggestions
- Offer alternatives, not just criticism
- Be open to discussion

### Responding to Reviews

**As Author**
- Respond to all comments
- Don't take feedback personally
- Ask for clarification when needed
- Push back respectfully if you disagree
- Fix issues promptly

**Handling Disagreements**
- Discuss offline if thread gets long
- Involve a third party if needed
- Document decisions for future reference
- Prioritize team consistency

### Automation Support

**Tools to Leverage**
- Linting (ESLint, pylint, go vet)
- Static analysis (SonarQube, CodeQL)
- Security scanning (Snyk, Trivy)
- Formatting (prettier, gofmt)
- Test coverage reports

**Automate the Obvious**
- Style violations → linter
- Common bugs → static analysis
- Security issues → security scanner
- Human reviewers → focus on architecture and logic

## Examples

See the `examples/` directory for:
- `review-template.md` - PR review template
- `good-review-comments.md` - Examples of effective comments
- `review-etiquette.md` - Team code review guidelines
- `checklist.md` - Comprehensive review checklist

## References

- [Google code review guidelines](https://google.github.io/eng-practices/review/)
- [Microsoft code review guide](https://docs.microsoft.com/azure/devops/repos/git/pull-requests?view=azure-devops)
- [Code review best practices](https://www.atlassian.com/agile/software-development/code-reviews)
- [How to do a code review](https://osm.etsi.org/wikipub/index.php/How_to_do_a_code_review)
