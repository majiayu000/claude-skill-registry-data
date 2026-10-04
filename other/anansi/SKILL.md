---
name: anansi
description: Use the reviewed Anansi adaptive web scraping framework for authorized web fetch, extraction, crawl, selector healing, browser rendering, screenshot, and MCP-driven scraping workflows. Use when the user mentions Anansi, self-healing selectors, adaptive scraping, anti-bot scraping, crawler repair, crawl_site, or LLM-driven crawling.
license: Apache-2.0
source: https://github.com/mdowis/anansi
source_path: ~/.hermes/external-repos/anansi
security_review: high_capability_network_tool
---

# Anansi

Use this skill for authorized adaptive web scraping with the reviewed Anansi source tree.

## Scope

- Source root: `~/.hermes/external-repos/anansi`.
- Package name: `anansi-scraper`; import package: `anansi`.
- Capabilities: HTTP fetch, browser rendering, adaptive selector healing, crawl queue, structured extraction, screenshots, exports, and MCP server tools.

## Safety Rules

- Only scrape sites the operator is authorized to access.
- Respect robots.txt, target terms, rate limits, privacy law, and data rights.
- Do not start the MCP server, run browser automation, install Playwright browsers, configure proxies, or enable TLS/anti-bot impersonation unless the user explicitly asks for that operation.
- Do not enable `ANANSI_ALLOW_PRIVATE_NETWORKS=1` unless the user explicitly requests it for a trusted isolated host.
- Prefer `ANANSI_DISABLE_ANTIBOT=1` for ordinary fetch/extract use unless the user explicitly asks for authorized anti-bot handling.
- Keep exports confined to the working project or Anansi's `~/.anansi/exports/` path.

## Install When Needed

Use a local virtual environment in the user's working project:

```bash
. ~/.hermes/skills/devops/anansi/.venv/bin/activate
```

Browser support is separate and should be explicit:

```bash
playwright install chromium
```

TLS impersonation support is separate and should be explicit:

```bash
pip install "~/.hermes/external-repos/anansi[tls]"
```

## First Probes

```bash
ANANSI_DISABLE_ANTIBOT=1 ~/.hermes/skills/devops/anansi/.venv/bin/python -m anansi --help
ANANSI_DISABLE_ANTIBOT=1 ~/.hermes/skills/devops/anansi/.venv/bin/python -m anansi.mcp_server.server --help
```

## Common Commands

```bash
ANANSI_DISABLE_ANTIBOT=1 ~/.hermes/skills/devops/anansi/.venv/bin/anansi fetch https://example.com --output markdown
```

```bash
ANANSI_DISABLE_ANTIBOT=1 ~/.hermes/skills/devops/anansi/.venv/bin/anansi mcp
```
