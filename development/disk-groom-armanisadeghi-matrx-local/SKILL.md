---
name: disk-groom
type: Skill
title: "disk-groom — leftover Docker builds and agent worktrees"
description: "Permanent-delete grooming for leftover Docker builds, agent worktrees, and .next caches. Use when creating or finishing a git worktree, after a local docker build, when the disk is full, or when /tmp or .wt trees were left behind."
tags: [operations, docker, worktrees, disk]
timestamp: 2026-09-19T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/disk-groom/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# disk-groom — leftover Docker builds and agent worktrees

The disk fills because agents build Docker images 20–30 times a day and
leave worktrees / `.next` trees behind. Deletes are permanent. Never
Trash.

Read the register: `common-docs/operations/disk-grooming.md`.

## When you create a worktree

1. Put it at `<repo>/.wt/<slug>` only.
2. Register it:
   `python3 /Users/armanisadeghi/code/common-docs/meta/scripts/disk-groom/groom.py register <path> --purpose "<why>" --ttl-hours 24`
3. When the task ends, `groom.py remove <path>`. Not Finder. Not Trash.

## When you build a Docker image locally

After the build (or after compose up):

`python3 /Users/armanisadeghi/code/common-docs/meta/scripts/disk-groom/groom.py docker --apply`

That keeps running containers and prunes unused images plus BuildKit
cache down to 8 GB. Old SHA tags from the last twenty pushes are the
thing that filled a 4 TB disk.

## When the disk is tight

`python3 /Users/armanisadeghi/code/common-docs/meta/scripts/disk-groom/groom.py daily --apply`

Daily launchd already runs this at 04:15. Do not invent a second
cleaner. Do not `mv` anything to `~/.Trash`.
