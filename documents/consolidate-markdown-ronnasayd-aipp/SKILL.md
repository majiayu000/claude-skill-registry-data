---
name: consolidate-markdown
description: "Consolidate several unstructured Markdown files with overlapping or conflicting information into one organized document, without losing data and with every divergence made explicit. Use when user says 'consolidar arquivos markdown', 'juntar essas notas', 'merge these md files', 'unify these docs', 'notas duplicadas/divergentes', or has multiple .md notes (Obsidian, Notion exports, scattered docs) covering the same topics with inconsistent details, even if they don't say 'consolidate'."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

# Consolidate Markdown

Merge messy `.md` files into one coherent document. Rule: **no info lost, no conflict silently resolved**. Keep source traceability until the final step — it's what makes divergences resolvable. Never edit originals.

Ask (`AskUserQuestion`) only what can't be inferred: files/glob, output path (default `consolidado.md` beside sources), output language, keep/drop frontmatter.

## Steps

| #   | Step        | Action                                                                                                                                                                             | Gate                                                                              |
| --- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1   | Prepare     | UTF-8 + LF (`file -i`, `iconv -f <enc> -t utf-8`, `sed -i 's/\r$//'`). Frontmatter keep/drop per user; if kept, move date/tags into origin header                                  | work on copy; accents intact                                                      |
| 2   | Concatenate | Oldest first (frontmatter date or mtime) so contradictions read as updates; origin header per file (snippet below); exclude output file from glob                                  | draft with `# Origem: <file>` per block                                           |
| 3   | Unify       | Read full draft → propose 5–12 macro-themes (confirm if split non-obvious) → move blocks under themes, keep wording, tag `<!-- src: file.md -->` → mark conflicts (template below) | every block under a theme; every conflict marked                                  |
| 4   | Refine      | Resolve per table below; dedupe; one H1; consistent lists/tables; working links. Strip `src` comments and `# Origem` only after user approves                                      | unresolved → final `## Pendências`                                                |
| 5   | Verify      | Each source's distinct facts appear in output or `Pendências`; grep (`rg -c`) unusual terms/numbers/names per source                                                               | report: files merged, themes, dupes collapsed, divergences found/resolved/pending |

```bash
out=consolidado_rascunho.md; : > "$out"
for f in *.md; do printf '\n\n# Origem: %s\n\n' "$f" >> "$out"; cat "$f" >> "$out"; done
```

```markdown
> ⚠️ **Divergência:** prazo do projeto
>
> - `notas_v1.md`: 30 dias
> - `reuniao_03.md`: 45 dias
>
> **Decisão:** _pendente_
```

## Conflict handling

| Case                         | Action                                                                              |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| Same fact, same value        | collapse to one line, list all sources                                              |
| Same fact, different wording | not a conflict — merge                                                              |
| Different values             | mark divergence; resolve by newer date, more authoritative source, or user decision |
| Resolved                     | record chosen value + why; keep rejected value as one-line note if it could matter  |
| Unresolvable                 | leave in `## Pendências`                                                            |
| >10 divergences              | also list in reply grouped by theme for one-pass decision                           |

## Output

Final `.md`: TOC, themed sections, `Pendências`; short summary to user.
