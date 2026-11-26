---
name: on-device-inference-cost
description: "Use when pricing an on-device model pass or its lag."
version: 1.0.0
author: Charles Ponti, Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [performance, benchmarking, latency, asr, coreml]
    related_skills: [apple-workflows]
---

# Pricing an on-device model pass

For the question "can this feature afford another pass over the input?" — a live preview, a re-read of a
growing buffer, a cap in the code that someone wants raised. On-device models are fast enough that instinct
lies in both directions, so the currency is a measurement, not an analogy to how a language model costs.

## When to Use

- deciding whether an interactive surface can re-run inference on input that grows with use
- a hard limit exists (`longestTake`, a sample cap, a timeout) and someone asks why it is that number
- a live view stops updating, or an app "looks broken" on long input
- a doc, table or benchmark has a cost figure you are about to quote in a decision

## Measure, then price

```bash
# 1. the configuration you ship — a debug build times the wrong program
swift build -c release

# 2. length-scaled input from real material, so the curve is visible
ffmpeg -v error -stream_loop -1 -i real-take.wav -t 60 \
  -ar 16000 -ac 1 -c:a pcm_s16le take-60.wav

# 3. the tool's own elapsed count, at several lengths
.build/release/<tool> --transcribe take-60.wav    # prints its own interval
```

- **Release only.** A Swift debug build is `-Onone`; the hot loop is usually in Swift rather than in the
  model, so a pass that costs seconds in release costs minutes in debug and every figure is meaningless.
- **The runner's elapsed, not wall clock.** Process start, model load and input conversion sit inside the
  same wall time and get charged to the pass.
- **Real material.** A synthetic benchmark (one sentence repeated) measured 1.87 s for ~370 s of audio where
  real speech of the same length measured 9.05 s — a 4.8× difference from the audio alone. Generated material
  is the right stress test for correctness, and the wrong one for cost.
- **Several lengths, then read the slope.** 60/180/360/600 s turns "it feels slow" into "about 1.4 s per
  minute of audio, linear".
- **Read the spread, not the headline cell.** A row that has measured 1.85 s and 10.3 s is a range; the
  caveats under a results table usually say so.

## What the number decides

- **A whole-input pass makes the preview's lag grow with use.** Cost is linear in length, so a throttle of
  `interval = k × cost` means the gap between updates is `k ×` the pass: report that lag, because that is what
  the person feels, not the pass cost.
- **Restate a cap in the unit it protects.** A limit written as "N minutes" is policy dressed as a
  constant; the honest form is "stop when the preview can no longer keep pace", which lands at whatever lag
  the measurement says is useless. Raising the minutes without changing the shape only makes a slower echo.
- **Duty cycle is a real cost.** With `interval = k × cost` the model is held at `1/k` of the machine's
  capacity for the whole session — battery, heat, and it delays the result the person is actually waiting
  for, which is the final pass.
- **Per-pass copies cost too.** Snapshotting a growing file per pass is fine at 10 s and a 38 MB copy at 20
  minutes.

## When the cost is not the bottleneck: instrument the chain

A costed pass is not a diagnosis. Count the owners of "the output is late": the ticker that fires late, the
input snapshot, the model, the hop onto the thread that draws, the work that folds the result in, and any
deliberate pacing animation still owed. Do not optimise the model until the attribution says it is the model —
in one measured case a 16 s interactive pass used **252 ms** of engine time and ran **0.23 s** behind the
input, while the first word did not appear until **3.28 s** and the pacing animation owed another 0.4 s. The
engine was innocent; the complaint was real.

So: emit one log line per pass with every stage timed, plus a per-session summary, behind a stable grep-able
prefix. Include the stage nobody measures — the return hop to the main thread — and the composite that the
person actually feels (`input on disk minus input this pass described`, which is _behind_, not pass cost).
Then keep the same code path reachable headlessly so a bad run can be replayed from a file instead of from a
microphone.

**A large `first word` has two owners that look identical from outside:** the model warming up, or the input not
carrying signal yet because the person had not started. Separate them by running the same path over a fixture that
begins speaking at t=0 — one pipeline reported 0.51 s from speech to first output there, against 2.1-2.3 s on real
sessions whose first second was the speaker drawing breath. When the fast case is fine, the fix is feedback during
the gap (see `apple-workflows` → macOS menu bar app), not a faster model, and reporting it as engine latency sends the next
session optimising the wrong stage.

Field-by-field table, the log contract, the fixture recipe and the real-time replay recipe:
`references/live-path-instrumentation.md`.

Trim silence from the input before pricing anything else: it is the cheapest lever there is, and leading noise is
where a model invents words. Floors, the room-relative threshold, the sustained-window test and the temp-copy recipe:
`references/audio-silence-trim.md`.

## When the answer is windowing

A fixed-size window makes per-pass cost independent of how long the input has grown, so the lag stays flat and
the cap can be deleted rather than raised. It is a correctness change, not just a speed one:

- **Stitching needs timings.** Words cut mid-syllable either duplicate at the seam or vanish; cut on a
  word/token boundary using the engine's own timings rather than guessing from text overlap.
- **Never rewrite what is already on screen.** Publish only up to the last stable word; a preview that
  visibly corrects itself is worse than one that lags.
- **The one-shot pass over the whole input stays the authority.** The windowed view is a courtesy; the final
  transcript must not inherit the window's seams.
- **Check the library before building it.** Sliding-window managers, chunk/overlap configs and timing
  results often already ship in the ASR package; reading its public API is cheaper than writing a stitcher.

## Pitfalls

- **Do not repeat a document's number as if you measured it.** A table row can be the best case of a range
  five times the typical one, measured on unrepresentative material. Quote the method alongside the figure,
  and when a measurement contradicts a document, re-measure before deciding which is wrong — then correct
  the document in the same pass so the next decision is not made on it twice.
- **A benchmark harness with `runs: N` across every model variant will time out on long input.** Time the
  one path you care about, at the lengths that bracket the decision.
- **A logged figure is not evidence until it calls the function the UI calls.** When a number in the log and
  the shipped behaviour disagree, the behaviour is right and the instrument is the bug; fix the log in the same
  pass, because a confident wrong number is what the next session will quote back as measured fact.
- **Do not reason by analogy to LLM cost.** Encoder-style models sweep the input in parallel on the Neural
  Engine: cost is linear in audio, not quadratic in tokens, and a "re-reading the essay" intuition prices the
  feature wrong in both directions.
- **A headless replay proves the pipeline, not the surface.** A CLI that shares the live loop times input →
  model → transform and bypasses the display entirely, so it cannot reproduce "the overlay never appeared" or a
  late redraw. Say which path every number came from, and when the complaint is about what the person sees, drive
  the real app (its own hotkey, its own log) rather than the replay — then compare the two, because a large gap
  between them is the display path's cost and a small one clears it.
- **Price the capture path by A/B on one recording.** Record the same fixture through the microphone, then replay
  that recording through the file path: equal numbers clear the capture stage, a gap localises it. Watch the level
  in the second half of the test — speaker-to-microphone playback clips (`max_volume: 0.0 dB` from `volumedetect`),
  and a clipped fixture inflates engine time enough to look like a capture problem: keep playback near 50–60 % and
  confirm the mean level is healthy before trusting the comparison.
- **A re-merged snapshot must not restamp what is already on screen.** A preview that rebuilds its line from the
  newest pass typically keeps only the shared prefix as settled and stamps everything after it with "arrived
  now"; one revised word — a capital, an apostrophe, a homophone — therefore restarts the entrance animation for
  the entire visible tail. Carry the arrival time forward for every word that survived, compared on the
  normalised form, and stamp only words that are genuinely new. Measured cost of getting this wrong: a twelve
  second reveal on a line that was 0.26 s behind the input, which reads as the app being far slower than it is.
  When the fix lands, re-measure the reveal figure too — the pacing may already show an overdue word at once, in
  which case the inflated number was the instrument's arithmetic rather than the product's behaviour.

- **A log line that names a requested value is not a log of what happened.** "listening on device X" when
  capture actually used device Y is a lie that sends the next diagnosis down the wrong path; the log misleads
  because it describes the request, not the run. Record the device, rate, and format actually in use, plus any
  fallback decision, so the log describes what happened. This is the same rule as everywhere else: log the
  effect, not the intent.

- **A throttle that logs on every check, before the interval is due, produces noise that looks like work.** A
  "skipping" line that fires on every pass — because the check runs before the interval test — floods the
  log and hides the passes that matter. Gate the line on the branch that actually skips, or remove it; a log
  that fires whether or not anything happened is not instrumentation, it is decoration.
