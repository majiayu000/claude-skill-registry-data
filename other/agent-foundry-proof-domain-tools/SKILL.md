---
name: agent-foundry-proof-domain-tools
description: "Add owner-scoped durable operational records and safe OpenAI Agents SDK tools to an AgentFoundry proof. Use after agent-foundry-proof-foundation when the product manages bookings, CRM records, orders, inventory, tasks, approvals, work orders, or another shared mutable domain rather than only chat or generated artifacts."
---

# AgentFoundry Proof Domain Tools

## Purpose

Apply a reusable secure domain-data overlay, then replace its generic record with the smallest real product schema. This skill owns operational records and mutations; use `agent-foundry-artifact-ui` separately when the agent also produces a durable presentation artifact.

## Prerequisites

Require a project created by `agent-foundry-proof-foundation` with `.agentfoundry-proof.json`. Read `references/domain-overlay-contract.md` before changing the schema, repository, or tool permissions.

## Apply The Overlay

```sh
node <skill-dir>/scripts/apply-domain-overlay.mjs \
  --project <proof-directory> \
  --domain-name <lower_snake_case_noun> \
  --domain-swift <UpperCamelCaseName> \
  --collection <lowerCamelCaseCollection>
```

Do not read or regenerate the assets unless diagnosing the overlay. The script refuses overwrites and records the capability in the proof manifest.

## Product Customization

Immediately replace the generic `title`, `note`, and statuses with the product's validated fields and invariants. Rename tool functions to user-workflow verbs such as `findAppointmentSlots`, `confirmBooking`, `updateCaseStatus`, or `reserveInventory`; never expose arbitrary Firestore read/write tools.

Wire HTTP endpoints and the agent's tool list explicitly. Owner or organization identity comes only from verified backend context. Add product queries and indexes, transaction checks, idempotency keys, audit fields, and confirmation gates required by the workflow.

The bundled Swift client is an injectable boundary, not a reason to import Firebase into a feature module. Implement its live transport in the platform layer and add real empty/loading/error/conflict states to the product surface under `agent-foundry-design`.

## Verification

Test at least:

- cross-owner access is rejected;
- duplicate mutation ids return one logical result;
- stale expected versions fail without lost updates;
- destructive/external operations require confirmation;
- backend build and iOS decoding/build pass;
- records restore after relaunch through backend-owned state.

Run the foundation validator after applying the overlay. Do not call the domain contour production-ready while its generic schema or generic tool names remain.
