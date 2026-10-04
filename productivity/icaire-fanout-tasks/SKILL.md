---
name: icaire-fanout-tasks
description: Fan out currently discussed ICAIRE task pages into separate Codex threads using handoff prompts built from the ICAIRE Cortex MCP task tools. Use when the user wants ICAIRE task threads, selected tasks from a recent what's-next snapshot, daily kickoff threads, or prompts filtered by task assignee, status, or priority.
---

# ICAIRE Fanout Tasks

Use this skill when the user wants currently discussed ICAIRE task pages fanned
out into handoff-ready Codex threads. ICAIRE tasks are page-backed records under
`tasks/*.md`; do not read or reconstruct local TODO files.

By default, create one new Codex thread per ready task in the current
conversation scope when the Codex app thread tools are available. The current
conversation scope is narrower than the whole task queue: it means tasks the
user just named, task slugs or titles just created or discussed, task numbers
from the immediately preceding ICAIRE what's-next snapshot, or a set explicitly
filtered in the user's fanout request.

Only fan out the broad active queue when the skill is invoked as the accepted
follow-up to an ICAIRE what's-next snapshot, for example after the assistant
offers fanout and the user replies `yes`, or when the user explicitly asks for
all ready/open/in-progress ICAIRE tasks, daily kickoff threads, or another broad
queue scope.

Only return copyable prompts instead of creating threads when the user
explicitly asks for prompts only, or when live thread creation is unavailable
after targeted tool discovery.

## Contract

- Use ICAIRE Cortex MCP, not local TODO files.
- Resolve the requested fanout scope before listing tasks. Do not default to
  the whole active ICAIRE queue merely because the user said "fan out".
- Start with `me` only when the request is for the authenticated member. If the
  authenticated user is not an active member, stop and explain that ICAIRE
  membership must be configured before member-scoped task fanout works.
- Fetch tasks with `tasks/list` only for the resolved scope.
- When task records include `readiness` and `execution_mode`, use them as
  handoff hints, then read the task body before generating prompts.
- Prefer slash tool names; use underscore aliases only if needed.
- Discover and use `codex_app.create_thread` for live fanout when available.
- Output launched thread IDs or links in chat. Do not write a file unless
  explicitly asked.

## Workflow

1. Resolve the fanout scope before listing tasks:
   - If the user names task slugs, task titles, task numbers, or says "these",
     "this", "the ones we just made", or similar, restrict fanout to those
     currently discussed tasks.
   - If the user is responding to an immediately preceding ICAIRE what's-next
     snapshot with `yes`, "fan these out", or selected numbers, preserve that
     snapshot's numbering and fan out only the accepted ready items.
   - If the user explicitly asks for "all", "daily kickoff", "all ready",
     "all open", "all in progress", or a broad assignee/status/priority filter,
     use that broad queue scope.
   - If there is no recoverable current task scope and no explicit broad scope,
     ask the user which tasks to fan out instead of defaulting to the whole
     active queue.
2. Call `me` and confirm `member.person_slug` exists only when the request is
   for "my" or assigned-to-me tasks.
3. Call `tasks/list` only for the resolved scope:
   - for broad queue scope, call `tasks/list` twice by default: first with
     `status: "in_progress"`, then with `status: "open"`
   - for selected task numbers from an ICAIRE what's-next snapshot, reuse the
     snapshot task records when available; otherwise call `tasks/list` for the
     necessary status/filter and match by slug/title
   - for slugs or titles from the current conversation, call the narrowest
     available `tasks/list` filters, then match by slug/title from the MCP
     records; do not launch unrelated tasks merely because they share a status
     or priority
4. If `tasks/list` is not visible, use targeted Codex tool discovery for the
   ICAIRE `tasks/list` tool before falling back to runtime or code inspection.
5. Honor explicit scoping in the user's request:
   - use `assignee: me` for "my tasks" or "assigned to me"
   - use a specific `people/<slug>` when the user names an assignee
   - use a named priority such as `p0`, `p1`, `p2`, or `p3` when requested
   - use a named status when requested; otherwise use the resolved scope rules
     above
6. Use the returned task title, body, priority, assignees, source slugs,
   readiness, execution mode, and slug to create one prompt per fanout-ready
   task. The prompt itself must contain the task context needed to begin; do
   not make the worker fetch or read the task page before starting.
7. Read linked `source_slugs` only when the task body is too thin to produce a
   good handoff prompt.
8. Treat `readiness` and `execution_mode` as useful hints, then read the task
   body. If `## Open Questions` contains substantive questions, keep the task
   out of worker prompt blocks and list it as needing input, unless the task is
   clearly an interactive guided session whose purpose is to answer those
   questions with the user.
9. Classify the remaining tasks with `readiness` and `execution_mode`:
   - Generate autonomous handoff prompts for tasks with `readiness: "ready"`
     and `execution_mode: "agent"`.
   - Generate guided-session prompts for tasks with `readiness: "ready"` and
     `execution_mode: "interactive"`, instructing Codex to walk through the
     task with the user step by step.
   - Keep `readiness: "underspecified"` and `execution_mode: "user"` tasks out
     of prompt blocks and list them separately as needing user action or input.
   - If `execution_mode` is absent because the remote server has not yet been
     updated, infer conservatively: use `agent` for autonomous implementation
     or research, `interactive` for review/judgement/approval, and `user` only
     for actions Codex cannot physically help with.
   If `readiness` is absent because the remote server has not yet been updated,
   infer readiness conservatively from the task body and open questions.
10. Produce up to 10 prompts, ordered by status, priority, due date, and task
    order returned by the server.
11. Discover the Codex thread tools before concluding live fanout is
    unavailable:
   - Call `tool_search` for `create_thread`.
   - Use `codex_app.list_projects` when available to choose an appropriate
     target for each worker thread.
   - Use `codex_app.create_thread` for each ready task, passing the generated
     handoff prompt as the new thread's initial prompt.
   - Use a repo project target with a local or worktree environment when the
     task clearly belongs to a known local project.
   - Use `target: { "type": "projectless" }` for general ICAIRE work or tasks
     that do not clearly belong to one code repository.
   - Preserve returned thread IDs or links so they can be reported.

Respond in chat with the launched thread list and any blocked/non-fanned-out
tasks. Do not write the result to a file, do not return only a file link, and
do not make the user open an artifact to see what was launched.

## Output Requirements

Default output is capped at 10 ready items within the resolved scope. Keep each
worker prompt short, self-contained, and suitable as the initial prompt for a
fresh Codex thread:

- When live thread creation succeeds, start with
  `Launched ICAIRE task threads`.
- Show ready `in_progress` tasks first, followed by ready `open` tasks.
- Include only tasks whose MCP record has `readiness: "ready"` and
  `execution_mode: "agent"` or `execution_mode: "interactive"` after the
  open-questions override above, or conservatively inferred equivalents only
  when fields are absent.
- Each ready task must be one concise fenced text prompt block that leads with
  the actual task content, using plain language drawn from the task page rather
  than a slug-heavy reference style.
- Do not use task slugs as prompt headings or lead text.
- The first paragraph must be only the task-specific brief: what to do, what to
  focus on, and the concrete output expected for this task. Do not mix generic
  workflow instructions into this paragraph.
- Put the reusable worker instructions in a separate paragraph after the
  task-specific brief.
- For `execution_mode: interactive` tasks, the prompt must ask Codex to work
  with the user step by step, pause at judgement or approval points, and avoid
  making the final decision for the user. Prepend this sentence before the
  task-specific brief:
  `I need to get this done, and I want you to walk me through it step by step.`
- After that prepend, keep the same task-specific brief format as autonomous
  prompts: what to do, what to focus on, and the concrete output expected for
  this task.
- Each prompt should stand on its own by pulling in the key task details, so a
  reader can tell what they are doing without needing to parse internal file
  references first or find the task in the brain before beginning.
- The reusable-instructions paragraph should be concise and use this wording:
  `Show me the result for approval once you finish the task. Once approved, update the ICAIRE brain, marking the task as done or in_progress, enriching related pages and their timelines, and noting the successor task if needed.`
- Include the source task slug only as a compact completion/update reference,
  for example `Source task: tasks/<slug>`. Do not instruct the worker to read,
  open, find, or fetch the task from the brain before starting.
- Do not format ready tasks as a numbered list.
- Do not add generic boilerplate about reading files, preserving local changes,
  verification, or commits beyond the required completion handoff.
- When live thread creation succeeds, do not print the full worker prompts by
  default. Instead, show a concise launched-thread list with each task title,
  execution mode, and returned thread ID or link.
- When the user explicitly asks for copyable prompts only, or live thread
  creation is unavailable, print the prompt blocks instead of thread IDs.
- Show a `Needs user action before fanout` section after ready prompts for
  input-needed tasks and `execution_mode: "user"` tasks.
- Keep the input-needed list succinct; name each task by human-readable title
  or action, not slug, and include the blocking question(s), preferring the task
  page's `## Open Questions` section when present.

If no actionable ICAIRE task pages match the requested filters, say that
directly and do not invent prompts.

If live thread creation is unavailable after targeted `create_thread`
discovery, output exactly:

`Parallel execution unavailable here.`

Then provide the shortest useful set of copyable worker prompts.

## Guardrails

- Treat MCP task data as authoritative for task status and assignees.
- Do not use local TODO files for this skill.
- Do not mutate tasks while fanning them out.
- Do not fan out the whole active queue merely because the skill was invoked.
  Whole-queue fanout is allowed only after an ICAIRE what's-next snapshot
  fanout offer is accepted, or when the user explicitly requests a broad queue
  scope.
- When the user has just created or discussed one or more ICAIRE tasks, treat
  those tasks as the fanout scope unless they say otherwise.
- Creating Codex threads is allowed by this skill; mutating ICAIRE task pages
  is not.
- Do not create prompts for tasks with `status: done` or `status: archived`
  unless the user explicitly asks for those statuses.
- Do not create prompts for input-needed tasks or tasks with
  `readiness: underspecified` when readiness is present.
- Do not create prompts for tasks with `execution_mode: user`.
- Keep each prompt scoped to one task; split multi-task records into
  input-needed items rather than guessing hidden subtasks.
- Do not show other members' tasks when the user asked for their own next work.
- Do not silently fall back to all tasks when `me` cannot resolve.
- Do not treat external people as assignable members.
- Do not claim fanout ran unless `codex_app.create_thread` succeeded for the
  relevant workers.
