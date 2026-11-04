---
name: task-status-update
description: Change a task's status in a project's artifacts and, at the end of the turn, publish Full Progress once. Use when work starts, finishes, fails, waits or is blocked on the owner, when a pull request is opened, ready or merged, when CI passes or fails, when a deploy goes live, when a hook reports queued status events or pending artifacts, or when the user asks to mark, update or move a task. The only way to change a status; never type a status row by hand.
model: sonnet
effort: medium
---

# Task — status update

Changes a task's status through the script. Full Progress shows the status.
Publish Full Progress once, at the end of the turn, never after each change:
claude.ai allows 200 publishes per account per day and every republish counts.
Feature artifacts are files in the repository and are never published.

Every activity is a task, the session's own included (contracts, joins, test
runs, releases, cleanup). A task is `Running` while any work for it runs. It is
`Waiting` or `Needs you` when it is blocked on something or someone. Before a
turn ends with work still running in the background, its task is `Running`.

`Built` means finished but not released. `Live` means released. `Done` is a
retired name that the script stores as `Built`. Release work that comes later
(join, CI, release) is its own task, Running or To do.

A task set to `Running` or `Built` rides a release: pass
`--rides <ID or RELEASE-n>` in the same call (the command refuses otherwise).
Two cases are exempt:
- The task is a release itself.
- The task ships nothing: `--no-release "REASON"`, at most 80 characters, never
  together with `--release` or `--rides`. Such a task is never Built; when
  finished, it goes Live. `--no-release ""` clears it.

Only the script writes the registry. Never edit `registry.json` or
`manifest.json` by hand, and never type a status row into an artifact. The
statuses reach the artifact's At a glance block by themselves, so never write
them into a lede. A `meta.json` lede holds one or two sentences of context the
registry cannot show (an incident, a constraint, a plan).

Every command below is
`python "${CLAUDE_PLUGIN_ROOT}/scripts/project_artifacts.py" <command>`. Run it
from anywhere inside the project's repository. Exit 0 is success. On any other
exit, read the message, fix the cause and rerun.

## Steps

1. **Find the task ID and the new status.** The ID is the one in the user's
   words, in a queued event (`queue list`), or at the start of the current
   branch name (`AR5-artifactspec` is task `AR5`). The status is one of Live,
   Built, Running, Needs you, Waiting, To do, On hold, Failed, Dropped. A
   suggested status from a queued event is a suggestion: confirm it
   matches what happened. A word outside the nine maps to the nearest
   (`Merged` is `Live`, or `Built` when the project's `merged_status` says so).
2. **Change it:**
   `set-task-status <ID> "<Status>" [--detail "TEXT"] [--expected "DD Mon"] [--item "TEXT"] [--basis "TEXT"] [--history "TEXT"] [--no-release "REASON"] [--started "DD Mon ~HH:MM"|HH:MM] [--into ID|RELEASE-n] [--reason "TEXT"]`.
   - `--detail`: plain text, at most 600 characters. Use it when what the row
     says changed.
   - `--expected`: a real date from `date` in the project's zone, `DD Mon` or
     `DD Mon ~HH:MM`, optionally followed by `; ` and a short note. Never
     `today`, `soon`, `tomorrow` or `next` alone. For Live or Built it defaults
     to the current date; do not pass one.
   - `--basis`: when you give an Expected time, give its basis too (what it waits
     on and how long), for example `"agent slot ~01:30, ~1.5 h"`. At most 80
     characters; `""` clears it. Open statuses only: a row that goes Live,
     Built or Failed drops it.
   - `--waits-on owner|work`: for a Waiting or On hold task, who it waits on.
     `owner` lists it under Needs you in At a glance. `work` (the default) lists
     it under Waiting for other work, with what it waits on (the basis) first.
     `""` clears it.
   - `--started`: when the work began, `DD Mon ~HH:MM` or `HH:MM` (today) in the
     project's zone, before Expected; `""` clears it. It is where a no-release
     task's bar starts on the release timeline. Give it for work that began
     earlier and is now Waiting or Needs you. A task that first moves to
     Running gets the current time by itself (R5.48).
   - `Dropped`: closes a task truthfully when its work was folded into another
     task or is no longer wanted (not Live, not Failed, not On hold). Give
     `--into <task ID or RELEASE-n>` (required for a release: the release that
     took its cargo) and/or `--reason "TEXT"` (at most 80 characters). The row
     leaves the open lists and the timeline and shows
     `dropped: folded into RELEASE-n` under `Live or built` (R5.49). First move
     any task that rides a dropped release, with `--rides`.
   - `--history`: one line for the feature artifact's History table. Use it for
     a feature task whose change the owner should be able to look up later.

   The command does these things:
   - renders every artifact that shows the task, and any other page whose look
     is older than the installed plugin's (R7.5)
   - removes the task's queued events
   - writes the record to `docs/artifacts/` in the working tree

   The plugin never commits or pushes the record; the project commits when it
   chooses.
3. **Do not publish yet.** Change as many statuses as the turn needs, each
   with `set-task-status`. They accumulate. Publish at the end of the turn, per
   "Publishing" below.
4. **Clear what is stale.** If `queue list` still shows events for tasks that
   no longer apply, remove them with `queue clear --id <ID>`.
5. **Report** the task, its old and new status, and whether Full Progress was
   published. If there is no Artifact tool, say what is still unpublished and
   stop.

## Publishing

Publish once, at the end of the turn, never mid-turn. Repeat until `pending`
exits 0:

- Run `pending --json`. It lists Full Progress (the only artifact it lists) and
  writes the publish copy: the same page with absolute `file:///` links to the
  feature files. The entry carries `key`, `title`, `path` (the absolute path of
  the publish copy) and `url`.
- Publish with the Artifact tool. `file_path` is the entry's `path`, unchanged.
  `url` is the entry's `url` when it is not empty.
  - If the publish is refused because the artifact does not exist, list the
    owner's artifacts (`action: "list"`) and match the exact `title`. Publish
    to that one. Publish a new one (with an `icon` such as `tracker`) only when
    none matches.
  - If the publish is refused because the artifact changed elsewhere, `read`
    the live version once. Copy content-section changes through
    `export-content full-progress --to <dir>` and
    `edit-content full-progress --from <dir>`, then retry once with the new
    `path`. Changes to the generated sections are dropped.
- Run `mark-published full-progress --url <URL>` with the URL the publish
  returned.
- `pending` lists Full Progress only when what the owner sees changed (a task
  added, or its status, item, Expected or release fields, an open decision, a
  feature row). A change to a detail, a basis or a content section rides the
  next publish.
- If claude.ai refuses the publish for its daily limit, do not retry. Run
  `mark-deferred full-progress --until <ISO time of the reset>` (for a limit
  that resets at UTC midnight, the next UTC midnight, for example
  `2026-10-13T00:00:00+00:00`). Until then `pending` lists Full Progress as
  `deferred until HH:MM (<zone>)` and exits 0, and the end-of-turn hook does
  not block; it prints one line. After that time `pending` lists it again. A
  later `mark-published` clears the deferral.

## Old claude.ai pages

`pending` also lists `retired` pages: claude.ai pages of feature artifacts
published before feature artifacts became files. They never block publishing,
and `pending`'s exit code ignores them. Delete one only with the owner's
confirmation: ask the owner, delete each confirmed page with the Artifact tool
(`action: "delete"`), then run `mark-deleted <key> --url <URL>` (add `--gone`
for a page that no longer exists). When the session-start or after-command
context lists retired pages, offer the deletion to the owner at the start.
