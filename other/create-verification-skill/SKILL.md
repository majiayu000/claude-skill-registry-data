---
name: create-verification-skill
description: "Create a project-local Roblox verification skill for Rojo assembly, existing Luau tests, source invariants, authored-context checks, and explicit user-run Studio scenarios."
---

# Create a Roblox verification skill

Inspect the repository's instructions, project files, scripts, test layout, and Studio integration. Create a project-local skill that records only checks the project can actually run.

The generated skill must define:

- project assembly commands, including `rojo build` when Rojo is used;
- existing unit or integration test commands and what each proves;
- source or artifact invariants for security, persistence, remotes, authored models, and configuration when relevant;
- safe Studio context inspection; if source/sync is unavailable, document any user-authorized non-playtest MCP edit as an unverified Studio change rather than a local check;
- a short checklist of user-run Studio scenarios with setup, action, expected observation, and cleanup;
- failure handling and temporary-artifact cleanup.

The generated skill must state that Roblox Studio MCP playtest controls are forbidden. It must not claim Rojo compilation or runtime proof. Validate the new skill and run every non-playtest check it documents before delivery.
