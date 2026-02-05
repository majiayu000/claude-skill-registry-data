---
name: software-engineer
description: Development workflows for Rails applications. Use when implementing features, fixing bugs, or making code changes. Currently provides the TDD Red-Green implementation workflow.
---

# Software Engineer

## Overview

This skill provides development workflows for Ruby on Rails applications. It defines methodologies for different types of engineering work.

## Workflows

### Implementation Workflow (TDD Red-Green)

When implementing features or fixing bugs, follow the Test-Driven Development cycle.

#### RED Phase

Write failing tests FIRST:
- Use fixtures for test data (check `test/fixtures/` for existing patterns)
- Refer to rails-basecamp-engineer skill references for test patterns
- Run `bin/ci` to confirm tests fail for the RIGHT reason
- Do NOT proceed until you have a failing test

#### GREEN Phase

Write the MINIMAL code to make tests pass:
- Refer to rails-basecamp-engineer skill references for implementation patterns
- Run `bin/ci` - do NOT proceed until all tests pass
- Avoid over-engineering; implement only what's needed for the test

#### Error Handling

If `bin/ci` fails:
- Read the error output carefully
- Fix the failing tests or implementation
- Do NOT proceed to the next phase until CI is green
- If stuck, explain the issue and ask for guidance

If you discover additional work needed:
- Create a new BD issue: `bd create "Discovered issue" -t task -p 2 --deps discovered-from:<current-ticket> --json`
- Continue with current task unless the discovery is blocking

#### Completion Criteria

- All tests pass (`bin/ci` or `bin/rails test`)
- Implementation is minimal and focused
- Code follows patterns from rails-basecamp-engineer references
