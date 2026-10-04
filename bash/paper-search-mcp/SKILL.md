---
name: paper-search
description: Search, download, and read academic papers from 20+ sources (arXiv, PubMed, Semantic Scholar, CrossRef, OpenAlex, etc). Use when the user asks to find papers, search academic literature, look up research papers, download a paper PDF, or extract text from a paper.
---

# Paper Search

Search, download, and read academic papers via the `paper-search` CLI from the local source clone.

Local source clone:

```bash
~/.hermes/external-repos/paper-search-mcp
```

## CLI Usage

All commands run via:

```bash
uv run --directory ~/.hermes/external-repos/paper-search-mcp paper-search <command> [args]
```

### Search

```bash
uv run --directory ~/.hermes/external-repos/paper-search-mcp paper-search search "<query>" -n <max_per_source> -s <sources> -y <year>
```

- `-n`: results per source (default: 5)
- `-s`: comma-separated sources or `all` (default: all)
- `-y`: year filter for Semantic Scholar, for example `2020` or `2018-2022`

For speed and cleaner evidence, prefer targeted sources such as `-s arxiv,semantic,crossref,openalex` over `all` unless broad coverage is needed.

### Download PDF

```bash
uv run --directory ~/.hermes/external-repos/paper-search-mcp paper-search download <source> <paper_id> [-o ./downloads]
```

### Read

```bash
uv run --directory ~/.hermes/external-repos/paper-search-mcp paper-search read <source> <paper_id> [-o ./downloads]
```

### List Sources

```bash
uv run --directory ~/.hermes/external-repos/paper-search-mcp paper-search sources
```

## Output

`search` and `download` return JSON. `read` returns plain text. Config warnings go to stderr and can be ignored.

## Sources

arxiv, pubmed, biorxiv, medrxiv, google_scholar, iacr, semantic, crossref, openalex, pmc, core, europepmc, dblp, openaire, citeseerx, doaj, base, zenodo, hal, ssrn, unpaywall

Optional env vars can enable or improve sources:

- `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL`
- `PAPER_SEARCH_MCP_CORE_API_KEY`
- `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY`
- `PAPER_SEARCH_MCP_GOOGLE_SCHOLAR_PROXY_URL`
- `PAPER_SEARCH_MCP_DOAJ_API_KEY`
- `PAPER_SEARCH_MCP_ZENODO_ACCESS_TOKEN`
- `PAPER_SEARCH_MCP_IEEE_API_KEY`
- `PAPER_SEARCH_MCP_ACM_API_KEY`

The package auto-loads `.env` from the current directory or the local repo root, and supports `PAPER_SEARCH_MCP_ENV_FILE` for an explicit env file path.

## Workflow

1. Search with targeted sources to find papers.
2. Present results as a table: title, authors, year, source, DOI/URL.
3. If the user wants full text, use `read <source> <paper_id>`.
4. If the user wants the PDF, use `download <source> <paper_id>` and report the saved path.

## Safety Notes

- This skill uses the CLI path only, not MCP server setup.
- Search commands make outbound requests to academic services.
- Download/read commands write files under the requested `-o` directory, defaulting to `./downloads`.
- The source repo contains optional MCP fallback code with Sci-Hub support; do not run MCP server fallback flows or enable Sci-Hub-style retrieval unless the user explicitly asks and accepts the legal/access risk.
