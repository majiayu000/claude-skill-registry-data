---
name: action-before-explanation-of-inaction
description: Grounds explanations of why an external action cannot or will not proceed in a real tool result, not in inference. Use before writing any clause of the form "X is blocked / waiting on / requires / needs / would fail" attached to an external action you have not attempted this turn. Use when about to explain why a PR cannot merge, why CI is waiting, why a deploy is held, why a permission is missing, or why any external system step is not proceeding. The safe action is attempted before the explanation is written; destructive actions are named and asked, not guessed at.
derives_from: ../../governance/action-before-explanation-of-inaction.md
---

# Action Before Explanation of Inaction

## Overview

An inaction explanation is a state assertion a reader will rely on. This skill runs the reversibility-gate protocol from the canonical rule [`governance/action-before-explanation-of-inaction.md`](../../governance/action-before-explanation-of-inaction.md) before any clause that explains why an external action cannot or will not proceed is emitted.

The rule is the source of truth for normative content (framework alignment, exception handling, rationale). This skill is the workflow wrapper: when to invoke the protocol and how to execute it step by step.

## When to Use

- Before writing "X is blocked because Y" attached to an external action (a PR merge, a deploy, a push, a status read, a permission check).
- Before writing "X is waiting on Y" / "X requires Y" / "X needs Y" / "X would fail because Y" attached to an external action.
- Before composing a turn-ending summary that explains why a step did not happen this turn.
- Before reporting a webhook subscription's silence ("CI must be still running") as a reason to wait.
- After a stop hook or pre-commit check fires, before drafting an explanation of the underlying state instead of addressing it.
- After an MCP tool returns a rate-limit, transient-network, or auth error, before treating that error as a reason to stop.

## Process

The reversibility-gate protocol from the canonical rule, executed in order:

1. **Identify the inaction explanation in the draft.** The trigger is the *pattern* (a state assertion about an external action attached to a clause that explains its non-progress), not the trigger words in isolation. "This function requires a string" is normal prose about an artefact. "The merge requires a reviewer," asserted without checking, triggers the protocol.

2. **Classify the action as safe-and-reversible or destructive.**
   - **Safe set:** status reads (CI state, branch protection, PR mergeability), pushes to a feature branch the actor owns, re-runs of a CI job or build or lint, a merge of a green PR through the project's documented merge mechanism in a project whose workflow has made that merge routine for the actor to perform.
   - **Destructive set:** force-push to a shared or protected branch, history rewrite, `reset --hard` over uncommitted work, deletion of data the actor did not create, production deploy, outward-facing publish, anything the project's documented governance or the operator's base instructions require to be confirmed before execution.
   - **When in doubt, treat as destructive.** Membership in the safe set is project-dependent; "merging a PR" is reversible-with-a-revert in a small project the actor co-owns and is outward-facing in a regulated repo. When the project file is silent on whether the action is routine, do not promote it into the safe set by default.

3. **For safe actions: attempt the action and report the actual tool result.** The attempt produces either success or a specific error response. Either grounds the next sentence; neither can be faked. If the attempt succeeds, the inaction explanation that was about to be drafted is moot and the message reports the success. If the attempt fails, the failure response names the cause and the draft is rewritten around the real cause.

4. **For destructive actions: name the action, state you have not attempted it and why, and ask.** The acceptable shape is "I have not run the force-push; it rewrites shared history, so I need your go-ahead." The unacceptable shape is "the branch is blocked because it would require a force-push": the same unverified-assertion failure dressed up in a scary-sounding reason to wait.

5. **Cross-check for decision doubt.** If the trigger appears *and* an authorial or ambiguous choice is also in scope (which option does the user want, which target branch, what scope), the [`clarify-before-acting`](../clarify-before-acting/SKILL.md) skill takes precedence: ask with named alternatives rather than attempt the optimistic action. Execution doubt is resolved by trying; decision doubt is resolved by asking.

6. **Rewrite the draft around the real result or the explicit "I have not attempted X".** Inaction explanations grounded in inference are removed. Action-grounded explanations ("the tool returned `mergeable_state: blocked`; the merge attempt then succeeded") replace them, or the explicit declination form ("I have not run X because it falls in the destructive set; need your go-ahead") replaces them.

## Red Flags

- Drafting "is blocked because", "is waiting on", "requires", "needs", "would fail", "can't because" about an external action without an accompanying tool call in the same turn.
- Inferring a destructive reason ("would need a force-push") to justify waiting, without checking the actual state.
- Hedging an unverified state assertion with "looks like" or "appears to": still a state assertion the reader will rely on.
- Polling against an external API in a loop instead of using a webhook subscription primitive when one is available.
- Composing the inaction summary in parallel with the tool call that would have grounded or refuted it.
- Reading user silence after an unverified inaction explanation as confirmation that the inaction was correct.
- Treating "the action did not happen" and "the action could not happen" as the same statement.

## Verification

The protocol is complete when one of the following holds:

- For a safe action: the action was attempted this turn, the tool result was read, and the message is grounded in that result (quoted or summarized with reference to the response).
- For a destructive action: the action was not attempted, the explicit "I have not attempted X because [property that places it in the destructive set]" form is in the draft, and a request for confirmation is surfaced.
- For an action the actor cannot attempt right now (tool unavailable, no credentials, network partition): the message says so explicitly and does not substitute a guessed cause for the missing attempt.

If none of these holds and the draft still contains an inaction explanation, the protocol is incomplete.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The system probably blocks this; saying so is cheap." | The user trusts "system facts" stated confidently. The cost lands on the user when the inference is wrong. |
| "I do not want to risk the action; better to explain and wait." | A safe action's failure is bounded; the explanation's wrongness is unbounded in the user's downstream decisions. |
| "Polling is the same as subscribing." | Polling consumes rate budget, fails silently, and produces output indistinguishable from "still running". Use the event primitive when available. |
| "Silence means the inaction explanation was accepted." | Silence is not signal. The user may not have noticed, or may be waiting for the action without further prompt. |

## See Also

- Canonical rule [`governance/action-before-explanation-of-inaction.md`](../../governance/action-before-explanation-of-inaction.md): framework alignment (NIST SSDF N/A; CSA CCM GRC-04 / GRC-05 / LOG-02; ISO 27001 Annex A.5.4 / A.5.18 / A.5.36 / A.8.15; OWASP ASVS V15.1 / V16.2), exception-handling protocol, and the discussion of why an AI coding assistant is the dominant target of this discipline.
- Related skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): handles decision doubt. This skill handles execution doubt. When trigger words appear with an authorial or ambiguous choice in scope, the clarify skill takes precedence.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): handles state assertions about artefacts the actor has not read. This skill handles state assertions about external actions the actor has not attempted. Together they cover the two main inference-vs-evidence failure modes.
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): handles gate failures. When a gate fails, fix the artefact rather than narrate why the gate cannot proceed.
