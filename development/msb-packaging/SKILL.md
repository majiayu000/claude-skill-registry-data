---
name: msb-packaging
description: "What ships and how it installs: install.sh --dev versus --package and its --uninstall, get.sh the curl|sh entry point with MSB_MANAGER_BASE_URL, scripts/package.sh with its explicit PAYLOAD list, reproducible dist/ and checksums, the symlink/.env/placeholder failures, and VERSION with msbctl self-update. Use when changing the payload or the installer, or when an install, upgrade, uninstall or self-update bug is reported."
---

# Packaging

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

- `install.sh` — two modes: `--dev` (a git checkout; symlinks the commands into it) and `--package` (copies the tree to `~/.local/share/msb-manager/versions/<v>/`, `current` link, commands link through it; keeps current + previous). Seeds `~/.config/msb/` from templates, never overwrites, `--uninstall` removes only what it owns. Never reads stdin (it runs under `curl | sh`) and has no backticks in its unquoted heredoc (they execute).
- `get.sh` — the `curl | sh` entry point (POSIX sh, modeled on microsandbox's installer): resolves the latest release via the GitHub API, downloads the tarball, verifies its sha256, runs the installer inside it. `@@GITHUB_REPO@@` is filled in by `scripts/package.sh`; `MSB_MANAGER_BASE_URL` (+ `--version`) serves assets from a mirror or `file://` for testing.
- `scripts/package.sh` — builds `dist/` (reproducible tarball, repo-bound `get.sh`, `checksums.sha256`) from an explicit PAYLOAD list (keep in step with `install.sh`); fails on symlinks, `.env` files or an unreplaced placeholder; normalizes modes. Does not publish.
- `VERSION` — the release version; `msbctl --version`, `msbctl self-update` (re-runs the packaged `get.sh`; a checkout says `git pull`).
