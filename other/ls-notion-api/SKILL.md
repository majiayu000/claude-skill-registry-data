---
name: ls-notion-api
description: Guide Notion API integrations. Use for databases, pages, blocks, OAuth,
  webhooks, internal integrations, and workspace automation.
metadata:
  version: '1.0'
---

# Notion Api

Use this skill when working on Notion API tasks.

## Workflow

- Choose internal integration vs OAuth, then verify scopes, shared pages/databases, rate limits, and pagination.
- Keep Notion tokens and workspace data out of source, logs, screenshots, and generated examples.
- Validate block/database schemas, rich-text handling, idempotency, and retry behavior for automations.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source classification: `official-docs-reference`
- This is a LocalSetup-native skill written from project workflow requirements and public/official documentation routing.
