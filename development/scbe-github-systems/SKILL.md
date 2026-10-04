---
name: scbe-github-systems
description: Navigate and develop Issac Davis' SCBE-AETHERMOORE projects with a consistent GitHub workflow. Use for repo orientation (14-layer pipeline, Sacred Tongues, Polly Pads), running build/test/demo/API, and git/GitHub tasks (branching, Conventional Commits, PR reviews, CI workflows, releases) in SCBE repos like SCBE-AETHERMOORE-working and scbe-ultimate.
---

# SCBE GitHub + Systems

## Quick Start

1. Identify the repo in scope and the goal (feature, fix, refactor, docs, release, PR review).
2. Read the repo's AI/developer instructions first and treat them as source of truth:
- `SCBE-AETHERMOORE-working/CLAUDE.md`
- `SCBE-AETHERMOORE-working/INSTRUCTIONS.md`
- `SCBE-AETHERMOORE-working/.cursorrules`
- `scbe-ultimate/README.md`
3. Run the baseline checks before making claims about behavior:
- `npm test`
- `npm run typecheck`
- `python -m pytest tests/ -v`
4. Follow the repo's commit/PR conventions (Conventional Commits; see `references/github.md`).

## Repo Map

- Primary dev monorepo: `SCBE-AETHERMOORE-working`
- NPM/package-focused repo: `scbe-ultimate`
- If `SCBE-AETHERMOORE-BEST` exists, treat it as a snapshot/symlink and prefer `SCBE-AETHERMOORE-working` for active changes.

## Where Things Live (SCBE-AETHERMOORE-working)

- Core pipeline (14 layers): `SCBE-AETHERMOORE-working/src/harmonic/`
- Hyperbolic operations (layers 5-7): `SCBE-AETHERMOORE-working/src/harmonic/hyperbolic.ts`
- Harmonic wall (layer 12): `SCBE-AETHERMOORE-working/src/harmonic/harmonicScaling.ts`
- Crypto primitives/envelopes: `SCBE-AETHERMOORE-working/src/crypto/`
- Fleet/multi-agent orchestration: `SCBE-AETHERMOORE-working/src/fleet/`
- FastAPI server: `SCBE-AETHERMOORE-working/src/api/` (see `INSTRUCTIONS.md` for how it is launched)
- Tests: `SCBE-AETHERMOORE-working/tests/`
- CI workflows: `SCBE-AETHERMOORE-working/.github/workflows/`

## GitHub Workflow (Local-First)

1. Check current state: `git status`, `git diff`, `git log -n 20 --oneline`.
2. Create a branch aligned with your change: `feat/...`, `fix/...`, `docs/...`, `chore/...`.
3. Commit with Conventional Commits (see `SCBE-AETHERMOORE-working/CLAUDE.md` and `references/github.md`).
4. Before opening/updating a PR, run the repo test suite and check `.github/workflows/` for CI expectations.
5. In PR reviews, map changes to layers/modules where possible and look for security regressions (crypto, secrets, constant-time ops).

## References

- Repo map and entrypoints: `references/scbe-repos.md`
- Core SCBE concepts (layers, tongues, states): `references/scbe-concepts.md`
- GitHub/PR checklist tailored to SCBE repos: `references/github.md`

## GitLab pond integration

Treat GitLab as a separate pond (lore/research) that feeds GitHub (code + public surfaces) via explicit mirroring.

- Read-only health check: `C:\Users\issda\SCBE-AETHERMOORE\scripts\gitlab\pond_flush.ps1`
- Mirror push: `C:\Users\issda\SCBE-AETHERMOORE\scripts\gitlab\mirror_push.ps1`
- Skill: `scbe-gitlab-pond-integration`
