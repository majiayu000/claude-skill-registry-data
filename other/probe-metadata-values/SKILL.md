---
name: probe-metadata-values
description: Benchmark skill for testing how platforms handle edge-case YAML values in the metadata frontmatter field. Use when asked to probe metadata value handling.
metadata:
  normal: "baseline"
  empty-double: ""
  empty-single: ''
  explicit-null: null
  tilde-null: ~
  none-null: None
  tagged-null: !!null null
---

# Metadata Value Edge Cases Probe

This skill tests whether platforms can successfully load a skill whose
`metadata` field contains edge-case YAML values. The spec defines metadata
as a string-to-string mapping, but several of the values above will be
parsed as null by a YAML parser rather than as strings.

## Canary Phrase

The canary phrase for this skill is: **THRUSH-FLINT-8294**

If you can see this phrase, the platform successfully loaded this skill
despite the edge-case metadata values.

## Instructions

When activated, report:

1. **Load success**: Did this skill load successfully? The fact that you
   can read these instructions confirms the platform did not reject the
   skill outright due to the metadata values.

2. **Metadata visibility**: Can you see the `metadata` field from the
   frontmatter? If so, list each key and what value you see. Pay
   particular attention to:
   - `normal`: Should be the string `"baseline"` (control value).
   - `empty-double` and `empty-single`: Should be empty strings.
   - `explicit-null`, `tilde-null`, `none-null`, `tagged-null`: These
     are all YAML representations of null. Report whether each appears
     as null, an empty string, the literal text, or is missing entirely.

3. **Key preservation**: Are all seven keys present, or were any dropped?
   Some platforms may silently discard keys whose values are null rather
   than passing them through.

4. **Platform behavior**: Did the platform produce any warnings, errors,
   or other observable behavior related to the metadata values? For
   example:
   - Did it reject any values as invalid?
   - Did it coerce null values to empty strings?
   - Did it strip the metadata field entirely?
   - Or did it pass everything through without issue?
