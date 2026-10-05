---
name: time-reporting
description: "Trigger: hours, effort, capacity, time tracking, Harvest, weekly allocation. Report team time ethically."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use when analyzing actual hours or capacity.

# Hard Rules
- Actual hours come from the configured tracker linked to Linear issues.
- Do not derive working hours from commits, chat activity or agent output.
- Never rank people or infer performance from time entries.
- Group reports by workstream and project first; show individual detail only to authorized PM/TL.

# Execution Steps
1. Verify time entries map to a Linear issue and date range.
2. Compare actual hours with estimates as calibration, not a productivity score.
3. Highlight missing, duplicate or unlinked entries.
4. Recommend capacity or scope changes.

# Output Contract
Return totals, variance, data-quality caveats and decisions needed.
