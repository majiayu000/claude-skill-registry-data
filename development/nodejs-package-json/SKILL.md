---
name: nodejs-package-json
description: Patch a Node.js project's package.json for standard build automation. Use when asked to add/standardize package.json scripts like prebuild/postbuild for TypeScript builds (rimraf dist + tsc-alias), adjust prebuild for Next.js (rimraf dist .next), or ensure an existing package.json pkg config includes required scripts/assets/targets/outputPath.
---

# Node.js `package.json`

## Goal

Quickly and safely update `package.json` to include:
- `scripts.prebuild`: `rimraf dist` (or `rimraf dist .next` for Next.js)
- `scripts.postbuild`: `tsc-alias`
- If `pkg` config exists: ensure `scripts/assets/targets/outputPath` contain required entries

## Workflow

1. Run the patcher (auto-detects Next.js):
   - `python3 "${CODEX_HOME:-$HOME/.codex}/skills/nodejs-package-json/scripts/patch_package_json.py" --path package.json`

2. If Next.js auto-detection is wrong, force it:
   - Force Next.js: `--nextjs true`
   - Force non-Next.js: `--nextjs false`

3. If `prebuild` or `postbuild` already exist with different values:
   - Re-run with `--force` to overwrite to the recommended defaults.

## Notes

- This skill edits `package.json` only; it does not install dependencies. Ensure `rimraf` and `tsc-alias` are available (typically as `devDependencies`).
- The patcher only edits `pkg` settings if a top-level `pkg` object already exists (it does not add one).
