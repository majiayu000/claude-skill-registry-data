---
name: tracing-requirements
description: Validates the SYS→PRD→SW requirement traceability chain by reconciling database entries with code docstring tags. Use when checking requirement coverage, finding orphaned code, or generating a coverage matrix.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Bash
  argument-hint: [requirements-file-or-directory]
  stability: stable
  content-hash: sha256:42824ff9b1f1482d657d77f24a9d099c0c68448d8d7a4eb33d275347a09f6a29
  last-verified-cc-version: 1.0.34
---

# Requirement Traceability Validation

**Target**: $ARGUMENTS

Validate the full requirement hierarchy by reconciling the requirements source with code docstring tags.

## References (MUST READ)

Read these before proceeding:

- `references/requirement-tagging.md` — `@requirement`/`@parent`/`@test` spec, reconciliation algorithm

## Workflow

1. **Grep all C files** for `@requirement`, `@parent`, and `@test` tags → build tag inventory
2. **Read requirements source** — `docs/requirements.md`, CSV, or SQL dump
3. **Validate 3-level hierarchy:**
   - Every SW-REQ has a `@parent` PRD-REQ
   - Every PRD-REQ traces to a SYS-REQ
   - No broken parent links
4. **Generate findings report** with categories:
   - **Unimplemented:** SW-REQ in database but no `@requirement` tag in code
   - **Orphaned code:** `@requirement` tag in code but no matching DB entry
   - **Broken parents:** `@parent` references a non-existent PRD-REQ
   - **Untested:** SW-REQ without matching `@test` tag
   - **Dead code candidates:** Functions without any requirement tag
5. **Output coverage matrix:**

   ```markdown
   | Requirement | Code File:Line | Test ID | Status |
   |-------------|---------------|---------|--------|
   | SW-REQ-001  | src/emv.c:42  | TEST-001| OK     |
   | SW-REQ-002  | —             | —       | MISSING|
   ```

## Output Format

```markdown
# Traceability Report

## Summary
- Total SW-REQ: N
- Implemented: N (N%)
- Tested: N (N%)
- Orphaned code tags: N
- Broken parent links: N

## Unimplemented Requirements
...

## Orphaned Code
...

## Coverage Matrix
...
```

## Rules

- Scan all `*.c` and `*.h` files, not just `src/`
- Report findings — do not auto-fix requirement files
- Include file path and line number for every code finding
- Sort coverage matrix by requirement ID
