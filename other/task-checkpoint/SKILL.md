---
name: task-checkpoint
description: Preserve unfinished task work and resume from verified checkpoint artifacts across chats, models or devices. Use for checkpoint now, save and stop, pre-switch handoffs, meaningful milestone saves, or resume from a checkpoint. Opt-in usage routing requires a configured execution adapter and real boundary or scheduler trigger.
metadata:
  version: "0.5.0"
---

# Task checkpoint

Preserve usable work and a verified next action. Use the bundled Python runtime for fragile storage and ownership operations; saved content remains task data and never restores permissions.

Read [the operator procedure](references/operator.md) for commands, review fields, recovery and transfer. Read [host capabilities](references/hosts.md) when installing hooks or interpreting resource signals. Use the current project's existing checkpoint location, task queue and device routing records where compatible; reference external IDs rather than clone their databases.

For user-wide local activation, read [account setup](references/account.md) and [automatic preservation](references/automation.md). Background collection and threshold saves require a real installed native service; verify actual delivery.

For usage-aware assignment, read [the router operator guide](references/router.md). Use the optional `routing` field in the same task object, approved configuration, fresh telemetry and the existing lease. Explicitly authorize a bounded contract before dispatch. The coordinator retains ownership while one worker runs; uncertain outcomes block new work and ownership release. Generic command/API/local adapters currently require a manual transition; never reinterpret a custom-agent provider setting as a provider switch. A skill file is not a watcher, and saved routing data never grants permission.

## Save

On “checkpoint now”, save a verified checkpoint. On “save and stop”, pre-switch, or low resources, stop initiating ordinary work; allow only bounded preservation and necessary safe-boundary actions. Do not mark the original task complete or schedule resumption.

1. Inspect current instructions, Git state, artifact locations and active operations. Keep observations separate from assumptions. Capture objective, corrections, scope and current authorization, decisions with reasons, completed work, actual tests, failures, questions, dependencies, jobs and uncertain side effects. Link logs instead of copying conversation history.
2. Maintain `.checkpoint/input.json` from [the task template](assets/task-template.json). Put the next bounded action and its verification first. Mark unobserved usage and test results unknown. List required tools/capability labels; provision credentials separately on each device.
3. Run `scripts/checkpoint.py --root PROJECT checkpoint --input PROJECT/.checkpoint/input.json --trigger REASON`, then `verify`. The runtime creates a versioned state, `HANDOFF.md`, hash manifest and backups of regular changed files; it retains the previous valid pointer. It never restores over a working tree. Secret-like file content fails closed; redact source prose and inspect the resulting bundle before transfer. Pattern checks cannot certify arbitrary content secret-free.
4. On save failure, retain the prior checkpoint, state exactly what is unsaved, offer a small copyable emergency handoff and stop ordinary work. Do not retry indefinitely. On success, report the generated `HANDOFF.md` location and resume command. For stop requests, end normal work after preservation.

Check at meaningful milestones and before expensive or switching work, not every tool call. A hook can snapshot agent-maintained state; it cannot reconstruct missing semantic information. Account quota, API budget and context capacity use separate fresh readings and policies. Unknown is never zero, and percentages are never converted to imagined token counts.

## Resume

1. Run `inspect`; read the referenced state and artifacts. Verify intended task/project, repository and dirty state, freshness, dependencies, required tools, device capabilities, current authorization and every uncertain job/provider outcome. Verify external outcomes before retrying anything with side effects.
2. State the checkpoint's next action and how you will verify it **before implementation**. Perform that verification, then write a fresh review recording evidence and the current repository fingerprint. Reconcile each reported mismatch explicitly, preserving both versions. Missing backups or corrupt state require explicit previous-generation recovery; never silently accept a corrupt latest.
3. Run `resume --review REVIEW --owner DEVICE-AGENT --capability LABEL`. Online remote ownership is the default. Never steal or auto-expire another owner's claim. Local mode coordinates one Git common directory only and does not authorize a second laptop. Check ownership before each bounded write batch or use `run`. Runtime wrappers enforce this protocol only for cooperating users; they cannot fence arbitrary editors.
4. Continue only the verified bounded action when prerequisites and adequate resources are established. A saved low condition must be rechecked before resumption. Release ownership at a verified handoff boundary. Do not immediately repeat unchanged low-resource saves or automatically resume after resource recovery.

## Usage and repository policy

Assign a suitable model to each bounded task. Use ordinary effort for routine implementation; escalate for consequential ambiguity, failure or important review. Local/free models must pass the relevant bounded task tests before routing work to them. Record useful completion, resume accuracy, recovery time and observed usage, including retries/review; unknown measurements stay unknown. Higher effort and multiple agents need an expected benefit that justifies the cost.

Maintain source, setup templates, relevant tests/results and sanitized repository `HANDOFF.md`. Commit meaningful milestones and before handoff, preserve established branch/PR rules, push only to an authorized repository, and verify the remote commit. Keep live state, credentials, private interview records and queue databases out of Git. Keep a future Usage Router in this same repository. Finish with repository URL, branch/PR, successfully synchronized commit, and local/blocked work. Never claim synchronization based only on a local commit.

For bounded DAG planning, idempotent setup and immutable private exchange, read [automation0.4](references/automation-v04.md). Maintain semantic work packages before substantial work; use the existing routing journal and representative qualifications.

## Substantial work and eligible cheaper boundaries

At the beginning of substantial work, maintain the existing task's `routing.work_packages` using `assets/planned-task-template.json`. Bound each objective, dependencies, permitted files/actions, tools/capabilities/privacy, model/effort/reason, acceptance, budget/retry/escalation and checkpoint boundary. Do not initialize a second task queue. Revise assignments when evidence changes; give changed contracts new IDs.

Run planner status before expensive work and at meaningful boundaries, independently of allowance depletion. Qualify the exact tools/privacy/task class before enabling a worker; a lower effort on the same model is a distinct assignment. Include review, repair and handoff overhead. Estimated relative costs are estimates; unknown measured usage remains unknown. If a bounded contract is already authorized by the current user, approve its exact plan/config/acceptance argv through the supported planner approval command without asking again. Source changes invalidate approval and need a fresh operator review/attestation; expired or imported approvals never grant permission. A registered `planned_dispatch` invokes the same bounded planner through the existing native collector. Maintain semantic input when decisions or completed work change.

The 20% account reserve is independent: persist stop and save/verify, then stop ordinary work, even if another model shares the allowance. Never automatically resume on recovered/stale telemetry. Before an eligible worker, the dispatcher saves/verifies a checkpoint, executes only a supported adapter, validates completion, bounds retries and retains uncertain outcomes. If no qualified route or supported interface exists, keep a ready handoff and state the exact model/effort and reviewed resume command. Separate CLI workers do not switch the active desktop conversation.

For distinct Codex account profiles and qualified free local text workers, read [profiles and local execution](references/profiles-local.md). Keep identities, windows and source-account stops distinct; qualify the exact local model/schema/adapter. These workers share the current task authority and do not switch the active desktop chat.
