---
name: frontend-development
aliases: [frontend-stage, epic-orchestrator]
description: Orchestrates frontend development with MidsReborn UI analysis, React component planning, visual verification, and quality gates
---

# Frontend Development (Verified Stages)

Orchestrates frontend epic development with MidsReborn UI analysis and visual verification gates.

**Invocation**: `/frontend-development epic-X.Y`

**Example**: `/frontend-development epic-1.1`

---

## Scope

This skill orchestrates frontend development by integrating with the superpowers plugin:

- ✅ Context Collection (previous epics, architecture docs, screenshots)
- ✅ MidsReborn UI Analysis Hook (Task tool with Explore agent)
- ✅ Planning Integration (invokes `/superpowers:write-plan` via SlashCommand)
- ✅ Two-Gate Approval Flow (human reviews before execution)
- ✅ Execution Integration (invokes `/superpowers:execute-plan` via SlashCommand)
- ✅ Visual Verification Workflow (compare with MidsReborn screenshots)
- ✅ Checkpoint Generation (documents progress and artifacts)
- ✅ Epic Progress Tracking (updates progress.json)

**Key Integration**: This skill does NOT directly create files. Instead, it:
1. Analyzes MidsReborn UI (via Task tool)
2. Invokes `/superpowers:write-plan` to create plans
3. Gets human approval at Gate 1
4. Invokes `/superpowers:execute-plan` to create components
5. Facilitates visual verification at Gate 2

---

## Parameters

- `epic-number` (required): Epic identifier (e.g., `epic-1.1`, `epic-2.2`)

---

## Process

### Phase 1: Context Collection

**Purpose:** Load all relevant documents with deterministic file list.

**Steps:**

1. **Parse epic number from invocation**

   - Extract from command: `/frontend-development epic-1.2` → `1.2`
   - Validate format: `epic-X.Y` where X.Y is digit pattern

2. **Read context map**

   - File: `docs/frontend/context-map.json` (if exists, else use defaults)
   - Look up key: `epic-X.Y`
   - Extract: `required_inputs`, `midsreborn_references`

3. **Check prerequisites**

   **If not first epic (X.Y > 1.1):**

   - Check: `docs/frontend/plans/PLAN-SUMMARY-epic-[X.Y-1].md` exists
   - Calculate previous epic number (e.g., 2.2 → 2.1)
   - If missing: ERROR and stop

     ```
     ERROR: Previous epic not complete.

     Cannot find: docs/frontend/plans/PLAN-SUMMARY-epic-[X.Y-1].md

     Complete Epic [X.Y-1] first before running Epic X.Y.
     ```

   **Check MidsReborn codebase:**

   - Verify: `/Users/w/code/mids-hero-web/external/dev/MidsReborn` exists
   - If missing: ERROR

     ```
     ERROR: MidsReborn codebase not found.

     Expected: /Users/w/code/mids-hero-web/external/dev/MidsReborn

     This is required for UI analysis and reference implementation.
     ```

   **Check MidsReborn screenshots:**

   - Location: `/Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots`
   - Screenshots are optional but highly recommended for visual verification
   - If directory exists, load screenshot list for reference in analysis

4. **Build explicit file list**

   Load common files (always required):

   ```
   - docs/frontend/architecture.md
   - docs/frontend/epic-breakdown.md
   - docs/frontend/tech-stack.md (if exists)
   - docs/midsreborn/00-navigation-map.md
   - docs/midsreborn/01-architecture-overview.md
   ```

   Load MidsReborn screenshots (if available):

   ```
   - Check: /Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots
   - List available screenshots for visual reference
   - Include screenshot paths in context for sub-agents
   ```

   Load epic-specific inputs:

   - Previous epic plan summary (if not Epic 1.1)
   - Epic-specific requirements from epic-breakdown.md
   - Relevant MidsReborn calculation specs (from `docs/midsreborn/calculations/`)

5. **Load all files**

   - Use Read tool for each file in the explicit list
   - Store in context for next phases
   - If any REQUIRED file missing → ERROR with specific filename
   - Track which files were loaded for verification

6. **Display context loaded summary**

   ```
   Phase 1: Context Collection
   ✅ Read: docs/frontend/architecture.md
   ✅ Read: docs/frontend/epic-breakdown.md
   ✅ Read: docs/frontend/plans/PLAN-SUMMARY-epic-[X.Y-1].md
   ✅ Read: [N] MidsReborn reference docs
   ✅ Verified: MidsReborn codebase exists
   ✅ Found: [N] MidsReborn screenshots in shared/user/midsreborn-screenshots

   Total files loaded: [N]
   Context loaded. Proceeding to Phase 2...
   ```

---

### Phase 2: MidsReborn UI Analysis Hook

**Purpose:** Analyze MidsReborn UI code to understand feature implementation.

**Implementation:** Dispatch sub-agent via Task tool.

**Steps:**

1. **Build sub-agent prompt**

   ```markdown
   You are a MidsReborn UI analysis agent for Epic X.Y of the Mids Hero Web frontend.

   ## CONTEXT

   [Include all files loaded in Phase 1]

   Epic to implement: Epic X.Y - [Feature Name]
   MidsReborn codebase: /Users/w/code/mids-hero-web/external/dev/MidsReborn
   MidsReborn screenshots: /Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots (if available)
   Frontend architecture: docs/frontend/architecture.md
   Epic breakdown: docs/frontend/epic-breakdown.md

   ## YOUR TASK

   ### 1. Locate MidsReborn UI Components

   Find the C# Windows Forms UI code for this feature:

   - Use Glob to find relevant Form files: `external/dev/MidsReborn/**/*.cs`
   - Search for UI components related to: [Feature Name from Epic X.Y]
   - Example patterns to search:
     - "ArchetypeSelector" for character creation
     - "PowerPicker" for power selection
     - "EnhancementSlotEditor" for slotting
     - "BuildTotalsPanel" for stats display

   ### 2. Extract UI Component Structure

   For each relevant Form/UserControl:

   - **Layout**: How are controls arranged? (panels, grids, lists)
   - **Data Displayed**: What information is shown to the user?
   - **User Interactions**: What can users click/select/edit?
   - **Data Flow**: How does UI get data? (direct DB calls, services, etc.)
   - **Validation**: What validation rules exist?
   - **Events**: What triggers recalculation/updates?

   ### 3. Extract Feature Requirements

   From the UI code, determine:

   - **MUST-HAVE features**: Core functionality that must be replicated
   - **SHOULD-HAVE features**: Important but could be deferred
   - **COULD-SKIP features**: Nice-to-have, not in v1 scope

   Cross-reference with user's skip list:

   - Skip: alternate IO slotting, enhancement boosters, attuned IOs, level scaling, incarnate powers, rotation recommendations

   ### 4. Identify State Management Needs

   Determine what state this feature manages:

   - **Server State**: What data comes from backend API?
   - **Client State**: What is managed locally in the UI?
   - **Shared State**: What state is shared across components?
   - **Derived State**: What is computed from other state?

   ### 5. Map to Web Equivalent

   For each MidsReborn UI pattern, propose web equivalent:

   - **DataGridView** → TanStack Table or custom table
   - **ListBox/ComboBox** → Select component or listbox
   - **TabControl** → Tabs component
   - **TreeView** → Tree component or nested lists
   - **ToolTip** → Tooltip component (shadcn/ui)
   - **Modal Dialogs** → Dialog/Modal component

   ### 6. Identify Available Screenshots

   Check for existing screenshots in: `/Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots`

   For each relevant screenshot found:

   - Note filename and what it shows
   - Reference in analysis report
   - Use as visual reference for component design

   If screenshots for this epic's features are missing:

   - List specific screenshots that would be helpful
   - Request user to capture them from MidsReborn

   ## OUTPUT FORMAT

   Create: docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md

   ## Structure:

   # MidsReborn UI Analysis: Epic X.Y - [Feature Name]

   **Created**: [date]
   **Epic**: [epic number and name]
   **MidsReborn Forms Analyzed**: [list]

   ## Executive Summary

   [2-3 sentences: what feature does, how MidsReborn implements it, key findings]

   ## MidsReborn UI Components

   ### Component 1: [Form/UserControl Name]

   - **File**: `external/dev/MidsReborn/[path]`
   - **Purpose**: [What this component does]
   - **Layout**: [How controls are arranged]
   - **Data Displayed**: [What information is shown]
   - **User Interactions**: [What users can do]

   ### Component 2: [Name]

   ...

   ## Feature Requirements

   ### MUST-HAVE Features

   1. **[Feature Name]**

      - **Description**: [What it does]
      - **MidsReborn Implementation**: [How MidsReborn does it]
      - **Web Equivalent**: [How we'll implement it]

   2. **[Feature Name]**
      ...

   ### SHOULD-HAVE Features

   [Features to include if time permits]

   ### COULD-SKIP Features

   [Features that can be deferred to v2]

   ## State Management Analysis

   ### Server State (TanStack Query)

   - **Endpoint**: `GET /api/[resource]`
   - **Data**: [What data is fetched]
   - **Caching Strategy**: [How to cache]

   ### Client State (Zustand)

   - **Store**: `[store-name]Store`
   - **State Shape**: [TypeScript interface]
   - **Actions**: [list of state mutations]

   ### Derived State

   - **[Computed Value]**: Derived from [source state]

   ## Web Component Mapping

   | MidsReborn Pattern | Web Equivalent | Library/Component |
   | ------------------ | -------------- | ----------------- |
   | DataGridView       | Table          | TanStack Table    |
   | ListBox            | Listbox        | shadcn/ui Listbox |
   | ...                | ...            | ...               |

   ## API Integration Points

   ### Backend Endpoints Needed

   1. **GET /api/[resource]** - [Purpose]
   2. **POST /api/[resource]** - [Purpose]

   (Cross-reference with backend API implementation)

   ## Screenshot Analysis

   ### Available Screenshots

   Location: `/Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots`

   [List screenshots found that are relevant to this epic]

   1. **[Screenshot filename]**
      - Shows: [What it displays]
      - Relevant to: [Which component/feature]

   ### Additional Screenshots Recommended

   [If key screenshots are missing, list them here]

   1. **[Feature] - [State]**
      - Filename suggestion: `midsreborn-[feature]-[state].png`
      - Should show: [What to capture]
      - Needed for: [Why it's important]

   ## Implementation Notes

   ### Key Behaviors to Replicate

   - [Important behavior 1]
   - [Important behavior 2]

   ### UX Improvements for Web

   - [Opportunity to improve on MidsReborn UX]

   ## Warnings & Edge Cases

   - [Any edge cases found in MidsReborn code]
   - [Potential issues to watch out for]

   ---
   ```

2. **Dispatch sub-agent**

   ```
   Tool: Task
   Parameters:
     subagent_type: Explore
     description: MidsReborn UI analysis for epic X.Y
     prompt: [prompt from step 1]
     model: sonnet (thorough analysis needed)
   ```

3. **Wait for sub-agent completion**

   Sub-agent will create: `docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md`

4. **Validate output**

   - Check file exists: `docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md`
   - If missing: Error and offer retry

5. **Display summary**

   ```
   Phase 2: MidsReborn UI Analysis Hook
   Launching analysis sub-agent...

   Analyzing MidsReborn Forms for Epic X.Y...
   - Found: [N] relevant Form files
   - Extracted: [M] UI components
   - Identified: [K] features

   ✅ Created: docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md
      - [N] MidsReborn components analyzed
      - [M] features identified
      - [K] screenshots recommended

   Proceeding to Phase 3...
   ```

---

### Phase 3: Planning Integration (write-plan)

**Purpose:** Create implementation plan with MidsReborn UI analysis via superpowers plugin.

**Implementation:** Invoke `/superpowers:write-plan` via SlashCommand tool.

**Steps:**

1. **Prepare context message for write-plan**

   Before invoking the slash command, output a clear message to the user explaining what will happen:

   ```
   Phase 3: Planning
   Invoking /superpowers:write-plan to create implementation plan...

   The planning agent will receive:
   - All context from Phase 1 (architecture docs, previous epic)
   - MidsReborn UI analysis from Phase 2
   - Enhanced instructions for frontend component planning

   This will create:
   - Detailed plan: docs/frontend/plans/[YYYY-MM-DD]-epic-X.Y-[feature].md
   - Summary: docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md
   ```

2. **Invoke the write-plan slash command**

   Use the SlashCommand tool:

   ```
   Tool: SlashCommand
   Parameters:
     command: "/superpowers:write-plan"
   ```

   **Important**: The write-plan agent has access to the ENTIRE conversation context up to this point, including:
   - All files loaded in Phase 1
   - MidsReborn UI analysis from Phase 2
   - The enhanced instructions below (Section 3)

   You do NOT need to pass parameters or repeat context - the agent sees everything in the conversation.

3. **Enhanced instructions for write-plan (in this message)**

   The planning agent should create an implementation plan for Epic X.Y of the Mids Hero Web frontend.

   ## CONTEXT PROVIDED

   All context from Phase 1 (architecture docs, previous epic, MidsReborn references)
   MidsReborn UI Analysis from Phase 2: docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md

   ## MANDATORY REQUIREMENTS

   ### 1. Component-Driven Development

   Break down implementation into React components:

   - Component hierarchy (parent/child relationships)
   - Props interface (TypeScript)
   - State management (local vs global)
   - API integration points

   ### 2. Test-Driven Development

   For each component, include:

   - Component test structure (React Testing Library)
   - User interaction tests (click, type, select)
   - State update tests
   - API integration tests (mocked)

   ### 3. MidsReborn Reference

   All UX decisions MUST reference the MidsReborn UI analysis.

   Format: "Implements [Feature] as shown in MidsReborn [Form Name] (ref: MIDSREBORN-UI-ANALYSIS-epic-X.Y.md, Component 2)"

   ### 4. State Management Integration

   Specify how components integrate with:

   - **TanStack Query**: Server state, caching, mutations
   - **Zustand**: Client state, actions, selectors
   - **React Hook Form**: Form state (if applicable)

   ### 5. API Integration

   For each backend API call:

   - Endpoint: `GET /api/[resource]`
   - Request/Response TypeScript types
   - Error handling strategy
   - Loading states

   ### 6. Visual Design

   Reference shadcn/ui components:

   - Which shadcn/ui components to use
   - Custom components to build
   - Tailwind classes for layout

   ### 7. Previous Epic Context

   This plan builds on previous epics. Reference and maintain consistency with:

   - Previous epic: docs/frontend/plans/PLAN-SUMMARY-epic-[X.Y-1].md
   - Architecture decisions: docs/frontend/architecture.md

   ### 8. Epic Objectives Alignment

   Your plan must accomplish objectives defined in:
   docs/frontend/epic-breakdown.md (Epic X.Y section)

   ## OUTPUT STRUCTURE

   Create TWO files:

   ### File 1: docs/frontend/plans/[YYYY-MM-DD]-epic-X.Y-[feature].md

   Detailed implementation plan:

   - Background & Context (links to MidsReborn analysis, previous artifacts)
   - Objectives (from epic breakdown)
   - Component Specifications (detailed, with TypeScript interfaces)
   - State Management Plan (TanStack Query + Zustand)
   - API Integration Plan (endpoints, types, error handling)
   - Implementation Tasks (step-by-step, with test examples)
   - Acceptance Criteria (traceable to epic breakdown)
   - Visual Verification Checklist (how to compare with MidsReborn)

   ### File 2: docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md

   Concise summary (500-1000 words):

   - What this epic accomplishes
   - Key components created
   - State management approach
   - API endpoints used
   - Next epic preview

   This becomes the master reference for Epic X.Y.

4. **After planning completes**

   The write-plan agent will return when it has created both files.

5. **Validate outputs and display summary**

   After write-plan returns, validate the outputs:

   - Check both files exist:
     - `docs/frontend/plans/[YYYY-MM-DD]-epic-X.Y-[feature].md`
     - `docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md`
   - Verify PLAN-SUMMARY is concise (500-1000 words)
   - Verify detailed plan references MidsReborn UI analysis

6. **Display summary**

   ```
   Phase 3: Planning
   Invoking superpowers:write-plan...

   Creating implementation plan with MidsReborn UI context...

   ✅ Created: docs/frontend/plans/[YYYY-MM-DD]-epic-X.Y-[feature].md
   ✅ Created: docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md

   Plan includes:
   - [N] React components to build
   - [M] API integration points
   - [K] test suites
   - [L] shadcn/ui components to install

   Proceeding to Gate 1 (Human Approval)...
   ```

---

### GATE 1: Human Approval (Post-Planning)

**Purpose:** Human reviews MidsReborn analysis and plan before execution.

**Steps:**

1. **Display gate header**

   ```
   ═══════════════════════════════════════════════════════════
   EPIC X.Y PLANNING COMPLETE
   ═══════════════════════════════════════════════════════════
   ```

2. **Display MidsReborn analysis summary**

   ```
   MidsReborn UI Analysis:
   ✅ docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md
      - [N] MidsReborn Forms analyzed
      - [M] features identified
      - [K] components to build
   ```

3. **Display plan creation summary**

   ```
   Plan Created:
   ✅ docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md
   ✅ docs/frontend/plans/[YYYY-MM-DD]-epic-X.Y-[feature].md
   ```

4. **Display screenshot status**

   ```
   📸 MidsReborn Screenshots:

   Found in /Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots:
   - [screenshot1.png] - [Description]
   - [screenshot2.png] - [Description]

   [If additional screenshots would be helpful:]
   Additional screenshots recommended (optional):
   1. midsreborn-[feature]-[state].png - [Description]
   2. midsreborn-[feature]-[state].png - [Description]

   Please capture from MidsReborn and save to shared/user/midsreborn-screenshots/
   ```

5. **Display gate instructions**

   ```
   ═══════════════════════════════════════════════════════════
   NEXT: Execute plan to build React components

   Please review:
   1. MidsReborn UI analysis (are all features captured?)
   2. Plan summary (does it align with epic objectives?)
   3. Component specifications (do they make sense?)

   Type 'proceed to execute' to continue
   Type 'abort' to stop
   ═══════════════════════════════════════════════════════════
   ```

6. **Wait for human response**

   - Listen for: "proceed to execute", "proceed", "execute", "continue", "yes"
   - If user says "abort", "stop", "cancel": Exit skill gracefully
   - If ambiguous: Ask for clarification

7. **On approval, display transition**

   ```
   ✅ Approval received. Proceeding to Phase 4...
   ```

---

### Phase 4: Execution (execute-plan)

**Purpose:** Create all React components and tests per verified plan.

**Implementation:** Invoke `/superpowers:execute-plan` via SlashCommand tool.

**Steps:**

1. **Prepare context message for execute-plan**

   Before invoking the slash command, output a clear message to the user explaining what will happen:

   ```
   Phase 4: Execution
   Invoking /superpowers:execute-plan to implement components...

   The execution agent will receive:
   - Implementation plan from Phase 3
   - All context from Phase 1
   - MidsReborn UI analysis
   - Enhanced instructions for React component development

   This will create React components, hooks, stores, and tests as specified in the plan.
   ```

2. **Invoke the execute-plan slash command**

   Use the SlashCommand tool:

   ```
   Tool: SlashCommand
   Parameters:
     command: "/superpowers:execute-plan"
   ```

   **Important**: The execute-plan agent has access to the ENTIRE conversation context up to this point, including:
   - Plans created in Phase 3
   - All files loaded in Phase 1
   - MidsReborn UI analysis from Phase 2
   - The enhanced instructions below (Section 3)

   You do NOT need to pass parameters or repeat context - the agent sees everything in the conversation.

3. **Enhanced instructions for execute-plan (in this message)**

   The execution agent should implement the plan for Epic X.Y of the Mids Hero Web frontend.

   ## CONTEXT PROVIDED

   Plan: docs/frontend/plans/[YYYY-MM-DD]-epic-X.Y-[feature].md
   Plan Summary: docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md
   All Phase 1 context (architecture docs, MidsReborn references)
   MidsReborn UI analysis: docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md

   ## EXECUTION REQUIREMENTS

   ### 1. Follow Plan Exactly

   Implement all components as specified in the plan.

   ### 2. Create Files in Correct Locations

   **Frontend structure:**
   ```

   frontend/src/
   ├── components/ # React components
   │ ├── [Feature]/
   │ │ ├── [Component].tsx
   │ │ ├── [Component].test.tsx
   │ │ └── index.ts
   ├── hooks/ # Custom React hooks
   │ ├── use[Feature].ts
   │ └── use[Feature].test.ts
   ├── services/ # API client services
   │ ├── [feature]Api.ts
   │ └── [feature]Api.test.ts
   ├── stores/ # Zustand stores
   │ ├── [feature]Store.ts
   │ └── [feature]Store.test.ts
   ├── types/ # TypeScript types
   │ └── [feature].types.ts
   └── lib/ # Utilities

   ````

   ### 3. TypeScript Strict Mode

   All code MUST be TypeScript with strict mode enabled:

   - No `any` types (use `unknown` if needed)
   - Explicit return types on functions
   - Proper interface definitions

   ### 4. Component Testing Pattern

   Every component MUST have tests following this pattern:

   ```typescript
   import { render, screen } from '@testing-library/react';
   import userEvent from '@testing-library/user-event';
   import { ComponentName } from './ComponentName';

   describe('ComponentName', () => {
     it('renders correctly', () => {
       render(<ComponentName {...requiredProps} />);
       expect(screen.getByRole('...')).toBeInTheDocument();
     });

     it('handles user interaction', async () => {
       const user = userEvent.setup();
       render(<ComponentName {...requiredProps} />);
       await user.click(screen.getByRole('button'));
       expect(...).toBeCalled();
     });
   });
   ````

   ### 5. State Management Integration

   **TanStack Query usage:**

   ```typescript
   import { useQuery, useMutation } from "@tanstack/react-query";

   export function useFeature() {
     return useQuery({
       queryKey: ["feature"],
       queryFn: fetchFeature,
     });
   }
   ```

   **Zustand usage:**

   ```typescript
   import { create } from "zustand";

   interface FeatureState {
     data: FeatureData | null;
     actions: {
       setData: (data: FeatureData) => void;
     };
   }

   export const useFeatureStore = create<FeatureState>((set) => ({
     data: null,
     actions: {
       setData: (data) => set({ data }),
     },
   }));
   ```

   ### 6. shadcn/ui Component Usage

   Use shadcn/ui components as specified in plan:

   ```typescript
   import { Button } from "@/components/ui/button";
   import { Dialog } from "@/components/ui/dialog";
   ```

   If component not yet installed, note in checkpoint for manual installation.

   ### 7. Batch Execution with Review Checkpoints

   Follow execute-plan skill's batch execution pattern.
   Present work for review between logical groups.

   ### 8. API Integration

   Use fetch or axios with proper error handling:

   ```typescript
   async function fetchResource(): Promise<Resource> {
     const response = await fetch("/api/resource");
     if (!response.ok) {
       throw new Error(`Failed to fetch: ${response.statusText}`);
     }
     return response.json();
   }
   ```

4. **After execution completes**

   The execute-plan agent will return when it has created all components, hooks, stores, and tests.

5. **Collect execution results and display summary**

   Track which files were created during execution for Phase 5 checkpoint.

   ```
   Phase 4: Execution Complete

   execute-plan has finished creating components...

   Executing plan tasks...

   ✅ Created: frontend/src/components/[Feature]/[Component].tsx
   ✅ Created: frontend/src/components/[Feature]/[Component].test.tsx
   ✅ Created: frontend/src/hooks/use[Feature].ts
   ✅ Created: frontend/src/stores/[feature]Store.ts
   ✅ Created: frontend/src/services/[feature]Api.ts

   Files created: [N] total
   - [X] Components
   - [Y] Tests
   - [Z] Hooks
   - [W] Stores

   Proceeding to Phase 5 (Visual Verification & Checkpoint)...
   ```

---

### Phase 5: Visual Verification & Checkpoint

**Purpose:** Generate checkpoint document, verify visually against MidsReborn, update progress.

**Steps:**

1. **Collect execution results**

   From Phase 4, we have:

   - List of all files created (components, tests, hooks, stores)
   - Any execution errors (if any)
   - Key decisions made (from plan)

2. **Visual verification instructions**

   ```
   📸 VISUAL VERIFICATION REQUIRED

   Please perform the following:

   1. Run the development server: `cd frontend && npm start`
   2. Navigate to: [URL/route for this feature]
   3. Interact with the feature to test functionality
   4. Capture screenshot: Save as docs/frontend/screenshots/implementation-[feature]-epic-X.Y.png
   5. Compare with MidsReborn screenshot(s) from shared/user/midsreborn-screenshots/

   Reference screenshots for comparison:
   - shared/user/midsreborn-screenshots/[relevant-screenshot].png

   Verification Checklist:
   - [ ] Feature displays correctly
   - [ ] User interactions work as expected
   - [ ] Data loads from backend API
   - [ ] UI matches MidsReborn functional layout (not pixel-perfect)
   - [ ] No console errors

   Type 'verified' when visual check is complete
   Type 'issues found: [description]' if problems discovered
   ```

3. **Wait for visual verification**

   - Listen for: "verified", "looks good", "working"
   - If "issues found": Offer to fix before checkpoint
   - If "not working": Offer to debug and re-run Phase 4

4. **Generate checkpoint document**

   Create: `docs/frontend/checkpoints/CHECKPOINT-epic-X.Y-[name].md`

   Template:

   ```markdown
   # CHECKPOINT: Epic X.Y - [Epic Name]

   **Date**: [YYYY-MM-DD]
   **Status**: Awaiting Approval
   **Plan**: docs/frontend/plans/PLAN-SUMMARY-epic-X.Y.md

   ---

   ## Executive Summary

   [3-5 sentences: what was accomplished, key components built, recommendation]

   ---

   ## Work Completed

   - ✅ MidsReborn UI analysis completed ([N] Forms analyzed)
   - ✅ Implementation plan created and approved
   - ✅ [Major component 1] built with tests
   - ✅ [Major component 2] built with tests
   - ✅ [State management] implemented
   - ✅ [API integration] completed

   ---

   ## Components Created

   ### React Components

   - 📄 `frontend/src/components/[Feature]/[Component1].tsx` - [Description]
   - 📄 `frontend/src/components/[Feature]/[Component2].tsx` - [Description]

   ### Hooks

   - 📄 `frontend/src/hooks/use[Feature].ts` - [Description]

   ### Stores

   - 📄 `frontend/src/stores/[feature]Store.ts` - [Description]

   ### Services

   - 📄 `frontend/src/services/[feature]Api.ts` - [Description]

   ### Tests

   - ✅ All components have test coverage
   - ✅ [N] test suites created
   - ✅ All tests passing

   ---

   ## Visual Verification

   ### MidsReborn Reference

   ![MidsReborn Reference](../../shared/user/midsreborn-screenshots/[feature]-reference.png)

   _Caption: MidsReborn implementation of [Feature]_
   _Source: /Users/w/code/mids-hero-web/shared/user/midsreborn-screenshots_

   ### Our Implementation

   ![Our Implementation](../screenshots/implementation-[feature]-epic-X.Y.png)

   _Caption: Mids Hero Web implementation of [Feature] (Epic X.Y)_

   ### UX Parity Checklist

   - [x] **Layout**: Functional parity achieved (modern web aesthetic)
   - [x] **Data Display**: All data points from MidsReborn are shown
   - [x] **User Interactions**: All core interactions work correctly
   - [x] **Validation**: Input validation matches MidsReborn behavior
   - [x] **Error States**: Proper error handling implemented

   ### UX Improvements Over MidsReborn

   - [Improvement 1]: [Description]
   - [Improvement 2]: [Description]

   ---

   ## Key Decisions Made

   ### Decision 1: [Decision Name]

   **Rationale**: [2-3 sentences explaining why]
   **Impact**: [What this enables or constrains]
   **Implementation**: [How it was implemented]

   ---

   ## State Management

   ### TanStack Query Integration

   - **Queries**: [List of queries created]
   - **Mutations**: [List of mutations created]
   - **Caching Strategy**: [How data is cached]

   ### Zustand Store

   - **Store Name**: `[feature]Store`
   - **State Shape**: [Brief description]
   - **Actions**: [List of actions]

   ---

   ## API Integration

   ### Endpoints Used

   1. **GET /api/[resource]** - [Purpose]

      - Response type: `[TypeName]`
      - Error handling: [Strategy]

   2. **POST /api/[resource]** - [Purpose]
      - Request type: `[TypeName]`
      - Response type: `[TypeName]`

   ---

   ## Test Coverage

   ### Component Tests

   - [Component1]: [N] tests, [M]% coverage
   - [Component2]: [N] tests, [M]% coverage

   ### Integration Tests

   - [Test suite 1]: [N] tests
   - [Test suite 2]: [N] tests

   ### Test Results
   ```

   PASS src/components/[Feature]/[Component].test.tsx
   PASS src/hooks/use[Feature].test.ts
   PASS src/stores/[feature]Store.test.ts

   Test Suites: [N] passed, [N] total
   Tests: [M] passed, [M] total

   ```

   ---

   ## Risks & Concerns Identified

   [If any risks found during implementation]

   ⚠️ **[Risk 1: Risk Name]**

   - **Description**: [What could go wrong]
   - **Impact**: High/Medium/Low
   - **Mitigation**: [Proposed approach]

   ---

   ## Dependencies for Next Epic

   The next epic ([X.Y+1 - Epic Name]) requires:

   - ✅ [PLAN-SUMMARY-epic-X.Y.md - Complete]
   - ✅ [Components from this epic - Complete]
   - ⏳ [Item waiting on external factor]

   ---

   ## Next Epic Preview

   **Epic [X.Y+1]**: [Epic Name]

   - **Will build**: [Key components]
   - **Will accomplish**: [1-2 sentences]
   - **Prerequisites**: [This checkpoint approval + any other items]

   ---

   ## Required Human Action

   Please review this checkpoint and:

   - [ ] Review all components created (links above)
   - [ ] Visually verify implementation matches MidsReborn UX
   - [ ] Review test coverage
   - [ ] Test feature functionality locally
   - [ ] **Provide approval to proceed**

   ### How to Respond

   - **"Approved - proceed to Epic X.Y+1"** - Mark epic complete, ready for next epic
   - **"Approved with changes: [details]"** - Make changes, regenerate checkpoint
   - **"Request revision: [what needs to change]"** - Fix issues, re-run

   ---

   **Generated by**: frontend-development orchestrator
   **Visual Verification Status**: ✅ Verified

   ```

5. **Update epic progress tracking**

   Update: `docs/frontend/progress.json` (or similar)

   ```json
   {
     "current_epic": "X.Y",
     "completed_epics": ["1.1", "1.2", "..."],
     "epic_X.Y": {
       "status": "complete",
       "completed_date": "YYYY-MM-DD",
       "components_created": N,
       "tests_created": M,
       "visual_verification": "passed"
     }
   }
   ```

6. **Display checkpoint summary**

   ```
   Phase 5: Visual Verification & Checkpoint

   Generating checkpoint...

   Execution summary:
   - [N] components created
   - [M] tests created (all passing)
   - [K] API endpoints integrated

   Visual verification:
   ✅ Feature tested locally
   ✅ Screenshots captured
   ✅ UX parity confirmed

   ✅ Created: docs/frontend/checkpoints/CHECKPOINT-epic-X.Y-[name].md
   ✅ Updated: docs/frontend/progress.json

   Proceeding to Gate 2 (Final Approval)...
   ```

---

### GATE 2: Human Approval (Post-Checkpoint)

**Purpose:** Human reviews checkpoint and approves epic completion.

**Steps:**

1. **Display gate header**

   ```
   ═══════════════════════════════════════════════════════════
   EPIC X.Y EXECUTION COMPLETE
   ═══════════════════════════════════════════════════════════
   ```

2. **Display checkpoint summary**

   ```
   Checkpoint Generated:
   📋 docs/frontend/checkpoints/CHECKPOINT-epic-X.Y-[name].md

   Components Created: [N] total
   ✅ [X] React components
   ✅ [Y] Custom hooks
   ✅ [Z] Zustand stores
   ✅ [W] API services
   ✅ All with tests (100% passing)
   ```

3. **Display visual verification status**

   ```
   Visual Verification:
   ✅ Feature tested locally
   ✅ Screenshots captured and compared
   ✅ UX parity with MidsReborn confirmed
   ✅ No console errors
   ```

4. **Display gate instructions**

   ```
   ═══════════════════════════════════════════════════════════
   NEXT: Review checkpoint and approve to continue

   Please review:
   1. Checkpoint document (see all components and tests)
   2. Visual verification (side-by-side screenshots)
   3. Test coverage (all tests passing?)
   4. Feature functionality (does it work correctly?)

   Type 'approved - proceed to Epic X.Y+1' to complete
   Type 'approved with changes: [details]' to revise
   Type 'request revision: [what needs to change]' to fix issues
   ═══════════════════════════════════════════════════════════
   ```

5. **Wait for human response**

   - Listen for: "approved", "approved - proceed to Epic X.Y+1"
   - If "approved with changes": Note changes, offer to revise
   - If "request revision": Note issues, offer to re-run phases

6. **Final epic completion**

   a. Update progress tracking final timestamp

   b. Display completion message:

   ```
   ═══════════════════════════════════════════════════════════
   ✅ EPIC X.Y COMPLETE
   ═══════════════════════════════════════════════════════════

   Summary:
   - MidsReborn Analysis: [N] Forms analyzed
   - Planning: Complete
   - Execution: [M] components + [K] tests created
   - Visual Verification: ✅ Passed
   - Checkpoint: Approved

   Next Epic: X.Y+1 - [Epic Name]

   Ready to run: /frontend-development epic-X.Y+1

   ═══════════════════════════════════════════════════════════
   ```

---

## Error Handling

### Prerequisite Errors

**MidsReborn codebase missing:**

```
ERROR: MidsReborn codebase not found.

Expected: /Users/w/code/mids-hero-web/external/dev/MidsReborn

This is required for UI analysis.
```

**Previous epic missing:**

```
ERROR: Previous epic not complete.

Cannot find: docs/frontend/plans/PLAN-SUMMARY-epic-[X.Y-1].md

Complete Epic [X.Y-1] first.
```

### Analysis Hook Errors

**Sub-agent timeout:**

```
ERROR: MidsReborn UI analysis sub-agent timed out.

Options:
1. Type 'retry' to run analysis again
2. Type 'abort' to stop
```

**Analysis output file missing:**

```
ERROR: Analysis sub-agent completed but did not create output file.

Expected: docs/frontend/analysis/MIDSREBORN-UI-ANALYSIS-epic-X.Y.md

Options:
1. Type 'retry' to run analysis again
2. Type 'abort' to stop
```

### Visual Verification Errors

**Component doesn't render:**

```
ERROR: Component failed to render during visual verification.

Check console for errors and fix before proceeding.

Options:
1. Type 'fix and retry' to debug and re-run Phase 4
2. Type 'abort' to stop
```

**Tests failing:**

```
ERROR: Tests are failing.

[Test output]

All tests must pass before proceeding to checkpoint.

Options:
1. Type 'fix and retry' to fix tests and re-run
2. Type 'abort' to stop
```

---

## Notes

- Modeled after `verified-stage-development` skill
- Frontend-specific adaptations for React/Next.js
- Visual verification is mandatory (not optional)
- Every component must have tests (TDD enforced)
- MidsReborn UI analysis informs all design decisions

---
