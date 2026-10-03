---
name: validate-matters
description: "Checks data integrity across all matters and the index. Use when Mandy says 'validate', 'check data', 'something seems off', 'fix index', or when errors suggest data corruption. Can auto-repair common issues."
---

# Validate Matters

## Instructions
1. Check each matter directory: matter.json exists, valid JSON, schema compliance, activity-log exists, PDFs have extracts, letters referenced exist, valid dates, valid enums.
2. Check index.jsonl: every dir has entry, every entry has dir, fields match matter.json.
3. Report: valid count, issues, mismatches.
4. Offer to fix: rebuild index from matter.json files, add missing flags, fix enums.
5. If fixes applied: commit with "validate-matters: system — Fixed {n} issues."
