---
name: syncing-design-snapshot
description: "Pull a Claude Design page template (.dc.html + shared scripts) into a repo's static-site snapshot and re-apply the repo's own patches, failing loudly on anything the design changed. Use when re-syncing a site from its design system."
compatibility: Designed for Claude Code
metadata:
  intended-tools: Read, Write, Bash, Artifact, DesignSync
  stability: experimental
---

# Syncing a design snapshot into a repo

A repo can ship pages that a design tool owns: the design system holds the templates (`*.dc.html` plus shared
scripts), and the repo keeps a flat snapshot of them (e.g. `packages/<site>/public/`) with a short, reviewed list
of its own changes. This skill re-syncs that snapshot. It never writes to the design system.

## 1. Fetch the template (main session; the scripts do not fetch)

Where the design system lives decides the tool:

- **A Design System artifact** (`claude.ai/artifact/<id>`; files under `project/`). Systems migrated from the
  standalone tool, and new ones, are artifacts. List the files with the Artifact tool (`action: "list"`,
  `scope: "files"`, the artifact `url`); the listing names the current version, so note it. Read the page and
  the shared files it loads (`action: "read"`, `paths`, an `out_dir`), e.g. `project/templates/<page>/*` and
  `project/templates/_shared/<script>.js`. `DesignSync` cannot reach an artifact.
- **A standalone claude.ai/design project** (`claude.ai/design/p/<projectId>`). Use `DesignSync` `list_files`
  and `get_file`. `get_file` is reported to cap at 256 KiB and truncate silently (unverified: no vendor doc
  states a limit, as of 2026-11-24); check that a large file ends where it should. Standalone Claude Design
  closes on 14 December 2026, per the help-centre article
  [Migrate from standalone Claude Design to Claude](https://support.claude.com/en/articles/17440474-migrate-from-standalone-claude-design-to-claude)
  (read 2026-11-24). After migration the standalone copy is read-only, so a migrated system must be read
  from its artifact.

Copy the text files flat into one directory (binary files such as photos stay in the snapshot; fetch them once).
Design systems can change several times a day: fetch right before syncing, and never reuse an earlier fetch.

## 2. Configure the patches

`scripts/sync_template.py` reads a project config with `TARGET_DIR` and `PATCHES`, a list of
`(file, original, replacement, why)` tuples (`replacement=None` deletes). Start from
`examples/project.config.example.py`: it has two replacements and a guarded deletion. Keep every patch listed
with its reason in the site's README, and send each design-side fix upstream so the patch can be dropped later.
The config is executed as Python, so use only the repo's own reviewed config, never one that came with the
fetched export. A replacement counts as carried once it is on the page, so make each replacement (and each
original) unique on the page; a short one that also occurs elsewhere can hide a patch that is still needed.
An empty original or guard, or a guard on a replacement, fails as a bad patch.

For a deletion that removes content (a held claim, a link the site must not show, a stored-data call), add a fifth
element, a **guard**: a short phrase of that content. Without it, a design that only restyles the markup (say, a
font-family literal turned into a CSS variable) makes the exact original disappear, and the patch reports
"carried" while the content ships. With a guard, the patch counts as carried only once the guard phrase is gone
too; otherwise it fails for review. An applied deletion also fails when the phrase is still on the page
afterwards (a second, restyled copy). Pick a phrase that occurs nowhere else on the page.

## 3. Dry run, then sync

```sh
python3 scripts/sync_template.py <fetched-dir> <project-config.py> --dry-run
python3 scripts/sync_template.py <fetched-dir> <project-config.py>
```

Each patch is reported `applied`, `carried` (the template has it: drop the patch from the config and the README)
or `FAIL` (the original changed: review). Any `FAIL` writes nothing. A `carried` deletion without a guard deserves
a manual check that the content is really gone.

## 4. After the sync

- Diff the snapshot (`git diff --stat`): new shared files the page loads come in with it; drop any the page does
  not reference.
- Build and check the site locally at desktop and phone sizes before a PR, then deploy production only.
- Update the README's fetch date and source (artifact URL and version, or project), and the patch list.
