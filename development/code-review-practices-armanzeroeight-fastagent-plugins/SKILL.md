---
name: code-review-practices
description: Provides practical guidance for conducting thorough code reviews that identify issues early, promote knowledge sharing, and deliver constructive feedback. This skill should be used when reviewing pull requests, establishing team review standards, or mentoring developers on effective review practices.
---

# Code Review Practices

This skill provides guidance for conducting effective, constructive code reviews that improve code quality and team collaboration.

## Review Mindset

**Goals of code review:**
- Catch bugs and issues early
- Share knowledge across the team
- Maintain code quality standards
- Improve code maintainability
- Foster learning and growth

**Not goals:**
- Assert dominance or superiority
- Enforce personal preferences
- Block progress unnecessarily
- Nitpick without value

## What to Review

### 1. Correctness

**Does the code work as intended?**
- Logic is sound
- Edge cases are handled
- Error conditions are managed
- Requirements are met

### 2. Design and Architecture

**Does it fit the system?**
- Follows existing patterns
- Appropriate abstractions
- Reasonable complexity
- Scalable approach

### 3. Readability

**Can others understand it?**
- Clear naming
- Logical organization
- Appropriate comments
- Consistent style

### 4. Testing

**Is it adequately tested?**
- Tests exist for new code
- Edge cases covered
- Tests are maintainable
- Integration points tested

### 5. Security

**Are there security concerns?**
- Input validation
- Authentication/authorization
- Sensitive data handling
- Known vulnerabilities

### 6. Performance

**Will it perform well?**
- No obvious bottlenecks
- Efficient algorithms
- Resource usage reasonable
- Scalability considered

## Review Process

### 1. Understand Context

Before reviewing code:
- Read PR description and linked issues
- Understand the problem being solved
- Check CI/CD results
- Note any special considerations

### 2. Review at Appropriate Level

**High-level first:**
- Overall approach
- Architecture decisions
- Major design choices

**Then details:**
- Implementation specifics
- Edge cases
- Code style

### 3. Provide Actionable Feedback

**Good feedback:**
- Specific and clear
- Explains the "why"
- Suggests solutions
- Prioritizes issues

**Example:**
```
Consider using a Set instead of an array here for O(1) lookups. 
With the current implementation, the nested loop creates O(n²) 
complexity which could be problematic with large datasets.
```

### 4. Use Review Comments Effectively

**Types of comments:**

**Blocking (must fix):**
- "This will cause a race condition when..."
- "Security issue: User input is not sanitized..."
- "This breaks the API contract by..."

**Non-blocking (suggestions):**
- "Consider: This could be simplified by..."
- "Nit: Variable name could be more descriptive"
- "Question: Why did you choose X over Y?"

**Positive:**
- "Nice solution! This is much cleaner than..."
- "Great test coverage on the edge cases"
- "I learned something new from this approach"

### 5. Distinguish Preferences from Problems

**Problems (objective):**
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Breaking changes

**Preferences (subjective):**
- Code style choices
- Naming preferences
- Organization approaches
- Minor optimizations

**Rule:** Block on problems, discuss preferences.

## Communication Guidelines

### Be Constructive

**Instead of:**
- "This is wrong"
- "Why would you do it this way?"
- "This code is terrible"

**Say:**
- "This could cause X issue because..."
- "Have you considered Y approach? It might..."
- "This could be improved by..."

### Explain Your Reasoning

**Weak comment:**
```
This should be refactored.
```

**Strong comment:**
```
Consider extracting this logic into a separate method. 
It's used in three places and would be easier to test 
and maintain as a standalone function.
```

### Ask Questions

Use questions to understand and guide:
- "What happens if X is null here?"
- "Could this be simplified using Y?"
- "Have you considered the case where...?"

### Acknowledge Good Work

Don't only point out problems:
- "Clever use of X to solve Y"
- "Great test coverage"
- "This is much cleaner than the old approach"
- "Nice documentation"

### Be Humble

You might be wrong:
- "I might be missing something, but..."
- "Could you explain why...?"
- "I'm not familiar with X, but..."

## Common Review Patterns

### Code Smells to Watch For

**Long methods/functions:**
- Hard to understand
- Difficult to test
- Multiple responsibilities

**Duplicated code:**
- Maintenance burden
- Inconsistent behavior
- Missed bug fixes

**Complex conditionals:**
- Hard to reason about
- Error-prone
- Difficult to test

**Large classes:**
- Too many responsibilities
- Hard to maintain
- Tight coupling

**Magic numbers/strings:**
- Unclear meaning
- Hard to change
- Error-prone

### Security Red Flags

- Hardcoded credentials or secrets
- SQL injection vulnerabilities
- XSS vulnerabilities
- Missing input validation
- Insecure data storage
- Weak authentication
- Missing authorization checks

### Performance Concerns

- N+1 query problems
- Inefficient algorithms (O(n²) when O(n) possible)
- Memory leaks
- Unnecessary database calls
- Large data structures in memory
- Blocking operations in async code

## Review Standards

### Establish Team Norms

**Define standards for:**
- Code style and formatting
- Naming conventions
- Comment requirements
- Test coverage expectations
- Documentation needs

**Document standards:**
- Style guides
- Architecture decision records
- Review checklists
- Example code

### Review Checklist

Use a consistent checklist:
- [ ] Code is correct and handles edge cases
- [ ] Tests exist and pass
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Code is readable and maintainable
- [ ] Documentation is updated
- [ ] No breaking changes (or properly communicated)
- [ ] Follows team conventions

## Handling Disagreements

### When You Disagree

**If it's a preference:**
- State your opinion
- Explain your reasoning
- Accept the author's choice
- Move on

**If it's a problem:**
- Clearly explain the issue
- Provide evidence or examples
- Suggest alternatives
- Escalate if needed

### When Author Disagrees

**Listen and understand:**
- They may have context you lack
- There might be constraints you don't know
- Your suggestion might not fit

**Discuss, don't dictate:**
- Explain your concerns
- Ask questions
- Find common ground
- Compromise when appropriate

## Review Timing

### Response Time

**Aim for:**
- Small PRs: Within 4 hours
- Medium PRs: Within 1 day
- Large PRs: Within 2 days

**If you can't review promptly:**
- Let the author know
- Suggest another reviewer
- Set expectations

### Review Size

**Optimal PR size:**
- 200-400 lines of code
- Focused on single concern
- Reviewable in 30-60 minutes

**For large PRs:**
- Request breakdown if possible
- Review in multiple passes
- Focus on high-level first
- Consider pair review

## Mentoring Through Reviews

### Teaching Opportunities

Use reviews to share knowledge:
- Explain patterns and practices
- Share relevant resources
- Demonstrate better approaches
- Encourage questions

### Growing Reviewers

Help others become better reviewers:
- Invite junior developers to review
- Explain your review comments
- Discuss review decisions
- Share review best practices

## Anti-Patterns to Avoid

❌ **Nitpicking without value** - Focus on meaningful improvements
❌ **Blocking on style preferences** - Use automated tools instead
❌ **Rewriting in your style** - Respect different approaches
❌ **Reviewing too quickly** - Take time to understand
❌ **Being overly critical** - Balance criticism with praise
❌ **Ignoring context** - Consider constraints and tradeoffs
❌ **Making it personal** - Focus on code, not the person

## Review Outcomes

### Approve

Code meets standards and is ready to merge:
- All critical issues addressed
- Tests pass
- Documentation updated
- No blocking concerns

### Approve with Comments

Minor issues that don't block merge:
- Style suggestions
- Future improvements
- Questions for discussion
- Nice-to-have changes

### Request Changes

Issues that must be addressed:
- Bugs or logic errors
- Security vulnerabilities
- Missing tests
- Breaking changes
- Architectural concerns

### Reject (Rare)

Fundamental problems requiring redesign:
- Wrong approach entirely
- Doesn't solve the problem
- Creates major technical debt
- Violates core principles

## Quick Reference

**Good review comment structure:**
1. Identify the issue
2. Explain why it's a problem
3. Suggest a solution
4. Indicate severity (blocking vs suggestion)

**Example:**
```
[Blocking] This query will cause N+1 problem when loading 
related records. Consider using eager loading with includes() 
to fetch all data in a single query. This will significantly 
improve performance with large datasets.
```

**Remember:**
- Be kind and constructive
- Focus on the code, not the person
- Explain your reasoning
- Acknowledge good work
- Know when to compromise
- Foster learning and growth
