---
name: leadership-okrs
description: Set or review OKRs for a team or individual — 2-3 objectives with measurable key results, baselines and targets, aligned upward, with explicit trade-offs. Use when the user needs to write next quarter's OKRs or check whether existing ones measure outcomes rather than activities. Not for per-person growth plans; see /leadership-develop.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# OKRs

Create or review OKRs for "$ARGUMENTS". Set clear objectives with measurable key results aligned to team and organizational goals.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"leadership-okrs","workflow":"leadership","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

## Prerequisites

None — utility skill, run anytime.

## Process

1. **Understand the context:**
   - What period are these OKRs for? (quarter, half, year)
   - What are the organizational or team-level goals?
   - If reviewing existing OKRs, read them first

2. **Define objectives:**
   - 2-3 objectives per team or individual
   - Each objective is qualitative, inspirational, and time-bound
   - Objectives should be ambitious but achievable (aim for 70% completion)

3. **Define key results:**
   - 3-5 key results per objective
   - Each key result is quantitative and measurable
   - Define the starting point, target, and how to measure
   - Must be outcomes, not activities ("Reduce churn to 3%" not "Run 5 campaigns")

4. **Align and prioritize:**
   - Do OKRs connect upward to organizational goals?
   - Are they realistic given capacity?
   - What will you NOT do to focus on these?

5. **Write the artifact** to `.singularskills/leadership/<project>/okrs.md`

## Output

The OKRs written to `.singularskills/leadership/<project>/okrs.md`. Present the objectives and key results to the user.
