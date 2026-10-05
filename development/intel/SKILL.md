---
name: intel
description: "This skill should be used to research a software package OR a developer/CI tool and create or update a structured Basic Memory note with post-write cross-linking. Triggers: 'research package', 'package intel', 'what does [pkg] do', 'add [pkg] to knowledge graph', 'enrich [pkg]', when adding depends_on [[npm-*]] relations, 'research crate/gem/go module/composer/pypi package', 'research a homebrew formula', 'brew intel', 'research a cask', 'research a GitHub Action', 'action intel', 'research a docker image', 'research a VSCode extension', 'vscode intel', 'research a gh CLI extension', 'research a Claude Code plugin', 'research an agent skill', 'tool intel', 'what does [tool] do', 'upgrade haul', or a pasted npm/brew (or crate/go/composer/pypi/gem) outdated/upgrade line. Prefixes: package family — npm:, crate:, go:, composer:, pypi:, gem: (no prefix defaults to npm); tool family — brew:, cask:, action:, docker:, vscode:, gh:, plugin:, skill:."
user-invocable: true
argument-hint: "<prefix>:<name>"
allowed-tools:
  - Bash
  - Read
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__write_note
  - mcp__basic-memory__edit_note
  - mcp__basic-memory__build_context
  - mcp__basic-memory__list_directory
  - mcp__deepwiki__ask_question
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
  - mcp__claude_ai_Context7__resolve-library-id
  - mcp__claude_ai_Context7__query-docs
  - mcp__hyper-mcp__context7-resolve_library_id
  - mcp__hyper-mcp__context7-query_docs
  - mcp__tavily__tavily_search
  - mcp__tavily__tavily_extract
  - mcp__raindrop__find_bookmarks
  - mcp__raindrop__fetch_bookmark_content
  - mcp__readwise__readwise_search_highlights
  - mcp__readwise__reader_search_documents
  - mcp__socket-mcp__depscore
  - mcp__homebrew__info
---

# Intelligence

Research a package **or** a developer/CI tool and synthesize a structured Basic
Memory note, then cross-link existing notes. **One research lifecycle** — detect
→ check → resolve → enrich → synthesize → write → cross-link — routed
per-ecosystem via the table below. The two families (package and tool) share
one BM-note lifecycle end to end; **Step 3 (enrichment) is the only point where
the source roster diverges**. Smaller family-specific bits also exist in
Arguments normalization, Batch mode, Step 1 freshness, Step 4 observation rules,
and Step 6 — but the unifying axis is the shared lifecycle, not the sourcing
mechanics.

Supported ecosystems, by family:

- **package** — npm, Rust crates, Go modules, PHP Composer, Python PyPI, Ruby gems.
- **tool** — Homebrew formulae/casks, GitHub Actions, Docker images, VSCode
  extensions, GitHub CLI extensions, Claude Code plugins, skills.sh agent-skill bundles.

## Arguments

One or more identifiers, each with an optional `<prefix>:` (a single call may mix
families — `npm:fastify brew:ripgrep` — and routes each token by its own prefix).
The prefix alone selects the **family** and the routing row:

| Prefix | Family | BM dir | Note type | Ecosystem ref | Note template |
|--------|--------|--------|-----------|---------------|---------------|
| `npm` | package | `npm/` | `npm_package` | `references/ecosystem-npm.md` | `references/note-template-npm.md` |
| `crate` | package | `crates/` | `crate_package` | `references/ecosystem-crates.md` | `references/note-template-crates.md` |
| `go` | package | `go/` | `go_module` | `references/ecosystem-go.md` | `references/note-template-go.md` |
| `composer` | package | `composer/` | `composer_package` | `references/ecosystem-composer.md` | `references/note-template-composer.md` |
| `pypi` | package | `pypi/` | `pypi_package` | `references/ecosystem-pypi.md` | `references/note-template-pypi.md` |
| `gem` | package | `gems/` | `ruby_gem` | `references/ecosystem-gems.md` | `references/note-template-gems.md` |
| `brew` | tool | `brew/` | `brew_formula` | `references/ecosystem-brew.md` | `references/note-template-brew.md` |
| `cask` | tool | `casks/` | `brew_cask` | `references/ecosystem-cask.md` | `references/note-template-cask.md` |
| `action` | tool | `actions/` | `github_action` | `references/ecosystem-action.md` | `references/note-template-action.md` |
| `docker` | tool | `docker/` | `docker_image` | `references/ecosystem-docker.md` | `references/note-template-docker.md` |
| `vscode` | tool | `vscode/` | `vscode_extension` | `references/ecosystem-vscode.md` | `references/note-template-vscode.md` |
| `gh` | tool | `gh/` | `gh_extension` | `references/ecosystem-gh.md` | `references/note-template-gh.md` |
| `plugin` | tool | `plugins/` | `claude_plugin` | `references/ecosystem-plugin.md` | `references/note-template-plugin.md` |
| `skill` | tool | `plugins/` | `claude_plugin` | `references/ecosystem-skill.md` | `references/note-template-plugin.md` |

Every prefix belongs to exactly one family (the two sets are disjoint), so the
family is unambiguous from the prefix alone.

**Per-prefix identifier normalization.** Package prefixes pass through (scoped
npm `@scope/pkg` stays npm; Go module paths keep their slashes). Tool prefixes
normalize first: `action:` / `docker:` strip a trailing `@version` / `:tag`;
`vscode:` is the dot-separated `publisher.name`; `gh:` / `plugin:` / `skill:`
strip a `github.com/…` URL to `owner/repo`, validate the two-part shape, and
keep an optional `#<name>` suffix.

**Backward compatibility.** No prefix always resolves to **npm** (package
family). A bare *tool* name in a batch is disambiguated inside the tool adapter's
formula-vs-cask auto-routing (see Batch mode), not hoisted here.

## Batch mode: upgrade haul

**Detection hook (before Step 0).** If the input is not a single prefixed
identifier but a **batch** — multiple bare/prefixed names, OR a pasted
upgrade/outdated command line (`npm outdated`, `npm i a@latest b@latest`,
`cargo install-update -l`, `go list -u -m all`, `composer outdated`,
`pip list --outdated`, `bundle outdated`, `brew upgrade`, `brew outdated`) —
treat it as an *upgrade haul* (a batch refresh of already-documented notes
against a version delta) rather than a from-scratch research call. The single
prefixed-identifier path is unchanged.

**Load the shared core.** Read `references/upgrade-haul.md` in full and follow
it — input parsing/de-qualification, highlights-reel synthesis, the two
recording axes, stale-cache arbitration, batch orchestration, and the `--stale`
relationship all live there. Route each operand by its prefix to its family
adapter:

- **package family** — Axis-B narrative target is the note's inline
  `## Release Highlights` section (a one-line convention, no separate adapter
  file). Run the Step-1 existence check as one listing per package directory.
- **tool family** — follow `references/upgrade-haul-adapter-tool.md`
  (bare-name formula-vs-cask auto-routing, the `not-in-api` re-dispatch, the
  `@`-suffix dual-key fetch, inline `[feature]` / `[version]` Axis-B target).

A mixed-family batch routes each operand independently by its own prefix. Batch
detection selects the *orchestration*, not the conclusion that a refresh is due:
if Step 1 finds no existing note for an operand, that operand is fresh research
(there is no recorded version to diff against), regardless of how the input was
shaped.

## Ecosystem Dispatch

### Step 0: Detect ecosystem & family

1. **Explicit prefix** — the part before `:` is the ecosystem. Look it up in the
   Arguments table to set `FAMILY` (`package` | `tool`), the BM directory, note
   type, ecosystem ref, and note template. `FAMILY` is set **once here** and read
   only at Step 3. Strip the prefix for the name (applying the per-prefix
   normalization above).
2. **No prefix (package family only)** — infer from project context:
   `Cargo.toml` → crate, `go.mod` → go, `composer.json` (no `package.json`) →
   composer, `pyproject.toml`/`requirements.txt` (no `package.json`) → pypi,
   `Gemfile` (no `package.json`) → gem, otherwise → npm. State: "No prefix
   detected — treating as `<ecosystem>:<name>` based on project context. Use an
   explicit prefix to override."
3. **Unknown prefix** — error and print the 14-row Arguments table.
4. **Third-party tap (`brew:` only)** — count `/`-segments after `brew:`; the
   zero/one/two-slash dispatch (core formula vs tap formula vs invalid shape)
   lives in `references/ecosystem-brew.md` ("Third-Party Tap Formulae"). BM dir,
   note type, and reference are unchanged; only Step 2's fetch mechanics differ.

**Title convention.** The command uses `:` delimiters, but the BM note title
replaces every `:`, `/`, and `#` with `-` (preserving `@` and `.`) — a purely
literal mapping matching the filename BM generates. Examples: `npm:fastify` →
`npm-fastify`, `npm:@fastify/postgres` → `npm-@fastify-postgres`,
`action:actions/checkout` → `action-actions-checkout`,
`plugin:voxpelli/vp-claude#vp-knowledge` → `plugin-voxpelli-vp-claude-vp-knowledge`.
See CLAUDE.md → "Prefix convention" for the full rule.

### Step 1: Check for existing note

Follow `references/note-lookup-and-freshness.md`: the existence glob, the
freshness-tier matrix (the `<60 days` fast-path differs by family — package runs
Context7 + Socket, tool does not), the append-don't-overwrite rule, and the
audit-context stale-handling branch. Hold the recorded version + `## Relations`
for later steps.

### Step 2: Resolve registry & repository

Read the routing row's `references/ecosystem-<ecosystem>.md` for the
registry/extraction API, required headers, and how to extract `owner/repo` for
the enrichment and changelog steps.

**Forge detection.** Parse the **host** of the resolved repository/homepage URL
and hold it as `repo_forge` (`github`, `codeberg`/any Forgejo, `sourcehut`
`*.sr.ht`, or `unknown`). When `repo_forge != github`, follow
`references/forge-fallback.md` for the DeepWiki-skip rule and the changelog
procedure. `action:` and `gh:` encode a GitHub `owner/repo` by construction — skip
forge detection for them.

When the registry's `repository` and `homepage` fields point at **different**
hosts, the `repository` field wins for `gh`/DeepWiki purposes — a non-GitHub
`homepage` alone does not make it a non-GitHub forge. It usually means a
canonical home with a GitHub mirror (observed: an npm package homed at
`tangled.org` with `repository` on GitHub), which is itself worth a `[gotcha]`
observation: issues and PRs may live on the canonical forge, so a GitHub issue
search understates the project's activity.

If the ecosystem reference documents a download/popularity source, fetch the
count now and hold it as `popularity_count` for Step 4.

### Step 3: Family enrichment — the source-roster branch

This is the point where the two families' **source roster** diverges (other
steps carry smaller family-specific bits). Route by `FAMILY`:

- `FAMILY=package` → load and follow `references/enrichment-package.md`
  (seven sources: DeepWiki, Context7, Tavily, Raindrop, changelog, Readwise,
  Socket depscore).
- `FAMILY=tool` → load and follow `references/enrichment-tool.md` (six sources:
  DeepWiki, Tavily, Raindrop, changelog, Readwise, man-page — plus Homebrew
  analytics and the Open VSX trust signal where applicable).

Five sources are common to both (DeepWiki, Tavily, Raindrop, Readwise,
changelog). **Design invariant:** each family file OWNS its per-ecosystem
skip/run gates as explicit conditionals — DeepWiki skip for brew/cask; man-page
for brew/cask only; Open VSX for vscode only; Context7 for the package family
only; Socket for npm/pypi/cargo/gem only. These gates are NEVER collapsed into a
generic "run these N sources" loop here or in either family file.

### Step 4: Synthesize into note

Read the routing row's `references/note-template-<ecosystem>.md`. Every note uses
three enrichment layers: **frontmatter** (`type`, `tags`, and any `packages`
array), **`## Observations`** with `[category]`-tagged items, and
**`## Relations`** with `[[wiki-links]]`.

Observation conventions:

- **`[version]` (mandatory, every cohort — and EXACTLY ONE per note)** — record
  the documented latest version as a clean leading token, e.g.
  `- [version] 5.8.5`. The same value goes in the header pipe
  (`… | v<version> | …`); keep them consistent. (Which slot `--stale` reads first
  is cohort-dependent — the `[version]` observation for npm, the header pipe
  otherwise — so refresh both.)
  **Never add a second `[version]` line, and never write release prose under the
  `[version]` category.** The extractor takes the first PARSEABLE `[version]`
  line in file order, so a narrative line like
  `- [version] 3.0 dropped Node 18` placed above the canonical token silently
  becomes the recorded version — the note then reads correctly to a human and
  wrong to every consumer. Version narrative belongs in `## Release Highlights`
  (package family) or a `[feature]` observation (tool family). When refreshing,
  UPDATE the existing `[version]` line rather than appending a new one.
- **`[popularity]`** — if a count was obtained, add it with metric window +
  source, e.g. `- [popularity] 2.1M downloads/week (npm, 2026-04)`. Omit for
  PyPI and Go (no reliable count).
- **`[security]`** — Socket depscore (package family) or the Open VSX trust
  signal (vscode); plus any advisory findings.

**No wiki-links in observations.** Never use `[[Target]]` in an observation line —
BM's parser treats `[[` as a relation boundary. Put all wiki-links in
`## Relations` only.

**Verify before capture.** For any note not on Step 1's fast path (missing, 60+
days, or security-sensitive/thin-evidence), follow `references/verify-before-capture.md`
before writing.

### Step 5: Write or update the note

Follow `references/note-write-mechanics.md` for the new-note / relocated-stub /
existing-note decision, the two `edit_note` find_replace templates, the
never-`append`-with-`section=Observations` rule, the large-note anchoring rule, and
the "trust `schema_validate` + the file, not the inline count" rule.

### Step 6: Confirm and summarize

Report a compact summary:

- Family and note location (directory + title).
- Key findings and any `[gotcha]`/`[limitation]` observations recorded.
- Security/analytics concerns — Socket scores (package) or Open VSX/analytics
  (tool), whichever applies.
- Cross-links added (or deferred to follow-up pass for large batches).
- Enrichment-source status — for each Step-3 source, report which of *used /
  attempted-but-failed / intentionally-skipped* applies. Sources must be
  *attempted*, not skipped by assumption; an attempt that fails (auth error,
  server not found) must be surfaced as a failure, never silently omitted or
  relabelled an intentional skip (non-GitHub forge, ecosystem not covered).
- Unresolved contradictions from Step 3–4.

### Step 7: Cross-link existing notes

Follow `references/cross-link-existing-notes.md`: search for notes referencing
this subject, add `relates_to` links where genuine, verify each edge resolved via
the relation index (not `build_context`), and reconcile bare-name stubs.

## References

Every file below is one level deep in `references/` and reachable from the steps
above:

- Lifecycle: `note-lookup-and-freshness.md`, `verify-before-capture.md`,
  `note-write-mechanics.md`, `cross-link-existing-notes.md`.
- Enrichment (Step 3 branch): `enrichment-package.md`, `enrichment-tool.md`.
- Changelog/forge fallbacks: `gh-api-fallback.md`, `forge-fallback.md`.
- Batch: `upgrade-haul.md`, `upgrade-haul-adapter-tool.md`.
- Per-ecosystem recipes + note templates: `ecosystem-<prefix>.md`,
  `note-template-<prefix>.md` (see the Arguments table).
