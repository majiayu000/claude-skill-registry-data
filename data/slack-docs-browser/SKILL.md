---
name: slack-docs-browser
description: Search, fetch, and convert Slack Developer Docs pages from https://docs.slack.dev into clean markdown files for local grep and analysis. Use when you need to browse Slack developer documentation, locate relevant pages by keyword, or extract a page's content into a temporary file.
---

# Slack Docs Browser

## Overview

Search the Slack Developer Docs sitemap and fetch individual pages as markdown using a bundled script that strips navigation and keeps the main content.

## Quick start

Search by keyword in URLs:

```bash
python3 scripts/slack_docs.py search "oauth" --limit 10
```

Fetch a page (path or full URL) into a temp file and print the file path:

```bash
python3 scripts/slack_docs.py fetch /tools/python-slack-sdk/
```

Grep locally:

```bash
rg -n "scopes" /tmp/slack-docs-*.md
```

## Commands

### Search sitemap URLs

Use the sitemap index to find candidate pages quickly.

```bash
python3 scripts/slack_docs.py search "socket mode"
python3 scripts/slack_docs.py search "chat\\.postMessage" --regex
python3 scripts/slack_docs.py search "blocks" --limit 5 --refresh
```

Notes:
- `--refresh` re-downloads the sitemap to include recent pages.
- Search is URL-based; use broader terms if the URL is short.

### Cache control

Control where the sitemap cache is stored.

```bash
SLACK_DOCS_CACHE_DIR=/tmp/slack-docs-cache python3 scripts/slack_docs.py search "events"
python3 scripts/slack_docs.py --cache-dir /tmp/slack-docs-cache search "events"
```

### Fetch page content as markdown

Extract the main doc content (`div.theme-doc-markdown`) and convert to GitHub-flavored markdown.

```bash
python3 scripts/slack_docs.py fetch /reference/methods/chat.postMessage
python3 scripts/slack_docs.py fetch https://docs.slack.dev/tools/python-slack-sdk/ --out /tmp/python-sdk.md
python3 scripts/slack_docs.py fetch /workflows/ --stdout > /tmp/workflows.md
```

## Troubleshooting

- If `pandoc` is missing, install it and rerun the fetch command.
- If the main content is empty or missing, try a different URL or fetch the full page and inspect the HTML for changes in the doc structure.
- If `bs4` is missing, install `beautifulsoup4` for Python or use a system package.

## Resources

- `scripts/slack_docs.py`: Search the Slack docs sitemap and fetch pages as markdown.
