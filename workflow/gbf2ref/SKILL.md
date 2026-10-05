---
name: gbf2ref
description: Use when working with GenBank format files and need to create reference indexers for sequence data retrieval or processing within the Entrez Direct toolkit.
disable-model-invocation: true
user-invocable: true
---

# gbf2ref

## Quick Start

- **Command**: `gbf2ref < records.gbf > ref_index.xml`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/gbf2ref`
- **Full reference**: See `references/help.md` for detailed documentation

## When To Use This Tool

- Convert GenBank flatfiles into the reference-indexer form expected by EDirect's `transmute -g2r` path.
- Prepare GenBank-derived reference structures for downstream lookup or transformation steps.
- Keep reference-index creation inside the EDirect pipeline rather than writing a custom parser.

## Common Patterns

```bash
# 1) Create a reference-index stream from GenBank input
gbf2ref < records.gbf > ref_index.xml
```

```bash
# 2) Inspect the generated reference-index structure on a small sample
gbf2ref < records.gbf | sed -n '1,40p'
```

## Recommended Workflow

1. Start from a representative GenBank flatfile stream.
2. Run `gbf2ref` via stdin redirection or a pipe.
3. Inspect the emitted structure on a small sample before batching.
4. Pass the generated reference-index stream to the next EDirect stage once it looks right.

## Guardrails

- This wrapper is only `transmute -g2r`, so the real behavior lives inside `transmute`.
- `--help` and `--version` do not produce custom docs; in the current build they fall through to the generic “Unable to create GenBank reference indexer” error.
- Prefer stdin or pipes over undocumented positional-file behavior.
- Validate output on a representative sample before depending on the exact structure in automation.
