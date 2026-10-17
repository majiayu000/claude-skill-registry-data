---
name: heimdall-documentation-review
description: Review documentation for accuracy, clarity, completeness, and consistency.
---

# Documentation Review

## Purpose

Independently review documentation for accuracy, clarity, completeness, and consistency with the implementation.

## When to Use

- Before publishing or delivering documentation to users.
- When recently created or updated documentation needs review.
- When reviewing API documentation, READMEs, or architectural docs.
- To confirm documentation is reliable and useful before it is delivered.

## Workflow

1. **Understand the intended audience.**
   - Identify who will read the documentation (end-users, developers, operators).
   - Determine what they need to accomplish with it.

2. **Verify accuracy.**
   - Check that code examples, commands, and configuration snippets are correct.
   - Verify that the documentation matches the actual implementation.
   - Test instructions if feasible to confirm they produce the expected result.

3. **Assess clarity and structure.**
   - Check that the documentation is well-organized and easy to navigate.
   - Evaluate whether explanations are clear and concise.
   - Look for jargon, ambiguous terms, or missing context.

4. **Identify gaps.**
   - Note missing information: error handling, prerequisites, edge cases, troubleshooting.
   - Check for broken links, missing references, or incomplete sections.
   - Identify sections that assume knowledge the reader may not have.

5. **Document findings.**
   - Report issues by category (accuracy, clarity, completeness).
   - Provide specific suggestions for improvement.
   - Highlight what was done well.

## Quality Criteria

- All code examples and commands are verified to work.
- The documentation is accurate against the current implementation.
- A reader with the expected background can follow the documentation without confusion.
- No dead links, missing sections, or contradictory information.

## Anti-Patterns

- **Write-only documentation**: Creating docs that are never read or maintained.
- **Assuming knowledge**: Skipping fundamentals because "everyone knows this."
- **Copy-paste errors**: Reusing documentation from other projects without adapting it.
- **Documentation rot**: Letting docs fall out of sync with the implementation.
