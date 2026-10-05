---
name: co-scientist-params
description: Show the supported Co-Scientist start parameters for Codex users.
---

# co-scientist-params

Goal:

- Explain the high-level run controls that can be used with `$co-scientist-start`.

Execution steps:

1. Run:

   ```bash
   python -m tools.host.project_cli params
   ```

2. For machine-readable details, run:

   ```bash
   python -m tools.host.project_cli params --format json
   ```

3. Summarize only the user-relevant controls. Avoid exposing low-level mechanics knobs unless the user explicitly asks.

Rules:

- If the user wants to begin a run, route back to `$co-scientist-start`.
- Do not invent unsupported flags.
