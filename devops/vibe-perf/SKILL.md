---
name: vibe-perf
description: >
  Full-stack performance audit for vibe-* projects — frontend, backend,
  agentic pipelines, and infrastructure. Measures, scores, compares against
  previous runs, and writes approved fixes automatically.
  Triggers on "perf:" prefix, "performance audit", "this is slow",
  "optimize performance", "Lighthouse score", "bundle size",
  "slow queries", "LLM latency", "token usage", "memory leak",
  "CPU usage", "cold start", "perf regression".
  Runs automatically after vibe-review flags performance as P1/P2,
  and as a recommended pre-deploy check — any perf **P0** it writes to
  vibe/reviews/backlog.md is then enforced by vibe-deploy's Step 0.5 gate
  (which blocks on open P0s), so a perf-critical finding does block deploy.
  Always use when performance is in question — even without the exact prefix.
  Shows fix plan by category, waits for human approval, then writes all fixes.
  Tracks scores over time and compares against previous perf: runs.
---

# Vibe Perf Skill

Full-stack performance audit grounded in actual measurements.
Measures every layer. Scores it. Compares to last run. Flags regressions.
Shows fix plan by category. Writes all approved fixes automatically.

**Runs in agent mode (Claude Code / Cursor). Requires filesystem access.**

---

## The principle this enforces

Performance problems that aren't measured are invisible.
Performance problems that aren't tracked regress silently.
Performance problems caught before deploy cost minutes to fix.
Performance problems caught in production cost users and reputation.

Measure first. Fix second. Never the other way around.

---

## Entry points

### Entry point A — On demand
Triggered by: `perf:`, "performance audit", "this is slow", "optimize X"

Default scope: full project audit across all applicable layers.
If user specifies scope ("perf: frontend only" / "perf: audit the Scout agent")
— scope to that layer/module only.
Go to **Step 0**.

### Entry point B — After vibe-review flags perf
Triggered when `vibe-review` produces P1/P2 findings tagged as performance.

Read the review report. Scope to flagged files and layers only.
Go to **Step 0**.

### Entry point C — Pre-deploy gate
Triggered automatically before `vibe-deploy` runs.

Full audit — all layers. If any P0 perf finding exists, deploy is blocked.
Go to **Step 0**.

---

## Step 0 — Read project context

Read in this order:

1. `vibe/ARCHITECTURE.md` — stack, patterns, any perf thresholds defined
2. `vibe/CODEBASE.md` — section 1 (stack), section 2 (commands),
   section 5 (routes), section 7 (components), section 8 (services)
3. `CLAUDE.md` — dev/build/test/run commands
4. `vibe/perf/baseline.json` — previous run data (if exists)

**Detect applicable audit layers from stack:**

| Stack indicator | Layers to audit |
|----------------|----------------|
| React / Next.js / Vue / Svelte | Frontend + Backend if API routes present |
| FastAPI / Express / Rails / Go | Backend + Infrastructure |
| LangGraph / LangChain / agent files | Agentic + Backend |
| Docker / docker-compose | Infrastructure |
| Supabase / Prisma / SQLAlchemy | Backend DB queries |

**Check for custom perf thresholds in ARCHITECTURE.md:**
Look for `## Performance` or `## Perf thresholds` section.
If found — these override all default thresholds in Steps 1–4.
If not found — apply the default thresholds defined per step.

**Check for previous run:**
```bash
mkdir -p vibe/perf
ls vibe/perf/baseline.json 2>/dev/null && echo "BASELINE EXISTS" || echo "FIRST RUN"
```

If baseline exists — comparison run. Load previous scores for delta calculation.
If first run — establish baseline. No deltas. Note "first run" in report.

---

## Step 1 — Frontend audit

**Skip entirely if no frontend detected in CODEBASE.md.**

### 1A — Lighthouse CI

```bash
# Install if not present
npm list -g @lhci/cli 2>/dev/null || npm install -g @lhci/cli

# Dev server must be running — start if not
curl -s http://localhost:3000 > /dev/null 2>&1 || \
  ([dev command from CLAUDE.md] & sleep 8)

# Run 3 times for reliable average
lhci autorun \
  --collect.url=http://localhost:3000 \
  --collect.numberOfRuns=3 \
  --upload.target=filesystem \
  --upload.outputDir=vibe/perf/lighthouse
```

Also test key routes beyond `/` — read routes from CODEBASE.md section 5.
Run Lighthouse on the 3 most trafficked routes.

**Default score thresholds:**

| Metric | P0 | P1 | P2 |
|--------|----|----|-----|
| Performance score | < 50 | 50–74 | 75–89 |
| LCP | > 4s | 2.5–4s | 1.5–2.5s |
| TBT | > 600ms | 300–600ms | 100–300ms |
| CLS | > 0.25 | 0.1–0.25 | 0.05–0.1 |
| FCP | > 3s | 1.8–3s | 1–1.8s |

### 1B — Bundle analysis

```bash
# Vite
npx vite-bundle-visualizer --json 2>/dev/null \
  > vibe/perf/bundle-analysis.json

# Next.js
ANALYZE=true npm run build 2>&1 | tee vibe/perf/bundle-build.log

# Webpack
npx webpack-bundle-analyzer stats.json --mode json 2>/dev/null \
  > vibe/perf/bundle-analysis.json
```

**Bundle thresholds:**

| Metric | P0 | P1 | P2 |
|--------|----|----|-----|
| Initial JS bundle | > 500kb | 250–500kb | 150–250kb |
| Any single chunk | > 300kb | 150–300kb | 100–150kb |
| Largest dependency | > 200kb | 100–200kb | 50–100kb |
| Unused JS | > 30% | 15–30% | 5–15% |

From bundle output, identify:
- Duplicate dependencies (same package, multiple versions)
- Large dependencies that could be lazy-loaded or replaced
- Missing route-level code splitting
- Unused exports being included in bundle

### 1C — Component render analysis

Read each component file from CODEBASE.md section 7. Check for:

- Missing `React.memo` on pure components receiving complex props
- Object/array literals created inline in JSX props (new reference every render)
- `useEffect` with missing or incorrect dependency arrays
- Large lists (> 50 items) without virtualisation
- Images without `loading="lazy"` or `next/image` optimisation
- Missing `key` props on mapped lists
- Waterfall data fetching (sequential awaits that could be `Promise.all`)

---

## Step 2 — Backend audit

**Skip entirely if no backend detected in CODEBASE.md.**

### 2A — API endpoint analysis

Read all route/controller files from CODEBASE.md section 5.

For each endpoint, identify:
- No response caching on idempotent GET endpoints
- Synchronous calls to external APIs where async would unblock the thread
- Missing pagination — list endpoints returning unbounded results
- Response payload including unused fields (over-fetching)
- Auth checks happening after expensive operations (should be first)

**Response time thresholds (estimated from code patterns):**

| Endpoint type | P0 | P1 | P2 |
|--------------|----|----|-----|
| Auth endpoints | > 2s | 1–2s | 500ms–1s |
| Data read | > 1s | 500ms–1s | 200–500ms |
| Data write | > 3s | 1–3s | 500ms–1s |
| File/media | > 5s | 3–5s | 1–3s |

### 2B — Database query analysis

```bash
# Check Prisma schema for missing indexes
cat prisma/schema.prisma 2>/dev/null

# Find N+1 patterns — DB calls inside loops
grep -rn "\.findMany\|\.find\|\.query\|\.execute\|SELECT" \
  --include="*.ts" --include="*.js" --include="*.py" \
  . | grep -v node_modules | grep -v ".test." | grep -v migrations
```

Read each service file that touches the database. Identify:
- DB queries inside `for` / `while` loops → N+1
- `SELECT *` where specific columns would do
- Missing `LIMIT` on queries that could return unbounded rows
- Filters on columns with no index
- Missing indexes on foreign key columns
- Multi-step writes not wrapped in a transaction
- Missing composite indexes on frequently joined columns

```bash
# Prisma — check foreign keys without @index
grep -A5 "@relation" prisma/schema.prisma 2>/dev/null | \
  grep -v "@@index\|@id\|@unique"
```

**DB query thresholds:**

| Issue | Severity |
|-------|---------|
| N+1 query pattern | Always P0 |
| Unbounded query (no LIMIT) | Always P1 |
| Missing index on FK | Always P1 |
| SELECT * on large table | P2 |
| Missing transaction on multi-write | P1 |

---

## Step 3 — Agentic performance audit

**Skip entirely if no agent patterns detected in CODEBASE.md.**

Read `references/AGENTIC_PERF.md` before this step.

### 3A — LLM call efficiency

Read all agent files from CODEBASE.md section 8. Identify:

**Token waste patterns:**
- System prompts > 2000 tokens without clear justification
- Full conversation history passed to sub-agents on every call
- Entire session state serialised into every LLM call
- No structured output (JSON schema) where it would halve token usage
- Same external data fetched multiple times across agent calls
- Verifier prompts duplicating the full task spec (send only rubric)

**Latency patterns:**
- Sequential LLM calls with no data dependency (could be parallel)
- No streaming on user-facing generation
- Retry logic without exponential backoff
- Sub-agent calls with no timeout

**Token thresholds:**

| Metric | P0 | P1 | P2 |
|--------|----|----|-----|
| System prompt size | > 4000 tokens | 2000–4000 | 1000–2000 |
| Avg context per call | > 8000 tokens | 4000–8000 | 2000–4000 |
| Parallelisable sequential calls | > 3 | 2–3 | 1 |
| Retry without backoff | — | Always P1 | — |
| No call timeout | — | Always P1 | — |

### 3B — Agent loop efficiency

Read orchestrator and state management files:

- State object grows unboundedly across iterations (no pruning)
- Full state object passed to sub-agents (should pass task slice only)
- No max iteration cap on the verification loop
- Completed sub-task results not cached for retry scenarios
- Session state not persisted — re-runs expensive extraction on each start

---

## Step 4 — Infrastructure audit

**Skip if no Dockerfile / docker-compose / deployment config found.**

```bash
# Read all config files
cat Dockerfile 2>/dev/null
cat docker-compose.yml docker-compose.yaml 2>/dev/null
cat Procfile 2>/dev/null
cat gunicorn.conf.py 2>/dev/null

# Check for resource limits
grep -n "mem_limit\|cpus\|memory\|cpu_shares\|max-old-space" \
  docker-compose.yml docker-compose.yaml package.json 2>/dev/null

# Node heap setting
grep -rn "max.old.space" . | grep -v node_modules
```

Check for:
- No memory limits on containers
- No CPU limits on containers
- Node.js heap not sized (default 512mb may be insufficient)
- Python workers not configured for async workload
- Docker image > 500mb (cold start impact)
- No multi-stage build (dev dependencies shipped to production)
- No health check endpoint defined
- No connection pooling configured for DB

---

## Step 5 — Score, compare, build fix plan

Read `references/PERF_REPORT_TEMPLATE.md` for full report format.

**Score calculation:**

| Layer | Method |
|-------|--------|
| Frontend | Lighthouse performance score (0–100) |
| Backend | 100 − (P0×20 + P1×10 + P2×5), floor 0 |
| Agentic | 100 − (P0×20 + P1×10 + P2×5), floor 0 |
| Infrastructure | 100 − (P0×20 + P1×10 + P2×5), floor 0 |
| Overall | Weighted average of applicable layers |

**Compare with baseline (if exists):**
Calculate delta per layer. Flag any layer down > 5 points as regression.
Regressions are P1 minimum. Regressions that push a layer below P0
threshold are P0.

**Build the fix plan — two categories:**

Read `references/FIX_RISK_GUIDE.md` for full risk classification.

Category A — Safe (auto-write on approval):
- DB indexes, query LIMIT additions
- React.memo, useMemo, useCallback additions
- Image lazy loading, next/image migration
- Bundle code splitting configuration
- Exponential backoff on retry logic
- Docker memory/CPU limits
- Agent token trimming, structured output adoption
- Promise.all for independent async calls

Category B — Risky (individual approval per fix):
- DB query restructuring (touches production data flow)
- Agent token budget changes (affects output quality)
- Orchestrator state management changes
- API response shape changes (pagination = breaking change)
- Component splits (may break existing tests)

**Present fix plan and wait for approval.**
See output format in Step 9 below.

**Approval commands:**
- `approve A` — write all Category A fixes
- `approve B: [N]` — approve one risky fix by number
- `approve all` — approve everything
- `skip [N]` — exclude a specific fix

---

## Step 6 — Write approved fixes

Write in this order: infrastructure → backend → agentic → frontend.

For each fix:
1. Read the target file in full
2. Make the minimal change that addresses the finding
3. Add inline comment: `# perf: [what fixed] — vibe-perf [date]`
4. Run verification immediately after:

```bash
# After DB index — check query plan
# After bundle change — rebuild and measure new size
# After component change — confirm no test failures
[test command from CLAUDE.md]
```

**Never:**
- Modify test files as part of a perf fix
- Remove functionality to gain performance
- Change public API interfaces without logging in DECISIONS.md
- Apply Category B fix without explicit approval

---

## Step 7 — Update baseline and history

```bash
# Save this run as new baseline
cat > vibe/perf/baseline.json << 'EOF'
{
  "run_date": "[ISO date]",
  "run_number": [N],
  "trigger": "[on-demand|pre-deploy|post-review]",
  "scores": {
    "frontend": [N],
    "backend": [N],
    "agentic": [N],
    "infrastructure": [N],
    "overall": [N]
  },
  "findings": { "p0": [N], "p1": [N], "p2": [N], "regressions": [N] },
  "fixes_applied": [N],
  "fixes_pending": [N]
}
EOF

# Append to rolling history (create if not exists)
python3 -c "
import json, os
path = 'vibe/perf/history.json'
history = json.load(open(path)) if os.path.exists(path) else []
history.append(json.load(open('vibe/perf/baseline.json')))
json.dump(history, open(path, 'w'), indent=2)
"
```

---

## Step 8 — Update vibe docs

**vibe/TASKS.md** — update "What just happened":
```
✅ Performance audit — [date] — Overall [N]/100 [↑/↓/→ vs last run]
   [N] fixes written · [N] pending manual review
   Report: vibe/perf/report-[date].md
```

**vibe/reviews/backlog.md** — add unfixed P1/P2 findings as perf backlog items.
Resolve any previously logged perf items that were fixed in this run.

**vibe/DECISIONS.md** — log any Category B fix that changed an API shape
or DB schema as a `tech-choice` entry with before/after detail.

**Pre-deploy gate result (Entry C):**
```
✅ PERF GATE PASSED — [N]/100 overall · 0 P0 findings · deploy unblocked
🔴 PERF GATE BLOCKED — [N] P0 findings must be resolved before deploy
```

---

## Step 9 — Final report

Save to `vibe/perf/report-[YYYY-MM-DD].md`.

```
✅ vibe-perf complete — [Project Name] — [date]

SCORES
  Frontend:       [N]/100  [was N → delta]
  Backend:        [N]/100  [was N → delta]
  Agentic:        [N]/100  [was N → delta]
  Infrastructure: [N]/100  [was N → delta]
  Overall:        [N]/100  [was N → delta]

FINDINGS
  P0 critical: [N]    P1 warning: [N]    P2 note: [N]
  Regressions: [N]

FIXES WRITTEN:  [N] (Category A)
FIXES PENDING:  [N] (Category B — flagged in backlog)

NEXT PERF RUN WILL COMPARE AGAINST THIS BASELINE.
Full report: vibe/perf/report-[date].md
Baseline:    vibe/perf/baseline.json (run #[N])
History:     vibe/perf/history.json
```
