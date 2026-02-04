---
name: release-codex-workspace-launcher
description: "Release codex-workspace-launcher: record pinned codex-kit/zsh-kit refs in CHANGELOG, run local real-Docker e2e, and publish via docker branch."
---

# Release Workflow (codex-workspace-launcher)

This repo publishes the launcher image from the `docker` branch (see `.github/workflows/publish.yml`).

This project-specific workflow extends the base `release-workflow` with two non-negotiables:

1) Record the pinned upstream pair (`VERSIONS.env`) in the release entry in `CHANGELOG.md`.
2) Run local real-Docker E2E (full matrix) and **abort** if it fails.

## Contract

Prereqs:

- Run in this repo root.
- Working tree is clean before running the E2E gate.
- Docker is available (E2E is real Docker): `docker info` succeeds.
- E2E environment is configured (via `direnv`/`.envrc` + `.env`, or equivalent).
  - At minimum, repo-backed cases require `CWS_E2E_PUBLIC_REPO`.
  - Auth-heavy cases require additional secrets/mounts (see `DEVELOPMENT.md`).
- `git` available on `PATH`.
- Optional (recommended): `gh` available + `gh auth status` succeeds (for tagging / releases / branch ops).

Inputs:

- Release version: `vX.Y.Z`
- Optional: release date (`YYYY-MM-DD`; defaults to today)
- Optional: E2E image tag (defaults to `cws-launcher:e2e`)

Outputs:

- `CHANGELOG.md` updated with a `## vX.Y.Z - YYYY-MM-DD` entry that includes:
  - `### Upstream pins`
    - `- zsh-kit: <ZSH_KIT_REF>`
    - `- codex-kit: <CODEX_KIT_REF>`
- Local E2E run result (pass required; artifacts under `out/tests/e2e/`)
- Optionally:
  - Git tag `vX.Y.Z` pushed
  - `docker` branch fast-forwarded to `main` to trigger publish

Stop conditions:

- Local E2E fails: stop immediately; do not publish; report the failure output and ask how to proceed.
- Changelog audit fails (missing pins / bad version heading / placeholders): stop; fix before publishing.

## Key rule: E2E gate is mandatory

Run E2E before publishing and before any irreversible actions.

Recommended: run via `direnv exec .` so your `.env` is applied:

```sh
set -euo pipefail
set -a; source ./VERSIONS.env; set +a

direnv exec . ./scripts/bump_versions.sh \
  --zsh-kit-ref "$ZSH_KIT_REF" \
  --codex-kit-ref "$CODEX_KIT_REF" \
  --image-tag cws-launcher:e2e \
  --run-e2e
```

Notes:

- `--run-e2e` forces `CWS_E2E=1`, `CWS_E2E_FULL=1`, and sets `CWS_E2E_IMAGE=<image-tag>`.
- Destructive `rm --all --yes` coverage remains gated by `CWS_E2E_ALLOW_RM_ALL=1`.

## Workflow

1. Decide version + date
   - Version: `vX.Y.Z`
   - Date: `YYYY-MM-DD` (default: `date +%Y-%m-%d`)

2. Run mandatory local E2E gate (real Docker)
   - Use the command in “Key rule: E2E gate is mandatory” above.
   - If it fails: stop and report (use `.codex/skills/release-workflow/references/OUTPUT_TEMPLATE_BLOCKED.md`).

3. Prepare the changelog (records upstream pins)
   - Use the helper that moves `## Unreleased` into a new release entry and injects pins from `VERSIONS.env`:
     - `./scripts/release_prepare_changelog.sh --version vX.Y.Z`
   - Review `CHANGELOG.md` (fill out wording; remove `- None` if you added real bullets).

4. Run required repo checks (per `DEVELOPMENT.md`)
   - `.venv/bin/python -m ruff format --check .`
   - `.venv/bin/python -m ruff check .`
   - `.venv/bin/python -m pytest -m script_smoke`

5. Commit the release notes
   - Suggested message: `chore(release): vX.Y.Z`
   - Do not run `git commit` directly; use the repo’s Semantic Commit helper (see `AGENTS.md`).

6. Audit (strict)
   - Run after committing (audit requires a clean working tree):
     - `./scripts/release_audit.sh --version vX.Y.Z --branch main --strict`

7. (Optional) Tag the release
   - Create: `git tag vX.Y.Z`
   - Push: `git push origin vX.Y.Z`
   - Optional GitHub Release:
     - Extract notes from `CHANGELOG.md` and publish with `gh release create`.

8. Publish images (this repo’s publish trigger)
   - Fast-forward `docker` to `main` and push:
     - `git fetch origin`
     - `git checkout docker`
     - `git merge --ff-only origin/main`
     - `git push origin docker`
     - `git checkout main`

9. Verify publish
   - Follow `docs/runbooks/INTEGRATION_TEST.md` (record the workflow run URL + tags evidence).

## Helper scripts (project)

- Prepare changelog + inject upstream pins: `scripts/release_prepare_changelog.sh`
- Audit changelog entry (pins + basic release checks): `scripts/release_audit.sh`
- Build + verify + local E2E (full matrix): `scripts/bump_versions.sh --run-e2e`

## Output templates

- Success: `.codex/skills/release-workflow/references/OUTPUT_TEMPLATE.md`
- Blocked: `.codex/skills/release-workflow/references/OUTPUT_TEMPLATE_BLOCKED.md`
