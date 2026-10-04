---
name: scbe-spiralverse-intent-auth
description: Implement and operate Spiralverse intent-authenticated communication for HYDRA/SCBE using six sacred tongues, governance gates, and signed audit packets.
---

<!-- change-note: 2026-02-20 Documentation-only note for skill maintenance; no runtime/code-path impact. -->

# scbe-spiralverse-intent-auth

## Purpose
Implement and operate Spiralverse intent-authenticated communication for HYDRA/SCBE using the six sacred tongues (KO/AV/RU/CA/UM/DR), governance gates, and signed audit packets.

## When to use
- User asks for AI-to-AI governed comms in SCBE.
- User asks for conlang-driven intent packets tied to crypto/auth.
- User asks to wire Layer 5/Layer 9 comm flow into swarm/HYDRA.

## Inputs expected
- Intent text
- Tongue or tongue sequence
- Recipients / signer set
- Governance thresholds (if custom)

## Core workflow
1. Build tongue packet from intent + metadata.
2. Encode and shuffle deterministically.
3. Run SCBE 14-layer governance gate.
4. If ALLOW: sign packet (single or multi-sig), verify signatures, emit audit record.
5. If QUARANTINE/DENY: emit quarantine audit record and do not execute action.
6. Persist packet + decision in hub/ledger logs.

## Output contract
- `status`: `ALLOW|QUARANTINE|DENY`
- `decision_record`
- `packet`
- `signature_verification`
- `governance_metrics`

## Safety checks
- Never execute when governance decision is not `ALLOW`.
- Require multi-sig for high-risk operations.
- Log all failures with deterministic reason fields.

## References
- `references/` for protocol notes and examples.
- `scripts/` for local helpers.

## Notes
Start with minimal deterministic behavior first, then layer additional heuristics.
