---
name: dev-meeting-followup
description: Review developer meeting notes from the UCEAP IT Software Engineering wiki to process any outstanding action items. Creates Jira tickets, updates meeting notes, and manages the wiki Home page. Use when processing UCEAP meeting followups or planning a dev meeting.
---

# Developer Meeting Followup Skill

This skill helps you systematically work through developer meeting notes from the UCEAP/.github-private wiki to identify and resolve unresolved followup items.

## Overview

Work through meeting notes listed on the wiki Home page in chronological order (oldest to newest), checking for unresolved action items and helping resolve them.

## Important Criteria

**Only consider unchecked checkboxes as followup items.** Do not treat general discussion topics or questions without explicit checkbox action items as followup items.

## Prerequisites

1. Clone the wiki repository if not already available:
   ```bash
   git clone https://github.com/UCEAP/.github-private.wiki.git /tmp/github-private-wiki
   ```

2. If the repository is already cloned, ensure it is up to date:
   ```bash
   cd /tmp/github-private-wiki
   git pull
   ```

3. Ensure you have access to:
   - GitHub CLI (authenticated)
   - Jira API credentials (check environment variables: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY)

## Workflow

For each meeting listed on the wiki Home page (starting with the oldest):

### 1. Read the Meeting Notes

Read the meeting agenda file to identify any unchecked checkboxes (`- [ ]`).

### 2. Review Each Unchecked Item

For each unchecked checkbox:
1. Present the item to the user
2. Ask if it has been resolved externally
3. If not resolved, help resolve it:
   - If it requires creating Jira tickets, create them using the Jira REST API
   - If it requires other actions, work with the user to complete them

### 3. Create Jira Tickets (if needed)

When creating Jira tickets:
- **Project**: Use WEBP4 for website issues, or ask user which project to use
- **Issue Type**: Task (unless specified otherwise)
- **Labels/Components**: DO NOT use labels or components
- **Linking**: Link related tickets using the "Relates" link type
- **Description**: Include context and link back to the meeting notes

Example API call:
```bash
curl -s -X POST "${JIRA_BASE_URL}/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" \
  -d '{
    "fields": {
      "project": {"key": "WEBP4"},
      "summary": "Task summary",
      "description": {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Description here"}]}]
      },
      "issuetype": {"name": "Task"}
    }
  }'
```

### 4. Update the Meeting Notes

After resolving an item:
1. Mark the checkbox as complete: `- [x]`
2. Add ticket references if applicable: `([WEBP4-123](https://uceapit.atlassian.net/browse/WEBP4-123))`

### 5. Update the Home Page

Once all unchecked items in a meeting are resolved:
1. Remove that meeting's link from the Home page
2. The oldest unresolved meeting should remain at the bottom of the list (just above "Previous meetings")

### 6. Commit and Push Changes

Make **separate commits** for:
1. Meeting agenda updates (e.g., "Mark excessive revisions action items as complete (WEBP4-988, WEBP4-989)")
2. Home page updates (e.g., "Remove resolved Developer Meeting Agenda 2025-09-16 from home page")

Then push all commits to GitHub:
```bash
cd /tmp/github-private-wiki
git add <files>
git commit -m "message"
git push
```

### 7. Move to Next Meeting

Repeat the process for the next oldest meeting on the Home page.

### 8. Create New Meeting Agenda (when all meetings are resolved)

When there are no meetings remaining with open action items:

1. **Determine the next meeting date**: Find the next Tuesday or Thursday from today's date, whichever is sooner
2. **Read the template**: Get the template content from the markdown code block in `Developer-Meeting-Agenda-Template.md` (lines between the ``` markers)
3. **Create new meeting file**: Create a new file named `Developer-Meeting-Agenda-YYYY-MM-DD.md` with the template content
4. **Update Home page**: Add the new meeting link at the top of the Meeting Agendas & Notes section
5. **Commit and push**:
   ```bash
   cd /tmp/github-private-wiki
   git add Developer-Meeting-Agenda-YYYY-MM-DD.md Home.md
   git commit -m "Create new Developer Meeting Agenda for YYYY-MM-DD"
   git push
   ```

## Notes

- The wiki Home page only shows recent meetings; older meetings not listed have already been fully resolved
- Use the TodoWrite tool to track progress through multiple meetings
- Always work chronologically from oldest to newest
- Be systematic and thorough to ensure no items are missed
- When all meetings are resolved, create a new meeting agenda for the next Tuesday or Thursday
