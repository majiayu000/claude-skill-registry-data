---
name: where-are-we-at
description: >-
  Answer "where are we at on <topic>?" with a deep ground-truth assessment of a module, feature, or subsystem. Cuts through
  stale documentation and superficial LLM scans by orchestrating /recon (codebase architecture & live
  symbols), /debug-mantra (empirical breadcrumb observation), and /merge-cleanup (multi-checkout,
  active sessions, tick claims, and PR detection) into a verified status report.
metadata:
  argument-hint: "<topic, module, issue, or subsystem>"
---

# /where-are-we-at — Deep Ground-Truth Topic, Module & Subsystem Status Assessment

`/where-are-we-at` delivers an authoritative, empirical status evaluation of any topic, module, feature,
or subsystem within a codebase.

Superficial LLM scans often hallucinate completeness or recite stale documentation: they read an
outdated markdown roadmap or architecture guide, perform a superficial grep in the current working
directory, and miss unlanded branches, active worktrees, in-flight PRs, or silent regressions.

`/where-are-we-at` solves this by orchestrating three core disciplines into an empirical verification ladder:
1. **[`/merge-cleanup`](../merge-cleanup/SKILL.md) (Multi-Checkout & Session Reality):** Audits active
   worktrees, task clones (`~/agent-workspaces`, `~/marathon-clones`), active `.tick` claims, driver locks,
   and open GitHub PRs (`gh pr list`).
2. **[`/recon`](../../1-hourly/recon/SKILL.md) (Architecture & Symbol Seams):** Traces actual entry points,
   callers, state readers/writers, contracts, tests, and centralized helper adherence. Employs the
   `codebase-memory-mcp` knowledge graph when indexed, confirmed against live source.
3. **[`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md) (Ground-Truth Observation & Disproof):**
   Treats documentation as a hypothesis-zero claim rather than evidence. Inspects primitive artifacts
   (raw source, database schemas, test receipts, recent commits via `git log -n 10 -- <paths>`).

---

## Recite this — verbatim, as the first thing in your first response

> **Status Discipline:**
> 1. **Scan multi-checkout & active session reality (Phase 1 /merge-cleanup).** Audit across safe roots (`~/agent-workspaces`, `~/marathon-clones`, worktrees) for active worktrees, driver locks, `.tick` claims, and open PRs (`gh pr list`). Do not rely solely on the current checkout.
> 2. **Trace live codebase architecture & seams (Phase 2 /recon).** Map real entry points, callers, state mutations, contracts, and tests. Query the knowledge graph (`codebase-memory-mcp`) when indexed and confirm against live source.
> 3. **Verify ground-truth breadcrumbs & disprove stale claims (Phase 3 /debug-mantra).** Inspect primitive artifacts directly (raw source, DB rows, test receipts, `git log -n 10 -- <paths>`). Falsify documentation claims against actual code reality.
> 4. **Synthesize empirical status report (Phase 4).** Emit structured status comparing documented claims vs actual implementation reality, active checkouts, test receipts, and verified capabilities.
>
> **Overall Goal:** Deliver an up-to-date, grounded status verdict of any topic or subsystem, exposing the gap between stale documentation and live implementation reality.

Then begin work.

---

## Conversational Triggers

Trigger `/where-are-we-at` when the operator asks:
- `"Where are we at on <topic>?"`
- `"What is the status of <topic/subsystem>?"`
- `"Check the status of <module>"`
- `"How far along is <feature>?"`
- `"Is the doc/plan for <feature> up to date with reality?"`
- `"Dig deeper on <subject> — don't just read the doc"`
- `"Are there active worktrees or open PRs touching <area>?"`

---

## The 4-Phase Status Ladder

```text
Phase 0: Target Intake & Scope Resolution  ──► Resolve subject: feature, module path, GH issue #, or subsystem
                 │
                 ▼
Phase 1: Multi-Checkout & Session Recon   ──► Scan safe roots (clones, worktrees), locks, tick claims, open PRs
         (/merge-cleanup lens)
                 │
                 ▼
Phase 2: Codebase Architecture & Seams     ──► Map live symbols, callers, state, contracts, tests (MCP graph + read)
         (/recon lens)
                 │
                 ▼
Phase 3: Ground-Truth Verification         ──► Primitive artifact inspection, recent git logs, test receipts,
         (/debug-mantra lens)                  falsify stale doc claims against live code reality
                 │
                 ▼
Phase 4: Deep Status Synthesis Report     ──► Ground-Truth vs Stale Doc Gap, Active Checkouts, Test Health, Verdict
```

---

## Phase 0: Target Intake & Scope Resolution

Resolve the exact topic under investigation:
- **Symbol / Module:** File path or package namespace (e.g. `utils/py/releases_app.py`, `relay-automation`).
- **Feature / Subsystem:** Named workflow or runtime area (e.g. `marathon-drive`, `express`, `AgentChorus`).
- **Issue / Planning Ticket:** GitHub issue number or PDDA tracking document (e.g. `GH-778`, `PROJECT/2-WORKING/`).

State the target scope in one line and establish the baseline inspection criteria.

---

## Phase 1: Multi-Checkout & Session Recon ([`/merge-cleanup`](../merge-cleanup/SKILL.md))

A major source of stale status reports is assuming the working tree at CWD is the only place work
exists. Active agents frequently work in linked worktrees or dedicated task clones.

Audit across the environment:
1. **Linked Worktrees:** Run `git worktree list --porcelain` in the primary checkout. Are there linked worktrees
   touching the target files or branches?
2. **Task Clones across Safe Roots:** Inspect `~/agent-workspaces/`, `~/marathon-clones/`, and `~/Documents/GH Repos/`.
   Check if any clone has a branch or uncommitted edits matching the subject.
3. **Active Driver Locks (Shared Git Common Dir Resolution):**
   - Resolve the lock path via the shared coordination root (`merge-cleanup` / `WORKTREE-SAFETY.md` contract):
     - Normal clone: `<root>/.git/relay-driver.lock`
     - Linked worktree: `<git-common-dir>/relay-driver.lock` (the parent clone's common dir, never worktree-local)
     - Vendored: `<root>/.relay-driver.lock`
   - Validate PID liveness via `kill -0 <pid>`. If held by a live PID, report active driver holder; if query unreadable, report as Unknown.
4. **Active Coordination Claims (Parent Coordination Root Pin):**
   - Inspect `.tick/` active claims through the event log fold, pinned to the coordination root (`TICK_REPO_ROOT`):
     ```bash
     TICK_REPO_ROOT="<coord-root>" "<coord-root>/bin/tick" claims --json
     ```
   - A linked worktree's coordination root is its parent clone's root. Any active claim names the task and agent.
   - If `tick` is unavailable or errors, report as `Unknown (coordination fold unreadable)`, never default to "None" (fail-closed principle).
5. **Open Pull Requests & Issues:** Run:
   ```bash
   gh pr list --state open --search "<subject>"
   gh issue list --state open --search "<subject>"
   ```
   Determine if the latest developments are currently staged on a remote branch rather than merged to `development`.
6. **Recency Ladder:** Check recent non-ephemeral file modifications (`mtime` ignoring `.git`, `node_modules`):
   - `ACTIVE_WRITING` ($\le 10$m)
   - `RECENT_IDLE` ($10\text{m} - 60\text{m}$)
   - `DORMANT` ($> 60$m)

---

## Phase 2: Codebase Architecture & Seam Recon ([`/recon`](../../1-hourly/recon/SKILL.md))

Map the real code footprint rather than accepting architectural descriptions at face value:
1. **Knowledge Graph Seeding:** If `codebase-memory-mcp` is available:
   - Call `search_graph` to locate actual classes, functions, routes, and variables.
   - Call `trace_path` to map inbound callers and outbound dependencies.
   - Call `check_index_coverage` to verify the freshness of the indexed symbols.
2. **Live Seam Verification:** Confirm every graph edge by reading source at `file:line`:
   - **Lane A (Callers):** Who actually calls this code today? Are calls active or dead paths?
   - **Lane B (State):** What data stores, SQLite tables, or disk paths does it read or mutate? Single writer?
   - **Lane C (Contracts):** What public CLI flags, JSON schemas, or APIs are exposed?
   - **Lane D (Tests):** What test suites exist under `test/`? Are they registered in `validate.sh`?
   - **Lane E (Centralized Helpers & DRY):** Does the module use canonical helpers (e.g. `utils/py/`, runtime libs)
     or does it construct parallel redundant machinery?

---

## Phase 3: Ground-Truth Verification & Stale Claim Disproof ([`/debug-mantra`](../../1-hourly/debug-mantra/SKILL.md))

Documentation easily rots. In this phase, rigorously falsify documentation claims against live reality:

1. **Mantra 1 — Observe Primitive Ground Truth:**
   - A doc in `PROJECT/` or `ARCHITECTURE.md` that says *"Feature X is implemented via Y"* is an **unverified claim**.
   - Check the primitive artifact: Does the file exist? Does the function exist? Does it actually execute, or is it an empty stub/TODO?
   - If SQLite tables are involved, inspect the schema (`.schema`) or query rows directly; do not trust markdown tables.
2. **Mantra 4 — Cross-Reference Every Breadcrumb:**
   - Run `git log -n 10 --oneline -- <paths>` to observe the last 10 real commits touching the code.
   - Cross-reference `CHANGELOG.md` to see when features were landed or deprecated.
   - Check `TESTS-RESULTS/` for committed `provenance.jsonl` execution receipts.
3. **The Stale-Claim Disproof Test:**
   - Find statements in project docs or READMEs claiming functionality.
   - For each claim, formulate a clean disproof check: *What command would fail if this doc is obsolete?*
   - Execute the check. Document any discrepancy where docs claim capabilities that are broken or missing in code.

---

## Phase 4: Deep Status Synthesis & Report

Structure findings into a comprehensive Ground-Truth Status Report:

```markdown
# 🔍 Status Report: <Topic / Module / Subsystem>

**Verdict:** `Implemented & Tested` | `In-Flight / Active Work` | `Stale / Drifted` | `Planned Only` | `Deprecated`
**Primary Branch:** `<branch>` | **HEAD Commit:** `<sha>`
**Inspection Mode:** `Empirical Multi-Checkout Ground Truth (/merge-cleanup + /recon + /debug-mantra)`

---

## ⚡ Executive Summary
[2–3 concise sentences giving the bottom line: true state, freshness, and immediate blockers.]

---

## 📊 Ground Truth vs. Documentation Gap Matrix

| Feature / Capability | Documented Claim | Ground-Truth Code Reality | Discrepancy / Drift Status |
|:---|:---|:---|:---|
| Lock acquisition | "Uses per-worktree lock" | `utils/py/rtl.py:45` uses git common dir | ✅ Doc stale; code upgraded (GH-376) |
| CLI flag `--dry-run` | "Supported across all verbs" | Missing in `subcommand_land()` | 🛑 Broken / Missing in code |
| Regression suite | "Covered by test/gh123.sh" | Suite registered; successful receipt tied to tested SHA | ✅ Verified passing (receipt rc=0 at <sha> in TESTS-RESULTS/) |
| Stale/Failed test | "Covered by test/gh789.sh" | Suite registered; receipt records failure or older SHA | 🛑 Defect / Stale (receipt rc!=0 or sha mismatch) |
| Integration tests | "Covered by test/gh456.sh" | Suite registered, but no execution receipt | ⚠️ Coverage present, execution unverified (needs run) |

---

## 🗂️ Active Checkouts & In-Flight Work
- **Primary Checkout:** Clean / Dirty (`N` uncommitted files).
- **Linked Worktrees:** `[None | Path (branch, agent, state)]`.
- **Task Clones:** `[None | ~/agent-workspaces/... (unpushed commits)]`.
- **Active .tick Claims / Locks:** `[None | Task-ID held by agent]`.
- **Open PRs & Issues:** `[None | PR #N: title (status, author)]`.

---

## 🏗️ Codebase Architecture & Seams
- **Core Implementation:** `file:line` citations of primary classes and entry points.
- **Inbound Callers:** Verified callers across CLI and test harnesses.
- **State & Data Invariants:** Single-writer verified; persistence sinks identified.
- **Centralized Helper Adherence:** Canonical utilities used; zero parallel subsystems detected.

---

## 🔬 Test Coverage & Verification Receipts
- **Automated Regression Suites:** `test/gh<N>-<slug>.sh` (registered in `validate.sh`: Yes/No).
- **Recent Landed Evidence:** Commit `<sha>` with `provenance.jsonl` receipt in `TESTS-RESULTS/`.
- **Live Test Execution Result:** [PASS/FAIL exit code and timing].

---

## ⚠️ Unknowns & Actionable Next Steps
- [ ] Unknown: `<unverified edge or remote state>` — Settled by: `<exact command>`
- [ ] Action: `<next operational or engineering step>`
```

---

## Operating Rules & Safety Rails

1. **Lead with the line that survives skimming:** State the overall status verdict and active work locations in the very first sentence.
2. **A doc is a hypothesis-zero claim, never evidence:** Never report that a feature exists simply because a README, plan, or PRD says so. Verify the live code and runnable tests.
3. **The local checkout is not the only checkout:** Always run Phase 1 multi-checkout discovery to catch work in linked worktrees or task clones before concluding work is missing.
4. **Graph and greps are leads, not citations:** Every cited symbol or caller must be confirmed by reading the file at `file:line`.
5. **Verified beats plausible:** If tests cannot be run or state is inaccessible, state it explicitly as an **Unknown**, never assume.
6. **Throwaway Full-Clone Isolation (GH-564 rail):** If running test suites to verify status, execute them in a disposable full clone; never run mutation-heavy gates in a primary checkout or linked worktree.
7. **Frozen Bash twins (GH-308 rail):** All Tier-A harness status queries examine Python implementations in `utils/py/`, not frozen `.sh` twins.
