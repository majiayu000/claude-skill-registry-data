---
name: agilab-installer
description: Guidance for installing AGILAB, installing apps/pages, and debugging install/test failures.
license: BSD-3-Clause (see repo LICENSE)
metadata:
  updated: 2026-01-09
---

# AGILAB Installer Skill

Use this skill when working on:
- `install.sh` / `install.ps1` (root installer)
- `src/agilab/install_apps.sh` / `src/agilab/install_apps.ps1` (apps/pages installer)
- `src/agilab/apps/install.py` (app install entry)
- Data seeding / dataset archives / post-install hooks

## Golden Rules

- Use `uv --preview-features extra-build-dependencies …` for Python entrypoints.
- Do not add silent fallbacks (detect missing capabilities and raise actionable errors).
- Keep installs **idempotent**: rerunning should not wipe user data or re-download unnecessarily.

## Common Commands

- Full install (macOS/Linux):
  - `./install.sh --non-interactive --cluster-ssh-credentials user:pass --apps-repository /path/to/apps-repo --install-apps --test-apps`
- Apps/pages install only:
  - `cd src/agilab && ./install_apps.sh --test-apps`

## Debugging Patterns

- **“Does not appear to be a Python project”**
  - You are installing a directory without `pyproject.toml`/`setup.py`.
  - Ensure the installer runs `uv pip install -e .` from the repo root.

- **App install fails with missing worker/manager**
  - Validate both manifests exist:
    - manager: `.../<app>_project/pyproject.toml`
    - worker:  `.../<app>_project/src/<app>_worker/pyproject.toml`

- **Dataset extraction wipes seeded files**
  - Avoid mtime heuristics on extracted files; use a stamp file tied to the archive.
  - Prefer linking to shared datasets rather than copying to each app.

## Data Dependencies Between Apps

Some apps depend on outputs of others (e.g. LinkSim needs satellite trajectories).
Preferred approach:
- Install/seed the producing app first.
- Reuse outputs via symlink/junction into the dependent dataset folder to avoid duplication.

