---
name: analyze-audio-quality-report
description: Analyze a Coval audio-quality testing report from runs across different voice, speaking-style, volume, interruption, and background-noise scenarios. Use when a user provides a Coval report URL, report export, run IDs, screenshots, or metric summary and wants evidence-backed next steps such as prompt changes, tool handling fixes, STT/TTS adjustments, trace setup, or expanded audio-scenario coverage.
argument-hint: "[Coval report URL, run IDs, or exported report summary]"
---

# Analyze Audio Quality Report

Turn a Coval audio-quality testing report into a practical agent-fix plan. This
skill assumes the user already ran comparable Coval evaluations across audio
quality scenarios, usually by using Coval personas and setting the report to
**Compare by Persona**.

If no report or run results exist yet, ask for them. Do not invent results. If
an end-to-end audio-quality workflow skill is installed in the user's
environment, use that workflow first to create the runs and report, then return
to this skill for analysis.

## Inputs

Accept any of:
- Coval report URL or shared report URL
- report export, screenshots, or copied metric table
- Coval run IDs from the same audio-quality testing sweep
- representative simulation links, recordings, transcripts, traces, or Human Review labels

If Coval CLI/API access is available, use it to inspect runs, simulations,
metrics, transcripts, recordings, and traces. If access is not available, work
from the provided report/export and ask only for the smallest missing evidence
needed to avoid guessing.

## Workflow

### 1. Verify The Comparison

Confirm:
- same agent or intentional agent variant
- same test set and sampled cases across audio-quality scenarios
- same metrics across runs
- all compared runs reached terminal status
- the report is grouped by audio scenario, with Standard Customer or another clear baseline

Call out caveats before interpreting results. Common caveats: missing audio
scenarios, different test cases, incomplete runs, too few simulations per
scenario, changed agent config between runs, or metric definitions that do not
apply to voice data.

### 2. Build Audio-Condition Deltas

Compare each audio-quality scenario against the baseline. Track direction and
magnitude for:

| Area | Typical Signals |
|------|-----------------|
| Task outcome | composite score, task completion, scenario-specific pass/fail metrics |
| Responsiveness | latency, time to first audio, trace TTFB, provider response time |
| Speech recognition | STT WER from traces, transcription error, audio-upload WER with ground truth |
| Generated voice quality | Voice Quality, Speech Artifact Score, artifact-specific metrics |
| Conversation flow | interruption rate, silence, repetition loops, sentiment, turn timing |
| Call shape | turn count, audio duration, early termination, abnormally short or long calls |
| Scoreability | UNKNOWN, missing, failed, or unscored metric results |

Use the metric's natural direction. Lower is better for latency, WER,
transcription error, artifact rate, silence, and interruption problems. Higher
is better for success, completion, accuracy, and quality metrics.

Do not overfit to one row. Treat one-off failures as hypotheses unless the
metric, transcript, recording, or trace evidence supports the pattern.

Treat UNKNOWN, missing, failed, or unscored metric results as evidence to
inspect, not as data to ignore. Under heavy audio stress, a judge may be unable
to score because the call ended early, the transcript is too sparse, or the
interaction became too anomalous to evaluate.

### 3. Inspect Representative Evidence

Open or request representative simulations:
- worst regression for each affected audio condition
- one healthy baseline simulation
- any surprising metric outlier
- any UNKNOWN, missing, failed, or unscored metric result
- very short calls, very long calls, or early terminations compared with baseline
- cases where binary task metrics passed but the transcript or recording shows a materially different experience
- Human Review disagreements, if present

For each important example, inspect the transcript and recording when available.
Use traces when present to distinguish agent-side latency, tool delay, STT/TTS
behavior, and turn-taking issues. Separate metric evidence from listening
judgment and label anything that is inferred.

### 4. Diagnose By Audio Condition

Use audio-condition hypotheses, then verify them against evidence:

| Audio Condition | Likely Failure Modes To Check |
|---------|-------------------------------|
| Standard Customer | General agent, test, metric, or tool issue if this baseline also fails |
| Impatient Customer | Long answers, slow tools without status, too much confirmation, poor concise recovery |
| Confused Customer | Prompt lacks clarification strategy, agent over-assumes, weak explanation or repair loop |
| Interruptive Speaker | Barge-in handling, state recovery after overlap, talking past the user, duplicated tool calls |
| Super Fast Speaker | STT finalization, compressed turns, missed entities, confirmation strategy, response pacing |
| High Background Noise Speaker | STT robustness, repeat/confirm policy, important-field validation, noise-sensitive routing |
| Low Volume Speaker | VAD/input gain, STT confidence, missed details, excessive reprompts, weak fallback path |

If the report uses custom Coval persona labels to represent audio conditions,
map each one to the closest audio-quality condition and state the mapping.

### 5. Recommend Fixes

Recommend specific next steps. Prefer small, testable changes over generic
advice. Separate:
- **Agent prompt changes**: instructions for clarification, concise status,
  read-back, interruption recovery, or escalating uncertainty.
- **Tool handling fixes**: timeout handling, idempotency, retry policy, tool
  result grounding, duplicate-call prevention, or better user-facing status.
- **STT/TTS adjustments**: STT model/config, VAD thresholds, input gain,
  partial/final transcript handling, TTS voice/rate, or artifact mitigation.
- **Trace or metric setup**: add OpenTelemetry traces, trace metrics, or Human
  Review labels when the current evidence cannot explain the failure.
- **Coverage changes**: add more cases or audio conditions only when the
  current data shows a blind spot or the sample size is too thin.

Tie each recommendation to the audio condition, metric delta, call-shape change,
scoreability issue, and representative simulation evidence that motivated it.
If a recommendation cannot be tied to evidence, mark it as a hypothesis and
explain how to validate it.

### 6. Plan The Confirmation Run

End with a small validation plan:
- which fix to try first
- which audio-quality scenario(s) and test cases to rerun
- which metrics should improve
- what regression guard should stay unchanged

Use the same baseline/report structure so the user can compare before and
after.

## Output Format

Return:

```markdown
## Audio Quality Report Analysis

### Executive Summary
- Biggest audio-condition regression:
- Most important call-shape or scoreability anomaly:
- Most likely root cause:
- Highest-confidence next fix:

### Scope And Caveats
- Report/runs analyzed:
- Baseline:
- Missing or weak evidence:

### Audio-Condition Regression Table
| Audio Condition | Main Regression Or Anomaly | Evidence | Likely Cause | Confidence |
|-----------------|----------------------------|----------|--------------|------------|

### Representative Evidence
- Baseline simulation:
- Regression examples:
- UNKNOWN/unscored examples:
- Trace/Human Review evidence:

### Recommended Agent Fixes
1. Fix:
   - Why:
   - Exact change:
   - Validation:

### Confirmation Plan
- Rerun:
- Metrics to watch:
- Pass criteria:
```

Keep the final answer concise enough for a product or engineering owner to act
on. Include links or IDs for report, run, simulation, trace, and Human Review
evidence when available.

## Guardrails

- Do not expose API keys, secrets, or private customer data.
- Do not claim traces explain a result unless trace data was available and
  inspected.
- Do not ignore UNKNOWN, missing, failed, or unscored metrics. Explain whether
  they look like measurement gaps or symptoms of an anomalous conversation.
- Do not treat generated voice quality metrics as STT accuracy metrics, or STT
  metrics as TTS quality metrics.
- Do not recommend changing Coval metrics or tests when the evidence points to
  the user's agent, unless the metric/test setup is genuinely flawed.
- Do not present "expand audio-quality coverage" as the main recommendation
  when the report already shows a clear fixable failure.
