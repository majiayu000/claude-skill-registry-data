---
name: paper-discovery-intake
description: Use when the user wants to add source identity from PDF, URL, arXiv, DOI, note, experiment result, manual reference, or Zotero item into a Research Pilot project.
argument-hint: "<project> <source>"
---

# Source Intake

Create project-local source identity without forcing a paper-manager workflow.

Accepted source types:

- PDF path;
- URL;
- arXiv link;
- DOI;
- Markdown note;
- experiment result;
- manual reference;
- Zotero item.

Use Zotero identity when available, but do not require it for first-run value.

Agent-internal CLI examples:

```bash
python3 "$PLUGIN_ROOT/tools/source_intake_cli.py" intake --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --paper "$PAPER_ID" --title "$TITLE" --zotero-key "$ZOTERO_ITEM_KEY" --json
```

```bash
python3 "$PLUGIN_ROOT/tools/source_intake_cli.py" intake --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --paper "$PAPER_ID" --title "$TITLE" --doi "$DOI" --url "$URL" --json
```

This skill records durable source identity. Zotero is a supported adapter, not the product identity.
