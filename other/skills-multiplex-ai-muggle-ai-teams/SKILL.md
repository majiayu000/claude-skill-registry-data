---
name: workflow-aware-brainstorming
description: Wrapper for superpowers:brainstorming that recognizes parent workflow context. Use this INSTEAD of superpowers:brainstorming when invoked from /muggle-ai-teams Step 1C.
---

# Workflow-Aware Brainstorming

This skill wraps `superpowers:brainstorming` with parent workflow awareness.

## When Invoked from /muggle-ai-teams

If this skill is triggered as part of `/workflow` Step 1C (Design Proposal), the following rules apply:

### Before Starting

Check that Step 1A and 1B outputs exist. If not, STOP and tell the orchestrator:
> "Cannot start brainstorming — Step 1A/1B outputs are incomplete. The following are missing: [list]."

Required 1A outputs:
- Codebase exploration results (from `feature-dev:code-explorer`)
- Industry research findings (from `WebSearch`)
- Library documentation (from `Context7` MCP)

Required 1B outputs:
- Clarified requirements
- Impact analysis (files, services, flows affected)
- Dependency mapping
- Risk identification

### During Brainstorming

Follow `superpowers:brainstorming` skill exactly as documented. All its rules, checklist items, and processes apply.

### At "Transition to Implementation" Step

**DO NOT invoke `superpowers:writing-plans` directly.**

Instead, announce:

> "This concludes the brainstorming phase (Workflow Step 1C: Design Proposal). The design spec has been written and committed.
>
> **Next steps in the parent workflow:**
> - Step 1D: Panel Review — dispatch panelists to scrutinize the design
> - Step 1E: User Approval Gate — present revised design for user sign-off
> - Step 1F: Implementation Plan — write the plan AFTER panel review and approval
>
> Control returns to the /muggle-ai-teams orchestrator."

Then STOP. Do not proceed further. The orchestrator handles Steps 1D, 1E, and 1F.

## When Invoked Standalone (not from /muggle-ai-teams)

Behave exactly like `superpowers:brainstorming` — follow all its steps including the "transition to implementation" step which invokes `writing-plans`.
