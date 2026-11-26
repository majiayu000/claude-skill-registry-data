---
name: elicit-research
description: "Search academic literature through the Elicit API: papers, clinical trials, reports, systematic reviews and Research Agent sessions. Use when a question needs published evidence or an outside, literature-backed view. Needs your own Elicit API key."
---

# Läseratte (elicit-research)

Use the Elicit API directly through `scripts/elicit.py` (Python 3 standard library plus curl). Resolve script paths relative to this skill folder. Authentication comes from `ELICIT_API_KEY`, then `~/.config/elicit/api-key` with mode 600. Never put credentials in skill files, request JSON, output artifacts, or command arguments. The credential file is local configuration and must not be packaged with the skill. The client reads that file itself, so no export is needed. Each OS user or host needs its own copy with the same restricted permissions.

## Choose the research workflow

- Paper discovery: `POST /search/papers`. Start with a focused natural-language `query` and `maxResults: 10` or 20. Use additional searches to cover terminology and opposing evidence as appropriate.
- Registered trials: `POST /search/trials`; read its schema for `trialFilters`.
- A synthesized research report: `POST /sessions/reports`, using `researchQuestion`; normal defaults retrieve 50 papers and extract 10. Set `isPublic: false` unless public access is requested.
- An explicit systematic review: `POST /sessions/systematic-reviews`. Configure inclusion criteria and extraction questions to match the user's protocol. Read the endpoint schema before constructing the request: omitted stages are skipped. Fulltext screening requires abstract screening; report generation requires extraction.
- Open-ended or iterative investigation: `POST /sessions/agents` with `query`. Follow events and artifacts; continue the same session through its `/messages` endpoint with `message`.

An Elicit research request authorizes appropriate research calls within its scope. Skill setup alone does not request a research run. Keep publication, sharing, and library changes within the user's requested scope. Do not substitute a long-running review for a simple paper lookup.

## Execute and preserve evidence

For difficult technical questions, blocked research hypotheses, or an independent literature-backed perspective, use [technical second-perspective workflow](references/technical-second-perspective.md). Preserve the exact system invariants and turn findings into falsifiable implementation hypotheses.

1. Check `GET /usage` before a substantial new job. Report actual quota limitations; do not enable extra usage or upgrade plans. Usage availability does not establish an exact job price.
2. Save request JSON and complete response JSON in the task workspace. Use `--body request.json --out response.json`. Record query, filters, retrieval date, returned IDs, warnings, and paper identifiers.
3. For asynchronous creation, save the returned session ID and URL immediately. Poll the corresponding typed detail endpoint; never create another session merely because the first is slow. Reports typically take 5–15 minutes. Use separate polls with approximately 20–30 second interruptible waits, keeping the user informed.
4. Handle `processing`, `completed`, `failed`, and `pausedForInsufficientQuota` distinctly. For agents, inspect the events schema for cursor and completion semantics, preserve the cursor, and collect artifacts when the turn finishes. A created session or intermediate artifact is not a completed report. If a bounded polling period ends, return the ID and current state explicitly; resume that ID on continuation.
5. Read the actual results before answering. Cite paper DOI or source URLs and distinguish abstract-only evidence from verified full text. Explain study design, conflicting results, and limitations relevant to the question. Elicit's generated synthesis is not independent verification of the underlying papers. Do not claim an exhaustive systematic review from a handful of semantic-search hits.

## Client examples

```bash
python3 scripts/elicit.py GET /usage
python3 scripts/elicit.py POST /search/papers --body request.json --out papers.json
python3 scripts/elicit.py POST /sessions/reports --body report-request.json --out report-session.json
python3 scripts/elicit.py GET /sessions/reports/RETURNED_ID --out report-status.json
```

Search request example: `{"query":"methods for reducing quantum resources in elliptic curve discrete logarithms","maxResults":10}`.

For a full systematic review with screening, extraction and a report, follow the [systematic review recipe](references/systematic-review-recipe.md) (quota check and request template).

Read [API notes](references/api-notes.md) for limits, failures, and advanced workflows. Inspect only the relevant operation with `METHOD /path --schema`. On first use the client downloads Elicit's public OpenAPI document to `references/api-schema.json` (not committed); later schema lookups stay offline. Verify current [official docs](https://docs.elicit.com/) and [OpenAPI](https://docs.elicit.com/openapi.json) when the API rejects a documented request or a needed feature is absent. Do not guess fields or endpoints.
