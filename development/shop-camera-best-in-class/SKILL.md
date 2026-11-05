---
name: shop-camera-best-in-class
description: "Use when designing, upgrading or judging a shop camera or office-audio lane: the car counter, customer wait time, the office ears (capture, speech gate, transcription), live view, plates, owner controls or watchdogs, or when Nour asks what the best camera or audio setup out there is, whether to move the cam system to a stack like Frigate, or which features and controls are still missing. Gives the mechanisms the best open-source stacks use (Frigate, go2rtc, Silero VAD, faster-whisper, whisper.cpp, WinSW), the matching gap in our lanes, and a kill criterion for each upgrade. Not for: adding or swapping one camera (camera-onboard-rtsp), a lane that is down or reads zero right now (systematic-debugging, production-health-report), running commands on a shop PC (shop-pc-remote-session), a shipped binary or capture (reverse-engineer-anything), or a verdict on one library alone (docs/UPSTREAMS.md, find-skill)."
triggers: camera system, cam system, car counter, customer wait, office ears, best setup, frigate, speech gate, watchdog, camera controls, what are we missing
---

# Shop cameras and ears: copy the mechanism, not the product

Answer first: before writing code for any camera or audio lane, find the row in
[references/mechanisms.md](references/mechanisms.md) for what you are building, take its mechanism and its kill criterion, and
check [references/upgrade-list.md](references/upgrade-list.md) for whether it is already ranked, built or parked. Then build the
smallest version that carries the mechanism, and end the PR body with a `Benchmarked against:` line naming the row. This is the
camera-and-audio instance of the general "learn from the best" stance: the rows are the best implementations, already found.

Why: three lanes were built from scratch and each missed a basic the mature stacks have (`evals/baseline.md`). The office worker
was deaf for four days behind a fresh heartbeat (2026-10-22 to 10-26): a no-speech capture returned and its CAPTURING state was
never cleared (a state-transition bug, fixed in PR 3305), and nothing paged because liveness read the heartbeat, not the work.
Reader timeouts and the capture bound (PR 3298) are separate hardening, not that fix. The counter restarts 20 to 73 times a day
and its portal counted 0 crossings on 10-24 and 10-25 while detections flowed.

## Where the lanes live (read before changing one)

- Office ears: `camera-bridge/vision/officewake.py` (wake, capture, heartbeat), `officeaudio.py` (ffmpeg probe and capture),
  `officepost.py` (whisper, post), `camera-bridge/docs/OFFICE-INTERACTION-COMMISSIONING.md` (settings, installs, rollbacks).
- Car counter: the edge (`camera-bridge/edge_main.py`, portal crossings, `--stall-*` flags) and `camera-bridge/visitd/` (the visit state
  machine in `camera-bridge/README.md` section 8: ENTERED_ZONE, ARRIVAL_CANDIDATE at 10 s, CONFIRMED_ARRIVAL at 45 s,
  PASS_THROUGH), plus `camera-bridge/docs/NICKSMAX-SIGN-LENS.md` (the crossing line and lens choice).
- Server: `apps/nickstire/server/routers/lot.ts`, `server/services/officeLaneAlert.ts`, `cameraHealthAlerts.ts`,
  `vehicleCounterTrust.ts`, `shared/cameraFleetHealth.ts`; Admin > Lot is `client/src/pages/admin/LotSection.tsx`.

## Procedure

1. **Name the lane and the job.** Lanes: office ears (front-desk PC), sign camera and car counter (lot PC), bay camera, counter
   mic, Admin > Lot (server and client). Job: count, time, hear, see, control, or keep alive.
2. **Read the row.** Each row in `mechanisms.md` gives what the best stack does, its doc link, our gap, and the kill criterion.
   VERIFIED means the linked doc says it; RESEARCH means the 2026-10-26 research said it and the doc page does not; INFERRED is a
   design. Do not raise a RESEARCH or INFERRED line to a fact in a PR body.
3. **Check the verdict.** `docs/UPSTREAMS.md` rules on adopting a product: Frigate is ADOPT-CANDIDATE pinned 0.17.2; Scrypted
   NVR, ZoneMinder, Viseron, CodeProject.AI and Agent DVR are REJECT; MediaMTX is ADOPT-CANDIDATE. Silero VAD, faster-whisper,
   go2rtc and WinSW have no verdict yet: an offline bench is fine, an install needs a verdict row first (find-skill, prior-art-grep).
   Adopting anything that costs money or touches a shop PC needs Nour's go.
4. **Keep the hard rules.** Audio never leaves the shop PC: the server gets the transcript and stills, never the audio. Local raw
   clips are pruned after `OFFICE_RAW_AUDIO_RETENTION_HOURS` (6 h default); never lengthen that or upload audio. Recording is
   gated by `OFFICE_AUDIO_POLICY_ACK` / `-AcknowledgeRecordingPolicy`: an operator assertion that notice/consent and counsel
   review are complete (`OFFICE-INTERACTION-COMMISSIONING.md`). An agent never sets it, and crew consent at hiring does not
   stand in for it (customers are recorded too); do not widen what is recorded. Nothing customer-facing. No shop-PC change except through Nour's paste or
   his own go for that action (`shop-pc-remote-session`). No production write without his go. No purchase without the price.
5. **Build the smallest carrier** of the mechanism, with a test that breaks it first (`positive-control-first`). Billed jobs over
   complete ET days are a LOWER bound for the car counter (every counter invoice is a car that came in; drive-ins that buy
   nothing make arrivals above billed normal): flag arrivals below billed, and require an independently labelled arrival
   sample before imposing any accuracy band. That read is a production SELECT, so it goes through `prod-db-guard`.
6. **State the kill criterion** from the row in the PR body, with the date it will be read, and update the row's status in
   `upgrade-list.md` in the same PR.

## Liveness, the rule behind every lane

A lane is alive only when its real work moves: PCM bytes for audio, decoded frames for video. On the server, liveness is accepted
heartbeats whose producer counters advance (frames, probes, captures), never posted episodes or visits: a quiet office or an
empty lot is healthy. A post is owed only after a capture that should produce one (that is the not-posting rule). A heartbeat
thread beside the work proves the process exists, nothing more, unless it reports the work's own counters and state. Every
lane needs three layers: a reader timeout inside ffmpeg (RTSP `-timeout` in microseconds before `-i`, RTSP inputs only; HTTP
and DirectShow inputs need their own bound; VERIFIED), a progress watchdog that kills and reaps a
stalled reader (RESEARCH), and a supervisor that restarts a process that exits nonzero. Task Scheduler's restart settings retry
a task that failed; a process that hangs never fails, so nothing restarts it (RESEARCH; seen live 2026-10-22 to 10-26).

## Never

- Count arrivals from zone occupancy or from a list of zones ever entered: that is membership, not an ordered crossing.
- Use a review-item or alarm duration as a customer's wait: a parked car stops producing motion.
- Put diarization, GenAI descriptions or plate reading in the capture path; they run after capture, on finished clips.
- Read a quiet lane as a healthy one without its progress counter (`empty-vs-error`).
