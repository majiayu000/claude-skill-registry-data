---
name: coda-ai
description: CLI to read Coda.io documents and pages. List docs, list pages, read content in markdown/json/html.
homepage: https://www.npmjs.com/package/coda-ai
metadata: {"openclaw":{"requires":{"bins":["coda-ai"]},"install":[{"id":"node","kind":"node","package":"coda-ai","bins":["coda-ai"],"label":"Install coda-ai (npm)"}]}}
---

# coda-ai

CLI to read Coda.io content for AI agents.

## Workflow

1. **docs** → list all documents
2. **pages** → list pages in a doc
3. **read** → get page content

## Setup (once)

```bash
npm install -g coda-ai
coda-ai auth # interactive setup
coda-ai whoami # verify auth
```

## Commands

### List Documents

```bash
coda-ai docs --compact        # only id + name in toon format (recommended for AI Agents)
coda-ai docs                  # full data in toon format
coda-ai docs --format json    # full data in json
coda-ai docs --format table   # human-readable table
```

Returns: All docs sorted by most recent update. Use `id` field for next step.

### List Pages

```bash
coda-ai pages --docId <docId> --compact        # only id + name, toon format (recommended for AI Agents)
coda-ai pages --docId <docId> --format json    # full data in json
coda-ai pages --docId <docId> --format tree    # visual tree
coda-ai pages --docId <docId>                  # full data in toon format (default)
```

Returns: Page hierarchy. Use `pageId` for next step.

### Read Content

```bash
coda-ai read --docId <docId> --pageId <pageId>  # markdown (default, recommended for AI Agents)
coda-ai read --docId <docId> --pageId <pageId> --format json    # structured data in json
coda-ai read --docId <docId> --pageId <pageId> --format html    # html export
```


## Reference

Full docs: https://github.com/auniik/coda-ai
