---
name: release
description: The gated release procedure — preconditions, version choice, CHANGELOG, Nick-signed tag, GitHub release via release.yml (a draft for a plain tag, a published pre-release for a -suffix tag). Use for any tagged release; releases are Tier-H (Nick signs off, per ADR-000).
---

# release

Releases are Tier-H: Nick signs off, always (ADR-000). The tag push is the
sign-off act; `release.yml` turns a plain `v*` tag into a draft GitHub release, and a tag with a pre-release suffix (`v0.1.0-alpha.1`) into a published pre-release for testers.

## Preconditions — all four, verified fresh, before any tag

1. CI green on `main` (`gh run list --branch main`), including the
   dogfood-check and p2-hardening-check jobs.
2. `go run ./e2e/p2-hardening` passes locally against the release commit. It
   is the P2 exit gate (issue #81) and runs the P1 canary, `e2e/dogfood`, as
   its last step, so this one command is both. A release **does not ship**
   when it fails. What it proves and how to read a failure: the manual
   section "The P2 hardening gate" (`docs/manual.md`).
3. The latest principal-review report shows no unresolved invariant drift
   (open drift → fix or get Nick's explicit acceptance first).
4. **Nick's sign-off is recorded** — on the release issue or in writing.
   Session-scoped authorization counts only if it explicitly names releasing.

## Procedure

1. Pick the version: `v0.x.y` SemVer (session-1 decision — pre-1.0, tags only
   at Nick-gated releases). Minor for features, patch for fixes; pre-1.0
   breaking changes ride minor bumps but must be called out in the CHANGELOG.
2. Update `CHANGELOG.md` (Keep a Changelog format; create the file on the
   first release): move Unreleased into the new version section, dated. Land
   this via a normal PR before tagging — the tag points at a clean `main`.
   **In the same PR, set the voice helper's version to the tag:** the
   `[workspace.package]` `version` in `voice/Cargo.toml` (for `v0.1.0-alpha.19`,
   `0.1.0-alpha.19`). A desktop release build (`CONCH_RELEASE_VERSION`, #1596)
   checks the bundled `conch-voice --version` against the tag and fails on a
   mismatch.
   A release build lists its own tag as a tested server by itself
   (`scripts/desktop-version.sh`, #1596). **After the upgrade, also add the
   new tag to `desktop/build/compat.json`,** the development builds' list, once
   the desktop app has been run against it. Unlisted, a development build
   refuses to sign in to that server with "server version not tested". The
   list sat at alpha.9 until alpha.18 because no step said so.
3. Tag: annotated, on the reviewed `main` commit —
   `git tag -a vX.Y.Z -m "..."` — pushed **by Nick**, or by the session only
   under his explicit, recorded authorization for this release.
4. Verify the `release.yml` run: `make check`, dogfood-check and
   p2-hardening-check re-ran green, binaries built for all three platforms,
   the `desktop-deb` job built the Linux desktop `.deb` (its first step,
   `scripts/desktop-release-guard.sh`, refuses unless the tag is the commit
   built, the tree is clean and `voice/Cargo.toml`'s version is the tag's),
   the `attest` job wrote `checksums.txt` and attested every file, and the
   release was created by `publish` (a draft, or for a pre-release tag a
   published pre-release). If any of the first three jobs fails, no release
   exists: fix on `main` and tag a new version, never move the tag. Never re-run a
   release (the run or a job of it): tag a new version. `attest` asserts the
   exact file set and `publish` verifies every attestation before it creates
   the release.
5. Sanity-check the artifacts (download one, `--version`, run against a temp
   db), note the dogfood-check run in the release notes, hand the draft to
   Nick to publish (a pre-release is already published: check its notes and tester checklist).
6. Verify the desktop `.deb` the way a tester does, from a directory holding
   the release's files:
   `sha256sum -c --ignore-missing checksums.txt` (the one `checksums.txt`
   covers every file), then `gh attestation verify conch-desktop_*_amd64.deb
   --repo njdaniel/conch --signer-workflow
   njdaniel/conch/.github/workflows/release.yml --source-ref
   refs/tags/<tag>`. With the two pinning flags it checks that this
   repository's `release.yml`, run for that tag, signed the file; `--repo`
   alone accepts an attestation from any workflow on any ref. `dpkg-deb -I` shows the package's Version (the tag with the
   first `-` as `~`). The `.deb` is a **technical preview** until real-device
   acceptance is recorded (#1603), and the release notes say so. **A green
   CI or release run, a CI artifact, a checksum or an attestation says the
   package was built from this tag by this workflow; it does not say the app
   works, and it is not approval or real-device acceptance.** Only the
   acceptance record (#1603) is that.

## Desktop release notes section

When the release ships the Linux desktop `.deb`, the CHANGELOG entry gets a
"Linux desktop app" section after the server notes. Fill it from recorded runs
only (the capability report and #1603's acceptance record); a row nobody has
run is "not tried", never "works". Link the user page,
`docs/desktop/linux.md`.

```markdown
### Linux desktop app
- **Verified on:** <distribution and version, desktop and compositor, session
  type, architecture, with the run that shows it (issue or record)>.
- **Experimental:** <what runs but has no recorded acceptance>.
- **Not supported:** <X11 screen share, ARM64, AppImage, Flatpak, RPM, and
  anything else that does not work>.
- **Not tried:** <rows with no run yet>.
- **Known issues:** <issue links>.
- Verify the download with `docs/desktop/linux.md` (checksums, then
  `gh attestation verify` for tag <tag>).
```

## Never

- Tag on a failing or stale dogfood-check or p2-hardening-check.
- Tag without recorded sign-off, or move/delete a pushed tag, or re-run a
  release: tag a new version.
- Tag a commit that is not on `main`: the guard refuses it, but that is only
  accident protection. The real control is a `v*` tag ruleset on the
  repository (Nick's setting).
- Edit a published release's artifacts — regressions get a new patch release.
