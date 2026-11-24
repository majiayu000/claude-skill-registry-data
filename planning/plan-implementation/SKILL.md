---
name: plan-implementation
description: "Generates the ceremonial master implementation plan from a ratified design document. Maps exact task distributions across swarm personas, concurrency and distributed locking schedules using Rhizo monotonic fencing tokens, and workspace virtualization using Vine strands. Establishes dynamic progress tracking via markdown task checklists, synchronization with native coding harness To-Do tools, and the Emergent Design Addendum Protocol. Triggers: 'plan implementation', 'create implementation plan', 'schedule swarm work', 'build execution plan'."
---

# `plan-implementation`: Ceremonial Implementation Planning & Locking Schedules

> **Bridging the Architectural Spec to Synchronized Swarm Execution**  
> *A plan is not a wish list; it is a deterministic state machine. It dictates who works on what, what locks prevent collisions, which branches isolate code, and how progress is tracked in real time.*

---

## 1. Core Principles & Architecture

The Orchestrator authors `implementation_plan.md` adhering to four core invariants:

1. **Deterministic Assignment**: Every subtask has exactly one primary persona owner.
2. **Resource Fencing Before Mutation**: Any non-mergeable resource (e.g. database schemas, configuration files, migration scripts) must have an explicit `rhizo lock file:<path> --fencing` lease scheduled before modification begins.
3. **Workspace Isolation via Vine & Feature Integration Branch (`epic/<slug>`)**: Complex, multi-file changes must occur in isolated Rift strands branching off the feature integration branch (`vine new <task_id> --parent epic/<slug>`). Strands cannot be woven until passing the Three-Key Gate (`vine submit`, `vine audit inspect`, `vine audit approve`, `vine weave`).
4. **Contract Skeleton Anchoring & Immutability**: Every implementation plan must anchor tasks directly to the committed types, interfaces, callable stubs (`UNIMPLEMENTED_CONTRACT`), and red contract test suites established during Stage 3.5 on `epic/<slug>`.
   - *Contract Immutability*: Workers branching off `--parent epic/<slug>` MUST NOT alter exported type declarations or signatures, nor weaken contract tests, without an approved `[DESIGN ADDENDUM]`.
   - *Anti-Mock-Fallback*: Workers must NEVER implement silent mock fallbacks (e.g. `lesMockFallback`); missing dependencies require immediately halting with `BLOCKER: MISSING_DEPENDENCY`.
5. **Auditor Merge-Clerk Decoupling & Inverted Effort Gradient**: The independent Adversarial Auditor ONLY inspects and ratifies Key 3 (`vine audit inspect` + `vine audit approve/reject`). Rejection is the fast path for any defect (`vine audit reject`); approval requires `--evidence "..."` citing changed files, call-sites, and negative controls. Using `--force` on audit approvals is strictly prohibited. The Auditor NEVER runs `vine weave`, NEVER edits `ROADMAP.md`, and NEVER resolves `CHANGELOG.md` merge conflicts on behalf of workers. Weaving is strictly the Lead Orchestrator's role.
6. **Zero Silent Architectural Drift**: If an implementer encounters an unforeseen constraint during coding, it cannot unilaterally alter the architecture. It must submit a formal design addendum.
7. **Closed-Circuit Two-Point Diff & Holistic Integration**: Every task specification must declare both the **Provider** (new capability) and the active **Consumer Call-Site** (runtime entrypoint, router, UI canvas, or CLI loop). Modules tested only by isolated unit tests are strictly prohibited as incomplete shelfware. The implementation must holistically integrate with real application state and live events (no toys, stubs, mocks, or hollow approximations). Any code intended to be replaced must be explicitly scheduled for **immediate deletion** in the same strand—never kept as a vestigial fallback or commented-out logic.

---

## 2. Structure of `implementation_plan.md`

The generated implementation plan must follow this exact template:

```markdown
# Implementation Plan: [Feature / Project Name]

## 1. Swarm Roster & Role Mapping
| Swarm Role (@tag) | Unique Listener Codename | Persona | Role Title | Assigned Subsystems |
| :--- | :--- | :--- | :--- | :--- |
| `@architect` | `<project>-sequoia` | Bramblestitch (or topical spirit) | Staff Systems Architect | Core data structures, API contracts |
| `@auditor` | `<project>-kestrel` | Prickle-Thistle (or topical spirit) | Verification & Adversarial Auditor | Unit tests, negative controls, Key 3 audit |
| `@implementer` | `<project>-falcon` | Moss-Weaver (or topical spirit) | DevEx & Implementation Lead | CLI commands, adapters, docs |

---

## 2. Distributed Locking & Concurrency Schedule
Before modifying any shared or non-mergeable file, the designated worker must obtain an atomic lease:
- **Lock Target**: `file:src/config.nim`
  - *Owner*: `@architect` (`<project>-sequoia`)
  - *Command*: `rhizo lock file:src/config.nim 600 --fencing`
  - *Monotonic Fencing Counter*: Record token in task execution log.
- **Lock Target**: `file:migrations/001_schema.sql`
  - *Owner*: `@implementer` (`<project>-falcon`)
  - *Command*: `rhizo lock file:migrations/001_schema.sql 300 --fencing`

---

## 3. Vine Strand Lifecycle & Verification Matrix
For all parallel development tracks:
1. **Provision Strand Branching off Feature Integration Branch (`epic/<slug>`)**:
   ```bash
   vine new <task_id> --parent epic/<slug> --worktree
   ```
   *Note: Vine stores strand identity in `.git/config` (`vine.taskId`, `vine.project`) and authoritative state in Redis (zero on-disk `.vine.json` state files).*
2. **Execute Work Inside Strand Under Contract Immutability**:
   - Implement real provider logic turning committed red contract stubs into green passing code.
   - Do NOT modify exported contract signatures or weaken contract tests without an approved `[DESIGN ADDENDUM]`.
   - Never implement fake mock fallbacks (`lesMockFallback`); halt with `BLOCKER: MISSING_DEPENDENCY` if dependencies are unavailable.
   - Run local unit tests and formatters.
3. **Three-Key Gate Verification**:
   - **Worker**: Runs `vine submit --author <worker>` (evaluates Key 1 mechanical merge-tree + Key 2 live compiler/test suite + changelog, and stamps cryptographic delivery ticket / `gate_token`).
   - **Independent Auditor**: Inspects Five Pillars and runs:
     ```bash
     # Step 1: Mandatory forensic inspection
     vine audit inspect <task_id>
     # Step 2: To ratify approval with evidence (Auditor NEVER weaves):
     vine audit approve <task_id> --auditor <auditor> --ticket <hex> --evidence "<files, call-sites, negative controls>" --listen
     # Or to reject if defects are found:
     vine audit reject <task_id> --auditor <auditor> --ticket <hex> --reason "<findings>" --listen
     ```
     *(Note: In Multiplexed Router harnesses such as Google Antigravity, OpenCode, and Pi, per-turn `--listen` re-arming is handled automatically by the host `rhizo router` service).*
     Remember: THE WORKER IS NOT THE AUDITOR. Auditors NEVER use `--force` and NEVER act as release/merge clerks (no editing `ROADMAP.md`, no resolving `CHANGELOG.md` merge conflicts, and no weaving on behalf of workers).
4. **Trunk Weaving & DAG Cascading (Lead Orchestrator Role)**:
   *Fast-forwards ratified branch into epic/<slug> or main, automatically calls `rhizo task complete <task_id>`, and unblocks downstream DAG child tasks (`BLOCKED` $\rightarrow$ `QUEUED`):*
   ```bash
   vine weave
   ```

---

## 4. Phase-by-Phase Task Checklist

### Phase 0: Contract Skeleton (Pre-Plan Stage 3.5 on `epic/<slug>`)
- [x] **Task 0.1: Contract Skeleton Strand & Red Tests** (`@architect`)
  - *Strand*: `strand/task-<slug>-skeleton` (`--parent epic/<slug>`)
  - *Committed Deliverables*: Idiomatic types, interfaces, and callable stubs with `UNIMPLEMENTED_CONTRACT` in `src/types.nim`, `src/api.nim`
  - *Committed Contract Tests*: `tests/test_contract.nim` asserting contract compliance (failing red against stubs)
  - *Weave*: `vine submit --skeleton && vine audit inspect task-<slug>-skeleton && vine audit approve task-<slug>-skeleton && vine weave`

### Phase 1: Core Engine Primitives (Branching off `epic/<slug>`)
- [ ] **Task 1.1: Core Data Structures** (`@architect`)
  - *Strand*: `strand/task-core-ds` (`--parent epic/<slug>`)
  - *Anchored Skeleton Symbols*: `src/types.nim:15-80` (`ASTNode`, `NodeKind`, `serializeNode`)
  - *Contract Test Suite*: `tests/test_contract.nim` (must turn from red to green)
  - *Lock*: `rhizo lock file:src/types.nim 300 --fencing`
  - *Provider*: `src/types.nim` (AST node kinds and serializers)
  - *Consumer / Call-Site*: Wire into `src/parser.nim` parse loop and `src/eval.nim`
  - *Replacement Deletion*: Delete deprecated ad-hoc string tuples in `src/legacy_types.nim`
  - *Holistic Verification*: Real AST nodes evaluate in full parser pipeline (no dummy mocks)
  - *Weave*: `vine submit && vine audit inspect task-core-ds && vine audit approve && vine weave && rhizo unlock file:src/types.nim`

- [ ] **Task 1.2: Test Harness & Negative Controls** (`@auditor`)
  - *Strand*: `strand/task-test-harness` (`--parent epic/<slug>`)
  - *Provider*: `tests/test_harness.py`
  - *Consumer / Call-Site*: Wire test runner into CI workflow and `tests/all.py`
  - *Verification*: `pytest tests/test_harness.py` (proves negative controls catch malformed JSON)
  - *Weave*: `vine submit && vine audit inspect task-test-harness && vine audit approve && vine weave`

### Phase 2: High-Level CLI & Integration
- [ ] **Task 2.1: CLI Subcommand Wiring** (`implementer`)
  - *Dependency*: Task 1.1, Task 1.2
  - *Strand*: `strand/task-cli-wiring`
  - *Provider*: `src/commands/generate.nim`
  - *Consumer / Call-Site*: Wire into `src/main.nim` CLI argument dispatcher table
  - *Replacement Deletion*: Delete old prototype script `scripts/gen_proto.sh`
  - *Holistic Verification*: Run compiled binary `app generate --input data.json` and verify live output
  - *Weave*: `vine submit && vine audit approve && vine weave`

---

## 5. Dynamic Progress Tracking & Harness To-Do Protocol
1. **Markdown Checkboxes**:
   - As each task begins, the orchestrator updates status notes.
   - When verified woven, the orchestrator changes `- [ ]` to `- [x]`.
2. **Harness To-Do Synchronization**:
   - If the runtime harness provides native To-Do tools (e.g. `todo_write`, `manage_tasks`), the orchestrator mirrors the active phase tasks into the harness's To-Do list.
   - Mark items complete in the harness tool at the moment of `vine weave`.

---

## 6. Emergent Design Addendum Protocol
If a worker discovers that an assumption in `design.md` is flawed or impossible to implement:
1. **DO NOT silently diverge code from `design.md`**.
2. Draft an addendum document: `docs/addenda/addendum_<topic>.md`:
   - *Problem Statement*: Why the original design cannot work as specified.
   - *Proposed Deviation*: Exact technical changes.
   - *Tradeoff Analysis*: Performance, ergonomics, backwards compatibility.
3. Submit notification to Orchestrator via `rhizo send --to orchestrator --subject "Design Addendum: <topic>"`.
4. Orchestrator reviews and ratifies the addendum, updates `design.md`, updates `implementation_plan.md`, and replies with approval before implementation resumes.
```

---

## 3. Plan Review & Gate Clearance

Before handing off to [`orchestrate-swarm`](../orchestrate-swarm/SKILL.md):
1. Assert that every task names a concrete persona owner.
2. Assert that all shared files have fencing locks scheduled.
3. Assert that all tasks requiring branch isolation specify `vine new`, `vine submit`, and `vine audit approve`.
4. Save file to `implementation_plan.md` in the project root.
