---
name: thrunt-complete-milestone
description: Archive completed milestone and prepare for next version
argument-hint: "<version>"
allowed-tools: Read, Write, Bash
---


<objective>
Mark milestone {{version}} complete, archive to milestones/, and update HUNTMAP.md and HYPOTHESES.md.

Purpose: Create historical record of published version, archive milestone artifacts (huntmap + requirements), and prepare for next milestone.
Output: Milestone archived (huntmap + requirements), MISSION.md evolved, git tagged.
</objective>

<execution_context>
**Load these files NOW (before proceeding):**

- @.github/thrunt-god/workflows/complete-milestone.md (main workflow)
- @.github/thrunt-god/templates/milestone-archive.md (archive template)
  </execution_context>

<context>
**Project files:**
- `.planning/HUNTMAP.md`
- `.planning/HYPOTHESES.md`
- `.planning/STATE.md`
- `.planning/MISSION.md`

**User input:**

- Version: {{version}} (e.g., "1.0", "1.1", "2.0")
  </context>

<process>

**Follow complete-milestone.md workflow:**

0. **Check for audit:**

   - Look for `.planning/v{{version}}-MILESTONE-AUDIT.md`
   - If missing or stale: recommend `/thrunt-audit-milestone` first
   - If audit status is `gaps_found`: recommend `/thrunt-plan-milestone-gaps` first
   - If audit status is `passed`: proceed to step 1

   ```markdown
   ## Pre-flight Check

   {If no v{{version}}-MILESTONE-AUDIT.md:}
   ⚠ No milestone audit found. Run `/thrunt-audit-milestone` first to verify
   requirements coverage, cross-phase integration, and E2E flows.

   {If audit has gaps:}
   ⚠ Milestone audit found gaps. Run `/thrunt-plan-milestone-gaps` to create
   phases that close the gaps, or proceed anyway to accept as tech debt.

   {If audit passed:}
   ✓ Milestone audit passed. Proceeding with completion.
   ```

1. **Verify readiness:**

   - Check all phases in milestone have completed plans (SUMMARY.md exists)
   - Present milestone scope and stats
   - Wait for confirmation

2. **Gather stats:**

   - Count phases, plans, tasks
   - Calculate git range, file changes, LOC
   - Extract timeline from git log
   - Present summary, confirm

3. **Extract accomplishments:**

   - Read all phase SUMMARY.md files in milestone range
   - Extract 4-6 key accomplishments
   - Present for approval

4. **Archive milestone:**

   - Create `.planning/milestones/v{{version}}-HUNTMAP.md`
   - Extract full phase details from HUNTMAP.md
   - Fill milestone-archive.md template
   - Update HUNTMAP.md to one-line summary with link

5. **Archive requirements:**

   - Create `.planning/milestones/v{{version}}-HYPOTHESES.md`
   - Mark all v1 requirements as complete (checkboxes checked)
   - Note requirement outcomes (validated, adjusted, dropped)
   - Delete `.planning/HYPOTHESES.md` (fresh one created for next milestone)

6. **Update MISSION.md:**

   - Add "Current State" section with published version
   - Add "Next Milestone Goals" section
   - Archive previous content in `<details>` (if v1.1+)

7. **Commit and tag:**

   - Stage: MILESTONES.md, MISSION.md, HUNTMAP.md, STATE.md, archive files
   - Commit: `chore: archive v{{version}} milestone`
   - Tag: `git tag -a v{{version}} -m "[milestone summary]"`
   - Ask about pushing tag

8. **Offer next steps:**
   - `/hunt-new-program` — start next milestone (questioning → research → requirements → huntmap)

</process>

<success_criteria>

- Milestone archived to `.planning/milestones/v{{version}}-HUNTMAP.md`
- Hypotheses archived to `.planning/milestones/v{{version}}-HYPOTHESES.md`
- `.planning/HYPOTHESES.md` deleted (fresh for next milestone)
- HUNTMAP.md collapsed to one-line entry
- MISSION.md updated with current state
- Git tag v{{version}} created
- Commit successful
- User knows next steps (including need for fresh requirements)
  </success_criteria>

<critical_rules>

- **Load workflow first:** Read complete-milestone.md before executing
- **Verify completion:** All phases must have SUMMARY.md files
- **User confirmation:** Wait for approval at verification gates
- **Archive before deleting:** Always create archive files before updating/deleting originals
- **One-line summary:** Collapsed milestone in HUNTMAP.md should be single line with link
- **Context efficiency:** Archive keeps HUNTMAP.md and HYPOTHESES.md constant size per milestone
- **Fresh requirements:** Next milestone starts with `/hunt-new-program` which includes requirements definition
  </critical_rules>
