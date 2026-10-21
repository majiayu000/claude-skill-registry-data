---
name: mvp-test-factory
description: Build a real unit, API, UI, and performance test foundation for an MVP or prototype that has little or no automated testing
agent: mvp-test-factory
argument-hint: "[project-path]"
pass-full-context: true
pass-conversation-history: true
---

# /mvp-test-factory

Build a test foundation for an MVP or prototype using real execution evidence.

Target project: $ARGUMENTS

## Usage

- `/mvp-test-factory` inspects the current repository.
- `/mvp-test-factory /path/to/project` inspects the specified repository.

The workflow:

1. Detects the stack, package manager, source boundaries, and existing tests.
2. Requires a clean Git working tree and a working k6 installation.
3. Shows the proposed frameworks, dependencies, files, and commands for approval.
4. Bootstraps a meaningful unit-test baseline when none exists.
5. Prepares shared end-to-end test configuration before parallel work starts.
6. Authors API, UI, and performance tests in separate scopes.
7. Runs build, unit, API, UI, and performance gates in order.
8. Reports the actual diff and real results for human review.

The factory never changes production source automatically. A product defect found by a test is reported for human direction.
