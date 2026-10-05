---
name: vault-canonical-promotion
description: Use when curated vault material may need to become stable canonical knowledge, or when an agent wants to update an existing canonical note without direct authority. Applies when promotion criteria, proposal files, registry updates, and merge safety matter.
---

# Vault Canonical Promotion

## Overview

This skill exists to stop agents from publishing working notes as official knowledge too early. It routes durable material through a promotion process instead of silent direct edits.

If your agent supports MCP, 优先 use the governance MCP server for proposal, queue, review, and apply operations.
Use this skill as the compatibility layer when MCP is unavailable.

## Promotion Conditions

The candidate should have:

- a resolved `topic_id`
- valid source lineage
- curation-level stability
- long-term reuse value
- a clear home in canonical knowledge

Read `references/promotion-criteria.md` before promoting.

## Standard Flow

1. Confirm the source note lives in `intake` or `curation`
2. Check whether canonical already exists for the topic
3. If canonical exists and you are not Hermes/human, prepare a proposal instead of overwriting
4. Add or update `promotion-queue.json`
5. Add ledger entry
6. Leave final merge to Hermes or a human

## Allowed Actions

- create promotion candidate
- update queue item
- prepare proposal note
- recommend canonical target path

## Disallowed Actions

- silent overwrite of canonical notes
- reclassifying raw notes as canonical without curation
- skipping queue update

## Common Mistakes

- treating polished wording as proof of canonical readiness
- publishing without checking for existing canonical home
- forgetting to record why this note deserves promotion
