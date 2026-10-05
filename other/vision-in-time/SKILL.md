---
name: vision-in-time
description: Understand videos, screen recordings, and time-based visual evidence by turning media into timestamped observations, key moments, timelines, and evidence-backed answers. Use when the user asks Codex to inspect a video, explain what happened over time, find key moments, analyze a screen recording, work around models without native video understanding, or answer questions with timestamps from visual/audio evidence.
---

# Vision In Time

## Contract

Treat video as state over time, not as a blob.

This skill converts video into bounded, timestamped evidence that an agent can
inspect, cite, delegate, and revisit. Prefer evidence pointers over dumping
frames into context. Produce answers that say what was observed, where it was
observed, and what remains uncertain.

## Operational Goal

Given a short test video and a user question, produce:

1. `evidence-index.json` with video metadata, sampled frames, candidate moments,
   evidence pointers, and unresolved uncertainties.
2. A contact sheet for first-pass visual inspection.
3. A timeline answer whose claims cite timestamps or evidence ids.
4. A validation pass confirming timestamps are monotonic, in bounds, and
   referenced evidence ids exist.

## Quick Workflow

1. Clarify the question only if the goal would change the sampling strategy.
2. Probe the video with `scripts/probe_video.py`.
3. Sample frames with `scripts/sample_frames.py`; start sparse, then densify
   around suspected changes.
4. Create a contact sheet with `scripts/make_contact_sheet.py`.
5. Build or update `evidence-index.json` with `scripts/build_evidence_index.py`.
6. Inspect the contact sheet and selected frames visually; use audio/transcript
   only when present or relevant.
7. Select key moments by change, salience, question relevance, diversity, and
   uncertainty reduction.
8. Answer with timestamps, evidence ids, confidence, and uncertainties.
9. Feed user corrections or failed validation back into a targeted reinspection
   pass instead of restarting from scratch.

## Delegated Observation

The root agent may spawn one or many Child Agents when the video is long,
multi-hour, visually dense, or naturally divisible into windows. Child Agents
inspect bounded evidence windows and return compressed observations only:
summary, candidate moments, evidence ids, uncertainties, and follow-up
recommendations. The root agent owns the final synthesis.

## Bounded Memory Rules

- Keep raw media out of the root context.
- Materialize frames, clips, or contact sheets only when they can change the
  answer.
- Store evidence artifacts in the user's workspace, not inside the skill.
- Use pointers first: `{ video, t_start, t_end, frame_id, reason }`.
- Prefer reinspection around uncertainty over globally increasing sample rate.

## Feedback Channel

Output can become optional input for the next pass. Convert feedback into one
of: new question, missing evidence target, timestamp correction, preference
signal, validation failure, or uncertainty to resolve.

## Resources

- `references/evidence-model.md`: terms and JSON shapes.
- `references/key-moment-selection.md`: how to pick important moments.
- `references/bounded-memory.md`: streaming and storage strategy.
- `references/delegated-observation.md`: root/child agent contract.
- `references/output-contracts.md`: answer and validation formats.
- `references/failure-modes.md`: common traps and recovery moves.
- `references/screen-recording-playbook.md`: v1 workflow for UI videos.
- `assets/evidence-index.schema.json`: minimal index schema.
- `assets/timeline-template.md`: timeline answer template.
- `assets/child-observation-template.json`: child-agent return shape.
