---
name: vibe-parallel
description: >
  Parallel task execution using Claude Code subagents. Reads task files,
  builds dependency waves, detects file conflicts AND read-write conflicts,
  and spawns tasks as parallel subagents. Size-aware wave splitting unlocks
  downstream tasks early when large tasks are in the same wave as small ones.
  If vibe-graph is installed, each subagent gets a graph-derived focus block
  (blast-radius files + rationale) on top of a shared cached baseline — precise
  scoping without blind spots, cheap via prompt caching.
  Structured subagent reporting with [x]/[~]/[!] states. Diagnostic retry on
  failure. Live wave progress log at vibe/parallel/. Post-wave graph update.
  Wave cost annotation for vibe-cost. Triggers on "parallel:" prefix,
  "run tasks in parallel", "spawn subagents", "parallelise the build",
  "which tasks can run in parallel", "run independent tasks simultaneously".
  Invoked by vibe-mode's autonomous-execution block (which vibe-new-app,
  vibe-add-feature, and vibe-fix-bug hand off to when VIBE_MODE=autonomous), or
  directly when the user runs `parallel:`. In manual mode the build skills do not
  call it automatically — the user opts in.
---

# Vibe Parallel Skill v2

Identifies independent tasks, builds dependency waves, and dispatches
each wave as parallel subagents via Claude Code.

**What's new in v2:**
- Read-write conflict detection (not just Touches field)
- Size-aware wave splitting (L tasks don't hold back S task dependents)
- Graph-aware context slicing per subagent (if vibe-graph installed)
- Structured subagent reporting with [x] / [~] / [!] states
- Diagnostic retry on failure (targeted, not blind)
- Live wave progress log written to vibe/parallel/
- Post-wave vibe-graph update
- Wave cost annotation for vibe-cost

---

## The principle

Independent tasks have no reason to run one after another.
If task B does not depend on task A — they run at the same time.
Subagents execute in parallel within the same Claude Code session.
The main session orchestrates: spawns waves, waits for completion,
unlocks the next wave, runs automatically until done.

---

## How it integrates with VIBE_MODE

```bash
grep "VIBE_MODE" CLAUDE.md 2>/dev/null | cut -d= -f2 | tr -d ' '
```

**VIBE_MODE=autonomous:**
Parallel detection runs automatically after every planning skill.
No prompt — if independent tasks exist, subagents spawn immediately.

**VIBE_MODE=manual (default):**
Shows the parallel plan. Asks once: "Run in parallel? (y/n)"
If `n` — sequential execution, user drives with `next`.
If `y` — subagents spawn.

**On-demand (`parallel:` command):**
Always shows the plan and asks — regardless of VIBE_MODE.
The user explicitly invoked it, so confirm before launching.

---

## Entry points

### Entry point A — On demand
Triggered by: `parallel:` prefix
Read `vibe/TASKS.md` for all pending tasks.
Always show plan + ask (y/n), regardless of VIBE_MODE.

### Entry point B — Called by vibe-add-feature
Source: `vibe/features/[date-slug]/FEATURE_TASKS.md`
VIBE_MODE=autonomous → skip prompt, launch directly.
VIBE_MODE=manual → show plan, ask (y/n).

### Entry point C — Called by vibe-fix-bug
Source: `vibe/bugs/[date-slug]/BUG_TASKS.md`
Same mode logic as Entry B.

### Entry point D — Called by vibe-new-app
Source: `vibe/TASKS.md` Phase 1 tasks only.
Same mode logic as Entry B.

### Entry point E — Called by the phase loop for a batch of features
Source: several `vibe/features/[date-slug]/FEATURE_TASKS.md` files — every feature the
autonomous phase loop planned as one batch (vibe-mode AUTONOMOUS_EXECUTION_BLOCK, "Run
the phase"). Parse all of them into **one** task pool (IDs are already unique by feature
prefix), build the waves across the pool as usual — the conflict passes are what keep
two features that write the same file apart — and mark each task `[x]` in its **own**
feature's file. Name the wave file after the phase (`Wave N — Phase P: feature A,
feature B`). Same mode logic as Entry B.

---

## Step 0 — Read project context

```bash
grep "VIBE_MODE" CLAUDE.md 2>/dev/null | cut -d= -f2 | tr -d ' '
mkdir -p vibe/parallel
```

Read `references/WAVE_BUILDER.md` — dependency graph and conflict detection logic.
Read `references/SUBAGENT_CONTEXT.md` — context slicing and prompt construction.
Read `references/REPORTING.md` — structured completion report format.

Read `vibe/ARCHITECTURE.md` — conventions every subagent must follow.

**Check for vibe-graph:**
```bash
ls vibe/graph/DEPENDENCY_GRAPH.json 2>/dev/null && echo "GRAPH_AVAILABLE" || echo "NO_GRAPH"
ls vibe/graph/.graph-meta.json 2>/dev/null && echo "META_AVAILABLE" || echo "NO_META"
```

Store result — used in Step 3 for context slicing.

---

## Step 1 — Parse tasks

Read the source task file in full.

**Where the metadata lives:** in `FEATURE_TASKS.md` / `BUG_TASKS.md` it is the
`**Size**` / `**Dependencies**` (or `**Depends on**`) / `**Touches**` fields. In
`vibe/TASKS.md` (Phase 1 and Phase 3) it is the indented line under each task:
`size: S|M|L · deps: [IDs or none] · touches: [files]`. When `touches` is `?` or missing,
write `"writes": null` in `tasks.json` — the wave engine then runs that task on its own
instead of guessing that it conflicts with nothing.

Extract for each pending `[ ]` task:

```python
tasks = []
for each task block:
    task = {
        "id":           "[TASK-ID]",
        "title":        "[Task title]",
        "size":         "S" | "M" | "L",
        "dependencies": [],           # list of TASK-IDs or []
        "touches":      [],           # files this task WRITES
        "reads":        [],           # files this task READS (infer if not explicit)
        "description":  "[What to do]",
        "criteria":     [],           # acceptance criteria list
        "spec_ref":     "[section]",
        "codebase_update": bool,
        "arch_ref":     "[which patterns apply]"
    }
    tasks.append(task)
```

**Inferring `reads` when not explicitly listed:**
A task Reads a file when any of these are true:
- The task description says "use", "call", "import", "extend", "read" a specific file
- The task type is "test" — it reads the file it's testing
- The task is a route handler — it reads the service/agent it calls
- The task is a component — it reads the model/API it consumes

If `reads` cannot be inferred confidently — leave empty and treat conservatively.

---

## Step 2 — Build dependency waves

Read `references/WAVE_BUILDER.md` for the full algorithm.

**Summary:**

**Pass 1 — Standard dependency resolution:**
```
Wave 1: tasks where dependencies = [] (or all deps already [x])
Wave 2: tasks whose deps are all in Wave 1
Wave N: tasks whose deps are all in Wave N-1
```

**Pass 2 — File conflict check (write-write):**
If two tasks in the same wave both WRITE the same file:
→ Move the alphabetically-later task ID to the next wave.
Exception: `vibe/CODEBASE.md` and `vibe/DECISIONS.md` — append-only, safe.

**Pass 3 — Read-write conflict check:**
If Task A WRITES a file and Task B READS that same file, and both are in the same wave:
→ Task B must move to the next wave — it needs Task A's output.
This catches inheritance, base class, and schema dependencies missed by Touches alone.

**Pass 4 — Size-aware wave splitting:**
Read `references/WAVE_BUILDER.md` for the full algorithm.

Short version: if Wave N contains an L task alongside S/M tasks, and some
Wave N+1 tasks depend only on the S/M tasks (not the L task) — those
Wave N+1 tasks can be promoted to run alongside the L task in Wave N as
a "fast lane." The L task and the promoted tasks run in parallel; the
remaining Wave N+1 tasks unlock after both the L task and fast lane complete.

**Minimum threshold:**
If Wave 1 has only 1 task → no parallelism available.
Autonomous mode: proceed sequentially, no mention of parallel.
Manual mode: proceed sequentially, no prompt shown.

---

## Step 3 — Build subagent context slices

Read `references/SUBAGENT_CONTEXT.md` for the full algorithm.

**Summary:**

For each task, build a context slice — the minimum context a subagent
needs to execute that task correctly.

**If vibe-graph is available:**
```python
def build_context_slice(task, graph, meta):
    slice = {
        "task_files":    task["touches"],
        "imports":       [],     # EXTRACTED deps of task files
        "concept":       None,   # concept node from CONCEPT_GRAPH
        "rationale":     [],     # WHY/DECISION nodes for task files
        "god_nodes":     [],     # god nodes in blast radius (extra care)
        "architecture":  [],     # relevant ARCHITECTURE.md patterns
    }

    for file in task["touches"]:
        node = graph.get(file, {})
        # Add EXTRACTED imports only
        for edge in node.get("imports", []):
            if isinstance(edge, dict) and edge.get("source") == "EXTRACTED":
                slice["imports"].append(edge["file"])
            elif isinstance(edge, str):
                slice["imports"].append(edge)
        # Add rationale
        slice["rationale"].extend(node.get("rationale", []))
        # Check concept
        if not slice["concept"]:
            slice["concept"] = node.get("concept")

    # Flag god nodes in the slice
    god_node_files = {gn["file"] for gn in meta.get("god_nodes", [])}
    for f in slice["imports"] + slice["task_files"]:
        if f in god_node_files:
            gn = next(gn for gn in meta["god_nodes"] if gn["file"] == f)
            slice["god_nodes"].append(gn)

    return slice
```

The graph slice is a **focus block layered on top of** a shared cached baseline
(ARCHITECTURE.md + CODEBASE.md), not a replacement for it — see
`references/SUBAGENT_CONTEXT.md` (Hybrid mode). It tells the subagent exactly
which files are in its blast radius and why (rationale), so it reads those fully
while the baseline gives it the whole map. This avoids the lossy-slice failure
mode (files not yet in the graph) that the token-savings-first design risked.

**If no vibe-graph:**
Provide CODEBASE.md + ARCHITECTURE.md; the subagent scopes from its task's
Touches list.

**Cost note:** keep the baseline prefix byte-identical across every subagent in
the wave so it's written to cache once and read back at ~10% cost for the rest
(see vibe-cost/references/PRICING.md → Cache economics). Cache-hit rate, not
slice size, is the dominant cost lever on current models.

---

## Step 4 — Present plan (manual mode only)

In autonomous mode — skip this step entirely.

```
⚡ PARALLEL EXECUTION PLAN

Wave 1 — [N] tasks run simultaneously:
  · [TASK-ID] (S) — [description]
  · [TASK-ID] (M) — [description]
  · [TASK-ID] (L) — [description]  ← long task

  Fast lane (runs with Wave 1 L task, unblocked early):
  · [TASK-ID] (S) — [description]  ← depends only on Wave 1 S/M tasks

Wave 2 — [N] tasks unlock when Wave 1 completes:
  · [TASK-ID] (M) — [description]

[Wave N...]

Conflict resolution:
  [TASK-ID] moved to Wave 2 — write conflict on src/models/brand_dna.py
  [TASK-ID] moved to Wave 2 — read-write conflict (reads base_agent.py written by [TASK-ID])

Context mode: [graph-aware slicing (vibe-graph) | full CODEBASE.md]
Est. time:    sequential ~[N]h → parallel ~[N]h (saving ~[N]h)
Est. cost:    [graph: ~$X per wave | no graph: ~$Y per wave]

Run in parallel? (y/n)
```

Wait for response. If `n` → exit, return to sequential flow.

---

## Step 5 — Initialise wave progress log

Before dispatching any subagent, write the initial status file:

```bash
mkdir -p vibe/parallel
cat > vibe/parallel/wave-[N]-status.md << 'EOF'
# Wave [N] — [feature/bug/phase name]
Started: [ISO timestamp]

## Tasks
| ID | Size | Status | Started | Completed | Duration |
|----|------|--------|---------|-----------|----------|
| [TASK-ID] | S | 🔄 running | [time] | — | — |
| [TASK-ID] | M | 🔄 running | [time] | — | — |
| [TASK-ID] | L | 🔄 running | [time] | — | — |

## Summary
Total tasks: [N]
Complete: 0
Failed: 0
Partial: 0

## Next wave
Wave [N+1] — waiting (unlocks when all Wave [N] tasks complete)
EOF
```

Update this file as each subagent reports completion.

---

## Step 6 — Execute wave as parallel subagents

Read `references/SUBAGENT_CONTEXT.md` for the full subagent prompt format.

**Build the subagent prompt for each task:**

```
You are executing [TASK-ID] as part of a parallel build.

═══ PROJECT CONTEXT ═══
[IF graph available:]
  Architecture patterns: [relevant sections from ARCHITECTURE.md]
  Your concept: [concept name] — [concept description from CONCEPT_GRAPH]

  Your files:
  [for each file in task touches:]
    [file_path] ([type])
    Imports: [EXTRACTED imports]
    [if rationale exists:]
    Rationale:
      [WHY/DECISION/HACK entries]

  [if god nodes in slice:]
  ⚠️ GOD NODE WARNING:
    [file] — [N] connections. Changes here affect [N] other files.
    Be especially careful with any modifications to this file.

[IF no graph:]
  Read vibe/CODEBASE.md and vibe/ARCHITECTURE.md for project context.

═══ YOUR TASK ═══
[Full task block verbatim from FEATURE_TASKS.md / BUG_TASKS.md / TASKS.md]

═══ SCOPE BOUNDARIES ═══
Files you MAY write:
  [Touches field contents]

Files you must NOT write (assigned to other parallel tasks):
  [all Touches fields from other Wave N tasks]

Files you MAY read (your imports):
  [slice imports list]

═══ COMPLETION REPORT ═══
When your task is complete, end your turn with a single fenced ```json block
matching this schema exactly (see references/REPORTING.md for the full spec).
Do NOT edit vibe/CODEBASE.md, DECISIONS.md, IMPLEMENTATION_LOG.md, TASKS.md, or CLAUDE.md
yourself — describe the deltas in the report; the main session applies them.

{
  "task_id": "[TASK-ID]",
  "status": "DONE" | "PARTIAL" | "FAILED",
  "files_modified": ["path", ...],
  "files_created": ["path", ...],
  "tests": { "passed": N, "total": N },
  "criteria": [ { "text": "...", "met": true|false, "note": "reason if unmet" } ],
  "codebase_update": "what changed, for the main session to record | ",
  "blockers": ["anything downstream tasks must know", ...],
  "rationale_added": "WHY/DECISION comments added | ",
  "decisions": [ { "title": "...", "why": "why this / why this lib / what was rejected",
                   "touches": "files or functions" }, ... ],   // [] if none meaningful
  "error": "failure detail | null"
}
```
`decisions` carries only MEANINGFUL implementation choices (hard to reverse · picked among
real alternatives · would surprise a future reader) — routine work reports `[]`. The main
session promotes them into vibe/IMPLEMENTATION_LOG.md after the wave.
Where the runtime supports schema-validated output/tool calls, this schema is
bound with `strict: true` so the shape is guaranteed.

**Dispatch all tasks in the wave simultaneously as subagents.**

**Parse completion reports:**

Read `references/REPORTING.md` for the full parsing logic.

For each subagent completion report:

```python
def parse_completion(report):
    status = extract("STATUS", report)
    criteria = parse_criteria(report)
    unmet = [c for c in criteria if not c["met"]]

    if status == "DONE" and not unmet:
        return "COMPLETE"    # mark [x]
    elif status == "PARTIAL" or unmet:
        return "PARTIAL"     # mark [~]
    elif status == "FAILED":
        return "FAILED"      # mark [!], trigger diagnostic retry
```

**Task states:**
- `[x]` — fully complete, all criteria met, tests passed
- `[~]` — partially complete, some criteria unmet — downstream tasks are WARNED
- `[!]` — failed — trigger diagnostic retry

---

## Step 7 — Handle failures and partial completions

### Partial completion [~]

A task is partial when:
- All code is written but one or more acceptance criteria not met
- Tests pass but not all criteria are verifiable automatically
- Task completed but CODEBASE.md update was skipped

**Action:**
Log the unmet criteria in the wave progress file.
Warn downstream tasks in their subagent prompts:
```
⚠️ UPSTREAM WARNING from [TASK-ID]:
   [criterion] was not fully met: [reason]
   Your task may need to account for this — verify before marking done.
```
Do NOT block downstream tasks. Propagate the warning.

### Hard failure [!]

A task fails when: STATUS=FAILED, or tests fail, or the subagent errors out.

**Diagnostic retry (not blind retry):**

Read `references/REPORTING.md` for the diagnostic extraction logic.

```python
def build_diagnostic_retry(task, failure_report):
    # Extract the specific error
    error = extract_error(failure_report)
    # Infer most likely cause
    cause = diagnose(error, task)
    # Build targeted retry
    return f"""
RETRY — [TASK-ID]

Your previous attempt failed:
  Error: {error}
  Most likely cause: {cause}

Targeted approach for this retry:
  {targeted_fix(cause, task)}

[Original task prompt]
[Same scope boundaries]
[Same completion report format]
"""
```

On retry → if COMPLETE: mark `[x]`, continue.
On retry → if still FAILED: mark `[!]`, stop wave, surface to human.

**Stop condition:**
Any task that fails twice stops the entire wave.
Do not proceed to the next wave.
First record the stop so anyone outside the session can see it (vibe-mode
`references/HEADLESS.md` §4):
```bash
python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py run-state set --status needs_human \
  --phase [N] --reason "[TASK-ID] failed after retry: [root cause]" --next "fix, then resume"
```
Then report clearly:

```
🔴 WAVE [N] PAUSED

[TASK-ID] failed after retry.
Error: [specific error from second attempt]

Completed tasks this wave: [list — marked [x] in task file]
Partial tasks: [list — marked [~]]
Failed task: [TASK-ID]

Fix the failure, then say "resume" to continue with Wave [N+1].
The completed tasks do not need to be re-run.
```

---

## Step 8 — Update task file and progress log

After all subagents in the wave complete (or fail):

**Update FEATURE_TASKS.md / BUG_TASKS.md / TASKS.md:**
```
[x] TASK-001 · [description]   ← complete
[~] TASK-002 · [description]   ← partial — [unmet criterion]
[!] TASK-003 · [description]   ← failed — [error summary]
```

**Update CODEBASE.md (batched — main session only):**
Collect all `FILES_MODIFIED` and `FILES_CREATED` from completion reports.
The main session updates `vibe/CODEBASE.md` once — not during parallel execution.
Each subagent reports what it changed; the main session writes the update.

**Promote decisions to IMPLEMENTATION_LOG.md (batched — main session only):**
Collect every non-empty `decisions` array from the completion reports and append one
`## D-NNN` entry per decision to `vibe/IMPLEMENTATION_LOG.md`, per that file's header
schema (newest last; map `title`→heading, `why`→Why/alternatives, `touches`→Touches, and
set Date/cycle to the wave's task id). De-duplicate if two subagents reported the same
choice. Skip empties — most tasks report `[]`. Subagents never write this file themselves.

> Subagents must **never** write the main-session-owned files directly —
> `vibe/CODEBASE.md`, `vibe/DECISIONS.md`, `vibe/IMPLEMENTATION_LOG.md`, `vibe/TASKS.md`, `CLAUDE.md`. They
> report deltas in their completion report and the main session applies them
> after the wave. This is why those files are skipped in write-conflict
> detection (see `references/WAVE_BUILDER.md` → `MAIN_SESSION_OWNED_FILES`):
> no concurrent subagent write ever lands on them, so there is nothing to
> corrupt. Two subagents both "touching" CODEBASE.md is not a conflict.

**Update wave progress log:**
```markdown
# Wave [N] — complete
Started: [time] · Completed: [time] · Duration: [Xm Ys]

## Tasks
| ID | Size | Status | Started | Completed | Duration |
|----|------|--------|---------|-----------|----------|
| TASK-001 | S | ✅ complete | 14:23:00 | 14:23:42 | 42s |
| TASK-002 | M | 🟡 partial  | 14:23:00 | 14:24:15 | 75s |
| TASK-003 | L | ❌ failed   | 14:23:00 | 14:26:00 | 3m |

## Summary
Total tasks: 3 · Complete: 1 · Partial: 1 · Failed: 1

## Unmet criteria
TASK-002: [criterion] — [reason]

## Files modified this wave
[complete list from all completion reports]

## Cost
Subagent tokens: ~[N] (estimated)
Context mode: graph-aware slicing
Approx cost: ~$[X]
vs sequential: ~$[Y] (parallel [cheaper/more expensive] by $[delta])
Time saved vs sequential: ~[N] minutes
```

**Update vibe/TASKS.md "What just happened":**
```
✅ Wave [N] complete — [N] tasks done · [N] partial · [N] failed
   [task IDs]
   Cost: ~$[X] · Time saved: ~[N]min
```

---

## Step 9 — vibe-graph update (post-wave)

After each wave completes, run one graph update:

```
vibe-graph: update
```

The git diff captures all subagent writes in a single pass.
More reliable than each subagent updating the graph independently —
subagents can't safely write the same JSON file concurrently.

If vibe-graph not installed — skip this step silently.

---

## Step 10 — Execute remaining waves

For each subsequent wave:

**Check if wave is unlocked:**
All tasks in this wave have their dependencies marked `[x]`.
Tasks depending on a `[~]` partial task — include the upstream warning in their prompt.
If any dependency is `[!]` — that wave cannot proceed. Stop.

**Apply size-aware splitting to subsequent waves too.**

**Repeat Steps 5–9 for each wave.**

Wave with 1 task → run as single subagent (no parallelism, but still automatic).
Wave with 2+ tasks → parallel subagents.

---

## Step 11 — All waves complete

**Emit cost summary:**

```
⚡ Parallel execution complete

Waves:
  Wave 1: [N] tasks ✅ · [N]m [N]s · ~$[X]
  Wave 2: [N] tasks ✅ · [N]m [N]s · ~$[X]

Totals:
  Tasks complete: [N]/[N]
  Tasks partial:  [N] (see vibe/parallel/ for unmet criteria)
  Time taken:     [Xm]
  Est. sequential: ~[N]h
  Time saved:     ~[N]h ([N]% faster)
  Total cost:     ~$[X]
  Context mode:   [graph-aware | full CODEBASE.md]

Progress log: vibe/parallel/
```

**In autonomous mode:**
Signal completion to the calling skill.
Do not stop — let vibe-add-feature / vibe-fix-bug / vibe-new-app
invoke the review gate automatically.

**In manual mode:**
```
Run review: to gate this phase.
```

---

## Absolute rules

**Never give two subagents the same file to write.**
Write-write conflicts caught in Step 2 Pass 2 before any subagent launches.

**Read-write conflicts are real conflicts.**
Task B reading a file Task A writes — Task B must wait.
Caught in Step 2 Pass 3. Never skipped.

**Each subagent is completely isolated.**
No subagent reads another subagent's in-progress work.
They read the codebase as it existed before Wave 1 started.
Results merged by main session after wave completes.

**[~] partial tasks never block — they warn.**
A partial task passes its unmet criteria as warnings to downstream tasks.
Downstream tasks decide how to handle. They are not blocked.

**[!] failed tasks always stop the wave.**
On second failure — stop, report clearly, wait for human.
Never mark a task [x] if tests did not pass.

**CODEBASE.md updates are batched by the main session.**
Each subagent reports changes. Main session writes CODEBASE.md once.
This prevents concurrent JSON write conflicts.

**Graph updates happen once per wave — not per subagent.**
`vibe-graph: update` runs after wave completion.
Git diff captures all subagent writes accurately.

**Autonomous mode never skips the review gate.**
When all waves complete, signal for review.
It runs automatically, but it always runs.

**Cost annotation is always included.**
Every wave completion includes token estimate and cost.
Even if vibe-cost is not installed — the annotation is written
to the progress log so vibe-cost can read it later.
