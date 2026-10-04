---
name: bootstrap-monorepo
description: Use when a folder containing several autonomous Git repos (each with its own CDev) must be conditioned as a CDev Monorepo orchestrating workspace — creating the global scaffolding (AGENTS.md, docs/develop/, workspace/, agents, scripts, the workspace's own git) without touching the child repos, or when the user asks to "bootstrap monorepo", "condition a multi-repo workspace", "condicionar workspace multi-repo", or to set up orchestration over existing repos.
---

# Bootstrap Monorepo (CDev)

Conditions a **multi-repo workspace** (colloquially "monorepo") as a CDev orchestration layer.
It does not merge the repos into a single Git nor replace their local CDev. Guiding principle:

> **The workspace governs coordination. Each repository governs its implementation.**

The unit of coordination is the **repository**, not the technology or the target. A repo with
web+mobile inside is ONE unit; its internal parity is its local CDev's business. The workspace
never creates per-technology agents ("backend agent", "web runner"): role differences are
absorbed by each repo's local `/cdev` (one loop reading the role profiles).

## Phase A — Discovery

1. Workspace root = cwd. Detect child Git repos (dirs with `.git/`), whether in the direct root
   or under `repos/` — **the real layout rules; repos are never moved**. External paths the
   user indicates may also be registered.
2. Per repo: current branch, origin, HEAD SHA, active local sprint (from its `SPRINTS.md`).

## Phase B — Per-repo CDev audit

Check: the repo guide (`AGENTS.md` or the host's equivalent) · `docs/develop/SPRINTS.md` ·
`AGENT_EXECUTION_PROTOCOL.md` · `AGENT_PROGRESS.md`. Classify:

- `CDEV_READY` — everything present.
- `CDEV_PARTIAL` — something non-critical missing (e.g. the root guide file). The gap is
  recorded in the workspace's DECISIONS; it does not block the bootstrap.
- `NOT_CONDITIONED` — no `docs/develop/`. Blocker: recommend the `bootstrap` skill and resume
  once conditioned. **The global bootstrap never invents a child's CDev.**

## Phase C — System map

Derive from the children's guides (`AGENTS.md`)/`PRODUCT.md`: each repo's responsibility, inter-repo
dependencies (who consumes whom), cross-cutting domains, known contracts. Generate:

- `workspace/repos.yaml` — registry: logical id → path, git, cdev state, informative role.
  Stacks are metadata, not rules; operational authority remains the child's guide. Any
  field asserting a child's state is re-derived on read or checked by the verification
  script — a stale registry is exactly the kind of artifact an agent will eventually trust.
- `workspace/repo-graph.yaml` — `depends_on` + `domains`. Informs planning; it does **not**
  define batch participation (that is done by each SYSTEM_BATCH's explicit references).
- `docs/develop/SYSTEM_ARCHITECTURE.md` — nodes, arrows, contracts.

## Phase D — Scaffolding

Generate at the workspace root:

```text
AGENTS.md                            # small: coordination, does not duplicate child docs
docs/develop/
├── PRODUCT.md                       # whole system + global clarity map
├── SYSTEM_ARCHITECTURE.md
├── SPRINTS.md                       # SYSTEM Sprints / SYSTEM_BATCHes (own numbering)
├── AGENT_PROGRESS.md                # coordination handoff, not code diffs
├── AGENT_EXECUTION_PROTOCOL.md      # local deltas; the generic loop lives in cdev-monorepo
├── ROADMAP.md
├── DECISIONS.md
├── TESTING.md                       # levels L0–L3; each batch declares its own
└── AUTONOMOUS_RUNBOOK.md            # how to launch and what to expect
workspace/
├── repos.yaml
├── repo-graph.yaml
├── state.lock.json                  # reproducible snapshot of coordinated state
├── contracts/                       # cross-repo contracts per SYSTEM_BATCH
└── snapshots/
.claude/agents/
├── monorepo-repo-runner.md          # bridge workspace → the repo's /cdev
└── monorepo-system-tester.md        # global acceptance L0–L3
scripts/verify-monorepo-bootstrap.ps1
```

Planning is NOT a local agent: it is the global `cdev-monorepo-planner` skill. The
`cdev-monorepo` and `cdev-monorepo-planner` skills remain global — no vendored copies.

Minimum content of each doc: follow the pattern of the already conditioned child repos.

## Phase E — Workspace git

If the root is not a repo: `git init`. `.gitignore` excludes **every registered repo path**
(child `.git` dirs are never nested), plus `worktrees/` and `logs/runs/`. No `origin` by
default; the workspace git versions only planning/contracts/state. Future working branch:
`cdev/system-sprint-<n>`. Initial commit of the scaffolding.

## Phase F — Initial state

`state.lock.json` with a per-repo snapshot: branch, SHA, active local sprint/batch. It is an
informative photograph; a batch's DONE gate only looks at its required references.

## Phase G — Human gate (single)

Before writing: present detected repos (path, branch, SHA, CDev classification), derived
graph, files to generate and the outline of the first SYSTEM Sprint if one is derived. One
confirmation and render everything. Existing file → diff and ask, never overwrite silently.
If the user already explicitly approved the design in the conversation, that approval counts
as the gate.

## On finishing

1. Run `scripts/verify-monorepo-bootstrap.ps1` (paths exist, no placeholders, ≤1 SYSTEM Sprint
   ACTIVE, references point at real sprints/batches, state.lock parseable, repos not versioned
   by the parent git).
2. First entry in the global `AGENT_PROGRESS.md`: bootstrap done, next action =
   `/cdev-monorepo-planner` to derive the first real SYSTEM Sprint.
3. "Conditioned — how to launch" summary pointing at the RUNBOOK.
