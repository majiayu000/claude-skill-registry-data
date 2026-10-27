---
name: autoresearch:plan
description: |
  7-step setup wizard that produces a complete, ready-to-run research.md without
  executing the research loop. Walks the user through goal, metric, search space,
  constraints, evaluator design, and baseline measurement, then writes the file.
  TRIGGER when: user wants to set up a research project; user wants to plan before
  running the loop; user says "plan my research"; user has a goal but no research.md;
  user invokes /autoresearch:plan.
  DO NOT TRIGGER when: research.md already exists and the user wants to run the loop;
  user wants a one-shot answer; user wants to debug, not optimize.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# autoresearch:plan — Research Setup Wizard

A 7-step interview that produces a complete `research.md` (and optionally `evaluate.py`) before a single experiment runs. The wizard is conversational — ask each step, wait for the answer, then proceed. Do not batch all questions at once.

## Wizard Protocol

**One step at a time.** Present the step title and question(s). Wait for the user's response. Summarize what you recorded ("Got it — I'll set metric: accuracy, direction: maximize"). Then proceed to the next step.

**Do not skip steps.** Each step produces a concrete artifact that feeds Step 7. If the user's answer is vague, probe once for specificity, then record your best interpretation and note it as an assumption.

---

## Step 1 — Goal Clarification

**Probe for specificity. Vague goals produce useless research loops.**

Ask:
1. "What are you trying to improve or discover?"
2. "What does success look like in concrete terms — not 'better', but what number or outcome?"
3. "Is there anything this work must NOT break?"

**Probe rules:**
- If the answer contains words like "better", "faster", "improve" without a reference point → ask "compared to what baseline?"
- If no domain is mentioned → ask "what system/file/model/prompt are we working on?"
- If multiple goals are stated → ask "if you could only achieve one of these, which one?"

**Record:** `goal_statement` (1-2 sentences, specific and measurable)

---

## Step 2 — Metric Definition

**What to measure, how to measure it, and what direction counts as progress.**

Ask:
1. "What is the single number that determines if this experiment succeeded or failed?"
2. "Are you maximizing or minimizing it?"
3. "What value would make you stop and say 'we're done'? That's the target."
4. "Is this metric noisy? (e.g., varies between runs due to randomness or timing)"

**Guide the user if stuck:**
- Performance → latency (ms), throughput (req/s), memory (MB) — direction: minimize
- Quality → accuracy (%), F1, LLM-judge score (1-10) — direction: maximize
- Cost → tokens, dollars, lines of code — direction: minimize

**Record:** `metric_name`, `direction` (maximize/minimize), `target_value`, `noise_runs` (1 if deterministic, 3-5 if noisy)

---

## Step 3 — Search Space Mapping

**Enumerate what can change and, critically, what must not.**

Ask:
1. "What files, parameters, configs, or components can the agent modify?"
2. "What must never change? (test sets, APIs, data formats, production files)"
3. "Are there any values with hard limits? (e.g., latency must never exceed 2s even if the metric improves)"

**Probe rules:**
- If the allowed scope is very broad → ask "can you narrow it? Broad search spaces waste iterations."
- If no forbidden list is given → explicitly confirm: "So the agent has free rein except for what you just listed — is that right?"

**Record:** `allowed_changes` (bullet list), `forbidden_changes` (bullet list), `guard` (optional hard constraint)

---

## Step 4 — Constraint Elicitation

**Scope the loop before it starts.**

Ask:
1. "How many iterations should the agent run? (default: 20 — more = more thorough, takes longer)"
2. "Do you want the agent to pause for your review at any point, or run fully unattended?"
3. "Any resource limits? (time per experiment, memory, API rate limits, cost caps)"

**If the user wants overnight/unattended:**
- Set `pause_every: never`
- Suggest: `nohup bash scripts/autoresearch-loop.sh ./research-dir/ > autoresearch.log 2>&1 &`
- Remind: "You can monitor progress anytime with `bash scripts/check_progress.sh`"

**If the user wants periodic reviews:**
- Ask: "Every how many iterations?" → set `pause_every: N`

**Record:** `max_iterations`, `pause_every`, `time_budget_per_experiment` (default: 5 minutes), any resource constraints

---

## Step 5 — Evaluator Design

**Can measurement be automated? This determines loop speed and quality.**

Ask: "Can the success metric be measured by running a script? For example, `python evaluate.py` that outputs a number."

### If YES — help write the evaluator:

Guide the user to produce a script that prints:
```json
{"pass": true, "score": 0.94}
```

Ask clarifying questions:
- "Where is the test data / benchmark?"
- "What command runs the current implementation?"
- "What command extracts the metric from the output?"

Offer to write a `evaluate.py` starter template based on their answers. Use the appropriate example from below as a starting point, adapt it to their domain, and write it to the research directory.

**Template — timing/benchmark (minimize):**
```python
#!/usr/bin/env python3
import json, subprocess, statistics, time
times = []
for _ in range(3):
    t0 = time.perf_counter()
    subprocess.run(["python", "TARGET_SCRIPT.py"], check=True)
    times.append(time.perf_counter() - t0)
median = statistics.median(times)
print(json.dumps({"pass": median < TARGET_VALUE, "score": median}))
```

**Template — accuracy/quality (maximize):**
```python
#!/usr/bin/env python3
import json, subprocess
result = subprocess.run(["python", "test_suite.py"], capture_output=True, text=True)
score = float(result.stdout.strip().split("score:")[-1].strip())
print(json.dumps({"pass": score > TARGET_VALUE, "score": score}))
```

**Keep policy:** Ask: "Keep only if strictly better than best so far (`score_improvement`), or keep anything that passes the threshold (`pass_only`)?"

### If NO — record manual evaluation:

Note in research.md: `Evaluator: _(none — agent judges manually)_`

Explain: "The agent will evaluate each experiment using its own judgment. This is slower and less reliable than a script — consider adding a script later."

**Record:** `evaluator_command` (or `none`), `keep_policy`

---

## Step 6 — Baseline Measurement (Dry-Run Verify Gate)

**Run the evaluator NOW to establish iteration 0. This is mandatory before writing research.md.**

If an evaluator was designed in Step 5:

```bash
# Run the evaluator dry run
python evaluate.py
```

**Expected output:** a JSON line like `{"pass": true, "score": 0.73}`

**If the evaluator runs successfully:**
- Record the score as the baseline (iteration 0)
- Say: "Baseline confirmed: [metric_name] = [score]. This is your iteration 0."
- Proceed to Step 7.

**If the evaluator fails (non-zero exit, invalid JSON, crash):**
- Do NOT proceed to Step 7.
- Diagnose the error: read the stderr, identify the cause.
- Fix `evaluate.py` and re-run.
- Repeat until the evaluator runs cleanly.
- Only then proceed to Step 7.

If no evaluator (manual evaluation):
- Ask the user to measure the current state manually: "Before we start, what is the current value of [metric_name]?"
- Record their answer as the baseline.
- Proceed to Step 7.

**Record:** `baseline_score` (iteration 0 value)

---

## Step 7 — research.md Generation

**Write the fully populated research.md using all recorded values.**

If `scripts/init_research.py` is available:

```bash
python scripts/init_research.py \
  --goal "GOAL_STATEMENT" \
  --metric "METRIC_NAME" \
  --direction "DIRECTION" \
  --target "TARGET_VALUE" \
  --evaluator "EVALUATOR_COMMAND" \
  --output ./research-dir/
```

If the script is not available, write `research.md` directly using this structure:

```markdown
# Research: GOAL_TITLE

## Goal
GOAL_STATEMENT

## Success Metric
- **Metric:** METRIC_NAME
- **Target:** TARGET_VALUE
- **Direction:** DIRECTION

## Constraints
- **Max iterations:** MAX_ITERATIONS
- **Time budget per experiment:** 5 minutes
- **Pause for review every:** PAUSE_EVERY
- **Evaluator:** EVALUATOR_COMMAND
- **Keep policy:** KEEP_POLICY
- **Guard:** GUARD (if any)
- **Noise runs:** NOISE_RUNS
- **Min delta:** 0

## Current Approach
BASELINE_DESCRIPTION

## Search Space
- **Allowed changes:** ALLOWED_CHANGES
- **Forbidden changes:** FORBIDDEN_CHANGES

## Context & References
REFERENCES (if any)

---

## History
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline | BASELINE_SCORE | -- | TODAY |
```

**After writing:**

1. Confirm the file was written: "research.md is ready at [path]."
2. If `evaluate.py` was written, confirm that too.
3. Print the next command:

```
To start the loop, tell your agent:
  "Run autoresearch on ./research-dir/research.md"

Or for overnight unattended:
  nohup bash scripts/autoresearch-loop.sh ./research-dir/ > autoresearch.log 2>&1 &
  bash scripts/check_progress.sh ./research-dir/
```

4. Chain suggestion: "When the loop completes, run `/autoresearch:ship` to publish the results."

---

## Output Checklist

Before declaring the wizard complete, verify:

- [ ] `research.md` written with all sections populated (no `TBD` or `TODO` placeholders)
- [ ] Baseline score recorded in the History table (iteration 0)
- [ ] Evaluator dry-run passed (or manual baseline confirmed)
- [ ] `evaluate.py` written if automated evaluation was chosen
- [ ] Next-step command printed for the user
