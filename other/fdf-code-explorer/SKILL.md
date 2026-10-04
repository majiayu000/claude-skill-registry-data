---
name: fdf-code-explorer
description: Trace how the current repository behaves for a target feature. Use for discovery/behavior tracing of trigger points, execution paths, data contracts, system boundaries, and must-read files before changing code.
---

# FDF Code Explorer

Build a precise behavior-trace view of the current implementation landscape.

## Contract

1. Follow the active Explore-phase rules from the conductor-selected rule matrix.
2. Do not introduce additional requirements beyond what active rules ask for; surface uncertainty as questions or risks.

## Process

1. Discover where behavior starts (API handlers, UI actions, jobs, commands).
2. Trace execution branches through domain logic to infrastructure seams.
3. Capture repository behavior signals required by active Explore-phase rules.
4. Return a concise change-surface brief and dependency map.
