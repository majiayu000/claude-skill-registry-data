---
name: test-triage
description: Diagnose failing TinyCart unittest cases, identify the smallest responsible change, and report the failure without unrelated edits.
---

# Test triage

Run `python run_tests.py`, isolate one failing behavior at a time, and avoid changing fixtures merely to make an assertion pass.
