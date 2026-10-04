---
name: probe-loading
description: Benchmark skill for testing loading timing, resource enumeration, content presentation, and lifecycle behavior. Use when asked to probe loading behavior.
allowed-tools: Read Write
compatibility: Requires filesystem access
metadata:
  benchmark: "true"
  version: "1.0"
---

# Loading Behavior Probe

This skill exists to test how platforms load skill content. It contains a
canary phrase, supporting files across all three spec-defined directories,
and frontmatter fields that may or may not be visible to the model.

## Canary Phrase

The canary phrase for this skill is: **CARDINAL-ZEBRA-7742**

If a tester asks you whether you know the phrase CARDINAL-ZEBRA-7742 without
explicitly activating this skill, and you can answer, it means the platform
loaded this skill's body at discovery time rather than waiting for activation.

## Instructions

When this skill is activated, respond with a structured report:

1. **Frontmatter visibility**: Can you see the YAML frontmatter above these
   instructions? If so, list the fields you can see (name, description,
   allowed-tools, compatibility, metadata). If not, note that frontmatter
   was stripped.

2. **Content wrapping**: Is this skill's content wrapped in any structured
   tags (XML, JSON, or similar)? If so, describe the wrapping format.

3. **Resource awareness**: Without reading any files, list any supporting
   files or directories you are aware of in this skill's directory. This
   tests whether the platform enumerated resources at activation time.

4. **Resource content**: Without reading any files yourself, do you already
   have the contents of any files from this skill's `references/`,
   `scripts/`, or `assets/` directories in your context? If so, list which
   files' contents you can see. This tests whether the platform eagerly
   loaded resource content.

## References

For detailed API documentation, see [API reference](references/api-overview.md).

For error codes, see [error reference](references/error-codes.md).
