---
description: Turn a rough idea into a structured project brief
argument-hint: "[project idea]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Bash(date:*)
---

Turn a rough idea into a structured project brief with requirements, user stories, acceptance criteria, risks, and timeline.

## Steps

### Step 1: Capture the idea

Take whatever the user described and identify:
- **The problem:** What pain does this solve?
- **The solution:** What are we building?
- **The user:** Who benefits?
- **The outcome:** What does success look like?

If any of these are unclear from the input, make reasonable assumptions and flag them.

### Step 2: Define scope

**In scope:**
- List specific capabilities / features this project will deliver
- Be concrete — "user can filter by date" not "filtering functionality"

**Out of scope:**
- Explicitly list what this project will NOT do
- This is as important as in-scope — prevents scope creep

**Assumptions:**
- What are we assuming to be true?
- Technical assumptions (platform, stack, integrations)
- Business assumptions (budget, timeline, team)

### Step 3: User stories

Write 5-10 user stories in standard format:

```
As a [user type], I want to [action] so that [benefit].

Acceptance criteria:
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
```

Prioritise using MoSCoW:
- **Must have:** Non-negotiable for launch
- **Should have:** Important but not critical
- **Could have:** Nice to have if time allows
- **Won't have:** Explicitly excluded from this version

### Step 4: Technical considerations

If relevant:
- **Stack / platform:** Recommended technology choices
- **Integrations:** Third-party services or APIs needed
- **Data:** What data is needed, where it comes from, how it's stored
- **Constraints:** Performance requirements, security needs, compliance

### Step 5: Risks and mitigations

Identify the top 3-5 risks:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk] | High/Med/Low | High/Med/Low | [what to do about it] |

### Step 6: Timeline estimate

Break into phases with rough estimates:
- **Phase 1 — Foundation:** [scope] — [estimate]
- **Phase 2 — Core features:** [scope] — [estimate]
- **Phase 3 — Polish & launch:** [scope] — [estimate]

Note: These are rough estimates, not commitments.

### Step 7: Write the brief

Save to `briefs/[project-name]-brief.md`:

```markdown
# Project Brief — [Name]

**Date:** [date]
**Status:** Draft

---

## Problem
[What pain are we solving?]

## Solution
[What are we building?]

## Target User
[Who benefits?]

## Success Criteria
[How do we know this worked?]

## Scope

### In Scope
- [specific feature]

### Out of Scope
- [explicitly excluded]

### Assumptions
- [assumption]

## User Stories

### Must Have
[user stories with acceptance criteria]

### Should Have
[user stories]

### Could Have
[user stories]

## Technical Considerations
[stack, integrations, data, constraints]

## Risks
[risk table]

## Timeline
[phased estimate]

## Open Questions
- [anything still unresolved]

---
Ready for review.
```

Output a summary and flag any open questions that need answers before work starts.
