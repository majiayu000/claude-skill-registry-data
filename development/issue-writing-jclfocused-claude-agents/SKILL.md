---
name: issue-writing
description: Use this skill when writing, reviewing, or discussing issue descriptions, acceptance criteria, or task breakdowns. Ensures consistent, high-quality issue structure that any developer or AI can pick up and execute. Triggers when drafting issues, defining requirements, or when users ask "how should I write this issue?" or "what should the acceptance criteria be?"
---

# Issue Writing Skill

This skill guides the creation of well-structured, actionable Jira issues that any developer or AI can pick up and execute independently.

## When to Use

Apply this skill when:
- Writing or drafting issue descriptions
- Defining acceptance criteria for tasks
- Breaking down features into Subtasks
- Reviewing existing issues for clarity
- Users ask how to document requirements

## Issue Structure: Parent Stories

```
h2. IMPORTANT: Jira Issue Discipline
[Standard discipline rules]

---

h2. Problem
[1-2 sentences: Why does this feature need to exist?]

h2. Solution
[1-2 sentences: What are we building to solve this?]

h2. High-Level Implementation
[Bullet points: Key technical decisions, patterns]

h2. Codebase Investigation Findings
[What patterns to follow, similar features, code locations]

h2. Out of Scope / Deferred
[Explicitly list what we're NOT doing]
```

## Issue Structure: Subtasks

```
h2. Objective
[1-2 sentences: What specific thing needs to be done?]

h2. Acceptance Criteria
* [Specific, testable criterion 1]
* [Specific, testable criterion 2]
* [Specific, testable criterion 3]

h2. Implementation Notes
* Relevant files: [paths]
* Patterns to follow: [reference]
* Dependencies: [other Subtasks]
```

## Writing Good Acceptance Criteria (SMART)

- **Specific**: Clear about what exactly needs to happen
- **Measurable**: Can objectively verify if it's done
- **Achievable**: Within scope of this single Subtask
- **Relevant**: Directly related to the objective
- **Testable**: Can be validated by running/checking

## Jira Formatting Notes

Jira uses Wiki markup, not Markdown:
- Headers: `h1.`, `h2.`, `h3.`
- Bold: `*bold*`
- Bullets: `*` or `-`
- Numbered list: `#`
- Code: `{{inline}}` or `{code}block{code}`
- Links: `[title|url]`

## Anti-Patterns to Avoid

- **Vague objectives**: "Improve the dashboard"
- **Missing acceptance criteria**: Assuming it's obvious
- **Implementation prescription**: Over-specifying the how
- **Hidden dependencies**: Not mentioning blockers
- **Scope creep**: Adding "nice to haves"

Remember: **A good issue can be executed by anyone who reads it.**
