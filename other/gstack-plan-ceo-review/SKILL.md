---
name: plan-ceo-review
preamble-tier: 3
version: 1.0.0
description: CEO/founder-mode plan review. (gstack)
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - WebSearch
triggers:
  - think bigger
  - expand scope
  - strategy review
  - rethink this plan
gbrain:
  schema: 1
  context_queries:
    - id: prior-ceo-plans
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/ceo-plans/*.md"
      sort: mtime_desc
      limit: 5
      render_as: "## Prior CEO plans for this project"
    - id: recent-design-docs
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/*-design-*.md"
      sort: mtime_desc
      limit: 3
      render_as: "## Recent design docs for this project"
    - id: recent-reviews
      kind: list
      filter:
        type: timeline
        tags_contains: "repo:{repo_slug}"
        content_contains: "plan-ceo-review"
      sort: updated_at_desc
      limit: 5
      render_as: "## Recent CEO review activity"
---

This skill is the git submodule file `.cursor/vendor/gstack/plan-ceo-review/SKILL.md`. Read that file now and follow it in full. This stub exists so Cursor discovers the skill under `.cursor/skills/gstack-plan-ceo-review/`. Update: `git submodule update --remote` on the vendor checkout, then commit the new pin.
