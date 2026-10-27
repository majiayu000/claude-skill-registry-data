---
name: snapshot-testing
description: "Snapshot testing discipline, preventing snapshot blindness, and reviewing structural serialization diffs."
---

# Snapshot Testing Protocol

1. Keep snapshots small and focused on critical structural outputs.
2. Never blindly run --updateSnapshot without reviewing the textual diff.
3. Prefer explicit assertions over sprawling 500-line snapshot dumps.
