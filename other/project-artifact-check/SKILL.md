---
name: project-artifact-check
description: Check a project's artifacts and record against ARTIFACTSPEC and explain every finding with its requirement ID. Use when the user asks whether the project's artifacts are right, up to date or conform, after any change to the record or the plugin, before a release, or when an artifact looks wrong or out of step with the registry.
model: sonnet
effort: medium
---

# Project artifact — check

Runs the conformance checks of ARTIFACTSPEC §14 on the project's record and
explains the result. It reports and changes nothing, except through the script.
Never edit `registry.json`, `manifest.json`, a rendered HTML file or the
structure stylesheet by hand.

## Steps

1. **Run the check:**
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/project_artifacts.py" check --json`
   from anywhere inside the project's repository. Add `--record PATH` to check
   a record somewhere else (a scratch clone, for example). Exit 0 is clean.
   Exit 1 means findings. Exit 2 means the record is unreadable.
   The JSON also lists `notes`. A note is not a finding.
   - A project's own `.claude/rules/project-artifacts.md` that differs from the
     plugin's means the plugin now delivers the rule at session start. The copy
     can be deleted; offer to delete it.
   - Another note lists `url` or `published_sha256` fields dropped from feature
     entries of an older manifest (feature artifacts are no longer published).
     The next writing command rewrites the manifest.
2. **Clean:** say so in one line and stop.
3. **Unreadable (exit 2):** quote the script's message. Say which file it could
   not read, and stop. Do not guess at the record's contents.
4. **Findings:** for each, give the requirement ID the script reports, what is
   wrong in plain words, and the fix. Group findings that share a cause.
   Typical fixes:
   - Rendered HTML differs from a fresh render (INV-3; also a feature artifact
     still in the old claude.ai fragment form, or a full-progress link that is
     not the relative `feature-<slug>.html`, R5.27 to R5.30), a checklist or tile
     that differs from the registry (INV-1, R5.8), a stamp or contents list out
     of step (R5.2, R5.5): run `render --all`.
   - A content fragment, `meta.json` or `extra_css` problem (R4.10, R4.11,
     R5.2): run `export-content <key> --to <scratch dir>`, fix the file there,
     then run `edit-content <key> --from <scratch dir>`.
   - A `decisions.json` problem (R5.14 to R5.19: options, choice, IDs, previews,
     or a hand-written Decisions section): export the content, fix
     `decisions.json` there, then run `edit-content`. A warning that an open
     decision has no task in Needs you (R5.26) is fixed with
     `set-task-status <ID> "Needs you"`.
   - A task row that is wrong (R6.6 expected format, R6.10 basis, R4.5 or R4.6 IDs and
     prefixes, R6.1 status): change it with `set-task-status` or `task-add`,
     never by hand.
   - A structure stylesheet that differs (R5.10): run `render --all`. The
     renderer includes `${CLAUDE_PLUGIN_ROOT}/templates/project-artifact.css`
     unchanged.
   - A token block that is incomplete (R5.11): complete a copy of
     `docs/artifacts/design.css` in a scratch directory to the contract in
     `${CLAUDE_PLUGIN_ROOT}/design/DESIGN.md`, then run `design set <file>`.
   - Missing full-progress artifact with feature artifacts present (INV-2): run
     `full-progress-artifact-new`.
   - Title wrong (R5.1) or History not last (R5.4): the renderer owns both.
     Run `render --all` and report it if the finding stays.
5. **Offer to apply the fixes.** Only on a yes, run them, then run `check`
   again and report the new result. A fix that changes the record leaves
   Full Progress to publish. At the end of the turn, run `pending` and publish
   what it lists, as `task-status-update` describes (once; never mid-turn;
   feature artifacts are files and are never published).
6. **Report** findings fixed and findings left, each with its requirement ID.

## Old claude.ai pages

`check` notes retired pages (old claude.ai pages of feature artifacts) and the
older record format. Neither is a finding. Offer to delete each retired page.
After the owner confirms, delete it with the Artifact tool
(`action: "delete"`), then run `mark-deleted <key> --url <URL>`. A record in the
older format migrates with `render`.

## Finished features

A feature whose tasks are all Live or Dropped, with no open decision, can be
retired to free `docs/artifacts` (ARTIFACTSPEC §4.10). Offer this to the owner.
`retire KEY` is a dry run that lists what would go. `retire KEY --yes`
retires the feature (see `feature-artifact-new`, "Retire a finished feature").
Damage to a retired record (a missing archive, an unknown owner) is reported as
R4.31, R4.32 or R4.6.
