---
name: rust-release-workflow
description: Prepare and cut an IronCrew release through develop and main, including PR review, complete validation, versioning, tagging, and workflow monitoring. Use only with explicit release intent.
---

# IronCrew release workflow

Use explicit user approval before merges, remote PR changes, commits, pushes,
version changes, tags, releases, images, or crates.io publication. Never
force-push, rewrite published history, or delete a remote tag.

## Branch model

- `develop` is the integration branch.
- `main` is the release branch.
- The flow is `develop` to a reviewed `main` PR, then an annotated tag on the
  verified `main` commit. Tags use the stable `vX.Y.Z` form. A versioned
  `repository_dispatch` selects the release workflow from default-branch
  `main`; the workflow separately checks direct annotation-to-commit type,
  manifest version, and reachability from `main`.

Default-branch dispatch selection and the checked-in guard are defense in depth,
not the complete platform boundary. Require reviewed default-branch controls
and a protected `release` environment before treating publication as
platform-enforced.

IronCrew uses an explicit sole-owner authority model: `skitsanos` is the trusted
root and may approve `develop` to `main`, create the stable tag, request and
self-approve a protected deployment, and rerun it. A malicious or compromised
owner is outside the claimed boundary. Do not dispatch either workflow until
`main` requires a PR and green CI, the protected `release` environment requires
deliberate owner self-approval with administrator bypass disabled, Docker
credentials have moved from repository secrets into that environment, only the
owner may create `v*` tags, tag update/deletion remains prohibited, immutable
releases are enabled, and the non-secret controls have been revalidated. Use
only the owner-authored Issues request controller, which exchanges a bounded
request for a fixed dispatch using its run-scoped `GITHUB_TOKEN`; do not use a
standing Contents-write personal token.

Default-branch dispatch does not stop a tag-capable actor from introducing a
different tag-push workflow. Under the sole-owner model, only the trusted owner
may create `v*` tags and owner compromise is out of scope. Record the workflow-
execution-policy state, but do not enable a broad preview policy that breaks
CI's intentional `push` and `pull_request` coverage or the Issues controller
without a separately validated policy design.

## Prepare

1. Require a clean worktree. Record branch, manifest/lock versions, latest tag,
   and divergence from `origin/develop` and `origin/main`.
2. List open pull requests targeting `develop`; summarize mergeability, review,
   and CI. Ask before merging, closing, or otherwise mutating them.
3. Review dependency drift and `cargo audit --deny warnings`. Ask before incompatible upgrades
   or audit-policy changes.
4. Run the complete `/check` gate, including required PostgreSQL and replica
   evidence. Do not proceed on a skipped required test. Treat unavailable
   platform runners as CI evidence, not as locally executed checks.
5. Read commits and resolved `IC-NNN` records since the latest tag. Propose a
   SemVer bump and release notes from actual behavior, then wait for approval.

## Release

After approval:

1. Update `Cargo.toml`, refresh the root package version in `Cargo.lock`, and
   read both back.
2. Rerun the complete gate. Stage only explicit release files; commit and push
   `develop` only when authorized.
3. Open or update the `develop` to `main` release PR. Wait for green CI and
   approval; merge only with user authorization.
4. Fast-forward local `main`, create an annotated `vX.Y.Z` on the verified
   release commit, prove it is reachable from `main`, and prove its manifest
   version matches.
5. Show the evidence and ask before pushing the tag. Pushing the tag does not
   publish a release. Once the remote controls above exist, separately ask to
   exercise the protected environment without publication. Replace the tag in
   this exact request with the pushed stable tag:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"release","tag":"vX.Y.Z","mode":"validate"}')
   gh issue edit "$request" --add-label release-request
   ```

   Confirm deliberate owner approval and a successful read-only run with no
   OIDC, release, Docker-secret, or registry operation, then close the request
   issue. Capture a separately designed
   denied adversarial canary; `repository_dispatch` always selects the default-
   branch workflow and cannot be pointed at an off-main ref.
6. Only after those canaries and separate explicit publication approval, use:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"release","tag":"vX.Y.Z","mode":"publish"}')
   gh issue edit "$request" --add-label release-request
   ```

   A release created with the workflow's `GITHUB_TOKEN` does not cascade into
   another release-event workflow; image promotion remains separate.
   Monitor `release.yml`. Its read-only image job must build the signed multi-
   platform OCI archive and strict receipt from the exact tag commit. The final
   protected job must verify those immutable artifacts, sign them, and create
   the release once without updating existing release assets.
7. Image promotion through `.github/workflows/docker-publish.yml` requires
   separate authorization. After the protected environment exists, its non-
   publishing path can be checked with:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"docker","tag":"vX.Y.Z","mode":"validate"}')
   gh issue edit "$request" --add-label release-request
   ```

   Before actual promotion, require the exact Docker Hub stable-semver
   immutability rule and IC-015's recorded non-production replay/conflict/
   concurrent-`latest` acceptance. IC-015 is resolved, but Docker publication
   remains deferred until this IC-014 control plane is complete and the user
   separately authorizes production promotion. Then use:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"docker","tag":"vX.Y.Z","mode":"publish"}')
   gh issue edit "$request" --add-label release-request
   ```

   It verifies and promotes tag-owned assets instead of rebuilding source.
   Monitor the version digest and final `latest` digest against GitHub's current
   stable release. Publish crates only with separate authorization too.
   Do not backfill a legacy release that lacks the signed OCI archive and
   receipt; promotion begins with the first release produced by the trusted
   default-branch workflow.

If an unpushed local step is wrong, make a corrective edit or ask for direction.
After a push, prefer a forward fix. Do not use destructive reset or broad
implicit staging as release recovery.
