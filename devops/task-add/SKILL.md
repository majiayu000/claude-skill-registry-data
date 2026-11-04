---
name: task-add
description: Add a task to a project's artifacts — a unit of work with an ID, a status and an owner (a feature artifact or the project). Use before starting any piece of work that should be tracked, when the user says "add a task", "track this", or names new work for a feature, and whenever a branch needs a task ID to start its name with. Never edit the task registry by hand.
model: sonnet
effort: medium
---

# Task — add

Records work as a task in the registry (`docs/artifacts/registry.json`,
ARTIFACTSPEC 1.8.0) before the work starts. Only the script writes the
registry. Never edit `registry.json` or `manifest.json` by hand.

Every activity is a task before it starts, whoever does it. This covers work
given to agents and the session's own work (contracts, specs, reviews, joins,
test runs, releases, deploys, cleanup). A task is Running while any work for it
runs. Work that comes after it (join, CI, release) is a task of its own,
Running or To do. `Built` means finished but not released. `Live` means
released. (`Done` is a retired name for `Built`.)

Every command below is
`python "${CLAUDE_PLUGIN_ROOT}/scripts/project_artifacts.py" <command>`. Run it
from anywhere inside the project's repository. Exit 0 is success. On any other
exit, read the message, fix the cause and rerun.

## Steps

1. **Find the owner.** Read `docs/artifacts/manifest.json` (read only) in
   the working tree. The record is in `docs/artifacts/` there; the plugin never
   commits or pushes it. The owner is a feature artifact's `key`, or
   `project`. If the manifest does not exist, stop and offer
   `feature-artifact-new` or `full-progress-artifact-new`.
2. **Collect** these items:
   - the item (at most 80 characters)
   - the detail (plain text, at most 600 characters)
   - the status (default `To do`; one of Live, Built, Running, Needs you,
     Waiting, To do, On hold, Failed; Dropped needs
     `set-task-status --into/--reason`)
   - the expected date
   - for a project task, the app or service

   Ask only for what is missing. Use `Running` for work that is running as you
   add it.

   `expected` is a real date from `date` in the project's zone (the manifest's
   `timezone`): `DD Mon`, or `DD Mon ~HH:MM` for work due within a day,
   optionally followed by `; ` and a short note. Never `today`, `soon`,
   `tomorrow` or `next` alone. When you give an Expected time, give its basis
   too (what it waits on and how long): `--basis "agent slot ~01:30, ~1.5 h"`,
   at most 80 characters, open statuses only. It shows under the Expected value.

   A release (`--release`) may carry phases, repeatable
   `--phase NAME=HH:MM-HH:MM` (`agents`, `join`, `ci`, `merge`), and one named
   `--risk "LABEL=MINUTES"`. Its Expected is the end of its last phase. Name
   the risk; never pad it in.
   `--release` gives the task the next release number, shown as `RELEASE-<n>`.

   Work that rides a release says so with
   `--rides <release ID or RELEASE-n>`. Every Running or Built task that is not
   itself a release must do this (the command refuses otherwise).

   A task that ships nothing (a publish, a study, a cleanup) says so instead:
   `--no-release "REASON"`, at most 80 characters. It needs no release and is
   never Built (when finished, it goes Live). The command refuses
   `--no-release` with `--release` or `--rides`. Full Progress shows the task
   under `Not in a release yet` with the line `ships nothing: REASON`.
3. **Add it:**
   `task-add --owner <key|project> --item "TEXT" --detail "TEXT" --expected "DD Mon" [--basis "TEXT"] [--app A] [--status S] [--prefix P]`.
   For `--owner project`, `--prefix` picks one of the project's prefixes. The
   command registers a new prefix that no feature uses. The command prints the
   new ID, then renders the record and writes it to `docs/artifacts/` in the
   working tree. It never commits or pushes; the project commits when it
   chooses.
4. **Do not publish now.** Status changes accumulate during the turn.
   Publish Full Progress once, at the end of the turn, per "Publishing" in
   the `task-status-update` skill (claude.ai allows 200 publishes per account
   per day). Feature artifacts are files in the repository and are never
   published.
5. **Tell the owner** the new task ID, and that its branch name must start with
   it (`<ID>-short-name`).

## Old claude.ai pages

If `pending` lists `retired` pages (old claude.ai pages of feature artifacts),
ask the owner to confirm. Delete each confirmed page with the Artifact tool
(`action: "delete"`), then run `mark-deleted <key> --url <URL>`.
