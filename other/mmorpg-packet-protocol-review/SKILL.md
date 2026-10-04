---
name: mmorpg-packet-protocol-review
description: Use when a C++ server and Unity client protocol manifest or wire compatibility review covers packet version negotiation, numeric opcode registry, byte layout order, direction, and request-response pairing.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: review
    risk_level: read-only
    packs: [cpp-lua-mmorpg]
    side_effects: none
    artifact: packet-protocol-review.json
    required_evidence: [client-manifest, server-manifest, mismatch-list]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [lua-client-server-contract-audit, registry/capabilities.yaml domain catalog]
      copied_text: none
---
# MMORPG Packet Protocol Review

## Overview
Compare versioned protocol manifests across clients and servers without sending traffic or editing generated packet definitions.

## When to use
Use for opcode drift, packet-version mismatch, direction errors, typed field order changes, request-response mismatches, or mixed client/server releases.

## When NOT to use
Do not use for exploit testing, live packet replay, generic Lua copy auditing, or runtime service control.

## Required inputs and context discovery
Collect protocol versions, source and generated paths, packet names, opcodes, direction, authority, ordered typed fields, response pairing, build compatibility matrix, and no-touch generated outputs.

## Safety and risk level
Read-only. Never send crafted packets, start servers, capture credentials, or hand-edit generated protocol outputs.

## Workflow
1. Identify authoritative protocol sources and version ownership.
   Completion criterion: every manifest is source, generated, copy, or unknown.
2. Normalize packet definitions into deterministic ordered structures.
   Completion criterion: parse ambiguity is reported rather than guessed.
3. Compare versions, presence, opcode, direction, authority, fields, and pairing.
   Completion criterion: each mismatch cites both sides.
4. Map mismatches to supported client/server build combinations.
   Completion criterion: compatibility risk is explicit.
5. Propose source-first changes and regression fixtures.
   Completion criterion: no live traffic or generated hand edit is required.

## Evidence and output contract
Produce `packet-protocol-review.json` with versions, compatibility, packet mismatches, source authority, limitations, and recommended source fixes.

## Handoff contract
Record manifest/build paths, supported versions, mismatches, generated files, parsing limits, and next source-first owner.

## Pitfalls and anti-rationalization
- Matching packet names do not prove compatibility.
- Field order is part of a binary contract.
- Do not test static drift by sending packets to production.
- Generated copies are not automatically authoritative.

## Verification checklist
- [ ] Protocol versions are explicit.
- [ ] Ordered typed fields are compared.
- [ ] Direction, authority, and pairing are checked.
- [ ] Compatibility matrix is recorded.
- [ ] No traffic or generated file was changed.

## References and scripts
Use the bundled [scripts/protocol_review.py](scripts/protocol_review.py) with its [scripts/lua_contract_audit.py](scripts/lua_contract_audit.py) dependency and project-local protocol generation maps.
