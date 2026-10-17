---
name: release-notes-writer
description: |
  Generate ship-ready release notes from specs and tickets. Use this skill when:
  - A release is being prepared and you need user-facing release notes
  - You need internal (engineering) release notes for a deployment
  - You want to generate release notes from completed specs or tickets
---

# Release Notes Writer

Generate structured release notes for each release cycle. Produces both **user-facing** (what changed and why it matters) and **internal** (technical changes, migration steps) release notes.

## Workflow

1. **Identify release scope** — List the features/fixes included
2. **Read source specs** — Read relevant spec files
3. **Read tickets** — If available, read completed tickets for the release
4. **Categorize changes** — Group into: New Features, Enhancements, Bug Fixes, Known Issues
5. **Write user-facing notes** — What changed, why it matters, in plain language
6. **Write internal notes** — Technical changes, migration steps, config changes
7. **Output** — Write to file

## User-Facing Release Notes

```markdown
# [Product Name] — Release Notes {version}

**Release Date:** {DD-MM-YYYY}
**Environment:** {Production / Staging / UAT}

## What's New

### {Feature Name}
{1-2 sentence description of what the feature does and why it matters.}

**Highlights:**
- {Key capability 1}
- {Key capability 2}

## Enhancements

### {Enhancement Name}
{What improved and why it's better now.}

| Before | After |
|--------|-------|
| {Old behavior} | {New behavior} |

## Bug Fixes

| Issue | Fix | Impact |
|-------|-----|--------|
| {description} | {what was fixed} | {who is affected} |

## Known Issues

| Issue | Workaround | Expected Fix |
|-------|-----------|-------------|
| {description} | {workaround} | {target version} |
```

## Internal Release Notes

```markdown
# Internal Release Notes — {version}

**Release Date:** {DD-MM-YYYY}
**Release Manager:** [your name]
**Deployment Type:** {Rolling / Blue-Green / Canary}

## Changes by Service

| Ticket | Type | Summary | Breaking? |
|--------|------|---------|-----------|
| {KEY-123} | Feature | {Summary} | No |

## Configuration Changes

| Config Key | Old Value | New Value | Service | Notes |
|-----------|-----------|-----------|---------|-------|

## Database Migrations

| Migration | Description | Reversible? | Duration |
|-----------|-------------|-------------|----------|

## Rollback Plan
{Steps to rollback if critical issues found}

## Monitoring Checklist

| Metric | Expected | Alert Threshold | Dashboard |
|--------|----------|-----------------|-----------|
```

## Writing Guidelines

### User-Facing
1. **Lead with benefits, not features** — "You can now track X" not "Added X API"
2. **Use plain language** — No technical jargon
3. **Be specific** — "Reports now show time per topic" not "Improved reports"
4. **Acknowledge bug fixes honestly**

### Internal
1. **Be precise** — Include ticket numbers, endpoint paths, config keys
2. **Flag breaking changes prominently**
3. **Include rollback steps**
4. **Reference monitoring dashboards**

## Anti-Patterns

- Don't write "various improvements" — be specific
- Don't skip the rollback plan for internal notes
- Don't use technical jargon in user-facing notes
- Don't forget known issues — transparency builds trust

## Quality Checklist

- [ ] User-facing notes use plain language
- [ ] Every change categorized (feature/enhancement/bug fix)
- [ ] Internal notes include ticket numbers
- [ ] Rollback plan documented
- [ ] Breaking changes flagged
- [ ] Known issues listed
