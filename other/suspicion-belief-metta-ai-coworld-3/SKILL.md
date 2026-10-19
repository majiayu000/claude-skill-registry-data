---
name: suspicion-belief
description: "Use for suspicion belief recipes in scripted Coworld policy optimization."
---

# Suspicion & belief modeling — recipes (loop tier)

On-demand recipes (2). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Debounce belief flips with a consecutive-frame counter and enumerate every reset
`loop` · ⚠ _session-derived, unverified_

Debounce belief flips driven by noisy frame-by-frame screen perception with a CONSECUTIVE-frame counter, not a single frame and not a cumulative count: a flip/exclusion fires only after the qualifying condition holds for a fixed number of consecutive frames (~0.5s worth), and the counter resets to 0 the instant contradicting evidence appears AND when the latch is freshly re-asserted. Enumerate EVERY reset condition explicitly (e.g. positive match, object coming on-screen, no detections at all, localization loss) -- missing one leaves the counter creeping toward a false flip. Test three cases: decays after threshold, does NOT decay when interrupted, does NOT decay when the contradicting condition is false. For multi-condition behavioral flags, verify the FULL conjunction does not fire when only one sub-condition holds (e.g. a flag requiring visible_ticks>200 AND entries==0 AND stationary_ticks>100).
  <sub>sources: codex:019e03bc-5520-7e72-aa5c-a572ead62b91, codex:019e05ac-239c-7bb0-8e34-1ec371fbabcd, codex:019e067b-643a-7100-abdb-8d6a0c79d242</sub>

#### 2. Design every sticky belief flag with its clear path; make clearing universal and phase-aware
`loop` · ⚠ _session-derived, unverified_

Design every sticky/latched belief flag together with its clear/decay path at the moment it is created. A one-way latch (set freely, cleared only by one narrow opposite event) silently rots: it persists a stale belief long after the justifying evidence is gone while downstream action keeps acting on it. Make clearing rules UNIVERSAL, not buried in one branch -- a flag cleared only inside one update branch goes stale on a state transition that skips that branch, so prefer a single universal rule expressed as a pure function of current state (e.g. in_chatroom = (view == Whisper)). When a belief shield depends on phase, make it phase-aware: a shield that is correct in one phase (watching an icon disappear as a completion signal) is wrong in another (the icon still renders during a hold phase, so a missing icon there is genuine negative evidence). When the stale-flag consumer is off-limits to edit, fix the belief at its SOURCE rather than patching every reader.
  <sub>sources: codex:019e04f4-9a40-7411-a0a5-872164eda3f1, codex:019e05ac-239c-7bb0-8e34-1ec371fbabcd, opencode:ses_201713d2dffe7pZ6AcZMDZXvNZ, codex:019e0140-e554-78e3-b66f-80634cc63f5d (+2)</sub>
