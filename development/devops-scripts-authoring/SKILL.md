---
name: devops-scripts-authoring
description: Create or modify devops helper scripts in scripts/ or packages/*/scripts. Use for new wrappers, automation, or script style conventions.
---

# Devops Scripts Authoring

## Conventions

- Use simple shell/python scripts to wrap common tasks.
- Avoid scripts when a popular native command exists.
- Locations: `scripts/` and `packages/*/scripts/`.
- Style: minimal arguments, `--help`, fail fast, forward common errors, idempotent when sensible.
- Avoid Makefiles/Justfiles.

## During development

- Run syntax checks and dry-runs.
- Manually inspect outputs and side effects.
- Document test steps in script comments.

## Documentation

- Use a brief header comment and why-comments.
- Keep usage-level instructions in onboarding docs (skills).
