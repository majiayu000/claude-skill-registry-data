---
name: localization-authority-audit
description: Use when auditing localization source authority, generated copies, translation keys, missing or extra entries, mismatched text, encoding, mojibake, or client and server localization drift.
version: 0.2.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: verify
    risk_level: read-only
    packs: [unity, cpp-lua-mmorpg]
    side_effects: none
    artifact: localization-audit.json
    required_evidence: [authority-map, copy-map, mismatch-list]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-17
    provenance:
      derived_from: none
      patterns_from: [Hermes localization promotion source unavailable locally BLOCKED, sanitized copy synchronization fixture]
      copied_text: none
---
# Localization Authority Audit

## Overview
Identify the localization source of truth and compare every generated or copied map without rewriting multilingual data or masking encoding problems.

## When to use
Use for missing keys, extra keys, stale translations, client/server text drift, generated localization copies, encoding mismatches, UTF-8 versus legacy encodings, or mojibake.

## When NOT to use
Do not use for Lua packet/RPC field contracts or bulk encoding conversion without project-specific approval and backup.

## Required inputs and context discovery
Collect authority path, copy/generated paths, generation pipeline, locale list, key format, encoding evidence, fallback behavior, runtime owner, and protected vendor/generated data.

## Safety and risk level
Read-only audit first. Never bulk-convert encodings, normalize multilingual text, or edit generated copies before source authority and backup are verified.

## Workflow
1. Identify source authority, generated copies, runtime consumers, and fallback order.
   Completion criterion: unknown authority remains BLOCKED.
2. Verify file encodings with evidence before decoding or comparing text.
   Completion criterion: mojibake is not mistaken for a translation difference.
3. Normalize keys without changing source text and compare missing, extra, and mismatched entries.
   Completion criterion: every finding cites authority and copy locations.
4. Trace generation or copy synchronization for stale outputs.
   Completion criterion: the editable source and regeneration path are known.
5. Propose source-first fixes, targeted encoding handling, and verification fixtures.
   Completion criterion: no bulk conversion or generated-file hand edit is proposed without safeguards.

## Evidence and output contract
Produce `localization-audit.json` with authority, encodings, locales, missing/extra/mismatched keys, generation paths, runtime fallback, limitations, and source-first recommendations.

## Handoff contract
Record authority and copy paths, encoding evidence, key mismatches, generated no-touch files, unresolved locale ownership, and next safe action.

## Pitfalls and anti-rationalization
- Similar-looking text may be encoded differently.
- Do not “fix mojibake” through bulk replacement.
- Generated copies are not the authority unless explicitly verified.
- Missing runtime access is BLOCKED for live rendering confirmation.

## Verification checklist
- [ ] Authority and copies are classified.
- [ ] Encodings were checked before comparison.
- [ ] Missing, extra, and mismatched keys are separate.
- [ ] Generation paths remain source-first.
- [ ] No bulk encoding mutation occurred.

## References and scripts
Use the bundled [scripts/localization_audit.py](scripts/localization_audit.py) on normalized maps and project-local copy/generation documentation.
