---
name: compile-intent
description: Build a structured intent spec through guided conversation, one decision at a time with a recommended answer for each. Use when the user wants to define what to build, sharpen a vague idea into a testable spec, or capture product intent before writing code. Writes intent.md in the project root and (if an API key is set) syncs to a Pathmode workspace.
---

<what-to-do>

Invoke the `compile-intent` MCP prompt from the @pathmode/mcp-server. This starts a guided conversation that turns a vague problem into a structured intent spec.

For each question you ask, propose your best-guess answer based on the conversation so far. Don't make the user generate from a blank page.

Before the spec is finished, gather implementation context. You are already sitting in the repo, so read it: which files and modules this change lands in, what already exists there, what it would touch, and how it could be verified. Pass it to `intent_save` as `implementationContext` — in both modes. A brand-new spec has no intent id yet, so there is nothing to address a separate call to; `intent_save` carries the context through as part of the save. Use `record_implementation_context` only to update the context on an intent that already exists. It is free text, sub-headings welcome, and it is advisory — it never changes the readiness verdict. Its job is to stop the implementing agent from rediscovering the codebase from scratch, and to catch the case where the thing being specified half-exists already.

Save the proposal before pretending its open choices are requirements. Use the typed `productChoices` input on `intent_save` for consequential unanswered behavior; supply only proposals, never state, human actors, timestamps, or source-settlement flags. Existing choice IDs are stable; do not replace a question by recycling its ID. Word each contingent outcome claim as an observable result (a state, a number, a visible element) before the first save, because a saved choice cannot be edited: accepting a choice adds its outcomes to the spec, and the preflight flags any it cannot read as measurable, since such an outcome counts against the outcomes check. If one is flagged, say so when you explain the choice; the answer can then carry a measurable outcome instead (`answer_product_choice` action `change` without a workspace, the reviewer's change with one). The server preserves existing choices. A failed capability check means this installed path is unavailable, not that the question was recorded.

For a new choice-bearing proposal, call `intent_save(localDraft: true)` to write `intent.md` locally, then run `npx @pathmode/mcp-server@latest adopt` in the repository and relay its link and code for browser approval. Adoption preserves the open choices and establishes repository ownership. Ordinary v1 creates remain cloud-owned and reject choice proposals. Do not detach an already connected file with `localDraft`; add proposals through its normal connected save once it has repository authority. After successful adoption, call `attach_original_request`, copying the original request verbatim, and invite the reviewer to the adopted proposal. Stop while its choices remain unresolved or its exact revision lacks human authorization. Answers create corrections for the repository agent to apply; application and authorization are separate steps.

</what-to-do>

<supporting-info>

## Why a conversation, not a template

The compile-intent prompt is interrogative on purpose. It pushes back on vague language, challenges unmeasurable outcomes, and forces concrete constraints before moving on. Specs written in one shot tend to be wishful; specs that survive grilling are agent-ready.

## Output shape

`intent.md` at the project root:

```markdown
---
id: "intent_..."
version: 1
status: "draft"
---
# [Title]

## Objective
[What needs to change and for whom]

## Implementation Context
[What the repo actually looks like where this lands — read from the working tree, not guessed]

## Outcomes
- [ ] [Observable state change, testable in under 5 minutes]

## Edge Cases
- **[Scenario]**: [Expected behavior]

## Constraints
- [Hard limit — what must never happen]
```

If `PATHMODE_API_KEY` is set, the spec also syncs to the user's Pathmode workspace and becomes visible to other team members and other agents.

## Evidence in a file that lives in git

`intent.md` is committed, so everyone who clones the repo can read it forever and deleting a line later does not remove it from history. Under the IntentSpec repo-safe profile the file must not carry raw customer quotes, names or contact details of individuals, support transcripts, confidential internal metrics, or credentials. Cite evidence as a summary or a reference instead: a ticket id, a dashboard name, a one-line paraphrase. Full evidence with quotes and attribution belongs in the private system of record (a connected Pathmode workspace), and the repo file points back at it. A claim with no evidence yet is labelled an assumption, not dressed as a fact.

## Downstream skills

After compiling, these skills consume the spec:

- `grill-intent` — re-enter the conversation to find weaknesses before code gets written
- `review-against-intent` — check code changes against outcomes and constraints
- `handoff-intent` — capture decisions and discoveries back to the spec at end of session

</supporting-info>

If adoption reports `AUTHORIZATION_PENDING`, preserve the draft and rerun the same command after the person approves.
