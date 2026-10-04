---
name: paper-review-source-intel
description: Route first-source academic paper and peer-review intelligence collection, crawling, normalization, and synthesis through public official sources by default. Use when Codex needs a no-required-MCP/no-required-API-key closure for papers, proceedings metadata, public OpenReview visibility, open-access PDFs, citation/author enrichment, or auditable evidence corpora from arXiv, OpenReview public pages, ACL Anthology, CVF, PMLR, NeurIPS proceedings, ACM DL, IEEE CSDL/Xplore, IACR TCHES, Semantic Scholar, OpenAlex, Crossref, Unpaywall, or optional paper-search-mcp.
---

# Paper Review Source Intel

## Overview

Use this skill for first-source paper and peer-review evidence collection. The default closure uses public official pages/APIs, proceedings, and open metadata before general web search or unofficial crawlers. It must remain usable without required MCP servers, paid services, private credentials, or login-gated review data.

If the user asks to configure the "complete", "full", or MCP-enabled setup, read `references/full-setup.md` and actively configure what can be made usable without secrets: isolated `openreview-py` and `acl-anthology` runtimes, optional `paper-search-mcp` runtime, and `paper_search_mcp` stdio registration when requested or clearly implied. Credentials, login-visible data, external OpenReview knowledge MCP URLs, proxies, paid connectors, and Sci-Hub-like fallbacks require explicit opt-in.

## Decision Tree

1. Identify the target:
   - topic or keyword paper search;
   - venue/year accepted-paper corpus;
   - OpenReview forum, venue, reviews, meta-review, rebuttal, decision, or score distribution;
   - arXiv ID, DOI, ACL Anthology ID, CVF/PMLR/NeurIPS URL;
   - author/citation enrichment;
   - PDF/full-text acquisition.
2. Run a route plan before installing or crawling:

```powershell
python skills\paper-review-source-intel\scripts\paper_review_source_intel.py plan `
  --target "ICLR 2025 retrieval augmented generation" `
  --venue ICLR `
  --year 2025 `
  --needs papers,reviews,decisions,pdfs,report
```

3. Execute only the required lane:
   - OpenReview reviews/decisions/rebuttals: capture public OpenReview visibility first; use `openreview-py` only as an optional local library.
   - Broad paper corpus and OA PDFs: use public arXiv, Crossref, OpenAlex, Semantic Scholar, Unpaywall, and official proceedings first; `paper-search-mcp` is optional.
   - Official proceedings: use ACL Anthology, CVF Open Access, PMLR, NeurIPS proceedings, ACM DL, IEEE CSDL/Xplore, IACR TCHES, or arXiv API directly.
   - Architecture/FPGA/EDA/circuits/ML/data-engineering/cryptographic-hardware venues: crawl MICRO, ISCA, ASPLOS, HPCA, FPGA, FCCM, ICCAD, DAC, DATE, TCAD, ISSCC, ICML, TKDE, or TCHES sources only when the user names the venue or states a clearly related direction.
   - Citation/author/topic enrichment: use OpenAlex and Semantic Scholar as secondary metadata backbones.
4. Keep raw captures and normalized outputs separate. Synthesize from normalized artifacts, not from browser state or loose snippets.

## Full Local Setup

For a complete no-secret local setup:

```powershell
powershell -ExecutionPolicy Bypass -File skills\paper-review-source-intel\scripts\setup_paper_review_source_intel.ps1 -RunNetworkSmoke
```

For an MCP-enabled setup, register the public-source `paper_search_mcp` stdio server too:

```powershell
powershell -ExecutionPolicy Bypass -File skills\paper-review-source-intel\scripts\setup_paper_review_source_intel.ps1 -RunNetworkSmoke -RegisterPaperSearchMcp
```

This installs isolated global-skill runtimes when the skill is installed under `%USERPROFILE%\.codex\skills\paper-review-source-intel`. It does not write real credentials. After MCP registration, verify with `codex mcp list`; a running Codex session may need restart before new MCP tools appear.

## Source Routing

Read `references/source-routing.md` before choosing a backend.

- Use public OpenReview pages/visible notes first for public reviews, scores, meta-reviews, rebuttals, decisions, venue stats, and rejection/weakness-pattern analysis.
- Use official proceedings first for accepted-paper lists: ACL Anthology for ACL/EMNLP/NAACL, CVF for CVPR/ICCV/WACV, PMLR for ICML/AISTATS/COLT, NeurIPS proceedings for NeurIPS accepted papers, ACM DL / IEEE CSDL / IEEE Xplore for relevant architecture, FPGA, EDA, and circuits venues, IACR TCHES for cryptographic hardware articles, and arXiv for preprints.
- Do not crawl MICRO, ISCA, ASPLOS, HPCA, FPGA, FCCM, ICCAD, DAC, DATE, TCAD, ISSCC, ICML, TKDE, or TCHES by default for unrelated topics. Add them only when the user names them or the research direction clearly matches the venue family.
- Use public arXiv, Crossref, OpenAlex, Semantic Scholar, Unpaywall, and proceedings pages for multi-source literature search, DOI recovery, and open-access PDF resolution by default.
- Use `paper-search-mcp` only as an optional convenience layer after the public-source closure is understood.
- If `paper_search_mcp` is registered, prefer its public arXiv/PubMed/bioRxiv/medRxiv tools for breadth; do not use its Google Scholar or download/read tools as canonical evidence without checking access/licensing and recording provenance.
- Use Semantic Scholar/OpenAlex for enrichment and cross-checking, not as the only source for official venue decisions.
- Use general crawlers only as a fallback when official pages are static but lack an API.

## Common Commands

Inspect a URL and infer the source lane:

```powershell
python skills\paper-review-source-intel\scripts\paper_review_source_intel.py inspect-url `
  "https://openreview.net/forum?id=abc123"
```

Print the normalized artifact contract:

```powershell
python skills\paper-review-source-intel\scripts\paper_review_source_intel.py schema
```

Check or repair the safe default runtime:

```powershell
powershell -ExecutionPolicy Bypass -File skills\paper-review-source-intel\scripts\setup_paper_review_source_intel.ps1
```

Generate a run scaffold:

```powershell
python skills\paper-review-source-intel\scripts\paper_review_source_intel.py scaffold `
  --output-dir output\paper_review_sources\iclr2025_rag `
  --target "ICLR 2025 RAG" `
  --venue ICLR `
  --year 2025 `
  --needs papers,reviews,decisions,pdfs,report
```

Normalize a raw JSON/JSONL capture:

```powershell
python skills\paper-review-source-intel\scripts\paper_review_source_intel.py normalize `
  --input output\paper_review_sources\iclr2025_rag\raw\openreview.json `
  --source openreview `
  --output-dir output\paper_review_sources\iclr2025_rag\normalized
```

## Output Contract

Use this directory shape for substantial runs:

- `raw/`: untouched source captures, API JSON, scraped HTML, PDFs, and logs.
- `normalized/papers.jsonl`: normalized paper/submission/proceedings rows.
- `normalized/reviews.jsonl`: normalized review, meta-review, rebuttal, and decision rows.
- `normalized/artifacts.jsonl`: downloaded PDFs, extracted text, BibTeX, screenshots, and other local files.
- `sources.csv`: source review table with URL, source type, source priority, and status.
- `manifest.json`: plan, commands, timestamps, limits, credentials policy, and blockers.
- `summary.md`: human-facing synthesis with links back to normalized source IDs.

Read `references/output-schema.md` before merging multiple sources.

## Guardrails

- Prefer first-party APIs and official proceedings over Google Scholar, search snippets, or aggregator pages.
- Default work must remain useful without MCP, paid services, private credentials, or login-only review data.
- Do not use Google Scholar or SerpApi as the canonical first source for papers or review evidence.
- Do not bypass paywalls, CAPTCHAs, login gates, private reviews, or venue access controls.
- Do not enable Sci-Hub-like fallbacks, Google Scholar proxy URLs, paid connectors, or private-record credentials as part of the default setup.
- Registering `paper_search_mcp` is allowed for public-source convenience, but using Google Scholar scraping or paper download/read tools must be justified by the task and source-access status.
- Download only open-access or user-authorized PDFs. Record license/access status when known.
- Keep API keys, OpenReview credentials, cookies, proxy URLs, browser storage state, and `.env` files out of git and final answers.
- Preserve `source_url`, `source_id`, `fetched_at`, and source-specific identifiers for every normalized row.
- Treat review data as visibility-dependent. If a public review, rebuttal, or decision is missing, report the access/visibility state instead of inventing a value.
- Run a small smoke crawl before bulk collection and record rate limits or blocked sources in `manifest.json`.

## Resources

- `scripts/paper_review_source_intel.py`: planner, URL inspector, scaffold generator, schema printer, and lightweight normalizer.
- `scripts/setup_paper_review_source_intel.ps1`: safe setup script for isolated `openreview-py`, `acl-anthology`, optional `paper-search-mcp`, and MCP registration.
- `references/full-setup.md`: complete setup matrix, optional MCP boundaries, credentials policy, and smoke tests.
- `references/source-routing.md`: detailed source selection and third-party tool notes.
- `references/output-schema.md`: normalized fields and merge policy.
