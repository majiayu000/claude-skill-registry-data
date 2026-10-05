---
name: knowledge-garden
description: "This skill should be used when the user asks to audit, health-check, or structurally validate one or more SPECIFIC named notes or a bounded topic cluster — 'audit these notes', 'check this note for orphans or broken links', 'fourth-wall check on [note]', 'validate the structure of [note]', 'spot-check [note]'. Runs a read-only audit inline. NOT for fixing issues (use /knowledge-maintain), NOT for freeform topic questions (use /knowledge-ask), and NOT for whole-graph audits ('audit my knowledge graph', 'graph health', 'full audit', no arguments) — those belong to the knowledge-gardener agent, which this skill delegates to when invoked graph-wide."
user-invocable: true
disable-model-invocation: true
argument-hint: "[note-or-topic ...]"
allowed-tools:
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__schema_validate
  - mcp__basic-memory__build_context
  - mcp__basic-memory__list_directory
  - Agent
---

# Knowledge Garden

Audit Basic Memory notes for structural and quality issues, then report
actionable, copy-paste-ready findings. **Read-only — never writes or modifies
notes.** Fixes are handed off to `/knowledge-maintain`.

This skill is the scoped, interactive sibling of the `knowledge-gardener` agent.
It owns the common case — auditing a handful of named notes inline in the main
session — and delegates the heavy, graph-wide sweep to the agent so the full
audit's hundreds of note reads stay out of the main context window.

## Arguments

The user names the notes or topics to audit after the invocation:

| Form | Example |
|------|---------|
| One note title | `/knowledge-garden npm-fastify` |
| Several notes | `/knowledge-garden npm-umzeption npm-umzug` |
| Prefixed identifier | `/knowledge-garden brew:ripgrep` |
| Topic phrase | `/knowledge-garden the IndieWeb concept notes` |
| No arguments | `/knowledge-garden` → whole-graph audit (delegated) |

## 1. Decide venue (scoped inline vs delegate)

This is the first and most important step. Classify the request:

**Delegate to the agent** when the request is graph-wide — any of:
- No arguments are provided.
- The argument is a whole-graph phrase: "my knowledge graph", "the whole
  graph", "everything", "all notes", "full audit", "--full", "graph health".
- The request implies graph-wide checks the inline path cannot do efficiently:
  schema drift across a whole type, version drift across ecosystems,
  cross-project scope leak, orphan detection across the entire graph, tag
  alignment.

To delegate, launch the read-only auditor and stop: call
`Agent(subagent_type="knowledge-gardener", description="Full graph health audit", prompt="<the user's original request, verbatim>")`
— i.e. pass a `description` summarizing the audit as "Full graph health
audit" and a `prompt` that is the user's original request, verbatim.

Relay the agent's report. Do **not** also run the inline path. **If the `Agent`
call fails or returns no usable report** (unknown subagent type, error payload,
or empty output — the `knowledge-gardener` agent may not be installed), say so
explicitly: name the failure, do **not** fabricate a clean result, and offer to
run the scoped inline path on a named subset as a fallback. Never report a
passing audit you did not actually receive.

**Run inline (scoped)** when the request names a bounded set of notes or topics
(roughly 1–8 targets). Proceed to step 2. If a "scoped" request resolves to more
than ~8 notes, stop and recommend delegating to the agent instead — inline audit
of a large set bloats context and is exactly what the agent exists for.

## 2. Resolve each target to a note

For each named target, find the canonical note:

- Plain title (e.g. `npm-umzeption`) → confirm it exists with
  `read_note` directly; if not found, fall back to `search_notes`.
- Prefixed identifier (`brew:ripgrep`) → map the prefix to its directory and
  locate via `list_directory(dir_name="<dir>", file_name_glob="*<name>*")`.
- Topic phrase → `search_notes(query="<phrase>", page_size=10)`, take the
  matching cluster, and audit those notes.

Prefix-to-directory mapping: `npm:`→`npm/`, `crate:`→`crates/`, `go:`→`go/`,
`composer:`→`composer/`, `pypi:`→`pypi/`, `gem:`→`gems/`, `brew:`→`brew/`,
`cask:`→`casks/`, `action:`→`actions/`, `docker:`→`docker/`,
`vscode:`→`vscode/`, `gh:`→`gh/`, `plugin:`→`plugins/`, `skill:`→`plugins/`,
`git:`→`engineering/git/` (git_builtin notes are conventionally plain-titled
like `git-replay` and also resolve via the plain-title path above).

Exclude schema notes (permalinks under `/schema/`) — they are structural
definitions, not subject content.

## 3. Audit each note

Load the parsed note and run the audit dimensions:

```
read_note(identifier="<permalink-or-title>", output_format="json")
```

Reading as JSON gives the parsed `observations` and `relations` arrays — the
source of truth for the note body. Then for each note check:

- **Schema** — `schema_validate(identifier="<permalink-or-title>")`. Validate
  the single named note via `identifier` — never `note_type`, which batch-
  validates every note of that type (hundreds of notes) and defeats the scoped
  purpose. Report `error_count` /
  `warning_count`, plus `unmatched_observations` and `unmatched_relations`
  (silently-absorbed categories/verbs the schema does not declare). If the
  validator output appears to repeat the same value, trust the `read_note` JSON
  (loaded above) as the source of truth for the actual body content rather than
  inferring a duplication from the validator response alone.
- **Structure** — required sections present (`## Observations` with
  `[category]`-tagged items, `## Relations` with `[[wiki-links]]`); frontmatter
  correct (type in snake_case, title/directory matching the prefix
  convention); `## Relations` is the final section (no observation-bearing
  section after it).
- **Relations** — verbs are canonical (`relates_to`, `depends_on`, etc. — flag
  `related_to`, `relates to`, trailing-colon forms). Use
  `build_context(url="<ecosystem-dir>/<note>", depth=1)` (the note's path, e.g.
  `npm/npm-foo` — not a bare title) to confirm each `[[wiki-link]]` target
  resolves and to surface inbound edges.
- **Orphan / isolation** — use two passes, because `build_context` traverses
  edges only and cannot surface a true zero-link note at all: outbound edges
  come from the `read_note` JSON `relations` array (loaded above); inbound edges
  come from `build_context`. A note absent from `build_context` results has no
  inbound links; a note with neither outbound nor inbound is a zero-link orphan.
- **Fourth-wall quality** (rules below, mirrored from the `vp-note-quality`
  skill — a skill cannot load another skill's content, so they are inlined here)
  — flag self-referential content in subject-domain notes: claims like "absent from
  Raindrop/BM/Readwise", "Connection to the Knowledge Graph" sections, or a
  lede describing coverage rather than what the subject IS. **Exemption:**
  meta-notes whose subject IS the knowledge graph (notes under
  `engineering/agents/*`, axioms, tool catalogs, conventions) may reference
  BM/Raindrop/Readwise freely — apply the rules strictly only to subject-domain
  notes (packages, people, patterns, concepts, history).

## 4. Report

Produce a structured report per note. Tier findings and, where possible, give
the exact remediation a `/knowledge-maintain` pass could apply:

````markdown
## Audit: <note title>
- **Permalink / type:** `<permalink>` (`<type>`)
- **Schema:** PASS / N errors, M warnings (+ any unmatched obs/relations)

### Findings
- **[Critical|Warning|Info] <short title>** — <what + why>.
  *Fix:* <concrete edit_note find_replace target, or "schema question → /schema-evolve">.

(repeat per note)

## Summary
| Note | Schema | Structure | Relations | Orphan | Fourth-wall |
|------|--------|-----------|-----------|--------|-------------|
````

When the audit set came from a **topic phrase** (resolved via `search_notes` in
step 2 rather than explicit titles), state in the report that you audited the
search-match set, not necessarily the whole cluster — e.g. "Audited N notes
matching 'IndieWeb'; the full cluster may contain more." Never present a
topic-phrase audit as exhaustive coverage.

Then, if any note has actionable fixes, suggest the handoff:
"Run `/knowledge-maintain <notes>` to apply the structural fixes." Distinguish:
- **Note-level edits** (missing section, trailing-obs-after-relations, verb
  drift) → actionable by `/knowledge-maintain`.
- **Schema questions** (unmatched observation categories recurring across a
  type) → defer to `/schema-evolve <type>`, NOT a note edit.

## Edge Cases

- **Note not found** — report which target failed to resolve; suggest
  `/intel` if it looks like an undocumented package/tool.
- **Scope creep** — a topic phrase resolving to 9+ notes → recommend delegating
  to the `knowledge-gardener` agent rather than auditing inline.
- **BM unavailable** — read-tool failures surface as raw error strings; report
  and suggest retrying.
- **Mid-audit BM failure** — if a `read_note` or `schema_validate` fails for one
  note in a multi-note audit, continue the rest, then report which notes
  completed, which were skipped on failure, and which were not reached. Never
  present a truncated batch as a full audit.
- **Ambiguous "audit X"** — if it is unclear whether X names a note or a whole
  area, prefer the scoped read; only delegate when the request is unambiguously
  graph-wide.

## Guidelines

- **Read-only** — never write, edit, or delete. Hand fixes to `/knowledge-maintain`.
- **Venue first** — always classify scoped vs graph-wide before doing any work.
- **Verify before reporting** — read the live note (`output_format="json"`)
  before asserting a structural defect; a flagged issue may be a parse artifact.
- **Cite specifics** — every finding references the note and the offending
  line/section, with a copy-paste remediation where possible.
- **Don't duplicate the agent** — the graph-wide 10-step sweep (schema drift,
  version drift, scope leak, tag alignment) lives in the agent; delegate to it
  rather than reimplementing those checks here.
