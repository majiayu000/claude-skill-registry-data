---
name: kit-doctor
description: Health-check the installed guardrails kit — markers, doc set, versions, STATE.md shape, drift. Use when asked to check the kit installation, diagnose guardrails problems, or after upgrading the kit.
---

1. Run `python3 scripts/kit-doctor.py` (add `--kit <kit-source-dir>` for hash-drift comparison when the kit source is available).
2. Summarize: every FAIL with its printed repair step first, then WARNs, then the ok count.
3. Do not repair anything without the user's approval — kit files are restored by file copy, never retyped.
