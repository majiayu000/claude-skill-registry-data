---
name: qfai-migration-v1-to-v2
title: QFAI 1.x to 2.x Migration
description: "Move an existing QFAI 1.x spec-pack project to the 2.x story-based spec tree using the bundled steps, then install and check the free-text entry. Use when asked to migrate a project that still holds QFAI 1.x spec packs."
allowed-tools: [Read, Glob, Write, Edit, Bash]
---

## /qfai-migration-v1-to-v2

## User Questions (AskUserQuestion Protocol)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`
for every user question. With `--auto`, ask nothing and record
explicit assumptions in the migration report.

Read `references/migration-guide.md` before changing the project.

Read `references/migration-placement.md` when you write `plan.yaml`, when a
step reports a retired configuration key, and when a step lists a document that
does not fit its template's shape. It holds the plan format, the retired keys,
the contract numbers, the business rules and what each document keeps.

Run this skill from the project root, where `qfai.config.yaml` and a locally
installed `qfai` package are available. The twelve scripts use the installed
package. They do not add a `qfai` subcommand or make network calls.

The skill serves two runs, and the steps tell them apart from the project
itself:

- **A 1.x project.** Every step runs: steps 1 to 10 migrate the spec packs,
  and step 11 installs the free-text entry and the reminder hooks.
- **A project an earlier 2.x release migrated.** Steps 1 to 10 each find no
  1.x layout and change nothing, since that release kept its working state
  under `.qfai/evidence/`, which no step reads. Step 11 adds only what that
  release lacked, such as the reminder hooks. Report that only the files step
  11 lists changed. The guide says how to reach this copy of the
  skill from an earlier release's.

Steps 1 to 10 each print one line before their report, in a dry run and a
real run. The line says what the step found:

| First line                                                      | What it means                                                                               |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `no 1.x layout found under <specsDir> (paths.specsDir=<value>)` | The tree shows no trace of the old layout, and steps 1, 9 and 10 have no work of their own. |
| `1.x layout found, migrating`                                   | The tree shows a trace of the old layout, or step 1, 9 or 10 has work of its own.           |
| `already migrated (id-map.json present)`                        | An earlier run migrated the project and no step has anything left to do.                    |

`<specsDir>` is the directory the project's configuration names for its specs
and `<value>` is the configured value, each written from the project root. Step
10 also ends with a `Summary:` line for the first two, and with the line saying
the migration is already done for the third. Steps 11 and 12 print neither
line, because they compare the project with the installed package and not with
the old layout. A step never decides that the project is in the wrong place: it
names the directory and leaves the check to the person.

Complete the launcher preflight in `.qfai/assistant/rule/references/launcher-preflight.md`
before running a CLI command.
Use `.qfai/assistant/rule/shared-skill-delegation-baseline.md` to route the declared roles and
keep authors separate from reviewers.

### Procedure

1. Inspect the spec packs, contracts, assistant files and configured paths. If
   the project already has the story tree and no migration ID map, run steps 1
   to 10. When every one of them prints
   `no 1.x layout found under <specsDir> (paths.specsDir=<value>)` first, then
   `none` under every section, and exits 0, report that there is nothing to
   migrate in the directory that line names and ask the person to check that
   the specs live there. Then continue at item 6. A step that prints another first line
   has found work: read its report as in item 2. If it has the story tree and
   the ID map, an earlier run migrated it, whole or in part: run steps 1 to 10
   all the same, each with `--dry-run` first. When each says the migration is
   already done, continue at item 6; otherwise they finish that run, and items 2 to 5
   apply to their reports. Otherwise write `tmp/qfai-migration/plan.yaml`
   with each old story's destination flow, any criterion whose parent story needs a judgment, and
   each old business rule's destination contract. Name that contract by its
   current path under `cli/`, `api/`, `db/` or `ui/` of the
   contracts directory: step 3 gives every contract a new ID and file name,
   and later steps find it from that path. Use the format in `references/migration-placement.md`. The plan
   may be written before step 1, from the old contract paths.
2. Before the first real run, tell the person that the migration deletes
   every 1.x file that has no destination and replaces every customised
   shipped skill and step directory, untracked files and uncommitted edits
   included, so that they
   commit or copy anything they need first: only what git history holds can be
   recovered. Run steps 1 to 3 in order. A dry run of a step refuses until the
   earlier steps ran, so each step's dry run follows the real run of the step
   before it. For **each** step, run `--dry-run` first, inspect its operations
   and write targets, then run it without `--dry-run`. Read the report each
   step prints and its exit code. Exit 2 stops before that step writes.
   Exit 3 means the step completed with items in `## For a person`; keep
   them for resolution. Step 1 removes the retired configuration keys
   `validation.traceability.scMustHaveTest` and
   `validation.traceability.unknownContractIdSeverity`, and step 3 replaces
   `prototyping.primarySpecId` where exactly one UI contract is tied to it.
   Steps 4 to 12 refuse, naming the key, while one of the three remains in
   `qfai.config.yaml`.
3. After step 3, confirm the old `_policies/11_Slice-Policy.md` is deleted
   and none of its sections was copied into `principle.md`. Current
   triage rules belong to `qfai-sdd/references/sdd-triage.md`. Read the four files assembled from multiple
   sources: `objective.md`, `initiative.md`, `principle.md` and `tech.md`.
   Remove facts duplicated in different words. Each document the steps write is in
   its `qfai-sdd` template's shape, and what does not fit is listed for a
   person. In `tech.md`, replace each `<...>` placeholder its old files did not
   supply.
4. Run steps 4 to 10 in order, each with `--dry-run` followed by the real run.
   Read every report as in item 2.
5. Resolve every reported item with the person responsible for the content.
   Preserve any item the scripts could not place. Before step 4 writes
   `id-map.json`, settle an example that cites several criteria and a rule that
   binds no contract through the plan keys `references/migration-placement.md` names. After it, do not
   change `plan.yaml` to move a mapped item. Place remaining content in the new
   tree through `/qfai-sdd`, and finish each listed item as the guide's
   "Resolve the reports" section says.
6. After step 10, run steps 11 and 12 in order, each with `--dry-run` followed
   by the real run, and read their reports as in item 2. Step 11 installs the
   free-text entry and the reminder hooks `npx qfai init` installs, through the
   same merge, and brings `.agents/rules/reminders.json`, the text the hooks
   print, to the package's copy. Do not edit
   `.claude/settings.json`, `.codex/hooks.json` or `reminders.json` by
   hand: relay what step 11 lists under `## Operations` and
   `## Reminder hooks`, the line about trusting the Codex hooks with `/hooks`
   included. Step 12 checks the entry and writes nothing.
7. Resolve every item step 12 lists under `## For a person`. Rerun step 11 for
   an item it installs, and step 10 for a `gitignore` item. Resolve each `old-path` item with the
   person who wrote the file, by rewording the line so that it no longer names
   the old path, using the 2.x path that the guide's table gives for it. Rerun step 12 until it exits 0.
8. Then run `npx qfai validate` through the launcher proven by preflight.
   Resolve layout and chain errors. Use its BF, AC and EX test-obligation
   findings to finish test coverage or record a permitted decision exception.
9. Hand the project's first free-text change request to `qfai-run`. From here
   on, a change goes to it in plain words.
10. When you report the migration done, tell the person that the plan and the
    ID map are under `tmp/qfai-migration/`, which git ignores and which they
    may delete, and that what the migration deleted survives only where git
    history held it.

| Step | Bundled script               | Result                                                         |
| ---- | ---------------------------- | -------------------------------------------------------------- |
| 1    | `01-rename-directories.mjs`  | Rename owned directories and update old default config paths.  |
| 2    | `02-merge-tables.mjs`        | Merge decisions, questions and change records into two tables. |
| 3    | `03-move-catalog.mjs`        | Move policy, catalog and assistant content; number contracts.  |
| 4    | `04-renumber-ids.mjs`        | Build the flow and story tree and write the fixed ID map.      |
| 5    | `05-cases-to-examples.mjs`   | Convert test-case-only rows into examples.                     |
| 6    | `06-derive-ac-refs.mjs`      | Derive each example's criterion reference.                     |
| 7    | `07-rules-to-contracts.mjs`  | Put business rules in their enforcing contracts.               |
| 8    | `08-rewrite-annotations.mjs` | Rewrite resolvable test annotations.                           |
| 9    | `09-repoint-links.mjs`       | Repoint host integration links only.                           |
| 10   | `10-update-gitignore.mjs`    | Reset the managed `.gitignore` block.                          |
| 11   | `11-install-entry.mjs`       | Install skills, links, ignores and hooks.                      |
| 12   | `12-check-entry.mjs`         | Check, without writing, the entry and the files' 1.x paths.    |

Each script is invoked as
`node <skill-dir>/scripts/<script>.mjs [--dry-run]`, with `<skill-dir>` set to
this installed skill directory. `scripts/_step.mjs` is the shared package
loader used by all twelve entry points and must be shipped with them. Step 9
only repairs links. Do not run `npx qfai init --force` during migration.

Every script prints `## Operations` even when empty, after the first line of
steps 1 to 10. Steps 2 through 12 also print `## For a person`; step 5 prints
`## Cases to examples`; step 8 prints `## Annotations kept`; step 11 prints
`## Reminder hooks`; step 12 prints `## Files scanned`. An empty section says
`none`. Rerunning a completed step changes no file. On a project whose migration finished, steps 1 to 10 add one last line
saying it is already done. The complete write boundary is in
`references/migration-guide.md#write-boundary`.

### Reviewer Gate

The reviewer is `architecture-reviewer`. It checks the old-to-new mapping and preservation of
unplaced content. The reviewer checks the twelve reports, rerun
behavior, and validation result. Enforce the Drift Protocol and
`.qfai/assistant/rule/test-layers.md` when reviewing test obligations. Counts and effort
estimates are signals, not gates. Record PASS or REVISE on the final tree.

## Default Autopilot Policy

- auto-decide:
  - output formatting
  - ID / sequence numbering
- ask-user:
  - a story or rule placement that project evidence cannot settle and that is
    needed to finish migration
  - an operation beyond the declared write boundary
- hard-required:

The skill authors the plan from project evidence. It has no separate
user-supplied input that every invocation must provide.

project_memory:

- After step 4, place unplaced content through `/qfai-sdd`, and finish each item as the guide says.
