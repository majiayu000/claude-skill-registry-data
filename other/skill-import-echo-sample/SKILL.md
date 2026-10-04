---
name: Echo Skill Sample
skill_key: echo_skill_sample
description: Echo input parameters as JSON.
runner:
  kind: python_file
  target: echo.py
requires:
  always: true
---

This skill echoes input parameters.
