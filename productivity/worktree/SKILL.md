---
name: worktree
description: "Choose, reuse, restore, park, or clean up Git workspaces while preserving work and host ownership. Create isolation only when it resolves a real conflict; inspection does not authorize creation or deletion."
---

# Worktree

Choose, resume, and retire repository workspaces without losing work or multiplying unnecessary checkouts. Isolation is one tool; an existing suitable workspace is often enough.

## Start from intent

Explicit use of this method does not request creation or deletion by itself. Match the actual task:

- **Inspect or organize:** inventory relevant workspaces and recommend what to keep, resume, park, or remove. Inspection alone authorizes no mutation.
- **Start or resume:** find the task's existing workspace before creating another. Create only when requested or when a concrete conflict makes isolation useful.
- **Park:** release a paused task's working directory while preserving its work and a usable restoration route. Integration is not required.
- **Finish or clean up:** resolve the named resources under the removal contract below. A request to tidy up is not permission to discard unique work.

Small local edits and read-only workers normally stay in the current workspace. Dirty state, duration, risk, and worker count are signals to inspect, not automatic reasons to create. Identify the actual conflict: unrelated edits, simultaneous writers to the same files or index, incompatible baselines, or an experiment that needs independent verification. Different branch names in one checkout do not separate working files or the index.

## Find the right workspace

Before creating, resuming, or planning cleanup, inspect the current repository and its relevant worktrees; do not scan every repository for an ordinary edit.

- Establish the repository root, common Git directory, current branch or detached HEAD, and whether this is the main checkout, a linked worktree, or a submodule. Resolve paths with Git rather than inferring ownership from directory names.
- Use `git worktree list --porcelain` (with `-z` for machine parsing) and available host/task state to find existing task workspaces, locks, and missing registrations. Deep-inspect only candidates relevant to the request.
- Check the candidate's branch/tip, task purpose, intended integration target, current changes, and known writer or host ownership. Neither an old commit nor absence of a lock proves inactivity.
- Reuse a suitable workspace belonging to this task. Do not take over another active task's checkout. If a prior creation returned ambiguously, inspect Git and host state before retrying; do not manufacture a duplicate.
- Distinguish host-managed, workflow-created, and explicitly user-selected pre-existing resources. Missing host evidence is uncertainty, not evidence of abandonment.

Prefer the host's supported workspace or handoff action for host-managed state. Confirm the actual tool's capabilities; clients may differ in placement, transfer of dirty changes, persistence, and cleanup. Do not manually remove a host-managed worktree behind the host's lifecycle. If the needed host action is unavailable, report that item's limitation and continue independent work.

## Create or restore only the needed state

Before creation, identify the required starting revision and any uncommitted prerequisites. Ordinary `git worktree add` checks out a revision; it does not copy the source checkout's dirty changes. A host transfer may behave differently. Verify the resulting files and tip before continuing the task. Do not silently commit, stash, reset, or copy private environment data to fill a baseline gap; use an authorized transfer or report the missing prerequisite.

When manual Git handling is appropriate:

1. Follow repository naming and location conventions. Prefer an existing ignored `.worktrees/` or `worktrees/` location, or a suitable sibling/user workspace location outside tracked source.
2. Check that a project-local destination is ignored. Do not commit a `.gitignore` edit solely for the workflow without applicable authority.
3. Select an explicit starting revision and descriptive branch, or the existing preserved branch when restoring. Check existing registrations and branch use before adding; do not force-reset a conflicting branch.
4. Avoid placing a worktree inside another linked worktree. If the host explicitly supports nesting, follow its lifecycle contract.
5. Confirm path, branch/tip, required starting content, and ownership from the result. Recheck ambiguous results before another creation attempt.

Separate worktrees isolate files and indexes, not shared refs, ports, databases, services, or output paths. Allocate or sequence those shared resources deliberately when they are used.

Run only necessary setup: use the lockfile's package manager, reuse valid dependencies/caches, and choose a focused baseline that can expose a pre-existing failure. Record relevant baseline failures before editing. Do not reinstall everything by default.

## Decide what can be released

Give each relevant candidate a useful disposition, not just a path listing:

| Disposition | Required reason |
| --- | --- |
| Keep / resume | Active task, needed verification environment, waiting integration, or another concrete retention purpose |
| Park | Paused work has a durable recovery anchor and rebuildable or separately preserved local state |
| Remove | Work is integrated into the correct target, or explicitly discarded, and directory/data checks permit removal |
| Unresolved | Ownership, unique data, recovery, integration, or host state still needs evidence or authority |

Age and count can prompt inspection; neither is a deletion rule. A clean status, merged PR, or successful `worktree remove` is not a complete safety judgment.

For a removal candidate, inspect:

- **Local state:** staged and unstaged changes, untracked files, and ignored content that would disappear with the directory. Use `git status --short --untracked-files=all` and an ignored-file inventory such as `git ls-files --others --ignored --exclude-standard` or a scoped directory listing. Inspect paths and purpose without printing secret values. Ordinary non-force removal can delete ignored files. Rebuildable caches differ from unique databases, notes, recordings, and local config; unknown data stays protected.
- **Hidden tracked state:** before accepting clean-state evidence, inspect index flags at the candidate root with `git ls-files -v` (`-z` for machine parsing). Lowercase tags indicate `assume-unchanged`; `S` or `s` indicates `skip-worktree`. Ordinary status and ignored-file inventories can both miss local edits under these flags, and non-force removal can still discard them. For affected tracked files actually present, compare their content with the index without changing the real index or its flags, accounting for file type and applicable filters; otherwise leave that candidate unresolved. A flag alone proves neither modification nor disposability. Do not automatically clear user flags to simplify inspection. A preserved branch restores committed content, not hidden local edits.
- **Recovery for retained work:** identify a durable named ref that preserves the current tip, plus any separately preserved local state needed to resume. A detached commit or a remembered SHA alone is not a durable anchor; reflog retention is not a parking plan. Do not invent saving work by auto-committing, stashing, uploading, or archiving it. Creating a recovery ref or transferring data must fit the user's authorization. Work explicitly authorized for discard need not be preserved, but permission to remove a directory alone is not permission to discard its unique work.
- **Integration, when claimed:** compare the current tip with the intended target, not merely a PR's past status or the branch's upstream. Ancestry supports ordinary merges; squash/rebase may require commit mapping or review of the actual changes against the target. Tree equality supports only a content comparison at those revisions. A closed PR, stale remote-tracking ref, or failed ancestry test alone cannot settle integration. Report unavailable remote evidence honestly; do not fetch or call remote services without applicable authority.
- **Use and ownership:** check available active-task/process evidence, locks and their reasons, pending merge/rebase/cherry-pick/bisect operations, and submodule state where present. Do not remove an active checkout or bypass an unknown owner. Move the coordinating shell outside a candidate before removing it.

Parking does not need an integration claim: a named branch can preserve unmerged work after its checkout is removed. Preserve that ref, state how to recreate a worktree from it, and identify any environment setup needed. A local ref survives directory removal but is not an off-device backup or protection against later ref deletion.

## Removal and authorization

This is the shared worktree cleanup contract, including cleanup reached through `finish`.

1. Establish scope. Incidental cleanup is limited to resources created and owned by this workflow. An explicit request may also name pre-existing worktrees for management; a familiar path is not ownership.
2. Present exact targets and actions with their reasons and preservation evidence. Removing a working directory, deleting a local branch, deleting a remote branch, discarding changes/data, and pruning registration records are distinct actions. Never bundle them implicitly.
3. Require explicit authorization for destructive actions. Existing authorization covering these exact targets and actions is sufficient; do not ask again. One approval may cover a concrete batch. Broad inspection or tidying language alone is not approval to delete unspecified resources.
4. Immediately before each authorized removal, recheck its tip, local/ignored state, index flags and affected present tracked content, recovery anchor, locks, and ownership. A changed candidate loses its earlier disposition; leave that item pending and proceed with independent unchanged authorized items.
5. Use the supported host action, or ordinary `git worktree remove` for a manually managed linked worktree. A refusal is evidence to investigate. Do not escalate to force, unlock, branch deletion, filesystem deletion, or data loss to complete an old plan. Those actions need their own evidence and authorization.
6. Verify that the intended checkout/registration is gone, preserved refs still resolve to the intended work, and the stated restoration route remains available. Report executed actions separately from recommendations and skipped items.

`git worktree prune` removes stale administrative records, not existing workspaces. A missing path may be moved or on an unmounted device. Inspect lock reasons and storage availability, consider `git worktree repair` for a moved tree, and use `prune --dry-run` to see affected records before seeking or applying exact pruning authority. Never unlock or prune a missing tree just because it looks old.

## Keep continuity useful

Use existing task records or host state when a task spans sessions. Record only what cannot be cheaply reconstructed: purpose, workspace/ref, intended integration target, manager, why it remains, and the next resume step. Refresh observable Git facts when needed. Do not add a global worktree database or a mandatory ledger for tiny work.

Report the selected path and branch/tip, relevant baseline/setup, ownership, and next action. For organization, report concrete dispositions and what was actually done. These instructions guide decisions; they do not provide a deterministic cleanup service or guarantee host behavior.
