---
name: unattended-work
description:
  Coordinate an authorized unattended project run using configured agents, task claims, review, validation, and commit
  policy. Use when the user requests autonomous or unattended implementation of a bounded task or milestone; selecting a
  named agent alone follows its normal configured profile.
---

# Unattended work

Run a bounded work queue using the project's shared coordination contract. This skill supplies the coordinator's
procedure; it does not launch a background service or grant permissions beyond the user's request.

## Resolve the run

Read the workspace `AGENTS.md`, `agent-workspace.json`, and its linked coordination guide. Run
`node .agents/agent-workspace/scripts/agents.mjs --help` for current command syntax, then inspect session status,
relevant repository changes, and the requested Backlog scope. Read the installed Backlog lifecycle instructions before
tracker operations.

This skill supports workspace schema 1 and runtime schema 1. For versioned projects, check
`.agents/agent-workspace/install-manifest.json` compatibility before changing workflow state. Use the project's
installed CLI, never a runtime inside a global plugin/cache. Unsupported versions require an explicit tooling/skill
migration. Plugin installation alone does not upgrade project scripts or authorize such a migration.

- Resolve a requested agent by the project's roster. A name is a project role, not a provider or model. Apply the user's
  explicit profile choice, otherwise the agent's default, otherwise the project default. Do not invent a missing roster
  member or change configuration to satisfy a name.
- A named-agent request selects its approved configured default profile and grants no permissions beyond that profile
  and the known task scope. If the resolved profile is assisted, use the ordinary shared workflow and leave this
  orchestration loop. If it is unattended, record the actual named-agent request and clear task context as authorization
  for that configured behavior; clarify missing task scope before starting.
- Establish the task IDs or milestone, actual user authorization, and configured limits before starting. An unattended
  request authorizes the applicable configured workflow only within that scope. Ambiguous scope or a requested
  permission that conflicts with project rules needs resolution before dependent work.
- Register a coordinator run with the chosen agent/profile, bounded scope, and authorization evidence. Retain its
  returned run and session IDs. Existing runs keep their own policy; do not mutate project defaults or another run to
  implement a temporary request.

Use the CLI's run record as the resolved policy for delegation, review, validation, commits, human input, agent count,
task count, and elapsed time. Honor stricter explicit user constraints. Review and approval gates remain active
regardless of profile.

Before implementation, confirm every repository to be changed has meaningful configured checks. For a foundation task
that creates its first checks, claim `agent-workspace.json` together with the implementation. After adding checks, use
`refresh-checks --session ID --task TASK-ID --repo PATH --note REASON` before taking final snapshots. This imports only
additional checks; existing definitions, execution order, permissions, limits and repository boundaries remain fixed. It
invalidates all snapshots, verification, visual declarations and reviews in the run. Renew them before committing. Do
not restart merely to load new checks and strand the implementation as inherited dirt. Older runtimes without this
command need the setup skill's supported update first.

## Coordinate eligible work

Use the CLI's ready-work view to select unblocked tasks within the authorized run. Inspect each task's dependencies,
acceptance criteria, ownership, and human gates before claiming it. Claim literal writable scopes and record a
researched implementation plan through the serialized Backlog wrapper.

Delegate only when the profile permits it and independent work or review benefits from another agent. Use available
native agent tools; do not create user-owned chats or install another provider as a substitute. Workers join the
existing run with their own session IDs and receive one bounded assignment, allowed paths, relevant acceptance criteria,
and expected evidence. Workers follow the shared workflow; they do not start nested coordinator loops. Count reviewers
and testers against the concurrent agent limit. If required independent review is unavailable, defer completion for
review instead of silently weakening the profile.

Keep active claims and heartbeats current. The coordinator integrates worker results and preserves unrelated changes. A
stale heartbeat is a reason to inspect an owner, never permission to take its files. Use the shared recovery procedure
for confirmed interruption or failed tracker synchronization.

For a stopped run, inspect `history --claim CLAIM-ID` and the source session. Resume only authorized unfinished work
with `claim ... --from-claim CLAIM-ID --note EVIDENCE`, using the original scopes. The guard requires a stopped source,
unchanged repository identity/HEAD, an empty index, and exact recorded file hashes. Unknown dirty files stay protected.
All checks and independent reviews must run again. If an older release discarded its claim, only inspected original
claim and snapshot CLI outputs can supply `--receipt FILE --confirm-receipt`; see the project guide. Never reconstruct a
clean baseline from current dirty files or hand-edit runtime to adopt them.

When exact recovery is unavailable and the human explicitly requests checkpoint commits of inspected inherited work, use
an `on-request` run and `claim --commit-request`. Repeat `--repo` for source and visual-evidence repositories and select
their exact `--file` paths in one claim. Committed comparison images can be bound as immutable evidence references
without another commit. Snapshot all changed repositories before declaring visual evidence, then run each repository's
checks, review and separate commit. Release an unfinished checkpoint paused and establish fresh ordinary ownership
before continuing implementation. An old unattended authorization alone does not permit this handoff; preserve any
successful commits if another repository remains blocked.

## Verify and complete

At a stable implementation point, inspect the final diff and use the configured validation and review requirements. Run
the minimum meaningful checks for the changed surface and record actual results, limitations, and the task's acceptance
evidence. Independent review must come from a separate session that examines the final changes; the author cannot attest
on its behalf.

Use the coordination CLI's snapshot, visual declaration, verification, review, and guarded commit operations as
documented in its help and the project guide. Bind evidence to the exact content under review. Changes after
verification or review require renewed relevant evidence; a previous passing result is not approval for a later diff.

Use the separate [visual-evidence-review skill](../visual-evidence-review/SKILL.md) for UI changes. Capture the baseline
before implementation, claim the task asset directory, and inspect final comparisons. Register evidence after the final
snapshots and before review. Non-UI work still declares `no-ui`; text-only and inspected visually unchanged exemptions
require a reason. Missing baseline, capture access, or required native permission blocks the task; defer it and continue
eligible work.

Active task metadata is excluded from its implementation snapshot. Authorized automatic or requested commits finalize it
separately after the Done transition, using recorded native-write provenance and the same Git ownership/index guards. A
successful finalization releases the claim; its SHA stays in the local journal and Git history so recording it does not
dirty the task again. Use `queue` and `commit-status` for a failed finalization, then `reconcile` after fixing its
blocker. Never treat a pending finalization as fully complete or silently adopt unknown task edits. Interrupted native
writers require the execution guide's inspected recovery.

- Commit only when the resolved run policy and user scope permit it. `on-request` requires actual commit authorization;
  `never` leaves changes uncommitted. Automatic commits still require task ownership, current evidence, and the
  configured review.
- Use the guarded operation to serialize repository Git mutations and stage only the task's owned changes. Inspect the
  target repository and its index first. Another person's staged checkpoint is a blocker: never include, reset, unstage,
  stash, or bypass it with an alternate index or an unguarded commit.
- Preserve unclaimed or pre-existing modifications even inside a claimed file. Resolve uncertain ownership before
  staging. A failed commit leaves its state to inspect; do not automatically clean up the index or weaken hooks/checks.
- Push, merge, tags, deployment, and destructive actions need their own authorization. Permission to commit locally does
  not authorize them.

Write the final task summary and verified criteria through the Backlog wrapper, including commit references when created
or an explicit uncommitted handoff. Complete only when the task's acceptance criteria and run completion requirements
are actually met. Release ownership with the truthful outcome.

## Defer human input and stop cleanly

For a product/architecture choice, human assessment, approval gate, or execution blocker, follow the run's human-input
policy. In a deferring run, record the issue using the CLI's defer/queue facilities, release affected ownership when
recovery guards permit it, and continue independent eligible tasks. Do not treat unattended mode, inactivity, or another
completed task as approval. Resolve gates only with the user's actual decision and its reference.

Every deferred record must state:

- The concrete question or blocked action and why it matters.
- Evidence or a reviewable artifact, realistic options, and a recommendation where useful.
- Affected tasks, completed checks, remaining work, and the exact next action after resolution.

Use the configured decision, human-review, approval, and blocked labels consistently; labels expose the issue and do not
grant ownership. A missing tool, failed check, or protected index is an execution blocker rather than a product
decision. Avoid repeatedly selecting a deferred task or retrying a known failure without new evidence.

Stop selecting work when the authorized scope is complete, a configured limit is reached, the user stops the run, or
only human-gated/blocked work remains. Safely finish or hand off active work, persist useful evidence in Backlog, and
release claims and close sessions/run according to the CLI. Unresolved Git journals or uncertain live writers retain
their ownership and locks: leave a blocked handoff with recovery evidence instead of forcing release/stop or weakening
recovery guards for cleanup. Otherwise, do not keep a session active while waiting on a future chat. Do not schedule a
wakeup or expand the task queue without user authorization.

Return a consolidated handoff: completed tasks, commits or uncommitted changes, checks and limitations, and the
decision/review queue with direct task or artifact links. Distinguish completed work from implementation awaiting review
or approval.
