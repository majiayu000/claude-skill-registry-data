---
name: pr-review
description: Structured PR review with scoring, bug detection, and actionable feedback. Use when reviewing pull requests or code changes.
---

# PR Review Skill

Provide a clear, concise, and actionable review of Pull Requests. Focus on overall codebase quality, including readability, maintainability, functionality, adherence to best practices, performance optimizations, and testing coverage.

## Focus Areas

1. **Code Quality:** Assess readability, organization, and maintainability.
2. **Functionality:** Ensure the PR meets its intended purpose and works as expected.
3. **Best Practices:** Evaluate adherence to coding standards, design patterns, and project guidelines.
4. **Performance:** Identify potential performance improvements or optimizations.
5. **Testing:** Review the comprehensiveness and effectiveness of test coverage.
6. **Security:** Identify any potential security vulnerabilities or concerns.
7. **Bugs Found:** List any bugs identified in the PR.

## Critical Instructions

- If you have nothing to say about a particular section, omit it from the review.
- If there are no issues and the PR is good to go, mention it in the conclusion. No unnecessary feedback.
- Avoid minor nitpicks and repetitive feedback.

## Scoring Criteria

| Score  | Level         | Criteria                                                                                        |
| ------ | ------------- | ----------------------------------------------------------------------------------------------- |
| 90-100 | Exceptional   | Clean, efficient, well-documented. >90% test coverage. No security issues. Optimal performance. |
| 75-89  | High Quality  | Well-structured, maintainable. 70-90% test coverage. Minor optimization opportunities.          |
| 60-74  | Average       | Functional but needs improvement. 40-70% test coverage. Some code duplication.                  |
| 40-59  | Below Average | Significant structural issues. <40% test coverage. Multiple security concerns.                  |
| 0-39   | Poor          | Major architectural problems. Missing/broken tests. Critical security vulnerabilities.          |

## Review Template

```markdown
### AI Review Summary

**Score:** [0-100]

_Brief summary of the PR purpose and main changes._

**Key changes:**

- Change 1
- Change 2

---

**Key Strengths**

- **[Area]:** Description of strength
- **[Area]:** Description of strength

---

**Areas for Improvement** (if any)

- **[Issue]:**
  _Suggestion:_ Actionable recommendation

---

**Bugs Found** (if any)

| Bug Name              | Affected Files | Description | Confidence      |
| --------------------- | -------------- | ----------- | --------------- |
| [Bug Link](#bug-name) | `path/file.ts` | Description | High/Medium/Low |

### Bug Details

#### Bug: [Bug Name](#bug-name)

- **Affected Files:** `path/file.ts`
- **Description:** Detailed explanation
- **Confidence:** High/Medium/Low

---

**Issues Found** (if any)

| Issue Type          | Issue Name                | Affected Components | Description | Severity        |
| ------------------- | ------------------------- | ------------------- | ----------- | --------------- |
| Performance/Testing | [Issue Link](#issue-name) | Component           | Description | High/Medium/Low |

### Issue Details

#### Issue: [Issue Name](#issue-name)

- **Type:** Performance/Testing
- **Affected Components:** `path/file.ts`
- **Description:** Detailed explanation
- **Severity:** High/Medium/Low

---

**Performance Considerations** (if any)

- **[Optimization]:** Actionable suggestion

---

**Testing** (if any)

- **[Coverage Gap]:** Suggestion for additional tests

---

**Conclusion**

_Summary of overall quality and readiness for merging._
```

## Best Practices

- Use clear and concise language
- Limit each section to 2-3 critical points
- Use bullet points and clear headings
- Provide actionable suggestions, not just complaints
- Link bug/issue names to their details sections
- Focus on impact, not style preferences
