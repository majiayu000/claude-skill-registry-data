---
name: run-accent-testing
description: End-to-end Coval accent testing workflow. Creates one persona per accent (each using a distinct accent voice and mirroring your Standard Customer behavior), launches one run per accent against the same voice agent + test set + metrics, polls for completion, builds a per-persona comparison table from the results, and creates the saved multi-run report (grouped by Persona) via the public API. Use when a user wants to follow the Testing Across Accents cookbook (https://docs.coval.dev/guides/testing-across-accents) without doing each step by hand.
argument-hint: "[agent-name-or-id] [test-set-name-or-id]"
metadata:
  author: coval-ai
  version: "1.0.0"
  homepage: https://docs.coval.dev/guides/testing-across-accents
  source: https://github.com/coval-ai/coval-external-skills
---

# Run Accent Testing

Set up and launch a Coval accent testing sweep end-to-end: one voice agent, one
test set, an accent persona pack, shared metrics, a per-persona comparison table
built from the results, and a saved multi-run report grouped by **Persona**
(created for you via the API). Mirrors the public cookbook at
https://docs.coval.dev/guides/testing-across-accents.

Unlike the audio-quality pack, **the accent personas are not built-in**. This
skill creates them in the user's organization, one per accent voice, and makes
each one mirror the org's **Standard Customer** behavior so the only variable
between runs is the speaker's accent.

When the runs complete this skill hands off to
[analyze-accent-report](../../reports/analyze-accent-report/) for the
recommended-fixes write-up.

## When To Use

- The user wants to follow the "Testing Across Accents" cookbook but does not
  want to hand-create personas and hand-launch each run.
- The user has a voice agent (PSTN, SIP, WebSocket, LiveKit, Vapi, OpenAI
  Realtime, Gemini Realtime, etc.) and a test set they trust.
- The user wants a saved multi-run report grouped by Persona (created via the
  API) that they can open, share, or pass to the analysis skill.

Do **not** use this skill for chat-only agents. Accent testing exercises speech
recognition (STT) and audio timing, none of which a chat agent runs.

## Prerequisites

```bash
coval --version    # CLI must be installed (brew install coval-ai/tap/coval)
coval whoami       # must be authenticated to the right org
```

If `coval whoami` fails, run `coval login` first.

## Accent Persona Pack

The cookbook compares one neutral baseline against six accent personas. Each
accent persona uses a distinct accent voice; every other setting mirrors the
baseline so differences come from the accent, not behavior.

| Persona Name | `--voice` | Accent |
|---|---|---|
| Standard Customer | (built-in baseline) | Neutral baseline |
| Indian Accent (Vidya) | `vidya` | Indian |
| German Accent (Marshal) | `marshal` | German-accented |
| Chinese Accent (Ziyu) | `ziyu` | Chinese-accented |
| US Southern Accent (Cletus) | `cletus` | US Southern |
| Nigerian Accent (Kehinde) | `kehinde` | Nigerian |
| Malaysian Accent (Darryl) | `darryl` | Malaysian |

> **Low concurrency is expected.** All six accent voices are lower-concurrency
> ElevenLabs voices, and ElevenLabs voice simulations are globally capped per
> organization. Launch these runs at a **low `--concurrency` (2 is a safe
> default)** and expect simulations to queue and finish more slowly than a
> standard sweep. This is normal for this suite — it is not a failure.

## Workflow

### Step 1: Confirm The Voice Agent

If `$ARGUMENTS` includes an agent name or ID, look it up. Otherwise list voice
agents and ask the user to pick one:

```bash
coval agents list --format json | jq '.[] | select(.model_type | test("VOICE|REALTIME|WEBSOCKET")) | {id, display_name, model_type}'
```

Pick exactly one. The cookbook is explicit: **keep the agent configuration
fixed across all runs**. Confirm with the user before continuing.

If the agent emits OpenTelemetry traces, recommend including trace-based STT and
timing metrics in step 3. If not, recommend setting up traces (see
[Coval traces docs](https://docs.coval.dev/concepts/simulations/traces/opentelemetry))
or proceeding with transcript-and-audio-only metrics such as Transcription
Error.

### Step 2: Confirm The Test Set

```bash
coval test-sets list
```

Pick one test set. The same test set must be used across every persona run.
Subsampling is allowed as long as the **same sampled cases** run across all
seven personas — use a fixed `--sub-sample-seed` (e.g. `42`) and the same
`--sub-sample-size` on every run.

### Step 3: Confirm Metrics

Accent testing is primarily a **speech-recognition** stress test: does the agent
correctly understand accented speech, and does any mis-recognition change the
task outcome? Lead with STT, then task outcome and call shape. Reuse any metrics
the agent already has attached when they fit.

| Goal | Useful Metrics |
|---|---|
| Speech recognition (headline) | Transcription Error (audio-derived, needs no traces) is the default; add STT Word Error Rate only after confirming the agent emits STT trace spans and the metric actually scores — otherwise it silently fails |
| Task outcome | Composite evaluation, task-completion LLM judges, or scenario-specific pass/fail metrics |
| Responsiveness | Latency, time to first audio, trace TTFB, provider response-time |
| Conversation flow | Turn count, repeated confirmation/clarification loops, early termination, silence, interruption rate |

Do **not** include `manager_audio_frequency` — it measures signal
characteristics, not accent comprehension.

Do **not** recommend `STT Word Error Rate (Audio Upload)` for this general
workflow. It only applies when the test set uses uploaded audio with reference
transcripts, which is a different setup from the normal voice-simulation sweep.

> **STT Word Error Rate needs the right trace spans, or it silently fails.**
> The trace-based `STT Word Error Rate` metric only computes when the agent's
> OpenTelemetry traces carry STT spans with both the recognized hypothesis and a
> reference value. Many voice stacks — Vapi/PSTN agents in particular — do not
> emit those spans, in which case this metric comes back `FAILED`/empty on
> nearly every simulation. That is a **trace-setup gap, not an accent finding**.
> Always include **Transcription Error** (audio-derived word error rate, needs no
> traces) as the reliable recognition headline, and only rely on `STT Word Error
> Rate` after you have confirmed it scores on a real run for this agent.

Recognition that works **without agent traces** (the common case — most agents,
Vapi/PSTN/Pipecat included, emit no STT spans) is **Transcription Error**: a
Coval built-in that re-transcribes the recording with its own STT and scores word
error rate, so it needs no traces. It is a built-in (`organization_id=NULL`) and
can be **paged out of a plain `coval metrics list`**, so resolve it by name —
note the metrics filter uses `=`, not the `:` personas use:

```bash
# Recognition metric that needs no traces — always attach this.
TRANSCRIPTION_ERROR_ID=$(coval metrics list --include-builtin --page-size 100 \
  --filter 'metric_name="Transcription Error"' --format json \
  | jq -r '.[] | select(.metric_name == "Transcription Error") | .id' | head -1)

# Browse task-outcome / responsiveness / flow metrics; reuse the agent's
# attached metrics when they fit.
coval metrics list --include-builtin
```

Build `METRIC_IDS` as a comma-separated string with **Transcription Error first**,
then the task-outcome and call-shape metric IDs you chose. **Always attach a
working recognition metric — measuring recognition is the entire point of an
accent sweep.** Do **not** just omit `--metric-ids` to fall back on the agent's
defaults: many agents have no metrics attached (or none that measure
recognition), so the sweep would score everything *except* the thing it exists to
test. Add `STT Word Error Rate` only *in addition* (never instead), and only
after confirming the agent emits STT trace spans and it actually scores.

### Step 4: Ensure The Accent Personas Exist

The accent personas are not built-in, so create any that are missing. Make each
one mirror the org's **Standard Customer** so the only variable is the accent
voice.

First resolve Standard Customer and read its behavior prompt and wait time so the
accent personas can mirror them:

```bash
STD_ID=$(coval personas list --filter 'name:"Standard Customer"' --format json \
  | jq -r '.[] | select(.name == "Standard Customer") | .id' | head -1)

STD_PROMPT=""
STD_WAIT=""
if [ -n "$STD_ID" ]; then
  STD=$(coval personas get "$STD_ID" --format json)
  STD_PROMPT=$(echo "$STD" | jq -r '.persona_prompt // ""')
  STD_WAIT=$(echo "$STD"   | jq -r '.wait_seconds // ""')
fi

# Fallbacks if Standard Customer is missing or has no prompt/wait time.
if [ -z "$STD_PROMPT" ] || [ "$STD_PROMPT" = "null" ]; then
  STD_PROMPT="You are a standard customer calling in with a routine request. Speak naturally and conversationally. Answer the agent's questions, provide the information it asks for, and work toward completing your task."
fi
if [ -z "$STD_WAIT" ] || [ "$STD_WAIT" = "null" ]; then
  STD_WAIT="0.5"
fi

# IMPORTANT: do NOT reuse Standard Customer's language code for the accent
# personas. Accent voices are locale-bound and most do NOT accept en-US, so
# `coval personas create` rejects the pair with
# "Voice 'X' does not support language 'Y'". Supported languages per voice:
#   vidya  en, en-IN     marshal en, en-GB    ziyu   en, en-GB
#   cletus en, en-US     kehinde en (only)    darryl en (only)
# The one language all six accent voices share is the base "en", so use "en" for
# every accent persona. A single shared language keeps the accent voice the only
# variable. (If you specifically want an accent-native locale, map each voice to
# a code it supports above instead — but then language co-varies with accent.)
ACCENT_LANG="en"
```

Then create each accent persona only if an exact-name match does not already
exist (idempotent — never create duplicates):

```bash
# "Persona Name|voice" — the voice is the Coval catalog name.
ACCENTS=(
  "Indian Accent (Vidya)|vidya"
  "German Accent (Marshal)|marshal"
  "Chinese Accent (Ziyu)|ziyu"
  "US Southern Accent (Cletus)|cletus"
  "Nigerian Accent (Kehinde)|kehinde"
  "Malaysian Accent (Darryl)|darryl"
)

for entry in "${ACCENTS[@]}"; do
  name="${entry%%|*}"
  voice="${entry##*|}"

  existing=$(coval personas list --filter "name:\"$name\"" --format json \
    | jq -r --arg n "$name" '.[] | select(.name == $n) | .id' | head -1)

  if [ -n "$existing" ]; then
    echo "exists: $name ($existing)"
    continue
  fi

  echo "creating: $name (voice: $voice)"
  coval personas create \
    --name "$name" \
    --voice "$voice" \
    --language "$ACCENT_LANG" \
    --prompt "$STD_PROMPT" \
    --wait-seconds "$STD_WAIT" \
    --format json
done
```

Notes:

- The `--voice` value is the lowercase Coval catalog name (`vidya`, `marshal`,
  `ziyu`, `cletus`, `kehinde`, `darryl`), not the display label.
- Use the **same** `--prompt`, the same `--wait-seconds`, and the shared `en`
  language for every accent persona so the accent voice is the only thing that
  changes between runs. Do not pass Standard Customer's `en-US` to an accent
  voice — most accent voices reject it (see the language note above).
- `coval personas create` does not expose `conversation_initiation` or
  `background_sound`, so new personas take the defaults. If your Standard
  Customer overrides either, the accent personas will differ on that secondary
  setting — note it, or set those fields in the app for a pixel-perfect mirror.
- Do not overwrite an existing persona. If one already exists with a different
  voice or prompt, tell the user and let them decide — do not silently recreate.

### Step 5: Resolve Persona IDs

Resolve all seven persona IDs by exact-name match (Standard Customer plus the
six accent personas) into ordered arrays the launch step reuses. Keep Standard
Customer first so it is the baseline column in the report:

```bash
# Canonical persona order — Standard Customer first (baseline).
PERSONA_NAMES=(
  "Standard Customer"
  "Indian Accent (Vidya)"
  "German Accent (Marshal)"
  "Chinese Accent (Ziyu)"
  "US Southern Accent (Cletus)"
  "Nigerian Accent (Kehinde)"
  "Malaysian Accent (Darryl)"
)

PERSONA_IDS=()
for name in "${PERSONA_NAMES[@]}"; do
  id=$(coval personas list --filter "name:\"$name\"" --format json \
    | jq -r --arg n "$name" '.[] | select(.name == $n) | .id' | head -1)
  if [ -z "$id" ]; then
    echo "MISSING persona: $name — resolve Step 4 before launching" >&2
    exit 1
  fi
  PERSONA_IDS+=("$id")
  echo "$id  $name"
done
```

If any persona is still missing after Step 4, the loop stops — fix it before
launching. Do not skip an accent.

### Step 6: Launch The Runs

Launch seven runs — one per persona — with the same agent, test set, metrics,
and (if subsampling) the same `--sub-sample-seed`. Keep `--concurrency` low
because these are lower-concurrency voices. Use shared tags so the runs are easy
to find later.

```bash
SUB_SAMPLE_SEED=42
SUB_SAMPLE_SIZE=0   # 0 = all cases; set to a positive integer to subsample
CONCURRENCY=2       # low on purpose — accent voices are lower-concurrency
TAGS="accent-testing,cookbook"
metric_args=()
if [ -n "${METRIC_IDS:-}" ]; then
  metric_args=(--metric-ids "$METRIC_IDS")
fi

# Uses PERSONA_NAMES / PERSONA_IDS from Step 5; captures each run_id into RUN_IDS.
RUN_IDS=()
for i in "${!PERSONA_IDS[@]}"; do
  persona_id="${PERSONA_IDS[$i]}"
  persona_name="${PERSONA_NAMES[$i]}"
  resp=$(coval runs launch \
    --agent-id "$AGENT_ID" \
    --persona-id "$persona_id" \
    --test-set-id "$TEST_SET_ID" \
    "${metric_args[@]}" \
    --concurrency "$CONCURRENCY" \
    --sub-sample-size "$SUB_SAMPLE_SIZE" \
    --sub-sample-seed "$SUB_SAMPLE_SEED" \
    --tags "$TAGS" \
    --name "Accent — $persona_name" \
    --format json)
  run_id=$(echo "$resp" | jq -r '.run_id // .id')
  RUN_IDS+=("$run_id")
  echo "launched $persona_name -> $run_id"
done
```

The loop appends each launched `run_id` to `RUN_IDS`, which Step 7 watches and
Step 8 turns into the report URL.

**Tip:** the public API also supports a batch launch (`POST /v1/runs/batch`) if
you prefer one HTTP call. The CLI does not expose batch launch today.

### Step 7: Watch For Completion

```bash
for run_id in "${RUN_IDS[@]}"; do
  coval runs watch "$run_id"
done
```

`coval runs watch` blocks until the run reaches a terminal status (COMPLETED,
FAILED, or CANCELLED). Because the accent voices are lower-concurrency,
simulations may queue and the sweep may take longer than a standard run — that
is expected. Run these in parallel shells or background jobs if you want all
seven watched at once.

If any run finishes as **FAILED** with `total_test_cases=0`, the run-setup
worker crashed before sub-sampling. Re-launch that single run with
`--sub-sample-size 1` (or omit subsampling) and report the failure as a Coval
issue — this has been observed in some orgs.

### Step 8: Build The Persona Comparison Table

The report URL in Step 9 opens Coval's report builder, but the grouping is a
manual UI step, so it does not by itself hand the user a comparison. **The user
asked for a report comparing the personas — produce that comparison here**,
directly from the API, so they get a ready-to-read artifact without touching the
app. For every run, list its simulations, pull each simulation's metric values,
and aggregate per persona:

```bash
# Map metric_id -> name once (include built-ins like Transcription Error).
coval metrics list --include-builtin --page-size 100 --format json \
  | jq -r '.[] | "\(.id)\t\(.metric_name // .name)"' > /tmp/accent_metric_names.tsv

# Gather every simulation's metric values across all runs.
: > /tmp/accent_metrics.jsonl
for i in "${!RUN_IDS[@]}"; do
  run_id="${RUN_IDS[$i]}"
  persona="${PERSONA_NAMES[$i]}"
  coval simulations list --run-id "$run_id" --format json \
    | jq -r '.[].simulation_id' \
    | while read -r sid; do
        coval simulations metrics "$sid" --format json \
          | jq -c --arg p "$persona" --arg s "$sid" \
              '.[] | {persona:$p, sim:$s, metric_id:.metric_id, status:.status, value:.value}' \
          >> /tmp/accent_metrics.jsonl
      done
done
```

Then aggregate per persona per metric and print one Markdown table the user can
read directly — **pass rate** (YES / total) for binary judges, **mean** for
numeric metrics — ordered Standard Customer first and **leading with the
recognition metrics** (Transcription Error, then STT Word Error Rate only if it
actually scored), then task-outcome judges, then call-shape metrics:

| Metric (direction) | Standard | Indian | German | Chinese | Southern | Nigerian | Malaysian |
|---|---|---|---|---|---|---|---|
| Transcription Error (lower=better) | 0.04 | 0.03 | 0.02 | 0.03 | 0.04 | 0.03 | 0.03 |
| Conversation Success (higher=better) | 100% | 80% | 80% | 100% | 100% | 80% | 80% |
| … | | | | | | | |

Rules for the table:

- Mark any metric that is `FAILED`/missing on most simulations as a **measurement
  gap, not a result** — flag it and exclude it from the regression call-outs.
  `STT Word Error Rate` is commonly all-`FAILED` when the agent emits no STT
  trace spans (see Step 3); say so rather than reporting it as 0 or as an accent
  signal.
- Call out the largest per-accent deltas vs Standard Customer, but **do not
  over-read thin samples** — with a small test set each accent run has few
  simulations, so treat single-case swings as hypotheses to confirm in Step 10,
  not conclusions.
- Before blaming the accent, check whether Standard Customer regressed on the
  same metric/case too. A failure the neutral baseline also hits is an agent,
  tool, or judge issue, not an accent issue.

### Step 9: Create The Saved Report (grouped by Persona)

Create the saved multi-run report directly through the public API so it lands in
the org's Reports section **already grouped by Persona** — no manual builder
step. The CLI has no `reports` command yet, so call the API directly (a `coval
reports create` command would be a good follow-up). Use the same API key your
`coval` CLI is authenticated with.

```bash
# Resolve ORG_SLUG from the agent/test-set app URL the user gave you, e.g.
# https://app.coval.dev/acme-co/agents/AbC123 -> ORG_SLUG=acme-co.
ORG_SLUG="${ORG_SLUG:?set ORG_SLUG to the org slug from the Coval app URL}"

# Build the run-id JSON array from the RUN_IDS bash array (Step 6).
RUN_IDS_JSON=$(printf '%s\n' "${RUN_IDS[@]}" | jq -R . | jq -s -c .)

resp=$(curl -s -X POST "https://api.coval.dev/v1/reports" \
  -H "x-api-key: ${COVAL_API_KEY:?use the API key your coval CLI is authenticated with}" \
  -H "content-type: application/json" \
  -d "$(jq -nc --arg name "Accent sweep — $(date +%F)" --argjson run_ids "$RUN_IDS_JSON" \
        '{name: $name, run_ids: $run_ids, compare_by: "persona"}')")

REPORT_ID=$(echo "$resp" | jq -r '.report.id // empty')
if [ -n "$REPORT_ID" ]; then
  echo "Saved report: https://app.coval.dev/${ORG_SLUG}/reports/${REPORT_ID}"
else
  echo "Report not created (response: $resp)" >&2
fi
```

`compare_by: "persona"` persists `view_config.compareBy=persona`, so the saved
report **opens already grouped by Persona** at
`https://app.coval.dev/<org>/reports/<id>`. The default is `PRIVATE`; pass
`"permissions": "PUBLIC"` only if the user wants a login-free shareable link
(that also marks the included runs public).

**Fallback — if `POST /v1/reports` returns 404** (an older Coval without the
reports API), emit the report **builder** URL and have the user group + save by
hand instead:

```bash
RUN_IDS_CSV=$(IFS=,; echo "${RUN_IDS[*]}")
echo "https://app.coval.dev/${ORG_SLUG}/reports/new?run_ids=${RUN_IDS_CSV}"
# Open it, set Compare by -> Persona (default is None), then Save.
```

The Step 8 table already gives the user the persona comparison inline; this saved
report is the interactive, shareable version of the same data.

### Step 10: Hand Off Analysis

Once the comparison table and report exist, point the user at
[analyze-accent-report](../../reports/analyze-accent-report/) for a structured
next-fix write-up. The analysis skill turns the grouped report into prompt,
STT/confirmation, routing, or coverage recommendations.

Suggest pasting the saved report URL into:

```text
Use the Coval `analyze-accent-report` skill on this report:
<paste saved report URL>
```

## Output Format

When the skill finishes, return a short, actionable summary:

```markdown
## Accent Testing — Launch Summary

**Agent:** <display_name> (<id>)
**Test set:** <display_name> (<id>)
**Subsample:** <sub_sample_size> cases (seed <sub_sample_seed>) — or "full test set"
**Metrics:** <comma-separated metric names>
**Personas created this run:** <list, or "none — all already existed">

**Runs:**
| Persona | Voice | Run ID | Status | Run link |
|---|---|---|---|---|
| Standard Customer | (baseline) | … | … | https://app.coval.dev/<org>/runs/<id> |
| Indian Accent (Vidya) | vidya | … | … | … |
| German Accent (Marshal) | marshal | … | … | … |
| Chinese Accent (Ziyu) | ziyu | … | … | … |
| US Southern Accent (Cletus) | cletus | … | … | … |
| Nigerian Accent (Kehinde) | kehinde | … | … | … |
| Malaysian Accent (Darryl) | darryl | … | … | … |

**Persona comparison (from Step 8 — recognition metrics first, baseline first):**
| Metric (direction) | Standard | Indian | German | Chinese | Southern | Nigerian | Malaysian |
|---|---|---|---|---|---|---|---|
| Transcription Error (↓) | … | … | … | … | … | … | … |
| <task-outcome judge> (↑) | … | … | … | … | … | … | … |
| … | | | | | | | |

**Largest deltas vs Standard:** <one line per notable accent delta, or "none — all accents within noise of baseline">. Note any `FAILED`/missing metrics as measurement gaps, and flag small-sample (few-sims-per-accent) conclusions as tentative.

**Saved report (grouped by Persona):**
https://app.coval.dev/<org>/reports/<id> — created via `POST /v1/reports` (`compare_by: persona`); opens already grouped. (Fallback if the reports API was unavailable: the builder URL `…/reports/new?run_ids=<csv>` + a manual Compare-by-Persona save.)

**Next step:** run the `analyze-accent-report` skill on the saved report.
```

## Guardrails

- One agent, one test set, same metrics, same subsample seed across all seven
  runs. Any divergence breaks the grouped comparison the report depends on.
- Make every accent persona mirror Standard Customer's prompt and wait time, and
  give them all the same shared `en` language, so the accent voice is the only
  variable. Do not copy Standard Customer's `en-US` onto an accent voice — most
  accent voices reject it; `en` is the one code all six accept.
- STT Word Error Rate only scores when the agent emits STT trace spans. If it
  comes back `FAILED`/empty across the sweep, report it as a trace-setup gap and
  lean on Transcription Error — never present an unscored metric as a result.
- Always hand the user the Step 8 persona-comparison table. A bare report-builder
  URL is not the comparison they asked for; the grouped view is a manual UI step.
- Create accent personas only when an exact-name match is missing. Never create
  duplicates, and never silently overwrite an existing persona.
- Keep `--concurrency` low and expect queueing — these are lower-concurrency
  voices. Slow completion is expected, not a failure.
- Do not change the agent's configuration mid-sweep. If you must, launch a fresh
  sweep so the comparison stays apples-to-apples.
- Do not use chat-only agents. The cookbook explicitly does not apply.
- Do not skip an accent because the org "doesn't serve" that population. The full
  pack is what makes the comparison interpretable.
- Do not invent persona, agent, test set, or metric IDs — always resolve them
  from the user's org.
