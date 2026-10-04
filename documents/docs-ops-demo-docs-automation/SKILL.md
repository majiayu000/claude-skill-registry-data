---
name: docs-ops-demo-docs-automation
description: Use when running docs automation workflows for docs-ops-demo.
---

# docs-ops-demo-docs-automation

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Documentation automation workflows for keeping project docs current.

## Workflow
- Scan README, docs, package metadata, and generated agent files
- Identify missing, stale, or duplicated documentation
- Update the smallest useful set of docs
- Run doc-related checks or explain why none exist

## Commands
- install: `npm install`
- test: `npm test`
- docs: `npm run docs`
- docs:check: `npm run docs:check`

## Principles
- Prefer source-of-truth files over stale summaries
- Keep generated documentation concise and easy to review
- Link commands, files, and examples that readers can verify
