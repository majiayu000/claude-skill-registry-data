---
name: clarila-capture
description: "Capture actual screenshots or recordings for a specified UI flow and candidate. Use for before/after visual evidence, not generated mockups or a behavioral PASS verdict."
---

# Capture trustworthy visual evidence

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the exact screen/flow, fixture, viewport/device, source and installed artifact. Verify permission to use the target and preserve existing device ownership.
2. For before evidence, execute the original scenario before edits. Do not manufacture historical before media after the source changed.
3. For iOS/Android screenshots or recordings, read the [mobile capture reference](references/mobile.md). Capture real UI with supported browser, simulator or device tools. Inspect the images and relevant video frames. Preserve originals without editing pixels to create a result.
4. For after evidence, use the matching screen/flow and identified candidate. Every UI change includes before/after screenshots. Interactive changes also include a short real recording of the original action and observed result, even when layout/styles are unchanged; static-only changes need no redundant clip. Existing Clarila limits are muted clips up to 20 seconds and 8 MiB, at most two per task unless explicitly revised.
5. Retain media hashes, capture method, source/artifact/fixture and observations. For an authorized Clarila UI workflow, upload a useful captioned batch to its verified Clarila-server thread through clarila-discord. Read back actual message and attachment IDs, names and media metadata. Local paths or a claim that captures exist do not complete delivery. If capture/upload is unavailable, retain the files and report the exact missing capability; do not mark capture delivered.

## Check comparison and delivery

Retain a compact manifest associating each before/after file with its source, artifact, fixture, viewport/device and action. Check that the compared files exercise the same acceptance scenario. Record a viewport, fixture or artifact mismatch as a specific comparison gap.

Read back the uploaded batch and inspect its usable media. Match message/attachment identity, filename, media type and dimensions or duration to the intended evidence. A host may transform media, so retain original hashes and describe the verified remote properties separately.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return inspected real media, provenance, observations and verified Clarila message/attachment receipts, or the concrete delivery gap. Capture alone does not establish complete acceptance.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/evidence.md) when performing this responsibility. For a frontend verification page, use the capture and delivery checklist in [interactive web evidence](../clarila-verify/references/interactive-web-evidence.md). Inspect exported clips for natural pacing and visible results.
