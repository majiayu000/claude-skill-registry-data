---
name: create-epic
description: Turn an idea into a structured epic draft using templates/epic-template.md
argument-hint: "[epic idea - can be a short prompt or a path to a raw idea note]"
---

# Create Epic

You help turn a raw product idea into a well-structured epic draft. The output follows `templates/epic-template.md` and lands in `epics/` with `stage: Explore`.

## Input

The user provides via `$ARGUMENTS`:
- A short prompt (e.g., "unified onboarding dashboard for CSMs"), OR
- A path to a raw idea note (e.g., `samples/sample-epic-idea.md`)

## Workflow

### 1. Gather context

**Read the raw idea.** If `$ARGUMENTS` is a path, read that file. Otherwise use the prompt directly.

**Read supporting context in parallel**:
- `templates/epic-template.md` - the target structure
- `docs/epic-lifecycle.md` - the stage framework
- `research/personas/` - personas that might match the target user
- `Dashboard/people-profiles.md` - any stakeholders mentioned
- `Loose Notes/Work/` and `Meetings/` - related prior discussions (search by keywords from the idea)
- `Initiatives/` - does this fit under an existing initiative?

### 2. Identify gaps in the idea

Before drafting, identify what's missing or unclear. Ask the user 3-5 focused questions in ONE `AskUserQuestion` round if any of these are unclear from the raw input:

- **Target user**: which persona does this serve? (Offer personas from `research/personas/` as options.)
- **Primary metric**: what measurable outcome should improve?
- **Scope boundary**: what is explicitly NOT in this epic?
- **Initiative fit**: does this belong under an existing initiative (show list from `Initiatives/`) or does it stand alone?
- **Competitor check**: has competitive research been done? (Offer `/competitive-research` if not.)

Skip questions where the raw idea already has a clear answer. Maximum one round.

### 3. Draft the epic

Use `templates/epic-template.md` as the structure. Fill what you can from the raw idea + answers:

**Required sections (always fill)**:
- **Value Proposition Statement** - one crisp statement of the outcome.
- **User Problem** - 1-2 paragraphs from the customer's perspective. Frame from the "why", not the product's failure.
- **User Stories** - 3-6 stories at the "what" level (Explore phase). Add the "how" later.

**Phase-specific (fill lightly in Explore, flag for Scope)**:
- **Breakdown** - list sub-activities under Explore (customer interviews, research, opportunity-solution tree).
- **Risk Assessment** - initial class only, full in Scope.

**Skip for now**:
- Release Notes (drafted in Scope or later).
- Implementation Notes (Scope phase).
- Design Planning, Documentation Planning (Scope phase).
- Validation Criteria (Validate phase).

**Fill placeholders honestly.** If you don't know something, write `[To determine during Scope]` or `[Needs user research]`. Don't fabricate.

### 4. File location and naming

- **Folder**: `epics/`. Create if it doesn't exist.
- **Filename**: `YYYY-MM-DD - [Epic Title slug].md`. Example: `2026-04-20 - Unified onboarding dashboard.md`.
- **Frontmatter**: set `stage: Explore`, `status: exploring`, `created: YYYY-MM-DD`.

### 5. Link the epic

- **Daily journal**: add a link in today's journal under `## Notes`. Format: `- [[YYYY-MM-DD - Epic Title]] - new epic in Explore stage`.
- **Initiative**: if the epic fits under an existing initiative (from step 2), add a link in the initiative file under `## Epics under this initiative`.
- **Nothing external**: do NOT push to any external tracker. The epic lives in the vault until you explicitly ship it elsewhere.

### 6. Propose follow-up tasks

Based on what's missing in the draft, propose 2-5 tasks that would move the epic out of Explore. Examples:

- Schedule 5 customer interviews with target persona
- Run `/competitive-research` on [topic]
- Run `/opportunity-solution-tree` for the primary metric
- Review the draft with [stakeholder]
- Draft a 3-bullet research brief for the user research team

Show the proposed task list and wait for user confirmation. After confirmation, append to `Dashboard/tasks.md` under "This week" with format:

```
- [ ] Task - source: [[YYYY-MM-DD - Epic Title]] - due: YYYY-MM-DD - priority: P3
```

### 7. Output summary

```
✅ Epic drafted: [[YYYY-MM-DD - Epic Title]]
✅ Linked in today's journal
[if initiative match] ✅ Linked under [[Initiative]]

Stage: Explore
Status: exploring

📋 Proposed follow-up tasks (to move to Scope):
1. [Task]
2. [Task]

Confirm: Add tasks to Dashboard/tasks.md? (Y/N)

💡 Next steps in the lifecycle: see docs/epic-lifecycle.md
```

## Notes

- **Honesty over completeness.** It's better to mark a section as `[Needs user research]` than to invent answers.
- **Epics start thin and grow.** The Explore-stage draft should be under 1 page. Sections get filled as the epic progresses.
- **One initiative per epic.** If the idea fits under multiple initiatives, flag this as a scope problem rather than dual-linking.
- **User stories from the customer's perspective**, not the product's. "As a support engineer, I can..." not "The product shall...".
