---
name: rag-coverage
description: Audit corpus distribution by source type and repo; identify coverage gaps and underindexed topics
triggers:
  - rag coverage
  - corpus audit
  - rag gaps
  - coverage audit
  - what's missing from rag
---

# RAG Coverage

Audit what's indexed and what's missing. Use coverage reports to plan curation and decide between incremental fixes and full rebuilds.

## Coverage audit

Run the weekly report to see coverage distribution:

```bash
cd ~/.claude/rag-index
venv/bin/python report.py
```

Read the coverage summary:

```bash
cat ~/.claude/rag-index/weekly.md | grep -A 50 "Coverage by source type"
```

Example output:

```
Coverage by source type:
  skills: 539 chunks (≥500 target: PASS)
  handoffs: 259 chunks (≥200 target: PASS)
  standards: 54 chunks (≥50 target: PASS)
  code: 1847 chunks (scales with repo)
  plans: 198 chunks
  codex: 31 chunks (low)
  repo-docs: 127 chunks
  commit: 156 chunks
  claude-mem: 203 chunks
  spec: 89 chunks
  changelog: 52 chunks
  TOTAL: 14,355 chunks
```

## Coverage by source type

Query the index directly to see distribution:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT source_type, COUNT(*) as chunk_count, 
       ROUND(AVG(LENGTH(text)), 0) as avg_size,
       MIN(LENGTH(text)) as min_size,
       MAX(LENGTH(text)) as max_size
FROM chunks
GROUP BY source_type
ORDER BY COUNT(*) DESC;
EOF
```

**Healthy coverage targets:**

| Source Type | Min Chunks | Reason |
|-------------|-----------|--------|
| skills | 500 | Comprehensive skill docs |
| handoffs | 200 | Context summaries, transition notes |
| code | 500+ | Scales with repo size and importance |
| standards | 50 | Style guides, conventions |
| plans | 100 | Roadmaps, architecture |
| codex | 50 | Templates, patterns, how-tos |
| claude-mem | 100 | Memory snapshots, context packs |
| repo-docs | 100 | READMEs, architecture docs |
| spec | 50 | Design specs, RFCs |
| commit | 100 | Recent commit messages for context |
| changelog | 30 | Release notes, version history |

## Coverage by repository

Find which repos are well-indexed:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT repo, COUNT(*) as chunk_count, COUNT(DISTINCT path) as file_count
FROM chunks
WHERE repo IS NOT NULL
GROUP BY repo
ORDER BY COUNT(*) DESC;
EOF
```

Repos with <50 chunks likely have gaps. Look for:
- Missing source globs in build.py
- Shallow documentation
- Newly added repos not yet in the index

## Coverage by source type + repo combo

Find niche coverage gaps:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT source_type, repo, COUNT(*) as chunk_count
FROM chunks
WHERE repo IS NOT NULL
GROUP BY source_type, repo
HAVING COUNT(*) < 20
ORDER BY source_type, COUNT(*) DESC;
EOF
```

## Find zero-hit patterns

Queries that return no results indicate coverage gaps. Check weekly report:

```bash
cat ~/.claude/rag-index/weekly.md | grep -A 20 "Zero-hit queries"
```

Example:

```
Zero-hit queries (no chunks retrieved):
  "authentication refresh token" — no auth docs indexed
  "database migration strategy" — missing infra/db standards
  "component prop validation" — missing React patterns in codex
  "error handling middleware" — missing code examples in standards
```

For each zero-hit query:
1. Identify the missing topic
2. Write or curate missing docs (see `adt-rag-curate`)
3. Add source globs if code is involved (see `adt-rag-curate`)
4. Incremental reindex
5. Re-run the query to verify

## Gaps by topic

Manual audit for missing categories:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT path, source_type, COUNT(*) as chunk_count
FROM chunks
WHERE source_type IN ('standards', 'codex', 'plans')
GROUP BY path
ORDER BY source_type, COUNT(*) DESC;
EOF
```

If you see topics with 1–2 chunks, they may be truncated or incomplete. Check with `adt-rag-inspect`.

## Coverage decision tree

| Situation | Detection | Action | Time |
|-----------|-----------|--------|------|
| Source type <50% of target | Weekly report | Write missing docs + curate | 30 min – 2 hrs |
| Repo has <50 chunks | rag-coverage query | Add source globs to build.py + reindex | 20 min |
| Zero-hit queries | Weekly report or user feedback | Identify missing topic, curate, reindex | 30 min |
| Many tiny chunks (<100 chars) | adt-rag-inspect | Rebuild with new chunk-size config | 1 hr |
| Stale/missing chunks | adt-rag-drift | Delete or reindex; see adt-rag-drift | 10 min |
| Widespread gaps (>100 chunks missing) | Weekly report | Full rebuild | 2–5 min |

## Post-coverage audit workflow

1. **Run report:**

```bash
cd ~/.claude/rag-index
venv/bin/python report.py
```

2. **Check targets:**

```bash
cat ~/.claude/rag-index/weekly.md | grep -A 20 "Coverage by source type"
```

3. **For each gap:**
   - If missing doc → write and incremental reindex (see `adt-rag-curate`)
   - If undercovered repo → add source globs and reindex
   - If zero-hit query → curate related content

4. **Re-run report** after curation:

```bash
venv/bin/python report.py
```

5. **Verify** with test queries:

```bash
venv/bin/python query.py "previously zero-hit query" --top 5
```

## Coverage maintenance cadence

- **Weekly**: Run `report.py` to track trends
- **After curation**: Re-run `report.py` to verify improvement
- **Monthly**: Audit zero-hit queries and plan curation sprints
- **Quarterly**: Review source type targets; adjust if project scope changes
- **Post-major-changes**: Full rebuild if repo structure or doc locations change

## See also

- `adt-rag-curate` — fill coverage gaps
- `adt-rag-quality` — audit retrieval quality (separate from coverage)
- `adt-rag-inspect` — examine chunks in detail
- `adt-rag-drift` — find stale or missing chunks
- `adt-rag-index-rebuild` — full rebuild if coverage strategy changes
