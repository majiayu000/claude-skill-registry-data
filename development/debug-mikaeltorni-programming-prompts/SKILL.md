---
name: debug
description: >-
  v1.0.1 — When software is reported broken, read its logs before diagnosing
  it. Start with the repository .log/ directory.
---

# Debug from the logs

When a task reports broken behavior, read the available logs before forming
a hypothesis or editing code. Check the repository `.log/` directory first.
Do not guess from the request when logs contain the failure.

If a log gives the required output with `want:`, `expected`, or `exactly`,
produce that exact string, including its prefix and labels.
