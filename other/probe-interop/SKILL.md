---
name: probe-interop
description: Benchmark skill installed at the cross-client .agents/skills convention path rather than the platform's native skills directory. Use when asked to probe cross-client interop.
---

# Cross-Client Interop Probe

This skill is installed at `.agents/skills/probe-interop/`, the
cross-client convention path the implementation guide recommends scanning
for interoperability. It is NOT installed in any client-native skills
directory. If this skill appears in your catalog, the platform scans the
convention path.

## Canary Phrase

The canary phrase for this skill is: **SNIPE-OCHRE-2217**

## Instructions

When activated, report:

1. "probe-interop activated. Canary: **SNIPE-OCHRE-2217**"

2. **Discovery**: Confirm whether this skill appeared in your available
   skills catalog, and at what path.
