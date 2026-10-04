---
name: analyze-accent-report
description: Analyze a Coval accent testing report from runs across different speaker accents. Use when a user provides a Coval report URL, report export, run IDs, screenshots, or metric summary and wants evidence-backed next steps such as prompt changes, STT/confirmation adjustments, accent-robust routing, or expanded accent coverage.
argument-hint: "[Coval report URL, run IDs, or exported report summary]"
---

# Analyze Accent Report

Turn a Coval accent testing report into a practical agent-fix plan. This skill
assumes the user already ran comparable Coval evaluations across speaker
accents, usually by creating one persona per accent voice and setting the report
to **Compare by Persona**.

If no report or run results exist yet, ask for them. Do not invent results. If
an end-to-end accent workflow skill is installed in the user's environment, use
that workflow first to create the personas, runs, and report (see
[run-accent-testing](../../runs/run-accent-testing/)), then return to this skill
for analysis.

## Inputs

Accept any of:
- Coval report URL or shared report URL
- report export, screenshots, or copied metric table
- Coval run IDs from the same accent testing sweep
- representative simulation links, recordings, transcripts, traces, or Human Review labels

If Coval CLI/API access is available, use it to inspect runs, simulations,
metrics, transcripts, recordings, and traces. If access is not available, work
from the provided report/export and ask only for the smallest missing evidence
needed to avoid guessing.

## Workflow

### 1. Verify The Comparison

Confirm:
- same agent or intentional agent variant
- same test set and sampled cases across accent personas
- same metrics across runs
- all compared runs reached terminal status
- the report is grouped by accent persona, with Standard Customer (or another
  clear neutral baseline) as the comparison point
- each accent persona differs from the baseline **only** by its accent voice
  (same behavior prompt and language); if not, the comparison mixes accent with
  behavior and you must say so

Call out caveats before interpreting results. Common caveats: missing accents,
different test cases, incomplete runs, too few simulations per accent (likely on
this suite, because accent voices are lower-concurrency), changed agent config
between runs, or accent personas whose prompts diverge from the baseline.

### 2. Build Per-Accent Deltas

Compare each accent against the baseline. Lead with speech recognition, since
accent testing is primarily a recognition stress test. Track direction and
magnitude for:

| Area | Typical Signals |
|------|-----------------|
| Speech recognition (headline) | Transcription Error (audio-derived, always available) is the default; use STT WER from traces only after confirming it actually scored — it silently fails when the agent emits no STT spans |
| Task outcome | composite score, task completion, scenario-specific pass/fail metrics |
| Responsiveness | latency, time to first audio, trace TTFB, provider response time |
| Conversation flow | repeated confirmation/clarification loops, repetition, sentiment, turn timing |
| Call shape | turn count, audio duration, early termination, abnormally short or long calls |
| Scoreability | UNKNOWN, missing, failed, or unscored metric results |

Use the metric's natural direction. Lower is better for WER, transcription
error, latency, silence, and confirmation-loop counts. Higher is better for
success, completion, and accuracy metrics.

Do not overfit to one row. Treat one-off failures as hypotheses unless the
metric, transcript, recording, or trace evidence supports the pattern.

Treat UNKNOWN, missing, failed, or unscored metric results as evidence to
inspect, not as data to ignore. Under heavy accent stress, a judge may be unable
to score because the call ended early, the transcript is too sparse, or the
interaction became too anomalous to evaluate.

One specific gap to recognize, not misread: **STT Word Error Rate that is
`FAILED`/empty on nearly every simulation is a tracing gap, not an accent
signal.** That metric only computes when the agent's traces carry STT spans with
a recognized hypothesis and a reference; many voice stacks (Vapi/PSTN especially)
emit no such spans, so it fails uniformly across all personas including the
baseline. When that happens, lead recognition with **Transcription Error**
(audio-derived, needs no traces) and recommend instrumenting STT spans as a
trace-setup fix — do not report the empty STT WER column as if accents scored
poorly on it.

### 3. Inspect Representative Evidence

Open or request representative simulations:
- worst regression for each affected accent
- one healthy baseline simulation
- any surprising metric outlier
- any UNKNOWN, missing, failed, or unscored metric result
- very short calls, very long calls, or early terminations compared with baseline
- cases where binary task metrics passed but the transcript or recording shows
  the agent mis-heard names, numbers, addresses, or other key entities
- Human Review disagreements, if present

For each important example, inspect the transcript and recording when available.
Look specifically for mis-recognized words, wrong entities captured, and extra
confirmation loops the baseline did not need. Use traces when present to
distinguish STT errors from downstream reasoning or tool errors. Separate metric
evidence from listening judgment and label anything that is inferred.

### 4. Diagnose By Accent

Use accent hypotheses, then verify them against evidence:

| Accent | Likely Failure Modes To Check |
|--------|-------------------------------|
| Standard Customer | General agent, test, metric, or tool issue if this baseline also fails |
| Indian Accent (Vidya) | Phoneme/vowel recognition, fast or stressed-syllable speech, mis-captured names and numbers |
| German Accent (Marshal) | Consonant devoicing (final /d/→/t/), vowel shifts, formal phrasing, STT word errors on common terms |
| Chinese Accent (Ziyu) | Tone and final-consonant recognition, mis-heard digits and entities, over-confirmation |
| US Southern Accent (Cletus) | Vowel shifts and drawl, contractions, regional phrasing, STT word errors |
| Nigerian Accent (Kehinde) | Rhythm and stress patterns, vocabulary, mis-captured entities, confirmation loops |
| Malaysian Accent (Darryl) | Syllable-timed rhythm, dropped final consonants, mis-captured entities, confirmation loops |

The shared pattern across accents is the same: check whether the STT layer
mis-transcribes accented speech, whether mis-transcription propagates into wrong
task outcomes, and whether the agent recovers with read-back or clarification.
If the report uses different persona labels, map each one to the closest accent
and state the mapping.

### 5. Recommend Fixes

Recommend specific next steps. Prefer small, testable changes over generic
advice. Separate:
- **Agent prompt changes**: read-back of critical entities (names, numbers,
  addresses), explicit clarification strategy, concise confirmation, and
  escalating uncertainty when recognition confidence is low.
- **STT/recognition adjustments**: STT model/config (e.g. an accent- or
  multilingual-robust model), VAD thresholds, partial/final transcript handling,
  endpointing, or per-language/locale routing.
- **Tool handling fixes**: validate entities captured from speech before acting,
  idempotency, retry policy, and grounding tool results in confirmed values.
- **Trace or metric setup**: add OpenTelemetry traces, STT/trace metrics, or
  Human Review labels when the current evidence cannot explain the failure.
- **Coverage changes**: add more cases or accents only when the current data
  shows a blind spot or the sample size is too thin.

Tie each recommendation to the accent, metric delta, call-shape change,
scoreability issue, and representative simulation evidence that motivated it.
If a recommendation cannot be tied to evidence, mark it as a hypothesis and
explain how to validate it.

### 6. Plan The Confirmation Run

End with a small validation plan:
- which fix to try first
- which accent(s) and test cases to rerun
- which metrics should improve (usually STT WER / transcription error and task
  outcome for the affected accent)
- what regression guard should stay unchanged (the baseline should not get worse)

Use the same baseline/report structure so the user can compare before and after.

## Output Format

Return:

```markdown
## Accent Report Analysis

### Executive Summary
- Biggest accent regression:
- Most important call-shape or scoreability anomaly:
- Most likely root cause:
- Highest-confidence next fix:

### Scope And Caveats
- Report/runs analyzed:
- Baseline:
- Missing or weak evidence (note thin per-accent samples from low concurrency):

### Per-Accent Regression Table
| Accent | Main Regression Or Anomaly | Evidence | Likely Cause | Confidence |
|--------|----------------------------|----------|--------------|------------|

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
- Do not confuse accent comprehension (an STT/recognition problem) with
  generated voice quality (a TTS problem). This suite tests whether the agent
  understands accented callers, not how the agent's own voice sounds.
- Do not recommend changing Coval metrics or tests when the evidence points to
  the user's agent, unless the metric/test setup is genuinely flawed.
- Do not present "expand accent coverage" as the main recommendation when the
  report already shows a clear fixable failure on an existing accent.
- Do not over-read thin samples. Accent voices are lower-concurrency, so each
  accent run may have few simulations — flag small-sample conclusions as
  tentative.
