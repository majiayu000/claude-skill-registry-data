---
name: repo-documenter
description: "Provide repository-wide documentation guidelines under `docs/`. Use tool-based inspection first, and keep `README.md` and `docs/` in sync with the current state of the app."
---

# Repository Documenter Skill

## General Guidance

This skill defines and maintains documentation guidelines for the repository. Primary documentation lives under:

```text
docs/
```

Always use **tool-based inspection first** (MCP tools if configured). Only fall back to CLI when necessary.

Documentation must always reflect **current reality**, not assumptions.

When asked to update documentation:

1. Inspect existing docs (if any).
2. Inspect code/configs/infrastructure via tools.
3. Determine which documentation files make sense for this project.
4. Create/update only relevant files.
5. Never guess — ask for confirmation if unclear.
6. Use **Mermaid diagrams** where they add clarity.

---

## Documentation Structure

### Index File (MANDATORY)

**Always create** `docs/architecture/index.md` as the main architecture entry point when architecture documentation is needed. For repository-level docs, ensure `docs/` contains an appropriate `index.md` or similar entry point for the reader.

This file should:

- Provide a brief overview of the system
- Link to other documentation pages (if any exist)
- Explain the system or repository structure in a way that's readable on its own
- Include a high-level diagram of key components where helpful

### Optional Supporting Documentation Files

Only create additional files if the repository complexity warrants them. Use these templates when relevant (templates live in the skill directory):

- `system-overview.md`
- `cloud-architecture.md`
- `service-architecture.md`
- `cicd-architecture.md`

You can also create custom documents based on the project's specific needs (for example `data-architecture.md`, `security-architecture.md`, `api-architecture.md`, or `usage.md`).

---

## Templates

Template files are provided in this skill directory and may be adapted to fit the project. Remove sections that don't apply, add sections that are needed.

- `index.md` - Entry point template
- `system-overview.md` - Optional system-level template
- `cloud-architecture.md` - Optional cloud infrastructure template
- `service-architecture.md` - Optional service/API template
- `cicd-architecture.md` - Optional CI/CD pipeline template

## Behavioral Rules

- **MANDATORY**: Ensure architecture entry points exist under `docs/architecture/` when architecture content is required.
- Use tool-based introspection before CLI.
- Ask for files or context when uncertain.
- Only create additional documents if the repository complexity warrants them.
- Update diagrams to match reality.
- Keep diagrams readable and scoped.
- Maintain consistency across documents.
- Filenames: All filenames MUST be lowercase and use dashes (-) as word separators. Do not use spaces or underscores.
- README maintenance: Keep the repository `README.md` up to date with the current state of the application. Prefer an overview-only README that links to the relevant `docs/` pages for detailed information.
- Suggested (non-mandatory): Add `docs/usage.md` to provide detailed usage guidelines and examples for users.
- If a suggested template doesn't fit, adapt or skip it.
- When in doubt about which files to create, ask the user.

## Notes

- When adding `docs/usage.md`, include a `Recommended` section near the top with the preferred, simple way to run the app and an optional minimal example config if the app requires configuration.
