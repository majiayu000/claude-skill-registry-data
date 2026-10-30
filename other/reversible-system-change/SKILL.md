---
name: reversible-system-change
description: Plan, prepare recovery material, rehearse, or execute persistent system changes with verified rollback and postconditions. Use for an install, upgrade, deployment, migration, destructive retention action, active-version promotion, or explicit machine-credential lifecycle inventory, plan, activation, or retirement with rollback, data, service, or activation risk. Plans and non-mutating workflow rehearsals stay read-only; recovery preparation and isolated restore rehearsals require bounded write authority. Pair with confirm-external-action when the same request also causes a consequential external app or account effect. Do not use for ordinary source/configuration edits, Git operations, generic status queries, or conceptual explanations.
---

# Reversible System Change

Make one authorized persistent change without losing the ability to identify,
restore, and verify the prior working state.

Defaults you may adapt, saying so: step order where no gate depends on it, and report layout. Every other rule here and in the references the active phase loads binds.

## Select One Phase

- Explicit machine-credential lifecycle: read `../using-axiom/references/credential-lifecycle.md` first. A metadata-only inventory stops there. For persistent activation, rollout, retirement, or cleanup, continue into the applicable phase below; provider-side creation, revocation, or secret disclosure also loads `confirm-external-action` under an independent envelope.
- Plan or non-mutating workflow rehearsal: read `references/preflight-and-rollback.md`. Keep the phase read-only; do not create a candidate, backup, capsule, cache, remote record, or sensitive content access.
- Prepare missing recovery material: read `references/preflight-and-rollback.md` and `references/recovery-material-preparation.md`. This bounded authorized phase may create an isolated backup before restore validation, but cannot prepare a candidate, overwrite prior material, or alter active state.
- Authorized isolated restore rehearsal: read `references/preflight-and-rollback.md` only. Freeze an isolated non-active target and its complete write set, obtain exact rehearsal-write authority, and verify only the restore outcome. This phase may establish `rehearsed` evidence; it never authorizes candidate preparation, active promotion, the complete change, or cleanup.
- Execute a complete authorized change: read `references/preflight-and-rollback.md` first. If recovery material must be created, enter its preparation phase within the current authority. Read `references/execution-and-verification.md` only after the exact target, write set, promotion authority, rollback coverage, and current restore validation pass, or after an informed waiver under `references/informed-waiver.md` replaces the last two.
- Conceptual explanations and pure status/version/availability queries do not select this skill or load its references.

## Authority Boundary

Resolve the requested outcome, exact target, authorized actions, and expected postcondition before mutation. Ask one question only when target, environment, destructive scope, credentials, sensitive asset use, promotion, or rollback authority would change execution. Settle an explicitly delegated target or environment choice only if every alternative is reversible and already authorized; choose by the user's environment and goal, and state which and why before acting.

Keep recovery-material preparation, isolated restore rehearsal, candidate
preparation, active promotion, service restart/reload, data migration,
destructive retention, sensitive asset access, rollback, and cleanup as separate
actions. Permission for one never implies another. Freeze the exact direct and
indirect write set; a newly
discovered target, dependency, service, data store, endpoint, or destructive
effect requires renewed authority.

Inventory sensitive assets by metadata only. Read or use content only after the exact path and exact action are frozen and authorized. Never print, copy broadly, hash, encode, or persist secret contents merely to inventory them.

## Rollback Gate

Before candidate or active-state mutation, require a rollback point that
represents the observed prior state and covers every non-forward-compatible
effect. It must be currently readable by the restore principal, with all
prerequisites present, and must have passed a target-native restore validation
or an authorized isolated rehearsal.
Recheck that evidence immediately before mutation.

Keep `identified`, `present`, `readable`, `restore-validated`, and `rehearsed`
as distinct evidence states. A backup job, artifact, script, manifest,
checksum, historical rehearsal, or user acceptance of risk is not verified
rollback. If current restore validation or complete coverage cannot run, stop
execution; a plan may report the gap.

An informed waiver under `references/informed-waiver.md` lifts this rollback requirement only for the effects named to the user; every other effect and rule still binds.

## Change Contract

1. Observe current target and runtime state with scoped read-only probes.
2. Freeze persistent effects, destructive roots, and the postcondition layers that own the requested outcome.
3. Prepare missing recovery material through its bounded phase, establish the full rollback gate, then validate a candidate or dry run without promotion.
4. Refresh drift-sensitive preconditions immediately before the authorized write.
5. Apply the smallest candidate mutation and promote only through separately authorized actions.
6. Verify every relevant materialization, selection, runtime, delivery, behavior, and preservation layer with fresh direct evidence.
7. On a declared failure gate, stop further writes and run only the pre-authorized bounded rollback; then verify the prior state at its owning layers.

Command success, upload acceptance, a configuration write, or process start
proves only that stage. A failed or unavailable outcome-owning observation is
unverified, not complete.

## Resume And Compaction Handoff

After resume or compaction, reobserve the target and drift-sensitive state, then fail closed unless host-native task context and current direct evidence from the owning system reconstruct the active phase, exact current user authority, frozen action envelope and complete write set, prior mutations and attempt identifiers, idempotency status, and phase-appropriate recovery evidence. Preparation resumes through its isolation and disposal gate; candidate or active-state mutation still requires current full rollback validation. If any required field is missing, stale, or inconsistent, perform zero new mutations. Never adopt post-change state as the prior rollback baseline. An unknown external outcome enters Verify only and must not be resent. Reestablish changed or missing evidence and obtain renewed authority; authority alone cannot waive the rollback gate, and only an informed waiver that current host-native context still shows lifts its rollback requirement. Do not add a daemon, cache, telemetry, or persistent handoff tool to reconstruct the handoff.

## Safety And Handoff

- Resolve destructive targets directly; never use an unresolved variable, broad glob, guessed parent, or symlink traversal.
- Preserve unrelated state and the only working copy. Do not reset, stash, clean, install adjacent tools, change global configuration, or widen remote permissions to make a gate pass.
- A host-mode denial is a stop, never a retry by another tool, flag or path; present the exact action for the user's grant first. Read `../using-axiom/references/host-permission.md`.
- Dispose of failed preparation output only through its frozen disposal gate. Delete other candidate or rollback material only under explicit cleanup authority after required postconditions pass and another required recovery route remains.

Report the target, actions actually authorized, mutation/promotion/rollback
outcome, material failed or unavailable postconditions, final observed state,
and retained recovery material. Include detailed successful layers only when
they support a completion or recovery decision.
