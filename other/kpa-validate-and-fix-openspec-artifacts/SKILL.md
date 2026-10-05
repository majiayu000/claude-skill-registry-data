---
name: kpa-validate-and-fix-openspec-artifacts
description: Run comprehensive validation of all OpenSpec specs and fix issues found
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Run comprehensive validation of all OpenSpec specs and fix issues found.

**Steps**

1. Run this command to perform a comprehensive validation of all the specs:

   ```bash
   openspec validate --all --strict --json
   ```

2. Fix any issues found, prioritizing CRITICAL issues first.
3. After fixing, re-run the validation to ensure all issues are resolved.
