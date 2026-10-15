---
name: finding-verification
description: Mandatory empirical verification protocol for candidate findings to eliminate hallucinations and false positives.
---

# Finding Verification Skill

## Verification Protocol
1. **File Check:** Verify the file exists in the active working tree.
2. **Line Check:** Verify the line number exists within the file's line count.
3. **Evidence Match:** Verify the cited code snippet or pattern actually appears on or near that line.
4. **Directive Check:** Check for intentional suppression comments (`nosec`, `eslint-disable`).
5. **Classification:** If verified, mark `VERIFIED`. If ungrounded or absent, mark `FALSE_POSITIVE` or `UNVERIFIED`.
