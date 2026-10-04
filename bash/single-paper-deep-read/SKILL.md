---
name: single-paper-deep-read
description: Use when the user wants an agent to create or update a project-local source/paper note from a PDF, URL, arXiv, DOI, manual source, or Zotero item.
argument-hint: "<project> <paper-id> <source>"
---

# Single Paper Deep Read

Create or update a project-local source/paper note:

```text
wiki/projects/<Project>/papers/<paper-id>/index.md
```

If the dossier does not exist, create it with:

```bash
python3 "$PLUGIN_ROOT/tools/paper_dossier_cli.py" create --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --paper "$PAPER_ID" --title "$TITLE"
```

Then fill the note with source identity, key claims, evidence, methods, assumptions, limitations, project relevance, and project impact. If project understanding changes, record a normal project memory update. Use graph delta proposals only in strict review mode.
