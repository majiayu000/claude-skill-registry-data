---
name: leadership-retro
description: Facilitate a team retrospective in Start/Stop/Continue format on how the team works together, digging into root causes and recurring patterns and ending with owned actions. Use when a leader wants to reflect with their team on a period, project or rough patch to improve how they work. Not for a sprint ceremony; see /project-management-retrospective.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# Retrospective

Facilitate a retrospective for "$ARGUMENTS". Structure a team reflection on what went well, what didn't, and what to improve.

See also `/project-management-retrospective` for the sprint ceremony — format, dot-voting and committed action items tied to last sprint.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"leadership-retro","workflow":"leadership","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

## Prerequisites

None — utility skill, run anytime.

## Process

1. **Set the context:**
   - What period or project is this retro for?
   - Who participated? What was the scope?

2. **Structure the retro (Start/Stop/Continue format):**
   - **Start:** What should we begin doing?
   - **Stop:** What should we stop doing?
   - **Continue:** What's working well and should continue?

3. **Dig deeper:**
   - For each item: why? What's the root cause?
   - What patterns repeat from previous retros?
   - Are there systemic issues to address?

4. **Define action items:**
   - Convert insights into 2-3 specific, assignable actions
   - Each action has an owner and a deadline
   - Focus on highest-impact changes

5. **Write the artifact** to `.singularskills/leadership/<project>/retro.md` with sections:
   - **Context** — period, team, scope
   - **Start** — new practices to adopt
   - **Stop** — practices to drop
   - **Continue** — practices to maintain
   - **Action Items** — owner, action, deadline

## Output

The retro summary written to `.singularskills/leadership/<project>/retro.md`. Present the key insights and action items to the user.
