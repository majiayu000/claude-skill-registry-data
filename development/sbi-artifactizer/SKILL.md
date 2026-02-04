---
name: sbi-artifactizer
description: Transform a skill into a Standard Binary Interface (SBI) artifact with deterministic PLAN/EXECUTE/VERIFY/COMMIT phases. Use when a skill must produce verifiable, committed execution artifacts with minimal recursion.
---

# SBI Artifactizer

Create deterministic SBI wrappers for skills with strict phase outputs.

## Contract

- Output only PLAN, EXECUTE, VERIFY, COMMIT, STATUS phases (JSON lines).
- Return 0 for success; non-zero for classified failure.
- Fail the run if no filesystem change was recorded.

## Script

- Run: python skills/sbi-artifactizer/v1/main.py --input runs/sbi_request.json
