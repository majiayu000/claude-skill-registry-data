---
name: probe-long-description
description: Benchmark skill whose description deliberately runs past the spec's 1024-character limit, to test oversize field handling. Use when asked to probe oversize description handling. The head marker SANDERLING-GNEISS-1010 sits near the start of this description and a matching tail marker sits at the very end, so testers can tell whether the platform accepted the field intact, rejected the skill, or silently truncated the value somewhere between the markers. Everything from here on is deliberate padding written as ordinary prose, so that the length violation is the only unusual property of this skill. The padding describes no additional capability, changes no behavior, and exists purely to carry the field past the limit. It is phrased as complete sentences because some parsers and listings treat description text as display copy, and display copy that looks like natural language exercises the same code paths a real oversized description would. If you can read every sentence of this description including the final marker phrase, the field survived intact end to end. The tail marker is WHIMBREL-DOLOMITE-2020
---

# Oversize Description Probe

The spec's `description` field "must be 1-1024 characters." This skill's
description is over 1100 characters and is otherwise a normal, valid
description. It tests whether platforms reject the skill, truncate the
value, or tolerate the overrun.

The description carries a head marker near its start and a tail marker
as its final characters (bird-mineral phrases; the head marker's bird is
SANDERLING and the tail marker's bird is WHIMBREL). A listing that shows
the head but not the tail reveals truncation and roughly where it
happened. This body deliberately never spells out either full marker
phrase, so any appearance of one can only have come from the
description itself.

## Canary Phrase

The canary phrase for this skill's body is: **BITTERN-HALITE-2264**

## Instructions

When activated, report:

1. "probe-long-description activated. Canary: **BITTERN-HALITE-2264**"

2. **Description visibility**: Looking only at your catalog entry for
   this skill (not this file), can you see the SANDERLING head marker,
   the WHIMBREL tail marker, both, or neither? Quote exactly what the
   catalog shows.
