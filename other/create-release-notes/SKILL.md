---
name: create-release-notes
description: Generate weekly release notes by reconciling merged GitLab MRs in a codebase area with a user-provided feature list. Use when drafting release notes for shipped work.
---

# PM: Create Release Notes

Generate weekly release notes by cross-referencing GitLab merge requests with
a user-provided feature list. The primary source of truth is the source code;
the user's feature list provides business context and framing.

This skill mirrors the weekly release notes process — querying shipped work in
a given week and drafting business-facing notes that PMs can review and refine.

---

## How to Help

When the user invokes this skill, follow this process:

### Phase 1: Confirm Scope

Before doing any work, confirm the following with the user:

1. **Date Range** — Default to the **current ship week** (Monday through Friday
   of the current week). If today is not a weekday, use the next upcoming week.
   Present the default and ask:

   > The default date range covers this week's ship window:
   > **Monday YYYY-MM-DD through Friday YYYY-MM-DD**.
   >
   > Would you like to:
   > - Use this week's ship window (default)
   > - Use a different week (e.g., next week, last week)
   > - Specify a longer duration (e.g., last 14 days, last 30 days, full quarter)
   > - Specify a custom date range (including future dates for upcoming releases)

   Calculate the dates based on today's date and the user's choice.

2. **Feature List (optional)** — Ask if the user wants to provide a list of
   features shipping this week. This list is the business context layer:

   > Do you have a list of features or items shipping this week? If so, paste
   > them or provide a markdown file path. I'll use these alongside the MR data
   > to generate accurate, business-facing release notes.

3. **Source Repository (optional but recommended)** — Ask if the user wants to
   cross-reference a GitLab source repository. If yes, collect:
   - The repository path (e.g., `your-org/platform/your-product`)
   - How far back to look for MRs (default: same as the date range)

4. **Audience** — Ask who the release notes are for:
   - **Internal teams** — Engineering, support, and PM stakeholders
   - **External developers** — Public-facing changelog or docs
   - **Both** — Generate two versions

### Phase 2: Query Source Code (Primary Source of Truth)

**Skip this phase if the user did not provide a GitLab repository.**

If a source repository was specified, use the Sourcegraph MCP tools to find
merge requests / commits completed in the date range:

```
sg_commit_search with:
  - repos: ["gitlab.example.com/your-org/<repo-path>"]  (or the user-provided path)
  - after: START_DATE
  - before: END_DATE
```

Also use `sg_diff_search` for broader pattern matching if needed.

**For each MR / commit, extract:**
- **Title** — Summary of what changed
- **Author** — Who shipped it
- **Merged date** — When it landed
- **Description** — First 200 chars for context
- **Labels / tags** — Any release stage, team, or category labels

**Present results in a working table:**

| Author | Summary | Merged Date | Labels |
|--------|---------|-------------|--------|
| Jane Smith | Campaign Level Portfolio View Settings Snapshot | 2026-01-30 | alpha |
| Alex Johnson | Generate weekly summary of Reliability SLOs | 2026-01-30 | |

### Phase 3: Reconcile Feature List vs. Source Code

**Run this phase if the user provided both a feature list and a repository.**

Compare the user-provided feature list against the MRs found:

1. **In the list but no MR found:** Flag items the user expects to be shipping
   that have no corresponding MR in the repository. These may be in a different
   repo, still in progress, or the dates may not align.

2. **MR exists but not in the list:** Flag any significant MRs that don't match
   items in the user's feature list. These might need to be added to release
   notes as undocumented changes.

Present findings as a gap analysis:

#### Potential Gaps: Features Without MRs
| Feature | Concern |
|---------|---------|
| Feature X | No matching MR found in repo — confirm it's shipping |

#### Potential Gaps: MRs Without Feature Entries
| MR / Commit | Description | Author | Concern |
|-------------|-------------|--------|---------|
| abc1234 | Major refactor of auth module | author@example.com | Not in feature list — add to notes? |

### Phase 4: Generate Release Notes

Using the data from all sources, generate two outputs:

#### Output A: Weekly Release Notes Table (for PM review)

This is the summary table for confirming what's shipping:

| Author | Summary | Merged Date | Release Stage |
|--------|---------|-------------|---------------|

Include review instructions:
1. If business-facing and shipping this week, the item belongs in release notes
2. If not shipping, flag it for follow-up
3. Note the deadline (typically EOD Thursday before the ship week)

#### Output B: Business-Facing Release Notes (for stakeholders)

Generate release notes using standard changelog categories:

- **New** — New features, capabilities, endpoints
- **Changed** — Modified behavior, performance improvements, updated defaults
- **Fixed** — Bug fixes (describe what was broken and what's fixed now)
- **Deprecated** — Features being phased out (include timeline and migration path)
- **Removed** — Features that have been removed
- **Security** — Security-related changes

**Writing guidelines:**
- Lead with developer/user impact, not implementation details
- Be precise about what changed and where
- For breaking changes, include migration guidance
- Note the release stage (Alpha, Closed Beta, Open Beta, GA) for each item
- Group items by product area or team when multiple teams are covered

**Present a draft to the user for review before finalizing.**

### Phase 5: Review & Iterate

After presenting the draft:
1. Ask if any items should be added, removed, or reworded
2. Confirm the audience — is this for external developers, internal teams, or both?
3. Ask about breaking changes requiring migration guidance
4. Flag items that appear to be missing release stage information
5. Iterate until the user approves

### Phase 6: Save as Markdown

Save the final release notes to the user's Desktop:

```
~/Desktop/release-notes-[YYYY-MM-DD].md
```

The output file follows this structure:

```markdown
# Release Notes — Week of [MM/DD]

## Summary Table

| Author | Summary | Merged Date | Release Stage |
|--------|---------|-------------|---------------|

---

## New

### [Feature Title]

**Release Stage:** [Alpha / Closed Beta / Open Beta / GA]

[Business-facing description of what changed and why it matters]

---

## Changed

[Same format]

---

## Fixed

[Same format]

---

## Deprecated / Removed

[Same format]

---

## Security

[Same format]
```

Confirm the file path after writing.

---

## Weekly Process Context

This skill supports the weekly release notes process:

1. Release management announces the upcoming ship week (typically mid-week)
2. PMs review what's shipping and either add business-facing notes or flag items not shipping
3. Deadline is typically **EOD Thursday** before the ship week
4. Once reviewed, the final markdown is shared with stakeholders

This skill automates step 2 — generating the summary table and drafting business-facing notes — so PMs can review and refine rather than write from scratch.

---

## Example Invocation

```
User: /create-release-notes

Claude: I'll generate release notes for you. Let me confirm the scope:

**Date Range:** This week's ship window is **Monday 2026-02-16 through Friday 2026-02-20**.

Would you like to:
1. Use this week's ship window (default)
2. Use a different week (e.g., next week, last week)
3. Specify a longer duration (e.g., last 30 days, full quarter)
4. Specify a custom date range (including future dates)

**Feature List (optional):** Do you have a list of features shipping this week?
Paste them or provide a markdown file path.

**Source Repository (optional):** Do you want to cross-reference a GitLab
repository? If so, which one?

**Audience:** Are these notes for internal teams, external developers, or both?
```

---

## Dependencies

- **Optional:** Sourcegraph MCP tools (for GitLab cross-reference)
- **Reference:** `prompts/claude/release-notes-writer.xml` for output template
