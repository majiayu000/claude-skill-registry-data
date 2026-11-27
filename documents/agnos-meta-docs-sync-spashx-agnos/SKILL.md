---
name: agnos-meta-docs-sync
description: "AGNOS maintainer skill. Updates CHANGELOG.md, AGENTS.md, CLAUDE.md and the user's guide AGNOS-GETTING-STARTED.md, agnos-init's template, from what changed in the repository since each of them was last changed. USE FOR: before a release, or after a series of tasks, when the entry-point documents may have drifted. Edits the four files only and never commits: the maintainer reviews and commits."
argument-hint: "(no arguments)"
---

# AGNOS Documentation Sync

<!-- FTR-DOC-001; RQ-DOC-001 (the report), RQ-DOC-002 (this procedure), RQ-DOC-003 (the sub-agent) -->

A maintainer skill, like `agnos-meta-demo`: it keeps the entry-point documents true to the repository. It is not a process
skill, so `AGENTS.md` and `CLAUDE.md` do not list it. Canonical procedure, shared by GitHub Copilot
(`.github/skills/agnos-meta-docs-sync/`) and Claude Code (`.claude/skills/agnos-meta-docs-sync/`, which points here). The
sub-agent that runs it is defined in `.github/agents/agnos-meta-docs-sync.agent.md`; `.claude/agents/agnos-meta-docs-sync.md`
points to it for Claude Code, on the Haiku model.

## Procedure

1. From the repository root, run the report (`python3` on `linux` / `macos`, `python` on `windows`):

   ```
   python .github/skills/agnos-meta-docs-sync/scripts/changes_since.py
   ```

   It prints JSON: `head`; `targets`, one per document, with `lastCommit` (the commit that last changed it, or null) and
   `commits` (the non-merge commits since, each with `sha`, `subject`, `files` and `moreFiles`); `skills`, with `name`,
   `path`, `description` and `maintainer`, true when the name starts with `agnos-meta-` <!-- RQ-MTA-002 -->. Commits that touch only the generated index and the session files are already
   left out. Exit code 1: the folder is not a git repository, stop and report.
2. For each document, in the order below, read the document, read the commits listed for it (open a commit's changed file
   when its subject is not enough to know what changed: `git show <sha> -- <file>`), and apply the rules below.
3. Never commit and never push: the maintainer reviews `git diff` and commits through the AGNOS workflow.
4. End with a summary: for each document, what you added, changed or removed (one line each) and what you left alone and
   why. Say so when a document needed nothing.

## Rules for every document

- Edit only these four files. Keep each document's own style, wording, heading levels and line width.
- Never state what no commit or file supports: no invented feature, version number, date or behaviour. When a commit's
  effect is unclear, leave the document as it is and say so in the summary.
- A skill whose report entry has `maintainer: true` is never listed in `AGENTS.md` or `CLAUDE.md`.

## `CHANGELOG.md`

- Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Put the new entries under a `## [Unreleased]` heading
  directly after the introduction and above the latest release; create it if it is missing. Under it, the sections that
  have entries, in this order: `### Added`, `### Changed`, `### Fixed`, `### Removed`.
- One bullet per user-visible change, from the commit subjects since the file's last change: `feat` is Added, `fix` is
  Fixed, a `refactor` or `docs` that changes what a user sees is Changed, a removal is Removed. Skip `chore`, tests-only
  and index-only commits. Several commits of one task are one bullet. End a bullet with the artifact IDs of the commit
  subject in an HTML comment, for example `<!-- TASK-TRC-046, RQ-TRC-058 -->`, never as plain text.
- If `## [Unreleased]` already exists, add only what it does not hold yet (compare the artifact IDs). Never edit, reorder
  or delete a released section.

## `AGENTS.md` and `CLAUDE.md`

- `AGENTS.md`: the table of section 3 ("Skills") has one row per skill, in the existing format; add a row for a skill that
  appears in the report with `maintainer: false` and is missing, remove the row of a skill that no longer exists, and
  correct a row whose description no longer matches the skill's `description`. Section 5 ("Where things are") follows the
  same rule for a folder the commits added or removed.
- `CLAUDE.md`: the "Tool Mapping" list has one bullet per non-maintainer skill, in the existing wording (its Claude Code
  entry point under `.claude/skills/`, its canonical procedure under `.github/skills/`); add, remove or correct the bullet
  the same way. Keep the `@` import and the HTML comments that cite requirement IDs.

## `.github/skills/agnos-init/assets/templates/AGNOS-GETTING-STARTED.md`

<!-- RQ-PLG-022 / DEC-PLG-017 -->
- The user's guide, which `agnos-init` writes into each project. It is a worked example, addressed to a user of the plugin: it
  names skills, never a path of this repository. Change only a passage that describes a behaviour the commits changed: a skill's name or
  commands, a session variable, the commit message format, the end-of-session steps. Find the passage with a search for
  the changed name or command, correct that passage, and leave the rest, including the example project.
- If no commit changed such a behaviour, leave the file as it is and say so.
