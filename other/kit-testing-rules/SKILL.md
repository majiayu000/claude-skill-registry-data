---
name: kit-testing-rules
description: "Testing conventions for this project. Use when reading, writing, or reviewing files matching `**/*.test.*`, `**/*.spec.*`, `**/test/**`, `**/tests/**`, `**/__tests__/**`, `**/*_test.go`, `**/test_*.py`, `**/*_test.py`. Do not use for other files."
---

# Testing conventions

- Use the project's existing test framework, helpers, fixtures, and file layout. Do not add a new framework.
- Test observable behavior through public interfaces, not private implementation details.
- Give each test one clear reason to fail. Name it after the behavior it checks.
- Cover the changed behavior, its edge cases, and its failure paths, not only the happy path.
- Keep tests deterministic: control time, randomness, network, and ordering. Do not depend on test execution order.
- Prefer real collaborators or the project's existing fakes over new mocks. Mock only at slow or external boundaries.
- Clean up files, processes, and global state that a test creates.
- When fixing a bug, add a test that fails without the fix.
- Never delete, skip, or weaken an existing test to make a change pass without explaining why to the user.
