---
name: workbench
description: Handle Workbench workflows and product guidance including task lookup, My Tasks, task dialogs, sprint planning, favorite spaces, Workbench/Attendance comparison, overdue-task review, project overview, wiki retrieval, project creation, task creation, and wiki-to-task drafting.
---

# Workbench Skill Tree

Navigate Workbench helpers categorized by functional domains:

## 1. Project Management & Spaces
- `skills/workbench/create_project/SKILL.md` — Create a new Workbench project/space with intake and confirmation (supports `--enable-sprint true|false`).
- `skills/workbench/update_project/SKILL.md` — Update project name, description, status, dates, icon, color, or enable/disable Sprint planning (`--enable-sprint true|false`).
- `skills/workbench/delete_project/SKILL.md` — Permanently delete a project/space after confirmation.
- `skills/workbench/show_project_overview/SKILL.md` — List and inspect projects, owners, statuses, and metadata.
- `skills/workbench/show_project_progress_report/SKILL.md` — View project progress, task completion metrics, and overdue stats.
- `skills/workbench/get_project_status_meta/SKILL.md` — Retrieve valid project status UUIDs and metadata.
- `skills/workbench/manage_project_members/SKILL.md` — List, invite, remove, or update roles for project members.
- `skills/workbench/share_and_permissions/SKILL.md` — Project sharing, visibility, and role permission guidelines.
- `skills/workbench/favorite_spaces_help/SKILL.md` — Help on pinning and managing favorite project spaces.
- `skills/workbench/manage_favorite_spaces/SKILL.md` — List, pin/add, or remove favorite spaces (projects).
- `skills/workbench/workbench_public_space_help/SKILL.md` — Help on public vs private spaces.

## 2. Task Management & Time Tracking
- `skills/workbench/create_task/SKILL.md` — Canonical public flow to create a task with missing-field intake and confirmation.
- `skills/workbench/update_task/SKILL.md` — Update task title, description, status, priority, dates, assignee, or story points.
- `skills/workbench/delete_task/SKILL.md` — Permanently delete a task by ID after explicit user confirmation.
- `skills/workbench/get_tasks/SKILL.md` — List/search tasks by project, assignee, status, priority, keyword, or paging.
- `skills/workbench/get_task_detail/SKILL.md` — Fetch one task's full details (description, dates, people, links, custom fields) by task UUID.
- `skills/workbench/show_my_highest_priority_task/SKILL.md` — Quickly identify the caller's highest priority task.
- `skills/workbench/get_overdue_tasks/SKILL.md` — List overdue tasks across projects.
- `skills/workbench/get_task_status_meta/SKILL.md` — Retrieve valid task status UUIDs and metadata.
- `skills/workbench/get_status_meta/SKILL.md` — Generic status metadata helper.
- `skills/workbench/get_status_latest/SKILL.md` — Check latest status updates.
- `skills/workbench/add_task_comment/SKILL.md` — Post a comment or update message on a task.
- `skills/workbench/get_task_comments/SKILL.md` — Retrieve comment history for a task.
- `skills/workbench/log_task_time/SKILL.md` — Log spent work time on assigned tasks.
- `skills/workbench/manage_linked_tasks/SKILL.md` — Link/unlink task dependencies (blocks, is blocked by, relates to).
- `skills/workbench/manage_custom_fields/SKILL.md` — List or set custom field values on tasks.
- `skills/workbench/my_tasks_help/SKILL.md` — User guidance on the My Tasks personal queue.
- `skills/workbench/task_dialog_help/SKILL.md` — User guidance on task dialog views, full-screen, and details.
- `skills/workbench/gantt_and_roadmap/SKILL.md` — How-to guidance for Gantt chart and timeline views.
- `skills/workbench/workbench_attendance_tracking_help/SKILL.md` — Guidance comparing Workbench tasks vs Attendance Tracking.

## 3. Sprint Planning & Agile Cycles
- `skills/workbench/create_sprint/SKILL.md` — Create a new sprint with goal, start/end dates (only for projects with sprint planning enabled).
- `skills/workbench/start_sprint/SKILL.md` — Activate a planned sprint (transition to ACTIVE).
- `skills/workbench/complete_sprint/SKILL.md` — Close active sprint with open-task rollover to backlog or next sprint.
- `skills/workbench/update_sprint/SKILL.md` — Update sprint name, goal, or dates.
- `skills/workbench/get_sprints/SKILL.md` — List all sprints (active, planned, closed) for a project.
- `skills/workbench/assign_tasks_to_sprint/SKILL.md` — Move tasks into sprint or return to backlog.
- `skills/workbench/sprint_planning_help/SKILL.md` — User guidance on sprint planning workflows.

## 4. Wiki & Space Documentation
- `skills/workbench/create_wiki_page/SKILL.md` — Create a new wiki page in project or company wiki.
- `skills/workbench/update_wiki_page/SKILL.md` — Update wiki title or Markdown content.
- `skills/workbench/move_wiki_page/SKILL.md` — Reorder or move wiki page in document tree.
- `skills/workbench/delete_wiki_page/SKILL.md` — Permanently delete a wiki page after confirmation.
- `skills/workbench/get_wiki/SKILL.md` — Fetch wiki page content with scope resolution.
- `skills/workbench/search_wiki/SKILL.md` — Search wiki documents by natural-language query via GraphRAG.
- `skills/workbench/page_content/SKILL.md` — Fetch project wiki page Markdown content.
- `skills/workbench/page_hierarchy/SKILL.md` — Get project wiki document tree hierarchy.
- `skills/workbench/company_page_content/SKILL.md` — Fetch company wiki page content.
- `skills/workbench/company_page_hierarchy/SKILL.md` — Get company wiki document tree hierarchy.
- `skills/workbench/manage_wiki_comments/SKILL.md` — List, reply to, create, resolve, or delete comment threads on wiki pages.
- `skills/workbench/project_wiki_help/SKILL.md` — User guidance on wiki and documentation features.
- `skills/workbench/generate_wiki_content/SKILL.md` — AI assistant to draft/synthesize wiki documents.
- `skills/workbench/create_task_from_wiki/SKILL.md` — Workflow to derive and create a task from wiki content.

## 5. AI Drafting & General Overview
- `skills/workbench/generate_task_description/SKILL.md` — AI assistant to draft structured task descriptions.
- `skills/workbench/feature_overview/SKILL.md` — High-level overview of Workbench modules and capabilities.

## Universal Design & Confirmation Principles (MANDATORY)
1. **No Implicit Assumptions**: If a user request is vague or lacks specific entities (e.g. "add task to sprint", "update task", "delete task"), **DO NOT guess, assume, or automatically select all items**. List available options and ask the user to explicitly select target tasks, sprints, or fields.
2. **Mandatory Input Verification & Preview**: Before calling ANY write/mutation script (create, update, delete, start/complete, assign, link, comment, log time), ALWAYS present a clear, structured summary of all resolved parameters to the user.
3. **Mandatory Turn Boundary (STOP & Wait for User Confirmation)**: The agent MUST NOT call the execution script in the same turn as presenting the preview. The agent MUST ask for explicit confirmation (e.g., "Do you confirm ...?") and END its turn, waiting for the user's explicit approval (e.g., "yes", "confirm", "đồng ý") in a subsequent turn before executing.

## Suggested Navigation & Resolution Flows
- **Project Resolution**: When `project_id` is unknown, run `python skills/workbench/show_project_overview/scripts/show_project_overview.py [--project-name "<name>"]`.
- **Enable/Disable Sprints**: To enable or disable sprints on a project (e.g. "enable sprint for this project"), resolve `project_id` and run `python skills/workbench/update_project/scripts/update_project.py --project-id <UUID> --enable-sprint true|false`. Do NOT call `create_sprint`.
- **Sprint Resolution**: Once `project_id` is known, run `python skills/workbench/get_sprints/scripts/get_sprints.py --project-id <UUID>` to resolve sprint UUIDs.
- **Task Resolution**: When task name/number is known, run `python skills/workbench/get_tasks/scripts/get_tasks.py --name "<title or keyword>" --page-number 0` to resolve `task_id`.
- **Status Resolution**: Run `get_project_status_meta` for projects or `get_task_status_meta` for tasks to keep valid status UUIDs visible during clarification.
