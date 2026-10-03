---
name: jira
description: >-
  Jira Cloud automation via jira-as CLI — router to 13 command domains
  (issue, search, agile, lifecycle, admin, …). Use when the user asks about
  Jira tickets, JQL, sprints, worklogs, service desk, or invokes /jira_*.
disable-model-invocation: true
---

### TO COPY

# jira

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/jira/scripts/skill_env.py)"
```

##### END TO COPY

# jira — Command Index

Router to `jira-as` command domains. References live in `command.md/` and `exemple.md/` under the **shared library** (`~/.meta-skills/skills/productivity/jira/`).

## Prerequisites

This skill documents the **`jira-as` CLI** ([PyPI](https://pypi.org/project/jira-as/) · [upstream](https://github.com/grandcamel/jira-as)). It is **not** bundled in Meta-Skills — install it once in the shared venv:

```bash
cd ~/.meta-skills/skills/productivity/jira
~/.meta-skills/install.sh pip init .
jira-as --help
```

`install.sh pip init` reads `requirements.txt` (includes `jira-as`). Load credentials into the shell, then call `jira-as` directly:

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/jira/scripts/skill_env.py)"
jira-as issue get PROJ-123
```

PowerShell:

```powershell
$env:CURRENT_SKILL_DIRECTORY = "{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/jira/scripts/skill_env.py --shell powershell | Invoke-Expression
jira-as issue get PROJ-123
```

`skill_env.py` reads `.env` via SkillCred and prints export commands for the detected OS/shell — no manual `source .env`.

## When to use

Trigger phrases: "create a Jira ticket", "search JQL", "move to Done", "log time",
"sprint backlog", "service desk request", "Jira admin", `/jira_*`.

## jira-issue

Core issue CRUD: create, read, update, and delete tickets.
Use for a single issue — view details, create a bug/task/story, or edit fields.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-issue.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-issue.exemple.md`

---

## jira-search

Find issues with JQL, saved filters, export, and bulk update from search results.
Use when you need to query, validate, export, or filter issues across a project.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-search.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-search.exemple.md`

---

## jira-lifecycle

Workflow transitions, assignments, resolution, versions, and components.
Use to change status, assign, resolve/reopen, or manage releases and components.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-lifecycle.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-lifecycle.exemple.md`

---

## jira-agile

Epics, sprints, backlogs, story points, and velocity tracking.
Use for Scrum/Kanban work — sprints, epics, backlog ranking, and estimates.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-agile.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-agile.exemple.md`

---

## jira-collaborate

Comments, attachments, watchers, notifications, and activity history.
Use to communicate on issues — add comments, upload files, or manage watchers.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-collaborate.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-collaborate.exemple.md`

---

## jira-relationships

Issue links, blockers, dependencies, and link statistics.
Use to link issues, trace blockers, or analyze dependency chains.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-relationships.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-relationships.exemple.md`

---

## jira-bulk

Bulk operations on many issues: transition, assign, clone, delete.
Use when acting on 10+ issues matched by JQL or key list — always dry-run first.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-bulk.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-bulk.exemple.md`

---

## jira-time

Worklogs, time estimates, tracking summaries, and timesheet reports.
Use to log time, manage worklogs, or generate time reports and exports.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-time.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-time.exemple.md`

---

## jira-fields

Custom field discovery, project field checks, and Agile field configuration.
Use to find field IDs, audit project fields, or set up Agile fields (admin).

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-fields.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-fields.exemple.md`

---

## jira-dev

Git branch names, commit parsing, PR linking, and PR descriptions from issues.
Use when connecting development workflow to Jira — branches, commits, and PRs.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-dev.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-dev.exemple.md`

---

## jira-jsm

Jira Service Management: service desks, requests, SLAs, queues, approvals, assets.
Use for ITSM workflows — incidents, service requests, SLAs, and customer portals.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-jsm.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-jsm.exemple.md`

---

## jira-admin

Project and system administration: permissions, users, screens, workflows, automation.
Use for Jira admin tasks — project setup, schemes, users, and configuration.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-admin.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-admin.exemple.md`

---

## jira-ops

Cache management and project discovery utilities.
Use to warm/clear cache or discover project metadata before other operations.

Commands → `~/.meta-skills/skills/productivity/jira/command.md/jira-ops.command.md`
Examples → `~/.meta-skills/skills/productivity/jira/exemple.md/jira-ops.exemple.md`

---