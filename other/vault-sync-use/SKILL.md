---
name: vault-sync-use
description: Use when the user wants an AI agent to answer questions or perform research from an already-synced Vault folder using local Markdown files and normal filesystem tools.
---

# Vault Sync Use

Use an already-synced Vault as local, read-only context. Vault Sync provides files; the agent does the reading and reasoning.

## Workflow

1. If `vault-sync` is available and the user has not asked to avoid updates, refresh the Vault:

```bash
vault-sync pull <path>
```

2. Read `<path>/README.md` first to learn the Vault source and conventions.
3. Ignore hidden control folders: `.git`, `.zine`, `.dossium`, `.graphlit`, `.claude`, and `.codex`.
4. Search and read Markdown directly with normal filesystem tools:

```bash
rg -n "<terms>" <path>
ls <path>
sed -n '1,160p' <file>
```

5. Cite local file paths in responses when useful.

## Boundaries

- Do not call app APIs for Vault consumption.
- Do not use `vault-sync` for search, query, read, summarize, rank, or index.
- Do not edit generated Vault files unless the user explicitly asks for local modifications.
- If QMD is installed, it can be an optional local search helper. Add the Vault folder with `qmd collection add <path> --name <name> --mask "**/*.md"`, add context with `qmd context add qmd://<name> "Local Vault synced by Vault Sync"`, then run `qmd embed`. Use QMD to find likely files and local file reads for the full source. Do not require QMD.
