---
name: user-story
description: Creates well-structured user stories for software development and project management. Use when the user asks to write, create, or format a user story, or needs to document requirements, features, or tasks in user story format.
---

# User Story Skill

Create clear, actionable user stories following industry best practices.

## Guidelines

- Use the standard user story format: "As a [type of user], I want [goal] so that [reason/benefit]"
- Keep titles concise and descriptive
- Write a brief 1-2 sentence summary explaining the context
- **Be concise - avoid over-doing it with too much detail**
- Focus on user value and outcomes, not implementation details

## Structure

Use the template provided in `template.md` to ensure consistency:

1. **Title**: Brief, descriptive headline starting with "As a..."
2. **Summary**: 1-2 sentences providing context
3. **Task List** (optional): Use for highly technical, non-user-facing work
4. **Acceptance Criteria** (optional): Use for user-facing stories to define what "done" looks like

**Important**: Stories typically have EITHER a task list OR acceptance criteria, not both. Choose based on the story type:

## Best Practices

- **Keep it simple**: Don't over-engineer the story with unnecessary detail
- Make acceptance criteria specific and measurable (when included)
- Use "Given-When-Then" format sparingly and only when it adds clarity
- Keep stories focused on a single piece of value
- For task lists, list only essential implementation steps
- For acceptance criteria, list only what's needed to verify completion

## Examples

### User-Facing Story (Acceptance Criteria)

**Title**: As a user, I want to reset my password via email

**Summary**: Users who forget their passwords need a secure way to regain access to their accounts.

**Acceptance Criteria**:

- User can request password reset from login page
- System sends reset link to registered email
- Reset link expires after 24 hours
- User can set new password using valid link

### Technical Story (Task List)

**Title**: As a developer, I want to upgrade the database schema

**Summary**: We need to migrate from the old schema to support new feature requirements.

**Task List**:

- Create migration script
- Test migration on staging environment
- Schedule maintenance window
- Execute migration on production
- Verify data integrity

### Balanced Story (Both - Use Sparingly)

**Title**: As an admin, I want to export user data to CSV

**Summary**: Administrators need to extract user data for reporting and compliance purposes.

**Task List**:

- Implement CSV export endpoint
- Add data filtering options

**Acceptance Criteria**:

- Admin can select which fields to export
- System handles 10,000+ users
- File downloads automatically when ready
- Export includes timestamp and admin username in filename
