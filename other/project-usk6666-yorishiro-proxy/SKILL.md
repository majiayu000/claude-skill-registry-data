---
description: "Development planning tool for tracking project progress, organizing Issues, and syncing the roadmap"
user-invokable: true
---

# /project

A skill that handles the planning and tracking sides of the "plan → implement → track" development cycle.
Provides milestone progress overview, Issue creation from the roadmap, and post-implementation document sync.

## Fixed Parameters

- **Team**: Usk6666
- **Project**: yorishiro-proxy
- **Roadmap doc ID**: d413edd7-d296-433a-ab94-11d4dd57d883

## Subcommands

- `/project status` — Overview of milestone progress
- `/project plan <milestone>` — Gap analysis between roadmap and Linear Issues, with Issue creation. If the roadmap has no Issue table for the target milestone (greenfield), run the milestone-planner agent to derive Issues from the milestone description + spec — see "Greenfield Mode" below.
- `/project sync` — Update roadmap documents after implementation is complete

---

## `/project status`

The entry point for checking milestone progress and deciding what to work on next.

### Steps

1. Fetch all milestone progress with `mcp__linear-server__list_milestones(project=yorishiro-proxy)`
2. Fetch the following **in parallel**:
   - `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=started)`
   - `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=backlog)`
   - `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=unstarted)`
3. Group Issues by `projectMilestone` field
4. Report the following:

### Output Format

```markdown
## Project Progress

### Milestone Progress
| Milestone | Progress | Remaining Issues | Status |
|-----------|----------|-----------------|--------|
| M1: Foundation | 100% | — | Complete |
| M2: MCP Interface v2 | 79% | 3 issues | ← ACTIVE |
| M3: Active Testing | 0% | N issues | Not started |
| M4: Multi-Protocol | 0% | N issues | Not started |
| M5: Production Ready | 0% | N issues | Not started |

### Active: M2 — MCP Interface v2
| ID | Title | Status | Priority |
|----|-------|--------|----------|
| USK-79 | ... | Backlog | High |
| USK-80 | ... | Todo | Normal |
| ...

### Blockers
- M3 depends on M2 completion (currently 79%)

### Recommended Actions
- `/orchestrate milestone M2` to implement remaining 3 Issues
- Or `/project plan M3` to prepare M3 Issues in advance
```

---

## `/project plan <milestone>`

The most important subcommand for setting up prerequisites for orchestrate.
Closes the gap between the roadmap (desired state) and Linear (actual Issues).

### Steps

1. Fetch roadmap document with `mcp__linear-server__get_document(id=d413edd7-d296-433a-ab94-11d4dd57d883)`
2. Parse the Issue table in the target milestone section
   - Extract Issue ID, title, description, priority, and dependencies
3. Fetch existing Issues for that milestone with `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy)`
   - Filter by milestone (fetch all then filter if milestone parameter filtering is unavailable)
4. Gap analysis:
   - **In roadmap but not in Linear** → Propose Issue creation
   - **In Linear but milestone unassigned** → Propose assignment fix
   - **Issues with insufficient description** → Propose description improvement
5. Present analysis results to user and get approval
6. After approval, execute `create_issue` / `update_issue`
7. Also set dependency relationships (`blockedBy`/`blocks`) between created Issues

### Output Format

```markdown
## <Milestone Name> — Issue Plan

### To Create
| # | Title | Priority | Basis |
|---|-------|----------|-------|
| 1 | Intercept rule engine | High | Roadmap M3 section |
| 2 | Intruder engine | High | Roadmap M3 section |
| ...

### Existing (No changes)
| ID | Title | Milestone | Status |
|----|-------|-----------|--------|
| USK-64 | Auto-transform rules | M3 | Backlog |

### Proposed Modifications
| ID | Change |
|----|--------|
| USK-XX | Milestone unassigned → assign to M3 |
| USK-YY | Improve description (reflect roadmap spec) |

### Dependencies
| Issue | blockedBy |
|-------|-----------|
| #2 Intruder engine | #1 Intercept rule engine |

Create N Issues and update M? Proceed?
```

### Config Checklist

At the final stage of Issue splitting, confirm the following (see "Config Checklist for New Feature Milestones" in CLAUDE.md):

- If a new feature requires adding a field to the config struct, explicitly include a config support Issue
- Same applies if config validation or init function changes are needed
- Include a config → runtime path integration test Issue if needed

### Notes

- Always get user approval before creating Issues
- Do not create Issues not in the roadmap
- When overwriting an existing Issue's description, show the diff explicitly
- Infer dependency relationships from Issue content and set blockedBy/blocks

### Greenfield Mode (no roadmap Issue table)

When the roadmap has only a milestone description (no per-Issue table) — typical for newly-added milestones — run the milestone-planner agent to derive a structured Issue breakdown from the milestone description, completed-milestone public surface, and applicable specs.

#### Steps

1. Confirm with the user that greenfield-mode planning is wanted (otherwise the roadmap is the source of truth and Step 2-7 above apply as-is).
2. Read `.claude/agents/milestone-planner.md` and `.claude/agents/design-reviewer.md` (the planner injects design-reviewer as a sub-step).
3. Replace the planner's placeholders:

| Placeholder | Value |
|---|---|
| `{{MILESTONE_NAME}}` | Target milestone name (e.g., "M5") |
| `{{MILESTONE_DESCRIPTION}}` | Full description from `mcp__linear-server__get_milestone` |
| `{{SPEC_REFERENCES}}` | Paths to spec/design docs that apply (e.g., `docs/rfc/envelope.md`, protocol RFCs) |
| `{{COMPLETED_CONTEXT}}` | One-paragraph summary of public surface from completed milestones the new work will integrate with |
| `{{PRODUCT_IDENTITY}}` | Read from `.claude/skills/review-gate/SKILL.md` Phase 1-4 "Product context" block — single source of truth |
| `{{PRINCIPLES}}` | The MITM Implementation Principles from `CLAUDE.md` (the 6-item list). Quote verbatim. |
| `{{DESIGN_REVIEW_AGENT}}` | Full Prompt Body section from `.claude/agents/design-reviewer.md` (the planner runs design review at milestone scope as Step 2 of its process) |
| `{{CHECKLISTS}}` | Whichever of "Config Checklist for New Feature Milestones" / "e2e Test Checklist for New Protocol Addition" (both from CLAUDE.md) apply. Quote verbatim — the planner enforces them as mandatory checks. |

4. Launch:

```
Agent(
  description="Plan milestone <name>",
  subagent_type="general-purpose",
  prompt=<composed prompt>
)
```

5. Present the planner's output — Issue breakdown, dependency graph, resolved decisions, unresolved decisions for user input, recommended order — and get user approval.
6. After approval, create each Issue via `mcp__linear-server__save_issue` with priority, scope, dependencies (`blockedBy`), and acceptance criteria. Then update the roadmap document to embed the new Issue table so subsequent `/project plan` runs hit the regular gap-analysis path instead of greenfield mode.

---

## `/project sync`

Update roadmap documents to match the actual state after implementation is complete.

### Steps

1. Fetch roadmap document with `mcp__linear-server__get_document(id=d413edd7-d296-433a-ab94-11d4dd57d883)`
2. Fetch latest progress with `mcp__linear-server__list_milestones(project=yorishiro-proxy)`
3. Fetch the following **in parallel**:
   - `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=completed)`
   - `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=started)`
4. Update each milestone section in the roadmap:
   - Update status markers in Issue tables (✅ Complete, 🔄 In Progress, ⏳ Not Started)
   - Update milestone progress summary
   - Record completion date if available
5. Show the diff to the user and get approval
6. After approval, apply with `mcp__linear-server__update_document`

### Output Format

```markdown
## Roadmap Sync

### Changes
- M2: Progress 79% → 100% (Complete)
- USK-75: ⏳ → ✅
- USK-78: ⏳ → ✅
- USK-79: ⏳ → ✅

### Updated Milestone Summary
| Milestone | Progress | Status |
|-----------|----------|--------|
| M1: Foundation | 100% | Complete |
| M2: MCP Interface v2 | 100% | Complete |
| M3: Active Testing | 0% | Next target |

Update roadmap? Proceed?
```

### Notes

- sync fetches completed Issues, but only for the purpose of document updates
- Always get user approval before updating the document
- Do not change the roadmap structure (milestone order, descriptions) — only update statuses
