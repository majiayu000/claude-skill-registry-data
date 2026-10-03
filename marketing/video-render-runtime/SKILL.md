---
name: video-render-runtime
description: Execute provider-neutral Aries video render briefs through Hermes.
metadata:
  hermes:
    tags: [aries, video, media, rendering]
    capabilities: [video-generation, artifact-contracts, callback-projection]
---

# Video Render Runtime

Use this skill when an Aries social-content workflow requests `video.generate` media work.

## Ownership boundary

Aries owns the brief, run/job/tenant ownership, callback destination, approval gates, and durable artifact projection. Hermes owns provider and model selection, credentials, generation execution, retries, and raw provider responses. Never add provider or model selectors to an Aries submission.

## Required flow

1. Validate the brief against `../../specs/video_job_contract_spec.v2.json`.
2. Accept only public HTTPS source assets. Reject credentials, traversal, local/private/link-local/unspecified destinations, and redirect chains that pivot away from public destinations.
3. Submit the work through the shared `HermesRunSubmissionSchema` envelope with a production `mkt_<uuid>` job id and matching callback ownership fields.
4. Emit terminal results only through the shared `HermesRunCallbackPayloadSchema` callback shape. A failed event must include a meaningful `error` object.
5. Report rendered video artifacts with `video/mp4`, byte count, dimensions when known, duration when known, platform slug, and family id.
6. Do not publish directly. Aries ingests artifacts into durable storage and applies the approval gate.

## Failure behavior

Fail closed. If no reported video artifact can be ingested, return a terminal failed callback rather than a completed or approval-required callback with an empty result. Never expose host paths, cache mount paths, tokens, tenant identifiers, or raw callback metadata in dashboard display fields.
