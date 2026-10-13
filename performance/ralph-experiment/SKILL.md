---
name: ralph-experiment
description: Hypothesis-driven experiment loop with structured notebook, git checkpoint/revert, and agent delegation
triggers:
  - "experiment"
  - "experiment loop"
  - "karpathy loop"
  - "try hypotheses"
  - "optimize"
  - "improve performance"
  - "ralph-experiment"
---

[EXPERIMENT LOOP — ITERATION {{ITERATION}}/{{MAX}}]

<Purpose>
Ralph-Experiment is a hypothesis-driven experiment loop inspired by the Karpathy Experiment Loop. It iteratively tests single hypotheses against measurable success criteria, using git as a state machine to keep or discard each attempt. Unlike ralph (which completes user stories), ralph-experiment optimizes toward a goal through structured experimentation with an experiment notebook that captures learnings across iterations.
</Purpose>

<Use_When>
- User wants to iteratively optimize something (performance, accuracy, reliability)
- User says "experiment", "optimize", "improve performance", "try hypotheses", "karpathy loop"
- The task has a measurable success criterion (latency < X, throughput > Y, error rate < Z)
- Multiple approaches are possible and the best one isn't obvious
- User wants to explore a solution space methodically
</Use_When>

<Do_Not_Use_When>
- Task has a clear implementation path -- use `ralph` instead
- User wants to implement a known feature -- use `ultrawork` or `ralph`
- There's no measurable metric to optimize -- use `ralph` with acceptance criteria
- User wants a one-shot fix -- delegate directly to an executor agent
</Do_Not_Use_When>

<Why_This_Exists>
Optimization tasks fail when treated as implementation tasks. "Make X faster" doesn't have a single correct solution -- it requires forming hypotheses, testing them, learning from failures, and iterating. Ralph-experiment provides:
1. Structured hypothesis tracking with predictions and outcomes
2. Git checkpoint/revert so failed experiments don't pollute the codebase
3. A queryable experiment notebook that captures learnings across iterations
4. Flexible termination: success criteria, budget limits, or manual interrupt
5. Agent/team delegation to increase hypothesis success rate
6. A simplicity criterion: prefer fewer lines of code at equal performance
</Why_This_Exists>

<Execution_Policy>
- One hypothesis at a time -- sequential experiments, not parallel
- Delegate implementation to executor agents or teams for each hypothesis
- Use `run_in_background: true` for measurement commands (builds, benchmarks, test suites)
- Always pass the `model` parameter explicitly when delegating to agents
- Git commit before measuring, git reset on discard -- no uncommitted experiments
- Never stop unless: success criteria met, budget exhausted, or human interrupts
</Execution_Policy>

<Steps>

## Step 1: SETUP (first iteration only)

Parse the user's request to extract:
- **Goal**: What are we optimizing? (e.g., "Reduce p95 latency for BatchAck messages")
- **Success criteria**: Measurable targets (e.g., `p95_latency_ms < 120`)
- **Measurement command**: How to measure (e.g., `npm run benchmark -- --type=BatchAck`)
- **Budget**: Termination limit. Parse from args:
  - `--budget N` → N experiments max
  - `--budget Nh` or `--budget Nm` → time limit
  - `--budget "scripts done"` → scope-based (scripts complete successfully)
  - Default: 20 experiments

Then:
a. Create experiment branch: `git checkout -b experiment/{tag}` from current HEAD
b. Initialize `experiment-notebook.json` in `.omg/` (see schema below)
c. Run the measurement command to establish **baseline metrics**
d. Record baseline in the notebook

## Step 2: HYPOTHESIZE

Review the experiment notebook:
- What has been tried? What worked? What failed?
- What learnings constrain the next hypothesis?
- What remains unexplored?

Form a hypothesis:
- **Statement**: "Doing X will improve metric Y because Z"
- **Prediction**: Specific expected outcome (e.g., "p95_latency_ms < 160")
- **Rationale**: Why this should work, informed by prior experiments

**Agent delegation for complex domains:**
- Spawn an `analyst` or `architect` agent to evaluate feasibility before committing to implementation
- Useful when the hypothesis involves unfamiliar code paths or architectural changes

Record the hypothesis in the notebook with status `in_progress`.

## Step 3: IMPLEMENT

Delegate the implementation to specialist agents:

**Single executor** (default — hypothesis touches 1-2 files):
```
Agent(subagent_type="oh-my-copilot:executor", name="executor-{N}", model="sonnet",
      prompt="Implement hypothesis EXP-{N}: {hypothesis}. Files to modify: {files}.
              Context from previous experiments: {learnings}")
```

**Team** (hypothesis requires coordinated multi-file changes, 3+ files):
```
TeamCreate(name="exp-{N}", members=["executor-1", "executor-2", "tester-3"])
→ Assign sub-tasks to each member
→ Wait for team completion
→ TeamDelete after experiment concludes
```

**Adaptive escalation**: If a single executor fails due to implementation complexity (not wrong hypothesis), retry with a team. Track `escalated: true` in the notebook.

After implementation, commit all changes:
```
git add -A && git commit -m "experiment(EXP-{N}): {hypothesis summary}"
```

## Step 4: EXECUTE & MEASURE

Run the measurement command:
```bash
{measurement_command} > .omg/experiment-run.log 2>&1
```

Extract metrics from output (grep, parse JSON, etc.).

**On crash:**
1. Capture last 50 lines of output
2. Spawn a `debugger` agent to examine the crash:
   ```
   Agent(subagent_type="oh-my-copilot:debugger", name="debugger-{N}",
         prompt="Experiment EXP-{N} crashed. Analyze: {last_50_lines}. Fix if simple.")
   ```
3. If fix is simple (typo, missing import, wrong arg) → fix, re-commit, re-run
4. If fix is non-obvious → log as crash, proceed to Step 5 with `status: crash`
5. If same crash 3+ times → escalate to human

## Step 5: EVALUATE

Compare metrics to:
- **Baseline**: Is this better than where we started?
- **Best so far**: Is this the new best?
- **Prediction**: Did the hypothesis prediction hold?

**Decision matrix:**

| Metrics vs Best | Code Simpler? | Decision |
|-----------------|---------------|----------|
| Better          | Yes           | **KEEP** (strong win) |
| Better          | No            | **KEEP** (if improvement justifies complexity) |
| Equal           | Yes           | **KEEP** (simplicity win) |
| Equal           | No            | **DISCARD** (no value added) |
| Worse           | —             | **DISCARD** |
| Crash           | —             | **DISCARD** |
| Marginal (+/- 2%) | —          | Spawn `reviewer` to assess code quality → **KEEP** or **DISCARD** |

**MODIFY** decision: If metrics improved but prediction wasn't fully met, the hypothesis direction is right but needs refinement. Keep the commit, and the next hypothesis should build on it.

**On KEEP:**
```bash
# Branch advances (commit stays)
# Update "best" in notebook if new best
```

**On DISCARD:**
```bash
git reset --hard HEAD~1   # Revert to last keep point
```

**On MODIFY:**
```bash
# Commit stays, next hypothesis refines it
```

Record full results in the notebook: metrics, decision, learnings.

**Cross-iteration analysis:** Every 5 experiments, spawn a `scientist` agent to analyze the notebook for patterns and suggest the next hypothesis direction.

## Step 6: CHECK EXIT CONDITIONS

| Condition | Action |
|-----------|--------|
| All success criteria met | EXIT → produce report |
| Budget exhausted (N experiments or time limit) | EXIT → produce report with best result |
| Human interrupts (stop/cancel) | EXIT → produce report with current state |
| Stuck (5+ consecutive discards with no new learnings) | Spawn `architect` for strategic pivot, or escalate to human |
| None of the above | GOTO Step 2 |

## Step 7: EXIT REPORT

Produce a structured summary:

```
═══ Experiment Report ═══
Goal: {goal}
Result: {ACHIEVED / NOT ACHIEVED / PARTIAL} ({summary})

Experiments: {total} total ({keep} keep, {discard} discard, {crash} crash)
Best: {best_experiment_id} ({best_metrics})
Baseline: {baseline_metrics}
Improvement: {percentage change}
Simplicity: net {+/-N} lines vs baseline

Top learnings:
1. {learning from most impactful experiment}
2. {learning from notable failure}
3. {cross-cutting insight}

Files changed: {list}
Branch: experiment/{tag}
Notebook: .omg/experiment-notebook.json
```

Then run `/oh-my-copilot:cancel` for clean state cleanup.

</Steps>

<Experiment_Notebook_Schema>
```json
{
  "goal": "string — what we're optimizing",
  "successCriteria": [
    { "metric": "string", "operator": "<|>|<=|>=|==", "target": "number" }
  ],
  "measurementCommand": "string — command to run",
  "budget": { "type": "experiments|time|scope", "limit": "number|string" },
  "branch": "string — experiment branch name",
  "baseline": {
    "commit": "string — 7-char hash",
    "metrics": { "metric_name": "number" },
    "timestamp": "ISO string"
  },
  "best": {
    "commit": "string",
    "experimentId": "string",
    "metrics": { "metric_name": "number" },
    "improvement": "string — human-readable summary"
  },
  "experiments": [
    {
      "id": "EXP-001",
      "hypothesis": "string — what we're testing",
      "prediction": "string — expected outcome",
      "rationale": "string — why this should work",
      "changes": ["file1.ts", "file2.ts"],
      "commit": "string — 7-char hash",
      "status": "keep|discard|modify|crash|in_progress",
      "escalated": false,
      "metrics": { "metric_name": "number" },
      "vsBaseline": "string — comparison",
      "vsBest": "string — comparison",
      "linesChanged": "number",
      "learnings": "string — what we learned",
      "crashLog": "string | null — if crashed",
      "timestamp": "ISO string"
    }
  ]
}
```
</Experiment_Notebook_Schema>

<Simplicity_Criterion>
"All else being equal, simpler is better."
- Code deletions that maintain metrics are wins
- Track `linesChanged` per experiment
- When two experiments have equal metrics, prefer the one with fewer lines changed
- Minimal improvements (< 1%) don't justify significant complexity additions
</Simplicity_Criterion>

<Examples>
<Good>
Hypothesis informed by prior experiments:
```
EXP-005 hypothesis: "Connection pooling will compound with batching (EXP-001)
because both reduce per-message I/O overhead, and pooling eliminates the
connection setup cost that batching doesn't address."

This references EXP-001's learning about batching and builds on it.
```
Why good: Each hypothesis builds on accumulated learnings.
</Good>

<Good>
Adaptive team escalation:
```
EXP-003: Single executor failed — couldn't coordinate changes across
handler + db layer + config simultaneously.
EXP-003 (retry): Spawned team with executor-1 (handler), executor-2 (db),
tester-3 (integration test). Team succeeded.
Notebook: { "escalated": true, "status": "keep" }
```
Why good: Detected implementation complexity, escalated to team, tracked it.
</Good>

<Good>
Clean discard with learnings:
```
EXP-002 result: p95_latency_ms = 190 (worse than baseline 200? No, better,
but worse than EXP-001's 170)
Decision: DISCARD (does not improve on current best)
Learnings: "Lock-free queue adds overhead for small batch sizes.
Contention is not the bottleneck — I/O is."
git reset --hard HEAD~1
```
Why good: Reverted cleanly, captured specific learning that informs future hypotheses.
</Good>

<Bad>
Hypothesis without prediction:
```
"Let's try caching and see what happens"
```
Why bad: No specific prediction. Impossible to evaluate whether the hypothesis was right or wrong.
</Bad>

<Bad>
Skipping learnings on discard:
```
EXP-004: metrics worse. Discard.
(no learnings recorded)
```
Why bad: The whole point of the loop is to learn from failures. Every discard should explain WHY it failed.
</Bad>

<Bad>
Multiple hypotheses in one experiment:
```
EXP-005: "Add caching AND connection pooling AND async writes"
```
Why bad: If metrics improve, which change helped? If they worsen, which hurt? One hypothesis at a time.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- Stop and report when success criteria are met — produce exit report
- Stop when budget is exhausted — produce exit report with best result
- Stop when human interrupts — run `/oh-my-copilot:cancel`
- Continue when hook sends "The boulder never stops" — this means keep experimenting
- Escalate to human when same crash occurs 3+ times
- Escalate to human when 5+ consecutive discards yield no new learnings (loop is stuck)
- Spawn architect for strategic pivot before escalating to human
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] experiment-notebook.json exists with baseline and all experiments logged
- [ ] Every experiment has: hypothesis, prediction, metrics, learnings
- [ ] No in_progress experiments remain (all resolved to keep/discard/modify/crash)
- [ ] Git branch is clean (no uncommitted changes)
- [ ] Discarded experiments were reverted (git reset)
- [ ] Best result is recorded in notebook
- [ ] Exit report produced with summary, learnings, and file list
- [ ] `/oh-my-copilot:cancel` run for clean state cleanup
</Final_Checklist>
