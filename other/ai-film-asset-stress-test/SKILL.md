---
name: ai-film-asset-stress-test
description: Validate recurring AI-film character, wardrobe, prop, vehicle, scene, and state assets before multi-shot or batch generation without redesigning or generating them.
---

# AI Film Asset Stress Test

Authority: `validation_only`.

Use this Skill after DIRcreative has produced a candidate asset foundation and
before the asset enters repeated shots, group compositions, or batch generation.

## Ownership

- DIRcreative owns asset truth, state families, shot scope, approvals, and final
  project state.
- This Skill validates stability only. It does not redesign assets, generate
  media, approve on behalf of a user/client, or grant `visual_assets_complete`.
- A producer-authored receipt cannot certify its own output. Missing real output
  evidence remains `unverified`.

## Required packet

Read and validate the packet with:

- legacy v1: `docs/film-preproduction/schemas/ai-film-asset-stress-test.schema.json`
- split face/headless compatibility v2: `docs/film-preproduction/schemas/ai-film-asset-stress-test-v2.schema.json`
- unified character-sheet v3: `docs/film-preproduction/schemas/ai-film-asset-stress-test-v3.schema.json`
- `python3 scripts/ai_film_asset_stress_test.py validate <report> --artifact-root <root> --review-receipt <receipt> --review-signature <sig>`

The packet binds one or more asset/state descriptors, exact references and
rights, target model surface, intended shot classes/light, required co-cast/prop
combinations, and a configurable per-asset test matrix.

`certified` and `conditional` require a detached signature over the exact review
receipt. The authority and public-key SHA-256 must already exist in the
host-owned registry selected by `DIRCREATIVE_REVIEW_TRUST_REGISTRY` or
`~/.codex/dircreative/review-trust-registry.json`; the generic
CLI cannot select a new key or pin. The package registry is an empty compatibility fallback
until a host administrator configures reviewer actor, authority kind, allowed
purpose/source, key path, and key hash. The validator fails closed if
OpenSSL, the signature, or the configured detached key is missing. A second
producer-written JSON is not a trust root.

## Matrix policy

Choose cases from actual risk. High-risk characters normally cover face close-up,
full body, wide/FOV, target lighting, group composition, occlusion/prop
interaction, state variants, handedness and scale/topology. New recurring
clothed-human certification uses v3. Its headed default binds one physical master
sheet and follows the single owner contract in
`skills/dircreative/references/character-master-sheet.md`. This validator checks
schema, hashes, source/derivation roles, required cases, evidence and signed
review binding. It does not measure subject pixels or prove final exact-graphic
composite fidelity; those are external visual-review findings. This is a risk
profile, not a universal fixed attempt count.

Existing v1 and v2 reports remain verifiable under their original schemas but do
not gain v3 unified-sheet guarantees. Migration requires a new physical master,
view and derivation metadata, required v3 cases, fresh evidence and a new detached
review signature. Never auto-promote an older report.

Each reference has one primary role. Planning boards cannot become canonical
identity, topology, geography, or clean-frame truth.

Coverage is per asset, not a global union. Required co-cast/prop combinations
must be named by passing cases, every passing case needs its own real evidence,
and evidence IDs/output hashes cannot be reused across unrelated matrix cases.
Canonical asset bytes/version/path are verified separately from supporting
references, and a planning-only path/hash cannot be aliased under a canonical ID.

## Verdicts

- `certified`: independently reviewed evidence covers the complete intended
  scope with no blocked scope.
- `conditional`: evidence supports only the listed allowed scope and explicitly
  blocks the remainder.
- `rejected`: demonstrated deviation blocks the asset.
- `unverified`: evidence, matrix coverage, or independent review is missing.

Always return allowed/blocked shot scope, observed deviations, evidence hashes,
review source, and the smallest next action. Never equate a stress-test verdict
with installation, host adoption, media delivery, or customer approval.
