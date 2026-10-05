---
name: literature-search
description: Run the canonical literature search bridge for one evidence query and persist traceable evidence artifacts.
---

# literature-search

Goal:

- Run the canonical literature search bridge for one evidence query and persist traceable evidence artifacts.

Inputs:

- active run directory
- a `SearchRequestContract` payload or enough context to build one
- optional existing `literature/queries/<query_id>/REQUEST.json`

Outputs:

- `literature/queries/<query_id>/REQUEST.json`
- `literature/queries/<query_id>/PROVIDER_RECEIPTS.json`
- `literature/queries/<query_id>/CANDIDATE_PAPERS.json`
- `literature/queries/<query_id>/VERIFIED_PAPERS.json`
- `literature/queries/<query_id>/EVIDENCE_BUNDLE.json`
- `literature/queries/<query_id>/EVIDENCE_BUNDLE.md`
- `literature/queries/<query_id>/SEARCH_TRACE.jsonl`
- `literature/bundles/<bundle_id>.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Open `skills/shared-references/literature-search-contract.md`.
- Read `packages/agent_contracts/literature.py` before building or editing a search request or evidence bundle.
- Read `tools/literature_search_client.py` before invoking the bridge.

Execution Contract:

- Import and call `from tools import search_literature`.
- When the host exposes the configured `co_scientist_search_bridge` MCP server, its tools are an allowed transport for the same canonical bridge.
- If the MCP server is unavailable, fall back to the Python tools surface instead of performing informal web search.
- Do not perform informal web search as a substitute for `tools.search_literature(...)`.
- Do not invent papers, DOIs, arXiv IDs, venues, citation counts, or abstracts.
- Preserve provider failure receipts. A failed provider is evidence about retrieval coverage and must not be hidden.
- If `retrieval_metadata.status` is `blocked`, return that blocked state to the caller instead of fabricating an evidence bundle.
- If `retrieval_metadata.status` is `partial`, downstream callers may continue only when they preserve the partial-source limitation.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, `skills/shared-references/literature-search-contract.md`, and `packages/agent_contracts/literature.py`.
2. Build a `SearchRequestContract` with a stable `query_id`, `goal`, `query`, `query_type`, `providers`, `filters`, and `consumer`.
3. Call `tools.search_literature(run_dir, request)` through the stable tools surface, or call the equivalent configured MCP search bridge tool when it is available.
4. Read the returned `EvidenceBundleContract` and confirm the run-local artifacts were written.
5. If the bundle status is `blocked`, stop and report the blocked retrieval state to the caller.
6. If the bundle status is `partial` or `succeeded`, return the `bundle_id` and `query_id` to the caller.
7. Run `python -m tools.validation.contract_validation <run_dir> --skill literature-search`.

Completion Rule:

- This skill is complete only when the search bridge has written a canonical evidence bundle or an auditable blocked retrieval state, and the literature artifacts validate.
