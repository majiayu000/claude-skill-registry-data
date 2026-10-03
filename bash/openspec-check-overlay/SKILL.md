---
name: openspec-check-overlay
description: Check that the intent-driven Codex overlay is compatible with the installed OpenSpec CLI. Use after installing/updating OpenSpec or the template.
license: MIT
compatibility: Requires OpenSpec CLI 1.3.x or compatible public commands.
---

**Project context preflight before workflow actions**: before this skill takes a workflow action, follow the `project-constitution` skill. Read root `CONSTITUTION.md` when present, enforce relevant project rules, stop on material conflicts, and follow the strict missing-constitution bootstrap/diagnostic policy. For architecture-sensitive work, also read `ARCHITECTURE.md`, `adr/README.md`, and relevant in-force `adr/*.md`. Read `.secrets.local.env` only when the current workflow actually needs a listed external system, and never reveal secret values.


# OpenSpec Overlay Check

Validate the project-local `intent-driven` overlay without patching OpenSpec. Prefer `scripts/check-overlay` when present; otherwise follow the manual steps below.

## Steps

1. Show the OpenSpec version:
   ```bash
   openspec --version
   ```

2. List schemas and confirm `intent-driven` is project-local:
   ```bash
   openspec schemas --json
   ```

3. Validate the schema:
   ```bash
   openspec schema validate intent-driven
   ```

4. List active changes with a command valid in OpenSpec 1.3.x:
   ```bash
   openspec list --json
   ```

5. Create a temporary smoke change using the intent-driven schema:
   ```bash
   openspec new change zz-smoke-intent-overlay-<unique> --schema intent-driven
   openspec status --change zz-smoke-intent-overlay-<unique> --json
   # after writing minimal proposal/specs/grill/design/design-review/adr/test-plan/tasks artifacts:
   openspec instructions apply --change zz-smoke-intent-overlay-<unique> --json
   ```

6. Report the compatibility layer for any failure:
   - OpenSpec CLI command changed
   - local `intent-driven` schema invalid
   - Codex prompt/skill adapter mismatch
   - generated skill mismatch
   - existing project artifact issue

7. Cleanup policy:
   - The script may automatically delete only a `zz-smoke-intent-overlay-*` change that it created in the same run.
   - Use `--keep-smoke` when the user wants to inspect the smoke change.
   - Never delete user-created changes or project artifacts silently.

## Guardrails

- Do not run bare `openspec status --json`; OpenSpec 1.3.x requires `--change`.
- Do not modify OpenSpec package files.
- Do not overwrite `openspec/changes/**`, `openspec/specs/**`, or `adr/**`.
