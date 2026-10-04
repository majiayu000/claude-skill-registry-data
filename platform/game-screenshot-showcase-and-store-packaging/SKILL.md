---
name: game-screenshot-showcase-and-store-packaging
description: Use when a Unity team needs approved PlayMode screenshots, immutable capture evidence, reviewed showcase slides, or report-only store screenshot packaging without auto-upload, signing, or submission.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [unity]
  versions: [2019.4+, 2021.3+, 6000+]
  platforms: [windows, steam, ios, android, webgl]
metadata:
  studio:
    type: workflow
    lifecycle_stage: ship
    risk_level: medium
    packs: [content-production]
    side_effects: files
    artifact: screenshot-showcase-report.json
    required_evidence: [capture-plan, capture-record, showcase-deck, store-export-manifest]
    owner: HoaTV Studio
    reviewer: Producer
    maturity: experimental
    last_reviewed: 2026-08-21
    provenance:
      derived_from: none
      patterns_from:
        [
          conceptual inspiration: ParthJadhav/app-store-screenshots (MIT), no copied text or code,
          playtest-evidence,
          build-and-runtime-verification,
          unity-batchmode-build-verification,
          unity-ui-rendering-debugging,
          store-submission-checklist,
        ]
      copied_text: none
---
# Game Screenshot Showcase and Store Packaging

## Overview
Capture and package Unity screenshots through an approval-gated workflow: discover the target moments, propose the exact checklist, capture only after approval, review the images visually, and package approved outputs without overwriting raw evidence or taking storefront actions.

## Provenance
This workflow is conceptually inspired by ParthJadhav/app-store-screenshots (MIT). No source text or code was copied into this skill.

## When to use
Use for Unity PlayMode feature capture, showcase contact sheets, approved slide decks, and report-only screenshot packaging for Steam, mobile stores, or WebGL listings.

## When NOT to use
Do not use for qualitative playtest synthesis without capture/package scope; route that work to `playtest-evidence`. Do not use to upload assets, sign binaries, accept legal terms, log into storefront accounts, or press submit; route publication readiness to `store-submission-checklist`. If the core question is runtime execution proof, Unity build proof, or a missing HUD/widget, route to `build-and-runtime-verification`, `unity-batchmode-build-verification`, or `unity-ui-rendering-debugging`.

## Required inputs and context discovery
Collect the Unity project root, target scenes or entry points, feature beats to capture, viewport/device targets, locale, intended store/platform, approved evidence/output roots, privacy redaction rules, reviewer identity, and whether a Unity Editor or PlayMode runner is actually available.

## Safety and risk level
This workflow may write new evidence files and report-only HTML/JSON outputs, but it must never overwrite raw captures, delete rejected evidence, traverse outside approved roots, consume credentials, or perform upload/signing/submission. Redact or exclude player names, email addresses, account IDs, chats, or other sensitive content that appears in screenshots.

## Workflow
1. Discover.
   Completion criterion: the exact feature moments, scenes, capture roots, device targets, and no-touch paths are named, and adjacent concerns are routed to `playtest-evidence`, `build-and-runtime-verification`, `unity-batchmode-build-verification`, `unity-ui-rendering-debugging`, or `store-submission-checklist` when they are the real owner.
2. Propose the interactive checklist.
   Completion criterion: an explicit `capture-plan` is prepared with ordered flows, viewport, locale, timeout, reviewer, and approval state, and no capture starts before human approval.
3. Capture only after approval.
   Completion criterion: Unity Editor or PlayMode capture runs only after approval, raw files are preserved as immutable evidence, and each capture yields a `capture-record` with hash, byte size, dimensions, build/editor snapshot, runtime result, visual review placeholder, and limitations. If Unity Editor, PlayMode, or the approved runtime path is unavailable, this phase is `BLOCKED`; do not substitute old screenshots, mocked renders, or compile confidence.
4. Visual review.
   Completion criterion: approved and rejected captures remain traceable through `verify-capture` results and an HTML contact sheet, and runtime verdicts stay separate from visual verdicts. A visually strong image with weak runtime evidence is not a runtime PASS; a runtime PASS does not auto-approve composition, crops, or messaging.
5. Package.
   Completion criterion: only approved showcase selections become a `showcase-deck` and `store-export-manifest`, store readiness stays separate from runtime and visual verdicts, and packaging remains report-only with no resizing, upload, signing, or submission.

## Evidence and output contract
Produce or validate these artifacts:

- `capture-plan`: approved checklist and scope before execution.
- `capture-record`: immutable raw evidence for each image, including runtime and review status.
- `showcase-deck`: reviewed slide or slot selection built only from approved captures.
- `store-export-manifest`: report-only export/readiness manifest with hashes, required slots, missing slots, rejected slots, and human approval state.
- HTML contact sheet: deterministic visual review artifact that retains rejected and blocked records.

Record three separate verdict lanes in the final report:

- `runtime_verdict`: what Unity execution evidence proves.
- `visual_verdict`: what image review and composition approve or reject.
- `store_verdict`: what store-format/export readiness proves.

## Handoff contract
Record approved roots, project/build snapshot, checklist approval state, commands used, artifact paths, hashes, rejected capture IDs, privacy redactions, runtime limitations, store blockers, and the exact human-controlled next action.

## Pitfalls and anti-rationalization
- A beautiful screenshot is not runtime proof.
- An old screenshot is not acceptable fallback evidence for a blocked capture run.
- Rejected or blocked records must stay visible in review artifacts; do not hide them to simplify a deck.
- Store packaging readiness is not approval to upload or submit.
- Never replace source images in place to make the export look correct.

## Verification checklist
- [ ] Discovery named the approved roots, target moments, and routed neighboring work correctly.
- [ ] Capture did not start before checklist approval.
- [ ] Raw capture evidence stayed immutable and hashable.
- [ ] Runtime, visual, and store verdicts are separate.
- [ ] Rejected and blocked records remain visible in evidence.
- [ ] Packaging stayed report-only and human publication stayed blocked.

## References and scripts
Use the report-only helper commands:

- `python -B scripts/screenshot_showcase.py verify-capture <project-root> --record <capture-record.json>`
- `python -B scripts/screenshot_showcase.py contact-sheet --records <records.json> --output <review.html>`
- `python -B scripts/screenshot_showcase.py export-manifest --deck <showcase-deck.json> --platform <platform> --locale <locale> --output-root <dir>`

Load `references/commands.md` when the task needs concrete Unity Editor or PlayMode capture command templates, helper CLI invocations, or exact evidence fields and mutation boundaries.

Use `store-submission-checklist` for current storefront requirements, `build-and-runtime-verification` for command-bound runtime claims, `unity-batchmode-build-verification` for Unity build evidence, `unity-ui-rendering-debugging` for missing UI/render-order issues, and `playtest-evidence` when the task is about observed player behavior rather than capture/package production.
