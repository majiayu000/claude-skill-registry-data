---
name: toolchain-health
description: |
  Validate Python toolchain alignment between mise, Poetry, and pyproject.
  Use when changing Python versions, editing pyproject.toml, or seeing Poetry/mise
  version solver errors. Invokes /toolchain-health to check:
    - .mise.toml python tool version
    - pyproject.toml python constraint
    - Poetry env python interpreter
  Keywords: python version, mise, poetry, toolchain, env use, lock, install
tags: [dx, tooling, python]
---

# Toolchain Health (Python + mise + Poetry)

Navigate and validate the Python toolchain configuration for this repo.

## Canonical Policy

- **Exact version source of truth:** `.mise.toml`
  - Example:
    ```toml
    [tools]
    python = "3.11.8"
    ```
- **Compatible range in `pyproject.toml`:**
  - Use a range that includes the mise version and allows patch bumps, e.g.:
    ```toml
    [tool.poetry.dependencies]
    python = ">=3.11,<4.0"
    ```
- **Poetry env uses the mise-managed interpreter:**
  - When (re)creating the env:
    ```bash
    poetry env use "$(mise which python)"
    poetry lock
    poetry install --only main
    ```
- **Upgrades:**
  1. Update `.mise.toml` first and run `mise install python`.
  2. Run `poetry env use "$(mise which python)"`.
  3. Only then tighten the `python` range in `pyproject.toml` if necessary.

Agents should avoid changing one layer (mise or pyproject) without considering the others.

## Command: /toolchain-health

Use the `/toolchain-health` command (see `.claude/commands/toolchain-health.md`) to:

1. Print Python from mise (`mise which python` + version).
2. Show the `python = ...` constraint in `pyproject.toml`.
3. Show the Python used by the Poetry env (if any).

## When to Use This Skill

- Editing `.mise.toml` to change Python versions.
- Editing `pyproject.toml` to change the `python` constraint.
- Seeing Poetry errors like:
  - "Current Python version is not allowed by the project"
  - Version solver failures related to `python` markers.
- Before running `poetry lock` or `poetry install` as part of dependency or LLM infra work.

## Agent Guidance

When this skill is relevant:

1. Run `/toolchain-health` to gather the current state.
2. Identify mismatches:
   - If `.mise.toml` and `pyproject.toml` disagree, recommend updating one to match the other, following the policy above.
   - If Poetry env uses a different interpreter than mise, recommend:
     ```bash
     poetry env use "$(mise which python)"
     ```
3. Explain the root cause and suggest a minimal, coherent fix rather than ad-hoc changes.

