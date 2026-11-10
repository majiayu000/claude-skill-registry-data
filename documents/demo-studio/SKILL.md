---
name: demo-studio
description: >
  Use this at Step 2.5 — AFTER the orchestrator reports the build green, before the submission is
  filed — to produce the hackathon's demo video autonomously on the user's machine: it writes a
  scene-by-scene demo script from the brief/spec/event.md, records the built app scene-by-scene
  (Playwright screencast for browser scenes, ffmpeg gfxcapture/ddagrab for native/wallet-popup
  scenes), narrates with TTS and word-timed captions, assembles with Remotion, runs a frame-level
  QC loop, has the user WATCH the final cut, then — on a separate consent — uploads it and resolves
  the submission draft's demo-video URL. Trigger it ONLY on the user's ask: "make the demo video",
  "record the demo", "create the hackathon video", "do the demo studio", the user starting Step
  2.5 after the orchestrator's offer, or an autopilot dispatch under a locked campaign contract
  (which counts as the user's start). NEVER self-trigger on build completion — the orchestrator
  offers, the user starts. It records under a foreground do-not-disturb session and never publishes
  without the user watching first — unless the locked contract's explicit WATCH policy delegates
  that watch (autopilot mode; references/campaign-contract.md). Do NOT use it to build (that's the
  orchestrator) or to run the faucet/deploy/signup gates (that's the gate-concierge).
---

# Demo Studio — Step 2.5: the demo video, recorded and assembled autonomously

## What this is

Every hackathon submission needs a 2–5 minute demo video, and hand-producing it — script, record,
narrate, caption, edit, upload — costs hours at the worst possible time. The kit has automated
everything up to here: the build is green, and the architect's `docs/gates/submission-draft.md`
carries a `TBD-post-build: demo video URL` waiting to be filled. This seat fills it. It drives the
built app through a scene-by-scene script, captures each scene, assembles a captioned narrated cut
with Remotion, and — only after the watch gate (Stage 7) and the upload consent — uploads it.

It is a **user-side seat** (like the guide and the gate-concierge): it runs on the user's machine
with their granted tooling, it **never self-triggers**, and its two outward actions — running a
foreground recording session and publishing the video — are **consented gates**. Quality comes from
gates, not hope: every scene has a pass/fail assertion and a bounded retake budget, every render
passes a frame-level QC loop, and **the user watches the final cut before anything is published**
(delegable only by an autopilot contract's explicit WATCH policy — Stage 7).

**Announce at start:** "I'm using the demo-studio skill — I'll write the demo script for your
approval, record the app scene-by-scene, assemble a captioned narrated cut, show it to you, and only
upload it once you've watched it and said go."

The operational ground truth — exact tool versions, the copy-paste ffmpeg/Playwright/Remotion
commands, and the Windows bootstrap steps — lives in `../references/demo-stack.md`. **Read it before
running anything**, and honor its freshness rule (re-verify the `[pin]`/`[policy]` rows before a
real campaign; the toolchain moves weekly). Music lives in `../references/music-kit.md`. The demo
script follows the **locked schema** `../references/demo-script-schema.md` (v1) — read it before
Stage 1, start from its skeleton, and keep its §8 status ledger current (stages append their
locked vocabulary rows as they land). At boot,
**run your tollgate session card** (`../references/tollgate.md` — rows 5–6, 8–13, 16: the
demo-stack probes plus browser/device access, the wallet extension when wallet scenes are on, and
disk) before Stage 1; a failing hard row stops
you with the row's fix hint — never discover mid-recording that ffmpeg lacks `gfxcapture`.

## Where you sit

Step 2.5, between the green build (Step 2) and the submission (Step 3's closing pass). Your input is
a working app; your output is a video URL that resolves the submission draft's TBD. You read the
brief, spec, `event.md`, and submission draft from the **project repo**
(`../references/repo-bootstrap.md`); you **write** the demo script and the Remotion project code to
the project repo (renders and captures stay git-ignored — see *Repo hygiene*), and you record your
upload evidence in the **same gate ledger** the concierge uses (one ledger per campaign — extend the
existing `docs/gates/*-gate-ledger.md`; **if none exists yet** — you can run before any concierge
pass — create `docs/gates/<YYYY-MM-DD>-gate-ledger.md` in the concierge's format, and never start a
second one). You do not extract, ideate, plan, build product code, or run the
faucet/deploy/signup gates — those are other seats.

Two consents are yours and only yours to ask for: **the recording session** (it takes over the
foreground of the user's desktop — a do-not-disturb window) and **the upload** (publishing is
irreversible-ish; watching the cut and consenting to upload are two separate human moments).
**In an autopilot campaign** (your kickoff carries an `AUTOPILOT CAMPAIGN` block —
`../references/campaign-contract.md`) both consents come pre-collected in the locked contract
**when the user granted them** — the recording-session pre-consent (field 12) and the UPLOAD
authorization (field 10, identity-bound). A pre-consent the contract struck, or an UPLOAD marked
`manual`, stays with the user — return that act BLOCKED / hand it back, never assume it. The
script and the WATCH gate follow the mode-aware notes in their stages below, and anything else the
contract does not enumerate is returned BLOCKED with the exact question.

## Kickoff inputs (defaults are set; the user overrides per campaign)

The kickoff (`../prompts/INVOKE_DEMO_STUDIO.md`) carries these; each has a working default so the
seat runs without interrogation, and the user overrides any:

- **VOICE** — default **Kokoro** (local, offline, zero-signup; English). `edge-tts` for nicer MS
  neural voices (network-dependent), or **ElevenLabs** for premium (its API key is a Tier-A
  concierge signup gate).
- **LENGTH** — default the event's mandated length, else **~3:00**.
- **MUSIC** — default **off** (captions-only; demos are often watched muted and the licensing
  surface is smaller). Opt in and pick a mood; tracks come from `../references/music-kit.md`.
- **WALLET-ON-CAMERA** — default **real MetaMask via dappwright** (what judges expect; proves the
  interaction). Auto-swaps to the clean injected-signer + block-explorer-confirmation shot only on
  retake-budget exhaustion, or set it per-scene.
- **UPLOAD** — default **unlisted YouTube** (consented browser upload), Drive fallback one flag away.
  This field is the standing authorization for the upload action class (see *Upload*).

## The stages

### 1. Script (committed, user-approved before any recording)

Read the brief (the **demo money shot**), the spec, the pack's `event.md` (the **published judging
criteria + weights**), and the submission draft. Write `docs/demo/<YYYY-MM-DD>-demo-script.md` **to the
locked schema** (`../references/demo-script-schema.md`, v1): copy its skeleton, fill §§0–5 and §7's
title/description/tags, and append §8's `scripted` row — the production card, the story +
judging-weight time budget (§1's seconds sum to the target), the seven-row pre-flight checklist, the
shot list (`id · seconds · visual (route/action/window) · narration cue · driver · wallet verbs ·
gate assertion · retakes · take`), the narration script (§4 is the single source of the words — the shot list carries
cues, not text), the assembly plan, and the publish copy.
**Allocate scene seconds by the judging weights** — if working-demo is 50%, most seconds go to the
money shot, not the intro. Commit and push it, then **get the user's approval before recording**
(in an autopilot campaign the approver is the autopilot, which reviews the script for contract
conformance — judging-weight allocation, money shot, length — plus the schema's conformance check,
and approves or re-dispatches with corrections). The approval covers the whole call sheet —
pre-flight, narration, publish copy — not just the scenes. A rubber-stamped script produces a
drifting video, same as a rubber-stamped spec.

### 2. Storyboard preview

Render the Remotion composition's **static frames** (title/section cards, caption layout, outro)
as stills — real narration text, empty footage slots — and show them to the user. This is the cheap
correction point: fix wording, ordering, and layout here, before spending capture time.

### 3. Capture (the foreground consented session)

Recording takes over the desktop foreground — get the **recording-session consent** first, and tell
the user it's a do-not-disturb window. **Verify the script's §2 pre-flight rows and tick its `✓`
column first** (append §8's `pre-flight verified` row) — the checklist exists so no take discovers a
missing fixture. Then, **scene-by-scene, sequentially** (one browser context
at a time — see `../references/demo-stack.md`):

- **Browser scenes** — Playwright `page.screencast` (JPEG frames → ffmpeg two-pass H.264), 1920×1080
  viewport, re-encoded to constant fps. Never `recordVideo` (banned — see `../references/demo-stack.md`).
- **Wallet scenes** — headed dappwright with the pinned/cached MetaMask; the **popup is a separate
  window** page-capture misses, so capture it with `gfxcapture` (window regex) or a second screencast
  on the popup, and add MV3 service-worker wake logic (workers suspend ~30s idle).
- **Native scenes** (terminal, native app) — `gfxcapture` (or `ddagrab`), **silent** (ffmpeg has no
  WASAPI; narration is TTS). Discover the monitor/window **at runtime** — never hardcode
  `output_idx`/`hwnd` (DPI + multi-monitor shift them).

Run the **gate assertion** after each take; retake on fail up to budget. **A wallet-scene retake must
first refresh its on-chain preconditions** (nonce, burner balance, pending txs — a prior take may
have already mined the tx or set the allowance), and tx-scene assertions tolerate testnet latency
variance rather than hard timeouts. On budget exhaustion: swap the wallet driver (dappwright →
injected + explorer shot), or mark the scene **BLOCKED** with a placeholder card and report it.
Record each scene's outcome in the shot list's `take` column (final take number, or `BLOCKED`), and
append §8's `recorded` row when the pass completes. Never
fabricate an interaction to make a scene pass — a real BLOCKED beats a faked take (same ethos as the
executor's "never fake green").

### 4. Narration + captions

TTS each scene's §4 narration text (the single source of the words) through the **VOICE** engine (`../references/demo-stack.md` for the
adapter matrix and per-engine timing source). Scene durations derive from the narration length via
the `mediabunny` package's `computeDuration()` (audio-first timing — the video fits the words; exact
snippet in `../references/demo-stack.md`). Build captions
directly as `@remotion/captions` `Caption` objects from the TTS word timestamps — no transcription
pass is needed for narration we authored (the whisper path is only for OpenAI-TTS or friend-recorded
voiceovers).

### 5. Assembly

A Remotion project under `demo/` in the project repo (committed code): title card, per-scene clips
via `@remotion/media` `<Video>`, word-timed captions, optional ducked music bed (MUSIC field), outro
(repo QR + the brief's track/bounty line). Final audio: two-pass loudnorm to **−14 LUFS** for
YouTube (`../references/demo-stack.md` has the exact recipe). QC passes render at reduced resolution; the final is
1080p h264.

### 6. QC loop

Extract per-scene keyframes (per-scene `-ss` seeks so frames map to scenes) and **read them as
images**: money shot visible, text legible, captions present, no Windows.Graphics.Capture yellow
border, duration within budget, and **no secret/address on screen that shouldn't be** (a hard
check). Confirm audio is present with sane loudness stats. Record every check in the script's §6 QC record —
re-render iterations append corrected rows, never overwrite. Fix the composition and re-render, bounded
iterations; if something stays imperfect after the bound, stop and carry a residual-imperfection note
into the watch step — never loop forever, never ship silently.

### 7. Watch (hard human gate in interactive mode; contract-delegable in autopilot — never skipped silently)

The user watches the final cut. In interactive mode this gate is not optional and not automatable;
the QC loop makes the cut *probably* good, the user makes it *actually* shippable. Surface the QC
residual notes (the script's §6) here. **In an autopilot campaign it is delegable — only by the locked contract's
explicit WATCH policy** (`../references/campaign-contract.md`, field 9, always asked at intake,
never defaulted): `pause-for-watch` keeps the human watch as a hard stop; `auto-publish-after-qc`
replaces it with the autopilot's own independent frame/audio review (a second context re-reading
keyframes and loudness stats against the script — not your QC re-asserted), and the user watches
the unlisted link after publish. No contract line → the watch pauses, as in interactive mode.

### 8. Upload (a separate consent)

Only after the watch (or its contract-delegated review, Stage 7), and only on the **upload
consent** (interactive, or the contract's UPLOAD authorization). **Re-read the live logged-in
account first** and proceed only if it matches the account the user authorized — in an autopilot
campaign, the account named in the locked contract (`../references/campaign-contract.md`
§Identity verification); mismatch or logged-out → stop and report what you found, never log in or
switch accounts. Default: consented browser upload to
YouTube Studio (unlisted). **Preflight the account's upload eligibility before spending upload time**
(new/low-history accounts can hit verification interstitials); on any interstitial or Studio DOM
drift, **stop and hand off to the user** — never fight bot detection — with the Drive fallback one
flag away. On success: **verify the link renders for a logged-out fetch**, append any required music
attribution to the description, fill the script's §7 publish rows (URL, verified date), append §8's
`uploaded` row, write the URL + evidence into the gate ledger, and resolve the
submission draft's `TBD-post-build: demo video URL`. (The concierge's closing-pass submission gate
then finds the URL already in the draft.)

## Upload — the ToS-honest doctrine

The YouTube **Data API path is dead** for a personal tool: uploads from unverified API projects are
locked private with no appeal (`../references/demo-stack.md`, PRD §13). So the default is browser automation of the
user's logged-in Studio session — which is **not ToS-clean**: YouTube's terms forbid automated access
with no own-session carve-out. Therefore: keep it low-volume, supervised, the user's own content;
**log every upload in the gate ledger**; and never present it as terms-clean. Authorization for this
action class is the kickoff's **UPLOAD field** — an explicit standing authorization, parallel to but
**distinct from** the concierge's SIGNUP AUTOMATION line (that authorizes signups/API keys, a
different action class; it does not cover uploads). The per-upload consent still gates each run
(in an autopilot campaign, that consent is the locked contract's UPLOAD authorization — Stage 8).

**Drive fallback** (`drive.file` scope, anyone-with-link): non-restricted scope so no app audit, but
still a Google Cloud OAuth client whose Testing-mode refresh tokens **expire after 7 days** — design
for re-consent per hackathon, never a cached-forever token. Standing up that OAuth client is the
user's own one-time setup; the UPLOAD authorization covers the upload action, not provisioning a
Google Cloud project.

## Repo hygiene

- **Committed** (project repo): the demo script, the Remotion project **code** (components,
  compositions — reviewable, re-renderable), and the upload evidence in the gate ledger (URL,
  checksum). A `.gitignore` for the render/capture output dirs.
- **Never committed:** rendered videos, captured scene clips, TTS audio, extracted frames (binaries),
  and — the hard rule — **any secret**. Burner keys live in env vars / keychain; the repo sees names
  and public identifiers only (`../references/conventions.md` §Safety).
- Music MP3s live in the local `~/.build-system/music-kit/` folder, never a repo
  (`../references/music-kit.md`).

## Hard boundaries

- **Never self-trigger.** The orchestrator *offers* Step 2.5; the user *starts* it. No firing on
  build-green. (An autopilot dispatch counts as the user's start — the user contracted Step 2.5 at
  lock time; you still never fire on a state condition.)
- **Two consents, never skipped:** the foreground recording session, and the upload. Watching the
  cut and uploading are separate moments. (In an autopilot campaign these consents and the WATCH
  delegation come from the locked contract, per the clauses above — and one the contract struck or
  marked manual stays with the user; it is never assumed.)
- **Never fabricate an interaction.** A scene that won't pass its gate is retaken, driver-swapped, or
  marked BLOCKED with a placeholder — never staged to look like something that didn't happen. The tx
  in the final cut really happened on testnet.
- **Burner wallet, testnet only** — the kit's standing rule. Never the user's main wallet or mainnet
  funds on camera.
- **No secrets anywhere** — not in a committed file, not in a frame (QC checks for it), not in the
  ledger.
- **You run the video, not the other gates.** Faucets, deploys, signups, and the submission form are
  the gate-concierge's; a build that's actually broken routes back through the guide to the
  orchestrator/architect — you record what's built, you don't re-open the build.

## When NOT to use this skill

- Before the build is green — there's nothing to record; the earliest legitimate timing is right
  after the orchestrator reports green.
- Non-demo-judged builds, or a submission that needs no video — nothing to produce.
- The user wants to record the video themselves — then stop at the committed, approved script
  (Stage 1); it's a usable pre-flight checklist, shot list, and narration sheet on its own.
