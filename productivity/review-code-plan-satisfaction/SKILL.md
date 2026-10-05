---
name: review-code-plan-satisfaction
description: Review implementation fidelity against `PLAN.md` and `AMENDMENTS.md`; emit `PS#` findings and validation-fact gaps into the task packet.
---

# review-code-plan-satisfaction

Phase 1 code review. Check whether the implemented change matches the approved plan and whether the claimed behavior is actually proved.

Keep this pass narrow, concrete, and findings-first.

## Read first

- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/review-phases-contract.md`
- `../references/compatibility-policy.md`
- `../references/final-state-authoring-policy.md`
- `../references/initiative-workflow-contract.md` when reviewing an initiative child packet
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter
- current task packet: `PLAN.md`, `AMENDMENTS.md`, `INDEX.md`, optional `CODE_REVIEW.md` if already present

## Core scope

Check:

- fidelity to `PLAN.md`
- fidelity to `AMENDMENTS.md`
- silent deviations
- missing approved amendments
- plan sequencing/design drift that should have triggered amendment
- validation facts: what was actually run, and whether it proves the claimed change
- whether `REVIEW_NOTE` markers were used only for non-blocking better alternatives
- unauthorized backward-compatibility work or unresolved compatibility decisions at real external boundaries
- canonical owner artifacts that still diverge from the plan because old/new vocabulary or status semantics were both kept alive

Not core scope:

- deep maintainability/evolvability/anti-slop review

## Core workflow

1. Establish review scope.
   - Identify the exact implementation commit under review, the exact diff from that commit, touched files, tests added or changed, and any untracked files that are intentionally part of the implementation.
   - Prefer reviewing the real patch over summaries from memory.
   - If the lead did not provide the commit hash and the workspace is dirty, stop and ask which commit is the review target instead of guessing from a floating workspace.
   - If the workspace has drift beyond the named commit, review the named commit and call out the drift explicitly so the lead can re-anchor the review.
2. Run a plan-fidelity pass.
   - Compare the implemented change against `PLAN.md`, not just against the desired outcome.
   - Flag silent deviations, missing amendments, and design changes made without approval.
   - Treat unapproved backward-compatibility code as non-compliant.
   - If the change touches a real external boundary and the packet never resolved whether backward compatibility was required, fail the handoff and require explicit human clarification.
3. Run a final-state fidelity pass.
   - Flag implementations that keep superseded contract vocabulary, owner semantics, or status models alive inside canonical artifacts when the approved plan chose one final model.
   - Flag code/docs/contracts that read like migration residue instead of the approved target state.
4. Run focused validation.
   - Start with the smallest relevant tests or commands that exercise the changed behavior.
   - Expand only as needed for confidence.
   - Record what was actually run.
5. Run a test-adequacy pass.
   - Treat a weak test as a finding when it claims to validate the change but would still pass if the bug remained.
   - Prefer one strong targeted test over a broad noisy suite.
6. Write or update `PLAN_SATISFACTION_REVIEW.md`.
   - Emit compact `PS#` findings ordered by severity.
   - Keep the explanation concrete and tied to the code path or missing proof.
7. Create or update `CODE_REVIEW.md` with the fixed rollup fields this phase owns.
   - If the file is missing, initialize it with the full canonical schema before handing off to phase 2.
   - `Compliance status:` `compliant`, `compliant_with_amendments`, or `non_compliant`
   - unresolved `PS#`
   - latest validation summary
   - `Phase 2 handoff:` concise note for maintainability review consumption
   - key dispositions already decided in `AMENDMENTS.md`
8. Update `INDEX.md` if review status changes.

## Findings bar

Only report a `PS#` finding when all are true:

- it is actionable
- it affects correctness, compliance, or confidence in the claimed behavior
- you can point to the exact code path, plan step, amendment, missing proof, or unauthorized compatibility layer

## How to inspect changes

- Start from the named implementation commit.
- Prefer `git show --stat <commit>`, then targeted diff reads, then final-code reads.
- Use workspace diff only to detect drift beyond the named review commit, not to silently move the review target.
- If behavior depends on runtime state, inspect both the writer and the reader.
- If behavior depends on persistence or recovery, inspect creation, update, load, and restart paths together.
- When reviewing tests, ask whether the assertion would fail if the bug still existed.

## Requester-response rule

Always report the review result back to the requesting side.

- If the lead/orchestrator requested the review, reply back to the lead/orchestrator.
- If a human directly requested the review in this pane, reply back in this pane.
- Local pane output without an explicit reply to the requester does not count as review completion.

## Output shape

Default output should include:

- findings first, highest severity first
- exact `PS#` findings
- concise validation notes
- explicit compliance verdict
- residual validation gaps if there are no findings

## Do not

- collapse this into a generic maintainability pass
- bless claimed validation that was not actually run
- confuse desired outcome with plan compliance
- write tracked `AGENTS.md`
- write `AGENTS.override.md`
- treat unapproved compatibility shims as harmless implementation detail
- accept canonical code/docs/contracts that visibly preserve both an old and a chosen new model

## Initiative child packets
For initiative-created child packets also check:
- alignment with `Parent Initiative` and `Imported Context`
- declared dependencies and contract surface still match the implementation
- optional `CONTRACT_DECISION.md` was followed when present
- `PLAN.md` was authored, not left as `Status: not_authored`

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
