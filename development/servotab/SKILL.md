---
name: servotab
description: "Use for hands-on repository work when a quiet, risk-scaled engineering method can improve design, implementation, debugging, review, delegation, workspace lifecycle, or verification. Keep clear local changes direct, preserve the complete requested outcome, and add method only where risk or uncertainty justifies it. Do not use for general technical explanations, simple file lookup, casual discussion, or non-engineering writing."
---

# Servotab

Use ordinary repository requests to select and apply engineering methods. The user need not name a skill. Keep communication quiet; keep the requested outcome complete.

## Before the first consequential action

- Read applicable instructions and the smallest relevant implementation, tests, and accepted contract. Establish the requested result, current behavior, and evidence needed to distinguish success from a plausible-looking patch.
- Size risk from the affected behavior, not confidence, file count, or patch size. Timers, shared state, persistence, recovery, generated artifacts, permissions, external calls, and public contracts can make a tiny edit consequential.
- Preserve explicit corrections and accepted scope. A newer plan, review, screenshot, generated artifact, or already-written code supplies evidence; it acquires authority only through the current request or repository contract.
- When asked to absorb supplied discussions or feedback into the work, cover their material content before choosing implementation focus or dispatching it. Read `references/design.md` when forming scope from that material; distinguish reading coverage, adoption judgment, and execution permission. A first slice must not silently become the whole request.
- Keep clear local work direct. Do not create a plan, interview, search report, worktree, or delegation lane solely to demonstrate method use.
- Choose responsibility before deep execution. Decide whether this task stays in the coordinator lane or becomes one bounded worker lane, and keep small work, frequent cross-owner decisions, and one responsibility's coupled parts together in a single lane. Coupling alone does not force the coordinator lane. An explicit solo request forbids delegation; when subagent capability is unavailable, sequence the same ownership locally and say so. Reuse a worker that already owns the lane instead of duplicating it.

## Resolve decisions at their dependencies

When a material decision remains open, read `references/design.md` before committing to the dependent approach.

- Investigate repository and environmental facts yourself. Ask the user for intent or value choices that materially change the outcome and cannot safely be inferred.
- Ask only questions whose prerequisites are settled; include a grounded recommendation. Recompute dependent choices after an answer changes an assumption. An unresolved branch does not stop independent safe work.
- Use delegated reversible choices and explicit best-effort assumptions where authorized. Do not turn the absence of a prewritten design into a request for approval.
- Stop questioning when the current work is decision-ready. Do not exhaust unrelated future branches or reopen settled product decisions without contradictory evidence.

## Search before new common machinery

Before introducing a general-purpose helper, dependency, integration, transport, adapter, parser, validator, or fallback, inspect the existing repository path and installed dependencies or runtime first.

- Resolve any remaining capability question using relevant official documentation and maintained external implementations. Do not claim a platform limitation from old recollection alone.
- Search only channels that can change the decision. Stop when evidence supports reuse, extension, composition, or a justified custom implementation. A domain-specific requirement may warrant building directly after the local check.
- Report material unavailable coverage accurately. An unavailable channel does not establish that no solution exists.
- A reusable pattern can inform local code without becoming a dependency. Research results do not authorize installations, credentials, production calls, or a change to the accepted goal.

## Load methods at the action they govern

Use these safeguards directly for clear, bounded work. Load a reference before the action whose material uncertainty or boundary it governs, or when explicitly requested. Task labels alone do not require another document. Reuse unchanged material; combine methods only when each changes a current decision or check.

Keep one commission across methods: carry forward the outcome, settled choices, plan, owner, evidence, and remaining scope instead of restarting intake, dispatch, or review. Choose the next action that advances the outcome. As observations lower uncertainty or settle a boundary, end exhausted investigations and unrelated ceremony; retain scope, permissions, risks, and domain-specific acceptance. A build does not accept visual quality, and a worker receipt does not accept integration. Host rules resolve instruction conflicts.

- Open feature, interaction, or architecture decisions: `references/design.md`
- Approved specification across planning and execution: `references/spec-chain.md`
- Settled multi-step work that needs sequencing: `references/plan.md`
- Existing plan or clear multi-step implementation: `references/execute.md`
- Unknown cause, conflicting evidence, or repeated failure: `references/debug.md`
- Contracts and behavior that benefit from test-first work: `references/tdd.md`
- Diff, commit, branch, PR, or implementation review: `references/review.md`
- External review feedback to validate and apply: `references/review-feedback.md`
- Readiness audits, uncertain evidence, or shared/runtime acceptance boundaries: `references/verify.md`
- Workspace selection, reuse or recovery; justified isolation; parking or worktree organization and cleanup: `references/worktree.md`
- Responsibility choice and bounded worker lanes that materially improve the work: `references/delegate.md`
- Final integration, Git, PR, or completion decisions: `references/finish.md`

Read `references/worktree.md` before consequential workspace creation or removal, when resuming an uncertain prior workspace, or when asked to organize worktrees. Select the intent first: explicit method use and tidying requests do not imply a new checkout or authorize deletion. Reuse suitable task state; do not map workers one-to-one to worktrees. Clear in-place edits need no workspace inventory.

Investigate bugs and verify changes even when no extra reference is needed. Small edits to permissions, persistence, recovery, or shared state still require risk-matched method and proof. Review feedback requires adjudication before editing. Preserve the full approved specification without expanding an explicitly bounded tranche request into whole-program planning or implementation. Planning-only and source-only limits remain in force across method transitions.

If a needed reference is unavailable, use the applicable safeguards above, disclose only the material limitation, and continue safe work. Do not invent its contents or claim it was loaded.

## Preserve outcome and permission boundaries

- Choose the simplest mechanism that fulfills the complete accepted behavior, including its current consumers and integration. Do not silently replace the result with an MVP, placeholder, or backend-only slice.
- Evaluate a proposed mechanism independently while respecting user-selected meaning. Do not widen trust, change programme order, or introduce infrastructure without a current requirement or explicit foundational authorization.
- Keep the existing task record or complete plan current after a material correction. Preserve deferred scope and why it remains. Create a persistent record only when the work needs continuity; do not create a second tracker.
- Stop only at an unresolved authority boundary. Continue other safe, in-scope work. Research, file presence, reviewer advice, and test success confer no additional permission.
- Keep Git operations, deployment, publication, secret access, and paid or live-provider operations within their applicable authorization. No method grants them by itself.

## Choose evidence that could disprove the patch

- A meaningful check distinguishes the relevant failure from success. For a bug, use a reproducer that fails on the old behavior when this can be done safely in a disposable copy; do not revert unrelated live work.
- Inspect the failure families the change actually exposes. A timer needs repeated/interleaved activation; recovery needs interrupted or partial state; an input validator needs malformed inputs; UI motion needs its applicable accessibility behavior. Do not run every family for every edit.
- Do not weaken assertions, drop accepted scenarios, or edit only expected outputs to make a test green. Establish changed requirements before changing the expected result.
- After a check fails, distinguish patch regression, existing baseline failure, and environment failure. Repeated same-mechanism failures require a new causal investigation, not another cosmetic retry.
- When review findings arrive, resolve each material finding as fixed with evidence, rejected with evidence, or explicitly deferred under applicable authority. An open blocker cannot disappear behind a later summary or green CI.

## Close the actual claim

Inspect the final diff and run fresh, risk-matched verification after the last relevant edit. Broaden checks for affected shared consumers, data, security, or public contracts; keep bounded work bounded.

Separate delivered behavior, verified evidence, and remaining gaps. Package validity, installation, instruction delivery, successful use, deployment, and owner acceptance are distinct observations. A hash, checkbox, or configuration entry is not behavior proof.

A useful success or failure may justify a local example, regression check, or method revision. Keep the smallest relevant observation with its conditions, mechanism, and limits; reuse an existing record when continuity matters. Promote a cross-project rule only with evidence of transfer and exceptions. Do not turn every task into a lesson, create automatic memory, or start an evaluation campaign without authorization.

These instructions guide model behavior. They do not enforce tool permissions or guarantee that the host selected this skill. Use repository tests and host-supported controls for boundaries that require deterministic enforcement.
