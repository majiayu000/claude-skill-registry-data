---
name: build-music-assets
description: Build staged instrumental and supplied-lyric tracks through the independent MUSIC pipeline with exact lyric rights, native provenance, full-track listening and separate runtime promotion.
engines: [AGNOSTIC]
---

# Build Music Assets

## When to use

Use for instrumental and supplied-lyric music. Route sound effects/ambience to AUDIO and spoken speech/cloning to VOICE. MUSIC loads independently alongside the selected visual workflow without replacing STYLE.md.

## Workflow

1. Resolve this skill and `resolve-media-pipeline.sh --modality instrumental` or `supplied-lyrics`. Read optional MUSIC.md, shared MEDIA.md and `.media/pipelines/music/PIPELINE.md`. Configure only the requested missing contract. Configuration and advertised capabilities do not prove native/provider readiness.
2. Define an `hephaera-music-brief/v1` using the schema/examples. Record instrumental/song intent, purpose, caption with mood/instrumentation/structure, explicit provider, whole 10..600 second duration, variations, spatialization/loop intent, exact installation/settings and finite budgets. For supplied lyrics preserve exact UTF-8 text/order and source-backed `lyricsRights`; require supported language and exact per-item lyric hashes. Never write or revise lyrics automatically.
3. Use `music-pipeline.sh brief`, `init`/`revise` and read-only `status`/`doctor`. Preserve task/domain/asset/version identities and rejected/failed ancestry. Setup planning is dry-run; installation, license acceptance and generation are separate authorizations. Ordinary discovery loads no model.
4. LOCAL dispatch delegates the exact verified Bubo music request using cuda:0/bfloat16/no offload, guidance 1, 1..8 steps, nonnegative int32 seeds and the shared approval/attempt root. Planning LM, automatic lyrics, reference audio, stems, mastering/editing, normalization and fallback are disabled or unsupported. Current-task prompt and lyric generation permission are required. CLOUD uses actual provenance import; unavailable unattended execution never selects LOCAL.
5. `validate` rechecks exact native ancestry, build/catalogue identities, complete 48000Hz stereo output measurements, actual music/conditioning settings, disabled planning/normalization and disclosed cleanup. Keep raw amplitudes and threshold failures. Metadata proves neither acoustic lyric fidelity nor musical quality; missing authoritative analysis stays ineligible.
6. Record actual complete-track human listening for intended instrumental/vocal content, brief, artifacts and head/tail; songs require every supplied line reviewed. Intended loops require a separate actual seam verdict. Bind the complete current output set, fingerprint, human source, reviewer and reasons. An instrumental cannot satisfy a song; old/synthetic evidence is not current acceptance.
7. Hand off through the compatible selected-engine owner using actual playback, load/dispose, spatialization/loop and format/budget evidence. Record separate current-task distribution permission and rehash its source plus lyric-rights sources. Generation-only MUSIC requires no invented style or engine.
8. Promote only after current technical/content/runtime evidence and separate explicit exact-output/target authorization. Shared no-overwrite copying/recovery retains intents and failures. Missing permission/readiness/evidence keeps outputs staged; source delivery grants no asset promotion.

## Output

- Immutable briefs/versions with exact lyrics, source rights, provider and native identities.
- Staged candidates, technical reports and actual complete-track/line/loop review.
- Separately reviewed target handoff and explicitly authorized promotion receipt when requested.

## Guardrails

- Preserve one physical approval-bound native ledger across domains/tasks/workspaces; never replenish an existing candidate/revision allowance.
- Preserve original tracks and lyrics. Do not infer generation/distribution permission from license metadata or historical approval.
- Do not fabricate human verdicts, CUDA readiness, allocator/driver measurements or quality claims from hashes.
- Stop an unavailable selected path; no silent provider, device, precision, backend or workflow fallback.
