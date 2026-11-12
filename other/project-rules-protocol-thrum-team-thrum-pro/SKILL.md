---
name: project-rules-protocol
description: "Use when loading project-specific rules - shared rule skill for role skills."
---


# Project-Specific Rules Protocol
Project-local rules of kind `agent_rule` at `--scope role` were loaded at
session start by your preamble (see the memory rules in your role preamble).
If a project-local rule conflicts with a universal rule above, the
project-local rule wins; surface the conflict in your reply so the user can
decide whether to graduate or remove the override.
