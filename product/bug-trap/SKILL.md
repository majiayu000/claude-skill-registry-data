---
name: bug-trap
description: Write and fix tests that catch real bugs, by testing behaviour, faking only the device boundary and seeding data the way the product writes it. Use when a bug needs a test that fails first, or a unit test is failing or flaky, or when the user says "add a test for this bug", "fix this failing test" or "why is this test flaky". For the bar every test is held to, use test-like-a-user.
---

# Tests

1. **Test behaviour, not layout.** Tests should survive a UI redesign.
2. **Below the UI first:** engine and service contract tests for what the feature does.
3. **Rendered tests** find elements by role, label or test id. Never by copy or position.
4. **Fake only the device boundary:** native modules, network, disk, clock, memory. No mocks of the project's own code.
5. **Seed through the product's own write paths.** Data enters the way the app writes it (capture, import, analysis), never by `INSERT` into its tables. A hand-seeded row tests your guess of the schema, not the product.
6. **A failing test is a finding.** Fix the cause. Never loosen the test or raise a timeout.
7. **Hard cases:** read `test-like-a-user/reference/test-doctrine.md`. For the full standard on journeys and review verdicts, see `test-like-a-user`.
