---
name: author-build-plan
description: Draft /implement's build plan for ONE epic — the working spine of the build. Reads the epic's box (the epic record, its functionalities' ICE, the slice's six lenses, the captured repo context + test harness) and breaks the epic into PIECES — stories, tasks, tests, docs — with explicit dependency edges forming a DAG, test-first (every epic acceptance criterion covered by a test piece authored from the spec, never from the implementation). Every piece carries a grounding citation into the box (epic | ice | lens | repo) — an ungroundable piece becomes an open_question, never invented work. Writes the plan draft to STM only, never the product model. Also applies revision directives (re-plan after retry exhaustion, steelman refutations as new pieces) to an existing draft. The generative planning work for the /implement play.
version: 0.1.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob, Grep
---

# author-build-plan

Turns one **ready epic** into its **build plan** — the ordered set of pieces /implement
executes. The epic is the tightest box: everything this plan may contain is what the epic
carries or references (outcome, user_check, functionality refs → ICE, acceptance, context)
plus the slice's six lenses and the repository as it actually exists. The plan never
crosses those walls; where the box has no wall, the skill records an open question — only
the human draws a new wall.

This skill drafts; it never persists to the model and never publishes. /implement
validates the draft mechanically (`validate_plan.py`), publishes it to the epic's issue
(project-orchestrator), and anchors the build to it.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `epic_file` | yes | The epic record (read-only) — the box: outcome, user_check, functionality_refs, context, acceptance. |
| `functionality_ices` | yes | Resolved ICE paths for the epic's functionality_refs (from the readiness gate). Referenced, never copied. |
| `lens_dir` | yes | The slice's lens folder (read-only) — quality (gates the build must end passing), architecture (components the work threads), ux, agentic, run. |
| `box_context` | yes | The captured repo context from the play's context step — affected areas, conventions, existing surfaces. |
| `harness` | yes | harness.yaml — the project's detected test/lint/build commands; names the test framework test pieces use. |
| `plan_path` | yes | Output path under STM for `plan.yaml`. |
| `directives` | no | Path to a revision-directives file (re-plan after retry exhaustion, or steelman refutations to absorb as pieces). When present, revise the existing plan at `plan_path` per the directives instead of cutting fresh — never silently rewrite unrelated pieces, and never delete a `done` piece. |

## Procedure

1. **Read the box.** The epic record, every functionality ICE, the six lenses, the
   captured repo context, the harness. The plan derives from these and ONLY these.

2. **Cut test-first.** For every epic acceptance criterion, author a `test` piece first —
   derived from the acceptance text and the ICE, never from any implementation piece. A
   test piece's `acceptance_refs` lists the acceptance indices it covers; it must not
   depend on a story/task piece sharing those refs.

3. **Cut the work.** Stories (user-visible behavior), tasks (the internal work a story
   needs, pulled INTO the story's chain — never standalone-internal without a surfacing
   story), and `docs` pieces (the documentation the change requires — or record
   `docs_waiver.reason` when genuinely none). Wire `depends_on` into an acyclic DAG with
   at least one dependency-free piece; order follows the epic's acceptance and the
   architecture lens's component seams.

4. **Ground every piece.** Each piece carries `grounding: [{source, ref}]` with source one
   of `epic | ice | lens | repo` and a ref precise enough to check (an epic field, an ICE
   path + clause, a lens file + entry, a repo path). A piece you cannot ground is NOT a
   piece — record it under `open_questions` with what it is and why the box has no wall
   for it.

5. **Write the draft** to `plan_path`:

   ```yaml
   plan:
     epic_ref: <epic id>
     created_by: author-build-plan
     version: 1
     pieces:
       - id: p-1-<slug>
         kind: story | task | test | docs
         title: <one line>
         intent: <what this piece delivers, one line>
         grounding: [{source: epic|ice|lens|repo, ref: <checkable ref>}]
         acceptance_refs: [<epic acceptance indices>]   # tests: required; others: where relevant
         depends_on: []
         status: planned
         files_hint: []        # best-guess touched paths; the box check uses reports, not this
     docs_waiver: {reason: ""}   # only when no docs piece exists
     open_questions: []          # [{question, context}] — gate the play's checkpoint
   ```

6. **Revision mode** (`directives` present): apply each directive — new pieces for
   refutations (grounded in the refutation's cited gap), re-planned pieces for retry
   exhaustion — bump `plan.version`, keep `done` pieces intact, and leave a
   `revision_note` per changed piece naming its directive.

## Output contract

Return JSON only: `{"plan": "<plan_path>", "pieces": <n>, "open_questions": <n>}`.
The artifact lives on disk; the contract carries paths, never content.
