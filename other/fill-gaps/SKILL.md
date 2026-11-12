---
name: fill-gaps
description: >
  Complete the wiki: no empty pages, no dangling [[wikilinks]], with the graph
  clustered around the project's core topics. Stages curated repo sources,
  ingests them, authors topic hub pages, resolves every dangling link, enriches
  thin pages, then heals + verifies. Trigger when the user says "fill the
  knowledge gaps", "complete the wiki", "no empty wiki pages/links", "make the
  graph cluster around <topics>", or invokes /claude-wiki-pages:fill-gaps
  directly.
allowed-tools: Bash(bash *) Read Glob Grep
disable-model-invocation: true
---

# LLM Wiki — Fill Knowledge Gaps

Turn a thin or hole-y vault into a **complete**, gap-free wiki. Two problems this
skill closes that ordinary ingest/lint do not:

1. **Dangling wikilinks** — `[[Target]]` references whose target resolves to no
   page. The Bun engine's `verify` does **not** detect these (they pass `0/0`),
   yet they render as empty grey nodes in Obsidian's graph. This skill scans for
   them with `scripts/graph-quality.sh` and drives them to **zero**.
2. **Shallow / off-topic coverage** — the graph should concentrate around the
   project's core topics, not scatter. This skill stages the high-signal repo
   sources, ingests them into topic clusters, and authors a **hub page** per
   topic so the majority of nodes and edges cluster there.

This skill **orchestrates existing capabilities** — the `ingest`, `curator`, and
`polish` agents plus the engine. It adds no new write logic of its own. Because a
Claude Code plugin cannot ship a runnable `.mjs` Workflow directly, this skill
carries the orchestration as a bundled **template** and **materializes it into
the project on demand** (the same pattern `init` uses for its vault scaffold),
then runs it with the Workflow tool.

## When to invoke

- The Obsidian graph shows empty nodes / the wiki has broken `[[links]]`.
- Coverage of the core topics is thin and you want it filled from the repo.
- You want the graph re-centered on a fixed set of topic clusters.
- Re-run any time — every phase is git-checkpointed and the run is idempotent
  (prefer-update, no duplicate pages; resolved links stay resolved).

This skill writes to the vault (via the agents it dispatches), so it is gated
like ingest and is `disable-model-invocation: true` — invoked only on explicit
request, never auto-fired.

## The capability contract (what the workflow does)

The bundled workflow runs **eight sequential phases**. Write phases are never
parallelized (they share one git tree and the `index.md` / `log.md` / folder
notes) and each self-checkpoints, so the whole run is a series of revertible
commits.

| Phase | Does | Driver |
|-------|------|--------|
| 0 Resolve+Baseline | resolve vault/repo, assert vault realpath, baseline `verify` + `graph-quality.sh` | bash agent (read-only) |
| A Stage | `cp` curated repo sources into `raw/repo/<topic>/` (NEW files only) | bash agent + `snapshot.sh` |
| B Ingest | one ingest-agent run per topic (≤25 sources each), pre-approved | `claude-wiki-pages-ingest-agent` |
| C Hubs | author the topic hub pages, each linking its whole cluster | `claude-wiki-pages-ingest-agent` |
| D Dangling | create real pages for backed concepts → curator alias/fuzzy fix → prose-ify the rest | ingest + `claude-wiki-pages-curator-agent` |
| E Enrich | update thin pages from their sources + the new material | `claude-wiki-pages-ingest-agent` |
| F Heal+Polish | final `engine heal` → `polish` (graph colors, index) → `verify` | curator + `claude-wiki-pages-polish-agent` |
| G Measure | re-scan dangling + cluster metric + hub spot-check; assert gates | bash agent (read-only) |

### Dangling-link resolution policy (no empty stubs — HARD RULE)

Never create an empty page to satisfy a link, and never link to a page that does
not exist. For each distinct dangling target `T`:

1. **Obsidian/markdown primitive or generic noun** (`wikilink`, `links`,
   `Source Title`, …) → **prose-ify**: rewrite `[[T]]` → `` `T` `` or plain
   prose. Never a page.
2. **Recurring concept backed by an ingested source** (e.g. `Search Score
   Object` → its `_sources/` ADR summary) → **create a substantive typed page**
   in the right cluster, grounded in that source, all template sections filled.
3. **Name/alias mismatch to an existing page** → **curator** rewrites the link
   (or adds `T` to the page's `aliases:`).
4. **Recurring concept, substantive, no page yet** → create a `derived: true`
   page citing the pages that reference it.
5. **True one-off, not substantive** → **prose-ify**.

### Quality gates (asserted in Phase G)

- `danglingCount == 0` — no empty links (the definition of "no empty pages").
- `engine verify` → `errors == 0 && warnings == 0`.
- `Cn ≥ 0.85` — ≥85% of topic pages sit in the 7 core clusters (node concentration).
- `Ce ≥ 0.85` — ≥85% of wikilink edges have both endpoints in the clusters
  (edge concentration — the faithful "majority of edges around the topics").
- Each hub page has filled body sections and ≥5 outbound links.

`Ch` (the fraction of edges touching a hub *node*) is reported for insight but
not gated — in a densely cross-linked vault it sits well below `Cn`/`Ce`.

If a gate fails the workflow reports which one and the offending phase's
checkpoint SHA — **never fabricate links to pass a gate**; surface instead.

## Procedure (materialize, then run)

1. **Resolve the vault and repo.** Source `scripts/resolve-vault.sh`; the repo
   root is the git toplevel of the resolved vault.
2. **Materialize the workflow.** Ensure `<project>/.claude/workflows/` exists and
   copy the bundled `${CLAUDE_PLUGIN_ROOT}/skills/fill-gaps/template/fill-knowledge-gaps.mjs`
   there **if absent or content-different**. If a user-modified copy exists with
   different content, do **not** overwrite — write
   `fill-knowledge-gaps-from-plugin.mjs` alongside it and tell the user. Identical
   content → no-op.
3. **Run it** via the Workflow tool, pointing at the materialized script and
   passing the resolved paths:
   `Workflow({ scriptPath: "<project>/.claude/workflows/fill-knowledge-gaps.mjs",
   args: { repoDir: "<repo root>", vault: "<absolute vault path>" } })`.
4. **Report** the workflow's `return` payload: baseline → final dangling count,
   `Cn`/`Ch`, verify status, and the per-cluster breakdown. Surface any failed
   gate with its checkpoint SHA.

## Reading & writing contract

- **Reads:** the bundled `template/` (always the plugin-cache path, never a
  project copy), `scripts/graph-quality.sh`, `scripts/tree-lint.sh`, the engine,
  and the resolved vault.
- **Writes:** `<project>/.claude/workflows/fill-knowledge-gaps.mjs` (materialize
  step only) and — through the agents it dispatches — the resolved vault under
  git checkpoints. It never writes another vault and never edits `raw/` existing
  files (it only `cp`s new sources in).

## Related

- `/claude-wiki-pages:ingest`, the ingest agent — Phases B/C/D/E.
- `/claude-wiki-pages:fix` and the curator agent — Phase D/F.
- `/claude-wiki-pages:lint` and `scripts/graph-quality.sh` — the gap detectors.
- `scripts/tree-lint.sh` (detector) + `scripts/strict-tree-reduce.sh`
  (remediation) — the strict-tree (ADR-0036) power-user direct path: report and
  then demote every non-spine edge so the graph draws only the `parent:` spine.
  Phase F's `polish` agent already runs the reducer; run these directly for a
  targeted reshape outside a full fill-gaps pass.
- `/claude-wiki-pages:wiki` — routes "complete the wiki" intent here.
