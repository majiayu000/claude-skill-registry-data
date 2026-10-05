---
name: governance-check-graph
description: >
  Validate documentation and graph integrity across the repo: the AI-SDLC artifact graph (every artifact declaring a
  `story:` has a valid work-item key, a known phase, and `relates:` links that resolve) AND the
  documentation wiki (no orphan pages, no broken relative links, indexes in sync), and documentation
  house-style (no em-dash characters). Use when the user says "check the artifact graph", "validate the
  artifact links", "lint the docs", "are the doc links broken", "check the wiki", "check for em-dashes",
  before opening a PR that touches docs or graph artifacts, or as the
  governance-check-graph step. It runs the same scripts the CI gates run, so local results match the
  pipeline. Do NOT use to create or fix artifacts, tickets, links, or docs (that is
  elaboration-upsert-user-story / governance-enrich-ticket / governance-author-adr / create-upsert-documentation).
---

# Check graph and docs-wiki integrity

Owned by the **Lead** persona (link integrity). Invoked as `/governance-check-graph`.

Validate that the repo's links are intact and its docs follow house-style - the artifact graph, the
documentation wiki, and the no-em-dash rule - and explain any failures. This is the local face of the
CI gates: it invokes the same shared scripts, so a clean local run means a clean pipeline run.

The conventions enforced are in `docs/ai-sdlc/artifact-graph.md` (the traceability graph) and
`docs/ai-sdlc/docs-wiki.md` (the documentation wiki). Read those for the schemas and rules.

## Run it

Run the repository scripts (cross-tool: Claude Code, Copilot CLI, or a plain shell):

```
pwsh MindNova/toolsCheck-ArtifactGraph.ps1      # traceability graph
pwsh MindNova/toolsCheck-DocsWiki.ps1           # docs wiki: orphans + broken relative links
pwsh MindNova/toolsBuild-DocsIndex.ps1 -Check   # docs wiki: index in sync with the pages
pwsh MindNova/toolsCheck-DocEmDashes.ps1        # docs house-style: no em-dash (U+2014)
```

Pass `-RepoRoot <path>` if you are not at the repository root. These are the same scripts wired (or,
for the docs-wiki checks, planned) into `MindNova/pipelines/Common/code-analysis-pipeline.yml`, so do
not reimplement the checks here; run them and interpret the output. To clear index drift, run
`Build-DocsIndex.ps1` without `-Check` to regenerate the indexes.

## What it checks

**Artifact graph** (`Check-ArtifactGraph.ps1`) - for every artifact under `docs/`, `docs-functional/`,
or `specs/` that declares `story:` in front-matter:
1. `story` is a valid work-item key (e.g. `MN-42`).
2. `phase` is present and one of `discovery | elaboration | create | mature | governance`.
3. Each `relates.*` repo path resolves to a file; each URL is well-formed.
Artifacts without `story:` front-matter are ignored (adoption is incremental).

**Docs wiki** (`Check-DocsWiki.ps1` + `Build-DocsIndex.ps1 -Check`) - over `docs/` and `docs-functional/`:
4. No orphan pages (every page is listed in its layer index or linked by another page; `index.md`,
   `README.md`, and templates are exempt).
5. No broken relative markdown links (links shown inside code spans or fences are ignored).
6. The committed `index.md` files match what the generator would emit (no drift).

**Docs house-style** (`Check-DocEmDashes.ps1`) - over `AGENTS.md`, `docs/`, and `docs-functional/`:
7. No em-dash (U+2014) characters; the house style uses ' - ', commas, colons, or parentheses.

## On failure

The scripts print `file : reason` per violation. Fix per the relevant convention:
- **Artifact graph** (`docs/ai-sdlc/artifact-graph.md`): a valid `story:` key, a known `phase:`, and
  `relates:` paths that exist; if a relation points at something not yet in the repo, add it or correct the path.
- **Docs wiki** (`docs/ai-sdlc/docs-wiki.md`): repoint or create the target of a broken link; add an
  orphan page to its index or link it; for index drift, regenerate with `Build-DocsIndex.ps1`.
- **Docs house-style**: replace each flagged em-dash (the script prints `file:line`) with ' - ', a comma, a colon, or parentheses.

## Guardrails

- **Read-only.** This validates; it does not edit artifacts or create links. Fixing is a separate step.
- Keep the rule in the script (the shared source of truth), not duplicated in this skill, so the local
  check and the CI gate never diverge.

## Next steps

- On a clean result, no further action.
- On a failure, fix with the owning skill and re-run: unresolved `relates:` links -> `/governance-enrich-ticket`; a missing ADR backlink -> `/governance-author-adr`; a malformed `story:` or `phase:` -> correct the artifact's front-matter; a broken doc link, orphan page, or index drift -> `/create-upsert-documentation` (regenerate the index and fix or repoint the links); an em-dash -> replace it with ' - ', a comma, a colon, or parentheses.
