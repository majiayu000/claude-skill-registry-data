---
name: pair-process-plan-epics
description: "Breaks initiatives into epics through structured analysis and collaborative validation. Composes /pair-capability-write-issue with $type: epic. Idempotent: detects existing epics, creates only missing ones. Includes Epic 0 assessment for new projects."
version: 0.4.1
author: Foomakers
---

# /pair-process-plan-epics — Epic Breakdown

Transform strategic initiatives into comprehensive epic breakdowns. Each epic delivers end-to-end user value in 2-4 sprints. Composes `/pair-capability-write-issue` for PM tool integration.

## Process Profile

<!-- process-step: id=plan-epics -->

Executable form of the **`plan-epics`** step, and a composer of `define-subdomains`. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill          | Type       | Required                                                  |
| -------------- | ---------- | --------------------------------------------------------- |
| `/pair-capability-write-issue` | Capability | Yes — creates or updates epic issues in the PM tool       |

## Arguments

| Argument      | Required | Description                                                                                           |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `$initiative` | No       | Initiative identifier (e.g., `#10`). If omitted, selects highest-priority Todo initiative.            |

## Algorithm

### Step 0: Prerequisite Check

1. **Check**: Prerequisites present?
   - Bootstrap complete: [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md), PRD, architecture, tech-stack
   - Initiatives exist in PM tool
2. **Skip**: If all present, proceed to Step 1.
3. **Act**: If bootstrap incomplete → **HALT**.
4. **Verify**: Context loaded, PM tool accessible.

### Step 1: Initiative Selection

1. **Check**: Is `$initiative` provided?
2. **Skip**: If provided, load the initiative from the PM tool. Proceed to Step 2.
3. **Act**: Query PM tool for initiatives in Todo state. Apply selection:
   - **Priority**: P0 > P1 > P2.
   - **Dependencies**: prefer initiatives whose dependencies are complete.
4. **Act**: Present recommendation and ask developer to confirm:

   > Recommend breaking down Initiative `#[ID]: [Title]` (Priority: [P0/P1/P2]).
   > Reason: [business value / readiness / dependency chain].
   > Proceed?

5. **Verify**: Initiative selected and loaded.

### Step 2: Detect Existing Epics

1. **Check**: Query PM tool for existing epic issues linked to the selected initiative.
2. **Act**: Build a registry of existing epics:

   ```text
   EXISTING EPICS:
   ├── #ID: [Title] (Status: [Todo/In Progress/Done])
   └── ...
   ```

3. **Verify**: Registry built. Existing epics will be skipped during creation.

### Step 3: Epic Analysis & Proposal

1. **Act**: Analyze initiative components:
   - Business objectives and success metrics.
   - User value propositions and journey stages.
   - Technical requirements from architecture and tech-stack.
   - Architecture alignment for service boundaries.
2. **Act**: Determine epic structure:
   - **Epic 0 assessment**: for new projects, assess if bootstrap epic is needed.
   - **Value-driven grouping**: natural feature groupings following user workflows.
   - **Sequential dependencies**: foundation-first, user journey progression.
   - **Duration sizing**: 2-4 sprints per epic with clear completion criteria.
3. **Act**: Present epic breakdown proposal to developer:

   > Epic breakdown for Initiative `#[ID]: [Title]`:
   >
   > [Epic 0: Bootstrap (if needed)]
   > Epic 1: [Name] (2-3 sprints) — [user value]
   > Epic 2: [Name] (3-4 sprints) — [user value]
   > ...
   >
   > [N] already exist (will be skipped).
   > Approve or adjust?

4. **Verify**: Developer approves the breakdown.

### Step 4: Epic Creation

Process epics sequentially (Epic 0 first if needed). For each epic:

1. **Check**: Does this epic already exist in the registry (Step 2)?
2. **Skip**: If exists → skip, report:

   > Epic `[Title]` already exists (#ID). Skipping.

3. **Act**: Draft the epic following [epic-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/epic-template.md):
   - Fill template sections: Epic Statement, Business Value, Solution Overview, Epic Breakdown, Technical Considerations.
   - Present to developer for validation.
4. **Act**: Compose `/pair-capability-write-issue` with:
   - `$type: epic`
   - `$content`: the filled epic template
   - `$parent`: the initiative identifier
5. **Verify**: Epic created in PM tool. Record the ID.

### Step 5: Completion

1. **Act**: Validate complete breakdown:
   - All epics documented. Epic sequence verified.
   - Initiative objectives fully covered by epic scope.
   - Tool hierarchy established (Initiative → Epics).
2. **Verify**: Breakdown complete.

## Output Format

```text
EPICS COMPLETE:
├── Initiative: [#ID: Title]
├── Total:      [N epics]
├── Created:    [X new]
├── Skipped:    [Y existing]
├── Sprints:    [estimated total sprints]
├── PM Tool:    [adopted tool]
└── Next:       /pair-process-plan-stories
```

## HALT Conditions

- **Bootstrap incomplete** (Step 0) — PM tool and tech context required.
- **No Todo initiatives** (Step 1) — nothing to break down.
- **Initiative not found** (Step 1) — invalid `$initiative` identifier.
- **Developer rejects breakdown** (Step 3) — must resolve before creation.

## Graceful Degradation

- If `/pair-capability-write-issue` is not installed, warn and provide formatted epic content for manual PM tool entry.
- If PM tool is not accessible, produce epic documents and ask developer to create manually.

## Notes

- This skill **modifies PM tool state** — creates epic issues linked to initiatives.
- Idempotent: re-invocation detects existing epics and skips them.
- Epic 0 rule: for new projects, always assess if a bootstrap/foundation epic is needed before functional epics.
- Each epic should deliver end-to-end user value in 2-4 sprints.
- After epic creation, proceed to `/pair-process-plan-stories` for user story breakdown.
