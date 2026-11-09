---
name: repo-map-dotnet
description: Inspect a host .NET repository and persist a concise semantic map of solution structure, responsibilities, and common commands. Use when .NET-specific structure is missing or stale in the Hephaera repository map.
engines: [AGNOSTIC]
---

## When to use
Use when the user asks how the repository works, where functionality lives, or how to get started.

## Output
- solution and project layout
- apps, libraries, and test projects
- likely layer boundaries
- common commands
- notable coupling or risks

## Workflow
1. Run the generic `maintain-repository-map` workflow first.
2. Add tagged .NET solution, project, test, and command entries to `REPO_MAP.md`.
3. Validate and stamp the map only after the semantic entries are current.
