---
name: ssot
description: Step 3 of the five-step flow. Delete first, then converge on one source of truth. Use for refactors, dead-code removal, contracts, projections, and drift.
---

# ssot: delete, then keep one source

Order matters (Musk's steps 2 and 3): delete the part, then simplify what remains.
Never optimize a step that should not exist.

## Rules

1. **Delete before you add.** The owner asked for "is this over-designed?" and "which existing logic must be cleaned?" in several reviews.
   For each shim, adapter, or flag, ask "what breaks if I remove it?" If nothing breaks, remove it.
   If nothing you removed needs to come back later, you removed too little.
2. **One fact, one source.** Name the single editable source before you write code. Close every other edit point.
   Derived files carry `DO NOT EDIT`, come from a one-way tool, and can be deleted and rebuilt at any time.
   Never hand-edit a derived file. A hand edit is a drift candidate: move it into the source.
3. **Remove the predecessor in the same change.** After the new mechanism works and equivalence is proved, delete the old code,
   old files, and old docs in the same PR. No `@deprecated`, no "delete later".
4. **Re-aim every guard after a deletion.** A guard written for the old structure can stay green and check nothing.
   Make the guard fail on the old shape first, then repoint it.
5. **Read the original intent first.** An agent once changed a mapping without asking why it was split from the content source.
   Read the issue that created the structure. Keep a split that has a reason.
6. **Keep global configuration minimal.** Each directory reads its own rendered artifact. A tool reads only that artifact.
   Global user directories belong to user-managed tools. A workspace script must not write there.
7. **Check reachability.** From the entry points (main, routes, CLI commands), compute what is called.
   Written but never read is waste: delete it. Read but never written is a defect: fix it.
8. **Contract first.** Lock signatures, schemas, and the observable endpoint before the internals.
   Prove equivalence with real inputs on old and new paths. Run staging first when a scheduler or alert stack changes.

## Mechanical Gates (MANDATORY)

An `/ssot` pass fails closed unless every gate below passes with physical command output:

1. **Predecessor Deletion & Net-Diff Gate**:
   - Run `git diff --stat <base>...HEAD` and `wc -l` on touched modules before opening or merging a PR.
   - Every new abstraction, shared helper, or unified entry point MUST delete its predecessor in the same PR.
   - Purely additive "unification" PRs are forbidden. If lines added exceed lines deleted on an `/ssot` or refactor slice, delete the remaining duplicate callers first, or name each added group and its removed predecessor lines in a `## Net diff` PR section. `ws-pr-gate` enforces this (`net-diff-positive`).
2. **Cross-Package & Standalone-Script Convergence Gate**:
   - When extracting a contract or helper into an SDK or `common/` module, migrate all in-repository callers and delete the local copy in the same change. Verify zero remaining local definitions with `git grep`.
   - Never duplicate dataclasses, registries, or parsers inside standalone or piped scripts via `try: from common... except ImportError:` fallbacks. Keep one authoritative definition and inline or pass it mechanically at the boundary.
3. **Zero-Caller Speculative Code Gate**:
   - Every new public function, class, dataclass field, or CLI flag MUST have at least one production caller in the same diff.
   - Delete pass-through aliases (`_X = X`), one-line private wrappers with a single caller, and unused re-exports (`__all__` entries with zero external imports).
4. **Falsifiable Guard Test Gate**:
   - Every deleted duplicate or predecessor must be locked by an executed test (`pytest <file>::<test> -x`) that fails if the second copy or legacy symbol returns.

## SSOT Swarm (M=10)

Before major refactorings or cleanups, dispatch 1 SSOT Swarm (M=10 Interns via `subagent_batch`). The Director dynamically defines the focus dimensions and allocation across the following baseline topology:
- **Intern 1 (Call graph reachability)**: Scans public entry points vs call graph to locate uncalled dead code and unused modules.
- **Intern 2 (Multi-source configuration drift)**: Scans for duplicate configuration definitions between Host, Repo, and App layers.
- **Intern 3 (Orphan links & rotting documentation)**: Runs link checkers (`python -m tools.doc_link_check`) to find broken documentation links and stale claims.
- **Intern 4 (Empty guard protection)**: Verifies that existing assertions and guards actually fail on deleted or mutated inputs.
- **Intern 5 (Deprecated shims & backward-compatibility wrappers)**: Finds temporary adapters and shims whose replacement has landed.
- **Intern 6 (Stale schema & contract duplication)**: Scans for duplicate DTO models, redundant interfaces, or manual copies of generated types.
- **Intern 7 (SQL query fragmentation)**: Locates fragmented database queries across consumer layers that bypass shared query services.
- **Intern 8 (Hardcoded magic numbers & constants)**: Scans for scattered thresholds, timeouts, or formulas that lack a single source of truth.
- **Intern 9 (Documented vs implemented invariant drift)**: Compares architectural documentation against reality to eliminate false defect claims.
- **Intern 10 (Dead test assertions & tautologies)**: Inspects test fixtures for deleted code paths or assertions that run on empty result sets.

## Report

Output a verification table with four columns:

| Deleted Predecessor (`file#Lxx`) | Single Source (`file#Lxx`) | Net Line Delta (`git diff --stat`) | Guard Test (`pytest <file>::<test> -x`) |
|---|---|---|---|

