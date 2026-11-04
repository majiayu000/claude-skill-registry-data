---
name: nix-config
description: Configure this Nix repo, Pi skills and profiles, credentials, and local system setup with task-specific recipes. Use for configuration changes, diagnosis, validation, or sync.
---

# Nix Configuration

Use the recipe matching the task. Read only its linked references as needed; do not load all recipes for every request.

| Task | Start here |
| --- | --- |
| Add a Pi skill | `recipes/add-skill.md` |
| Add or change a Pi profile | `recipes/add-profile.md` |
| Onboard a macOS host | `recipes/add-host.md` |
| Edit Nix or agent configuration | `recipes/change-nix-config.md` |
| Add, edit, or reference a secret or provider | `recipes/manage-secrets.md` |
| Find the source of an active setting or diagnose a failure | `recipes/diagnose-config.md` |
| Validate and roll out a configuration change | `recipes/validate-and-sync.md` |

## Common rules

- Change the repository source of truth, not generated files under `~/.config/nix-agents`.
- Never put plaintext secrets in Git or the Nix store; use the repository's SOPS rules.
- Prefer current code and inventory over old examples. Follow `references/coding-style.md` for Nix edits.
- After a change, run the relevant checks from `recipes/validate-and-sync.md` before syncing.
