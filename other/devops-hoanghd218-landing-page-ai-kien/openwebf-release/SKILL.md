---
name: openwebf-release
description: DEPRECATED umbrella Skill (backward compatibility). Use only when release work spans deployment + cache headers + versioning + rollback. Prefer focused `openwebf-release-cdn-deploy` and `openwebf-release-versioning-rollback` Skills.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related
---

# OpenWebF Release Skill

## Deprecated

Prefer:
- `openwebf-release-cdn-deploy`
- `openwebf-release-versioning-rollback`

## Instructions

If this umbrella Skill is active, route to the appropriate focused release Skill based on trigger terms (CDN/provider vs versioning/rollback/rollout). Ensure store compliance when remote updates are involved.

If repo context is missing, start with `/webf:doctor` and then route to the focused Skill.

## Examples

- “Design a rollout and rollback plan for CDN-hosted WebF assets with cache-busting.”
