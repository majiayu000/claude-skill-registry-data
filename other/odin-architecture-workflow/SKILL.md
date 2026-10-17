---
name: odin-architecture-workflow
description: Orchestration doctrine for the Architecture workflow — gather structural context when it is not established, draft the arc42 architecture with a decision record for each structurally significant decision, ratify, persist into the target project (creating the folder layout when absent). Standalone; run to completion as a stage of a larger plan.
---

# Architecture Workflow

## Purpose

Define the orchestration doctrine for the Architecture workflow — a trigger-gated workflow that produces one arc42 architecture document and persists it into the target project. It packages the pattern `[Context → Review] │ Draft │ Checkpoint │ Persist → Review │ Response`.

**Judgment and mechanics have separate owners, in separate media.** Kvasir authors one architecture Workfile in the workspace and touches no project file; Brokk fills the folder layout in the project — creating it when it is absent — strictly by that Workfile's layout map, and decides nothing. No role writes in another's medium.

**The drafting step receives no review — permanently, for this one step.** Its gates are the ratification checkpoint, where the user or adoption ratifies the decisions, and the persistence review, which checks the persisted form mechanically, including that the target's state matched the Workfile header before anything was written. The standing per-Subtask review applies to every other dispatched session.

This skill is dispatch doctrine only. `mimir-architecture-context`, `kvasir-software-architecture`, `heimdall-architecture-review`, and `brokk-architecture-persistence` are the per-step methodologies, loaded by the dispatched sessions themselves. Briefs name the skill, the inputs, and the output to write — **never the method**.

**Fixed Deliverable (per § Deliverables and § Deliverable Determination in your system prompt):** a Response (drafted by Bragi, step 5) and an Artifact (the persisted arc42 directory — a folder per section holding its documents and index, the decision records in their own folder, and the top index):

```text
Deliverable: response=yes, artifact=yes — persisted arc42 directory (absent only when the user declined persistence or a review blocked the run), source=workflow-fixed
```

**Kvasir Consultation Check:** this workflow is exempt (`Kvasir check: substantive Subtasks=<n>, criteria=<…> → skip — packaged workflow`). Its strategic consultation is internal — the drafting step — and its ratification checkpoint is the user's steering point. Mid-Execution Consultation and Failed Review Classification remain in force inside the workflow.

## When to Use

- When the Architecture check verdict is **invoke** — via the `/yggdrasil/architect` command, explicit document-the-architecture, as-is, arc42, decision-record, or decide-the-architecture language, or a user-accepted suggestion, per the Trigger Thresholds in your Communication Policy.
- **As a stage of a larger plan:** run this workflow to completion, exactly as you run Research or Deliberation. No request line and no result line exist.

**Firing criteria** — when architecture work is warranted at all. It fires when ANY: architecture, a decision record, or arc42 documentation is asked for; a change introduces components, modules, or services, or crosses a module boundary; a change adds an integration, a persistence mechanism, a schema change, or a dependency; multiple viable structural approaches carry material trade-offs; non-functional requirements drive the design. It fires **without exception whenever two or more work packages are expected** — the split is an architecture decision and the packages need the contracts §5 specifies. Skip when the change fits the existing structure and one package suffices, or the user declines.

A request to explain a codebase's structure where no architecture document exists is a *suggestion candidate*; a pure research request or a question is a **skip**.

## Workflow

1. **Context (conditional).** Skip Mimir only when the module boundaries, entry points, boundary interfaces, and existing architecture documentation of the system in scope are already established in the conversation — supplied by the user, or by a reviewed `NN-context-architecture-*.md` from an earlier run in this session — or when the objective is greenfield with no code yet. Otherwise dispatch. A TDD-context Workfile is **never** a skip reason: it records behavior, conventions, and test infrastructure, none of which grounds a §5 blackbox. Record the skip as `Context: skipped — <reason>`, never silently.

    Brief: the objective; the declared scope — the system or a named subsystem when the objective records it, the change's structural footprint when it changes something; the architecture location, so the documentation inventory looks there first; and the requirement that the output be **fact-rich and framing-poor**, with proofs per finding. Exclude task-scoped facts — the runner and its commands, the conventions new code must imitate, implementation-phase test infrastructure, and what the touched paths do today. Writes `NN-context-architecture-<area>.md`; its standing review is `Focus: context`.

2. **Draft (unreviewed).** Dispatch Kvasir with `kvasir-software-architecture`, the objective, the architecture location — stated so its two-fact target check has somewhere to look — the path of the Workfile to **create** (`NN-architecture-arc42.md`), and the requirements and context Workfile paths when they exist. Record from its report: the header's `Target:` and `Document scope:`, the `Section scope:` line, the decision list with each decision's kind and one-line rationale, the `Package check:` line (or `n/a`), and the investigation gaps.

    **Every record ships at `Status: Proposed`.** Ratification is the checkpoint's; promotion to `Accepted` is persistence's. Neither is the author's.

3. **Ratification checkpoint (no dispatch).** Surface exactly: the decisions awaiting ratification — ID, title, kind, one-line rationale; the context review verdict, or `context skipped — <reason>`; the persistence location, with the header's `Document scope:` read out as *the layout will be created* (`seed`) or *merged into the existing document* (`update delta`); and the dispatch cost, qualitatively, with the count on request. Whether to pause for steering or auto-proceed is governed by your Communication Policy; when auto-proceeding, ratify by adoption and let the summary ride the Deliverable disclosure.

    Record the outcome as the **ratification record**, one line, in the grammar `brokk-architecture-persistence` § The Ratification Record defines — echoed here so you can write it; that section, not this echo, is normative:

    ```text
    Ratification: ratified=<ADR-NNNN[, ADR-NNNN …] | none>, withheld=<ADR-NNNN[, ADR-NNNN …] | none>, by=<user | adoption>
    ```

    Every decision in the Workfile's Appendix A appears in exactly one of the two lists. The user may withhold individual decisions — those records persist at `Status: Proposed` — or decline persistence altogether: record `persisted=declined`, skip step 4, leave the Workfile in the workspace, and say so in the Response.

4. **Persist (unless declined).** Dispatch Brokk with `brokk-architecture-persistence`: the architecture Workfile path, the ratification record, and the pinned baseline. The session creates the folder layout when — and only when — the target is absent **and** the header reads `seed`; otherwise it fills the existing layout by the Workfile's Appendix C. It returns the persistence manifest. Its standing review is `Focus: persistence`.

    **The session checks its own preconditions and writes nothing when they fail.** A failed precondition is a drafting-side defect: resume Kvasir once to correct the header or renumber, then re-dispatch persistence. Never re-brief persistence to make it fit.

5. **Deliverable (Response).** Dispatch Bragi to draft the user-facing response from the reviewed outputs: what the document covers and what it omits; the architecture summary (§4 Solution Strategy in a paragraph); the top index path and the decision-record paths; whether the layout was created or an existing document updated; the open risks from §11; the investigation gaps; and what the user should verify. When the user declined persistence, say so. When prior architecture documentation exists beside the target, name it and state that the workflow left it untouched — retiring it is the user's decision. Writes `NN-response-draft.md`. **When this workflow is a stage of a larger plan, these items ride the enclosing plan's Response and this step is folded into it.**

**Failure handling (one rule).** A `BLOCKED` context or persistence review goes through § Failed Review Classification: resume the producing session **once** for an execution defect; a plan-level mismatch, or a second `BLOCKED`, ends the run — no Response claiming success, and the review path named to the user. Files persistence created before a block stay in place and are disclosed; this workflow does not delete project files it created.

**Review-skill assignment:** every review gate dispatches a fresh Heimdall session with `heimdall-architecture-review` and exactly one `Focus:` line.

| Reviewed node | Brief line | Workfile |
| --- | --- | --- |
| Context session (step 1) | `Focus: context` | `NN-review-context-architecture-<area>.md` |
| Persistence session (step 4) | `Focus: persistence` | `NN-review-architecture-persistence.md` |

Supply the originating brief, the artifact paths, and the pinned baseline with every dispatch. The Kvasir and Bragi sessions receive no dedicated review.

## Quality Criteria

- **Ratification is explicit** — every persisted decision was ratified at the checkpoint or by recorded adoption, and only then promoted to `Accepted`.
- **Every skip is recorded with its reason**, never taken silently.
- **Only §1–§12 and the decision records persist.** Appendices B and C of the architecture Workfile are transient planning content.
- **One Workfile per run.** The drafting session creates `NN-architecture-arc42.md` and every later step reads that same file.
- **The target's state is verified against the header at persistence**, never assumed from the draft.
- **The drafting step is the one unreviewed node, by design**; its output reaches the repository only through the checkpoint and the persistence review.
- **The Deliverable discloses** the decisions ratified, the persisted location and whether it was created or updated, any prior documentation left untouched, and the investigation gaps.
- **Cost:** 3 dispatches with context already established, 5 when the context gate fires, 1 when persistence is declined; add 2 when this workflow runs standalone — the Response and the Final Review Gate. Disclose it qualitatively at the checkpoint and quantitatively on request.

## Anti-Patterns

- **Restating a specialist's method in a brief.** Name the skill, the inputs, and the output.
- **Re-introducing a review of the drafting step, a mode line, or a pre-drafting structure dispatch "to be safe."** All three were removed by design; adding one back costs a dispatch and restores an inconsistency the redesign eliminated.
- **Re-briefing persistence to create over a present target, or to fill an absent one, when its precondition fails.** The header is wrong, and Kvasir fixes headers.
- **Persisting after a `BLOCKED` verdict**, or drafting a Response that reports success over a blocked review.
- **More than one resume per blocked node.** One resume for an execution defect; a plan-level mismatch or a second `BLOCKED` ends the run and surfaces the review.
- **Deleting project files on abort.** A run that stops at a blocked review discloses what it wrote and leaves it; removal is the user's direction.
- **Treating a TDD-context Workfile as structural evidence.** Behavior, conventions, and a baseline test run do not establish module boundaries, entry points, or boundary interfaces, so skipping step 1 on one leaves §5 ungrounded and makes the recorded skip reason false.
- **Creating a second architecture Workfile.** A parallel draft guarantees two documents that disagree.
- **Skipping the Final Review Gate.** The Deliverable — the Response and the persisted directory — is user-facing output and must pass the gate like any other.
