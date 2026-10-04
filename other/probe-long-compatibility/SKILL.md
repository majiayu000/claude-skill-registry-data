---
name: probe-long-compatibility
description: Benchmark skill whose compatibility field runs past the spec's 500-character limit. Use when asked to probe oversize compatibility handling.
compatibility: This compatibility value deliberately runs past the spec's 500-character limit to test oversize field handling, while remaining otherwise ordinary requirement prose. It nominally requires a POSIX shell, network access to nothing in particular, and no specific product, because the length violation should be the only unusual property of this skill. The padding is phrased as complete sentences for the same reason a real compatibility note would be, and it carries a marker as its final characters so truncation is detectable. The tail marker is TURNSTONE-ARAGONITE-3030
---

# Oversize Compatibility Probe

The spec's `compatibility` field "must be 1-500 characters if provided."
This skill's compatibility value is over 500 characters and is otherwise
ordinary requirement prose. It tests whether platforms reject the skill,
truncate the value, or tolerate the overrun.

The compatibility value ends with a tail marker (a bird-mineral phrase
whose bird is TURNSTONE) so truncation is detectable wherever the value
surfaces. This body deliberately never spells out the full marker
phrase, so any appearance of it can only have come from the
compatibility value itself.

## Canary Phrase

The canary phrase for this skill's body is: **KESTREL-BAUXITE-6690**

## Instructions

When activated, report:

1. "probe-long-compatibility activated. Canary: **KESTREL-BAUXITE-6690**"

2. **Field visibility**: Can you see a compatibility value for this
   skill anywhere other than by reading this file, and if so, does it
   end with the TURNSTONE tail marker? Quote exactly what you see.
