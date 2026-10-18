---
name: release-aid
description: >
  Cut a release of THIS repo (the AID methodology repo) end-to-end: bump the version, update
  the release notes, gate, tag, publish to every channel, and verify all checks green. One
  level argument decides the bump: major | minor | patch | beta. Maintainer-only ops tooling —
  NOT an AID methodology skill, never rendered to profiles/, never shipped to adopters.
  Sequence: RESOLVE -> PRECHECK -> BUMP -> DOCS+NOTES -> PR(merge=human) -> DRY-RUN -> TAG -> VERIFY -> CONFIRM -> close-out.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
argument-hint: "<level>  REQUIRED: major | minor | patch | beta  (bump that level, zero the levels below)"
---

# Release AID

> **Maintainer-only skill — outside `canonical/`.** Like `generate-profile`, this lives only
> at `.claude/skills/release-aid/` — it is NOT in `canonical/skills/`, is NOT rendered to
> `profiles/`, and is NEVER shipped to adopters. It operates on the AID repo itself. Edit it
> directly. It is a runnable procedure, not a spec — for the format/architecture of a release
> see `.aid/knowledge/infrastructure.md`; for the deep runbook (recovery, `release.sh` flags)
> see `docs/release.md`. This skill EXECUTES the process and closes the gap those two leave
> open: it always updates the release notes as part of the release.

Cuts one release of the AID repo — beta or stable — from the command to artifacts published in
the right places with every check green. Runs the whole sequence autonomously, **pausing only at
the irreversible human-gated points**: the PR merge, the tag push, and confirming the publish.

---

## Argument — REQUIRED

`/release-aid <level>` where `<level>` is exactly one of `major` | `minor` | `patch` | `beta`.

**The argument is required. If it is missing or not one of the four values, STOP and ask** (one
clear question) which level to release — do NOT default, guess, or proceed. Only continue once a
valid level is chosen.

---

## Step 0 — Resolve the target version

Read the current version: `cat VERSION` (source of truth; format `M.m.p` optionally `-beta.N`).
Never trust a version hard-coded in prose. Compute the target by the level, **bumping that level
and zeroing every level below it**:

| level | current is stable `M.m.p` | current is beta `M.m.p-beta.N` |
|-------|---------------------------|--------------------------------|
| `major` | `(M+1).0.0` (stable) | `(M+1).0.0` (stable) |
| `minor` | `M.(m+1).0` (stable) | `M.(m+1).0` (stable) |
| `patch` | `M.m.(p+1)` (stable) | **`M.m.p` (stable — PROMOTE: drop the `-beta.N`, do not bump)** |
| `beta`  | `M.m.(p+1)-beta.1` (start the next patch's beta line) | `M.m.p-beta.(N+1)` (next beta of the same target) |

**Worked from `2.2.3-beta.1`:** `beta`→`2.2.3-beta.2` · `patch`→`2.2.3` · `minor`→`2.3.0` ·
`major`→`3.0.0`. **From stable `2.2.3`:** `patch`→`2.2.4` · `beta`→`2.2.4-beta.1`.

Rationale for `patch`-from-beta = promote: a `X.Y.Z-beta.N` is the release candidate *for*
`X.Y.Z`, so finalizing that beta line ships `X.Y.Z` (never skips to `X.Y.Z+1`).

Print `current -> target` and the resulting channel plan (see Step 7's table), then proceed.

---

## Step 1 — Preconditions (STOP on any failure; do not force)

```bash
git rev-parse --abbrev-ref HEAD      # must be master
git fetch origin && git status -sb   # clean worktree; up to date with origin/master (pull if behind)
git tag -l "v<target>"               # must print nothing (no tag collision)
gh run list --workflow test.yml --branch master --limit 3   # latest master run must be green
python .claude/skills/generate-profile/scripts/run_generator.py && git diff --exit-code -- profiles/   # render-drift clean
```

- If the worktree shows only the unrelated `.aid/.aid-manifest.json` local mod, `git checkout --`
  it (it is not a release artifact) — otherwise a dirty tree STOPs the release.
- If `test.yml` is not green on the target commit, STOP — fix master first.

---

## Step 2 — Bump the version carriers

The four carriers are `VERSION`, `packages/npm/package.json`, `packages/pypi/pyproject.toml`, and
the git tag `v<target>`. The `gate` job runs `check-version-sync.sh` and fails unless the present
carriers agree.

- **stable** (`major`/`minor`/`patch`): set **all three files** to `<target>` (the tag in Step 6
  makes the fourth).
- **beta**: set **`VERSION` + `pyproject.toml`** to the SemVer form `<target>` (e.g.
  `2.2.3-beta.2`), and **leave `packages/npm/package.json` at the last stable** — the version-sync
  gate detects a pre-release and exempts the npm carrier (npm ships no betas).

> **CRITICAL — beta version format:** use SemVer `X.Y.Z-beta.N` (with the dash), NOT PEP 440
> `X.Y.ZbN`. The CLI tool-bundle name regex needs the separator; PyPI normalizes `-beta.N`→`bN`
> on publish. A PEP-440 form makes `aid add/update --from-bundle` reject the bundle and CI go red.

---

## Step 3 — Update documentation & release notes (the step the runbook omits — never skip it)

Docs drift precisely because no release step audits them; the release is NOT done until every
documentation surface reflects the released state. Two parts, both landing in the release PR.

### 3.1 — Release notes / changelog ledger

- **Drain `.aid/knowledge/backlog.md` § `## Next Release` into
  `.aid/knowledge/release-tracking.md`** — that section is the committed slice for this tag and is
  the drain's only source. Open a NEW `## v<target> - <YYYY-MM-DD>` section (today, UTC) at the top
  of `release-tracking.md` and write one bullet per row of `## Next Release`: the row's `Tag`
  (`[NEW]` / `[CHANGE]` / `[FIX]`) verbatim — the drain re-tags nothing — led by its `Title`, with
  its `Definition & done-condition` as the bullet's text. **`Title` is the key the drain matches
  on**, since a release-note bullet carries no id.
  - **It is a move, not a copy.** Delete each drained row from `backlog.md` § `## Next Release` in
    the SAME run that adds it to the new version section; an item left in both documents is a
    checkable defect. `## Next Release` is empty when the drain is done.
  - Sanity-check first: only items that genuinely ship in THIS version belong. If the committed
    slice has fallen behind (`## Next Release` holds already-shipped items, or intermediate
    versions have no section), reconcile against the published GitHub Releases +
    `git log <last-tag>..HEAD` before draining — never stamp a version with the wrong items.

### 3.2 — Documentation sync (audit EVERY affected surface)

Per-feature docs are updated during each feature's own work; THIS is the release-level sweep that
(a) makes the release-spanning updates (version references, highlights) and (b) catches anything a
feature's work missed or that the release makes stale. Derive "what changed" from this version's
`release-tracking.md` items + `git log <last-tag>..HEAD` (new/changed commands, behaviors,
capabilities, and the version bump itself), then audit and update each surface it affects:

- **`README.md`** — keep a short "recent releases -> see the changelog / GitHub Releases" pointer
  (**no** per-version "What's New in vX" block — that is the shape that froze at v1.1.0; OD-2 resolved
  = pointer only). The pointer carries no version-specific text, so it never goes stale. Also update
  any command/feature enumeration the release changed.
- **KB — `.aid/knowledge/`** — any doc describing a capability/command/behavior/channel that
  changed: `capability-inventory.md` + `module-map.md` (a new/changed command or module),
  `infrastructure.md` (release/channel/version facts — e.g. which distribution channels are
  enabled), `technology-stack.md`, and any other affected doc.
- **`docs/`** — `install.md` (command surface), `release.md`, and any versioned reference.
- **Docs site — `site/src/content/docs/`** — `reference/cli.mdx` (command reference), guides,
  reference pages. (The site's release *changelog* page lives separately at
  `site/src/pages/releases/changelog.astro` — it is auto-sourced from GitHub Releases, so leave it.)
- **Methodology content** — if the release changes a methodology skill/template/agent surface, the
  SOURCE is `canonical/` (rendered to `profiles/`); edit `canonical/` and re-render via the
  `generate-profile` skill — never hand-edit `profiles/`. The render-drift gate (Step 1 + the
  release gate) catches a missed re-render.

Discovery aid: grep the doc surfaces for the outgoing version string and for enumerations of any
command/feature the release touches — every stale hit is a doc to fix. Keep every edit TRUTHFUL:
never add an unreleased/newer feature to a historical, version-frozen section (a "What's New in vX"
block describes vX; cumulative history lives in the changelog / GitHub Releases).

> Related: the `aid-document-changelog` skill authors *adopter-project* changelogs; the AID-repo
> ledger drain (3.1) and this documentation sweep (3.2) are this skill's own responsibility.

---

## Step 4 — PR the bump + notes  ⏸ (human-gated merge)

Branch off master, commit **all of Steps 2-3** — the version carriers, the ledger drain, and
every documentation file touched by the 3.2 sweep (do NOT include `.aid/.aid-manifest.json`,
which is never a release carrier) — push, open a PR.

```bash
gh auth switch --user AndreVianna     # pushes/PRs to AndreVianna/aid-methodology need this account
git checkout -b release-<target>
git add VERSION packages/pypi/pyproject.toml            # carriers (Step 2)
[ stable ] git add packages/npm/package.json            # npm carrier (stable only)
git add .aid/knowledge/release-tracking.md .aid/knowledge/backlog.md   # ledger drain (Step 3.1)
git add README.md docs/ site/ .aid/knowledge/ canonical/ profiles/   # doc sweep (Step 3.2) — stage ONLY the files you actually changed
git status   # confirm ONLY intended files are staged; .aid/.aid-manifest.json must NOT be
git commit -m "chore(release): <target>"
git push -u origin release-<target>
gh pr create --base master --title "chore(release): <target>" --body "..."
gh auth switch --user AndreVianna-Ross   # restore
```

**⏸ PAUSE — hand the merge to the user.** The auto-mode classifier BLOCKS `gh pr merge`; print the
command for the human to run and wait for confirmation it merged:
`! gh pr merge <N> --repo AndreVianna/aid-methodology --merge --delete-branch`
Verify the PR's CI is green (each check individually — see Step 7) before handing off the merge.

---

## Step 5 — Sync + dry-run the release workflow

After the merge: `git checkout master && git pull origin master`. Then dry-run (publishes
nothing — npm does `npm pack --dry-run`, pypi skips upload; catches version-sync/render/pack
issues before the tag):

```bash
gh auth switch --user AndreVianna
gh workflow run release.yml --ref master -f ref=master -f dry_run=true
gh run watch    # then verify the dry-run run is fully green (each job)
```

> Use `-f ref=master` (NOT `-f ref="v<target>"`) — the tag does not exist yet, and the gate's
> version step falls back to the `VERSION` file.

---

## Step 6 — Tag + push  ⏸ (irreversible — confirm first)

**⏸ PAUSE for explicit confirmation before tagging** — a published version can never be reused.

```bash
gh auth switch --user AndreVianna     # re-verify active account right before the tag push
git tag "v<target>" && git push origin "v<target>"   # triggers release.yml end-to-end
```

---

## Step 7 — Verify the release workflow (every check, individually)

```bash
gh run watch    # convenience only
gh run list --workflow release.yml --limit 1        # then inspect the run's jobs one by one
```

> `gh run watch` / `gh pr checks --watch` exiting 0 is NOT proof every job passed — verify each
> job's conclusion individually.

Expected jobs by channel:

| level | gate | github-release | pypi-publish | npm-publish |
|-------|------|----------------|--------------|-------------|
| stable | pass | pass (release = latest) | pass | pass |
| beta | pass | pass (release marked **prerelease**, carries skill tarballs) | pass | **skipped** |

For a **beta**, confirm on the run that `npm-publish` shows *skipped*, `github-release` created a
**pre-release**, and `pypi-publish` is green. If `NM08` (npm-pack file-listing) fails on a stable,
it is a known flake — `gh run rerun --failed` (a version-only bump cannot drop a packed file).

---

## Step 8 — Confirm the artifacts landed  ⏸ (publish confirmation — third human-gated point)

Confirm every channel published what it should:

- **PyPI:** `curl -s https://pypi.org/simple/aid-installer/ | grep <target-normalized>` — use
  `/simple/` (the `/pypi/<pkg>/json` `info.version` lags a minute+ after upload). Beta normalizes
  `-beta.N`→`bN`.
- **GitHub Release:** `gh release view "v<target>"` — beta must show `Pre-release: true` and NOT be
  `/releases/latest`; stable must be latest. Assets = `aid-shared-v<target>.tar.gz`, five
  agents-only `aid-<tool>-v<target>.tar.gz` artifacts, and `aid-cli-v<target>.tar.gz`, plus the
  two installer libraries and `SHA256SUMS`.
- **npm (stable only):** `npm view aid-installer@<target> version`.

**⏸ PAUSE — present the confirmed-publish report to the user and await acknowledgment** before
close-out. This is the third and final human-gated point: the version is now live and can never be
reused, so the skill STOPs here with the per-channel confirmation (version shipped, channels, release
URL) instead of silently finishing. Proceed to Step 9 only after the human acknowledges — and if any
channel failed to publish, surface it here rather than closing out.

---

## Step 9 — Close out

```bash
gh auth switch --user AndreVianna-Ross    # restore the default account
```

Verify the Step 3.1 drain landed, before reporting — for every `Title` drained:

```bash
grep -F "<title>" .aid/knowledge/backlog.md          # must print NOTHING (row deleted)
grep -F "<title>" .aid/knowledge/release-tracking.md # must match, inside the new ## v<target> section
```

A title still present in `.aid/knowledge/backlog.md`, or missing from the new version section,
means the drain half-ran — finish it before closing out.

Report: the version shipped, the channels it went to, the release URL, and a one-line note that
`release-tracking.md`, `.aid/knowledge/backlog.md` and README were updated.

---

## Autonomy

Run Steps 0-9 straight through **without** per-step check-ins, EXCEPT the three ⏸ points:
(1) the PR merge — hand the `gh pr merge` to the human; (2) the tag push (Step 6) — confirm before
the irreversible publish; (3) the publish confirmation (Step 8) — present the confirmed-publish
report and await the human's acknowledgment before close-out. Everything else (version math,
carrier bumps, notes rewrite, branch/PR, dry-run, verification) proceeds autonomously. Stop
and surface any precondition failure, red check, or version-math ambiguity rather than working
around it.

## Gotchas (learned the hard way — all embedded above)

- `gh` active account silently reverts to `AndreVianna-Ross`; run `gh auth switch --user AndreVianna`
  immediately before EACH push/PR/tag and restore after.
- Classifier BLOCKS `gh pr merge` in auto-mode — hand it to the human.
- Beta = SemVer `X.Y.Z-beta.N` (not PEP 440 `bN`); npm carrier exempt for betas.
- `gh ... --watch` exit 0 ≠ all-pass — verify each job.
- PyPI `/json` lags; use `/simple/`. `NM08` npm-pack is flaky; rerun.
- Never bump/commit `.aid/.aid-manifest.json` as part of a release (not a gate carrier).
- Always dry-run (`-f ref=master -f dry_run=true`) before the tag.
