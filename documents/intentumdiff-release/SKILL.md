---
name: intentumdiff-release
description: How IntentumDiff ships a release — the release-candidate branch, what PRs target, and how a version reaches PyPI, the VS Code Marketplace and Open VSX. Use this whenever you open a PR, cut or tag a release, decide which branch to base work on, or answer "where does this change go?". Applies to EVERY repo in the estate (intentumdiff-core, -python, -vscode, -ast, -registry, -plugin-sdk and all 69 parser repos). Read it before creating a branch — targeting the wrong base is the most common and most expensive mistake here.
---

# Releasing IntentumDiff

## The rule

**Work is never merged straight to `main`.** Every release gets a **release-candidate
branch**, and PRs target *that*. `main` only moves when the RC is released.

```
feature branch  ──PR──▶  release/v0.0.2-rc  ──PR──▶  main  ──tag──▶  published
```

**The next release is `0.0.2`**, so today's RC branch is:

```
release/v0.0.2-rc
```

## Why

`main` is what gets tagged and published, and publishing is irreversible: **PyPI has no
delete**, a Marketplace version cannot be overwritten, and a burned version number is burned
for everyone. Merging directly to `main` means every merge is a potential release, so the
branch is only ever as good as the last thing pushed to it.

An RC branch makes the release a *decision* rather than a side effect. It also gives a place
to accumulate and verify a set of changes together — which matters here because the estate
is 80 repos with cross-repo dependencies, and a change that is green alone can still break
the combination.

## What to do

**Starting work**

```bash
git fetch origin
git checkout -b feat/my-change origin/release/v0.0.2-rc   # base on the RC, NOT main
```

Basing on `main` when the RC has moved ahead produces a PR carrying every RC commit. That
has happened before and needed a full rescope; `git checkout -B <branch> origin/<base>`
plus a cherry-pick is the recovery.

**Opening the PR**

```bash
gh pr create --base release/v0.0.2-rc --head feat/my-change
```

Branch protection requires a PR and passing checks; approvals are set to **0** because this
is a solo-maintainer estate, so a review requirement above zero would make every merge
impossible.

**Cutting the release**

1. RC is green and complete → PR `release/v0.0.2-rc` → `main`
2. Verify `main` is green **before** tagging — this is the step that has caught every real
   release bug so far
3. Tag from `main`; the tag triggers publication
4. Open the next RC branch immediately, so in-flight work has a base

## Definition of ready to release

**Nothing is published until every box below is ticked.** Not "mostly", not "the important
ones" — all of them. This list exists because 0.0.1 was published with green CI and had to
be pulled from three registries within a day.

If a box cannot be ticked, the release does not happen. The correct response to schedule
pressure is a later release, never a lower bar.

### Artefact

- [ ] `smoke_published_wheel.py` passes against a **locally built** artefact
- [ ] Every check inside it passes — install, import, console script, `python -m`, a real
      diff, **clean stderr**, **all URLs resolve**
- [ ] The extension VSIX installs into a **clean VS Code profile** and works there
- [ ] Extension host log is clean — no errors, no warnings about missing files
- [ ] Tested on every platform the artefact claims to support

### Docs

- [ ] Documentation site is **live**, not planned
- [ ] **Every** example in **every** README has been extracted and run verbatim, and its
      real output matches what the doc claims
- [ ] **Every** link in user-facing docs resolves — READMEs, error messages, `--help`,
      the Marketplace listing
- [ ] No reference to a page, domain or command that does not exist
- [ ] Demo media shows the CURRENT build, not an older UI

### Correctness

- [ ] Full test suite green in every affected repo, run in **that** repo
- [ ] The headline claim demonstrably works on a real repository — not a fixture
- [ ] Known limitations are written down and honest. A missing capability documented is
      fine; one implied to work is not
- [ ] No regression against the previous release on a real-world diff

### Release hygiene

- [ ] Version is a **prerelease** unless the artefact has been used in anger
- [ ] Tag matches the manifest exactly
- [ ] CHANGELOG says what changed, in the user's terms
- [ ] Prior broken versions yanked or unpublished
- [ ] A rollback plan exists — and note that for PyPI and the marketplaces, "rollback"
      means yank plus a new version, never delete

### The rule behind the list

**Green CI is not evidence a product works.** It is evidence the code compiles and the
tests we thought to write pass. Every 0.0.1 defect passed CI and was obvious thirty seconds
after installing the package.

Before publishing, someone must install the artefact and use it the way the README says to.
Every time. No exceptions, however small the change looks.

## MANDATORY: smoke-test the artefact before any publish

**CI proves the code builds. It does not prove the artefact works.** These are different
claims, and only the second one matters to a user.

IntentumDiff **0.0.1 shipped broken and had to be pulled from PyPI and both extension
marketplaces**, despite every check being green. Four defects, all invisible to CI and all
obvious within thirty seconds of installing the published package:

| Defect | Why CI could not see it |
|---|---|
| ~69 "Failed to catalog parser plugin" errors on every run | the distribution name was missing from the package's own first-party trust list; in a source checkout the distribution resolves differently and the check passes |
| `python -m intentumdiff` failed | no `__main__.py`; nothing in CI invoked it |
| Error message linked to an unregistered domain | no test followed a documented URL |
| README's headline example raised `NameError` | it was a fragment; nothing ever ran it |

None of these is exotic. All four were found by installing the wheel and typing what the
README says to type.

### The gate

Before tagging **any** release:

```bash
python scripts/smoke_published_wheel.py --wheel dist/<built>.whl   # pre-publish
python scripts/smoke_published_wheel.py                            # post-publish
```

It installs into a clean venv and checks what a user does in their first five minutes:
install, import, console script, `python -m`, a real diff, **clean stderr**, and that
**every URL in the output resolves**.

Two of those deserve emphasis, because exit codes hide both:

- **Clean stderr.** 0.0.1 returned correct results *and* printed 69 errors. Exit code 0.
- **Live URLs.** A link in an error message is a promise; a dead one is worse than none.

### Beyond the script

The script is the floor, not the ceiling. Also required before a release:

- **Run every example in every README verbatim.** Extract the code block, execute it,
  compare against the documented output. A fragment that cannot run is a broken example.
- **Follow every link in user-facing docs.** Dead links are how docs rot silently.
- **Exercise the extension in a vanilla VS Code**, not a dev host — a clean profile, no
  workspace settings, no other extensions.
- **Confirm the claimed feature actually works.** Not "the code path is covered" — install
  it and watch it do the thing.

## Ship beta first

The first release of anything user-facing is a **prerelease**: `0.0.2b1`, `0.0.2-beta.1`.

A version without a beta marker is a claim of stability. Make that claim after the artefact
has been installed and used, never before — the cost of retracting it is far higher than
the cost of a `b1` suffix. PyPI cannot delete a version and a Marketplace listing cannot be
overwritten, so "we can fix it in the next one" is not a recovery plan.

Promote to a stable version only once the beta has been smoke-tested and actually used.

## Version rules

- The tag **must** match the version in the manifest — `pyproject.toml`, `package.json`,
  `Cargo.toml`. Workflows assert this and fail closed, deliberately: a mismatch means the
  published artefact and the git history disagree about what shipped.
- **Derive the expected version from the tag**, never a literal. A hardcoded version goes
  stale silently and fails at the very end of a release, after every platform wheel has been
  built, blaming the artefact when the gate was wrong.
- A published version is never reused. If a release fails after publishing, the next attempt
  is a new version.

## Cross-repo releases

Repos depend on each other by **git tag**, not branch — `intentumdiff-plugin-sdk`,
`intentumdiff-ast`. A tag is immutable, so it keeps the vocabulary and ABI stable underneath
consumers.

The consequence, learned the hard way: **a rename or breaking change needs a NEW tag, and
every consumer re-pinned.** After the IntentumDiff rebrand the components still pinned SDK
`v0.1.0`, where the package was named `intentdiff-plugin-sdk`, so the build failed with
"no matching package named `intentumdiff-plugin-sdk`". The dependency key was renamed; the
pinned tag was not.

Order for a coordinated release:

1. Release the **leaf** first (`intentumdiff-ast`, `intentumdiff-plugin-sdk`)
2. Re-pin consumers to the new tag
3. Release the consumers

## What NOT to do

- **Do not merge to `main` directly.** Even as an admin — protection allows it, which is
  precisely why the discipline has to be deliberate.
- **Do not tag before CI on `main` is green.** Publishing is irreversible; a red suite is
  free to fix beforehand and impossible to fix afterwards.
- **Do not change the WIT package namespace** to match a rename. It is a wire contract, not
  a brand: all 69 certified components are pinned against `intentdiff:plugin@1.0.0`, and
  renaming it breaks every one of them.
- **Do not re-pin the registry casually.** Its checksums certify specific component builds.
  Re-pinning is a deliberate release task with its own verification, never a side effect.
