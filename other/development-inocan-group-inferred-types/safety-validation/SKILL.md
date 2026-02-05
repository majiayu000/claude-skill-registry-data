---
name: safety_validation
description: Validate changes against .agentignore before commit.
metadata:
  short-description: Safety validation
---

## Purpose
Ensure forbidden zones are never modified.

## Steps
1. Compare modified paths against `.agentignore`.
2. Stop if any forbidden path is touched.
3. Record validation in `ACTION_LOG.md`.
