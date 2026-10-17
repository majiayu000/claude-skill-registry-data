---
name: maintain-llm-wiki
description: Maintain a compounding LLM wiki that integrates immutable sources into an interlinked, agent-owned knowledge base. Use when setting up a persistent markdown wiki, ingesting sources into it, answering or filing cited wiki queries, or linting the wiki for contradictions, staleness, gaps, and broken links.
disable-model-invocation: true
---

# Maintain LLM Wiki

Treat the wiki as compiled knowledge: integrate each source once, then keep the resulting pages current as sources and questions accumulate.

## Operating contract

- Let the human curate sources, direct the analysis, choose the review mode, and approve material schema changes. Let the agent own the wiki maintenance.
- Resolve the read-only source roots, agent-owned wiki root, and governing schema before editing.
- Compile only immutable local snapshots. For a mutable URL or remote object, follow the schema's authorized intake workflow or ask the human to add a snapshot; treat the captured version as read-only evidence.
- Identify every source and immutable version before ingestion. Detect duplicates and resumptions before creating pages.
- Integrate reusable knowledge into the existing graph instead of stopping at a source summary.
- Preserve a claim-local evidence chain from every material factual claim through an evidence record and exact locator to the immutable raw snapshot.
- Surface contradictions with both claims and their citations. Preserve uncertainty until the evidence resolves it.
- Treat the schema as a living human-agent agreement. Propose focused revisions when repeated patterns, corrections, or scale make an existing rule inadequate.

## Route the operation

1. Read the nearest governing agent instructions, then the wiki schema, `index.md`, and log entries relevant to the current inputs or recent work.
2. Select the requested branch:
   - **Set up or reshape the wiki:** read [references/setup.md](references/setup.md). Also use this branch before another operation when no schema exists.
   - **Ingest one or more sources:** read [references/ingest.md](references/ingest.md).
   - **Answer a question or file a durable analysis:** read [references/query.md](references/query.md).
   - **Report on or repair wiki health:** read [references/lint.md](references/lint.md).
3. When one request spans branches, run them in dependency order: setup → ingest → query → lint.

## Maintain shared records

Apply these rules in every branch. Let the schema add domain-specific metadata without weakening them.

- Keep `index.md` as the content map. List every in-scope wiki page with a link and current one-line description, grouped by the domain's page model. Refresh entries after creation, rename, removal, or a meaning-changing revision. Keep the index useful for humans even when search tooling is added.
- Keep `log.md` as append-only operation history. Assign an operation ID before the first write; reuse it on resumed attempts.
- Start each entry with `## [YYYY-MM-DD] <operation> | <operation-id> | <subject>`. Record the attempt, terminal status (`complete`, `partial`, or `blocked`), workflow mode, inputs, pages changed, per-source dispositions when applicable, contradictions, gaps, and proposed schema changes.
- Append one terminal entry per execution attempt unless the human explicitly requests a zero-write audit. Preserve earlier entries; let immutable evidence records and their integration status act as per-source batch checkpoints.

## Finish the operation

1. For write operations, bring `index.md` into agreement with the completed branch work.
2. Validate every created or changed local link, claim-local evidence link, raw locator, and recorded source version. Confirm that source snapshots remain unchanged.
3. Append the terminal `log.md` entry unless this is an explicitly zero-write audit. For a partial or blocked batch, list completed and pending source versions so a later attempt can resume safely.
4. Report pages changed, checkpoint status, unresolved evidence or contradictions, and decisions that need human judgment.

Declare success only when the branch criterion and every applicable shared check pass.
