---
name: create-custom-command
description: Create reusable Codex workflow skills or prompt templates to automate repetitive tasks. Use when establishing team workflows, automating code reviews.
---

# Create Custom Codex Workflows

Create reusable Codex workflow skills or prompt templates to automate repetitive tasks and establish consistent workflows across your team.

## When to Use This Skill

Use this skill when you need to:

- Automate repetitive Codex interactions
- Establish team-wide workflows
- Create project-specific skills
- Standardize code review processes
- Build custom documentation generators
- Create onboarding workflows

**Trigger phrases**: "create custom skill", "Codex workflow", "automate workflow", "create reusable skill", "custom skill"

## What This Skill Does

Creates reusable Codex skills under `%USERPROFILE%\.codex\skills\<workflow-name>\SKILL.md`. Convert any external slash-command style workflow into a `SKILL.md` with clear trigger phrases and instructions.

### Skill File Structure

```
%USERPROFILE%\.codex\skills\
├── review\
│   └── SKILL.md
├── test\
│   └── SKILL.md
├── document\
│   └── SKILL.md
└── onboard\
    └── SKILL.md
```

## Instructions

### Step 1: Create Skill Directory

```bash
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills\review"
```

### Step 2: Create SKILL.md Files

Each workflow lives in `%USERPROFILE%\.codex\skills\<workflow-name>\SKILL.md`. Codex can use it by skill name or when a request matches the description and trigger phrases.

#### Example: Code Review Workflow

```markdown
<!-- %USERPROFILE%\.codex\skills\review\SKILL.md -->
# Code Review Command

Review the provided code for:

## Quality Checks
1. **Code Style**: Check for consistent formatting, naming conventions
2. **Best Practices**: Identify anti-patterns and suggest improvements
3. **Error Handling**: Verify proper exception handling
4. **Performance**: Look for potential bottlenecks

## Security Checks
1. Input validation
2. SQL injection vulnerabilities
3. XSS vulnerabilities
4. Hardcoded secrets

## Output Format
Provide findings in this format:

### Summary
Brief overview of the code quality.

### Issues Found
| Severity | Location | Issue | Suggestion |
|----------|----------|-------|------------|
| High/Medium/Low | file:line | Description | Fix |

### Recommendations
Prioritized list of improvements.
```

#### Example: Test Generation Workflow

```markdown
<!-- %USERPROFILE%\.codex\skills\test\SKILL.md -->
# Generate Tests Command

Generate comprehensive tests for the provided code:

## Test Types
1. **Unit Tests**: Test individual functions/methods
2. **Edge Cases**: Test boundary conditions
3. **Error Cases**: Test error handling
4. **Integration**: Test component interactions

## Requirements
- Use the project's testing framework
- Follow AAA pattern (Arrange, Act, Assert)
- Aim for 80%+ code coverage
- Include meaningful test descriptions

## Output
Provide complete, runnable test code with:
- Test file structure
- All imports
- Setup/teardown if needed
- Descriptive test names
```

#### Example: Documentation Workflow

```markdown
<!-- %USERPROFILE%\.codex\skills\document\SKILL.md -->
# Documentation Generator

Generate documentation for the provided code:

## Documentation Types

### For Functions/Methods
```
/**
 * Brief description
 *
 * @param {type} name - Description
 * @returns {type} Description
 * @throws {Error} When condition
 * @example
 * // Usage example
 */
```

### For Classes
- Purpose and responsibility
- Constructor parameters
- Public methods
- Usage examples

### For Modules
- Overview
- Exports
- Dependencies
- Example usage

## Output Format
Provide documentation in the language's standard format.
```

#### Example: Onboarding Workflow

```markdown
<!-- %USERPROFILE%\.codex\skills\onboard\SKILL.md -->
# Codebase Onboarding

Provide a comprehensive overview of this codebase:

## Analysis Required

### 1. Project Structure
- Directory layout and purpose of each folder
- Key files and their roles
- Configuration files

### 2. Architecture
- Overall architecture pattern (MVC, microservices, etc.)
- Main components and their interactions
- Data flow

### 3. Technology Stack
- Languages and frameworks
- Key dependencies
- Development tools

### 4. Entry Points
- Main application entry
- API endpoints
- CLI commands

### 5. Getting Started
- Setup instructions
- Environment requirements
- Running locally
- Running tests

### 6. Key Concepts
- Domain-specific terminology
- Important patterns used
- Common conventions

## Output
Provide a structured onboarding guide a new developer can follow.
```

#### Example: PR Description Workflow

```markdown
<!-- %USERPROFILE%\.codex\skills\pr\SKILL.md -->
# Generate PR Description

Analyze the current changes and generate a PR description:

## Required Information

1. **Summary**: One-line description of changes
2. **Motivation**: Why these changes are needed
3. **Changes Made**: Bullet list of modifications
4. **Testing**: How changes were tested
5. **Screenshots**: If UI changes (placeholder)
6. **Breaking Changes**: If any
7. **Related Issues**: Link to tickets

## Output Format

```markdown
## Summary
[One line summary]

## Motivation
[Why this change is needed]

## Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
[Add screenshots if UI changes]

## Breaking Changes
[List any breaking changes or "None"]

## Related Issues
Closes #[issue-number]
```
```

### Step 3: Use Workflows with Arguments

Codex skill prompts can include an argument placeholder pattern when the user names the skill with extra text:

```markdown
<!-- %USERPROFILE%\.codex\skills\fix\SKILL.md -->
# Fix Issue Command

Analyze and fix the issue described: $ARGUMENTS

## Process
1. Understand the issue from the description
2. Locate relevant code
3. Identify root cause
4. Implement fix
5. Verify fix doesn't break existing functionality

## Output
- Explanation of the issue
- Root cause analysis
- Code changes with explanation
- Verification steps
```

Usage: `$fix the login button doesn't work on mobile`

### Step 4: Create Parameterized Workflows

```markdown
<!-- %USERPROFILE%\.codex\skills\scaffold\SKILL.md -->
# Scaffold Component

Create a new component with the following parameters:

**Name**: $ARGUMENTS

## Generate
1. Component file (`{name}.tsx`)
2. Styles file (`{name}.module.css`)
3. Test file (`{name}.test.tsx`)
4. Story file (`{name}.stories.tsx`)

## Component Template
```tsx
import styles from './{name}.module.css';

interface {Name}Props {
  // Define props
}

export function {Name}({ }: {Name}Props) {
  return (
    <div className={styles.container}>
      {/* Implementation */}
    </div>
  );
}
```

## Test Template
```tsx
import { render, screen } from '@testing-library/react';
import { {Name} } from './{name}';

describe('{Name}', () => {
  it('renders correctly', () => {
    render(<{Name} />);
    // Add assertions
  });
});
```
```

Usage: `$scaffold UserProfile`

### Step 5: Team-Wide Workflows

Create skills for team workflows:

```markdown
<!-- %USERPROFILE%\.codex\skills\standup\SKILL.md -->
# Daily Standup Helper

Analyze recent changes to prepare standup notes:

## Look For
1. **Git commits** from the last 24 hours
2. **Modified files** and their purpose
3. **TODO comments** added or resolved
4. **Test coverage** changes

## Output Format

### Yesterday
- [What was completed]

### Today
- [Planned work]

### Blockers
- [Any impediments]

### Notes
- [Additional context]
```

```markdown
<!-- %USERPROFILE%\.codex\skills\release\SKILL.md -->
# Prepare Release

Prepare release notes and checklist:

## Gather
1. All commits since last tag
2. New features (feat commits)
3. Bug fixes (fix commits)
4. Breaking changes
5. Dependencies updated

## Output

### Release v[X.Y.Z] Notes

#### New Features
- [Feature 1]
- [Feature 2]

#### Bug Fixes
- [Fix 1]
- [Fix 2]

#### Breaking Changes
- [Change 1]

#### Migration Guide
[If breaking changes, provide migration steps]

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Release notes written
- [ ] Stakeholders notified
```

## Skill Workflow Best Practices

### Do's

```markdown
# Good: Clear structure
## Steps
1. First, do X
2. Then, do Y
3. Finally, do Z

## Output Format
[Clear specification of expected output]
```

### Don'ts

```markdown
# Bad: Vague instructions
Do the thing.

# Bad: No output format
Review the code.
```

### Include Context

```markdown
# Good: Project-specific context
This project uses:
- React with TypeScript
- Jest for testing
- Tailwind for styling

Follow existing patterns in src/components/.
```

## Quality Checklist

- [ ] Skill has clear purpose
- [ ] Instructions are specific
- [ ] Output format is defined
- [ ] Arguments are documented
- [ ] Skill works consistently
- [ ] Team has reviewed command

## Advanced: Workflow Composition

Reference other workflows:

```markdown
<!-- %USERPROFILE%\.codex\skills\full-review\SKILL.md -->
# Full Code Review

Perform a comprehensive review combining multiple checks:

1. First, run quality checks as defined in the review workflow
2. Then, generate tests as defined in the test workflow
3. Finally, update documentation as defined in the document workflow

Provide a combined report with all findings.
```

## Related Skills

- `plan-before-code` - Planning workflows
- `code-quality` - Review workflows
- `test-structure` - Testing workflows

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: Codex reusable workflow guidance


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
