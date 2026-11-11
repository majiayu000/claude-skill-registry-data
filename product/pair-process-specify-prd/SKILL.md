---
name: pair-process-specify-prd
description: "Creates or updates a Product Requirements Document through structured template analysis, hypothesis-driven information gathering, and iterative review. Idempotent — detects existing PRD and offers selective section update."
version: 0.4.1
author: Foomakers
---

# /pair-process-specify-prd — PRD Creation

Create a comprehensive Product Requirements Document through collaborative analysis and structured information gathering. Follows a template-first approach: analyze PRD template, gather information via hypothesis-driven questions, create PRD, review and approve.

## Process Profile

<!-- process-step: id=specify-prd -->

Executable form of the **`specify-prd`** step. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Arguments

| Argument   | Required | Description                                                                              |
| ---------- | -------- | ---------------------------------------------------------------------------------------- |
| `$section` | No       | Specific PRD section to update (e.g., `goals`, `features`). If omitted, full PRD process |

## Phase 0: Detect Existing PRD (Idempotency Gate)

### Step 0.1: Check Current State

1. **Check**: Does [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) exist?
2. **Act** (file exists): Read the file. Determine if it is a **template** (contains `[Product/feature name]` or `[Creation date]`) or a **populated** PRD.
   - If **template**: treat as new PRD. Proceed to Phase 1.
   - If **populated** and `$section` provided: jump to Phase 3 (selective update of that section).
   - If **populated** and no `$section`: present current PRD summary and ask:

     > PRD already exists for **[product name]**. Options:
     > 1. **Update specific sections** — tell me which sections need changes
     > 2. **Full review** — walk through the entire PRD for updates
     > 3. **Cancel** — no changes needed

3. **Verify**: Mode is set to `create`, `update-section`, `full-review`, or `cancelled`. If cancelled → stop.

## Phase 1: Template & Reference Analysis

### Step 1.1: Study Reference Materials

1. **Check**: Has the PRD template been analyzed in this session?
2. **Skip**: If yes, proceed to Step 1.2.
3. **Act**: Read and analyze:
   - [PRD template](../../../.pair/knowledge/assets/PRD_template.md) — understand all required sections and structure
   - [PRD example](../../../.pair/knowledge/assets/PRD_example.md) — understand quality standards, specificity level, writing tone
4. **Verify**: Template structure and quality expectations are understood.

### Step 1.2: Create Section Checklist

1. **Act**: Build a checklist of all PRD sections from the template:

   ```text
   PRD CHECKLIST:
   ├── [ ] 1. Overview (name, version, date, owner, summary)
   ├── [ ] 2. Vision & Mission
   ├── [ ] 3. Problem Statement (current state, pain points)
   ├── [ ] 4. Goals & Success Metrics (KPIs with targets)
   ├── [ ] 5. Target Users (personas, journey)
   ├── [ ] 6. Solution Overview (core solution, features P0/P1/P2)
   ├── [ ] 7. User Stories & Acceptance Criteria (epics, stories, ACs)
   ├── [ ] 8. Technical Considerations (architecture, requirements, constraints)
   ├── [ ] 9. Design Requirements (UI/UX, visual)
   ├── [ ] 10. Timeline & Milestones (phases, dependencies)
   ├── [ ] 11. Risks & Mitigations (table)
   ├── [ ] 12. Launch & Go-to-Market (strategy, marketing, support)
   └── [ ] 13. Post-Launch (monitoring, iteration plan)
   ```

2. **Verify**: All template sections are tracked.

## Phase 2: Information Gathering

### Step 2.1: Request Existing Documentation

1. **Act**: Ask the developer for any existing project materials:

   > Before I start asking questions, do you have any existing documentation I should review?
   > Examples: market research, user interviews, technical specs, business plans, competitive analysis, previous PRDs, wireframes, design mockups.

2. **Act**: If documentation provided, analyze each document:
   - Map which checklist sections are covered
   - Mark covered items in checklist
   - Extract relevant information
3. **Verify**: Documentation analysis complete. Remaining gaps identified.

### Step 2.2: Iterative Hypothesis-Driven Questioning

For each uncovered checklist section, gather information using this pattern:

1. **Act**: Ask **one specific question at a time** with a **plausible hypothesis** based on available context:

   > Based on [context/docs], I assume [specific hypothesis]. Is this accurate?

   Example questions:
   - *"Based on the documentation, the primary problem is [pain point hypothesis]. Is this accurate?"*
   - *"The primary user persona would be [role hypothesis] who needs [need hypothesis]. Correct?"*
   - *"The must-have MVP features would include [3-4 feature hypotheses]. Are these the right priorities?"*

2. **Act**: Wait for developer response (confirmation, correction, elaboration).
3. **Act**: Update checklist — mark section as covered when sufficient information gathered.
4. **Act**: Move to next uncovered section.
5. **Verify**: All checklist sections have sufficient information. If not, continue questioning.

**Rules**:

- Ask ONE question at a time — never batch multiple questions
- Always propose a reasonable assumption — never ask open-ended "what is X?"
- Validate understanding by summarizing complex responses
- Do NOT proceed to Phase 3 until all sections have information

## Phase 3: PRD Creation

### Step 3.1: Write PRD

1. **Check**: If mode is `update-section`, read existing PRD and modify only the target section. Skip to Step 3.2.
2. **Act**: Create (or overwrite template) at [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md):
   - Follow [PRD template](../../../.pair/knowledge/assets/PRD_template.md) structure exactly
   - Match quality standard from [PRD example](../../../.pair/knowledge/assets/PRD_example.md)
   - Replace all placeholders with gathered information
   - Use specific numbers, dates, and measurable criteria
   - Structure user stories and acceptance criteria per example format
3. **Verify**: PRD file created with all sections populated. No `[placeholder]` text remains.

### Step 3.2: Self-Review

1. **Act**: Verify against quality standards:
   - [ ] Success metrics are measurable and time-bound with exact targets
   - [ ] Technical requirements are implementable and clearly articulated
   - [ ] User stories include clear acceptance criteria
   - [ ] Risks have corresponding mitigation strategies
   - [ ] All template sections completed
   - [ ] Terminology is consistent throughout
   - [ ] Writing tone matches example standard
2. **Act**: Fix any quality issues found.
3. **Verify**: PRD passes self-review.

## Phase 4: Review & Approval

### Step 4.1: Present for Review

1. **Act**: Present the complete PRD to the developer:

   > I've completed the PRD. Please review each section and provide feedback on:
   > - Accuracy of information
   > - Missing details or requirements
   > - Clarity and specificity
   > - Alignment with your vision
   >
   > Please prioritize feedback as **critical** (must fix) or **enhancement** (nice to have).

2. **Act**: Apply feedback — update PRD file directly.
3. **Act**: Present updated sections for re-review.
4. **Act**: Repeat until developer approves.
5. **Verify**: Developer has explicitly approved the PRD.

## Output Format

```text
PRD COMPLETE:
├── Product:  [product name]
├── File:     [path to PRD file]
├── Mode:     [Created | Updated (sections: X, Y) | Full Review]
├── Sections: [N/N completed]
└── Status:   [Approved | Pending review]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` detects missing or template PRD and invokes `/pair-process-specify-prd`.
- **Output**: Returns path to the PRD file and approval status.
- `/pair-process-bootstrap` proceeds to next phase only after PRD is approved.

When invoked **independently**:

- Interactive: full Phase 0-4 flow. Developer commits changes when satisfied.

## HALT Conditions

- **Template not reviewed** (Phase 1) — must understand structure before gathering information
- **Example not analyzed** (Phase 1) — must understand quality expectations
- **Information incomplete** (Phase 2) — do not create PRD with gaps
- **Developer rejects PRD** (Phase 4) — iterate until approved, never force completion

## Graceful Degradation

- If [PRD template](../../../.pair/knowledge/assets/PRD_template.md) not found, use the 13-section structure defined in Phase 1 Step 1.2 checklist as a minimal template.
- If [PRD example](../../../.pair/knowledge/assets/PRD_example.md) not found, proceed without quality reference but warn: "No PRD example found — quality benchmarking unavailable."
- If adoption directory doesn't exist, create `adoption/product/` and warn: "Created adoption directory — this appears to be a new project."

## Notes

- Target file is always [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — the single source of truth for product requirements.
- This skill modifies one file: the PRD. Changes should be committed by the calling skill or developer.
- Hypothesis-driven questioning reduces developer effort: confirm/correct is faster than open-ended answers.
- One question at a time prevents cognitive overload and ensures thorough coverage.
