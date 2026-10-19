---
name: co-gas-xp-loop
description: Run the co-gas no-submit hosted XP loop for a source-backed Coworld policy candidate.
---

# co-gas XP Loop

1. Refresh mandate state.
2. Select the lower owned lane.
3. Diagnose one failure from completed artifacts or focused local runs.
4. Patch source and run focused checks.
5. Update candidate YAML.
6. Run `co-gas submit-source --no-submit`.
7. Run `co-gas xp create` against leaders, lower champion, and bad matchups.
8. Poll with `co-gas xp status`.
9. Fetch and inspect completed artifacts.
10. Submit the exact proven policy version or record a hold.
