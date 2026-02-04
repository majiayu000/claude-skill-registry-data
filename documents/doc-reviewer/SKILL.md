---
name: doc-reviewer
description: Review all .md files for naming conventions, conciseness, consistency, and completeness. Use when creating or editing any markdown file.
allowed-tools: Read, Grep, Glob
---

# Documentation Reviewer

Reviews the quality of markdown documentation.

## Instructions

1. Reference `.claude/rules/documentation.md`
2. Identify target files
3. Execute review based on guidelines
4. Report with fix proposals when issues are found

## Output Format

```
## Documentation Review Results

### ✓ Compliant
- [item]

### ✗ Needs Fix
- file.md:line_number - issue
  Fix proposal: [specific fix details]

📚 Reference: .claude/rules/documentation.md
```

## Notes

- Use only Read, Grep, Glob (no modifications)
- Report issues with file_name:line_number
