---
name: complete-spec
description: Interactive conversation to resolve [NEEDS CLARIFICATION] markers using /speckit.clarify command. Claude asks questions about missing features, UX/UI details, behavior, and priorities. Updates specs in .specify/memory/ with answers to create complete, unambiguous documentation. This is Step 5 of 6 in the reverse engineering process.
---

# Complete Specification (with GitHub Spec Kit)

**Step 5 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 30-60 minutes (interactive)
**Prerequisites:** Step 4 completed (`docs/gap-analysis-report.md` exists with clarifications list)
**Output:** Updated specs in `specs/` with all `[NEEDS CLARIFICATION]` markers resolved

---

## When to Use This Skill

Use this skill when:
- You've completed Step 4 (Gap Analysis)
- Have `[NEEDS CLARIFICATION]` markers in specifications
- Ready for interactive clarification session using `/speckit.clarify`
- Want to finalize specifications before implementation

**Trigger Phrases:**
- "Complete the specification"
- "Resolve clarifications"
- "Run speckit clarify"
- "Let's clarify the missing details"

---

## What This Skill Does

Uses `/speckit.clarify` and **interactive conversation** to fill specification gaps:

1. **Use /speckit.clarify** - GitHub Spec Kit's built-in clarification tool
2. **Interactive Q&A** - Ask questions about missing features and details
3. **Update Specifications** - Add answers to specs in `specs/`
4. **Resolve Ambiguities** - Remove all `[NEEDS CLARIFICATION]` markers
5. **Update Implementation Plans** - Refine plans in `specs/`
6. **Finalize for Implementation** - Ready for `/speckit.tasks` and `/speckit.implement`

**Note:** `/speckit.clarify` provides structured clarification workflow. This skill can also supplement with custom Q&A for project-specific needs.

---

## Process Overview

### Step 1: Collect All Clarifications

From `specs/gap-analysis.md` and all feature specs:
- List all `[NEEDS CLARIFICATION]` markers
- Group by feature
- Prioritize by impact (P0 first)

### Step 2: Interactive Q&A Session

**For each clarification, ask the user:**

Example questions:
- "The Analytics Dashboard feature is missing. What charts/metrics should be displayed?"
- "For photo upload, should it be drag-and-drop or click-to-browse?"
- "Should offline sync download full data or just metadata?"
- "What's the maximum number of photos per fish?"
- "For species input, free-text field or autocomplete dropdown?"

**Listen for:**
- Feature requirements
- UX/UI preferences
- Business logic rules
- Constraints and limitations
- Priority adjustments

### Step 3: Update Feature Specs

As user answers questions:
- Add details to feature specs
- Define acceptance criteria
- Specify UI behavior
- Document business rules
- Remove `[NEEDS CLARIFICATION]` markers

### Step 4: Confirm Priorities

Review the prioritized implementation plan:
- Are P0 items truly critical?
- Should any features move up/down in priority?
- What's the target timeline?

### Step 5: Finalize Specifications

Ensure all specs are:
- Complete (no clarification markers)
- Unambiguous (clear requirements)
- Testable (acceptance criteria defined)
- Prioritized (P0/P1/P2/P3)

---

## Example Interactive Session

**Claude:**
> I found 12 items that need clarification. Let me go through them by priority.
>
> **F003 - Analytics Dashboard [P1]**
> This feature is marked as missing. What specific charts and metrics should be displayed?

**User:**
> I want to see:
> - Fish count over time (line chart)
> - Water parameter trends (multi-line chart)
> - Tank health score (gauge)
> - Recent alerts (list)

**Claude:**
> Got it! I'll add those requirements to F003.
>
> Should these be real-time updates or daily aggregates?

**User:**
> Daily aggregates for the charts, but real-time for alerts.

**Claude:**
> Perfect. Next question:
>
> **F002 - Photo Upload UI [P0]**
> For uploading fish photos, would you prefer drag-and-drop or click-to-browse?

**User:**
> Both options would be ideal.

**Claude:**
> Understood. What's the maximum number of photos per fish?

**User:**
> Let's limit it to 10 photos per fish.

[...continues for all clarifications...]

---

## Output Updates

### Updated Feature Specs

**Before:**
```markdown
## Analytics Dashboard [NEEDS CLARIFICATION]

Status: ❌ MISSING

[NEEDS CLARIFICATION] What charts and metrics to display?
```

**After:**
```markdown
## Analytics Dashboard

Status: ❌ MISSING
Priority: P1

### Overview
Dashboard displaying fish count trends, water parameter history, tank health, and recent alerts.

### Acceptance Criteria
- [ ] Fish count over time line chart (daily aggregates)
- [ ] Water parameter trends multi-line chart (pH, temp, ammonia)
- [ ] Tank health score gauge (0-100)
- [ ] Recent alerts list (real-time updates)
- [ ] Date range selector (7d, 30d, 90d, all)

### UI Requirements
- Responsive design (desktop + mobile)
- Charts use Recharts library
- Real-time updates for alerts via WebSocket

### API Requirements
- GET /api/analytics/fish-count?range=30d
- GET /api/analytics/water-params?range=30d
- GET /api/analytics/health-score
- WebSocket /ws/alerts for real-time alerts
```

### Updated Gap Analysis

Remove resolved clarifications from the list.

### Updated Implementation Status

Reflect finalized priorities and details.

---

## Success Criteria

After running this skill, you should have:

- ✅ All `[NEEDS CLARIFICATION]` markers resolved
- ✅ Feature specs updated with complete details
- ✅ Acceptance criteria defined for all features
- ✅ Priorities confirmed (P0/P1/P2/P3)
- ✅ Implementation roadmap finalized
- ✅ Ready to proceed to Step 6 (Implement from Spec)

---

## Next Step

Once specifications are complete and unambiguous, proceed to:

**Step 6: Implement from Spec** - Use the implement skill to systematically build missing features.

---

## Interactive Guidelines

### Asking Good Questions

**DO:**
- Ask specific, focused questions
- Provide context for each question
- Offer examples or common patterns
- Ask one category at a time (don't overwhelm)
- Confirm understanding by summarizing

**DON'T:**
- Ask overly technical questions (keep user-focused)
- Assume answers (always ask)
- Rush through clarifications
- Mix multiple questions together

### Handling Uncertainty

If user is unsure:
- Suggest common industry patterns
- Provide examples from similar features
- Offer to defer to later (mark as P2/P3)
- Document the uncertainty and move on

### Documenting Answers

For each answer:
- Update the relevant feature spec immediately
- Add to acceptance criteria
- Remove clarification marker
- Confirm understanding with user

---

## Technical Notes

- Use the AskUserQuestion tool for structured Q&A
- Group related questions together
- Prioritize P0 clarifications first
- Keep a running list of resolved items
- Update specs incrementally (don't batch)

---

**Remember:** This is Step 5 of 6. After this interactive session, you'll have complete, unambiguous specifications ready for implementation in Step 6.
