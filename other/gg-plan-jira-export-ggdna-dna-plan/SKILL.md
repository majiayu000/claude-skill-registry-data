---
name: gg-plan-jira-export
description: Exports the next tickets of one person as a CSV file for the Jira import - matches the open tickets of the PM repo to the person by their areas, fills one sprint by the estimates and writes doc/exports/<date>-<name>-sprint.csv. Use when the user says "/gg-plan-jira-export", wants tickets in Jira, asks for a sprint or a CSV export, or names a person to plan the next tickets for.
---

# /gg-plan-jira-export

Read [jira-export-guide.md](../../../doc/guides/jira-export-guide.md)
and work by it.

## Important

- The person is required; ask for it if the user did not name one
- Export only tickets without a Jira key, and only one sprint's worth
- Use user names, issue types, priorities and sprint IDs exactly as the
  Jira project has them; read them from a Jira connection if one is
  available, else ask
- Show the matching and the sprint before writing the CSV
- Never write the person into a ticket file
- Write the Jira keys back only when the user asks for it after the import
