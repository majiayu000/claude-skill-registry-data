---
name: copilot-instruction-creator
description: Guide for creating custom instructions to tailor GitHub Copilot responses for personal, repository, or organization use. Use this when setting up Copilot customization for better responses.
license: MIT
---

# Copilot Custom Instructions

This skill provides comprehensive guidance for creating custom instructions that tailor GitHub Copilot's responses to your personal preferences, team workflows, project requirements, or organization standards. Custom instructions help Copilot generate higher quality, more relevant responses without needing to repeat context in every interaction.

## When to Use This Skill

Use this skill when:

- Setting up personal custom instructions for consistent Copilot behavior
- Creating repository-wide instructions for project-specific standards
- Developing organization-level instructions for company-wide preferences
- Configuring path-specific instructions for different file types or directories
- Optimizing Copilot responses for coding standards, frameworks, or workflows
- Ensuring consistent AI assistance across team members

## Prerequisites

- **Always check the latest GitHub documentation**: <https://docs.github.com/en/copilot/concepts/prompting/response-customization>
- Access to GitHub Copilot (Pro, Pro+, Business, or Enterprise plan)
- Understanding of your project, team, or organization's needs
- Knowledge of the context where instructions will be applied

## Latest Information Check

**IMPORTANT**: Before creating any custom instructions, always check the official GitHub documentation for the latest information: <https://docs.github.com/en/copilot/concepts/prompting/response-customization>

Key points from the latest documentation:

- Three types: Personal, Repository, and Organization instructions
- Repository instructions include repository-wide, path-specific, and agent instructions
- Precedence: Personal > Repository (path-specific, then repository-wide, then agent) > Organization
- All relevant instruction sets are sent to Copilot; precedence only decides conflicts between them
- Path-specific `.instructions.md` files require an `applyTo` glob in YAML frontmatter
- Instructions should be short, self-contained statements
- Support varies by surface (GitHub.com, VS Code, JetBrains, Copilot CLI, and others) — check the [support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support)

## Instructions

### Step 1: Determine Instruction Scope and Type

1. **Identify the scope**: Personal, repository, or organization level?
2. **Choose instruction type**:
   - **Personal**: Individual preferences — Copilot Chat on GitHub.com, or `~/.copilot/copilot-instructions.md` and `~/.copilot/instructions/**/*.instructions.md` for the Copilot CLI
   - **Repository-wide**: `.github/copilot-instructions.md` for entire repository
   - **Path-specific**: `.github/instructions/**/NAME.instructions.md` for specific paths (requires `applyTo` frontmatter)
   - **Agent instructions**: `AGENTS.md` anywhere in the repository (the nearest one in the directory tree wins), or a single `CLAUDE.md` or `GEMINI.md` at the repository root
   - **Organization**: Organization-wide settings (owners only, Copilot Business or Enterprise; GitHub.com Chat, code review, and cloud agent only)

3. **Assess requirements**: What behaviors need to be customized?

### Step 2: Analyze Context and Requirements

1. **Gather project information**:
   - Project purpose and goals
   - Technology stack and frameworks
   - Coding standards and conventions
   - Team workflows and processes

2. **Identify pain points**:
   - Common Copilot suggestions that need correction
   - Missing context that causes poor responses
   - Inconsistent behavior across team members

3. **Define success criteria**:
   - What should Copilot always/never do?
   - What standards must be followed?
   - What context is always relevant?

### Step 3: Structure Your Instructions

1. **Start with project overview**:

   ```markdown
   # Project Overview
   This project is a [description]. It is built using [technologies] and uses [databases/frameworks].
   ```

2. **Document folder structure**:

   ```markdown
   ## Folder Structure
   - `/src`: Contains the source code for the [component]
   - `/tests`: Contains test files
   - `/docs`: Contains documentation
   ```

3. **Specify coding standards**:

   ```markdown
   ## Coding Standards
   - Use [naming convention] for variables/functions
   - Follow [style guide] for formatting
   - Use [patterns] for [specific cases]
   ```

4. **List libraries and frameworks**:

   ```markdown
   ## Libraries and Frameworks
   - [Library] v[version] for [purpose]
   - [Framework] with [configuration]
   ```

### Step 4: Write Effective Instructions

**Guidelines for writing instructions**:

- Keep statements short and self-contained
- Use natural language
- Focus on broadly applicable information
- Avoid conflicting instructions
- Test for effectiveness

**Common instruction patterns**:

- Language preferences: `Always respond in [language].`
- Coding standards: `Use [convention] for [element].`
- Framework usage: `Use [framework] with [library].`
- Response style: `Be clear and concise.`
- Context requirements: `Always consider [requirement].`

### Step 5: Create the Instruction Files

#### For Repository Instructions

1. **Repository-wide instructions**:
   - Create `.github/copilot-instructions.md`
   - Include all broadly applicable instructions

2. **Path-specific instructions**:
   - Create `.github/instructions/` directory (subdirectories are allowed)
   - Add `NAME.instructions.md` files (e.g., `frontend.instructions.md`)
   - Start each file with YAML frontmatter containing `applyTo` — a glob, or comma-separated globs, matching the files the instructions cover. Without it, the file is never applied.
   - Optionally add `excludeAgent: "code-review"` or `excludeAgent: "cloud-agent"` to keep one of those agents from using the file

   ```markdown
   ---
   applyTo: "**/*.ts,**/*.tsx"
   ---

   Use strict TypeScript. Never use `any`.
   ```

3. **Agent instructions**:
   - Create `AGENTS.md` files anywhere in the repository — the nearest one in the directory tree takes precedence
   - Alternatively, use a single `CLAUDE.md` or `GEMINI.md` at the repository root
   - Include agent-specific customizations

#### For Personal Instructions

- **GitHub.com**: In Copilot Chat, click your profile picture, select **Personal instructions**, enter your preferences, and save
- **Copilot CLI**: Create `~/.copilot/copilot-instructions.md`, or modular `~/.copilot/instructions/**/*.instructions.md` files matched by `applyTo`
- **VS Code / JetBrains**: Personal instructions live in the IDE's user profile — see the IDE's documentation

#### For Organization Instructions

1. Organization owners only, for organizations with Copilot Business or Copilot Enterprise
2. Go to organization **Settings** > **Copilot** > **Custom instructions**
3. Enter instructions in the **Preferences and instructions** box and save
4. Applies only to Copilot Chat, Copilot code review, and Copilot cloud agent on GitHub.com

### Step 6: Test and Refine

1. **Test in different contexts**:
   - Try Copilot Chat with various queries
   - Test in different files and scenarios
   - Verify behavior across team members

2. **Monitor effectiveness**:
   - Check if responses follow instructions
   - Identify areas needing clarification
   - Gather feedback from team members

3. **Iterate and improve**:
   - Refine wording for clarity
   - Add missing context
   - Remove ineffective instructions

### Step 7: Maintain and Update

1. **Regular review**: Check instructions periodically
2. **Update with changes**: Modify when project standards change
3. **Version control**: Track changes to instruction files
4. **Team communication**: Ensure team knows about updates

## Examples

### Example 1: Repository-Wide Instructions for a React Project

Create `.github/copilot-instructions.md`:

```markdown
# Project Overview

This project is a modern web application built with React and TypeScript. It provides a task management interface for teams to collaborate on projects and track progress.

## Folder Structure

- `/src/components`: Reusable React components
- `/src/hooks`: Custom React hooks
- `/src/utils`: Utility functions and helpers
- `/src/types`: TypeScript type definitions
- `/tests`: Unit and integration tests
- `/docs`: Project documentation

## Libraries and Frameworks

- React 18 with TypeScript
- React Router for navigation
- Axios for API calls
- React Query for data fetching
- Tailwind CSS for styling
- Jest and React Testing Library for testing

## Coding Standards

- Use functional components with hooks
- Prefer custom hooks over class components
- Use TypeScript interfaces for all data structures
- Follow the single responsibility principle
- Write descriptive variable and function names
- Use early returns in functions
- Handle errors gracefully with try-catch blocks

## UI Guidelines

- Use Tailwind CSS classes for styling
- Maintain consistent spacing and typography
- Ensure responsive design for mobile and desktop
- Follow accessibility best practices (WCAG guidelines)
- Use semantic HTML elements

## API Guidelines

- Use RESTful API design principles
- Include proper error handling for API calls
- Implement loading states for async operations
- Cache data appropriately with React Query
- Validate API responses before using data
```

### Example 2: Path-Specific Instructions for Tests

Create `.github/instructions/tests.instructions.md`:

```markdown
---
applyTo: "**/*.test.ts,**/*.test.tsx"
---

# Testing Instructions

These instructions apply to all test files in the repository.

## Testing Framework

- Use Jest as the testing framework
- Use React Testing Library for component testing
- Write tests in TypeScript (.test.tsx files)

## Test Structure

- Group related tests in describe blocks
- Use descriptive test names (it should...)
- Follow the Arrange-Act-Assert pattern
- Test one behavior per test case

## Testing Best Practices

- Test component behavior, not implementation details
- Mock external dependencies (API calls, hooks)
- Test error states and edge cases
- Aim for high test coverage (>80%)
- Write integration tests for critical user flows

## Naming Conventions

- Test files: `ComponentName.test.tsx`
- Test cases: descriptive sentences
- Mock files: `ComponentName.mock.tsx`
```

### Example 3: Personal Instructions

In Copilot Chat on GitHub.com (profile picture > **Personal instructions**):

```text
Always respond in clear, concise English.
Explain code concepts with practical examples.
Prefer modern JavaScript/TypeScript features.
When suggesting code, include brief comments for complex logic.
Focus on readable, maintainable solutions over clever optimizations.
```

### Example 4: Organization Instructions

For organization owners (Copilot Business or Enterprise), in organization **Settings** > **Copilot** > **Custom instructions**:

```text
Always respond in English unless specifically requested otherwise.
For security-related questions, reference the company security guidelines.
Use the organization's approved coding standards.
When suggesting code, ensure it follows our accessibility requirements.
Prefer our standard technology stack unless there's a specific reason to deviate.
```

## Best Practices

### Writing Effective Instructions

- **Be specific**: Use concrete examples rather than vague guidance
- **Keep it concise**: Short statements are more effective than long explanations
- **Test thoroughly**: Verify instructions work as intended
- **Avoid conflicts**: Ensure instructions don't contradict each other
- **Update regularly**: Review and update as project needs change

### Repository Instructions

- **Broad applicability**: Focus on information relevant to most repository interactions
- **Version control**: Track instruction files in git
- **Team alignment**: Ensure instructions reflect team consensus
- **Documentation**: Reference instruction files in project README

### Personal Instructions

- **Individual preferences**: Focus on your personal workflow preferences
- **Complement repository**: Don't override important project standards
- **Minimal but effective**: Few high-impact instructions are better than many

### Organization Instructions

- **Company standards**: Enforce organization-wide policies and preferences
- **Cultural alignment**: Reflect company values and communication style
- **Security first**: Include security-related guidelines
- **Scalable**: Work across different teams and projects

## Common Issues

**Issue**: Copilot not following instructions
**Solution**: Check precedence (personal > repository > organization), ensure instructions are clear and specific

**Issue**: Path-specific instructions never apply
**Solution**: Confirm the file is under `.github/instructions/`, ends in `.instructions.md`, and has an `applyTo` glob in frontmatter that matches the target files

**Issue**: Instructions too broad or conflicting
**Solution**: Refine wording, remove contradictions, test in different contexts

**Issue**: Instructions not applying to certain features
**Solution**: Check support matrix at <https://docs.github.com/en/copilot/reference/custom-instructions-support>

**Issue**: Team members getting different responses
**Solution**: Ensure repository instructions are consistent, check for personal overrides

**Issue**: Instructions becoming outdated
**Solution**: Regular review process, update when project standards change

## Additional Resources

- **[GitHub Custom Instructions Documentation](https://docs.github.com/en/copilot/concepts/prompting/response-customization)** - Official documentation (always check first)
- [Adding Repository Custom Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) - Step-by-step guide
- [Custom Instructions Library](https://docs.github.com/en/copilot/tutorials/customization-library/custom-instructions) - Curated examples
- [Custom Instructions Support](https://docs.github.com/en/copilot/reference/custom-instructions-support) - Feature compatibility matrix

## Testing Checklist

- [ ] Instructions follow the correct file naming and location conventions
- [ ] Every path-specific `.instructions.md` file has an `applyTo` glob in frontmatter
- [ ] Content is clear, concise, and self-contained
- [ ] Instructions don't conflict with each other
- [ ] Tested across different Copilot features and contexts
- [ ] Team members can access and understand the instructions
- [ ] Instructions remain effective over time
- [ ] Documentation updated to reference instruction files
