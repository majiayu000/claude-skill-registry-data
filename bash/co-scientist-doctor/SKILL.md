---
name: co-scientist-doctor
description: Diagnose the local Co-Scientist host-agent environment from Codex.
---

# co-scientist-doctor

Goal:

- Inspect whether the local project has the required runtime dependencies, skill installation surface, dashboard tooling, and optional bridge configuration.

Execution steps:

1. Run:

   ```bash
   python -m tools.host.project_cli doctor
   ```

2. If structured output is needed, run:

   ```bash
   python -m tools.host.project_cli doctor --format json
   ```

3. Report failing and warning checks with the exact recommended command from the doctor payload.

Rules:

- Do not guess installed state from memory. Always call the doctor command.
- Warnings for optional bridges are not pipeline failures unless a requested feature depends on that bridge.
