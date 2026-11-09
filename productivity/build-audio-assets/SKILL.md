---
name: build-audio-assets
description: Build staged game sound effects and ambience through the independent AUDIO pipeline with explicit providers, native provenance, full listening and loop review, and separate runtime promotion.
engines: [AGNOSTIC]
---

# Build Audio Assets

## When to use

Use for game/effect sounds and ambience. Route instrumental or supplied-lyric tracks to MUSIC and spoken speech/cloning to VOICE. AUDIO loads alongside them and the selected visual workflow without replacing STYLE.md.

## Workflow

1. Resolve this skill and `resolve-media-pipeline.sh --modality sfx` or `ambience`. Read the optional AUDIO.md, shared MEDIA.md and `.media/pipelines/audio/PIPELINE.md`. Configure only the requested missing domain contract; absent unrelated domains stay optional. Native/provider readiness is separate from configuration.
2. Define an `hephaera-audio-brief/v1` using the audio schema/examples: purpose/event/environment, SFX/ambience, explicit provider, bounded duration/variants, spatialization and loop intent, exact rights/installation/settings and finite budgets. Reject unsupported controls or long local ambience before attempts; never tile, clip duration, normalize, downmix or change providers implicitly.
3. Use `audio-pipeline.sh brief`, `init`/`revise` and read-only `status`/`doctor`. Keep immutable task/domain/asset/version state and original names. Setup planning is dry-run; tool/model installation, license acceptance and generation are distinct authorizations. Ordinary discovery loads no model.
4. LOCAL generation delegates the exact native SFX request through verified Bubo, preserving its shared approval-state root, candidate/revision claims, supported bounded controls and current installation/license checks. Bubo owns synthesis, decoding, models and GPU/process ownership. CLOUD uses actual provenance import; unavailable unattended execution does not select LOCAL.
5. `validate` rechecks exact native request/result/context/output ancestry and measured duration/rate/channels/bytes/peak/RMS/clipping/silence. Preserve original amplitude and disclose failed thresholds and unavailable LUFS/loop/memory counters. Missing compatible imported analysis remains ineligible; a requested setting is not a measurement.
6. Record actual complete-output human review for intended effect/texture, artifacts, unwanted speech/music and head/tail. Accepted intended loops require actual seam review. Bind the current full output set, brief, human source, reviewer, verdict and reasons. Historical or synthetic evidence is never a new listening verdict.
7. Hand off through the selected compatible engine owner with actual playback, load/dispose, spatialization/loop and codec/rate/channel/duration/size evidence. Record separate current-task distribution-rights assertions and nested source hashes. Generation-only AUDIO requires no invented visual style or engine.
8. Promote only after current technical/content/runtime evidence and explicit exact-output/target authorization. The shared executor owns no-overwrite copying and retained recovery evidence. Missing target evidence keeps outputs staged; source merges grant no asset promotion.

## Output

- An immutable brief/version with explicit rights, provider and native identities.
- Staged candidates, current technical observations and actual complete listening/loop reviews.
- Separately reviewed target handoff and explicitly authorized promotion receipt, when requested.

## Guardrails

- Do not turn original QA consent, license metadata or an accepted historical sample into fresh generation/distribution permission.
- Keep all started attempts and original outputs; changing task/workspace/provider never replenishes native allowances.
- Do not fabricate human acceptance, analysis, CUDA readiness or driver-memory observations. Metadata hashes establish identity, not the truth of rights or acoustic judgment.
- Stop the selected execution path when unavailable; no silent provider, device, precision, backend or workflow fallback.
