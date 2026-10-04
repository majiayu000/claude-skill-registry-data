---
name: apply-all
description: Validate versioned proposal dependencies, admit only approved and prerequisite-ready changes, then execute in isolated worktrees and verify integration.
---

# Apply All

Prefer one isolated worktree and branch per admitted proposal. Worktrees isolate file edits, not databases, services, credentials, ports, caches, generated outputs or external state. Read durable repository artifacts; never depend on a previous conversation's plan.

## Required proposal contract

Every selected active change MUST start its `proposal.md` with YAML frontmatter:

```yaml
---
execution:
  version: 1
  depends_on: []
---
```

`depends_on` contains exact change-directory IDs, not paths, display names or task IDs. It means **the whole prerequisite must be verified complete and integrated into the dependent's execution base before any implementation of the dependent begins**. An explicit empty list means reviewed and dependency-free; a missing field does not. No phase/milestone semantics are supported by version 1. Do not interpret prose allowing early implementation as permission to bypass this boundary: report inconsistent declarations and request repair.

This contract is scheduling metadata, not approval, completion state, a resource lock or evidence. `tasks.md` remains authoritative for task state. A shared file is a conflict to serialize, not automatically a dependency. Do not add hidden edges or silently repair missing metadata and execute it. Material dependency changes require review before admission.

## Preflight — before worktrees or workers

1. Load the explicit selected change IDs. Do not select every active change by default or automatically add unselected dependencies to implementation scope. Locate project OpenSpec config, all selected proposals/designs/specs/tasks, and related active changes. Use `openspec instructions apply --change <id>` when supported to consume project/schema guidance; then retain all `apply` terminal gates.
2. Validate each selected change with `openspec validate <id> --strict`. Run the repository dependency validator when the repository provides one. In repositories adopting the standard location, run `python3 scripts/openspec/validate_dependencies.py --root . --json <selected-id> ...`; inspect its exit status and JSON. For another repository, use its documented equivalent. If no validator exists, perform a bounded deterministic check of each selected proposal's version-1 frontmatter, exact dependency IDs, active/archived resolution, and acyclic transitive graph; record that this is a manual-equivalent check rather than validator-backed evidence. Never infer hidden edges or silently install/copy a validator. Install missing validator dependencies only with appropriate authorization, never silently.
3. Require contract version 1, unique well-formed IDs, resolvable dependencies and an acyclic transitive graph. Resolve references against active and archived changes. Duplicate/ambiguous archive matches, missing metadata on active prerequisites, unsupported versions and dangling references block the affected selection; do not choose a convenient match. Legacy archived prerequisites may need explicit manual evidence review, never an automatic pass.
4. A structural graph pass is NOT execution readiness. For each selected proposal, verify maintainer implementation approval from an explicit instruction or durable approval record. Drafting approval does not count. For each prerequisite, inspect tasks, acceptance artifacts, independent review and archive/closure evidence; verify no required operator gate remains unchecked or unsupported. A directory under `archive`, all checked boxes, a worker message or successful dry-run alone is insufficient.
5. Prove prerequisite integration: record implementation/integration revisions and verify their ancestry in the execution base with git. If squash/cherry-pick history prevents ancestry proof, require an explicit reviewed mapping and verify the resulting content and gates; do not guess equivalence. An externally satisfied legacy prerequisite needs a documented manual evidence decision. Refresh evidence when relevant code, runner configuration or external resources have changed.
6. Pin the initial repository revision and inspect dirty edits. Assign one owner to each overlapping file/API/schema/cache/resource; include lockfiles, generated configs, environment stores, DB targets, runner groups and deployment writers. Serialize or isolate conflicts. Unknown security/production activation relationships block affected work for review. A DAG layer is not proof of safe parallelism.
7. Record an admission report using the native task/report mechanism: proposal, approval evidence, dependencies, prerequisite evidence/integration revisions, ready/blocked/completed status, blocker reason, resource ownership, source base and next action. Keep this a derived report, not a second task-state database. Structural validator output must never be relabelled as approved or ready. Continue only with explicitly approved ready proposals; park blocked dependents while unrelated ready work proceeds.

## Execution and integration

1. Create worktrees only for admitted proposals. Independent proposals may share the initial base. Dependents MUST start from the updated verified integration HEAD containing completed prerequisites, not the original common base. Record each actual worktree base; refresh the graph if proposal metadata changes.
2. Dispatch bounded work through `apply`. Each worker receives exact proposal/task scope, prerequisite evidence, file/resource ownership, forbidden actions, verification recipe and stop conditions. Follow that proposal's task graph; do not impose universal layer phases.
3. Keep implementation separate from activation and operator actions. Missing runner readiness, credential provisioning, protected-environment approval or live evidence leaves the corresponding task blocked. Never enable a production consumer merely because automatic CI starts passing. Do not claim a partially implemented proposal complete to unblock another.
4. Reconcile verified work into the integration branch without discarding another proposal's changes. Re-run affected contracts and shared-resource gates after reconciliation. A worker's branch passing does not prove the integrated tree passes.
5. Run fresh gates and independent review; repair findings and repeat gates/review. Update authoritative tasks from evidence. Persist bounded work with the authorization and scoped commits required by `apply`; this skill is not a bypass for repository commit policy. Archive only changes whose required tasks, operator gates, final review and integration evidence pass. Reconfirm history and archive persistence before completion.
6. Re-run admission for newly unblocked dependents against current integration HEAD. On resume, reconstruct state from files, git and evidence rather than conversation memory. Clean up branches/worktrees only after results and cleanup are verified. Never push automatically.

## Failure examples

- CI depends on runner isolation: runner code is merged but live isolation proof is missing -> CI remains blocked.
- CI completes with production disabled; release depends on CI -> valid DAG. Do not add the reverse dependency merely because release owns later activation.
- Two otherwise independent proposals edit `ci.yml` -> serialize shared-file integration and rerun tests, not a fabricated dependency cycle.
- An archived prerequisite has no integration proof -> `needs prerequisite evidence`, not ready.
- A dependency is not selected -> verify it if already complete; otherwise report it as an external blocker, never dispatch it without approval.
- All graph checks pass but proposals are drafts -> awaiting implementation approval, not ready.

## Invariants

No Beads, vendor-specific tracking, wave-priority system, mandatory DB/API/UI/E2E schedule, implicit dependency repair, automatic push or completion claim without fresh evidence. Preserve `apply` gates, independent review, task updates, authorized scoped persistence, integration, archive and final history verification. Do not introduce a skip-gates/review/archive completion mode.
