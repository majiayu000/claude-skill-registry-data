---
description: Copy project emails from Gmail into Asana tasks for Noesis, Tyrn, Tymes
model: sonnet
---

# Goal

- Read the emails in the Gmail mailbox `saggese@gmail.com` about the projects
  `Noesis`, `Tyrn`, and `Tymes`
- Update the Asana board of each project:
  - Copy each email into the comments of the matching task
  - Create new tasks to track the activities that the emails describe
- Write a short plan with links to the Asana tasks and get the user approval before
  any change to Asana

# Conventions

- Follow the rules in `.claude/skills/asana.rules.md`
- Follow the template `.claude/templates/asana_plan.template.md`
- Follow the markdown conventions in `.claude/skills/markdown.rules.md`

# Arguments

- `<PROJECTS>`: projects to process, any of `Noesis`, `Tyrn`, `Tymes`
  - Default: all three
- `<SINCE>`: first day of the email window, in the format `YYYY-MM-DD`
  - Default: 7 days before today

# Workflow

## Resolve the Projects

- Fetch the contributors file:
  ```bash
  > gh api repos/gpsaggese/gpsaggese.github.io/contents/research/contributors.md \
      --jq .content | base64 -d
  ```
  - If `gh` fails, use `WebFetch` on the GitHub URL of the file
- For each project in `<PROJECTS>`, find its section in the file
  - Match the section by the start of its title, as described in
    `.claude/skills/asana.rules.md` `# Source of Truth`
  - Extract `<PROJECT_GID>` from the URL segment `/project/<PROJECT_GID>/` of the
    `Asana board` link
  - Collect the project signals from the other links of the section
  - Collect the names and emails of the people of the project
    - Use the contributors table (`Project` column) when the project has rows
    - Otherwise use the Asana project members from `get_project`
- If a project has no `Asana board` link, report it and skip the project
- Call `get_project` with `<PROJECT_GID>` for each project, before any read or write
  of its tasks
  - Record the name, the permalink, and the members
  - If the call fails, report the error and skip the project
  - Do not use the `workspaces` list of `get_me` as a check, since the workspace can
    be missing from it

## Verify the Mailbox

- Load the Gmail tools with `ToolSearch` if their schemas are not available
- Verify the connected mailbox is `saggese@gmail.com` as described in
  `.claude/skills/asana.rules.md` `# Gmail`
  - Open one recent thread with `get_thread`
  - Check that `saggese@gmail.com` appears in its headers
- If the check fails, stop and tell the user

## Collect the Emails

- For each project, build one Gmail query:
  - `after:<SINCE>`
  - AND an OR group of the contributor emails (`from:`, `to:`, `cc:`), the project
    name, and the project signals
- Run `search_threads` with the query, then `get_thread` for each thread
- For each message, record:
  - Message ID, thread ID, date
  - From, To, Cc
  - Subject, body, attachment names
- Drop the messages that are not relevant, following
  `.claude/skills/asana.rules.md` `## Relevance`
- If one message matches several projects, mark it `Decide`

## Read the Asana State

- For each project, list the tasks with `get_tasks` using `project=<PROJECT_GID>`
  - Request the fields `name,notes,assignee.name,due_on,completed,permalink_url`
  - Include recently completed tasks with `completed_since`
  - Follow the pagination token until all tasks are read
- For the tasks that match some email, read the comments with `get_task_stories`
  using `task_ids` and `resource_subtype=comment_added`
  - Find the markers `[gmail:<MESSAGE_ID>]`
  - Mark the messages that already have a marker as `Skip`

## Match Emails to Tasks

- Give each remaining message one outcome (`Comment`, `New task`, `Skip`, `Decide`)
  following `.claude/skills/asana.rules.md` `# Matching Emails to Tasks`
- Before a `New task` outcome, search the project for duplicates
  - Call `search_tasks` with `projects_any=<PROJECT_GID>` and `text`
  - If a similar task exists, change the outcome to `Comment` on that task
- Note any change to an existing task that an email states explicitly
  - Do not apply it: it goes to `Suggested Field Changes` in the plan

## Write the Plan

- Create `plan-asana.update_from_gmail.md` in the current directory
  - Create it before any change to Asana
- Follow the template `.claude/templates/asana_plan.template.md`
  - Add one H1 section per project
  - Link each task to update with its Asana URL
  - Put each `Decide` message under `Needs Decision`
  - Put each suggested change under `Suggested Field Changes`
- Print the path of the plan and these counts for each project:
  - Comments to add
  - Tasks to create
  - Suggested field changes
  - Skipped messages
  - Messages that need a decision

## Get Approval

- Make no Asana write call before this step is done
- Ask the user to choose one of:
  - Approve the plan as written
  - Approve after the user edits the plan file
  - Cancel
- For each message under `Needs Decision`, ask the user to pick a task or to skip it
- If the user cancels, stop and leave the plan file in place

## Apply the Plan

- Re-read the plan file after approval and execute only the items that it still
  contains
  - Skip an item that the user deleted or left out
- Create the new tasks first with `create_tasks`
  - Set `project_id`, name, notes, section, and due date from the plan
  - Set the assignee only if the plan lists one
- Add the email comments with `add_comment`, oldest message first
  - Use the comment format in `.claude/skills/asana.rules.md` `## Comment Format`
  - Use the plain `text` field and keep the body verbatim
  - If Asana rejects a comment for size, split it into consecutive comments
    - Label the parts as described in `.claude/skills/asana.rules.md`
      `## Comment Format`
- Apply a suggested field change only if the user approved it explicitly
- After each write, update the plan file
  - Tick the item
  - Replace a new task name with a link to the created task
  - Set `Status` to `applied`, or to `partially applied` on any failure
- On an error, stop, record it in the plan, and report it
  - Do not retry in a loop

## Report

- For each project, print:
  - The links to the tasks that received comments
  - The links to the new tasks
  - The messages that were skipped or not applied, with the reason
- State plainly what was not done

# Constraints

- Make no change to Asana before the user approves the plan
- Use Gmail in read-only mode
- Never hard-code Asana project IDs: read them from `research/contributors.md`
- Do not change the name, assignee, due date, or status of an existing task unless
  the user approves the change explicitly
- Do not commit `plan-asana.update_from_gmail.md`
- Do not copy an email that has no link to a project

# Examples

- **Bad** (comment is a summary and has no marker)
  ```text
  Simran says the draft is late
  ```
- **Good** (verbatim body with marker and headers)
  ```text
  [gmail:18f3a1c2d4e5b678] Email copied from Gmail
  From: <NAME> <<EMAIL>>
  To: saggese@gmail.com
  Date: Tue, 10 Nov 2026 09:14:00 -0500
  Subject: Noesis task unit draft
  Link: https://mail.google.com/mail/u/saggese@gmail.com/#all/18f3a1c2d4e5b678

  Hi, I will send the draft of the task unit definition by Friday.
  ```
- **Bad** (new task duplicates an existing one)
  - Plan: create "Write task unit definition" while the task "Task unit draft" exists
- **Good** (comment on the existing task)
  - Plan: add the email as a comment on "Task unit draft"

# Verification

- [ ] The plan file exists and has the line
  `Generated by .claude/skills/asana.update_from_gmail/SKILL.md`
- [ ] Every task to update in the plan has an Asana link
- [ ] No Asana write call happened before the user approved the plan
- [ ] Every copied email starts with the marker `[gmail:<MESSAGE_ID>]`
- [ ] A second run adds no duplicate comments
- [ ] No existing task changed name, assignee, due date, or status without approval
- [ ] The final report lists every skipped or failed item
