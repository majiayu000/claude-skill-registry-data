---
name: hikyo-contributor-bootstrap
description: Bootstrap a Hikyo contributor checkout from Git identity and commit signing through pinned dependencies, scoped tests, pull-request readiness, and an optional local playground. Use for first-time contributor setup or repairing an incomplete local environment, rather than production deployment.
---

# Hikyo contributor bootstrap

Produce a working contributor environment, with evidence for each completed
stage. Default to local setup and validation. Perform the authorized local work;
push, PR creation, merge, release, and deployment
require their own existing authorization.

## Establish the checkout

Find the selected repository with `git rev-parse --show-toplevel`; verify its
remote and the Hikyo Go module rather than using a saved absolute path. The
canonical repository is `https://github.com/Hikyo-Org/Hikyo`. For a fresh clone,
choose the user's destination and fork/canonical topology before creating it.
For an existing checkout, preserve dirty work and do not reset it or silently
switch its remote. Work in the requested branch or an isolated feature worktree.

Read that checkout's `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, and the nearest
rules for the contribution scope. Determine whether the user needs the full app,
Go/CLI only, frontend/prototype, generated client, or documentation site. Full
app build and validation are the default when no narrower target is given. Do
not confuse contributing to Hikyo with fetching an unrelated application's
production secrets from Hikyo.

## Offer a local playground

Early in bootstrap, ask once: "Would you also like a local Hikyo instance to
play around with?" Offer **Docker**, **source-built**, and **setup/tests only**.
Explain that Docker isolates the runtime but requires a working local daemon
and supported container configuration; source-built uses the contributor's
checkout directly; setup/tests only leaves no persistent instance running.
Recommend Docker when an existing local daemon and a supported lightweight
setup are available, otherwise source-built. Preserve an earlier explicit
answer or already-authorized instance request instead of asking again.

Use an asynchronous question when available and continue independent signing,
dependencies, build, and test work while awaiting the choice. Do not launch a
persistent playground until the user selects it; an unanswered question remains
pending. A declined playground does not prevent contributor setup completion.
Test suites may still create and tear down their own disposable test instances.

For Docker, read [docker-playground.md](references/docker-playground.md).
For source-built, use the runtime/admin sections of the local-development
reference. Keep the instance available for the requested experimentation window
and provide its URL, data location, and exact scoped stop/restart commands.

## Follow the setup stages

1. **Git identity, signing, and fork access:** read
   [signing-and-git.md](references/signing-and-git.md). Preserve a working
   signing configuration. Keep both DCO and cryptographic signing. Request only
   missing identity or human key-registration/unlock steps, while continuing
   independent local preparation.
2. **Toolchain, dependencies, and development app:** read
   [local-development.md](references/local-development.md). Derive versions
   from the checkout, use its separate lockfiles, and verify the build. Start
   and verify a persistent app only when selected or already requested.
   Do not weaken the loopback restriction to make a preview reachable.
3. **Tests and contribution delivery:** read
   [validation-and-pr.md](references/validation-and-pr.md). Select checks by
   changed scope; explain what preflight omits. Continue through the authorized
   endpoint, retaining explicit human and maintainer gates.

Repository manifests and executable scripts own current commands and pins.
The references explain traps and provide starting commands, not permission to
override newer repository instructions. Inspect a changed script before running
it, especially one installing tools or regenerating source. Bootstrap should
not change lockfiles, generated source, or application code without a diagnosed
need; inspect and report any resulting diff.

## Completion evidence

Report each relevant stage as passed, failed, human action pending, or not
requested, with concise evidence:

- Selected checkout, branch, base, and fork push destination.
- Contributor identity confirmed; signing key configured and registered; hook
  installed; actual contribution commits locally verified and GitHub Verified
  when a push was authorized. Configuration inspection alone is not proof of
  a signed commit. Do not create an empty probe commit merely to test signing.
- Required tool versions selected; scoped frozen-lockfile installs completed.
- Build verified; playground choice recorded. If selected, verify the running
  app with process/container handle, storage location, health result, and URL.
  Record pending first-admin credential establishment and keep the requested
  instance alive. If declined, mark the playground not requested.
- Relevant tests passed, including browser or PostgreSQL behavior when needed;
  skipped checks and external prerequisites stated explicitly.
- Remaining contribution gates, such as fork vouching, review, or exact-head CI.

Do not claim start-to-finish readiness while a required stage is unresolved.
For a fresh checkout with no contribution commits, report signing as configured
but commit verification as pending the first real contribution. Keep private
keys, root keys, administrator authorities, passwords, and database contents out
of chat and tracked files. Cleanup stops only processes and disposable resources
created by this bootstrap; preserve the user's database, keys, and other work.
