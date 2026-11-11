---
name: pair-process-plan-stories
description: "Breaks epics into user stories using vertical slicing and INVEST validation. Composes /pair-capability-write-issue with $type: story. Idempotent: detects existing stories, creates only missing ones."
version: 0.4.1
author: Foomakers
---

# /pair-process-plan-stories — User Story Breakdown

Transform epics into user stories through vertical slicing, INVEST validation, and collaborative definition. Each story delivers end-to-end user value within a single sprint. Composes `/pair-capability-write-issue` for PM tool integration.

## Process Profile

<!-- process-step: id=plan-stories -->

Executable form of the **`plan-stories`** step. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill          | Type       | Required                                                  |
| -------------- | ---------- | --------------------------------------------------------- |
| `/pair-capability-write-issue` | Capability | Yes — creates or updates story issues in the PM tool      |

## Arguments

| Argument | Required | Description                                                                                  |
| -------- | -------- | -------------------------------------------------------------------------------------------- |
| `$epic`  | No       | Epic identifier (e.g., `#42`). If omitted, selects highest-priority Todo epic.               |

## Algorithm

### Step 0: Prerequisite Check

1. **Check**: Prerequisites present?
   - Bootstrap complete: [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)
   - Epics exist in PM tool
   - [User story template](../../../.pair/knowledge/guidelines/collaboration/templates/user-story-template.md) available
2. **Skip**: If all present, proceed to Step 1.
3. **Act**: If any missing → **HALT**:

   > Prerequisites incomplete: [list missing]. Epics must exist before story breakdown.

4. **Verify**: Context loaded, PM tool accessible.

### Step 1: Epic Selection

1. **Check**: Is `$epic` provided?
2. **Skip**: If provided, load the epic from the PM tool. Proceed to Step 2.
3. **Act**: Query PM tool for epics in Todo state. Apply selection:
   - **Priority**: P0 > P1 > P2.
   - **Bootstrap rule**: if Epic 0 exists and is Todo, it must be broken down first.
   - **Dependencies**: prefer epics whose dependencies are complete.
4. **Act**: Present recommendation and ask developer to confirm:

   > Recommend breaking down Epic `#[ID]: [Title]` (Priority: [P0/P1/P2]).
   > Reason: [business value / sprint urgency / dependency chain].
   > Proceed?

5. **Verify**: Epic selected and loaded.

### Step 2: Detect Existing Stories

1. **Check**: Query PM tool for existing story issues linked to the selected epic.
2. **Act**: Build a registry of existing stories:

   ```text
   EXISTING STORIES:
   ├── #ID: [Title] (Status: [Todo/Refined/In Progress/Done])
   └── ...
   ```

3. **Verify**: Registry built. Existing stories will be skipped during creation.

### Step 3: Story Identification

1. **Act**: Analyze epic components for story candidates:
   - **Workflow steps**: distinct user journey phases.
   - **CRUD operations**: create, read, update, delete patterns.
   - **Business rules**: different scenarios and conditions.
   - **User roles**: admin, member, guest variations.
2. **Act**: Apply vertical slicing — every story must deliver end-to-end user value with visible UI manifestation.
3. **Act**: Present story candidates to developer:

   > Story candidates for Epic `#[ID]: [Title]`:
   >
   > 1. [Story name] — [user value] — [UI manifestation]
   > 2. [Story name] — [user value] — [UI manifestation]
   > ...
   >
   > [N] already exist (will be skipped).
   > Approve or adjust?

4. **Verify**: Developer approves the candidate list.

### Step 4: Story Definition & INVEST Validation

For each approved story not already in the registry:

1. **Check**: Does this story already exist in the registry (Step 2)?
2. **Skip**: If exists → skip, report:

   > Story `[Title]` already exists (#ID). Skipping.

3. **Act**: Define story scope using the Initial Breakdown section of [user-story-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/user-story-template.md):
   - Story statement (As a / I want / So that).
   - Rough scope boundaries with expected uncertainty.
   - Initial sizing: XS(1), S(2), M(3), L(5), XL(8).
   - UI value manifestation for sprint demo readiness.
4. **Act**: Validate against INVEST criteria:
   - **I**ndependent: can be planned separately.
   - **N**egotiable: focuses on user value, not implementation.
   - **V**aluable: clear benefit to user persona.
   - **E**stimable: scope clear enough for rough sizing.
   - **S**mall: fits within single sprint.
   - **T**estable: outcome can be verified.
5. **Act**: Compose `/pair-capability-write-issue` with:
   - `$type: story`
   - `$content`: the story definition
   - `$parent`: the epic identifier
6. **Verify**: Story created in PM tool. Record the ID.

### Step 5: Coverage Validation & Completion

1. **Act**: Validate epic coverage:
   - All epic scope areas addressed by stories.
   - No critical gaps in user value delivery.
   - Epic objectives achievable through story completion.
2. **Act**: Report completion:

   > Epic coverage: [X]% of scope addressed.
   > Stories ready for backlog prioritization and future refinement.

3. **Verify**: Coverage validated.

## Output Format

```text
STORIES COMPLETE:
├── Epic:     [#ID: Title]
├── Total:    [N stories]
├── Created:  [X new]
├── Skipped:  [Y existing]
├── Points:   [total estimated points]
├── INVEST:   [all validated]
├── PM Tool:  [adopted tool]
└── Next:     /pair-process-refine-story
```

## HALT Conditions

- **No epics in Todo state** (Step 1) — nothing to break down.
- **Epic not found** (Step 1) — invalid `$epic` identifier.
- **Bootstrap incomplete** (Step 0) — PM tool required.
- **Developer rejects candidates** (Step 3) — must resolve before creation.

## Graceful Degradation

- If `/pair-capability-write-issue` is not installed, warn and provide formatted story content for manual PM tool entry.
- If PM tool is not accessible, produce story documents and ask developer to create manually.
- If epic documentation is sparse, proceed with available context and flag gaps.

## Notes

- This skill **modifies PM tool state** — creates story issues linked to epics.
- Idempotent: re-invocation detects existing stories and skips them.
- Stories at breakdown stage are rough planning units — detailed requirements are added during `/pair-process-refine-story`.
- INVEST validation is mandatory — stories failing INVEST must be reworked before creation.
- After story creation, proceed to `/pair-process-refine-story` for detailed specification.
