---
name: build-voice-assets
description: Build staged preset speech and locally consented voice cloning with private reference ancestry, exact spoken-text review and separate runtime disclosure and promotion.
engines: [AGNOSTIC]
---

# Build Voice Assets

## When to use

Use for preset speech or locally consented cloning. Route SFX/ambience to AUDIO and tracks to MUSIC. VOICE loads independently alongside visual work and does not select STYLE, ENGINE or a provider.

## Workflow

1. Resolve this skill and `resolve-media-pipeline.sh --modality preset-speech` or `consented-cloning`. Read shared MEDIA.md, optional VOICE.md and `.media/pipelines/voice/PIPELINE.md`. Configure only requested missing contracts. Contract/capability/receipt presence is not native readiness.
2. Use the linked strict schemas and non-authorizing examples to define exact spoken text, task purpose, explicit LOCAL/CLOUD provider, spatialization, loopIntent:false and finite budgets. LOCAL uses explicit native autoregressive sampling and cuda:0/bfloat16/no offload. Backend follows kind: CustomVoice preset or Base cloning; the coordinator owns IDs/output paths. Reject diffusion/fixed seconds, loops, editing, transcription and unsupported controls.
3. Cloning needs canonical project-local audio/transcript/rights/native-consent identities, distinct ignoring case, plus a fifth independent human consent-source identity. Keep exact private inputs and hashes in local task state. Rehash all sources; do not infer speaker identity or rights. Bind ordered references and exact purpose through typed `localUse`. Fresh generation requires current-task generation permission and native scope; QA-only consent additionally needs its matching existing bounded acceptance case. Never reset shared attempts or upgrade scope.
4. Use `voice-pipeline.sh brief`, `init`/`revise`, read-only `status`/`doctor` and dry-run `setup-plan`. Setup execution, license acceptance and synthesis need separate applicable authorization. Preserve failed/started versions and original shared media-state root. No command silently installs or changes provider/device/precision.
5. LOCAL dispatch delegates to verified Bubo. CLOUD preset speech accepts actual provenance import only; CLOUD cloning is unavailable under local-only consent. Stop an unavailable selected path and request direction; never upload private references or fall back. Historical import preserves original native task/scope/approvals and gives no new generation allowance.
6. `validate` rehashes native ancestry, exact text/sampling/RNG/EOS/code-frame accounting, raw 24000Hz mono metrics and zero measured allocator cleanup. Preserve intrinsic decoder clamp and reference decode/prefix-removal disclosures. No denoise/trim/normalization occurs. Native worker verification of decoded private bytes is not a reason to inspect private source media during implementation QA. Missing authoritative analysis remains ineligible.
7. Record actual complete-output human listening for spoken text, pronunciation, artifacts and preset/reference match, bound to current fingerprint/output identities and human source. Metadata/synthetic/history cannot certify current acceptance. Hand off through a compatible selected-engine owner with actual playback/load/dispose/spatialization and finite format/budget evidence.
8. Runtime use requires separate current task/purpose distribution/public-disclosure permission. Cloned outputs additionally need an explicit exact-output/reference-bound disclosure grant, separate from local/QA consent; a later grant may cover existing outputs without rewriting native history. Rehash every nested source. Promote/recover only with current technical/content/runtime reviews and separately authorized exact outputs/target through shared no-overwrite controls.

## Output

Return staged provenance and honest technical/content/target gaps. Public reports use nonidentifying summaries; private recordings, transcripts, conditioning, generated speech and their identifying hashes remain local. Source implementation or merge grants no real consent, generation, human acceptance, disclosure or promotion.
