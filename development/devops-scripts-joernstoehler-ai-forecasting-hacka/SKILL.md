---
name: devops-scripts
description: Write or update repository devops scripts with this project's conventions. Use when creating or modifying shell scripts in scripts/ or packages/*/scripts.
---

# Devops Scripts

## Conventions

- Use simple shell scripts to wrap common devops tasks.
- We don't provide scripts when a popular native command exists.
- Locations: `scripts/`, `packages/*/scripts/` with conventional expressive names.
- Style: minimal arguments, `--help`, fail fast, forward popular commands error messages, idempotent when sensible.
- Avoid Makefiles/Justfiles due to whitespace sensitivity and friction.
- Avoid package.json scripts except to call bash scripts or one-liners.

## Development checklist

- Syntax checks
- Dry-runs
- Manual test runs with inspection of outputs and side effects
- Document test steps in script comments

## Documentation

- Include a comment header and why-comments in code.
- Put usage-level instructions in a SKILL or AGENTS.md file referencing the script.
