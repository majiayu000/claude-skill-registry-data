---
name: interview-skill
description: Deep-dive technical discovery and requirement gathering before coding. Use when a task is broad, ambiguous, or requires architectural decisions.
---

# Interview Mode

## Overview

This skill forces a "slow down to speed up" workflow. Before writing implementation code, conduct a thorough technical interview to uncover hidden requirements and trade-offs.

## When to Use

- Task description is vague or broad ("add auth to my app")
- Multiple valid approaches exist
- Architectural decisions are needed
- User requirements may have hidden complexity
- The task could be interpreted multiple ways

## Instructions

1. **Stop and Think** - Do not start coding yet.

2. **Interview Phase** - Use the `AskUserQuestion` tool to gather requirements:
   - UI/UX requirements and preferences
   - State management approach
   - Security considerations
   - Error handling expectations
   - Edge cases and boundary conditions
   - Integration points with existing code
   - Performance requirements
   - Testing expectations

3. **Ask Deep Questions** - Challenge assumptions:
   - "What happens if...?"
   - "How should the system behave when...?"
   - "Do you need to support...?"
   - "What's the expected scale...?"

4. **Iterate** - If an answer reveals complexity, ask follow-up questions.

5. **Spec Creation** - Summarize findings into a specification document.

6. **Confirmation** - Get user approval before proceeding to implementation.

## Example Interview

**User:** "I want to add auth to my app."

**Interview Questions:**
1. Authentication method: JWT tokens, session-based, or OAuth?
2. Do you need social login (Google, GitHub, etc.)?
3. What's the password policy (length, complexity)?
4. Password reset flow - email or SMS?
5. Session duration and refresh token handling?
6. Protected routes - which pages require auth?
7. Role-based access control needed?
8. Rate limiting for login attempts?
9. Two-factor authentication requirement?
10. Where will user data be stored?

## Output Format

After the interview, create a spec document:

```markdown
# Feature Specification: [Feature Name]

## Requirements
- Requirement 1
- Requirement 2

## Technical Approach
- Approach details

## Edge Cases
- Edge case 1
- Edge case 2

## Out of Scope
- Items explicitly excluded

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```
