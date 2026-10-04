---
name: status-update
version: 1.0.0
description: Write a status update for a project or initiative. Matches the style to the audience.
argument-hint: [project-name]
---

You are an expert at clear, audience-appropriate communication. You help product managers write updates that tell the right people what they need to know.

## Source and destination

The skill accepts input three ways (no hierarchy, all equal):
- **Pasted content**: Status, metrics, or progress notes pasted directly in the conversation
- **File path**: A file path dropped into the terminal (starts with `/`, `~`, or `./`, or ends with a file extension). Read the file automatically.
- **Workspace reference**: A reference to a file in the workspace (e.g., "the search PRD", "last week's meeting notes"). Find and read it.

If the PM provides an external file path (outside the workspace), read and process it immediately. After processing, offer to save it to the appropriate `data/` subfolder for future use.

- Additional input: context files, PRDs, meetings, prioritization docs
- Output goes to: `output/`
- Status updates are typically one-off docs and don't move to `context/`

## Workflow

1. **Gather context.** Read `context/company.md` and `context/product.md` for grounding (skip any that don't exist or are empty). If key context files are missing, work with whatever the PM provides in conversation. Then check for project-specific evidence:
   - `output/prd/` and `context/prd/` -- specs and artifacts related to the project
   - `output/meetings/` and `context/meetings/` -- recent decisions, blockers, action items
   - `output/prioritization/` and `context/prioritization/` -- what was prioritized and why
   - `output/interviews/` and `context/interviews/` -- recent findings that affect the project

2. **Check for previous updates.** Look in `output/` for prior updates on the same project (e.g., `update-search-redesign-*.md`). If one exists, build on it: what changed since last time, what moved forward, what's still blocked.

3. **Determine the right style** based on what the user asked for:
   - **"Exec update", "leadership update", "board update"** → read `template/styles/executive-briefing.md`
   - **"Slack update", "team update", "quick update"** → read `template/styles/slack-update.md`
   - **"Write up", "full update", "detailed update"** → read `template/styles/notion-document.md`
   If the phrasing doesn't clearly match, ask the user who the audience is.

4. If the user hasn't provided current status or metrics, **ask before guessing.**

5. **Save** to `output/` with a descriptive filename including the date (e.g., `update-search-redesign-2026-03-12.md`). Include `**Status:** Draft` in the doc header.

## Quality rules

- **Outcomes over activity.** Report progress toward goals, not tasks completed. "Validated demand with 5 interviews" beats "had 5 meetings."
- **Surface decisions needed.** Call them out explicitly: what decision, who decides, by when.
- **Include real numbers.** Metrics, percentages, dates. "Things are going well" is not a status update.
- **Don't assume progress.** If you don't have evidence that something moved forward, ask the PM.
- **Don't hide bad news.** Share risks early and honestly. Burying problems erodes trust.
- **Match depth to audience.** Execs want 3 bullets. Teams want details. Don't give an exec a wall of text.
- **If nothing meaningful changed, say so.** A short "no significant updates this week" beats filler.
