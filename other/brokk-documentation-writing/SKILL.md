---
name: brokk-documentation-writing
description: Create and maintain technical documentation and project documentation.
---

# Documentation Writing

## Purpose

Create clear, accurate, and maintainable documentation that helps users and developers understand, use, and contribute to the project.

## When to Use

- When implementing a feature that needs usage documentation.
- When creating or updating READMEs, API docs, or architecture guides.
- When onboarding documentation needs to be created or updated.
- After code changes that affect documented behavior or interfaces.

## Workflow

1. **Understand the audience.**
   - Identify who will read the documentation (end-users, contributors, operators).
   - Determine what they need to accomplish and what they already know.

2. **Identify what to document.**
   - Focus on what is not obvious from the code itself.
   - Cover: purpose, setup, usage, configuration, examples, troubleshooting.
   - Prioritize accuracy over completeness.

3. **Write clearly.**
   - Use consistent terminology and phrasing.
   - Include concrete examples — code snippets, commands, expected output.
   - Explain the "why" as well as the "how."

4. **Structure for readability.**
   - Use headings, lists, and tables to organize information.
   - Put the most important information first.
   - Keep sections focused and reasonably sized.

5. **Verify the documentation.**
   - Check that code examples work as written.
   - Review for typos, broken links, and outdated information.
   - Ensure a newcomer can follow the documentation without confusion.

6. **Report.** Summarize completed work and remaining concerns to the requesting agent.

## Quality Criteria

- The documentation is accurate against the current implementation.
- Code examples and commands are tested and work.
- The intended audience can follow the documentation without prior context.
- The documentation is structured for scanning, not just linear reading.

## Anti-Patterns

- **Copy-paste documentation**: Reusing docs from other projects without adapting them.
- **Documentation rot**: Letting docs fall out of sync with the code.
- **Wall of text**: Large paragraphs without structure or visual breaks.
- **Assuming knowledge**: Skipping fundamentals that the reader needs.
