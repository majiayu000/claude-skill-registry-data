---
name: gz-ontology
description: Use to sweep the governance shape, trace a node's lineage, diff against the last sweep, or read its blast radius.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "0.1.2"
model: haiku
---

# gz ontology

## Overview

Wield the `gz ontology` read-only sonar (ADR-0.32.0) to image the actual shape
of governance lineage instead of reasoning from stale or partial docs. The
ontology is a Tier-B derived projection — never authority — rebuilt from L1
canon and the L2 ledger. Every verb is read-only and never writes graph state
(Boundary Invariant #2); the only filesystem write is the regenerable
`.gzkit/ontology/last_sweep.json` diff-baseline cache.

## Output Contract

Human-readable tables and provenance lines by default; `--json` for
machine-readable output (including the rebuild-fidelity self-report); `--dot`
for a graphviz rendering.

## Workflow

1. Confirm the node id(s) of interest from `gz state` or the ledger.
2. Image the whole current shape and surface STRUCTURAL seams:

   ```bash
   uv run gz ontology sense
   uv run gz ontology sense --json    # + rebuild-fidelity self-report
   ```

3. Walk one node's vertical lineage + lateral proof with edge provenance:

   ```bash
   uv run gz ontology trace <ID>
   ```

4. Before acting at the airlock, diff the shape versus the last sweep — the
   re-sense gate:

   ```bash
   uv run gz ontology resense
   ```

5. Run the fast contacts-only STRUCTURAL seam check, or read a node's
   downstream blast-radius:

   ```bash
   uv run gz ontology seams
   uv run gz ontology reach <ID>
   ```

## Boundaries

- `sense` images STRUCTURAL coverage only and never claims semantic
  completeness (Boundary Invariant #3). Semantic-seam recall is deferred to
  RECALL / Phase-4 (L3-advisory).
- `sense`, `seams`, and `resense` always exit 0 — the sonar never gates.
  `trace` and `reach` exit 1 on an unknown node id.
- The ontology is a Layer-3 derived view. It never gates a `gz validate` scope,
  gate, or closeout (state-doctrine Rule 5).

## Reference

- Manpage: [`gz ontology`](../../docs/user/manpages/ontology.md)
- Parent ADR: `ADR-0.32.0-gzkit-ontology`
