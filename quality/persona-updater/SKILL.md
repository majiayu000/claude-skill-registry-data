---
name: persona-updater
description: |
  Update user personas from new feedback, pilot data, or research. Use this skill when:
  - New pilot data or feedback reveals changed user behaviors or pain points
  - Annual persona review is due (1-2x per year)
  - New user segments are discovered that need persona documentation
  - Existing personas need validation against recent data
---

# Persona Updater

Systematically update user persona files when new data (pilot observations, feedback, research) reveals changes in user behaviors, pain points, goals, or context. Generates diffs and preserves existing persona structure.

## When to Use

- After pilot rounds with new user observations (1-2x per year)
- After significant feedback collection rounds
- When expanding to new user segments or geographies
- During annual persona review cycles

## Workflow

1. **Read existing personas** — Load all persona files from your persona directory
2. **Read new data sources** — Pilot debrief reports, feedback, research
3. **Compare** — Identify what's new, changed, or no longer relevant
4. **Generate diff** — Structured change list per persona
5. **Propose updates** — Show the diff to the user for approval
6. **Apply updates** — Edit persona files preserving existing structure

## Persona Dimensions to Track

| Dimension | What to Look For |
|-----------|-----------------|
| **Demographics** | Age range, role, geography, segment |
| **Goals** | What they're trying to achieve |
| **Pain Points** | Current frustrations and blockers |
| **Behaviors** | How they use the product, daily routines, device usage |
| **Context** | Environment, connectivity, device type |
| **Motivations** | What drives engagement |
| **Barriers** | What prevents usage |
| **Mental Models** | How they think about the domain |

## Output Format

```markdown
# Persona Update Report

**Date:** {DD-MM-YYYY}
**Data Sources:** {list sources reviewed}
**Personas Reviewed:** {count}
**Changes Found:** {count}

---

## Persona: {Persona Name} ({file path})

### New Findings

| # | Dimension | Finding | Source | Confidence |
|---|-----------|---------|--------|-----------|
| 1 | Pain Points | {new pain point discovered} | {source} | High/Med/Low |

### Changed Findings

| # | Dimension | Current Text | Proposed Update | Source | Rationale |
|---|-----------|-------------|-----------------|--------|-----------|
| 1 | Goals | "{current}" | "{updated}" | {source} | {why} |

### Removed / No Longer Relevant

| # | Dimension | Current Text | Reason for Removal | Source |
|---|-----------|-------------|-------------------|--------|
| 1 | Pain Points | "{old}" | Resolved by {feature} | {evidence} |

### No Change (Validated)

| # | Dimension | Current Text | Validation Source |
|---|-----------|-------------|------------------|
| 1 | Goals | "{goal}" | Confirmed in pilot |

---

## Summary

| Persona | New | Changed | Removed | Validated | Action |
|---------|-----|---------|---------|-----------|--------|
| {name} | 2 | 1 | 0 | 5 | Update |
```

## Update Rules

1. **Always generate the diff first** — Never edit persona files without showing proposed changes
2. **Preserve existing structure** — Match the heading hierarchy and writing style
3. **Mark confidence levels** — Single observation is "Low"; data from 50 users is "High"
4. **Don't remove without evidence** — Only mark as "no longer relevant" with explicit evidence
5. **Add source citations** — Every change must cite where the new data came from
6. **Version the update** — Add a note: `Last updated: {date} — Source: {data source}`
7. **Flag new segments** — If data reveals uncovered user segments, flag as new persona candidates

## Anti-Patterns

- Don't update personas without new data — that's just editing, not updating
- Don't merge multiple personas without evidence they overlap
- Don't remove pain points just because a fix was shipped — verify the fix worked

## Quality Checklist

- [ ] Every change has a data source citation
- [ ] Confidence levels marked on all findings
- [ ] Diff shown to user before applying changes
- [ ] Existing persona structure preserved
- [ ] New segments flagged if discovered
