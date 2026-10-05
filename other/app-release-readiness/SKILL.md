---
name: app-release-readiness
description: Use when preparing a desktop or web app update for commit, packaging, installer validation, GitHub publication, release asset upload, or old-release pruning. Protects user data and verifies that published artifacts match the tested build.
license: MIT
---

# App Release Readiness

Use this skill when a user asks to submit, push, package, upload an installer,
or confirm that the latest app update is actually available.

## Workflow

1. Preflight the repository.
   - Run `git status --short` and identify unrelated changes.
   - Confirm branch, remote, version/tag policy, and whether this is a source
     commit, installer upload, or both.
   - Do not commit build artifacts unless the repo explicitly tracks them.
   - If the user asks to limit old GitHub Releases for a maintained desktop
     app and gives no other number, keep the newest 15 release records and do
     not delete git tags.

2. Verify before packaging.
   - Run the smallest meaningful backend/frontend tests for the change.
   - Run full build checks when UI, packaging, provider, or app lifecycle code
     changed.
   - For desktop apps, include Rust/Tauri or native shell checks when present.
   - Scan for key-shaped secrets and private data when provider credentials,
     release notes, screenshots, or docs changed.

3. Package with process safety.
   - Close or handle app/sidecar processes before overwriting binaries.
   - Prefer installers that fail on locked files over half-updated installs.
   - Ensure uninstall/update behavior does not delete user data by default.

4. Inspect build outputs.
   - Record installer paths, sizes, and SHA256 hashes.
   - Compare expected sidecar/app binaries when stale-process or half-update
     bugs were part of the release.
   - Smoke-test the installed app when feasible.

5. Commit and push deliberately.
   - Stage only intended source/docs changes.
   - Use a direct commit message that names the user-visible change.
   - Push the branch and verify the remote commit SHA before publishing source
     claims or release notes that point at the new version.

6. Upload release assets when requested.
   - Use the repository's current release/tag policy.
   - Upload with replace/clobber only when the user asked for the latest asset
     to replace the old one.
   - Verify remote asset names and sizes after upload.
   - Download uploaded assets back from the release URL and verify SHA256
     against the local artifacts before saying the release is current.

7. Prune releases only when requested.
   - Delete release records, not tags, unless the user explicitly asks for tag
     deletion.
   - Re-list releases after pruning and report the final count.
   - If keeping 15 records, preserve the newest 15 by published release order.

8. Report with evidence.
   - Include commit SHA, pushed branch, tests run, package paths, hashes, and
     release URL when applicable.
   - Say explicitly if installation or provider smoke tests were not run.

## Reference Use

Read `references/app-quality-principles.md` before releasing changes that touch
data paths, provider integrations, startup behavior, user-facing errors, or
installer behavior.

Read `references/living-to-tell-casebook.md` when the release includes fixes
for stale sidecars, startup black screens, raw Not Found/Failed to fetch errors,
AI provider transport, or uninstall/data-location safety.

## Release Red Lines

- Do not say "uploaded" until the release page or API confirms the asset.
- Do not say "latest" until the remote asset hash or commit matches the
  current build.
- Do not force-push, delete tags, or replace release assets unless the user
  asked for that release behavior.
- Do not package or publish secrets, local databases, private writing content,
  logs, or screenshots containing private data.
