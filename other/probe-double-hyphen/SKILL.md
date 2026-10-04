---
name: probe--double-hyphen
description: Benchmark skill whose name violates the consecutive-hyphen rule. Use when asked to probe double-hyphen name handling.
---

# Consecutive-Hyphen Name Probe

The spec's `name` field "must not contain consecutive hyphens." This
skill's name contains `--` (and matches its directory name exactly, so
only the hyphen rule is violated). It tests whether platforms reject,
repair, or tolerate consecutive hyphens.

## Canary Phrase

The canary phrase for this skill is: **PETREL-GALENA-3306**

## Instructions

When activated, report:

1. "probe--double-hyphen activated. Canary: **PETREL-GALENA-3306**"

2. **Catalog identity**: What name does this skill appear under in your
   catalog: with the double hyphen intact, collapsed to one hyphen, or
   something else?
