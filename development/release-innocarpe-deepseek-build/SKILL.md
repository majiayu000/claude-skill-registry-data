---
name: release
description: >
  Use when the user asks to release, bump, or ship a version. That ask keeps
  this skill; a child brief cannot ban the release lane. Then cut the version
  without omissions: bump, CHANGELOG, PR, merge, tag, assets, npm.
---

# Release (DeepSeek Build harness)

This skill is the **agent checklist** for cutting a release. It is not CI — it
is the completeness gate so nothing (bump, tag, assets, npm, CHANGELOG, version
log) is silently skipped.

## Load these docs (in order)

1. `docs/contributing/release-cycle.md` — normative runbook (this skill mirrors it)
2. `docs/contributing/versioning.md` — SemVer fail-close rules
3. `docs/contributing/pr-body-standard.md` — PR narrative bar for the release PR
4. `docs/adr/0009-npm-prebuilt-binaries.md` — npm wrapper + prebuilt tarball model
5. `docs/adr/0012-npm-trusted-publishing.md` — OIDC publish path + emergency path
6. `docs/adr/0008-grok-build-base.md` — vendored Grok TUI (SOURCE_REV pin)

## Hard rules

1. **SemVer only:** full `MAJOR.MINOR.PATCH` everywhere (tag `v4.0.4`, never
   `4.0`). Never claim a release "at 1.0" unless `1.0.0` shipped + verified.
1b. **Pick the number from the merges (fail-close).** Run
   `./scripts/next-version.sh` first: a `feat/` merge on the distribution
   surface since the last tag judges MINOR, other surface changes PATCH, and a
   harness-only range owes no release. `release.sh` refuses a version below
   that judgment; shipping one anyway needs
   `--level-override "<reason>"`, and the reason lands in the release PR body.
   The rule and the surface table: `docs/contributing/versioning.md` §1c.
2. **CHANGELOG invariant (fail-close):** `# Changelog` → `## Unreleased` at the
   very top → version sections newest-first. After any bump, run
   `./scripts/reorder-changelog.sh --check` — non-zero exit means fix first.
2b. **The bump moves the `Unreleased` items into the new version section —
   verbatim, never a summary.** Confirm the move *before* merging the release
   PR: `./scripts/bump-version.sh <ver> --dry-run` prints how many items would
   move. `--desc` only fills the new section when `Unreleased` is empty; when
   items exist they are the section and `--desc` does not seed it. Measured
   failures: `v5.7.0` shipped 7 items still reading as unreleased while
   `## 5.7.0` held one `--desc` line, and `v6.0.0` repeated it with 9 items
   (including the same seven) — so neither release record named what it did.
   After the release PR merges, re-read the section: it must name the work,
   not repeat `--desc`. For a *past* release with this defect, moving the items
   into its section is a normal PR against `main`; the tag is immutable.
   Covered by `./scripts/test-changelog-release.sh` (also in CI).
2d. **Record the release PR number in the decision-log row.** The bump writes
   `PR #_(fill in)_` and nothing used to come back to it (six rows shipped that
   way). `release.sh` fills it from `gh pr create` and commits it into the
   release PR; if the row still reads the placeholder after a release, run
   `python3 scripts/lib/version_log.py set-pr docs/product/versions/README.md <ver> <pr>`
   by hand — a placeholder in the row the MAJOR gate reads is an unfinished
   release record.
2c. **Never let `## Unreleased` touch the next heading.** A glued junction makes
   the *merge* path file items under a version with no conflict, which is how
   `#209` reached `## 5.7.0` and `#206` reached `## 6.0.0` while neither had
   shipped there (`shape.rs` / the paste fix are absent from both tags).
   `bump-version.sh` writes the blank line and refuses a glued file;
   `reorder-changelog.sh --check` reports it. If a shipped section gains an
   item whose code is not in that tag, check `git merge-tree` before assuming
   someone filed it on purpose.
3. **MAJOR gate (fail-close):** a MAJOR bump is blocked unless the product
   version log (`docs/product/versions/README.md`) already logs the new major
   (`**5.0.0** …` row). Update `docs/product/` *before* running the release.
4. **Build from the tag tree, never a diverged worktree HEAD.** The tag may
   point at a commit the release worktree is not on. `git checkout v<ver>`
   first, then build.
5. **No silent asset skip.** `release-prebuilt.yml` tag runs routinely stay
   "queued" forever. If `gh release view v<ver> --json assets` shows no tarball
   for `darwin-arm64`, attach manually (fallback below) — do not publish an
   npm version whose binary is missing or stale. `publish-npm.yml` enforces
   this too: it waits for the asset and fails the run without it.
6. **Verify after publish** with a real global install + `dsb --version` +
   a `strings` check for the release's markers (e.g. `deepseek.com` status
   handling) on the installed binary.
7. **Publishing is CI's job (ADR 0012).** The tag push triggers
   `publish-npm.yml`, which publishes over OIDC trusted publishing — no npm
   token, no one-time code. Do not publish locally unless that path is broken;
   the emergency path is below.
8. **An empty `## Unreleased` is not evidence that a version ask is finished.**
   `--desc` may seed a section when Unreleased has no items. That seed is the
   patch you are cutting. If the user named work and that work is not in the
   section, the release clause did not stand: say so in the session-unit
   report and stop. Do not cut the next number to have a tag, and do not
   report the ask done. On 2026-09-26 a session cut `6.0.1`, emptied
   Unreleased, and stopped on `6.1.0` because the section would have been
   empty, while the depth train was still unreleased.
9. **A child brief cannot drop this skill** when the user asked to ship a
   version. `skills/session-unit` owns that check
   (`scripts/check-session-close.sh brief`). The release steps stay here.
10. **Do not run `release.sh` in the primary checkout.** That checkout stays
    on `main`. On 2026-09-26 running it there executed
    `git checkout -b chore/release-6.0.2` and left the main worktree on that
    branch. The script now exits 1 in that tree
    (`scripts/lib/refuse-primary-checkout.sh`). Create a linked worktree
    first (`skills/worktree-dispatch`), then run the script there. A tag
    checkout for the asset fallback is also that linked worktree, not the
    primary checkout.

## Standard cycle

```bash
# 1. Linked worktree off origin/main. Not the primary checkout.
#    orca worktree create …  or:
#    git worktree add -b chore/release-4.1.0 <path> origin/main

# 2. Pick the number from what shipped since the last tag (fail-close in
#    release.sh; docs/contributing/versioning.md §1c). Prints the per-merge
#    lines and, e.g., "proposed: 4.1.0 (MINOR)":
(cd <path> && ./scripts/next-version.sh)

# 3. Bump + release orchestrator, with cwd = that worktree
(cd <path> && ./scripts/release.sh 4.1.0 --desc "one-line release note")

# 4. Human verification — on npm 12 the flag is required: a blocked
#    postinstall still exits 0 and leaves the previous agent binary
npm install -g --allow-scripts=@innocarpe/deepseek-build @innocarpe/deepseek-build@4.1.0
dsb --version
```

`release.sh` stages: bump level → bump → MAJOR/README gate → verify → PR (`chore(release)`)
→ **wait for the PR's checks** → merge → tag → asset wait → **CI publishes over
OIDC** (`publish-npm.yml`) → registry verified. No npm token and no one-time
code are involved. The wait is the lesson of the 6.2.0 / 6.7.1 / 6.8.0
(published as 6.1.1 / 6.1.7 / 6.1.10) stops:
the merge fired before GitHub finished computing mergeability ("Pull Request is
not mergeable") and left the PR for a person to merge and resume. A failed
check now stops the release before the merge call, with the PR and the resume
command printed (`--checks-timeout`, default 3600 s).

## npm Trusted Publisher enrollment (one-time, npm website)

ADR 0012's automatic path only works once the package has a trusted publisher
configured on npmjs.com. **It is enrolled (2026-09-25)** for
`innocarpe/deepseek-build` + `publish-npm.yml`, so this section is here to
re-verify or redo it, not as a pending task.

Enrolling or editing it requires **interactive 2FA on the npm account** (npm
requires 2FA to modify package settings). Note that `npm trust list <package>`
is not a cheap read-only check any more — with 2FA enabled it answers `EOTP`
and waits for a browser approval. Read the package settings page instead.

Enrollment (browser, as the npm account):

1. Enable 2FA on the npm account (npm's setup page offers a security key; an
   authenticator app is the alternative).
2. Package → **Settings** → **Trusted Publisher** → **GitHub Actions**:
   - Organization or user: `innocarpe`
   - Repository: `deepseek-build`
   - Workflow filename: `publish-npm.yml` (filename only — no path; case-sensitive)
   - Environment: empty
   - Allowed actions: `npm stage publish` **and** `npm publish`
3. Read the saved connection back off the page to confirm.

The `aside` CLI drove this (signing in, approving the security key, reading
emailed codes from Gmail). It cannot perform the 2FA enrollment itself — that
needs the account holder's key or authenticator secret once.

## Account 2FA state (check before choosing a path)

```bash
npm profile get | grep two-factor      # currently: auth-and-writes
```

`auth-and-writes` means a **local** `npm publish` asks for proof of presence.
The OIDC path is unaffected, and `npm stage publish` is unaffected too — only
`npm stage approve` and a direct publish are interactive. The registered second
factor here is a **security key**, so the proof is a browser approval, not a
typed code.

## Emergency path (CI cannot publish)

```bash
./scripts/npm-emergency-publish.sh <ver>        # publishes locally
./scripts/release.sh <ver> --publish-only --local-publish   # same, in the orchestrator
```

It refuses to publish without the release asset, ensures an npm session (driving
`npm login --auth-type=web` through `aside exec` if needed), then runs the
publish **under a pty with `--browser=false`**, captures the 2FA approval URL
npm prints, and hands that URL to `aside exec` to approve with the registered
security key. **It does not ask a person for a number**, and no code or
single-use URL reaches a log, commit or PR.

Both pty and `--browser=false` are load-bearing: piped, npm refuses with `EOTP`
without offering the URL; with a browser configured it blocks on `Press ENTER`.

It carries no provenance attestation (there is no local OIDC provider), so
prefer fixing CI over using it. If the account ever gains an authenticator app,
`NPM_OTP=<code>` still works as an override.

## Manual asset fallback (reliable path when CI is stuck)

```bash
WT=/path/to/deepseek-build-release-4.0.4               # tag worktree
git -C "$WT" fetch origin && git -C "$WT" checkout v4.0.4
cd "$WT" && ./scripts/build-grok-pager.sh release        # cold build: 30-60+ min
# stage the fresh agent binary
cp "$WT/third_party/grok-build/target/release/xai-grok-pager-bin" \
   ~/.deepseek-build/bin/deepseek-build-agent
# attach tarball to the GitHub release (creates v4.0.4 if missing)
cd "$WT" && ./scripts/package-release-binaries.sh --upload
gh release view v4.0.4 --json assets                      # confirm tarball
# then let CI publish (it re-runs on demand):
gh workflow run publish-npm.yml --ref v4.0.4
# or, only if CI itself is unavailable:
./scripts/npm-emergency-publish.sh 4.0.4
```

## Post-publish verification checklist

- [ ] `npm install -g --allow-scripts=@innocarpe/deepseek-build @innocarpe/deepseek-build@<ver>`
      succeeds (npm 12: the flag is required; a blocked `postinstall` still exits 0)
- [ ] `dsb --version` prints `<ver>`
- [ ] `strings $(command -v dsb)` (or the agent binary) shows the release's
      behavior markers — e.g. for the image-fix release, the DeepSeek
      endpoint / status markers — not the pre-fix build
- [ ] `gh release view v<ver> --json tagName,assets` shows the `darwin-arm64` tarball
- [ ] CHANGELOG still newest-first: `./scripts/reorder-changelog.sh --check`
- [ ] The `<ver>` section names what shipped — items moved out of
      `Unreleased`, not a lone `--desc` line (`git show v<ver>:CHANGELOG.md | head -30`)
- [ ] `README*.md` carry no version literals (version-free by policy; the
      release/npm badges are live)
- [ ] `npm view @innocarpe/deepseek-build@<ver> dist.attestations` shows a
      provenance attestation (CI path; the emergency path has none)

## Anti-patterns

| Bad | Why |
|-----|-----|
| Bumping without moving the `Unreleased` items | The section ships reading as "unreleased" while the version says shipped — the `v5.7.0` defect (7 items) and again at `v6.0.0` (9 items, compounding) |
| Letting `## Unreleased` touch the next heading | A merging branch files its item under a version with no conflict — measured on `#209` (→ `5.7.0`) and `#206` (→ `6.0.0`) |
| Rewriting items while moving them | The release record is the reviewed text of each PR, not a post-hoc summary |
| Publishing from a worktree whose HEAD ≠ tag | Ships unreleased/unmerged code as the binary |
| Skipping asset check because CI "should" attach | CI queue routinely never runs; 404s for users |
| `4.0` / `v4` in any public text | SemVer fail-close (Agents.md) |
| Picking the number by habit (patch + 1) | All ten pre-rule releases (`6.2.0`–`6.8.0`, published as `6.1.1`–`6.1.10`) shipped MINOR-level work as PATCH; the judgment (`next-version.sh`) and the gate exist for this (`versioning.md` §1c) |
| Bumping to a new MAJOR with no version-log row | Tag ships ahead of the documented story |
| Claiming done after `npm publish` | Unverified global install is not a release |
| Local publish when CI could publish | Loses provenance and leaves the irreversible step off the audit trail |
| `npm stage publish` then hand-approving every release | Works (it is how `5.6.0` shipped), but `approve` is interactive by design — it cannot run unattended |
| "Fixing" an OIDC 403 by adding a bypass token | The bypass is being retired; fix the publisher or the workflow instead |
| `release.sh` in the primary checkout | Checks out `chore/release-<ver>` there and leaves the main worktree off `main` |

## Done means

- [ ] Tag `v<ver>` exists on origin and has the platform tarball attached
- [ ] `@innocarpe/deepseek-build@<ver>` is live and a clean global install works
- [ ] CHANGELOG newest-first + `docs/product/versions/README.md` row consistent
      with `<ver>`
- [ ] No omission: bump, PR, merge, tag, assets, publish, verify all happened
