---
name: kpa-apply-tdd
description: Apply in Red/Green TDD style - implement change tasks with failing tests first
metadata:
  author: kpa
  updated-date: "2026-03-19"
argument-hint: "[change name]"
---

Run the `/opsx:apply $ARGUMENTS` command to apply the change. For anything that requires a code change, use red/green TDD style to implement the change.

Red/green TDD style means:
1. Write a test for the new functionality (RED phase)
2. Run the test and it should fail (RED phase)
3. Write the code to make the test pass (GREEN phase)
4. Run the test and it should pass (GREEN phase)