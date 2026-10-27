---
name: defend-a-figure
description: >
  Cross-check a targeting figure against outside data and write its defence. Use
  before a number reaches a funder or a published document.
disable-model-invocation: false
---

# Defend a Figure

**The method lives in the GiveWell project, not here.** It is the shared skill
`defend-a-figure` of the canopy workspace project `connect/givewell`, so every agent and
person defends a figure the same way. Load it and follow it:

```
project_skill "connect/givewell" "defend-a-figure"
```

(`mcp__plugin_canopy_projects__project_skill`, from the canopy plugin.) Its rule is **lead with
the weakest check**: `targeting_methodology` for the exact selection, its honesty fields and four
cross-checks, an outside source, the method spread, the criterion spread
(`targeting_compare_criteria`), the traps in `targeting_research`, then the three paragraphs and a
Sources table. Change the method there, never by copying it back into this file.

## In an ACE run

- **Products:** `<phase>/defend-a-figure_summary.md` (the three paragraphs), a **Sources** table
  with a live URL per input from the methodology's own source table, and a named conservative
  figure where the methods disagree. `build-targeting-model` takes the paragraphs and the table as
  its document body.
- **Auto:** run the checks, write the defence, notify the admin group with the headline figure and
  any check reading *worth watching* or worse.
- **Review:** present the cross-check verdicts, the method spread and the draft paragraphs for
  approval before anything is published.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-08-29 | Initial version — weakest-check-first rule, external validation step, method spread, three-paragraph pattern | ACE team |
| 2026-09-01 | `off_method_units` became `inherited_units` | ACE team |
| 2026-09-07 | Added the criterion spread (`targeting_compare_criteria`) as step 6 | ACE team |
| 2026-09-07 | Corrected the ADM2 caveat: the ceiling is geoBoundaries coverage (18/55 countries), not the indicators | ACE team |
| 2026-10-25 | Method moved to the GiveWell project's shared `defend-a-figure` skill (connect/givewell); this file keeps ACE's products and modes | Eva |
