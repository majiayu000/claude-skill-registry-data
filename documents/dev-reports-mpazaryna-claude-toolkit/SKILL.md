---
name: dev-reports
description: Developer reporting skill for work documentation and communication. Use when writing journals, devlogs, status updates (22A/22B), progress reports, or documenting development work. Generates reports from git history or manual input.
---

# Dev Reports

Document and communicate development work. From git commits to polished reports.

## Report Types

This skill supports multiple report formats:

| Type | When to Use | Trigger Phrases |
|------|-------------|-----------------|
| **Git Journal** | Summarize work from commits | "journal this", "journal today's work" |
| **Devlog** | Narrative work documentation | "devlog", "write a devlog" |
| **Status (22A)** | Full Progress/Plans/Problems | "22A", "PPP update", "full status" |
| **Status (22B)** | Condensed status update | "22B", "quick status" |

## How to Use This Skill

1. **Identify the report type** from the request
2. **Load the appropriate template** from `examples/`:
   - Git journal → Read `examples/github-journal.md`
   - Devlog → Read `examples/devlog.md`
   - Status (full) → Read `examples/form-22a.md`
   - Status (condensed) → Read `examples/form-22b.md`
3. **Follow the workflow** in that template
4. **Generate the report** in the specified format

## Quick Reference

| Request | Template |
|---------|----------|
| "Journal this", "journal the last 4 hours" | `examples/github-journal.md` |
| "Write a devlog", "devlog update" | `examples/devlog.md` |
| "22A", "PPP update", "progress report" | `examples/form-22a.md` |
| "22B", "quick status" | `examples/form-22b.md` |

## Report Purposes

### Git Journal
Generates structured journal entries from git commit history. Great for:
- End of day summaries
- Sprint retrospectives
- Documenting refactors or features

### Devlog
Narrative-style work logs with context and decisions. Great for:
- Explaining technical decisions
- Sharing learnings with the team
- Building institutional knowledge

### Status Updates (22A/22B)
Structured Progress/Plans/Problems format. Great for:
- Team standups
- Leadership updates
- Weekly reports

## Part of the dev-* Family

| Skill | Purpose |
|-------|---------|
| `dev-inquiry` | Technical investigation and decision-making |
| `dev-reason` | Problem-solving and debugging (future) |
| `dev-reports` | Work documentation and communication |
