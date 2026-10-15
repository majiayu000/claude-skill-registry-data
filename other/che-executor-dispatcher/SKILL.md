---
name: "che-executor-dispatcher"
description: "Parallel batch executor for the che. Given a TASK GRAPH, builds topological batches, enforces blast-radius file-lock partitions, fans-out independent che-developer instances in parallel, runs per-batch MERGE AUDIT + scope/QA/compliance gates, and produces a BATCH_REPORT. Invoked BY che-act only when task_graph.md has >=2 tasks with no dependencies sharing zero files. Or explicitly by /che-parallel."
---

# Che — Parallel Executor Dispatcher

This skill is the **parallel execution backbone** of the che.
It takes a `task_graph.md` (from Scrum Master) + one task envelope per task,
performs **Kahn's topological sort by dependency + file-lock blast-radius partition**,
fans out `che-developer` calls as parallel independent sub-agent calls in BATCHES,
then runs per-task gates (scope/QA/compliance-light) and a per-batch **MERGE AUDIT** to catch
cross-task file conflicts BEFORE the next batch starts.

**CRITICAL CONTRACT**: This skill is called BY `che-act`. It is **NOT** a top-level
orchestrator — SM retains authority over scope + overall gates. This skill only does dispatch.

---

## -0.1 STORAGE BOUNDARY PREFLIGHT (CANONICAL, NON-NEGOTIABLE — run BEFORE §0 and BEFORE FIRST WRITE)

NO work asset (execution_batches, dev_reports, merge_audits, batch_execution_report, _locks, dispatcher.config, etc.) is written to the USER WORKTREE by default. UNIQUE exception: user explicitly asks VERBATIM to save a specific file there. **HARD STOP exit 99 if any path falls within WORKTREE_ROOT.**

Execute EXACTLY:

```bash
# 1. Resolve the `che` CLI (owns the 5-tier Che-home cascade)
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. HARD STOP without storage boundary. exit 99"; exit 99; }

# 2. SESSION_ID (via SM or derived)
SESSION_ID="${SESSION_ID:-${CHE_SESSION_ID:-${HARNESS_SESSION_ID:-dispatcher-$(date -u +%Y%m%d-%H%M%S)}}}"
RELATED_ID="dispatcher-${WORKTREE_SLUG_CANONICAL:-$(basename "$WORKTREE_ROOT" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g; s/--*/-/g; s/^-//; s/-$//')}"

# 3. Compute canonical paths + ensure dirs
eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"

# 4. DOUBLE-GUARD outside worktree
che assert_outside_worktree "$CHE_SESSION_DIR"       "$WORKTREE_ROOT" --label "CHE_SESSION_DIR"
che assert_outside_worktree "$CHE_WORKSPACE_SHARED"  "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED"

# ==== SKILL PATHS CONSTRUCTED ONCE (reuse variables below, do not reconstruct) ====
# INPUTS (durable workspace-shared, produced by SM before dispatcher):
TASK_GRAPH_PATH="${TASK_GRAPH_PATH:-$(che output_path "task" "task-graph" "${RELATED_ID}" "workspace" "md")}"  # SM Phase 0 input
# DURABLE OUTPUTS (workspace-shared, consultable in future sessions on same worktree):
EXECUTION_BATCHES_PATH="$(che output_path "config" "execution-batches" "${RELATED_ID}" "workspace" "md")"
DISPATCHER_LOCK_DIR="${CHE_WORKSPACE_SHARED}/_locks"                              # canonical subfolder created in ensure_dirs LOCK subdir mapping
DISPATCHER_CONFIG_TEMPLATE_PATH='${CHE_WORKSPACE_SHARED}/tasks/<task-id>/dispatcher.config.json'  # per-task override (DURABLE WORKSPACE_SHARED)
# EPHEMERAL OUTPUTS (per-session, do not need to survive che restart):
DEV_REPORT_PATTERN_SUFFIX='<TASK_ID>'                                                 # construct per task via: che output_path "report" "dev-report" "T${TASK_ID}-${TASK_SLUG}" "session" "md"
# MERGE_AUDIT per batch/mini-batch (§4.1 loop below = construct each with related_id="B${BATCH}-MB${MINI}"):
#   MERGE_AUDIT_Bx_MBy_PATH="$(che output_path "merge_audit" "merge-audit" "${RELATED_ID}-B${BATCH}-MB${MINI}" "session" "md")"
# Final BATCH_EXECUTION_REPORT (§5 step 4 below = construct ONCE):
BATCH_EXECUTION_REPORT_PATH="$(che output_path "report" "batch-execution-final" "${RELATED_ID}" "session" "md")"
```

---

## 0. Preconditions (MANDATORY — fail immediately)

The SM MUST pass, either as function arguments or in a well-known dispatch config file:

| Input | Source | Purpose |
|---|---|---|
| `WORKTREE_ROOT` | Confirmed by SM preflight | Absolute path |
| Task graph (DURABLE workspace-shared) → `$TASK_GRAPH_PATH` (via PREFLIGHT above — canonical path helper `task/task-graph/dispatcher-<wt-slug>/*.md`) | SM Phase 0 output | Full task list, deps, status |
| Task envelope per task TODO/READY → (same structure WORKSPACE_SHARED/tasks/<id>/task_envelope_*.md via `che output_path "task" "<slug>" "<related_id>" "workspace" "md"`, built by SM Section 2.1 before calling dispatcher) | SM Section 2.1 output | Each with **Blast Radius → ALLOWED files** |
| `max_parallel` (optional, int) | SM or user | Concurrent Devs cap. Default = `min(cpu_cores, 3)`. Hard cap 4. |

If ANY task marked READY-for-parallel does NOT have a fully enumerated `Blast Radius → ALLOWED files` list (with globs resolved to concrete files, not just "src/*") → **REFUSE parallel for that task and fall back to serial.** Blast-radius glob wildcards are not allowed in parallel mode because the lock system cannot validate intent.

---

## 1. Step 1 — Validation + Topological Batching

### 1.1 Ingest task_graph.md

Parse:
- All rows from `Task Table`.
- For each row: `ID`, `Depends_on[]`, `Status`.

### 1.2 Kahn's topological sort to get READY batches

A "READY" task = all tasks in `Depends_on[]` have `Status == DONE`.

Algorithm:
1. Let `in_degree[T] = len(Depends_on[T] not DONE)` for all T.
2. `queue = [ T where in_degree[T] == 0 and Status == TODO ]`.
3. While queue not empty:
   - `batch_candidates = queue` (all zero-in-degree currently) → this is **Batch N**.
   - Apply **Blast-Radius File Partition** (next step) on `batch_candidates`.
   - If partitioning reduces the batch → remainder go back to queue as "READY-for-next-batch-within-phase"; they'll run in mini-batch **after** current mini-batch finishes + merge audit passes (still before advancing in-degree to next Kahn's wave).
4. Mark batch as complete after all tasks + merge audit pass.
5. Reduce in-degrees for successors. Repeat.

### 1.3 Blast-Radius File-Partition (the critical correctness guard)

Given a candidate set `S = {T1, T2, ...}` from the same Kahn wave:

1. For each task `T` in `S`, extract the **EXPLICIT** file list from `task_envelope_<T>.md` → `Blast Radius → ALLOWED` section. Call this `Files(T)`.
2. Build an **intersection conflict graph** where tasks are vertices and an edge `T1—T2` means `Files(T1) ∩ Files(T2) != ∅`.
3. Run a **greedy graph colouring** on the conflict graph (colours = mini-batches). Tasks of the SAME colour = NO pairwise file conflict → safe parallel.
4. Each colour = one **mini-batch**. Mini-batches are run SERIALLY within the same Kahn wave (they share files), but tasks INSIDE one mini-batch run PARALLEL (no shared files).

**This ensures correctness even if T2 and T1 both want to edit `utils.ts` — they will be automatically split into different mini-batches, so T1 writes, merges, then T2 reads updated + writes.**

### 1.4 Step 1 Output

Save to `$EXECUTION_BATCHES_PATH` (constructed PREFLIGHT — DURABLE workspace-shared, timestamp UTC prefix in filename, `config/dispatcher-<wt-slug>/` subfolder).
DO NOT manually reconstruct `$CHE_WORKSPACE_SHARED/execution_batches.md`; use the variable.
Atomic write via helper (avoids half-written files on SIGTERM):

```bash
cat <<'EOF' | che write_file_atomic "$EXECUTION_BATCHES_PATH"
# EXECUTION BATCHES — <task-id>

## Strategy
- algorithm: Kahn topological sort + greedy graph colouring on file-conflict graph
- max_parallel: <N>
- batches_count: <B>

## Batch B1 (Kahn wave 1, mini-batch 1/2, parallel-safe, files pairwise disjoint)
| Task | Depends on | Files (count) | Status |
|---|---|---|---|
| T1 | - | 7 files | READY |
| T3 | - | 3 files | READY |

## Batch B1b (Kahn wave 1, mini-batch 2/2, serial fallback, conflict with B1 on src/lib/utils.ts)
| Task | Depends on | Files sharing reason | Status |
|---|---|---|---|
| T2 | - | utils.ts overlaps T1 | QUEUED |

## Batch B2 (Kahn wave 2, depends on B1+B1b DONE)
...
EOF
```

---

## 2. Step 2 — File Lock System

For every mini-batch about to run:

1. Before fanning out Devs:
   - For each task T in the mini-batch, for each file f in Files(T):
     - **ASSERT**: no `${DISPATCHER_LOCK_DIR}/<normalized-f>.lock.json` exists with state `HELD` (DIR constructed PREFLIGHT = `$CHE_WORKSPACE_SHARED/_locks/`, canonical contract subfolder, OUTSIDE worktree per contract + assert double-guard).
     - If any exists held → re-queue T into next mini-batch.
2. On task T start (just before invoking che-developer):
   - Atomically for ALL files in Files(T):
     - Atomic write via `che write_file_atomic "${DISPATCHER_LOCK_DIR}/<hash>-<basename>.lock.json"` helper (DURABLE workspace-shared, runtime, NEVER staged/committed — che-ship §0.8 blacklist covers `**/_locks/**` pattern):
       ```json
       {"task_id": "T1", "batch": "B1", "held_at": "<ISO>", "state": "HELD"}
       ```
   - If atomic acquisition fails → rollback + re-queue to next mini-batch.
3. On task T end (regardless of success/failure):
   - Atomically for ALL files in Files(T): change state to `RELEASED` with `ended_at` + `outcome` (PASS/FAIL_SCOPE/FAIL_QA/FAIL_COMPLIANCE).

Lock directory is `${DISPATCHER_LOCK_DIR}` = `${CHE_WORKSPACE_SHARED}/_locks/` → lives OUTSIDE user worktree code by design (engineering-contracts §20 MORATORIUM EXPANDED to ENTIRE worktree); blacklist synced in che-ship §0.8 Stage 3, never staged/committed.

---

## 3. Step 3 — Fan-Out: Parallel Developer Calls

For each task T in current mini-batch:

1. Mark `task_graph.md` row for T: `Status = IN_PROGRESS (parallel, batch=<B>, mini-batch=<MB>)` (dispatcher/SM is ONLY writer; DO NOT let dev agents write task_graph).
2. Construct task report path ONCE (outside invocation loop) via helper (ensures timestamp UTC prefix, `reports/T<id>-...` subfolder):
   ```bash
   DEV_REPORT_T_PATH="$(che output_path "report" "dev-report" "T${TASK_ID}-${TASK_SLUG:-unnamed}" "session" "md")"
   ```
3. Invoke a **dedicated parallel-execution sub-agent call** for `che-developer` with:
   - Full env variable context: `WORKTREE_ROOT`, `SESSION_ID`, `TASK_ID=T`, envelope path, `DEV_REPORT_OUTPUT_PATH="${DEV_REPORT_T_PATH}"`.
   - `general_purpose_task` sub-agent invoked with **isolation semantics** — each agent writes its own report file in `${DEV_REPORT_T_PATH}` (EPHEMERAL per-session, via PREFLIGHT above + path helper, NOT inside worktree) and **never writes to task_graph.md** (that is dispatcher's single-writer role).
   - Output: when all sub-agents return, collect all per-task dev reports (read each `${DEV_REPORT_T_PATH}` and concatenate).

### 3.1 Parallel Developer Report Per-Task Contract

Every parallel Dev MUST return a machine-readable section:
```
## PARALLEL_WRITES (for dispatcher merge-audit)
Files modified: /absolute/path/a.ts, /absolute/path/b.ts, ...
```
If absent → dispatcher treats task as FAILED_SCOPE (contract not upheld), rejects + re-runs serially (not parallel).

---

## 4. Step 4 — Per-Task Gates (parallel, per-task but SM-validated)

Once ALL tasks in mini-batch have returned a Dev report:

1. **For EACH task T in mini-batch, SERIALLY** (SM is still single-writer for gates + task_graph, because QA/compliance scan shared worktree state):
   - Scope Validation (che-act rules section 2.3).
   - If PASS → mark `SCOPE_OK`.
   - Run QA (che-qa) on task T.
   - If PASS → mark `QA_OK`.
   - Run Compliance LIGHT (che-compliance, per-task).
   - If PASS → mark `DONE`.
   - If any gate fails → mark FAILED_*, stop advancing this task; DO NOT release locks (they remain `RELEASED_FAILED` so next re-run forces overwrite caution); this task goes back to SM flow.
2. Per-task failures DO **NOT** block other tasks of same mini-batch (they passed gates independently). But they DO block dependent tasks in next Kahn wave.

### 4.1 MERGE AUDIT (cross-task within same mini-batch)

Before moving to next mini-batch or next Kahn wave:

Algorithm:
1. Collect every file in every `PARALLEL_WRITES` list from tasks in this mini-batch.
2. Build frequency map.
3. **Any file with frequency > 1 written by different tasks in THIS mini-batch → FLAG CONFLICT.**
4. Conflict severity:
   - `LOW`: different files in same directory (no overlap, coincidence) → ok.
   - `MEDIUM`: exact same file path but disjoint diff (hunks don't overlap) → SM reviews, applies with explicit decision entry via `che decision_append "$WORKTREE_ROOT" "MERGE_AUDIT_MEDIUM_CONFLICT_SM_APPROVED" '{"batch":"'${BATCH}'","mini":"'${MINI}'","files_overlap": [...]}'`.
   - `HIGH`: exact same file path AND overlapping hunks (or file is > 100 lines modified by both) → **HARD FAIL.** Roll back one of the two task's changes (git stash or git checkout HEAD -- <file> for whichever has more LOC committed), re-run task serially, re-apply gates. Append decision log via `che decision_append "$WORKTREE_ROOT" "MERGE_AUDIT_HIGH_CONFLICT_ROLLBACK" '{"batch":"'"${BATCH}"'","mini":"'"${MINI}"'","rolled_back_task":"<task_id>"}'`.
5. Construct path for this merge-audit (one per BATCH + MINI) via helper + atomic write:
   ```bash
   MERGE_AUDIT_BATCH_MINI_PATH="$(che output_path "merge_audit" "merge-audit" "${RELATED_ID}-B${BATCH}-MB${MINI}" "session" "md")"
   cat <<'MAEOF' | che write_file_atomic "$MERGE_AUDIT_BATCH_MINI_PATH"
   # Merge Audit — B${BATCH} / MB${MINI}
   ...
   MAEOF
   ```
   (EPHEMERAL per-session, `merge_audits/dispatcher-<wt-slug>-B<N>-MB<K>/` subfolder ordered by alphabetical timestamp UTC prefix.)

If ANY task fails gates OR merge audit reports HIGH conflict → mark mini-batch PARTIAL and continue. Dispatcher returns structured status to SM.

---

## 5. Step 5 — Loop, Batch Complete, Return

1. Once mini-batch passes gates + merge audit → release HELD locks → `rm` lock files (`${DISPATCHER_LOCK_DIR}` directory).
2. Advance Kahn in-degree counter by 1 for each DONE task.
3. Build next mini-batch or next Kahn wave.
4. When **no more tasks remain** (all in task_graph marked DONE or FAILED_*):
   - Atomic write to `$BATCH_EXECUTION_REPORT_PATH` (constructed PREFLIGHT. EPHEMERAL per-session, `reports/dispatcher-<wt-slug>/` subfolder. Timestamp prefix ensures ordering between future dispatcher runs on same worktree.)
     ```bash
     cat <<'REOF' | che write_file_atomic "$BATCH_EXECUTION_REPORT_PATH"
     # BATCH EXECUTION REPORT — dispatcher run <UTC iso>
     - Batches run, minibatches, tasks per batch, conflicts caught
     - Per-task status (DONE / FAIL_SCOPE / FAIL_QA / FAIL_COMPLIANCE / CONFLICT_ROLLBACK)
     - Per-batch merge audit tally
     - Wall-clock approx
     - Lock contention count
     REOF
     ```
     DO NOT manually reconstruct path (`$CHE_SESSION_DIR/reports/BATCH_EXECUTION_REPORT.md`) — use PREFLIGHT variable.
   - Return structured summary to `che-act`.
   - SM proceeds to **Compliance HEAVY → manual_test_plan → final_summary** as usual (no parallelism in final stage; single cross-cut pass).

---

## 6. When to REFUSE parallelism (FALL BACK to serial)

Safety first. Dispatcher MUST fall back to SM's serial loop if ANY:

1. Any task in current candidate set does not have full, enumerated (non-glob) file list.
2. Conflict graph colouring produces > `len(S)` colours (fully serial, no parallel win) → use serial.
3. `max_parallel == 1` set by user.
4. User explicitly requests `--serial` flag.
5. Worktree has uncommitted dirty changes outside che scope (risk of interleaving non-che edits).
6. A lock file from PREVIOUS aborted session exists → present list to user; ask "purge stale locks and proceed?" or abort.

**Rule: parallelism is an OPTIMISATION, never a REQUIRED path.** Correctness beats speed 100% of the time.

---

## 7. Never-Dos

- NEVER have two tasks in same mini-batch sharing files. If this slips (lock acquisition race) → merge audit catches and rolls back. Defense-in-depth.
- NEVER let a parallel Dev write directly to `task_graph.md`. Single writer = dispatcher/SM.
- NEVER run Compliance HEAVY (final sweep) or HEAVY cross-file checks in parallel; they scan entire cumulative diff and are single-pass.
- NEVER trust a task that doesn't emit `PARALLEL_WRITES`. Refuse its output.
- NEVER allow > 4 parallel Devs. Context window + reasoning cost grows O(n).

---

## Appendix A: Configuration Defaults

```yaml
max_parallel_default: 3
max_parallel_hard_cap: 4
lock_dir: ${DISPATCHER_LOCK_DIR}  (DURABLE workspace-shared via PREFLIGHT; OUTSIDE user worktree)
stale_lock_timeout_seconds: 3600
merge_audit_high_conflict_min_lines_overlap: 5
```

User can override via file: `$DISPATCHER_CONFIG_TEMPLATE_PATH` (expand `<task-id>` → real TASK_ID. DURABLE WORKSPACE_SHARED. Outside worktree.) on a per-task basis.
**DO NOT create dispatcher config files INSIDE the worktree. All che sessions share the same DISPATCHER_LOCK_DIR. Che-ship §0.8 blacklist covers _locks and tasks/.*\.json patterns.**
