---
name: "che-graph"
description: "Canonical and generic wrapper for Graphify CLI (pipx package graphifyy = 100% local tree-sitter AST knowledge graph, 33 languages). Subcommands: refresh, query 'question', path A B, stats. Output cache stays OUTSIDE WORKTREE in $CHE_WORKSPACE_SHARED/graphify/<related_id>/. Supports fallback chain of alternative Node.js engines (CodeGraph npm, @sentropic/graphify, codebase-vis, @lubab/madar) and a final lightweight grep-based fallback if none installed. Integration with che-xray (auto refresh during onboarding). DOES NOT create artifacts NOR edit .gitignore in the user's worktree."
---

# Che Graph — Knowledge Graph AST (Engine Wrapper with fallback chain)

> **Canonical default tool:** Graphify CLI (PyPI: `graphifyy`, double `y`)
> **Install (RECOMMENDED default):** `pipx install graphifyy`
> **Version tested:** 0.9.x+
> **Where it generates output:** `CHE_PROJECT_GRAPH_DIR` (`project/graphify/` at the project L2 level).

---

## -0.1 STORAGE BOUNDARY PREFLIGHT (MANDATORY BEFORE EVERYTHING)

```bash
# 1. Resolve the `che` CLI (owns the Che-home cascade + canonical path construction)
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Cannot write outputs without storage boundary. Aborting write."; exit 98; }

# 2. Resolve WORKTREE_ROOT + SESSION_ID
WORKTREE_ROOT="${WORKTREE_ROOT:-$(pwd)}"
SESSION_ID="${SESSION_ID:-graph-standalone-$(date -u +%Y%m%d-%H%M%S)}"

# 3. Compute canonical paths + ensure dirs
eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"

# 4. Double-guard: outputs NEVER inside worktree
che assert_outside_worktree "$CHE_SESSION_DIR" "$WORKTREE_ROOT" --label "CHE_SESSION_DIR"
che assert_outside_worktree "$CHE_WORKSPACE_SHARED" "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED"

# 5. Construct graph output paths ONCE (all in L2)
GRAPHIFY_OUTPUT_ROOT="${CHE_PROJECT_GRAPH_DIR}"
che assert_outside_worktree "$GRAPHIFY_OUTPUT_ROOT" "$WORKTREE_ROOT" --label "GRAPHIFY_OUTPUT_ROOT"
mkdir -p "$GRAPHIFY_OUTPUT_ROOT"

GRAPH_REPORT_PATH="${GRAPHIFY_OUTPUT_ROOT}/GRAPH_REPORT.md"
```

**DO NOT INVENT:** No other path in this skill. All cache, index, graphify artifacts stay UNDER `$GRAPHIFY_OUTPUT_ROOT`. If other subfiles are needed (graph.db, index.sqlite, nodes.json) → `$GRAPHIFY_OUTPUT_ROOT/<name>`. If a legacy `graphify-out/` accidentally landed inside an old worktree, move it out manually: `mv "$WORKTREE_ROOT/graphify-out" "$CHE_WORKSPACE_SHARED/legacy_cleanup/"` (it is a cache, always safe to delete).

> **100% Node.js alternatives (OPTIONAL · unify JS-only ecosystem):**
> che uses the first engine found in this order (declarative fallback chain):
> 1. `codegraph` CLI — `npm install -g @colbymchenry/codegraph` (21 languages · MCP · SQLite FTS5 · incremental file watcher · ~58% fewer tool calls benchmarks)
> 2. `graphify` (@sentropic) CLI — `npm install -g @sentropic/graphify` (multimodal code+PDFs+CSVs+ontology)
> 3. `codebase-vis` CLI — `npm install -g codebase-vis` (depgraph only, 6 languages, 17 deps, lightweight)
> 4. `madar` CLI — `npm install -g @lubab/madar` (TS/Node context-pack compiler, 5.28× fewer tokens)
> 5. `graphify` Python default above
> 6. **Final fallback:** grep-based (no tool installed, lower precision)
>
> Full comparison + install commands:
> → [README.md §Getting Started 3b](file:///home/laion/.che-ai/README.md#L38-L55)

---

## 0. WHEN TO USE

| Subcommand | When | Example |
|---|---|---|
| `refresh` | (1) 1st time in repo · (2) after large pull · (3) before `/che-xray` | `/che-graph refresh` |
| `query "question"` | Natural language questions about code STRUCTURE | `/che-graph query "where are the refund tables and which service validates the maximum refund amount?"` |
| `path "A" "B"` | Searches dependency/call path between 2 symbols or files | `/che-graph path "RefundService.processRefund" "Stripe.refunds.create"` |
| `stats` | Knowledge snapshot: indexed files, top languages, import hubs | `/che-graph stats` |

---

## 1. CLI PREREQUISITE + FALLBACK CHAIN (6 engines)

```bash
# Declarative fallback chain: codegraph → @sentropic/graphify → codebase-vis → madar → graphify python → grep-fallback
unset GRAPH_ENGINE; unset GRAPH_ENGINE_V
for candidate in "codegraph:codegraph" "graphify:@sentropic" "codebase-vis:codebasevis" "madar:madar" "graphify:graphifyy"; do
  bin="${candidate%%:*}"
  label="${candidate##*:}"
  if command -v "$bin" >/dev/null 2>&1; then
    GRAPH_ENGINE="$label"
    GRAPH_ENGINE_V="$("$bin" --version 2>/dev/null || echo unknown)"
    break
  fi
done
if [ -z "${GRAPH_ENGINE:-}" ]; then
  echo "[che-graph] ⚠️  No knowledge graph engine installed."
  echo "  Choose ONE (1 command each, ~30s):"
  echo "    · (RECOMMENDED default) pipx install graphifyy       (Python · 33+ languages · multimodal | canonical graph.html)"
  echo "    · (Node 1st choice)  npm i -g @colbymchenry/codegraph (Node · 21 languages · MCP + FTS5 · incremental auto-sync)"
  echo "    · See full list in README.md §Getting Started 3b."
  echo "  Proceeding with Grep-based FINAL FALLBACK (lower precision, no graph knowledge)."
  GRAPH_ENGINE="grep-fallback"
fi
echo "[che-graph] Selected engine: $GRAPH_ENGINE v${GRAPH_ENGINE_V:-}"
```

**Blast radius rule:** DO NOT automatically install ANY engine inside the skill. Prompt the user to manually run ONE installation command of their choice. (Security + no system packages installation without OK.)

---

## 2. SUBCOMMANDS

### 2.1 `refresh` (updates knowledge graph cache)

Canonical execution. **ALL outputs stay in `$GRAPHIFY_OUTPUT_ROOT` OUTSIDE worktree. We DO NOT use standard `graphify-out/` inside worktree.**

```bash
# Ensure output directory OUTSIDE worktree (already created in PREFLIGHT)
[ -n "${GRAPHIFY_OUTPUT_ROOT:-}" ] || { echo "[che-graph refresh] ❌ PREFLIGHT NOT run. GRAPHIFY_OUTPUT_ROOT empty." >&2; exit 99; }
che assert_outside_worktree "$GRAPHIFY_OUTPUT_ROOT" "$WORKTREE_ROOT" --label "GRAPHIFY_OUTPUT_ROOT"

if [ "$GRAPH_ENGINE" = "graphify" ]; then
  if [ -f "$GRAPH_REPORT_PATH" ]; then
    # Incremental (faster ~50%). --output-dir ensures cache OUTSIDE worktree.
    graphify "$WORKTREE_ROOT" --update --output-dir "$GRAPHIFY_OUTPUT_ROOT" 2>&1 | tail -n 5
  else
    # First time. --output-dir ensures cache OUTSIDE worktree, DOES NOT generate anything inside $WORKTREE_ROOT.
    graphify "$WORKTREE_ROOT" --output-dir "$GRAPHIFY_OUTPUT_ROOT" 2>&1 | tail -n 5
  fi
  RESULT=$?
elif [ "$GRAPH_ENGINE" = "codegraph" ] || [ "$GRAPH_ENGINE" = "codebasevis" ] || [ "$GRAPH_ENGINE" = "madar" ] || [ "$GRAPH_ENGINE" = "@sentropic/graphify" ]; then
  # Node.js fallback engines: always pass output-dir outside worktree.
  # If engine does not support --output-dir, CD to $GRAPHIFY_OUTPUT_ROOT and run from there pointing to $WORKTREE_ROOT
  ( cd "$GRAPHIFY_OUTPUT_ROOT" && "${GRAPH_ENGINE%%:*}" scan "$WORKTREE_ROOT" 2>&1 | tail -n 5 )
  RESULT=$?
else
  # Final fallback: folder structure + top-N extensions (no file generation, only prints summary)
  echo "[che-graph refresh] fallback grep-based scan:"
  find "$WORKTREE_ROOT" -maxdepth 3 -type d -not -path '*/node_modules*' -not -path '*/.git*' -not -path '*/.next*' | head -40
  find "$WORKTREE_ROOT" -type f -not -path '*/node_modules*' -not -path '*/.git*' \
    | sed -E 's/.*\.([a-z]+)$//' | sort | uniq -c | sort -rn | head -10
  RESULT=0
fi

# Audit trail (always append decision log OUTSIDE worktree — using official helper)
che decision_append "$WORKTREE_ROOT" "GRAPH_REFRESH" "{\"related_id\":\"${GRAPHIFY_RELATED_ID}\",\"engine\":\"${GRAPH_ENGINE}\",\"version\":\"${GRAPHIFY_V:-n/a}\",\"ok\":${RESULT},\"output_root\":\"${GRAPHIFY_OUTPUT_ROOT}\"}"

[ $RESULT -eq 0 ] || { echo "[che-graph refresh] ❌ failed. Check graphify --version." >&2; exit 1; }

# We DO NOT edit the user's .gitignore. As cache is OUTSIDE worktree, it never appears in git status.
```

### 2.2 `query "<question>"` (NL question)

Lean response (maximum 20 lines in chat output). Prioritises:
1. graphify CLI response if available
2. Fallback: smart grep with regex derived from the question + file-type filter

Useful real query examples:
```bash
/che-graph query "what is the Next.js app entry point and where is tRPC createCallerFactory configured?"
/che-graph query "list all TypeORM Entity classes and their files"
/che-graph query "where are auth middlewares defined (route protection) and how are they applied in routers?"
/che-graph query "is there any maximum refund amount validation? where is it?"
```

Rule: **ALWAYS return canonical absolute paths with line ranges** (e.g. `packages/db/src/entities/RefundRequest.ts#L12-L34`) so the agent can jump directly to code using Read.

### 2.3 `path "symbA" "symbB"` (dependency path)

Returns call/import chain from A → B in **DIRECT ORDER**.

Example:
```bash
/che-graph path "RefundRouter.processRefund POST handler" "Stripe.Refunds API call"
# Expected output:
# RefundRouter (L52) → RefundService.process() (L203) → RefundValidator.assertWithinLimits() (L81)
#                 → StripeClient.refundCreate() (L44 packages/stripe/src/client.ts)
```

Lightweight fallback (graphify without path): manual import chain analysis via `grep -R "from .*" import { A }` BFS acyclic.

### 2.4 `stats` (10-line snapshot)

Always stable format (parsed by scripts):
```
[che-graph stats] <repo-slug> @ <ISO ts UTC>
  engine: graphify v0.9.53
  files_scanned_total: 4,286  (excluded 18,302 = node_modules/.git/.next)
  languages:
    TypeScript .ts + .tsx = 83.2%   (3,566)
    SQL migrations .sql = 6.1%      (261)
    Shell .sh = 3.9%                (167)
    CSS .css = 2.8%                 (120)
    Markdown .md = 4.0%             (172)
  import_hubs_top5 (most imported):
    1. @flockr/db/src/index.ts        (referenced 142x)
    2. @flockr/trpc/src/client.ts     (89x)
    3. packages/platform/src/lib/stripe.ts (67x)
    4. @flockr/ui/src/button.tsx      (55x)
    5. packages/platform/src/app/api/trpc/route.ts (41x)
  knowledge_graph_age: 1h 17m  (last refresh: 2026-09-01 18:05 UTC)
```

---

## 3. CHE ECOSYSTEM INTEGRATIONS

Skills that use che-graph:
1. **che-xray (onboarding)** — calls `/che-graph refresh` as Step 1 of the scan pipeline; absorbs `stats` + top hubs into `project_profile.md`.
2. **che-scope-checker (CHECK 5 LEAN)** — `/che-graph query "which modules are used in this implementation? which don't need to be imported?"` to detect overabundant imports (high coupling = Lean finding).
3. **che-code-review (before code)** — If diff introduces new package ≥3 files → `/che-graph path "router.handler" "new.Package.method"` to check for information leakage (Ousterhout Appendix D = HIGH finding).
4. **che-fix (scientific debugging)** — Bug at point X? `path "API entry" "point X"` = full path identification = reduces unnecessary hypotheses.
5. **che-spec (before specifying)** — query "how do we already do X today in code?" → spec does not propose reimplementing what already exists (KISS/YAGNI).

---

## 4. VERSIONING + ROLLBACK

- **graphify CLI versions:** pin to >= 0.9.x if installing via pipx. Ousterhout + Graph knowledge graph API version may change in 1.0.
- **Rollback:** If graphify crashes on some project, just uninstall → che-graph automatically falls back to grep-based. Nothing breaks. Reversible.
- **Cache (ALL OUTSIDE WORKTREE):** `$GRAPHIFY_OUTPUT_ROOT` can be deleted at any time (`rm -rf "$GRAPHIFY_OUTPUT_ROOT"`). Next `refresh` recreates from scratch without side effects.
- **Legacy cleanup:** If an old `graphify-out/` accidentally landed inside a worktree, move it out: `mkdir -p "$CHE_WORKSPACE_SHARED/legacy_cleanup" && mv "$WORKTREE_ROOT/graphify-out" "$CHE_WORKSPACE_SHARED/legacy_cleanup/"`. It is a cache and always safe to delete.
