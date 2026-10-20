---
name: prd
description: Create a formal PRD from Lark notes or user description
---

# PRD Creator

Creates a formal Product Requirements Document from user input (pasted notes, verbal description, or a Lark doc URL read via the Lark CLI — read-only).

**Before drafting, read `references/conventions.md`** for the required frontmatter, required sections, naming rules, and the split between main PRD and service PRDs.

## Commands

### `/prd create <slug>`
Create a new PRD for a feature.

**Steps:**

0. **Activate phase.** Flip `features[active_feature].phase_status` to `"inprogress"` in `.workflow-state.json`.

1. **Enter plan mode (MANDATORY).** Call your harness's plan mode before reading any file or forming conclusions:
   - Claude Code: `EnterPlanMode`
   - Cursor: plan mode
   - OpenCode: plan mode
   - Amp: no plan mode — announce an explicit "research phase" and stay read-only until Step 9.

2. Verify workflow state is in `prd_creation` phase. If `idle`, route the user back to `/workflow start <slug>` so the brainstorming phase runs first.

3. Read `features[active_feature].brainstorming.summary` and `.brainstorming.questions` — these are the primary inputs to the PRD. Also read `features[active_feature].initial_request`.

4. Ask user for additional input if needed (use your ask tool — Claude Code: `AskUserQuestion`; Cursor: ask tool; OpenCode: question tool; Amp: ask as plain text and wait):
   - "Anything to add beyond the brainstorming summary? (e.g., Lark notes, doc URL, extra constraints)"
   - If Lark CLI is connected: "Or provide a Lark doc URL"

5. If a Lark URL provided and the Lark CLI is connected, fetch the doc through the CLI (read-only).

6. **Estimate PRD size. If > ~8000 tokens, propose split (MANDATORY).** Rough token count ≈ char_count / 3.5. If the source material is large enough that the drafted PRD would exceed ~8000 tokens, use your ask tool to propose splitting into priority-ordered sub-PRDs:
   - **P0** — must-have, first release
   - **P1** — important, follows P0
   - **P2** — nice-to-have, last

   Each sub-PRD becomes its own feature (own branch, own PRs). They share a parent feature slug: `<slug>-p0`, `<slug>-p1`, `<slug>-p2`. Record `features[<parent>].sub_features` on the parent entry and `features[<sub>].parent_feature` on each sub. User confirms split boundaries (which sections go in which sub-PRD) before creation. Each sub-PRD goes through the full workflow independently.

7. **Research current system state (MANDATORY — BEFORE DRAFTING).** Devs do this naturally, non-devs don't. Skipping produces PRDs that ignore existing behavior. Note: brainstorming already captured `service_state_snapshots` — start there, then deepen as needed.
   - Read relevant service code (`api/app/`, `web/src/`, `ai-service/app/`, `data-service/app/`)
   - Read existing PRDs in `docs/prd/` — is there a related or overlapping feature?
   - Check recent commits on base branches (`develop` / `development`) in affected areas
   - Summarize findings to the user: "Here's what already exists that this PRD must reconcile with: [list]"

9. **Challenge assumptions (MANDATORY).** Identify at least 3 aspects that are ambiguous, underspecified, or conflict with existing system behavior. Ask about each via your ask tool. Prefer multiple small questions.

10. **Relentless clarifying questions (MANDATORY).** Surface EVERY remaining ambiguity. Do NOT draft until ALL are answered. Also ask the baseline:
   - Which services does this touch?
   - Who are the primary users?
   - Technical constraints?
   - "Done" criteria?

11. Wait for user answers.

12. Exit plan mode. Read template from `.agentic-workflows/templates/prd/main-prd.template.md`.

13. Generate the PRD. Include a `## Brainstorming Outcome` section pulling in the brainstorming summary verbatim plus a bullet list of decided questions/answers. Also include "Existing System Reconciliation" and "Assumptions and Clarifications" subsections.

14. Present the draft to user for review.

15. On approval, write to `docs/prd/<slug>.md`.

16. Update `.workflow-state.json` with `prd_path` (and `parent_feature` / `sub_features` if split). Flip `phase_status` to `"completed"`. Do NOT auto-advance — tell the user to run `/workflow next` to advance to PRD splitting.

### `/prd edit`
Edit the current feature's PRD.

**Steps:**
1. Read current PRD from path in `.workflow-state.json`
2. Ask user what to change (via your ask tool)
3. Present proposed changes
4. On approval, write changes
