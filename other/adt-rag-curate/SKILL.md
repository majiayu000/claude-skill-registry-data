---
name: rag-curate
description: Manually improve corpus quality by adding missing docs and filling retrieval gaps
triggers:
  - rag curate
  - curate corpus
  - improve rag
  - add to rag
  - rag coverage gaps
---

# RAG Curate

Add missing docs or rewrite weak chunks after a diagnostic (`adt-rag-inspect`, `adt-rag-quality`, `adt-rag-coverage`) identifies a gap. Surgical alternative to a full rebuild.

## Corpus directories

| Type | Path |
|---|---|
| Skills | `~/.claude/skills/` |
| Standards | `~/.claude/standards/` |
| Plans | `~/.claude/plans/` |
| Codex | `~/.claude/codex/` |
| Handoffs | `~/.claude/handoffs/` |
| Code | tracked repos in `build.py` |

## Three curation patterns

### A. Missing doc → write + incremental reindex

```bash
cat > ~/.claude/standards/new-pattern.md <<'EOF'
# New Pattern Name
...
EOF

cd ~/.claude/rag-index
venv/bin/python build.py --incremental ~/.claude/standards/new-pattern.md
sqlite3 index.sqlite "SELECT COUNT(*) FROM chunks WHERE path LIKE '%new-pattern.md%';"
```

Expect >0 chunks.

### B. Weak retrieval (cos <0.40) → rewrite

```bash
cd ~/.claude/rag-index
venv/bin/python query.py "your weak query" --top 3
# note path + chunk id; edit the source file to add keywords / clarify context
venv/bin/python build.py --incremental <path>
venv/bin/python query.py "your weak query" --top 3   # cosine should rise
```

### C. Undercovered repo → widen globs in build.py

```bash
sqlite3 ~/.claude/rag-index/index.sqlite \
  "SELECT repo, COUNT(*) FROM chunks WHERE repo='your-repo' GROUP BY repo;"
grep -n "your-repo" ~/.claude/rag-index/build.py
# add globs (e.g. add 'src/**/*.tsx'), then incremental reindex
```

## Gap-filling cheatsheet

| Gap | Detection | Fix | Time |
|---|---|---|---|
| Missing doc | zero chunks for topic | write + incremental | 10 min |
| Weak retrieval | score <0.40 | rewrite + reindex | 15 min |
| Undercovered repo | <50 chunks, many files | widen globs + reindex | 20 min |
| Dead code chunks | orphaned (rag-drift) | sqlite DELETE + reindex | 5 min |
| Stale (sha mismatch) | rag-drift | reindex modified file | 5 min |

## When NOT to curate

Curation is wrong tool if:

- >100 chunks missing → full rebuild via `adt-rag-index-rebuild`
- >20 stale chunks → full rebuild
- Many chunks <100 chars → rebuild with new chunk-size config

## Validation

After every curation:

```bash
cd ~/.claude/rag-index
venv/bin/python query.py "<original weak query>" --top 5   # cos > 0.40
venv/bin/python report.py                                   # check weekly delta
```

Commit any doc edits or new standards files to the appropriate repo.

## See also

- `adt-rag-coverage` — find gaps
- `adt-rag-quality` — confirm curation worked
- `adt-rag-inspect` — verify chunk shape
- `adt-rag-index-rebuild` — full rebuild fallback
