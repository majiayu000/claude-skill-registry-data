---
name: ls-paddle-agent-skills
description: Inventory wrapper for Paddle Billing agent skills. Use when planning
  Paddle checkout, subscriptions, webhooks, pricing, portal, or sandbox work.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: wrapper
    source_url: https://github.com/PaddleHQ/paddle-agent-skills
    source_path: <repository inventory>
    source_commit: 72e6fdf6ec313ea773595e5bb1fbb665fa89bbc8
    source_ref: main
    source_sha256: 59cf54a9655e0228732011e229580fe7e4c2b4ac7da64ed45c4b11bc5aa0f9c9
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Paddle Billing Agent Skills

Use this skill when working on Paddle Billing agent skills tasks.

## Workflow

- Treat Paddle API keys, webhook secrets, customer data, and billing state as sensitive production surfaces.
- Select one narrow upstream skill for future import only after checking overlap with existing payment or billing skills.
- Validate sandbox mode, webhook signature verification, idempotency, and rollback behavior before production changes.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## Upstream Coverage

See [upstream coverage](./references/upstream-coverage.md) for the compact inventory captured during this import wave.

## Provenance

- Source: `https://github.com/PaddleHQ/paddle-agent-skills`
- Ref: `main` at `72e6fdf6ec313ea773595e5bb1fbb665fa89bbc8`
- Source path: `<repository inventory>`
- License classification: `Apache-2.0`
- Source SHA-256: `59cf54a9655e0228732011e229580fe7e4c2b4ac7da64ed45c4b11bc5aa0f9c9`
