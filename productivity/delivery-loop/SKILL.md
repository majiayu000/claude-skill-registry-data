---
name: delivery-loop
description: "Execute an approved Markdown task packet through a bounded loop: validate it against the repository, implement it, run targeted tests and builds, fix failures, and retest. Use for delivery loops, executing task Markdown, implementing a task packet, or test-build-fix-retest work. Research and planning belong to task-research and the task owner; PR work belongs to fast-pr-workflow."
license: MIT
metadata:
  display-name: "Delivery Loop"
  version: "2.1"
  platforms: "claude-code codex"
  tags: "workflow implementation verification repair"
---

# Delivery loop

Execute one approved Markdown task packet without reopening settled product or architecture decisions.

Read [references/delivery-checklist.md](references/delivery-checklist.md) at the start of the run and keep its concise evidence block current.

## Entry contract

- Identify the exact task Markdown named by the request. Stop if more than one file could be the authority.
- Treat the task as an execution contract, not proof that its repository claims are current.
- The current request must authorize implementation. A packet produced by another skill does not grant permission by itself.
- Research and decomposition are complete before this loop. Route missing repository evidence to `task-research` and return unresolved product or architecture decisions to the task owner. Never solve either silently during implementation.
- Repository instructions and project workflow skills outrank the packet when they conflict.

## Four phases

1. **Validate task Markdown**
   - Read the packet and applicable repository instructions completely.
   - Record the full `HEAD`, branch, upstream ref, and worktree status. Verify the packet's committed evidence with its pinned commit and keep dirty or ignored evidence separate.
   - Run pinned evidence commands against the named object. If a mutable ref matters, assert its full object ID first; do not let the checkout's current `HEAD` stand in for the packet base.
   - Verify the base commit or ref, prerequisite output identities and digests, referenced files, symbols, behaviors, dependencies, and verification commands against the pinned object plus any explicitly separated relevant local state.
   - Confirm exactly one writable repository and delivery history. Stop if the packet silently couples separate repository writes or PRs.
   - Classify commands as runnable current-state proof or post-change proof. Run safe preflight, confirm exact working directories and tools, and inspect output collision, idempotency, retry, and partial-failure recovery before editing.
   - Verify toolchain and credential provenance. Reject unprovenanced ambient installs and implicit cross-job filesystem assumptions. Record actual credential capability, treat it as no authorization to mutate, and require least privilege when the packet's threat model does.
   - Confirm every mandatory top-level section or equivalent embedded-ledger field is present: Readiness, Objective, Why, Scope, Starting point, Decisions already made, Decision authority, Contract, Change required, Invariants, Non-goals, Acceptance, Verify, Escalate, and Handoff. A field that truly does not apply must remain present and say `Not applicable - <reason>`.
   - Run a packet-provided validator command when one is part of Verify. Structural green does not replace repository evidence checks.
   - Read packet status separately from the informational canonical tracker status. Only `READY`, `BLOCKED_BY_SPEC`, or `NO_CHANGE_NEEDED` in the packet controls this loop.
   - Confirm the packet distinguishes existing code from proposed work.
   - Record exactly one outcome: `READY`, `BLOCKED_BY_SPEC`, or `NO_CHANGE_NEEDED`.
   - `READY` enters implementation only when inputs resolve, tracked and untracked state is clean or explicitly isolated, and the execution path is collision-safe. `BLOCKED_BY_SPEC` stops before editing with the conflicting claim, repository evidence, decision owner, and exact output needed. `NO_CHANGE_NEEDED` records no implementation change and runs the complete acceptance proof from the pinned clean or isolated state, including required cross-repository, runtime, browser, artifact, or served-response checks, before handoff.
2. **Implement**
   - Make only the changes required by the validated packet, using the repository's existing patterns and relevant stack skills.
   - Read each complete target file before editing. Never reconstruct a file from a snippet, search result, or partial transcript.
   - Preserve unrelated work and every stated invariant, public contract, compatibility rule, and non-goal.
   - Do not weaken acceptance criteria or tests to make the implementation pass.
   - Start from the packet's reproducer or baseline observation, then follow its exact read set and write set. Preserve failed evidence and use only the approved retry identity.
   - Return to the validation gate if repository evidence changes or implementation appears to require new scope, a dependency, schema work, or another unsettled decision.
3. **Test and build**
   - Run the packet's focused checks first, then its broader relevant tests, type checks, linters, or build commands.
   - Add or update a regression test when the packet requires one and the repository has an established test location.
   - Record exact commands and actual results. Classify failures as product, test, environment, or preexisting.
4. **Fix and retest**
   - Fix only in-scope product or test defects.
   - Rerun the smallest check that proves each fix, then rerun every broader command affected by the change.
   - Repeat until the packet's acceptance and verification contract is green or a stop condition is reached.

## Loop bounds

Stop after two materially similar failed repair attempts, after three repair cycles without convergence, or when progress needs credentials, dependency installation, destructive action, external service access, or expanded scope. Produce a diagnostic handoff with the failing command, observed output, attempted fixes, and unresolved question.

## Optional durable state

Use durable state only for work likely to cross sessions or explicit pause/resume requests. Run `scripts/delivery-state.py init <task> --repository .`, then update the generated record after each phase or material failure. On resume, run `scripts/delivery-state.py verify <task> --repository .` before writing.

Do not hand-create or reimplement private state. The helper rejects symlinked parents and targets, rejects hardlinked targets, enforces mode `0600`, and verifies the state is actually ignored and untracked. State records evidence only; it does not add phases or authorize implementation, Git, or external actions.

When an allowed browser command needs the shared local browser resource, run it through `scripts/browser-suite-lease.py` and pass the exported worker limit to the runner. Browser coordination is part of test execution, not a separate phase.

## Optional PR handoff

PR work is not a delivery phase. After all required checks pass, invoke `fast-pr-workflow` only when the current request explicitly authorizes the relevant commit, push, or pull-request action. Otherwise stop with a local handoff that is ready for that workflow.

## Handoff

Report the task file, readiness outcome, changed files, commands and actual results, failures and fixes, reruns, discrepancies, blockers, whether `fast-pr-workflow` was authorized, and the full PR URL as a standalone Markdown link when one exists. Keep it factual and concise.
