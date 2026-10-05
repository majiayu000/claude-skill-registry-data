---
name: ship
description: Full release pipeline — tests → coverage → review gate → version bump → CHANGELOG → commit → PR
when_to_use: "ship a release, full release pipeline, version bump, create PR, CHANGELOG update, release this feature — NOT for committing mid-session (use /commit)"
argument-hint: '[--dry-run] [--no-bump] [--no-pr]'
user_invocable: true
---

# /ship — Full Release Pipeline

Full release pipeline: tests → coverage → review gate → version bump → CHANGELOG → commit → PR.
Each step is a hard gate — failure stops the pipeline and reports clearly.

## After shipping

Run `/document-release` to sync README, CHANGELOG, and docs with the new release.
For web projects: run `/seo audit <url>` to verify no SEO regression from the release.
If running paid ads: run `/ads audit` to verify tracking pixels and conversion events still fire correctly after the release.
For blog projects: run `/blog audit` to check content health, quality scores, and AI citation readiness.
