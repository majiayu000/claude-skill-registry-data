---
name: open-coscientist
description: "Open-source AI Co-Scientist based on Google Research — PubMed literature search, INDRA knowledge graph, hypothesis generation. From jataware/open-coscientist"
version: 1.0.0
author: jataware, adapted for Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scientist, research, literature, pubmed, hypothesis, biology, biomedical]
    triggers: [scientist, research, literature-review, pubmed, biomedical, hypothesis, paper-search, academic]
    related_skills: [ai-scientist, gpt-researcher, arxiv]
---

# Open Coscientist

## Overview

Open-source adaptation of Google Research's AI Co-Scientist paper, providing an MCP server with:
- **PubMed search** — search biomedical literature with full-text extraction
- **INDRA CoGex knowledge graph** — query gene-disease networks, drug info, clinical trials, pathways, enrichment analysis
- **Hypothesis generation** — multi-agent architecture that generates, reviews, ranks, and evolves research hypotheses

## Setup

### Prerequisites
- Docker and Docker Compose
- NCBI Entrez email (free, for PubMed API)

### Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/jataware/open-coscientist.git
   cd open-coscientist
   ```

2. Configure environment:
   ```bash
   cp mcp_server/.env.example mcp_server/.env
   # Edit mcp_server/.env:
   #   ENTREZ_EMAIL=your_email@example.com
   #   ENTREZ_API_KEY=your_key  (optional but recommended)
   ```

3. Start the MCP server:
   ```bash
   docker compose up -d
   ```

4. Verify it's running:
   ```bash
   curl http://localhost:8888
   # → {"status":"running","service":"coscientist-lit-review","version":"0.1.0","mcp_tools":[...]}
   ```

## Hermes MCP Configuration

Add to your `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  coscientist:
    url: "http://localhost:8888/mcp"
    transport: streamable-http
    timeout: 120
    connect_timeout: 30
```

**Why streamable-http:** The coscientist server sets `stateless_http = True` and uses `mcp.http_app()` with streamable-http transport. Its MCP endpoint is at `/mcp`, not `/sse`. This is the correct transport for this server — do not change it to `sse`.

## Available MCP Tools

Once configured, these tools become available to Hermes:

| Tool | Purpose |
|------|---------|
| `check_pubmed_available` | Test PubMed service connectivity |
| `search_pubmed` | Search PubMed by query terms |
| `pubmed_search_with_fulltext` | Search PubMed + download full text from PMC |
| `query_gene_disease_network` | Query gene-disease associations |
| `query_gene_codependents` | Find genes that co-depend with a target gene |
| `query_drug_info` | Look up drug information |
| `query_clinical_trials` | Search clinical trials |
| `query_pathways` | Query biological pathways |
| `query_causal_subnetwork` | Query causal subnetwork |
| `query_mechanistic_statements` | Get mechanistic statements |
| `run_enrichment_analysis` | Run enrichment analysis |

## When to Use

- Biomedical literature searches
- Drug discovery research
- Gene-disease network analysis
- Clinical trial investigation
- Hypothesis generation and testing
- Academic paper synthesis
- Scientific literature review

## Pitfalls

- PubMed API requires an Entrez email — without it, requests may be rate-limited
- Docker container must be running for the MCP server to be available
- INDRA CoGex queries on large networks can be slow (timeout handled up to 60s)
- Paper cache stored at `./mcp_server/paper_cache/`
