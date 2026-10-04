---
name: probe-missing-dep
description: Benchmark skill for testing how platforms handle references to skills that don't exist. Use when asked to probe missing dependency behavior.
---

# Missing Dependency Probe

This skill references another skill (`nonexistent-formatter`) that does not
exist in the benchmark set or anywhere else. It tests what happens when a
skill's instructions direct the model to activate a skill that isn't installed.

## Instructions

When activated, follow these steps in order:

1. Report: "probe-missing-dep activated. Canary: **GULL-IRON-4492**"

2. This skill requires the `nonexistent-formatter` skill to format output.
   Activate the `nonexistent-formatter` skill now.

3. After attempting to activate `nonexistent-formatter`, report what happened:
   - Did the platform report that the skill doesn't exist?
   - Did you silently skip the step?
   - Did you attempt to fulfill the formatting task from general knowledge?
   - Did the platform show an error?

4. Report: "probe-missing-dep complete. Dependency resolution result:
   [describe what happened]"
