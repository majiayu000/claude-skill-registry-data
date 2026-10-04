---
name: fleet-epic-breakdown
description: How to decompose epics into stories and subtasks — dependency chains, contribution requirements, estimation, and the common mistakes that turn a clean epic into a tangled mess
user-invocable: false
---

# Epic Breakdown

## The Problem This Solves

An epic that goes straight to "create 5 stories" produces stories that
overlap, miss critical paths, and have invisible dependencies. Three
sprints later the team discovers a blocker that should have been visible
from day one.

Good epic breakdown is ANALYSIS, not transcription.

## Step 1: Understand the Whole Before Splitting

Before creating a single subtask:

1. **Read the verbatim requirement** — what did the PO actually ask for?
2. **Identify the user outcome** — what changes for the user when this is done?
3. **Map the system boundary** — which systems are touched?
4. **Identify the risk center** — where is the unknown? Where will things break?

The risk center is where you start, not the easy parts.

## Step 2: Identify Natural Seams

Epics split along natural boundaries:

| Seam Type | Example | Signal |
|-----------|---------|--------|
| Data boundary | "User model" vs "Auth flow" | Different tables/APIs |
| System boundary | "Backend API" vs "Frontend form" | Different codebases |
| Role boundary | "Security review" vs "Implementation" | Different expertise |
| Risk boundary | "New tech spike" vs "Known pattern" | Different uncertainty |
| User flow | "Registration" vs "Login" vs "Password reset" | Different user actions |

**Anti-pattern:** Splitting by layer ("do all models first, then all APIs,
then all UI"). This creates stories that can't be demo'd or validated independently.

## Step 3: Build the Dependency Chain

For each story, ask:
- What MUST exist before this can start?
- What does this PRODUCE that others need?
- Can this be worked on in parallel with anything?

Draw the chain:
```
Epic: User Authentication
  ├── Story 1: User model + migration (no deps — foundation)
  │   └── Contribution: architect design_input
  ├── Story 2: Registration API (depends on Story 1)
  │   └── Contributions: architect, QA, devsecops
  ├── Story 3: Login API (depends on Story 1)
  │   └── Contributions: architect, QA, devsecops
  ├── Story 4: Password reset (depends on Story 3)
  │   └── Contributions: QA, devsecops
  └── Story 5: Frontend integration (depends on Stories 2+3)
      └── Contributions: UX, QA
```

Stories 2 and 3 can run in parallel. Story 4 and 5 cannot start until
their dependencies are done. This is what the PM should see BEFORE
creating tasks.

## Step 4: Set Contribution Requirements

For each story, check the synergy matrix:

| Story Type | Always Needs | Sometimes Needs |
|------------|-------------|-----------------|
| New feature | architect, QA | devsecops, UX, writer |
| Bug fix | QA | architect (if architectural) |
| Refactor | architect, QA | devsecops (if auth-related) |
| Infrastructure | devops, devsecops | architect |
| Documentation | writer | UX (if user-facing) |

Create contribution subtasks when creating the story — don't wait.

## Step 5: Estimate

| Points | Meaning | Typical Duration |
|--------|---------|-----------------|
| 1 | Trivial, known pattern | < 1 heartbeat |
| 2 | Small, mostly known | 1-2 heartbeats |
| 3 | Medium, some unknowns | 2-3 heartbeats |
| 5 | Significant, real complexity | 3-5 heartbeats |
| 8 | Large, multiple unknowns | Full sprint |
| 13 | Epic-sized, should be split further | Split this |

**If you estimate 13, you haven't broken it down enough.**

## Common Mistakes

1. **Stories too large** — if a story can't be completed in one sprint,
   split it further
2. **Missing the spike** — if you don't know HOW to do something, the
   first story should be a spike to find out
3. **Hidden dependencies** — "oh we need that service deployed first" —
   map infrastructure dependencies explicitly
4. **No contribution tasks** — creating stories without architect/QA/security
   input means the engineer will make mistakes
5. **Splitting by layer** — "all backend, then all frontend" means nothing
   is demo-able until everything is done

## The Group Call

```
pm_epic_breakdown(task_id)
```

This call reads the epic, checks existing subtasks, and helps you identify
gaps. Use it as a starting point, not a replacement for thinking.
