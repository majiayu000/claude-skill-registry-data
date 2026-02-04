---
name: sdlc
description: Software development lifecycle guidance. This skill should be used when planning development work, conducting code reviews, or establishing development workflows. Use proactively when reviewing code, preparing commits, creating pull requests, refactoring, or discussing development process and best practices. (user)
---

# Software Development Lifecycle

This skill provides guidance on the software development lifecycle, with emphasis on code review and iterative improvement.

## Code Review Process

All significant code changes require **3 sequential code reviews**, each followed by refactoring.

### Process

1. **Review Phase**: Conduct a thorough code review, documenting findings
2. **Refactor Phase**: Make changes based on the review findings
3. **Repeat**: Pass the refactored code to the next reviewer

Each subsequent reviewer sees the refactored code from the previous cycle.

### Review Criteria

Each review should evaluate:

- **Correctness**: Does the code work as intended? Are edge cases handled?
- **Design**: Does the code follow SOLID principles? Is coupling minimized?
- **Readability**: Are names intention-revealing? Is the code easy to understand?
- **Simplicity**: Does the code follow the Four Rules of Simple Design?
- **Testing**: Are tests adequate? Do they serve as executable specifications?
- **Security**: Are there any security vulnerabilities? (See the `security` skill for detailed guidance)

### For AI Agents

When implementing the code review process with subagents:

1. Complete the initial implementation
2. Spawn a subagent with the role "Code Reviewer 1" to review and refactor
3. Spawn a second subagent with the role "Code Reviewer 2" to review the refactored code and refactor again
4. Spawn a third subagent with the role "Code Reviewer 3" for final review and refactoring

Each subagent should:

- First produce a written code review documenting findings
- Then make the refactoring changes based on those findings
- Consider security implications in every review

## Development Workflow

### Before Writing Code

- Understand the requirements fully before starting
- Consider the design implications
- Think about how the code will be tested

### While Writing Code

- Write tests first (TDD) when practical
- Keep commits small and focused
- Refactor continuously

### After Writing Code

- Run the full test suite
- Conduct the 3-review process
- Ensure documentation is updated if needed
