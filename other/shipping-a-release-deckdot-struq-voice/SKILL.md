---
name: shipping-a-release
description: "Cut, sign, verify, publish and push a Struq Voice release with one command. INVOKE BEFORE TOUCHING package.json's version: any request to 'bump the version', 'bump to x.y.z', 'set the version', or to run release:cut by hand must come here first, because hand-bumping corrupts the pipeline's input and silently skips a version. Also use for 'ship it', 'ship a release', 'release this', 'cut a release', 'publish an update', 'push a new version', after merging a PR that should reach users, and when diagnosing 'the update never arrives', 'no update notification', 'still on the old version', or a feed serving a stale latest.yml. Knows the one command, what it decides on its own (version bump, release notes), the flags, how to confirm the feed actually moved, and how to recover from a failure at each stage without shipping the wrong number. NOT for building an unsigned local installer (pnpm dist) or for the gates alone (use verification-gates)."
argument-hint: "[--dry-run | --bump patch|minor|major|x.y.z | --skip-gates]"
---

# Shipping a Struq Voice release

## The command

```bash
pnpm release:auto
```

That is the whole thing. It goes from whatever state the working tree is in to
a signed release live on the feed and the tag pushed. **Do not run the
individual steps** (`release:cut`, `ship`, `release:publish`) unless recovering
from a specific failure, see the table at the bottom.

Run it from the repo root, on `main`.

## Never bump the version by hand

`release:auto` computes the next version from `package.json` plus the commits
since the last `v*` tag. Bumping `package.json` yourself, or calling
`scripts/release-cut.mjs` directly, corrupts that input: the pipeline then
bumps again from your already-bumped number and **skips a version entirely**
(0.1.2 hand-bumped to 0.2.0 ships as 0.3.0, and 0.2.0 never exists).

If it has already happened, revert the stray bump commit and let the pipeline
own the number:

```bash
git revert --no-edit <the chore: release commit>
pnpm release:dry     # confirm it now targets the version you expect
```

The same applies to tags. Do not create a `vX.Y.Z` tag by hand, because the
pipeline reads the last release tag to decide the commit range.

## A merged PR is not a release

Merging to `main` changes source only. Until `release:auto` runs, no tag
exists, no GitHub release exists, and `releases/latest/download/latest.yml`
still serves the previous version. Installed copies check that feed, see their
own version, and correctly report no update. **"The update never arrives" is
almost always this**, not a bug in the updater.

Confirm what the feed actually serves before debugging anything in
`src/main/updater.ts`:

```bash
curl -sL https://github.com/Deckdot/struq-voice/releases/latest/download/latest.yml
```

If that reports the version the user is already running, there is nothing to
fix in the app. Ship a release.

## What it decides, so nobody has to

| Decision | How |
|---|---|
| version bump | Conventional Commits since the last `v*` tag: a breaking change gives major, any `feat:` gives minor, otherwise patch |
| release notes | the same commits, grouped into Breaking / New / Fixed / Other |
| dirty tree | committed as `chore: pre-release working tree` before the cut |
| is it safe | typecheck, lint and unit tests run **before** the version is cut |

The bump rule lives in `src/shared/release-plan.ts` and is unit tested. It is
not duplicated in the script.

## The order, and why it is that order

```
preflight -> read commits -> commit tree -> plan -> GATES -> cut -> build
          -> sign -> verify -> push -> publish -> read back
```

Gates run **before** the cut because the cut is a commit plus a tag. Everything
before it is reversible; everything after it is verified. The irreversible step
sits between a passing suite and a verifier that refuses to publish what it
cannot check.

The push sits **before** the publish, and must stay there: `gh release create`
refuses a tag that exists only locally ("tag vX.Y.Z exists locally but has not
been pushed"). Publishing first deadlocks the pipeline on its own last step.
This does not weaken the safety property, because the push still happens after
build, sign and verify. A pushed tag with no release attached is harmless: the
feed keeps serving the previous version until the upload lands.

Preflight fails early on: not a git repo, wrong branch, no `gh`, `gh` not
authenticated, missing signing key. Each of those would otherwise be discovered
*after* a 116MB build.

## Flags

| Flag | When |
|---|---|
| `--dry-run` | rehearse: really builds, signs and verifies, but never commits, tags, uploads or pushes |
| `--bump minor` | override the inferred bump. Also takes an explicit `1.2.3` |
| `--skip-gates` | retry after a failed upload, when the gates already passed minutes ago |
| `--no-commit` | refuse on a dirty tree instead of committing it |
| `--yes` | allow a branch other than `main` |

`pnpm release:dry` is `release:auto --dry-run`.

## Refusals, and what they mean

**"nothing user-facing has changed"** means every commit since the last tag is
`docs:`, `chore:`, `test:`, `style:`, `ci:`, `build:` or `refactor:`. Shipping
would burn a version number on a release whose notes are empty. Override with
`--bump patch` if that is genuinely wanted.

**"on branch X, not main"** means the tag would point at a commit main does not
contain, so the tag and the shipped history would disagree.

**"no signing key"** means the private half is missing. Every installed copy
verifies against the public key it shipped with, so an unsigned release is one
no machine will accept. Restore from backup or set `STRUQ_VOICE_RELEASE_KEY`.

## Recovering from a failure

The script says which stage failed and what to run. In summary:

| Failed at | State | Recovery |
|---|---|---|
| preflight or gates | nothing changed | fix and re-run `pnpm release:auto` |
| gates, after auto-commit | tree committed, not cut | fix, re-run. Or `git reset --soft HEAD~1` to get the changes back |
| build / sign / verify | cut and tagged locally, nothing pushed or published | fix, then `pnpm ship` to retry from the existing tag. Or undo: `git tag -d vX.Y.Z && git reset --hard HEAD~1` |
| push | built and verified, tag still local, **nothing published** | `git push origin main && git push origin vX.Y.Z`, then `pnpm release:publish` |
| publish | built, verified and pushed, feed still on the old version | `pnpm release:publish` alone |

Never re-run `release:auto` to recover from a failure at the push or publish
stage. The version is already cut, so a second run bumps again and ships the
wrong number. Resume with the single command in the table.

The reassuring property: a failure at push or publish leaves the feed serving
the **previous** version. No installed copy sees a partial or unverifiable
update, so there is no rush and no user-visible damage.

## After shipping, confirm the feed actually moved

`release:auto` reads the manifest back, but confirm the feed independently.
This is the check that catches a release which was cut and tagged but never
uploaded:

```bash
curl -sL https://github.com/Deckdot/struq-voice/releases/latest/download/latest.yml | head -3
curl -sL https://github.com/Deckdot/struq-voice/releases/latest/download/struq-voice-release.json
```

Both must report the version just shipped. Four assets belong on the release:
`latest.yml`, the setup `.exe`, its `.blockmap`, and
`struq-voice-release.json`.

**If `struq-voice-release.json` is missing, every installed copy will download
the update and then refuse it** at the signature gate with "manifest fetch
returned 404". That looks identical to a broken updater and is not.

## Verifying the gate is real

```bash
pnpm release:dry     # build, sign, verify, no side effects
```

To prove the refusal path, flip a byte in the built installer and run
`node scripts/verify-release.mjs`: it must FAIL on hash and signature and exit
1. `src/main/updater.test.ts` covers the in-app refusals (swapped artifact,
downgrade replay, wrong key, tampered signature, unreachable manifest).

## Notes

- The build goes to `%TEMP%/struq-voice-release`, not `release/`. Under
  `Documents` electron-builder's `win-unpacked.tmp` rename hits EPERM.
- The signed message is `<sha512>|<version>`. The version is bound in so a
  genuinely signed older build cannot be replayed as an update.
- Full background in `docs/RELEASING.md`.
