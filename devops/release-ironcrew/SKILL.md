---
name: release-ironcrew
description: Prepare, verify, version, and publish an IronCrew release through develop and main with explicit approval gates. Use when the user asks to release, cut a release, ship a version, bump the product version for release, or integrate dependency work into a release. Do not use for routine dependency updates, PR review alone, or deployment without release intent.
---

# Release IronCrew

Use explicit user approval before merges, remote PR changes, commits, pushes,
version changes, tags, releases, images, or crates.io publication. Never
force-push, rewrite a published commit, or delete a remote tag.

## Establish release state

1. Require a clean worktree. Record the current branch, `Cargo.toml` and
   `Cargo.lock` versions, latest `v*` tag, and divergence from remote
   `develop` and `main`.
2. Confirm the repository still integrates on `develop` and releases from
   `main`. A release tag must be an annotated stable `vX.Y.Z` tag whose commit
   is reachable from `main`.
3. Stop if unrelated changes would enter the release or version/tag history is
   inconsistent. Do not repair history destructively.
4. List open pull requests targeting `develop` and summarize mergeability,
   review state, and CI. Ask before changing remote state.

Release and Docker publication are admitted through versioned
`repository_dispatch` events so GitHub selects the workflow from the default
branch rather than from a tag commit or caller-selected workflow ref. That
selection is still only repository-level defense in depth. Require reviewed
default-branch controls and a protected `release` environment before treating
publication as platform-enforced.

IronCrew currently uses an explicit sole-owner authority model: `skitsanos` is
the trusted root and may approve `develop` to `main`, create a stable release
tag, request a release, approve the protected deployment, and rerun it. A
malicious or compromised repository owner is outside this model. Do not dispatch
either workflow until `main` requires a PR and green CI, the protected `release`
environment requires deliberate owner self-approval with administrator bypass
disabled, Docker credentials have moved from repository secrets into that
environment, only the owner may create protected `v*` tags, tag updates and
deletions remain prohibited, immutable releases are enabled, and the documented
non-secret controls have been revalidated.

The owner-only Issues controller is the request channel. It validates an exact
issue and uses its run-scoped `GITHUB_TOKEN` to create the fixed repository
dispatch, avoiding a standing Contents-write personal token. `validate` mode is
non-publishing, but it still waits for the protected environment because its
purpose is to prove that enforcement.

Default-branch dispatch does not prevent a tag-capable actor from adding a
different tag-push workflow to an off-main commit. Under the sole-owner model,
only the trusted owner may create `v*` tags and owner compromise is out of
scope. Record the workflow-execution-policy state, but do not enable a broad
event restriction that breaks CI's intentional `push` and `pull_request`
coverage or the Issues request controller without a separately validated
policy design.

## Verify and propose

1. Prove Cargo freshness with `cargo outdated --root-deps-only`,
   `cargo upgrade --dry-run --incompatible`, and `cargo update --dry-run
   --verbose`, then run `cargo audit --deny warnings`. Every direct dependency
   must be current before release. A lower transitive version is acceptable only
   when the current direct dependency graph pins it exactly; record the upstream
   constraint and never force an incoherent lockfile. Ask before incompatible
   major upgrades or audit-policy changes.
2. Open the official MCP specification index and verify the newest published
   revision. IronCrew supports only that revision: its strict discovery pin,
   transports, tests, examples, and docs must move together, with no fallback to
   the superseded protocol.
3. Use `$check-ironcrew` to run the complete locally reproducible repository,
   Rust, Lua, evaluation, PostgreSQL, replica, and release-build gates. Required
   live tests may not be skipped. Platform-only jobs remain a later CI gate.
4. Read commits and resolved `IC-NNN` entries since the latest tag. Propose a
   Semantic Versioning bump from behavior, not commit-message prefixes alone.
5. Draft release notes grouped by area and referencing relevant issue IDs.
   Wait for the user's version approval.

## Cut the release

After approval:

1. On `develop`, update the package version in `Cargo.toml`, refresh the exact
   root package entry in `Cargo.lock`, and read both back.
2. Rerun the complete gate. Stage only explicit release paths and commit/push
   only when authorized.
3. Open or update the `develop` to `main` release PR. Wait for green CI, then
   merge only with explicit sole-owner authorization.
4. Fast-forward local `main` from `origin/main`. Create an annotated `vX.Y.Z`
   tag only on the verified release commit.
5. Prove the tag is reachable from `main` and its `Cargo.toml` contains the same
   version. Show the evidence and ask before pushing the tag.
6. Push the tag only with explicit approval. Pushing it does not publish a
   release. After the remote controls above exist, first ask for authorization
   to exercise the protected environment without publication. Replace the tag
   in this exact request with the pushed stable tag:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"release","tag":"vX.Y.Z","mode":"validate"}')
   gh issue edit "$request" --add-label release-request
   ```

   The issue must be open, owner-authored, have the exact title and only the
   `release-request` label, and contain the canonical single-line JSON body
   shown above. Confirm that the protected `release` environment required
   deliberate owner approval and that the
   run completed without contents-write, OIDC signing, a GitHub release, or
   registry access. Close the request issue after the downstream run completes.
   Capture a separately designed denied adversarial canary; the controller's
   `repository_dispatch` always selects the default-branch workflow and cannot
   be pointed at an off-main ref.
7. Only after those canaries and a separate explicit publication approval,
   dispatch the exact release request:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"release","tag":"vX.Y.Z","mode":"publish"}')
   gh issue edit "$request" --add-label release-request
   ```

   A release created with the workflow's `GITHUB_TOKEN` does not cascade into
   another release-event workflow; Docker promotion remains the separately
   authorized dispatch below.
   Monitor `.github/workflows/release.yml`. It must create the release once and
   publish the signed OCI archive plus strict image receipt; it must not update
   an existing release or replace its assets.
8. Docker publication through `.github/workflows/docker-publish.yml` is a
   separate authorization. It verifies and promotes the tag-owned signed
   archive rather than rebuilding source. Before any Docker
   publication, require the exact Docker Hub stable-semver immutability rule and
   IC-015's recorded non-production replay/conflict/concurrent-`latest`
   acceptance. After the protected environment exists, its non-publishing
   Docker path can be checked with a separate authorization and this exact
   request; it must not read Docker credentials or touch the registry:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"docker","tag":"vX.Y.Z","mode":"validate"}')
   gh issue edit "$request" --add-label release-request
   ```

   IC-015's non-production registry acceptance is resolved, but actual Docker
   publication remains deferred until this IC-014 control plane is complete and
   the user separately authorizes production promotion. Then use this exact
   request:

   ```bash
   request=$(gh issue create --repo skitsanos/ironcrew \
     --title 'IronCrew release request' \
     --body '{"target":"docker","tag":"vX.Y.Z","mode":"publish"}')
   gh issue edit "$request" --add-label release-request
   ```

   Monitor the version digest and final `latest` digest against GitHub's current
   stable release. Publish a crate only with separate authorization too.
   Do not use this path to backfill a legacy release without the signed OCI
   archive and receipt; promotion begins with the first release produced by the
   trusted default-branch release workflow.

If an unpushed local release step is wrong, make a corrective edit or ask for
direction. Once anything is pushed, use a forward fix unless the user explicitly
authorizes another safe recovery.
