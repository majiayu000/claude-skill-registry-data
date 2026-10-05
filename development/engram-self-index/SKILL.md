---
name: engram-self-index
description: Use when asked to dogfood engram on itself, self-improve via the code graph, find improvement targets in this repo, or periodically audit the codebase with its own tools. Triggers on "index yourself", "self-index", "use engram on this repo", "dogfood", "what should we improve here". Scans mem-alpha into the dedicated self store, runs the code-intel battery, VERIFIES findings against source, and registers actionable items in the backlog. Not for indexing OTHER repos (just scan those into their own stores).
---

# Skill: engram-self-index

Turn engram's code-intelligence on this repository itself, verify what it
reports against the real source, and register the surviving findings.

## The store

`~/.engram/mem-alpha-self` (project `mem-alpha-self`) — dedicated, this repo
ONLY, deliberately kept across sessions so a second scan activates
`whats_changed` temporal discrimination (it is flat on a single baseline).
Do not wipe it casually; a wipe resets the temporal baseline.

## Procedure

1. **Re-scan (cheap — manifests make it incremental):**

```bash
python3 scripts/dev/mcp_driver.py --storage ~/.engram/mem-alpha-self \
  --project mem-alpha-self --no-vector \
  call scan_repo '{"path": "/home/videogamer/projects/mem-alpha"}'
```

Expect sub-second on unchanged trees; `errors: 0` always (empty files skip,
minified assets filter — any error is a regression).

2. **Run the battery:**

```bash
python3 scripts/dev/mcp_driver.py --storage ~/.engram/mem-alpha-self \
  --project mem-alpha-self --no-vector \
  call architecture '{"limit": 10}' \
  call code_health '{}' \
  call whats_changed '{}' \
  call change_impact '{"target": "<top-bridge-symbol>", "depth": 2}'
```

Read it like this:
- **Bridges (betweenness)** = chokepoints/god-modules. A symbol ~5× the next
  is a named refactor target; check its blast radius before scoping the split.
- **Central (PageRank)** = coupling magnets. Short generic names (`cn`, `run`,
  `get`) are centrality artifacts, not findings.
- **Dead code** = leads, NEVER verdicts. This repo's list is dominated by
  test doubles (`Failing*`, `Fake*`, `Stub*`), prototype UI, and public-API
  surface — all legitimately uncalled in-repo.

3. **VERIFY against source before believing anything.** The 2026-08-28 run
   flagged `FastEmbedEmbeddingProvider` dead — grep proved it called from
   BOTH backends (qualified-path + self-method calls under-resolve; see the
   `[receiver-resolution-gap]` backlog item). For every dead-code candidate:

```bash
grep -rn "<SymbolName>" --include="*.rs" --include="*.ts" | grep -v "fn <name>"
```

If real callers exist, it is a resolution bug — add the reproduction to the
backlog, do not "fix" the code.

4. **Register survivors** in `docs/backlog.md` under `self-index-findings`
   with the measured numbers, and store a summary via the harness engram MCP
   (workspace `agentzero`).

## Cadence

Run after significant merges to main (the repo convention) or on request.
Each run also refreshes the temporal baseline — after ≥2 scans, prioritize
`whats_changed` output: recent-churn × high-blast-radius is where review
effort pays best.
