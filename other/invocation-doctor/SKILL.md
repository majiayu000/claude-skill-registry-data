---
name: invocation-doctor
description: Test and improve whether an agent invokes a skill on the right requests and avoids invoking it on near-miss requests. Use when a skill works explicitly but is under-triggered, over-triggered, or has a weak description.
---

# Invocation Doctor

1. Create positive, near-miss negative, and ambiguous trigger cases.
2. Split cases before optimizing; do not tune on every example.
3. Use Waza when available to run the actual trigger suite.
4. Rewrite only the skill description first; avoid bloating the body to solve discovery.
5. Compare held-out precision/recall before vs after.
6. Publish both regressions and improvements.

