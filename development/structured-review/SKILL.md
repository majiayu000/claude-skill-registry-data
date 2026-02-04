---
name: structured-review
description: Automatically invoked when conducting reviews (code, specs, architecture, UX). Ensures systematic analysis and actionable findings with consistent format.
---

# Structured Review Skill

This skill activates when conducting any type of review to ensure systematic analysis and actionable output.

## When This Skill Activates

Automatically engage when:
- Reviewing code implementations
- Evaluating feature specifications
- Assessing architectural designs
- Analyzing user experience flows
- Checking performance characteristics
- Evaluating test coverage
- Conducting security audits

## Review Principles

### Systematic
- Follow consistent methodology
- Cover all relevant aspects
- Don't skip areas
- Use checklists

### Objective
- Base findings on evidence
- Reference standards and best practices
- Avoid personal preferences
- Focus on facts

### Actionable
- Provide specific findings
- Include file:line references
- Show code examples
- Suggest concrete fixes

### Balanced
- Note positives and negatives
- Distinguish critical from nice-to-have
- Consider context and constraints
- Acknowledge trade-offs

### Constructive
- Frame as opportunities for improvement
- Explain impact of issues
- Provide learning context
- Focus on outcomes, not blame

## Review Types

### Code Review
**Focus:** Readability, maintainability, correctness, performance
**Checklist:** See Code Review section below

### Specification Review
**Focus:** Completeness, clarity, feasibility, alignment
**Checklist:** See Spec Review section below

### Architecture Review
**Focus:** Patterns, boundaries, scalability, maintainability
**Checklist:** See Architecture Review section below

### Security Review
**Focus:** Vulnerabilities, auth, data protection, injection
**Checklist:** See Security Review section below

### UX Review
**Focus:** Usability, accessibility, flows, error handling
**Checklist:** See UX Review section below

### Performance Review
**Focus:** Bottlenecks, efficiency, scalability, resource usage
**Checklist:** See Performance Review section below

## Standard Review Format

Use this format for all review outputs:

```markdown
# Review: [Type] - [Subject]

**Date:** [YYYY-MM-DD]
**Reviewer:** [Agent/Person]
**Scope:** [What was reviewed]

---

## Summary

[High-level overview of findings - 2-3 sentences]

**Overall Assessment:** [Pass / Pass with Concerns / Needs Improvement / Fail]

---

## Findings

### Critical Issues

[Must fix before proceeding]

**[ID] [Issue Title]**
- **Location:** [file:line or component]
- **Issue:** [Description of the problem]
- **Impact:** [What this affects]
- **Recommendation:** [How to fix]
- **Code:** [Example if applicable]

### High Priority Issues

[Should fix soon]

[Same structure as Critical]

### Medium Priority Issues

[Should address]

[Same structure]

### Low Priority Issues

[Nice to have]

[Same structure]

---

## Positive Observations

[What was done well]

- [Observation 1]
- [Observation 2]

---

## Recommendations

### Immediate Actions
1. [Action item]
2. [Action item]

### Future Improvements
1. [Improvement]
2. [Improvement]

---

## Metrics (if applicable)

[Relevant metrics like coverage, complexity, etc.]

---

## References

[Links to standards, prior decisions, documentation]
```

## Severity Levels

### Critical
- **Definition:** Must fix immediately, blocks progress
- **Examples:** Security vulnerabilities, data loss bugs, system crashes
- **Action:** Do not proceed until fixed

### High
- **Definition:** Significant impact, should fix before release
- **Examples:** Important bugs, major performance issues, accessibility violations
- **Action:** Fix before merging/deploying

### Medium
- **Definition:** Moderate impact, should address
- **Examples:** Code quality issues, minor bugs, maintainability concerns
- **Action:** Fix in near term

### Low
- **Definition:** Minor improvement, nice to have
- **Examples:** Style inconsistencies, better variable names, minor optimizations
- **Action:** Address when convenient

## Code Review Checklist

### Correctness
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No obvious bugs

### Readability
- [ ] Clear naming
- [ ] Self-documenting code
- [ ] Appropriate comments
- [ ] Logical organization

### Maintainability
- [ ] DRY - no duplication
- [ ] Single responsibility
- [ ] Easy to modify
- [ ] Clear abstractions

### Performance
- [ ] No obvious inefficiencies
- [ ] Appropriate algorithms
- [ ] Resource usage reasonable
- [ ] Scalable approach

### Testing
- [ ] Tests exist and pass
- [ ] Edge cases tested
- [ ] Good coverage
- [ ] Tests are clear

### Security
- [ ] Input validated
- [ ] No injection vulnerabilities
- [ ] Auth/authz correct
- [ ] Secrets not exposed

## Specification Review Checklist

### Completeness
- [ ] All requirements identified
- [ ] Success criteria defined
- [ ] Error scenarios covered
- [ ] Dependencies listed

### Clarity
- [ ] Unambiguous language
- [ ] Examples provided
- [ ] Terms defined
- [ ] Visual aids included

### Feasibility
- [ ] Technically possible
- [ ] Timeline realistic
- [ ] Resources available
- [ ] No blockers

### Alignment
- [ ] Fits architecture
- [ ] Consistent with standards
- [ ] Aligns with goals
- [ ] No conflicts with other work

## Architecture Review Checklist

### Structure
- [ ] Clear boundaries
- [ ] Appropriate layers
- [ ] Logical organization
- [ ] Proper separation of concerns

### Patterns
- [ ] Appropriate patterns used
- [ ] Patterns correctly implemented
- [ ] Consistent pattern application
- [ ] No anti-patterns

### Coupling
- [ ] Low coupling between components
- [ ] High cohesion within components
- [ ] Dependencies point correctly
- [ ] No circular dependencies

### Scalability
- [ ] Horizontal scaling possible
- [ ] No bottlenecks
- [ ] Stateless where appropriate
- [ ] Resource usage scales

## Security Review Checklist

### Authentication & Authorization
- [ ] Auth required where needed
- [ ] Credentials handled securely
- [ ] Authorization consistent
- [ ] Sessions secure

### Input Validation
- [ ] All input validated
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] Command injection prevented

### Data Protection
- [ ] Sensitive data encrypted
- [ ] TLS for transport
- [ ] Secrets not in code
- [ ] PII handled correctly

### Error Handling
- [ ] Errors don't leak info
- [ ] Generic error messages to users
- [ ] Detailed errors logged securely

## UX Review Checklist

### Usability
- [ ] Clear navigation
- [ ] Intuitive flows
- [ ] Helpful feedback
- [ ] Error messages clear

### Accessibility
- [ ] WCAG compliant
- [ ] Keyboard accessible
- [ ] Screen reader friendly
- [ ] Good contrast

### Forms
- [ ] Required fields marked
- [ ] Format hints provided
- [ ] Inline validation
- [ ] Errors actionable

### Feedback
- [ ] Loading states
- [ ] Success confirmation
- [ ] Progress indicators
- [ ] Error recovery

## Performance Review Checklist

### Algorithms
- [ ] Appropriate complexity
- [ ] No unnecessary iterations
- [ ] Efficient data structures

### Database
- [ ] No N+1 queries
- [ ] Indexes present
- [ ] Efficient queries
- [ ] Pagination implemented

### Caching
- [ ] Static data cached
- [ ] Appropriate TTLs
- [ ] Cache invalidation strategy

### Resources
- [ ] No memory leaks
- [ ] Connections pooled
- [ ] Files closed
- [ ] Async operations

## Review Workflow

### 1. Prepare
- Read the subject thoroughly
- Understand context and requirements
- Review related documentation
- Note areas to focus on

### 2. Analyze Systematically
- Use appropriate checklist
- Take notes as you review
- Flag issues immediately
- Note positive observations

### 3. Categorize Findings
- Assign severity levels
- Group related issues
- Distinguish must-fix from nice-to-have
- Prioritize by impact

### 4. Provide Context
- Explain why it matters
- Show impact of issues
- Reference standards
- Include examples

### 5. Suggest Solutions
- Provide specific recommendations
- Show code examples
- Consider alternatives
- Note trade-offs

### 6. Write Review Report
- Follow standard format
- Be specific with locations
- Include code examples
- Balance criticism with positives

### 7. Review Your Review
- Is it actionable?
- Is it constructive?
- Is it clear?
- Is it complete?

## Examples

### Good Finding
```markdown
**[HIGH-1] SQL Injection Vulnerability**
- **Location:** `src/api/users.js:45`
- **Issue:** User input directly concatenated into SQL query
- **Impact:** Attacker can execute arbitrary SQL, access all data
- **Current Code:**
  \`\`\`javascript
  db.query(`SELECT * FROM users WHERE id = ${userId}`)
  \`\`\`
- **Recommendation:** Use parameterized queries
  \`\`\`javascript
  db.query('SELECT * FROM users WHERE id = ?', [userId])
  \`\`\`
```

### Poor Finding
```markdown
**Issue:** Security problem
- **Location:** users file
- **Recommendation:** Fix it
```

### Good Positive Observation
```markdown
- Clear separation between API and business logic layers
- Consistent use of async/await throughout
- Well-structured error handling with custom error classes
- Comprehensive test coverage (92%)
```

## Best Practices

### Be Specific
Always include:
- Exact location (file:line)
- Description of issue
- Why it matters
- How to fix it

### Show, Don't Just Tell
Include code examples:
- Current code (the issue)
- Recommended code (the fix)

### Prioritize Ruthlessly
Not everything is critical:
- Security vulnerabilities: Critical
- Major bugs: High
- Code style: Low

### Balance Feedback
- Acknowledge good work
- Frame issues constructively
- Focus on high-impact items
- Don't nitpick

### Make It Actionable
- Provide clear next steps
- Suggest specific changes
- Note what to do first
- Estimate impact

## Review Etiquette

### Do
- Focus on code/design, not people
- Explain reasoning
- Ask questions when unsure
- Provide context
- Acknowledge constraints
- Be respectful

### Don't
- Use "you" statements ("you did this wrong")
- Make it personal
- Demand perfection
- Ignore constraints
- Be dismissive
- Assume malice

## After the Review

### For Reviewer
- Be available for questions
- Help prioritize fixes
- Review fixes when ready

### For Reviewee
- Read review thoroughly
- Ask for clarification if needed
- Address critical issues first
- Thank reviewer for feedback

## References

- Code review best practices: See `ai_docs/knowledge/code-review/`
- Security standards: OWASP Top 10
- Accessibility: WCAG 2.1
- Architecture: See `docs/architecture/`

## Constraints

- Don't review everything - focus on what matters
- Balance thoroughness with practicality
- Consider context and constraints
- Distinguish opinion from fact
- Focus on impact, not perfection
