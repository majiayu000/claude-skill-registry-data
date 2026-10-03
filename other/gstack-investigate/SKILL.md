---
name: investigate
preamble-tier: 2
version: 1.0.0
description: Systematic debugging with root cause investigation. (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
triggers:
  - debug this
  - fix this bug
  - why is this broken
  - root cause analysis
  - investigate this error
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: 'bash -c ''S="$HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"; [ -x "$S" ] && exec bash "$S"; exit 0'''
          statusMessage: "Checking debug scope boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: 'bash -c ''S="$HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"; [ -x "$S" ] && exec bash "$S"; exit 0'''
          statusMessage: "Checking debug scope boundary..."
gbrain:
  schema: 1
  context_queries:
    - id: prior-investigations
      kind: list
      filter:
        type: timeline
        tags_contains: "repo:{repo_slug}"
        content_contains: "investigate"
      sort: updated_at_desc
      limit: 5
      render_as: "## Prior investigations in this repo"
    - id: project-learnings
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/learnings.jsonl"
      tail: 10
      render_as: "## Recent learnings (patterns + pitfalls)"
    - id: recent-eureka
      kind: filesystem
      glob: "~/.gstack/analytics/eureka.jsonl"
      tail: 5
      render_as: "## Recent eureka moments (cross-project)"
---

This skill is the git submodule file `.cursor/vendor/gstack/investigate/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-investigate/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
