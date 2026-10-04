---
name: "Docs: Changelog"
description: "Build or update the changelog from conventional commits and project it to every surface the project uses"
when_to_use: "After a release tag lands (pr-land names this moment), or when the user asks for a changelog, release notes, a what's-new page or to bring an existing CHANGELOG.md up to date."
model: sonnet # was haiku: auto mode skips haiku and keeps the session model, which is sometimes Fable here; sonnet pins it
effort: medium
metadata:
  glyph: ᛊ
  family: doc
disable-model-invocation: false # programmatic (built from commits), and its trigger moment follows pr-land; approval gates the write
allowed-tools: ["Read", "Glob", "Grep", "Write", "Edit", "Bash(git:*)", "Bash(gh:*)", "Bash(svu:*)", "Bash(~/.claude/library/scripts/slop-scan.py:*)", "Bash(~/.claude/library/scripts/safe-version-next.sh:*)"]
arguments: ["scope", "targets", "version"]
argument-hint: "[root|plugin:NAME] [md|release|app|docs|all] [tag (optional, scopes to one release)] (default scope: root; default targets: md + whatever already exists)"
---

# Distro: Changelog

One source of truth, projected outward, the same shape as the roadmap system. `CHANGELOG.md` at the repo root is canonical; GitHub Releases, an in-app what's-new surface and a docs-site page are projections built from it, never written independently. A projection that drifts from the file is a bug.

## Scope

The first argument, always optional, always defaulting to `root`:

| Scope | Covers | Tag series | Changelog file |
|---|---|---|---|
| `root` (default) | the whole repo | `v*` | `CHANGELOG.md` |
| `plugin:NAME` | one plugin's own subtree | `NAME-v*` | plugin's own changelog source, or `<plugin dir>/CHANGELOG.md` |

`plugin:NAME` resolves `NAME` against `.claude-plugin/marketplace.json`'s `plugins[]` entries: `name` gives the tag prefix (`NAME-v`), `source` gives the subtree directory (strip a leading `./`) that `git log` and `safe-version-next.sh` scope to. No matching entry is an error, not a silent fallback to root. This is why the token carries a `kind:` prefix rather than a bare name: `docs` is both a target and a real top-level directory here, so slot one has to be unambiguous on sight. A future non-plugin subtree gets its own kind (`dir:`, `pkg:`) with its own resolver; the parse rule (`root`, or anything containing `:`, is a scope; anything else is a target) never changes.

**Where the changelog is written is not always inside `{scope-dir}`.** A plugin's own subtree is usually build output (a generated `marketplace/{name}/` folder that its build script regenerates wholesale on every source change, then a pre-commit hook stages), so a file written directly into it gets silently deleted the next time anything else in the plugin changes. Find the plugin's build script (this repo's convention: `library/scripts/build-{name}-plugin.py`; a differently-built plugin needs its own equivalent, found by reading its docs or asking rather than assumed) and read its own named constant for this (`CHANGELOG_SOURCE` in `build-roadmap-plugin.py`, alongside `README_SOURCE` and `VERSION_SOURCE`) if it has one; that constant's path is `{changelog-path}`, and the build copies it into the shipped plugin the same way it does the readme, so it survives every rebuild. No such constant, or no build script at all: fall back to `<plugin dir>/CHANGELOG.md` directly (this is the pre-existing behaviour, and the right one for a plugin that isn't generated build output). Root scope has no such indirection: `{changelog-path}` is always `CHANGELOG.md` at the repo root.

Every step below runs identically for either scope; only the directory git log and svu/`safe-version-next.sh` are scoped to (`{scope-dir}`), the tag prefix they use (`{prefix}`) and where the changelog file itself is written (`{changelog-path}`) change. All three are plain prose placeholders, not literal shell variables, filled in from what Step 1 resolves. `{scope-dir}` and `{changelog-path}` are the same path for root scope, but diverge for a build-output plugin, where history is scoped to the built subtree while the file itself lives with the plugin's other hand-maintained sources.

## Targets

| Token | Surface | Applies when |
|---|---|---|
| `md` | `CHANGELOG.md`, Keep a Changelog layout | always; this is the source |
| `release` | GitHub Release notes per tag (`gh release`) | repo has tags on GitHub |
| `app` | structured data for an in-app what's-new surface | the app has (or wants) one |
| `docs` | changelog page in the docs site | a docs site exists |
| `all` | every surface that applies to this project | |

No arguments: build `md`, then refresh any projection that already exists in the repo (an existing release for the previous tag, an existing changelog data file or docs page). Never scaffold `app` or `docs` surfaces unasked; offer when the project looks like it wants one.

## Step 1: Establish the range

Parse `$ARGUMENTS` (whitespace-separated words) into scope, targets and an optional tag, in that order. This is prose parsing, not variable substitution: `$ARGUMENTS` is the only token the harness fills in; every other placeholder in this skill (`{scope-dir}`, `{changelog-path}`, `{prefix}`, `{tag}`) is a value this step resolves and later steps refer back to.

1. **Scope** (always optional, first word only counts as scope): the literal word `root`, or any word containing `:`, is consumed as the scope word and removed from the argument list. Any other first word (`md`, `release`, `v2.5.0`, no arguments at all) means scope defaults to `root` and that word is left for the next rule to read. `root` resolves to `{scope-dir}` = `{changelog-path}` = `.` (repo root, and `CHANGELOG.md` within it) and `{prefix}` = `v`. `plugin:NAME` resolves `NAME` against `.claude-plugin/marketplace.json`'s `plugins[]` entries: `source` (with a leading `./` stripped) becomes `{scope-dir}`, and `{prefix}` becomes `NAME-v`; `{changelog-path}` is resolved per the Scope section above (the plugin's own build-script constant when one exists, else `{scope-dir}/CHANGELOG.md`). No matching entry is an error, not a silent fallback to root.
2. **Targets**: the next remaining word, if it's one of `md`/`release`/`app`/`docs`/`all`; otherwise targets defaults per the Targets section below and that word is left for the next rule.
3. **Tag**: whatever word remains, if any; this is the optional version argument scoping the run to one release.

- **(a) No file at `{changelog-path}`** → build fresh from the earliest tag matching `{prefix}*` (or full history under `{scope-dir}` if untagged).
- **(b) Placeholder, or already Keep a Changelog-shaped** → a `<!-- doc-changelog: generated ... -->` marker (left as the first line by this skill from now on, mirroring `doc-readme`'s convention) or a file that's already unambiguously in Keep a Changelog structure (a prior unmarked run of this same skill); proceed with the normal forward-generation logic below.
- **(c) Hand-written changelog in some other format/voice** → stop and flag it explicitly before writing anything: offer to convert it to Keep a Changelog format, or to respect the existing format and append new entries in its own voice instead. Don't silently Frankenstein a Keep a Changelog section onto a differently-structured hand-written file.

`git tag --sort=-v:refname --list "{prefix}*"` for existing tags in this scope's series; `~/.claude/library/scripts/safe-version-next.sh` (with `--plugin NAME --dir {scope-dir}` for a plugin scope) rather than bare `svu current`/`svu next`, so the 0.x guard and the plugin's own tag/directory scoping both apply here the same as they do to any other tag this config creates. The unit of work is tag-to-tag within this series: each version section covers `previousTag..tag` (both `{prefix}`-matching), and `[Unreleased]` covers `latestTag..HEAD`, in both cases limited to commits touching `{scope-dir}` (`-- {scope-dir}` on every `git log`, a no-op for the root scope, where `{scope-dir}` is `.`). If the file at `{changelog-path}` exists (state b), its most recent version heading shows where it stopped: only generate forward from there; never rewrite sections already published.

The resolved tag from Step 1's parse (if any) names a tag in this scope's series: scope the run to that single release (`previousTag..{tag}`), leaving every other section untouched. This is pr-land's hand-off; it can invoke `/doc-changelog root md {tag}` or `/doc-changelog plugin:NAME md {tag}` right after tagging.

**Promote, don't regenerate:** when a new tag lands and `[Unreleased]` already carries curated entries, promote that content into the new version section, verify nothing in the tag range is missing (add what is), and rebuild `[Unreleased]` from `newTag..HEAD`. Hand-polish survives; only genuinely new material gets derived.

## Step 2: Build the canonical entries

For each version in range, read `git log --first-parent previousTag..tag --format='%h %s%n%b' -- {scope-dir}`: with merge-commit landings this yields one commit per merged PR (plus direct-to-main commits), so each entry derives from a PR-level change rather than branch-internal noise. The `-- {scope-dir}` limit is what makes a plugin scope mean anything: a PR that touches both root config and a plugin (docs plus `marketplace/roadmap/**` in one PR, say) contributes an entry to both changelogs independently, each reading only the part of that PR's diff under its own scope. Stacked-PR landings are expected to preserve this (a stack merge lands each layer bottom-up, probably with its own merge commit; the docs do not say so, so check the first-parent output the first time a stack lands). Fall back to the full log (still `-- {scope-dir}`-limited) only when the first-parent output is too thin to describe the release. Map conventional-commit types to Keep a Changelog sections:

| Commit type | Section |
|---|---|
| `feat` | Added |
| `fix` | Fixed |
| `enhance`, `perf` | Changed |
| `BREAKING CHANGE` footer or `!` | its own **Breaking** entry, listed first |
| `refactor`, `docs`, `test`, `chore`, `ci`, `deps` | omitted unless user-visible |

Entries describe the change from the user's side ("Exports now include timestamps"), not the commit's ("add timestamp to export serialiser"). Collapse commit-level noise: one entry per coherent change, not per commit. British spelling; no em-dashes.

## Step 3: Write `{changelog-path}`

Keep a Changelog structure: `# Changelog` intro, `## [Unreleased]`, then `## [x.y.z] - YYYY-MM-DD` sections newest first, comparison links at the bottom when the repo is on GitHub. On a fresh build (state a/b from Step 1), the very first line is the marker comment: `<!-- doc-changelog: generated {date}. Delete this line once you hand-edit this file. -->`.

**Collapsibility for older entries.** Once the file holds more than a handful of version sections, wrap everything older than the most recent few in GFM's native `<details><summary>`: `[Unreleased]` and the newest 2-3 versions stay always-visible, older ones collapse behind a one-line summary (`<summary>0.4.0 and earlier</summary>`). No custom chevron needed. Adjusting which sections are wrapped as new versions land is presentational only; it doesn't touch a section's own entries, so it isn't the "rewrite already-published sections" the red flags below warn against.

No badge row and no separate provenance line here: each entry is already dated by construction, which is its own honesty record; a "generated on X" line would just repeat what the file already states more precisely.

Scan the new or changed sections before showing them:

```bash
~/.claude/library/scripts/slop-scan.py --strict - <<'SLOP_EOF'
<draft sections>
SLOP_EOF
```

Non-zero exit: rewrite to clear every `L<n> <rule>: <excerpt>` line and rescan, at most twice. If hits remain, list them under the draft so the reviewer decides.

Show the draft (or the diff, when updating) and **await approval** before writing.

**npm packages** (a `package.json` with no `"private": true`): check `CHANGELOG.md` ships or is reachable: either listed in `files` or linked from the README, since the npm page shows only the README. Flag whichever is missing; registry users otherwise never see release history.

## Step 4: Project

Only after `md` is approved and written:

- **`release`**: for each new tag (in this scope's `{prefix}` series), `gh release create {tag} --title {tag} --notes-file -` fed with that version's section verbatim (`gh release edit` when the release exists). The Release body is the section, not a rewrite. A plugin's `NAME-v*` tags get their own GitHub Releases, distinct from the root `v*` series; both point at the same commit when a landing bumped both.
- **`app`**: emit the structured form the app consumes. Root scope only; a plugin has no in-app what's-new surface of its own. If none exists yet and the user asked for `app`, propose the simplest fit for the stack (for SvelteKit: a `changelog.json` importable by a route) and build it from the same entries.
- **`docs`**: update the docs-site changelog page from the same sections, matching that site's existing format. Root scope only, for the same reason.

## Step 5: Report

Versions covered, surfaces written, surfaces skipped and why, plus any npm visibility flag from Step 3.

## Red flags

**Never:** write a projection that disagrees with `CHANGELOG.md`; rewrite already-published version sections (corrections get an explicit edit, called out to the user); invent user-facing descriptions for changes you don't understand; quote the commit and ask.

<raw-arguments value="$ARGUMENTS" />
