---
name: figma-to-code
description: "Routes Figma implementation to the original native design-to-code skill with owner scope and evidence rules."
---

# Figma To Code

Load and follow the complete original `figma:figma-design-to-code` skill
exposed by the current host. It is the mandatory prerequisite for Figma design
implementation. Load `figma:figma-use` when the original workflow requires
direct Figma API work. Keep the native plugin's skill, references and tooling
under native ownership; this adapter does not reproduce its workflow.

If the original skill or required Figma connection is missing, the route is
unavailable. Use the host's official Figma plugin setup to install or enable
it and refresh session exposure. Files on disk alone do not establish a live
connection; do not substitute a local summary for the original.

## Owner Policy

- Limit implementation to the requested Figma selection and repository scope.
  Preserve unrelated local changes and project conventions.
- Keep credentials and unrelated private app state outside design evidence.
- Report the actual provider, affected Figma node IDs and source changes,
  rendered verification results and any unavailable evidence.
