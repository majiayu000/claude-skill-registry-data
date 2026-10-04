---
name: release-notes
description: "Generate release notes from a Linear cycle — pulls completed issues, categorizes them, and formats the notes using the previous cycle's format as a template."
argument-hint: "<cycle_number>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
  - mcp__plugin_linear_linear__list_teams
  - mcp__plugin_linear_linear__list_cycles
  - mcp__plugin_linear_linear__list_issues
  - mcp__plugin_linear_linear__list_issue_statuses
---

# Release Notes

You **generate release notes from a Linear cycle** — pulling completed issues from engineering teams, categorizing them, and formatting them for the team. This is a standalone utility skill, not a pipeline stage.

## Inputs

- `$ARGUMENTS` — the cycle number (integer, e.g., `47`)
- The conventions file — projects path (from Pipeline Configuration → Work Directory → Projects) and project tracker config
- `<projects-path>/release-notes/*.md` — previous release notes (for format reference)

## Pre-Flight Checks (MANDATORY)

Run ALL checks before doing anything else. If any check fails, **STOP** and report the issue.

### Check 1: Argument Is a Number

`$ARGUMENTS` must be a single integer (the cycle number). If it's missing, empty, or not a number, **STOP**:

> "Usage: `/release-notes <cycle_number>` — provide a cycle number (e.g., `/release-notes 47`)."

### Check 2: Pipeline Config Exists

Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract:
- **Projects path** from Work Directory → Projects
- **Project Tracker → Tool** — must be "Linear"

If no conventions file is found, **STOP**:

> "No conventions file found (`CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md`). This skill requires Pipeline Configuration with Linear as the project tracker."

If the project tracker is not Linear, **STOP**:

> "This skill requires Linear as the project tracker. Current tracker: [value]."

### Check 3: Cycle Exists

Look up the Engineering team using `list_teams` (search for "Engineering"). Then use `list_cycles` on that team to find the target cycle by number.

Try `list_cycles` with type `current` first. If the target cycle number isn't in the current cycle, try `previous`, then `next`.

If the cycle is not found across all three queries, **STOP**:

> "Cycle $ARGUMENTS not found on the Engineering team. Available cycles: [list what you found]."

Record the cycle's **start date**, **end date**, and **ID** for later use.

## Step-by-Step Procedure

### Step 1: Read Previous Release Notes (Template Discovery)

Check for existing release notes:

```bash
mkdir -p <projects-path>/release-notes
```

Use Glob to find `<projects-path>/release-notes/*.md`. If files exist, read the most recent one (sorted by filename, which includes the date). This becomes your **format template** — match its structure, tone, section headings, and bullet style.

If no previous files exist, use the **Built-In Template** (see below).

### Step 2: Look Up Teams and Cycles

Find the four engineering teams using `list_teams`:
- **Engineering** (the primary team — cycle numbers match user-facing cycle numbers)
- **Web**
- **iOS**
- **Android**

For each team found, look up the target cycle. The Engineering team's cycle is already found from Pre-Flight Check 3. For the other teams, search for a cycle with the same number or overlapping date range.

Not all teams may have a matching cycle — that's OK. Record which teams have cycles and which don't.

### Step 3: Fetch Completed Issues

For each team that has a matching cycle, fetch issues in "Done" and "Pending Release" statuses:

1. First, use `list_issue_statuses` for each team to find the exact status names/IDs for completed states (look for statuses of type "completed" — typically "Done"). Also look for any status named "Pending Release" or similar.

2. Then use `list_issues` with the team and cycle filters, filtered to those completed statuses.

Collect all issues across all teams. For each issue, record:
- Title
- Team (Engineering, Web, iOS, Android)
- Labels (if any)
- Issue identifier (e.g., `ENG-123`)

### Step 4: Categorize Issues

Group issues into three categories using this priority order:

**Priority 1 — Label-based (most reliable):**

| Label Pattern | Category |
|---------------|----------|
| "feature", "enhancement" | New Features |
| "bug", "fix" | Maintenance |
| "tech-debt", "cleanup", "deprecation", "chore" | Cleaning Up |

**Priority 2 — Title keyword heuristics:**

| Title Pattern | Category |
|---------------|----------|
| Starts with or contains: "Add", "New", "Introduce", "Launch", "Enable" | New Features |
| Starts with or contains: "Fix", "Resolve", "Update", "Improve", "Upgrade", "Patch" | Maintenance |
| Starts with or contains: "Remove", "Delete", "Clean", "Deprecate", "Refactor", "Drop" | Cleaning Up |

**Priority 3 — Default:**

If neither labels nor title keywords match, default to **Maintenance**.

**Internal flagging:**

Flag issues that appear to be internal/engineering-only (not customer-facing) with `[INTERNAL?]` in the draft. Heuristics for internal items:
- Title mentions "refactor", "tech debt", "CI", "pipeline", "deploy", "infrastructure", "migration" (without user-facing context)
- Labels include "internal", "devops", "infra"

These flags help the operator decide what to include in the final notes.

### Step 5: Rewrite Issue Titles

Transform Linear issue titles into customer-friendly descriptions:

- Remove prefixes like "Fix:", "Bug:", "Feature:" — incorporate them naturally
- Replace internal jargon with user-facing language
- Focus on what changed for the user, not how it was implemented
- Keep descriptions concise (one sentence)
- For bug fixes, describe what works now, not what was broken

Examples:
- `"Fix: PDF export crashes when area has no inspections"` → `Fixed an issue where PDF exports could fail for areas without recent inspections`
- `"Add inspection schedule limit setting"` → `**Inspection Schedule Limit** - Administrators can now set a maximum number of inspections that can be scheduled per area`
- `"Remove deprecated v3 API endpoints"` → `Retired legacy API v3 endpoints (replaced by v4)`

### Step 6: Ask for Mobile Build Numbers

Use `AskUserQuestion` to ask the operator:

1. **Current iOS build version** (e.g., "5.2.1 (Build 847)")
2. **Current Android build version** (e.g., "5.2.1 (Build 312)")

Present as a single question with two text fields. If the operator doesn't have them yet, they can enter "TBD" and fill them in later.

### Step 7: Write Release Notes

Generate the release notes file. Use the format from the previous cycle's notes (Step 1) if available, otherwise use the Built-In Template.

**Filename:** `<projects-path>/release-notes/<end-date>-cycle-<N>.md`

Where `<end-date>` is the cycle end date in `YYYY-MM-DD` format and `<N>` is the cycle number.

Write the file.

### Step 8: Present Draft Summary

Tell the operator:

1. The file path where notes were written
2. Summary: number of issues categorized (X new features, Y maintenance, Z cleanup)
3. Which teams had cycles (and which didn't)
4. Any items flagged `[INTERNAL?]` — list them so the operator can decide whether to keep or remove
5. Remind them: "Review and wordsmith the descriptions before posting. Remove `[INTERNAL?]` flags — either delete the item or remove the flag to keep it."

## Built-In Template

Use this template when no previous release notes exist in the `release-notes/` directory:

```markdown
# Release Notes for Cycle {N} ({start_date} - {end_date})

## Mobile App Builds

* **iOS**: {ios_version}
* **Android**: {android_version}

## Links

* [iOS in the App Store](https://apps.apple.com/us/app/orangeqc/id324039524)
* [OrangeQC in the Google Play Store](https://play.google.com/store/apps/details?id=com.orangeqc.native)

## New Features

* **{Feature Name}** - {Customer-friendly description of what's new}

## Maintenance

* {Customer-friendly description of fix or improvement}

## Cleaning Up

* {Description of removal or deprecation}
```

**Format notes:**
- Use `*` for bullet points (not `-`)
- Bold the feature name in New Features (e.g., `**Feature Name** - description`)
- Maintenance and Cleaning Up items don't need bold names — just descriptions
- Dates in the header use the format from the cycle data (e.g., "Jan 27 - Feb 3, 2026")
- If a category has no items, omit that section entirely

## What NOT To Do

- **Do not post or publish the notes.** Write them to a file — the operator posts them after review.
- **Do not prompt for each issue individually.** Categorize in batch, review at the end.
- **Do not include issue identifiers** (like `ENG-123`) in the output — release notes are customer-facing.
- **Do not make up issues.** Only include issues that came from the Linear cycle query.
- **Do not include cancelled or backlog issues.** Only "Done" and "Pending Release" statuses.
