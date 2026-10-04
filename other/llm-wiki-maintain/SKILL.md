---
name: llm-wiki-maintain
description: Routine maintenance and safe commits. Use when committing changes, rebuilding indexes, or checking overall vault health.
---

# LLM Wiki Maintain

Keep the vault healthy and every commit clean.

## Maintenance Gate (before every meaningful commit)

```bash
python scripts/wiki_tool.py doctor
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

After source ingestion, also run:

```bash
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
```

All commands must pass before committing.

## Routine Tasks

- **Coverage review:** `python scripts/wiki_tool.py source-coverage` shows
  which Raw sources are covered by Wiki notes; `source-delta` shows sources
  missing from the manifest.
- **Index rebuild:** `build` regenerates `Wiki/catalog.jsonl`, `Wiki/index.md`,
  and per-folder indexes. Commit the regenerated artifacts.
- **Logging:** record meaningful changes with
  `python scripts/wiki_tool.py log --title "..." --details "..."`.
- **Hooks:** `scripts/install_hooks.sh` points git at `.githooks/` so the
  pre-commit hook runs the full gate (doctor, build, lint, source-lint,
  audit_public) automatically.

## Rules

- Never commit with failing checks.
- Never commit secrets, machine-local paths, or plugin/cache state —
  `scripts/audit_public.py` guards this; take its failures seriously.
- Keep commits scoped: content changes and generated artifacts may share a
  commit, but unrelated changes should not.
