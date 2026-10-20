---
name: iru-setup-changelog
description: Bootstrap a root `CHANGELOG.md` for a repository that doesn't have one yet, by exploring its actual release history (git tags and, if hosted on GitHub, GitHub Releases) and backfilling one entry per past release in Keep a Changelog format. Invoke as `/iru-setup-changelog`, optionally with an `args` line setting `on-existing` to `ask`/`keep`/`update`/`replace` (scripted runs; default `ask`). Announces whether it is creating the changelog from scratch or updating an existing one; if `CHANGELOG.md` (or an equivalent `HISTORY.md`/`CHANGELOG.rst`/`CHANGELOG.txt`) already exists it warns and asks whether to Keep it as is (the old skip behaviour), Update it (append only the releases/tags missing from it, never rewriting existing entries), or Replace it (rebuild from history, losing hand-written entries). Use whenever a repository has release history but no changelog file yet and the user wants one backfilled from that real history instead of started blank.
model: sonnet
---

# Setup Changelog

Create a root `CHANGELOG.md` for a repository by reconstructing its release history from git tags, GitHub
Releases, and the actual code changes between them — not by guessing or leaving placeholder entries. This skill
makes no assumptions about language or build system. It is primarily a bootstrap, not a fill-gaps tool: an
existing changelog may already follow its own format and cadence, so when one exists this skill never touches it
without asking first (Step 1) — and even on **Update** it only appends releases missing from it, never rewriting
an existing entry.

## Step 0 — Resolve inputs

This skill takes one optional `args` line, `on-existing: <ask|keep|update|replace>` — passed by an orchestrator
only when its own `args` received it (scripted runs). Default `ask`. Any other `key: value` line is ignored. When
`on-existing` is `keep`/`update`/`replace`, Step 1 still prints its warning about the existing changelog but applies
that value without asking. `mode: existing` alone (if an orchestrator happens to pass it) does **not** mean "update
silently" — Step 1 still asks unless `on-existing` says otherwise.

## Step 1 — Check whether `CHANGELOG.md` already exists

Look at the repository root for `CHANGELOG.md` (case-insensitive; also treat `CHANGELOG.rst`/`CHANGELOG.txt`/
`HISTORY.md` as "already exists" — a repository may already maintain changelog-equivalent content under a
different name). A WordPress plugin/theme `readme.txt` with a `== Changelog ==` section does **not** count — it's the
WordPress.org listing, owned by its own release process; this skill never edits it, but Step 3 reads it as a source.

- **Not found**: tell the user "Creating `CHANGELOG.md` **from scratch** from the repository's release history"
  and continue to Step 2.
- **Found**: tell the user "**Updating an existing changelog** — found `<path>`" and warn that a prior changelog
  exists. Before asking, list the tags (Step 2's `git for-each-ref` command) and check which of them have no
  version heading in the file (match `## [<version>]`/`## <version>` with or without a leading `v`) — the
  "missing releases". Then, unless Step 0's `on-existing` already decided (`keep`/`update`/`replace`, applied
  without asking), ask with `AskUserQuestion` (header e.g. "Changelog"; the recommended option listed first and labeled
  "(Recommended)"), explaining each consequence:
  - **Keep as is** — "Leave the changelog untouched — this skill's original behaviour. Nothing you wrote changes,
    but <N> tagged releases (<list>) stay missing from it." Recommended when there are no missing releases (then
    say "it already covers every tag").
  - **Update** — "Append only the <N> missing releases (<list>) in Keep a Changelog style, inserted in version
    order, plus their compare links; never rewrite, reorder, or reformat an existing entry. Your hand-written
    entries survive." Recommended when there are missing releases and the file is Markdown. Not offered for a
    `.rst`/`.txt` file (its format isn't Keep a Changelog Markdown — appending Markdown would corrupt it).
  - **Replace** — "Rebuild the whole changelog from git tags / GitHub Releases. Result is a consistent
    Keep a Changelog file, but every hand-written entry (and any wording richer than the reconstruction) is lost —
    recoverable only from git history." Never the recommended option. For a differently-named file
    (`HISTORY.md`, `.rst`, `.txt`), **Replace** writes a new root `CHANGELOG.md` and leaves the old file for the user
    to delete — say so.

  Then act on the answer:
  - **Keep as is**: stop here — do not continue to Step 2; Step 7 reports only that the existing file was kept (and
    the missing releases, if any).
  - **Update**: read the existing file in full, then continue to Step 2 restricted to the missing releases.
  - **Replace**: continue to Step 2 as for a from-scratch run.

## Step 2 — Discover the release history

- List git tags oldest-to-newest with their creation dates: `git for-each-ref --sort=creatordate --format
  '%(refname:short) %(creatordate:short)' refs/tags`.
- Tags are version tags with or without a leading `v` (`v1.2.0`, `1.2.0`) whatever the stack — Maven/Gradle
  (`pom.xml`, `gradle.properties`), npm (`package.json`), Laravel (`config/app.php` `version`), WordPress (plugin
  header / `style.css` `Version:`), PrestaShop (module class `$this->version`), Python (`pyproject.toml`
  `[project].version`) all release by tagging. Use the
  tag's version (without `v`) as the heading; ignore non-version tags (e.g. `latest`, deploy markers). Never take a
  heading from an in-tree version: a `-SNAPSHOT`/`-dev`/`-dev.N` value (or Python's PEP 440 `.dev0`, e.g.
  `0.2.0.dev0`) there is unreleased work, not a release.
- **No tags at all**: there is no release history to reconstruct. Ask the user (via `AskUserQuestion` if
  available) whether to still create a minimal `CHANGELOG.md` containing just an `## [Unreleased]` section (Step
  6's format, with all commits so far treated as unreleased work), or to stop entirely since there's nothing to
  backfill. Respect either choice; don't invent version numbers. Exception: a WordPress plugin/theme released
  through WordPress.org SVN can have real releases but no git tags — when its `readme.txt` `== Changelog ==` lists
  versions, offer to backfill those entries (dated only if the text gives dates; otherwise undated headings, said
  so in Step 7) instead of the Unreleased-only file.
- **Tags found**: determine whether the repository is hosted on GitHub (`git remote get-url origin` matches
  `github.com`) and the `gh` CLI is available. If so, fetch richer data per tag:
  `gh release view <tag> --json tagName,name,body,publishedAt` (a tag may have no matching GitHub Release — that's
  fine, fall back to the tag's own creator date and derive content from commits instead).
- If the repository isn't on GitHub, or `gh` isn't available/authenticated, work from tags and commits alone —
  don't fail the skill over missing GitHub access, just note in the final report that GitHub Release bodies
  weren't available as a source.

## Step 3 — For each release, determine its actual source of content

Process oldest-to-newest so later "since previous release" ranges are well-defined. Under Step 1's **Update**,
process only the missing releases — `P` is still the tag immediately before `T` in the full tag list, even when `P`
already has an entry in the file. For each tag `T` with predecessor `P` (or the repository's first commit, if `T`
is the oldest tag):

- **A non-empty GitHub Release body exists for `T`**: prefer it as the primary source — it's already
  human-curated. Use it to compose that release's entries (Step 4), lightly reformatted to Keep a Changelog style
  rather than copied verbatim if its structure doesn't already fit.
- **No Release body, but a `readme.txt` `== Changelog ==` entry for `T`'s version** (WordPress plugin/theme):
  use it the same way — it was written for users at release time.
- **No usable Release body** (missing, empty, or GitHub Releases unavailable): derive the change set yourself.
  Read `git log P..T --oneline` and the actual diffs for commits that look meaningful (not just the commit
  subjects — terse messages like "Updated pom.xml" don't tell you whether it's a real dependency bump or a
  one-line fix) to understand real, user-facing changes: new/changed/removed public APIs or behavior, bug fixes,
  breaking changes. Confirm with `git diff --stat P T -- <source-dirs>` whether the release actually touched
  library/application source at all, or was purely docs/CI/tooling — say so plainly in that release's entry rather
  than fabricating a feature that didn't happen (a release can legitimately be "build tooling and CI updates" with
  nothing else).
- Skip changes that don't affect users of the project (repository tooling, CI config, editor/assistant
  configuration, formatting-only diffs) unless they're genuinely the entire content of that release — then say so
  rather than inventing something more exciting.
- For the **oldest** tag with no predecessor, treat everything up to it as the initial release: summarize the
  project's capabilities at that point rather than walking individual early commits one by one.
- If the repository has a long tag history (a few dozen releases or more), this step can get context-heavy.
  Dispatch one `iru-change-summarizer` agent per release (or small batch of releases) instead of reading every diff
  inline yourself: `Agent({description: "Summarize changes for <tag-range>", subagent_type: "iru-change-summarizer",
  prompt: "Summarize <predecessor>..<tag> for a Keep a Changelog entry. Source directories for this repository:
  <source-dirs>. Report back only a short bullet list of user-facing changes, grouped by
  Added/Changed/Deprecated/Removed/Fixed/Security where applicable."})`. Collect each returned bullet list here,
  keyed by tag, rather than reading every diff inline yourself.

## Step 4 — Compose each release's entries

For each tag, write one or more Keep a Changelog subsections under its version heading, using only the
subsections that actually apply:

- `### Added` — new features, APIs, capabilities.
- `### Changed` — behavior changes to existing functionality (including tooling/build changes worth surfacing).
- `### Deprecated` — soon-to-be-removed features, if any were flagged as such at the time.
- `### Removed` — removed features/APIs.
- `### Fixed` — bug fixes.
- `### Security` — security-relevant fixes.

Keep each bullet to one line, concrete about what changed rather than restating the commit message verbatim.

## Step 5 — Determine each version's date and ordering

For each tag, the date shown in its heading is, in preference order: (1) the GitHub Release's `publishedAt` date
if one was found in Step 2, (2) the tag's own creation date from Step 2's `git for-each-ref` output. Order
sections newest-first with an empty `## [Unreleased]` at the very top, above the newest release.

## Step 6 — Write `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [<newest-version>] - <YYYY-MM-DD>

### Added

- ...

## [<previous-version>] - <YYYY-MM-DD>

### Changed

- ...

[Unreleased]: <compare-link-newest-to-HEAD>
[<newest-version>]: <compare-link-previous-to-newest>
...
[<oldest-version>]: <release-or-tag-link-for-oldest>
```

- If the remote is GitHub (`owner/repo` derived from `git remote get-url origin`), use GitHub compare links:
  `https://github.com/<owner>/<repo>/compare/<previous>...<version>` for every version with a predecessor, and
  `https://github.com/<owner>/<repo>/releases/tag/<oldest-version>` for the oldest one. The `[Unreleased]` link
  compares the newest tag to `HEAD`.
- If the remote isn't GitHub, or has no remote at all, omit the compare-link reference section entirely rather
  than guessing a URL scheme for an unknown host — note this in the final report.
- **Under Step 1's Update**: don't rewrite the file. Insert each missing release's section at its correct
  newest-first position (below `## [Unreleased]`, between the existing versions it falls between), add its
  compare-link line to the existing reference section if the file has one (following the file's existing link
  style), and correct only the `[Unreleased]` link's base tag if a newer tag was inserted. Every existing line stays
  byte-for-byte as it was. Show the user the resulting diff (`git diff -- <path>`) in the report.

## Step 7 — Report

Start by restating the mode — "created from scratch", or for an existing changelog the option applied
(**kept as is** / **updated** / **replaced**, and whether it came from the user or from `on-existing`). Under
**Keep as is**, report only that plus any missing releases. Otherwise summarize: how many releases were
reconstructed (under **Update**: appended) and their version range, which releases used a GitHub Release
body as their source vs. derived analysis of commits/diffs, any release noted as tooling/docs-only rather than a
feature release, and whether compare links were included or omitted (and why). Remind the user to review the
backfilled entries themselves — this is a best-effort reconstruction of history, not a guarantee of completeness
— and that going forward, keeping `CHANGELOG.md` current on each new release is a separate, ongoing concern (in
this repository, that's handled by the `iru-release` skill's Step 10; other repositories should wire up their own
equivalent).
