---
name: lua-client-server-contract-audit
description: Use when normalized Lua client/server RPC contract copies or generated protocol tables disagree on opcode, request-response fields, types, ordering, or source authority.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [lua-5.1+]
  platforms: [windows, linux]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: verify
    risk_level: read-only
    packs: [cpp-lua-mmorpg]
    side_effects: none
    artifact: lua-contract-audit.json
    required_evidence: [client-contract, server-contract, mismatch-list]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [sanitized client-server synchronization map, source-to-generated ownership]
      copied_text: none
---
# Lua Client Server Contract Audit

## Overview
Compare normalized client and server protocol contracts without editing either copy, then identify missing packets, opcode drift, field drift, and authority ambiguity.

## When to use
Use for Lua packet failures, RPC mismatch, silent request drops, wrong opcodes, missing response fields, duplicated protocol tables, or client/server copy drift.

## When NOT to use
Do not use for translation text authority, generic localization keys, or runtime network capture that requires service control or credentials.

## Required inputs and context discovery
Collect authoritative and copied protocol paths, generation pipeline, packet names, opcodes, field order/types, request/response direction, client/server versions, and no-touch generated paths.

## Safety and risk level
Read-only. Never edit generated protocol copies directly, send live exploit packets, start servers, or mutate network state during the audit.

## Workflow
1. Identify source-of-truth and generated/copied protocol files.
   Completion criterion: every compared file is labeled source, generated, copy, or unknown.
2. Normalize packet names, opcodes, direction, and fields into deterministic maps.
   Completion criterion: parsing ambiguity is reported rather than guessed.
3. Compare presence, opcode, field names/order/types, and request/response pairing.
   Completion criterion: mismatches cite both client and server paths.
4. Trace the generation or synchronization path for each mismatch.
   Completion criterion: the correct editable source is identified or BLOCKED.
5. Propose source-first fixes and regression fixtures without mutating live services.
   Completion criterion: generated copies are never hand-edited.

## Evidence and output contract
Produce `lua-contract-audit.json` with source/copy classification, missing packets, opcode mismatches, field mismatches, authority, generation path, limitations, and recommended source fixes.

## Handoff contract
Record client/server paths, versions, source authority, mismatches, generated no-touch files, parsing limitations, and next source-first action.

## Pitfalls and anti-rationalization
- Same packet name does not prove same opcode or fields.
- Copy synchronization should not be fixed in every destination manually.
- Do not treat localized labels as protocol fields.
- Do not send packets to prove a static contract mismatch.

## Verification checklist
- [ ] Source and copies are classified.
- [ ] Packet presence, opcodes, and fields were compared.
- [ ] Mismatches cite both sides.
- [ ] Generated files remain untouched.
- [ ] Source-first regression plan exists.

## References and scripts
Use the bundled [scripts/lua_contract_audit.py](scripts/lua_contract_audit.py) on normalized JSON exports and project-local generation maps for authority.
