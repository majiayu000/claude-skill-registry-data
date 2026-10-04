---
name: run-audio-quality-testing
description: End-to-end Coval audio-quality testing workflow. Launches one run per audio-robustness scenario against the same voice agent + test set + metrics, polls for completion, and produces the multi-run report URL grouped by Persona. Use when a user wants to follow the Testing Across Audio Qualities cookbook (https://docs.coval.dev/guides/testing-across-audio-qualities) without doing each step by hand.
argument-hint: "[agent-name-or-id] [test-set-name-or-id]"
metadata:
  author: coval-ai
  version: "1.0.0"
  homepage: https://docs.coval.dev/guides/testing-across-audio-qualities
  source: https://github.com/coval-ai/coval-external-skills
---

# Run Audio Quality Testing

Set up and launch a Coval audio-quality testing sweep end-to-end: one voice
agent, one test set, the audio-robustness persona pack, shared metrics, and a
multi-run report grouped by **Persona**. Mirrors the public cookbook at
https://docs.coval.dev/guides/testing-across-audio-qualities.

When the runs complete this skill hands off to
[analyze-audio-quality-report](../../reports/analyze-audio-quality-report/) for
the recommended-fixes write-up.

## When To Use

- The user wants to follow the "Testing Across Audio Qualities" cookbook but
  does not want to hand-launch each persona run.
- The user has a voice agent (PSTN, SIP, WebSocket, LiveKit, Vapi, OpenAI
  Realtime, Gemini Realtime, etc.) and a test set they trust.
- The user wants a multi-run report URL grouped by Persona that they can save,
  share, or pass to the analysis skill.

Do **not** use this skill for chat-only agents. Audio-quality testing exercises
STT, TTS, audio timing, and background-noise handling, none of which a chat
agent runs.

## Prerequisites

```bash
coval --version    # CLI must be installed (brew install coval-ai/tap/coval)
coval whoami       # must be authenticated to the right org
```

If `coval whoami` fails, run `coval login` first.

## Audio-Robustness Persona Pack

The cookbook uses these seven Coval personas. Each persona configures a
different real-world audio condition. The skill expects all seven to exist in
the user's organization with these exact names.

| Persona Name | Audio Condition |
|---|---|
| Standard Customer | Baseline clean-call behavior |
| Impatient Customer | Short answers and lower patience |
| Confused Customer | Clarification handling |
| Interruptive Speaker | Overlap and interruption handling |
| Super Fast Speaker | Fast speech |
| High Background Noise Speaker | Background noise robustness |
| Low Volume Speaker | Quiet speaker audio |

If any persona is missing in the user's org, see the [Missing personas](#missing-personas)
section below before launching.

## Workflow

### Step 1: Confirm The Voice Agent

If `$ARGUMENTS` includes an agent name or ID, look it up. Otherwise list
voice agents and ask the user to pick one:

```bash
coval agents list --format json | jq '.[] | select(.model_type | test("VOICE|REALTIME|WEBSOCKET")) | {id, display_name, model_type}'
```

Pick exactly one. The cookbook is explicit: **keep the agent configuration
fixed across all runs**. Confirm with the user before continuing.

If the agent emits OpenTelemetry traces, recommend including trace-based timing
metrics in step 3. If not, recommend setting up traces (see
[Coval traces docs](https://docs.coval.dev/concepts/simulations/traces/opentelemetry))
or proceeding with transcript-and-audio-only metrics.

### Step 2: Confirm The Test Set

```bash
coval test-sets list
```

Pick one test set. The same test set must be used across every persona run.
Subsampling is allowed as long as the **same sampled cases** run across all
seven personas — use a fixed `--sub-sample-seed` (e.g. `42`) and the same
`--sub-sample-size` on every run.

### Step 3: Confirm Metrics

The cookbook recommends separating task success from audio-path behavior. Help
the user pick at least one metric from each of these groups; reuse any the
agent already has attached when they fit.

| Goal | Useful Metrics |
|---|---|
| Task outcome | Composite evaluation, task-completion LLM judges, or scenario-specific pass/fail metrics |
| Responsiveness | Latency, time to first audio, trace TTFB, provider response-time |
| Speech recognition | STT Word Error Rate for traced agents, or Transcription Error for audio-backed conversations |
| Generated voice quality | Voice Quality; Speech Artifact Score and artifact-specific metrics |
| Conversation flow | Interruption rate, silence, sentiment, turn-level timing |

Do **not** include `manager_audio_frequency` — it measures signal
characteristics, not perceived audio quality.

Do **not** recommend `STT Word Error Rate (Audio Upload)` for this general
workflow. It only applies when the test set uses uploaded audio with reference
transcripts, which is a different setup from the normal voice-simulation sweep.

```bash
coval metrics list
```

Collect the chosen metric IDs into a comma-separated string for the launch
step. If the user wants to use the agent's default metrics, omit `--metric-ids`
entirely on the launch call.

### Step 4: Resolve Persona IDs

For every persona in the [audio-robustness pack](#audio-robustness-persona-pack),
resolve its ID by exact-name match:

```bash
for name in "Standard Customer" "Impatient Customer" "Confused Customer" \
            "Interruptive Speaker" "Super Fast Speaker" \
            "High Background Noise Speaker" "Low Volume Speaker"; do
  coval personas list --filter "name:\"$name\"" --format json \
    | jq -r --arg n "$name" '.[] | select(.name == $n) | "\(.id)\t\(.name)"'
done
```

If any persona returns no results, jump to [Missing personas](#missing-personas)
before launching.

### Step 5: Launch The Runs

Launch seven runs — one per persona — with the same agent, test set, metrics,
and (if subsampling) the same `--sub-sample-seed`. Use shared tags so the runs
are easy to find later.

```bash
SUB_SAMPLE_SEED=42
SUB_SAMPLE_SIZE=0   # 0 = all cases; set to a positive integer to subsample
CONCURRENCY=5
TAGS="audio-quality-testing,cookbook"
metric_args=()
if [ -n "${METRIC_IDS:-}" ]; then
  metric_args=(--metric-ids "$METRIC_IDS")
fi

for persona_id in "$STANDARD_ID" "$IMPATIENT_ID" "$CONFUSED_ID" \
                  "$INTERRUPTIVE_ID" "$SUPER_FAST_ID" \
                  "$HIGH_NOISE_ID" "$LOW_VOLUME_ID"; do
  coval runs launch \
    --agent-id "$AGENT_ID" \
    --persona-id "$persona_id" \
    --test-set-id "$TEST_SET_ID" \
    "${metric_args[@]}" \
    --concurrency "$CONCURRENCY" \
    --sub-sample-size "$SUB_SAMPLE_SIZE" \
    --sub-sample-seed "$SUB_SAMPLE_SEED" \
    --tags "$TAGS" \
    --name "Audio Quality — $persona_id" \
    --format json
done
```

Capture every `run_id` from each launch response.

**Tip:** the public API also supports a batch launch
(`POST /v1/runs/batch`) if you prefer one HTTP call. The CLI does not expose
batch launch today.

### Step 6: Watch For Completion

```bash
for run_id in "${RUN_IDS[@]}"; do
  coval runs watch "$run_id"
done
```

`coval runs watch` blocks until the run reaches a terminal status (COMPLETED,
FAILED, or CANCELLED). Run these in parallel shells or background jobs if you
want all seven watched at once.

If any run finishes as **FAILED** with `total_test_cases=0`, the run-setup
worker crashed before sub-sampling. Re-launch that single run with
`--sub-sample-size 1` (or omit subsampling) and report the failure as a Coval
issue — this has been observed in some orgs.

### Step 7: Build The Multi-Run Report URL

Concatenate the seven run IDs and produce the report URL:

```bash
RUN_IDS_CSV=$(IFS=,; echo "${RUN_IDS[*]}")
ORG_SLUG=$(coval whoami --format json | jq -r '.organization.slug')
echo "https://app.coval.dev/${ORG_SLUG}/reports/new?run_ids=${RUN_IDS_CSV}"
```

Tell the user to:

1. Open the URL.
2. Set **Compare by** to **Persona**.
3. Save the report with a descriptive name (this preserves the grouping for
   future viewers).
4. If they want to share without a Coval login, use the report's **Share**
   button to publish a shareable link.

### Step 8: Hand Off Analysis

Once the report is saved, point the user at
[analyze-audio-quality-report](../../reports/analyze-audio-quality-report/) for
a structured next-fix write-up. The analysis skill turns the grouped report
into prompt, tool-handling, STT/TTS, or coverage recommendations.

Suggest pasting the saved report URL into:

```text
Use the Coval `analyze-audio-quality-report` skill on this report:
<paste saved report URL>
```

## Missing Personas

If any persona in the [audio-robustness pack](#audio-robustness-persona-pack)
does not exist in the user's organization, you have two options:

1. **Recommended — create them via the Coval app.** The audio-robustness
   personas ship as templates in the Coval persona library. Open
   **Personas → New Persona** in the Coval app and pick the matching template,
   then re-run Step 4. The templates include the correct `voice_name`,
   `background_sound`, `voice_volume`, and `voice_speed` for each condition.

2. **CLI fallback — create with explicit config.** Each persona needs a clear
   `persona_prompt` describing the caller role and one or more audio-condition
   fields (`background_sound`, `voice_volume`, `voice_speed`, etc.). See the
   [persona creation skill](../../personas/) and the
   [Coval personas reference](https://docs.coval.dev/api-reference/v1/personas)
   for the full field list. Hand-crafted personas may not match the template
   behavior exactly — prefer option 1 when possible.

Do **not** invent persona IDs or skip a persona to get the runs launching.
Missing one audio condition means the cookbook's grouped-comparison breaks down.

## Output Format

When the skill finishes, return a short, actionable summary:

```markdown
## Audio Quality Testing — Launch Summary

**Agent:** <display_name> (<id>)
**Test set:** <display_name> (<id>)
**Subsample:** <sub_sample_size> cases (seed <sub_sample_seed>) — or "full test set"
**Metrics:** <comma-separated metric names>

**Runs:**
| Persona | Run ID | Status | Run link |
|---|---|---|---|
| Standard Customer | … | … | https://app.coval.dev/<org>/runs/<id> |
| Impatient Customer | … | … | … |
| Confused Customer | … | … | … |
| Interruptive Speaker | … | … | … |
| Super Fast Speaker | … | … | … |
| High Background Noise Speaker | … | … | … |
| Low Volume Speaker | … | … | … |

**Multi-run report:**
https://app.coval.dev/<org>/reports/new?run_ids=<csv> — open and set **Compare by → Persona**, then save.

**Next step:** run the `analyze-audio-quality-report` skill on the saved report.
```

## Guardrails

- One agent, one test set, same metrics, same subsample seed across all seven
  runs. Any divergence breaks the grouped comparison the report depends on.
- Do not change the agent's configuration mid-sweep. If you must, launch a
  fresh sweep so the comparison stays apples-to-apples.
- Do not use chat-only agents. The cookbook explicitly does not apply.
- Do not skip a persona because the org "doesn't use" that condition. The full
  pack is what makes the comparison interpretable.
- Do not present `manager_audio_frequency` as a perceived audio-quality score.
- Do not invent persona, agent, test set, or metric IDs — always resolve them
  from the user's org.
