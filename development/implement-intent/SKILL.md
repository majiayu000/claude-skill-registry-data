---
name: implement-intent
description: Implement the repository's active intent only after running its deterministic preflight. Use when the user asks to build, implement, fix, or change product code under an intent.md. Works in keyless local mode and connected team mode.
---

<what-to-do>

If the repository has no `intent.md`, stop implementation and propose an intent for the user's actual request. Never substitute the workspace's most recent intent. Use `intent_save(localDraft: true)` with open `productChoices` for consequential behavior the request leaves undecided; each needs a recommendation, reason, alternative, trade-off, reopen trigger, and contingent claims. Do not copy those claims into required outcomes before a reviewer answers. In keyless mode, the person's explicit answer to each choice is recorded with `answer_product_choice`, which adds the accepted claims itself; never write a choice's state or claims by hand. If the installed server does not support this input, report the version limitation rather than claiming the choices were saved.

For team review of a new local draft, run `npx @pathmode/mcp-server@latest adopt` in the repository and relay its link and code for browser approval. Adoption carries the open choices and establishes repository ownership; an API key or a choice-bearing create does not. If adoption is unavailable, preserve the local draft and stop rather than create an unbound repository intent. After successful adoption, call `attach_original_request` with the verbatim request, then send the review link and stop at not ready. A terminal answer is not another person's judgment or workspace authorization. In keyless mode retain the source request alongside the intent and report the open choices; do not invent a cloud handoff.

Before applying a repository choice request, use `get_intent` to refresh the current body and read the request. Call `intent_save` using the request's original `changeRequestId` and `baseRepoBodyRevision`. Do not include new choice proposals or unrelated body edits in that apply. Unchanged sibling answers may apply sequentially; a changed target or parent needs renewed human review. Refused applies are not permission to bypass the request. A requested deferral still waits for application and remains a readiness blocker afterward.

After application, inspect the returned revision and stop for separate whole-revision authorization. In a fresh implementation session, call `get_intent` and verify that `authorization` is authorized and `authorizedRepoBodyRevision` equals `repoBodyRevision`, then use the existing readiness/prompt path below. A change-request read receipt is not proof that this authorized revision was read.


Read `intent.md` from the project root first. It is the repository-bound authority. Call `check_intent_readiness` before changing product code: with no arguments for that file, or with `intentId` only when the user explicitly selected a cloud-only intent.

If Preflight has unresolved blockers, show its exact verdict and work through the `preflight` repair loop one targeted question at a time. Do not silently begin implementation from a failing spec.

The user may explicitly accept named blockers and ask you to proceed. That is **accepted risk**, not a waiver: a waiver says a dimension does not apply, while accepted risk says the gap is real. Preserve the judgment by calling `intent_save` with the complete current spec and an added decision:

- `choice`: `Proceed despite preflight blockers: <exact gate names>`
- `ruledOut`: `Repair every blocker before implementation`
- `reason`: the user's stated reason, without embellishment

Re-run Preflight afterward and show the still-failing verdict. Never turn accepted risk into a green check. The acceptance authorizes only this implementation conversation; a later agent must ask again unless it has fresh human authorization for the exact revision.

In connected mode, a save changes the repository-body revision. Stop until a signed-in product manager authorizes that exact revision. Then call `get_agent_prompt`: use `mode: execute` when Preflight passes, or `mode: draft` when the user explicitly accepted still-visible blockers. Stop on an open change request or a pending, rejected, or stale authorization banner. Fetch `get_constitution` before implementation.

In keyless mode, do not call `get_agent_prompt`, `get_constitution`, or other cloud-only tools. Use `intent.md`, the repository instructions, and the codebase itself as the implementation context.

Create a small implementation plan mapped to the outcomes. Make only the changes needed for the authorized scope. Run the spec's verification checks, review the diff against outcomes, constraints, and edge cases, and finish with `handoff-intent` so material decisions and discoveries survive the session.

</what-to-do>

<supporting-info>

## Three independent judgments

- **Preflight** asks whether the spec is concrete enough to build and verify.
- **Accepted risk** records a human decision to proceed while a known gap remains. It never changes the Preflight verdict.
- **Authorization** confirms that a human permits an agent-originated repository revision to be implemented. It does not make a failing gate pass.

## Pull-request delivery

In connected mode, name the intent where the merge can find it: branch `intent/<intent-id>`, or `pathmode:<intent-id>` in the pull-request body. When a pull request is involved, do not call `update_intent_status`; the merge grades the real diff and owns the transition to Shipped. Without a pull request, mark Shipped only when the outcome is observable.

</supporting-info>

## When building contradicts the spec

Record the contradiction with `record_implementation_finding` the moment you find it. If you can name the exact correction, call `propose_spec_change` with the same finding (`findingId`), the `baseRepoBodyRevision` you read, the target field and item, the value you observed and the value you propose, and the contradiction as the reason. That records a proposal for a signed-in person to accept or reject and stores your observation as unreviewed evidence; it does not change the spec. Keep implementing against the current authorized revision. Never call `intent_save` for your own proposal, and do not re-propose anything listed under "YOUR PENDING PROPOSALS" in the execution bundle.

If adoption reports `AUTHORIZATION_PENDING`, preserve the draft and rerun the same command after the person approves.
