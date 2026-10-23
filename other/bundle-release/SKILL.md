---
name: bundle-release
disable-model-invocation: true
description: 'Prepares ycc bundle releases for ycc maintainers only. Use when bumping ycc version, regenerating release bundles, or drafting ycc release notes.'
argument-hint: '<new-version> [--dry-run] [--skip-notes] [--no-publish]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash(git:*)
  - Bash(python3:*)
  - 'Bash(ycc/skills/bundle-release/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/bundle-release/scripts/*.sh:*)'
  - Bash(./scripts/sync.sh:*)
  - Bash(./scripts/validate.sh:*)
---

# ycc Bundle Release

This skill prepares a `ycc` release by validating a clean tree, bumping the version
across all source product version fields, regenerating the derived Cursor,
Codex, and opencode bundles, running the full validator sweep, and drafting release notes. It
never auto-commits or pushes — the user reviews all changes and runs the emitted
commands manually.

## Arguments

Parse `$ARGUMENTS` for:

- **new-version** (required, first positional) — target semver, e.g. `2.1.0`.
- **--dry-run** — run preflight and print the full release plan, write nothing.
- **--skip-notes** — skip drafting `docs/releases/<version>.md`.
- **--no-publish** — this is the default; the skill never invokes `gh release create`.
  The flag is accepted silently for clarity.

**Questions:** class `confirm-publish` (semver concern, release-branch intent); headless (no question tool or chat turn): stop before the bump and print the concern plus the rerun command. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Phase 0: Pre-flight

Run `ycc/skills/bundle-release/scripts/preflight.sh`. On non-zero
exit, STOP and surface the full stderr output to the user. Do not proceed.

Checks owned by `preflight.sh`:

- Working tree is clean (`git status --porcelain` returns empty output).
- Currently on `main` branch (or user has confirmed a release branch is intentional).
- Version parity: every participating product version field (marketplace `plugins[]`
  entries, optional metadata versions and package manifests) equals the canonical
  `ycc/.claude-plugin/plugin.json` version. The helper reads
  `ycc/settings/packages.json` directly: every included native entry must have an
  existing versioned manifest regardless of `listed`; deferred/excluded paths are
  suppressed from the bounded scan, and file-copy entries are skipped. Included
  opencode npm manifests are required to exist at the lockstep version
  (check-only). `ycc-mods` is excluded. The bounded scan
  remains a backstop for unmodeled manifests; versionless marketplace entries and
  unmodeled optional manifests stay versionless. See `references/version-policy.md`
  for the exact runtime paths.
- No stale version literals (`version: X.Y.Z` or `"version": "X.Y.Z"`) in hand-edited
  docs (`CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/README.md`) where the semver does
  not match the current bundle version. Author should use the `<managed by
bundle-release>` placeholder form in example snippets — see
  `references/version-policy.md` for the full rule.
- `./scripts/validate.sh` passes on the pre-release tree.

## Phase 1: Semver sanity check

Read `ycc/skills/bundle-release/references/version-policy.md`.
Compare the current version (reported by preflight output) against the requested
`<new-version>`.

Determine the bump kind (major / minor / patch) by inspecting recent commit history:

```
git log $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD --oneline
```

If the requested bump looks mismatched with the recent history — for example, new
skills were added but a patch bump was requested — surface the concern and ask the user
to confirm before continuing.

## Phase 2: Dry-run check

If `--dry-run` was passed, print the full release plan:

- Current version and new version.
- Source files that will be modified: `ycc/.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, and `ycc/package.json` when it carries a version.
  The package model is validated, not bumped; generated `packages/**` and runtime
  manifests are check-only (including the required opencode npm manifest).
- Derived bundles that will be regenerated (`.cursor-plugin/`, `.codex-plugin/`, `.opencode-plugin/`,
  the `.omp-plugin/` catalog, and `packages/omp/<pkg>/.omp-plugin/plugin.json`).
- All commands that would be executed, in order.

Then STOP without writing or executing anything.

## Phase 3: Bump version

Run `ycc/skills/bundle-release/scripts/bump-version.sh <new-version>`.

The wrappers share `scripts/release_versions.py`, which reads
`ycc/settings/packages.json`, discovers required included native and bounded
unmodeled product version fields, and validates all inputs before writing. A missing
or malformed model or required manifest causes no writes; a write error mid-bump
has best-effort rollback only (not crash-atomic).
Generated surfaces (`packages/` including `packages/omp/<pkg>/.omp-plugin/plugin.json`,
runtime bundles, the `.omp-plugin/` catalog, `.agents/plugins/marketplace.json`)
are checked by preflight but never bumped directly. Bumped files are JSON
re-serialized (2-space indent, trailing newline), preserving key order and unrelated
fields. After it exits, surface the diff (`git diff` of the modified files from
`git status --short`) for user review. If the script exits non-zero, surface stderr
and STOP.

## Phase 4: Regenerate derived bundles

Run `./scripts/sync.sh`. Source and generated versions temporarily differ after the
bump; sync must finish before post-bump parity checks can pass. Never fix stale
generated versions by hand. Review all source package/marketplace changes along
with the generated diff; after committing the reviewed changes, `preflight.sh` can
check parity again (its clean-tree gate still applies).

If it fails, surface the following rollback command and STOP:

```
for path in ycc/.claude-plugin/plugin.json .claude-plugin/marketplace.json \
            ycc/package.json \
            packages .agents/plugins/marketplace.json .agents-plugin \
            .cursor-plugin .codex-plugin .opencode-plugin .omp-plugin docs/inventory.json; do
  if git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
    git checkout -- "$path"
  fi
done
./scripts/sync.sh
```

Do not hand-edit `packages/`, `.agents/plugins/marketplace.json`, `.agents-plugin/`,
`.cursor-plugin/`, `.codex-plugin/`, `.opencode-plugin/`, or `.omp-plugin/` — regenerate them only.
The rollback loop restores tracked paths (including deleted files) but does not
remove newly generated untracked files; review those separately.

## Phase 5: Validate

Run `./scripts/validate.sh`.

If it fails, surface the same rollback command as Phase 4 and STOP. Fix the reported
error, re-run `./scripts/sync.sh` if needed, then re-run `./scripts/validate.sh` before
continuing.

## Phase 6: Draft release notes

Unless `--skip-notes` was passed, run:

```
ycc/skills/bundle-release/scripts/draft-notes.sh <new-version>
```

This reads `references/release-notes-template.md` and writes `docs/releases/<new-version>.md`.
The `{{PACKAGES_TABLE}}` placeholder is rendered from `ycc/settings/packages.json`
with Package, Runtime, Status, Mechanism, Listed, Version or target, and Notes
columns. Included packages show the release version; deferred/excluded entries
show their target. The opencode npm package is experimental, opt-in, and not yet
published; file-copy fallback is noted separately. Prompt the user to review the
Packages, Summary, and Upgrade Notes sections before committing. If the script
exits non-zero, surface stderr and STOP.

## Phase 7: Emit next-step commands

ALWAYS emit the following block, substituting the actual `<new-version>` value:

```
Release prepared. No commits have been made — review the diff, then run:

for path in ycc/.claude-plugin/plugin.json .claude-plugin/marketplace.json \
            ycc/package.json \
            packages .agents/plugins/marketplace.json .agents-plugin \
            .cursor-plugin .codex-plugin .opencode-plugin .omp-plugin docs/inventory.json \
            docs/releases/<new-version>.md; do
  if [ -e "$path" ] || git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
    git add -A -- "$path"
  fi
done
git commit -m "chore(release): v<new-version>"
git tag v<new-version>
git push origin main --tags

# Optional GitHub release:
gh release create v<new-version> --notes-file docs/releases/<new-version>.md --title "v<new-version>"
```

The loop skips absent paths safely. If `--skip-notes` was passed, omit the
`docs/releases/<new-version>.md` line from the loop.

## Important Notes

- Never auto-commits or pushes. The user reviews all changes and runs the emitted
  commands manually.
- Never hand-edits generated paths, including `packages/**`; use `./scripts/sync.sh`.
- Rollback command for any mid-run failure after Phase 3: the conditional
  `git checkout` loop from Phase 4 followed by `./scripts/sync.sh`.
- See `references/release-checklist.md` for the full manual checklist.
- `references/release-notes-template.md` is the release-notes template; `scripts/draft-notes.sh` reads it (Phase 6), so read it directly only when editing the notes layout.
- See `references/version-policy.md` for semver bump rules and the never-edit list.
