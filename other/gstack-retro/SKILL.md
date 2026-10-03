---
name: retro
preamble-tier: 2
version: 2.0.0
description: Weekly engineering retrospective. (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
triggers:
  - weekly retro
  - what did we ship
  - engineering retrospective
gbrain:
  schema: 1
  context_queries:
    - id: prior-retros
      kind: filesystem
      # #2552: /retro writes .context/retros/*.json (repo-local; see the save
      # step below) — the old ~/.gstack/.../retros/*.md glob matched a
      # directory and extension nothing ever writes, so this query was dead.
      glob: ".context/retros/*.json"
      sort: mtime_desc
      limit: 5
      render_as: "## Prior retros for this project"
    - id: recent-timeline
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/timeline.jsonl"
      tail: 30
      render_as: "## Recent timeline events"
    - id: recent-learnings
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/learnings.jsonl"
      tail: 10
      render_as: "## Recent learnings"
---

This skill is the git submodule file `.cursor/vendor/gstack/retro/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-retro/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
