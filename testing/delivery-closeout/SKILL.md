---
name: delivery-closeout
description: "Use this skill for this scope: commit/PR-near handoff after QA/OR/UAT. Boundary: never performs VCS actions automatically. The requested effect, not discovery, decides AGDF activation."
---

# delivery-closeout

## Purpose
Standardize the operational delivery closeout.

It answers:

- what operational delivery status applies after QA, OR, or UAT
- whether a commit-ready Git summary should be provided
- whether a commit should be actively offered after `Approval: UAT`
- which next delivery step makes sense: commit, push, PR, rollout, or none
- whether evidence-based technical follow-up remains useful
- whether Context Graph follow-up from OR/QA remains open

This skill does not replace `qa-gate`, `release-or`, user approvals, or gate decisions.

## Runtime Contract
Use `continuation.runtime_contracts` after `skill_continuation`. If absent: listed MCP `agdf_inspect` (`operation: contract`, `module: <name>`); else supplied schema-2 executable/argv_prefix[0] `contract --module <name>`; else bundled files below. MCP reads need no hook or shell. Missing module: stop; never infer/search for runtime.

- `../../meta/contracts/closeout.md`
- `../../meta/contracts/context-graph.md`
- `../../meta/contracts/gate-transition.md`

`instruction_only`: first load `../../meta/contracts/task-target-resolution.md` and `../../meta/contracts/interaction.md`.

<!-- AGDF-REQUEST-ACTIVATION-GUARD:START -->
## Request Activation

- `owner`: `request_activation_contract`
- `path`: `meta/contracts/request-activation.md`
- `policy_version`: `1`
- `guard_fingerprint`: `sha256:af2f01f9e18a3ba1c520faf0691aa1cd4a4299bdfa027cf83651c5d14319bfdc`

Decide effect from loaded instructions before AGDF action.

Abstain silently (no AGDF call) for assessment/explanation/comparison/recommendation/review/diagnosis/advice; hypothetical/example/error/code/quoted/negated delivery language; AGDF as subject; or a read-only constraint absent other delivery. Ambiguity is read-only: answer or ask one neutral question.

Activate for any requested file/code change however small, a binding gate artefact, explicit AGDF/control-lifecycle operation or unambiguous active-run action; delivery wins mixed intent.

Invocation proof: explicit user text/trusted ephemeral action, not discovery/selection, skill load, hooks, cwd, repo/control or prior runs.

Then pick one catalog route; non-authorizing, downstream checks remain.
<!-- AGDF-REQUEST-ACTIVATION-GUARD:END -->

## Executable Dispatch

Use listed MCP `agdf_dispatch` (load deferred; host prefix allowed): `skill_id` `delivery-closeout`, `presentation_language`, `working_directory`, and only bound `target_source`/`primary_target` and `run_id`. Never search unlisted tools.
If absent/failing: supplied schema-2 executable, child-only environment, immutable argv_prefix, declared arguments; `--skill delivery-closeout`, language and working directory.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Quote shell values as data.
For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
On skill_continuation use only its target/control. Without that tool and a valid binding: `dispatcher_unavailable`; no runtime search, environment repair
or help retries. Dispatch never authorizes.

## Rules
1. Delivery follows gate clarity.
2. Never perform commit, push, or PR automatically.
3. Use one handoff format:
   - `Commit title`
   - `Commit body`
   - optional `Migration/Rollout note`
4. `Approval: UAT` unlocks an active commit offer when code changes exist.
5. No commit handoff for runs without code changes.
6. Always include exactly one next step and one quality outlook.
7. If OR, QA or current run state reports `context_graph_reconciliation: open_gap`, do not provide a clean commit-ready handoff; set the next step to resolve or explicitly retain the Context Graph gap.

## When To Use
- after `QA pass` with code changes
- after OR when delivery handoff should be clean
- after `Approval: UAT`
- when the user asks for commit, push, or PR handoff

Do not use as a substitute for `qa-gate`, `release-or`, or `gate-check`.

## Inputs
Use what is available:

- QA Report
- OR
- current gate status
- whether code changes exist
- existing commit-ready summary
- rollout or migration notes
- open technical risks or documentation gaps
- Context Graph impact from OR/QA/review
- Parent reconciliation projection already reported by OR

If code-change status is unclear, do not claim a commit handoff.

## Workflow
1. Classify the closeout:
   - `qa_pass_with_code`
   - `qa_pass_without_code`
   - `uat_approved_with_code`
   - `uat_approved_without_code`
   - `non_delivery_closeout`
2. Check Context Graph reconciliation from OR, QA, review and current run state.
3. If reconciliation is `open_gap`, report the delivery status as not cleanly handoff-ready and do not derive commit-ready Git text.
4. Derive Git handoff only when code changes exist and no unresolved Context Graph gap remains.
5. Set exactly one next delivery step:
   - offer commit
   - offer push
   - offer PR
   - no further delivery step
   - run QA/review
   - obtain UAT/approval
   - perform documentation follow-up
   - resolve Context Graph gap
6. Set quality outlook:
   - no further technical follow-up
   - more tests
   - refactoring
   - documentation sharpening
   - monitoring/runtime verification
   - Context Graph reconciliation
7. If `Approval: UAT` exists, code changes were delivered, and no Context Graph gap remains, actively offer the commit but do not run it.
8. If OR reports an `open` Parent reconciliation, retain its named Parent and one next action in the
   handoff while preserving an otherwise valid commit offer. This coordination warning is not a
   Child gate failure.
9. Consume Parent reconciliation from the OR only. Do not inspect sibling runs, infer Parentage,
   reevaluate evidence or mutate a Parent.

## Output
For code-changing runs:

```text
Delivery status:
Next step:
Quality outlook:
Commit title:
Commit body:
Migration/Rollout note:
```

For non-code runs:

```text
Delivery status:
Next step:
Quality outlook:
```

## Forbidden
This skill must not:

- decide QA pass
- replace OR
- execute commit, push, or PR
- invent a commit handoff for non-code runs
- imply new gate approvals
- rediscover, reclassify or repair Parent reconciliation outside the OR
