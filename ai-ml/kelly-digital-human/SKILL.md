---
name: kelly-digital-human
description: "Digital-human implementation and demo skill for choosing, prototyping, and QA-ing low-cost 2D photoreal digital humans and high-control 3D custom digital humans. Use when the user wants a digital-human avatar, AI host, customer-service presenter, multimodal voice-to-lip-sync video stream, vendor comparison for services such as Silicon Intelligence / Tencent Zhiying / ZEGO-like real-time providers, or a UE/Unity 3D digital-human architecture and launch-ready demo."
metadata:
  category: production
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-digital-human
    resources:
      - qa-decisions
    risk: local-write

---

# Kelly Digital Human

## Overview

Kelly Digital Human is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The same
Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. It is Kelly's digital-human solution desk: pick the
right path, review the vendor/architecture comparison, and run the launch QA
gate before a real provider or engine build.

This skill is mostly curated reference content, not per-user data: the
project overview, personas, pipeline routes, vendor comparison, and QA
checklist itself are fixed (ported from the retired local app's demo
dataset -- there was never a script or route that wrote different content).
The one genuinely dynamic piece is the human verdict on each QA gate check
(approve / request changes / block, with a note) -- that decision is written
directly onto its own Busabase record, the same direct-field-write pattern
`kelly-clm`'s approval queue uses. There is no separate decisions-log bucket.

## Two Implementation Paths

### 1. 2D photoreal digital human, low cost and fast launch

Use this when the goal is an online demo, customer-service agent, product
explainer, training host, livestream assistant, or any scene where speed and
cost matter more than fully custom body motion.

Operating model:

- Connect an existing digital-human service, for example Silicon
  Intelligence, Tencent Zhiying, ZEGO-style real-time avatar/RTC providers, or
  another vendor the user already has access to.
- Send text or a speech/audio stream into the service.
- Receive a rendered video stream or clip with lip-sync and facial motion.
- Keep all business logic, script review, safety wording, telemetry, and QA
  gates in Kelly's local workflow.
- Best first milestone: one approved persona, one scene, one voice, one
  Chinese and one English demo script, one web demo page, and a
  latency/quality dashboard.

### 2. 3D custom digital human, high freedom

Use this when the brand needs a custom character, proprietary body motion,
special clothing, stylized art direction, a stage/event scene, game-like
interactivity, or reusable UE/Unity assets.

Operating model:

- Use UE or Unity as the renderer.
- Drive face, lip-sync, gaze, and body motion through a digital-human driving
  layer.
- Treat the engine project as the final render surface; this skill owns the
  solution design, persona bible, QA checklist, demo script, and launch
  decision.
- Best first milestone: one hero character, one calibrated voice, three
  production motions, one camera scene, and an executable or web-streamed
  demo.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-digital-human-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's artifact and product
contracts, stop before the unavailable Busabase operation, and report the
exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Digital Human overview"></td>
    <td width="50%"><img src="assets/screenshots/studio.webp" alt="Kelly Digital Human live studio"></td>
  </tr>
  <tr>
    <td><strong>Solution overview</strong><br>Side-by-side 2D fast-launch and 3D custom-build paths, with readiness score, latency targets, and launch blockers.</td>
    <td><strong>Multimodal studio</strong><br>Animated avatar stream with lip motion, waveform, transcript, provider mode, route latency, and stream events.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/vendors.webp" alt="Kelly Digital Human vendor architecture"></td>
    <td width="50%"><img src="assets/screenshots/qa.webp" alt="Kelly Digital Human QA gate"></td>
  </tr>
  <tr>
    <td><strong>Vendor and architecture desk</strong><br>Compares 2D service integration, real-time RTC rendering, and UE/Unity 3D architecture with cost, speed, and control tradeoffs.</td>
    <td><strong>Launch QA gate</strong><br>Checks lip sync, stream latency, consent, script safety, fallback behavior, and production handoff state before launch.</td>
  </tr>
</table>

## Default Workflow

1. Clarify the target scene: sales demo, AI host, customer support,
   livestream, training, product onboarding, event screen, or brand
   character.
2. Choose the path:
   - choose **2D** when "低成本", "快上线", "先 demo", "真人感", "视频流",
     "语音驱动", or "客服/讲解员" is the priority.
   - choose **3D** when "专属形象", "品牌 IP", "动作自由度", "UE", "Unity",
     "舞台", "互动", or "长期资产" is the priority.
3. Open the AirApp (or `pnpm --dir content/kelly-digital-human-app dev` for local preview) and use demo
   mode (`?demo=1`) to show the concept before any vendor contract or engine
   work.
4. Draft the persona bible: appearance, voice, tone, forbidden claims,
   supported languages, scene background, fallback lines, and consent
   requirements.
5. Draft the multimodal pipeline:
   - input: text, uploaded audio, live mic, or TTS output from another skill.
   - cognition: LLM reply, retrieval answer, scripted explainer, or support
     macro.
   - voice: TTS or user-supplied audio.
   - renderer: 2D vendor service or UE/Unity.
   - transport: video clip, WebRTC/RTC stream, HLS, or embedded player.
6. Walk the `#/qa` review queue and record approve / request changes / block
   per check, with a note, for lip sync, latency, identity consistency,
   pronunciation, unsafe content, disclosure, fallback, and device
   performance.
7. Do not execute external calls, purchase vendor plans, upload identity
   assets, or stream live user audio unless the user explicitly approves that
   step.

## Boundary

- This skill never calls Silicon Intelligence, Tencent Zhiying, ZEGO, UE,
  Unity, TTS, STT, a camera, a microphone, or any other external model or
  vendor API. It is a solution desk and QA gate, not a live rendering
  pipeline.
- Treat face images, voice samples, customer conversations, support
  transcripts, and brand scripts as sensitive. Never upload identity assets,
  voice samples, or live audio to a vendor without explicit approval.
- Always include a visible or spoken AI disclosure in customer-facing
  experiences unless the user has a legally reviewed policy saying otherwise.
- For production, require a human approval gate before public launch and
  before any live customer support flow.
- Keep demo data, vendor credentials, SDK tokens, recordings, and generated
  clips out of git. Use demo data for screenshots.

## Busabase Resources

One Base under one application Folder (`kelly-digital-human`), declared in
`content/kelly-digital-human-app/app/js/config.js` and the generated template sidecars under `content/`:

- `qa-decisions`: one row per launch-QA-check decision, keyed by the curated
  check id (`lip-sync`, `latency`, `ai-disclosure`, `voice-consent`,
  `script-safety`, `fallback`, `privacy`, `mobile`). A row only exists once a
  human has decided on that check. The project overview, personas, pipeline
  routes, vendor comparison, and the QA checklist's own labels/owners/evidence
  are curated reference content ported into
  `content/kelly-digital-human-app/app/js/digital-human-model.js` -- they are not stored in Busabase
  because nothing in the retired local app ever made them editable.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space.

## Views

- `#/overview`: recommended path, readiness score, latency/lip-sync/stability
  metrics, and the primary pipeline.
- `#/qa`: launch QA review queue; approve / request changes / block writes
  the decision directly onto the check's Busabase record.
- `#/studio`: simulated multimodal stream -- avatar, waveform, persona/route
  selectors, route latency, and stream events. Entirely client-side; no
  camera, microphone, or vendor call.
- `#/vendors`: vendor and architecture comparison table plus reference
  pipeline diagram.
- `#/settings`: data provider, Busabase resources, and the safety boundary.

## Demo Mode

- `?demo=1` opens a deterministic, fully offline tour of the same curated
  project/persona/pipeline/vendor/QA content used in real mode. It never
  reads or writes Busabase. A decision action in demo mode only shows a
  notice ("Demo mode: this is a read-only tour, nothing was saved.") -- it
  never applies, matching the retired local app's demo behavior.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-digital-human-app dev` only when local preview/debugging is explicitly
requested.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-digital-human-app/` project and
  `pnpm --dir content/kelly-digital-human-app dev` remains supported;
- all persistent state uses `busabase-sdk` and the declared resource map — no
  local JSON, browser storage, or provider choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, QA review, Studio, Vendors, and Help & Settings render on desktop
  and phone widths;
- `pnpm --dir content/kelly-digital-human-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never call a real digital-human vendor, engine, TTS/STT
service, camera, or microphone from the AirApp.
