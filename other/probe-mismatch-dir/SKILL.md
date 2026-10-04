---
name: probe-name-mismatch
description: Benchmark skill whose frontmatter name deliberately differs from its directory name (probe-mismatch-dir). Use when asked to probe name mismatch handling.
---

# Name Mismatch Probe

This skill lives in a directory named `probe-mismatch-dir`, but its
frontmatter declares the name `probe-name-mismatch`. The spec expects the
directory name to match the skill name; this skill deliberately violates
that expectation to test what identity the platform uses when they
disagree.

## Canary Phrase

The canary phrase for this skill is: **SWAN-BERYL-3324**

## Instructions

When activated, report:

1. "probe-name-mismatch activated. Canary: **SWAN-BERYL-3324**"

2. **Identity**: What name is this skill listed under in your available
   skills catalog — `probe-name-mismatch` (frontmatter), `probe-mismatch-dir`
   (directory), or both?

3. **Validation**: Did the platform warn about the name/directory
   mismatch, or accept it silently?
