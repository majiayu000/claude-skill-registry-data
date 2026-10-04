---
name: report-publisher
description: Turn research, analysis, or any markdown the agent just produced into a live, beautifully designed web report with a shareable tracked URL via ReportRoom. Use when the user says "publish this", "make this shareable", "turn this into a report", "put this on a page", or wants findings to live beyond the chat. Not for recurring client deliverables (use client-reporter), slide decks (use deck-publisher), or proposals that need view alerts (use proposal-tracker).
---

# Report Publisher

The default "get it out of the chat" skill: whatever was just produced — deep research, a competitive analysis, a technical write-up — becomes a live web report with a URL worth sharing.

Follow the shared flow in the root `SKILL.md` (access check → `get_design_system` → author → `lint_document` → approval → `publish`). This file covers only what's specific.

## When to use

- The user finished a research/analysis task and says "publish this", "make this a report", "make this shareable", "I want to send this to someone"
- Long markdown output that deserves better than a chat scroll or a raw gist
- The user wants a link, not a file

## Steps

1. **Scope the content.** Confirm what goes in (the whole conversation output? just the final analysis?) and the audience (colleague, community, public). Audience decides tone of the framing, not the facts. If it's for the team rather than the world and the user is in a team workspace (`account_status` → `org_kind: team`), publish with `visibility: "team"` so only signed-in org members can view it.
2. **Structure for the web, don't paste.** Reshape chat-formatted output into a real document: a title that states the finding, an executive summary up top, sections with descriptive headings, data moved into tables/charts where the design system provides them, sources/appendix at the end. Cut conversational scaffolding ("as we discussed above…").
3. **Author + lint + approval gate** per the shared flow. In the preview, include your suggested title — titles that state the conclusion travel better than topic labels ("X is 30% cheaper than Y at scale", not "X vs Y comparison").
4. **Publish and hand over the URL.** Mention the page is tracked: "ask me later how it's doing" (`get_analytics`).

## Hard rules

- Preserve the substance exactly — restructuring is allowed, changing findings, numbers, or hedges is not.
- Keep the user's citations/sources; a published report without its sources is a downgrade, not an upgrade.
- If content contains third-party confidential material (client names in research, quoted private messages), flag it at the approval gate.
