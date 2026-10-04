---
name: scbe-npm-prepublish-autopublish
description: Enforce deterministic npm prepublish cleanup and auto-publish workflow gates for SCBE-AETHERMOORE. Use when preparing npm releases, hardening package contents, adding tarball guard checks, or updating GitHub Actions publish jobs to run the same local gates.
---

# SCBE NPM Prepublish Autopublish

Use this skill to keep npm releases clean and repeatable.

## Required Repo Wiring

Ensure these files exist and stay aligned:

- `scripts/npm_prepublish_cleanup.js`
- `scripts/npm_pack_guard.js`
- `package.json` scripts:
  - `clean:release`
  - `publish:prepare`
  - `publish:check:strict`
  - `prepublishOnly`
  - `prepack`
- `.github/workflows/auto-publish.yml`

## Workflow

1. Read baseline config from `package.json`, `.npmignore`, and `.github/workflows/auto-publish.yml`.
2. Wire local gates:
   - `publish:prepare` runs cleanup then build.
   - `publish:check:strict` runs tarball guard.
   - `prepublishOnly` calls `publish:prepare`.
   - `prepack` calls `publish:check:strict`.
3. Wire CI gates in `auto-publish.yml` before `npm publish`:
   - `npm run publish:prepare`
   - `npm test`
   - `npm run publish:check:strict`
4. Validate locally:
   - `npm run clean:release`
   - `npm run publish:prepare`
   - `npm run publish:check:strict`
5. Report changed files and guard results.

## Guard Rules

Fail release if the npm tarball contains dev or Python artifacts:

- `__pycache__/`
- `.pyc`, `.pyo`, `.py`
- `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- `src/`, `tests/`, `scripts/`
- `.zip`

Require these files in the tarball:

- `README.md`
- `LICENSE`
- `dist/src/index.js`
- `dist/src/index.d.ts`

## Resources

- Use `scripts/run_release_guard.ps1` to execute local release gates quickly.
- Read `references/release-guard-rules.md` for checklist and troubleshooting.
