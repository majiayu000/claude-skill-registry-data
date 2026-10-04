---
name: extract-software-requirements
description: Extract and consolidate software requirements from a project's Claude Code session transcripts, git commit history, and spec or PRD markdown files into a single traceable RF-xxx/RNF-xxx requirements document with an explicit unresolved-conflicts section. Use when user says "extract requirements from this project", "generate a requirements doc from commits", "extract requirements from transcripts", "consolidate PRD and specs into one doc", "what requirements were implemented vs still pending", or "audit requirements across conversations, code history, and formal specs".
license: CC-BY-4.0
metadata:
  author: Ronnasayd
  version: 1.1.0
---

# Extract Software Requirements

Mines and consolidates software requirements from three independent sources — session transcripts, commit history, formal specs — into one RF-xxx/RNF-xxx requirements doc with a dedicated conflicts section.

Each phase below is independent — run only what's requested. "Requirements from commits" = Phase 2 only, don't force Phase 4 merge with sources that don't exist.

## Phases

| Phase | Source                                                               | Detail                                                                                                                     |
| ----- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1     | Session transcripts (`~/.claude/projects/<url-encoded-cwd>/*.jsonl`) | `references/source-extraction-steps.md` §Phase 1                                                                           |
| 2     | Git commit history                                                   | `references/source-extraction-steps.md` §Phase 2                                                                           |
| 3     | Formal spec/PRD `.md` files                                          | `references/source-extraction-steps.md` §Phase 3                                                                           |
| 3.5   | Test files (only if a test suite exists in the repo)                 | `references/source-extraction-steps.md` §Phase 3.5                                                                         |
| 4     | Consolidate ≥2 phase outputs                                         | `references/merge-and-conflicts.md` (precedence rule, doc structure, ID scheme, status vocabulary, conflict-vs-stale test) |

Phase 4 only runs once at least two of Phases 1-3.5 have produced output — merging one source is meaningless. Phase 3.5 is skipped entirely (not run, not flagged missing) when the repo has no test directory/files.

## Delivery (all phases)

Write each phase's output to a scratch file, send as file — never paste full docs into chat. Chat reply: 1-2 sentences (what produced, item/conflict count, any caveat e.g. truncation bypassed). Iterating on an already-delivered doc ("restructure this", "add X") → overwrite same file path, resend — don't create a differently-named file for a refinement.

Phase 4's final consolidated document always saves to `docs/consolidated-requirements.md` (repo root) — fixed path, not a scratch file. Overwrite it in place on refinements, same rule as above.

## Examples

**Single-source** — "extrai requisitos com base nos commits": Phase 2 only, dump log, read full, cluster, write, send. One file, no merge, Itens Abertos section limited to what's derivable from commits alone.

**Full audit** — "quero um documento final cruzando specs, commits e transcrições, com conflitos": Phases 1→2→3→4 in order, each own file, Phase 4 consolidates per `references/merge-and-conflicts.md`. 4 files delivered (3 intermediate + final).

**Restructure delivered doc** — "esse documento está confuso, separa requisitos de conflitos com prefixos RF/RNF": re-read merge-and-conflicts.md structure rules, re-partition existing content (no re-extraction), overwrite same file, resend.

## Reference files

- `references/source-extraction-steps.md` — step tables for Phases 1-3 (transcript extraction script usage, commit dump verification, spec precedence rules)
- `references/merge-and-conflicts.md` — Phase 4 precedence order, final doc structure (header block + Legenda de Domínio + Requisitos/Itens Abertos/Notas de Contexto), RF-/RNF-/OPEN- ID numbering, status vocabulary (✅/🟡/❌), conflict-vs-stale-doc test, timestamp reconciliation
- `references/troubleshooting.md` — commit/line count mismatch, `promptSource` schema drift, unorderable contradicting facts
