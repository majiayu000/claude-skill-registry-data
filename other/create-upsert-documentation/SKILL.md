---
name: create-upsert-documentation
description: >
  Maintain BOTH documentation layers as one linked wiki after a change:
  technical docs in docs/ and functional docs in docs-functional/. Use after
  implementing or changing a feature, when the user says "update the docs",
  "sync the documentation", "the docs are out of date", "document how this
  works", or as the documentation step of a development cycle. Also use when a
  good answer to a real question deserves to become a page. Reads the layer
  index first, routes each change to the right layer, cross-links related
  pages, and flags stale sections. Do NOT use for ADRs (governance-author-adr),
  the constitution (governance-constitution), or API spec / OpenAPI generation.
---

# Create documentation (dual-layer wiki)

Owned by the **Tech Writer** persona (the create-upsert-documentation step). Invoked as `/create-upsert-documentation`.

Documentation rots silently and then misleads. Treat `docs/` and `docs-functional/` not as loose
files but as one persistent, interlinked, LLM-maintained wiki: compile understanding into
cross-linked pages once, rather than re-deriving it from the code every time. The convention this
embodies is `docs/ai-sdlc/docs-wiki.md` (the knowledge layer); read it for the full schema. This is
complementary to the traceability graph in `docs/ai-sdlc/artifact-graph.md`: a single page can be
both a wiki page (index entry plus cross-links) and a graph node carrying `story:` front-matter.

## The two layers (route each change correctly)

| Layer | Folder | Audience | Holds |
|---|---|---|---|
| **Technical** | `docs/` | developers | architecture, API reference, handlers, libraries, deployment, conventions, troubleshooting - how it works |
| **Functional** | `docs-functional/` | product / business / new joiners | personas, domain model, lifecycle, glossary, overview - what the product does and why |

A single change often touches both: a new endpoint updates `docs/api/*` (technical) and may shift
`docs-functional/domain-model.md` or `lifecycle.md` (functional) if it changes observable behaviour.
Always ask "did developer-facing detail change?" and "did product-observable behaviour change?"
separately, and decide each even if the answer is "no functional change".

## Wiki discipline

- **Index, read first.** Before answering or editing, read the layer index (`docs/index.md`,
  `docs-functional/index.md`) to find the right page and avoid spawning duplicates or orphans. The
  index is generated, one entry per page (a relative link plus a one-sentence summary). If a layer
  has no index yet, scan that layer directly and note the index is absent.
- **Single-pass synthesis.** When a change lands, read it once and update *all* affected pages plus
  the index together, not one page in isolation. The common failure is fixing one page and leaving
  its neighbours and the index stale.
- **Synthesis over storage.** A page holds evolved understanding, not a raw dump. Link to the source
  (code symbol, ADR, ticket) for the detail rather than pasting it.
- **Cross-link, portably.** Link related pages with **relative markdown links** (e.g.
  `[lifecycle](../lifecycle.md)`), never `[[wikilinks]]`: GitHub and the IDE do not render
  Obsidian wikilinks or Dataview front-matter, but relative links render everywhere and are what the
  lint validates. Every new or substantially changed page should join the web, not sit orphaned.
- **Query-filing.** A good answer to a real question becomes (or updates) a page, so knowledge
  compounds in the wiki instead of disappearing into chat history. If you just explained how
  something works, file it.
- **Concept and entity pages.** `docs-functional/` already holds concept pages (domain model,
  glossary, lifecycle, personas, overview). Grow that set as new concepts, terms, or entities emerge,
  each cross-linked into the existing pages rather than added in isolation.

## Workflow

1. **Read the index** for both layers first; locate the page(s) that already cover the affected
   area. Prefer extending an existing page over creating a new one.
2. **Scope the change.** Identify what changed (the current diff, the feature just built, or a named
   area). List the affected code surfaces by path plus symbol, never line numbers.
3. **Map to docs.** For each affected surface, find the doc(s) that describe it in both layers:
   - API endpoint -> `docs/api/<resource>.md` (technical); behaviour change -> `docs-functional/lifecycle.md` / `domain-model.md`.
   - new/changed handler -> `docs/handlers/<name>.md`; new/changed library -> `docs/libraries/<name>.md`.
   - new domain concept or term -> `docs-functional/domain-model.md` + `glossary.md` (and `docs/glossary.md` if present).
   - new persona-visible capability -> `docs-functional/personas.md` / `overview.md`.
4. **Draft updates** for every matched page in both layers, plus the cross-links between them and any
   index entries the change implies. Keep each layer in its own voice: technical = precise and
   developer-facing; functional = behaviour and intent, minimal jargon.
5. **Flag staleness.** Search the docs for references to symbols, paths, or terms this change renamed
   or removed; list them as "stale, needs update" even if out of scope, rather than leaving them
   silently wrong.
6. **Confirm the diffs, then write.** Report which layer each edit landed in and list any stale
   references you flagged but did not fix.
7. **Regenerate the index and lint.** After writing, regenerate the layer indexes with
   `Build-DocsIndex.ps1` (so the index cannot drift from the pages), then run the wiki lint via the
   `governance-check-graph` skill (which runs `Check-DocsWiki.ps1`) to catch orphans, broken relative
   links, and index drift. Fix what it reports before considering the docs done. (In Claude Code:
   `/governance-check-graph`; from any tool the lint is the script behind that skill.)

## Guardrails

- **Verify before asserting.** Do not document behaviour you have not confirmed in the code.
  Reference code by file path plus symbol name, never line numbers (constitution C02). If a doc claim
  is now uncertain, mark it for review rather than restating it confidently.
- **Confirm before writing.** Show the diffs and get a go-ahead; do not write pages or index changes
  unprompted.
- **Surgical edits.** Update the sections the change affects; do not rewrite untouched pages or
  "improve" adjacent prose outside the change.
- **Both layers, every time**, and the index with them. Single-pass synthesis means a page is never
  updated while its cross-links or its index entry are left behind.
- **No em-dashes** (use " - ", commas, colons, or parentheses); match each page's existing heading and
  tone. Relative markdown links only; no `[[wikilinks]]` or Dataview-only front-matter.
- **Tool-neutral.** This skill is read by Claude Code and GitHub Copilot; the scripts run from any
  shell. Claude-only conveniences are noted in parentheses. Do not invent docs structure: if only one
  layer exists, update that one and note the other is absent.

## Next steps

- `/governance-check-graph` (Lead) - lint the wiki (orphans, broken links, index drift) and, if a page
  opted into the artifact graph, confirm its `story:` and `relates:` links resolve.
- `/governance-enrich-ticket` (any) - if the docs are a story deliverable, link them onto the ticket.
- `/create-code-generation` (Developer) - if this is part of a full cycle, return there for review and
  the PR.
