---
name: docs-prune
description: Analyze a repo's documentation corpus and prune/exclude stale docs so knowledge-graph and vault tooling (graphify, Obsidian sync) index only live, high-signal content. Use whenever the user wants to "prune docs", "clean up documentation", "make the repo less doc heavy", "reduce graph noise", prepare a repo for a graphify build or Obsidian vault sync, or asks whether old plans/archives/research files are safe to remove. Also use before any first graphify semantic pass on a doc-heavy repo, or when graph queries return stale/dead documents next to live ones.
---

# Stale Documentation Pruning

Built for graphify (`uv tool install graphifyy`); the classification steps work for any indexer.

Audit a repo's docs, classify staleness risk, and exclude stale content from
graph/vault indexing, **preferring exclusion over deletion**. The goal is
signal quality: stale docs become stale graph concepts that pollute query
results. Cost is almost never the motive (LLM extraction of a few MB of
markdown costs pennies); say so honestly if the user assumes otherwise.

## Core principle: exclude, don't delete

`.graphifyignore` (gitignore syntax, merged after `.gitignore`, can only
exclude more, never re-include) removes files from the graph while they stay
in the repo. Deletion loses history and breaks references; exclusion is a
one-line reversal. Only recommend actual deletion when the user explicitly
wants repo cleanup AND the content is recoverable from git history AND nothing
references it.

## Workflow

### 1. Inventory (analysis first; never prune before presenting findings)

Measure the doc corpus, excluding junk that indexers already skip
(`node_modules`, `.venv`, `.worktrees`, `.git`, vendored trees, build output):

```bash
find . \( -path ./node_modules -o -path ./.venv -o -path ./.worktrees \
  -o -path ./.git -o -path ./graphify-out -o -path "./*/node_modules" \) -prune \
  -o -type f \( -name "*.md" -o -name "*.mmd" -o -name "*.rst" -o -name "*.txt" \) -print0 \
  | xargs -0 du -k | sort -rn | head -40
```

Also aggregate by top-level directory (size + file count): pruning decisions
are made per-bucket, not per-file.

If `graphify-out/graph.json` exists, measure how much of the current graph
comes from docs (bucket node `source_file` prefixes). This quantifies the
noise being carried and gives the before-number for step 5.

### 2. Classify risk per bucket

Cross-reference before classifying: grep `CLAUDE.md`, `README`, `AGENTS.md`,
and code comments for references to each doc path. A referenced doc is never
LOW risk.

| Risk | Typical content | Action |
|------|-----------------|--------|
| **LOW** | Executed implementation plans, `archive/` dirs, dated one-shot research/reports/handoffs, completion reports for shipped work | Exclude |
| **MED** | Thought/scratch artifacts (check whether mirrored elsewhere, e.g. an Obsidian vault; a second recall path lowers risk), specs for shipped features not referenced anywhere | Exclude, note the caveat |
| **HIGH** | Sources of truth (`BACKLOG`, `CHANGELOG`, `README`, `CLAUDE.md`), live design docs, anything referenced by config/code/skills, architecture diagrams | Keep indexed |

Signals of staleness: date-stamped filenames for work that has since shipped
(check git log / changelog), "plan"/"handoff"/"report" naming, dirs the
project itself labels archived. Signals of liveness: referenced from
CLAUDE.md or code (e.g. "per TDD 16.4"), edited recently, named as a source
of truth.

### 3. Present the analysis and stop

Show a table: path, size, risk, one-line justification, proposed action.
State the honest motive (graph signal, not cost). Wait for approval: this is
the user's judgment call, not yours.

### 4. Apply exclusions

Write `.graphifyignore` at repo root with a comment explaining reversal:

```
# Exclude stale/historical docs from the knowledge graph (files stay in repo).
# Remove a line + re-run `graphify update .` to re-index.
docs/archive/
docs/plans/
```

**Negation gotcha (verified the hard way):** to re-include specific files with
`!`, the parent must be excluded as a contents glob (`research/*`), NOT a dir
pattern (`research/`). Gitignore's parent-exclusion rule makes `!` under an
excluded directory silently dead. Always verify re-included files actually
appear in `graph.json` after rebuild; zero nodes from them means this bug.

For Obsidian: apply the same exclusion list to whatever sync mechanism the
project uses (sync script filter, or the vault's `Files & Links → Excluded
files` setting). The classification is the deliverable; the enforcement point
differs per tool.

### 5. Rebuild and verify

Re-run the graph build (`graphify update .`). **Gotcha:** graphify's shrink
guard can refuse to overwrite `graph.json` with a smaller graph after an
intentional prune. Read the refusal first: force only when it names the docs
you pruned on purpose, not sources you meant to keep. The `GRAPHIFY_FORCE=1` env var is honored by the
CLI but NOT by direct `to_json()` calls, which need `force=True`. Verify the
node reduction matches expectation (before/after doc-node counts) and that
kept docs still resolve in `graphify query` results. Report before → after.

## Anti-patterns

- Pruning to "save API cost": extraction is cached and cheap; don't let the
  user believe cost is the reason. Signal quality is.
- Deleting `archive/` content that code or docs still cite by section number.
- Classifying by size alone: a 130 KB `BACKLOG.md` source of truth stays; a
  4 KB dead handoff goes.
- Editing/compacting doc *content*: out of scope; this skill only decides
  what gets indexed.
