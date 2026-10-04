---
name: sync-upstream
description: Sync this Rust port to a new upstream `rich` or `rich-cli` release. Use when a new version of Python rich/rich-cli is out, or the user says "sync upstream", "bump to rich X.Y.Z", "update the port to the latest rich".
---

# Sync an upstream release into the port

Goal: absorb a new Python `rich` (or `rich-cli`) release so the mirror crate
matches it exactly, keeping our `rich-ext` code working. Read
[AGENTS.md](../../../AGENTS.md) first — the versioning and mirror rules are binding.

## 0. Identify what changed

- The current pins are in [`UPSTREAM.toml`](../../../UPSTREAM.toml)
  (`git_sha` / `git_tag` / `version` per mirrored crate).
- Determine the new target tag (e.g. `v15.1.0`). Confirm it exists upstream:
  ```bash
  gh api repos/Textualize/rich/git/ref/tags/<new_tag> --jq '.object.sha'
  ```

## 1. Diff upstream between the pinned ref and the new tag

Get the list of changed `.py` files and their diffs (pick one):

```bash
# Using the GitHub compare API (no clone needed):
gh api repos/Textualize/rich/compare/<pinned_sha>...<new_tag> \
  --jq '.files[] | "\(.status)\t\(.filename)"'
```

Or clone/fetch upstream and `git diff <pinned_sha>..<new_tag> -- rich/`.

## 2. Map changed modules to Rust files

For each changed `rich/<module>.py`, find its target in
[docs/PORTING.md](../../../docs/PORTING.md). If a changed module isn't ported yet
(⬜), note it — you only need to port the delta for modules already at 🟡/🟢, and
optionally open/refresh its roadmap issue.

## 3. Port the diffs into `crates/rich`

- Apply the upstream changes to the mapped Rust files, preserving the
  `//! Port of upstream rich/<module>.py` headers and upstream structure so the
  next diff stays legible.
- **Do not** let any of our own behavior leak into core here. If upstream added an
  extension point, mirror it in `protocol.rs`.

## 4. Repin the upstream reference

- Update the matching `[rich]` / `[rich-cli]` block in `UPSTREAM.toml`
  (`version`, `git_tag`, `git_sha`). This is now the **only** record of which
  upstream release the port tracks.
- **Do not touch any crate `version`.** Crate versions are independent of the
  upstream number and move only at release time — see AGENTS.md → Versioning for
  why the old mirror-the-version rule was dropped, and the `release` skill for
  how a version actually gets bumped.

## 5. Refresh parity fixtures

```bash
pip install "rich==<new_version>"
python scripts/capture_golden.py
```

Add golden cases for any newly-ported behavior. Investigate every fixture that
changed — a diff means either upstream changed output (expected) or our port
drifted (fix it).

## 6. Verify + record

```bash
cargo fmt --all
cargo clippy --all-targets -- -D warnings
cargo test
```

- Confirm `rich-ext` still compiles and its tests pass unchanged. If it required
  edits, that signals coupling that was too tight — prefer widening a core trait
  over patching `rich-ext`.
- Add a `CHANGELOG.md` entry: `Synced rich to <version>` plus any notable deltas.
- Update statuses in `docs/PORTING.md` if coverage changed.


## 8. Land it

Work that isn't on `main` doesn't exist. Read
[docs/BRANCHING.md](../../../docs/BRANCHING.md) — this repo has twice lost work
that GitHub reported as merged.

```bash
gh pr create --base main --fill        # ALWAYS --base main
```

After it merges, verify rather than trusting the badge — a squash or rebase merge
rewrites every SHA, so `git branch --contains` and `git cherry` both lie:

```bash
git fetch origin --prune
git merge-base --is-ancestor   "$(gh pr view <number> --json mergeCommit -q .mergeCommit.oid)" origin/main   && echo "landed" || echo "NOT ON MAIN"
```

The branch is dead once merged. Never push to it again; cut a new one from
`origin/main`.

## Done when

`UPSTREAM.toml` is repinned (and no crate version was touched), golden tests are
green against the new version, the full `fmt`/`clippy`/`test` gate passes, **and
the PR has merged with the ancestor check above confirming it reached `main`**.
