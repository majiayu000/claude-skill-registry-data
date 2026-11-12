---
name: lint
description: >
  Read-only audit of vault/wiki/ for structural and provenance drift. Reports
  Errors, Warnings, and Info per the lint rules in vault/CLAUDE.md.
  Trigger when the user says "lint the vault", "audit the
  wiki", "check for broken links", "run a health check on the wiki", or
  invokes /claude-wiki-pages:lint directly. Does not repair anything —
  that is /claude-wiki-pages:fix.
allowed-tools: Read Glob Grep Bash Edit
---

# LLM Wiki — Lint

Audit the wiki. Do not repair.

Every rule enumerated here is also listed in `vault/CLAUDE.md`, the
authority for the lint rules. This skill is the executor for those rules;
when the rules change, update this skill.

## When to invoke

- The user asks for a health check on the wiki.
- Periodic audit (recommended every 10 ingests, or monthly).
- As the first half of a lint-fix cycle — the `claude-wiki-pages-curator-agent` agent invokes
  this skill, consumes the report, invokes `/claude-wiki-pages:fix`, and
  reinvokes this skill to verify.

## Reading contract

- `vault/CLAUDE.md` — the schema.
- `vault/wiki/**/*.md` — every wiki page.
- File modification times — for staleness checks against `raw/`.

## Writing contract

Exactly one write: a single append to `vault/wiki/log.md`:

```
## [YYYY-MM-DD] lint | errors: <n> warnings: <n> info: <n>
```

No other writes. Not even a scratch file. If a rule would require a write to
verify, the rule is out of scope for lint and belongs in fix.

## Rules (severity enumerated)

### Errors (block the wiki from being usable)

- **Missing required frontmatter.** Every field required for the page's
  `type:` per `vault/CLAUDE.md` must be present.
- **Dangling wikilinks.** `[[Target]]` with no matching file or alias.
- **Plain-string sources.** `sources:` entries not in `[[wikilink]]` form.
- **Missing `parent` / `path`.** Required on every page except the vault MOC.
- **MOC missing members.** A page exists under a folder but does not appear
  in the folder note's `children:` (the per-folder index is the folder note
  `<folder>/<folder>.md`, or legacy `_index.md` if present). A subfolder
  exists but does not appear in `child_indexes:`.
- **Banned legacy values.** `type: moc`, references to `_MOC.md`, field name
  `child_mocs:` — all retired in schema version 1.
- **Missing sources (provenance-completeness).** A page whose `type:` is
  `entity`, `concept`, `topic`, `project`, or `synthesis` must carry at least
  one entry in `sources:`. An empty or absent `sources:` list is an error.
  `source`, `index`, `manifest`, and `log` pages are exempt. Pages with a
  non-empty but malformed `sources:` list (already caught by the plain-string
  check above) are NOT double-flagged here — presence is counted in entries,
  not format. Implemented in `scripts/verify-ingest.sh` CHECK 5a and
  `src/core/provenance.ts` (`checkProvenance`, `provenance-completeness`
  check); covered by `tests/scripts/verify-ingest.bats` (I3 cases) and
  `src/commands/verify/verify.test.ts` (I3 cases).

### Warnings (structural drift; wiki still usable)

- **Contradictions.** Two pages on the same entity or concept make
  incompatible claims. Flag both.
- **Orphan pages.** No inbound wikilinks from any other page.
- **Single-source high confidence.** `confidence ≥ 0.8` with only one entry
  in `sources:`. Allowed only for direct quotes or settled facts.
- **Vault MOC drift.** `wiki/index.md` lists pages that no longer exist, or
  omits pages that do.
- **MOC missing aliases.** A per-folder index note lacks `aliases:` covering
  the folder topic's common display variants.
- **Legacy index filename.** A per-folder index still named `_index.md`
  instead of the folder-note name (`<folder>/<folder>.md`). Mirrors the
  engine verify WARN `legacy-index-filename`; remediation is
  `bash scripts/engine.sh migrate --write` (lint never renames).
- **Excessive nesting.** A folder more than four levels deep under `wiki/`.
- **Derived high confidence (provenance-consistency).** A page with
  `derived: true` signals LLM inference synthesised across sources rather than
  a direct statement in any single source. Granting it `confidence ≥ 0.8`
  misrepresents its evidentiary weight. Emit a warning when both conditions
  hold simultaneously. Implemented in `scripts/verify-ingest.sh` CHECK 5b and
  `src/core/provenance.ts` (`checkProvenance`, `provenance-consistency` check);
  covered by `tests/scripts/verify-ingest.bats` (I3 cases) and
  `src/commands/verify/verify.test.ts` (I3 cases).

### Opt-in WARN checks (run separately — not in the always-run verifier)

These checks are **opt-in WARN-tier only** — not blocking, not in
`scripts/verify-ingest.sh`. Run them on demand:

```
bash scripts/lint-ontology.sh [--target <vault>]
bash scripts/lint-structural.sh [--target <vault>]
bash scripts/lint-vocabulary.sh [--target <vault>] [--min-tag-usage N]
```

**S1-check — predicate domain→range conformance.**
Reads the `ontology-profile-v1` predicate table from `vault/CLAUDE.md`
(the single source of truth — the checker does not copy the table) and
flags any typed wikilink whose domain (source page class) or range (target
page class) violates a row. Examples of violations:

- A `depends_on` field on a `concept` page pointing at a `source` page
  (range violation: `depends_on` range allows only `concept`, `entity`).
- A `parent` field pointing at a non-`index` page (range violation).
- A predicate used by a page type not in its domain row.

WARN findings cite: predicate name, offending page, resolved type, and the
allowed domain or range from the profile. Unresolvable wikilink targets
(dangling links) are silently skipped — `CHECK 2` in `verify-ingest.sh`
already handles those. Implemented in `scripts/lint-ontology.sh`; covered
by `tests/scripts/lint-ontology.bats`.

**S2-structural — template-skeleton conformance + no-raw-HTML.**
Two independent sub-checks:

- **Skeleton conformance:** for each typed page (`entity`, `concept`,
  `topic`, `project`, `synthesis`), verify it contains every H2 heading
  (`## Section`) defined in its `_templates/<type>.md` skeleton. Missing
  sections signal authoring drift from the structured-authoring templates.
  `source`, `index`, `manifest`, and `log` pages are exempt (their content
  is bookkeeping, not narrative). Drafts under `_proposed/` are exempt.

- **No-raw-HTML:** flag any `<div>`, `<span>`, `<table>`, `<thead>`,
  `<tbody>`, `<tr>`, `<td>`, `<th>`, `<iframe>`, `<script>`, `<style>`,
  `<form>`, `<input>`, `<button>`, `<select>`, or `<textarea>` tag in the
  page body. Raw HTML couples content to a specific renderer and violates
  presentation independence (§5 "the Obsidian render is a view"). Content
  inside fenced code blocks (`` ``` `` delimited) is excluded.

Both sub-checks are WARN-level. Implemented in `scripts/lint-structural.sh`;
covered by `tests/scripts/lint-structural.bats`.

> **Phase 3 — deferred:** S2-overlap (>50% token-overlap single-sourcing
> detector) is explicitly deferred due to false-positive risk. Do NOT build
> it until the Phase 3 gate is open (PM sign-off required).

**S3-vocabulary — controlled-vocabulary freshness.**
Three WARN-level signals that flag drift between the synonym lexicon
(`_vocabulary.md`) and the live wiki:

- **Orphaned form:** a canonical or variant in a vocabulary group that
  matches no wiki page (frontmatter `tags:`/`aliases:`/`title:` or body
  prose), case-folded. Signals a term the lexicon governs but the wiki no
  longer uses — a candidate for curation.
- **Fully-unreferenced group:** every form in a group is absent from the
  wiki. Reported as a single WARN citing the YAML `canonical` form (not
  one line per variant) so the signal stays actionable.
- **Tag below usage floor:** a vocabulary form that appears as a page `tag:`
  on fewer than N pages (default N=2; override with `--min-tag-usage N`).
  N=2 is a named constant, not a magic number — callers can lower or raise
  the floor per vault.

Advisory-only (WARN, never blocks). Detection only: never mutates
`_vocabulary.md` — humans curate it; repair is the curator/fix path.
Implemented in `scripts/lint-vocabulary.sh`; covered by
`tests/scripts/lint-vocabulary.bats`.

### Info (candidate for review, not drift)

- **Stale pages.** No `updated:` advance in 30+ days despite newer sources
  citing the same topic in `raw/`.
- **Missing pages.** A concept or entity name appears in prose on three or
  more pages but has no dedicated page of its own.
- **Low confidence.** `confidence < 0.5` on any page.

### Staleness rules — detailed

Two distinct staleness mechanisms exist; do not conflate them:

**S4 — source-relative staleness (WARN, `scripts/verify-ingest.sh` CHECK 4).**
For each wiki page with a `sources:` list, resolve every `[[wikilink]]` to its
corresponding file in `wiki/_sources/`. Find the newest date on that source
file (field priority: `updated:` → `date_ingested:` → `date_published:`). If
that date is strictly greater than the wiki page's own `updated:` field, emit a
WARN-level `stale-source` finding. Rationale: a cited source moved on (was
updated after ingest) but the wiki page did not follow — the page may contain
claims the source has since superseded.

- The comparison is **source-relative**, not calendar-relative — no fixed
  30-day window applies here.
- Detection only: the check emits a WARN and may recommend `status: stale`, but
  does **not** auto-rewrite `status`. Mutation is the curator/`fix` path.
- A `[[wikilink]]` in `sources:` that cannot be resolved to any file in
  `_sources/` (by `title:` or `aliases:` match) is reported as a separate
  `dangling-source` WARN. A dangling link is never silently treated as fresh.
- The check is deterministic: same vault + same dates → identical findings.
- Implemented in `scripts/verify-ingest.sh` (CHECK 4, `_fm_field`,
  `_resolve_source_wikilink`, `_source_best_date` helpers). Covered by
  `tests/scripts/verify-ingest.bats` (S4 cases).

**30-day calendar staleness (Info, `skills/lint/SKILL.md` "Stale pages" rule).**
A wiki page that has not had its `updated:` field advanced in 30 or more days
despite newer related sources appearing in `raw/` is a calendar-relative Info
finding. This is a separate, independent mechanism from S4.

**Stale-memory flagging — agent-session pages (no new field, no parallel system).**
A `source_type: agent-session` page is a first-class source note that follows
the same lifecycle as every other page in `wiki/_sources/`. There is no new field
and no parallel staleness system for agent-session memories — they decay and are
flagged via the EXISTING mechanisms:

- **S4 source-relative staleness:** if a wiki page that cites the agent-session
  source has its `updated:` date fall behind the session source's own `updated:`
  field, S4 emits a WARN-level `stale-source` finding, identical to any other
  source that moved on after ingest. The session source is resolved through
  `wiki/_sources/` by `title:` or `aliases:` match, exactly as article or paper
  sources are.
- **`status: stale` + `confidence` decay:** when the curator or fix path acts on
  an S4 finding for an agent-session page, it sets `status: stale` on the
  affected wiki page and may lower `confidence`, the same mutation applied to any
  stale wiki page. The agent-session source note itself may also receive
  `status: stale` when it has been unconfirmed past the staleness threshold or
  contradicted by newer sources — again, the standard lifecycle fields, not a
  memory-specific override.
- **30-day calendar staleness:** applies equally to any wiki page sourced from an
  agent-session source that has not been updated in 30+ days despite newer related
  sources appearing in `raw/`.

In summary: stale agent-session memories are flagged the same way any stale
claim is flagged — through `status: stale`, `confidence`, and the S4 staleness
machinery. No new field, no memory-specific deletion, no parallel staleness path.

## Workflow

1. Read the schema.
2. Walk `vault/wiki/` with `git ls-files` or `find`.
3. For each page: parse frontmatter; bucket by `type:`; queue against the
   rules above.
4. Resolve wikilinks by scanning filenames and `aliases:` across the wiki.
5. Build the report.
6. Append the single log line.
7. Print the report to the terminal.

## Report format

```
LINT REPORT — <YYYY-MM-DD>

Errors (<N>):
  <path>:<lineno> — <rule>: <specific>
  ...

Warnings (<N>):
  <path> — <rule>: <specific>
  ...

Info (<N>):
  <path> — <rule>: <specific>
  ...

Summary: <N> errors, <N> warnings, <N> info items across <P> pages.
```

Exit codes:

- `0` — zero errors and zero warnings (info allowed).
- `1` — warnings present, no errors.
- `2` — errors present.

The `claude-wiki-pages-curator-agent` agent uses the exit code to decide whether to invoke
`/claude-wiki-pages:fix`.
