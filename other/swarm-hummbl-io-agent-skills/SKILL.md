---
name: swarm
description: Fan-out/fan-in orchestration across machines using claude -p over SSH. Dispatch parallel agents, collect results, synthesize.
version: 0.1.0
execution-mode: side_effecting
argument-hint: "<task_description> [--machines mbp,$REMOTE_HOST,local] [--model opus|sonnet|haiku] [--lanes N] [--synthesize]"
category: fleet-ops
status: candidate
---
# Swarm

Dispatch parallel Claude agents across the Tailscale mesh using `claude -p` over SSH. Each agent gets a fresh context window, runs autonomously, writes results to a file. Optional synthesis step combines all outputs.

## When to Use
- Task is decomposable into 2-6 independent lanes
- Single context window is too small for the full task
- Need to run on different machines (GPU on Windows, services on local machine, inference on $REMOTE_HOST)
- Want model diversity (Opus for hard reasoning, Sonnet for bulk, Haiku for fast)
- When `[dispatch]` subagents aren't enough (cross-machine, need full context per lane)

## Architecture

```
                    ┌─────────────┐
                    │  Orchestrator│  (this machine)
                    │  writes prompts, launches, collects
                    └──────┬──────┘
                           │ fan-out (parallel SSH)
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌─────────┐ ┌─────────┐ ┌─────────┐
         │ local machine     │ │$REMOTE_HOST │ │ local   │
         │claude -p│ │claude -p│ │claude -p│
         │ Sonnet  │ │ Haiku   │ │ Opus    │
         └────┬────┘ └────┬────┘ └────┬────┘
              │            │            │
              ▼            ▼            ▼
         results/     results/     results/
         lane-1.md    lane-2.md    lane-3.md
                           │
                    ┌──────┴──────┐
                    │  Synthesizer │  (Opus, this machine)
                    │  cat *.md | claude -p
                    └─────────────┘
```

## Machine Map

| Machine | SSH Alias | Best For | Model Default |
|---------|-----------|----------|---------------|
| Windows desktop (local) | — | GPU tasks, code quality, testing | opus |
| local machine | `ssh others@$LOCAL_IP` | Services, adapters, health, briefing | sonnet |
| $REMOTE_HOST | `ssh others@$LOCAL_IP "ssh $REMOTE_HOST ..."` or `ssh $REMOTE_HOST` from local machine | Inference, Open Brain, bulk processing | haiku |

## Execution

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=swarm] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 1. Decompose Task
Break the user's task into independent lanes. Each lane gets:
- A name (e.g., `quality-audit`, `security-scan`, `test-analysis`)
- A target machine
- A model selection
- A self-contained prompt (must include all context -- no shared state)

#### Lane Decomposition Strategy (evidence-based routing)

Choose domain-based vs function-based lanes by task type. Backed by sandbox
experiment `experiment-2026-07-26-lane-decomposition-task-type-interaction.md`
(interaction F=204, p=0.01).

| Task type | Strategy | Why |
|-----------|----------|-----|
| **Cross-domain synthesis** (risk audit, compliance, strategic analysis spanning 3+ domains) | **Domain-based** (security, governance, ops, legal...) | d=1.63 — surfaces cross-domain connections |
| **Single-domain deep** (code review, bug fix, perf profile) | **Underpowered** (d=0.09, 95% CI [-0.79, 0.97]) | n=10 — could not detect small/medium effects. Pick natural. |
| **Narrative** (docs, blog post, exec summary, onboarding) | **Function-based** (research, outline, draft, edit) | d=-0.37 — domain-based fragments coherence |

See `swarm-subagent` SKILL.md for full routing details and mixed-task guidance.

### 2. Write Prompt Files
For each lane, write a prompt file to `/tmp/swarm/`:
```bash
mkdir -p /tmp/swarm/prompts /tmp/swarm/results
```

Each prompt file should:
- Be fully self-contained (the agent has no context from this session)
- Include the repo path on the target machine
- Include specific instructions and success criteria
- End with: "Write your complete findings. Be concise and structured."

### 3. Launch Agents
```bash
# Local lane
cat /tmp/swarm/prompts/lane-1.md | claude -p --model sonnet > /tmp/swarm/results/lane-1.md 2>&1 &
PID1=$!

# local machine lane
cat /tmp/swarm/prompts/lane-2.md | ssh -o ConnectTimeout=10 others@$LOCAL_IP "cd $PROJECT_ROOT && claude -p --model sonnet" > /tmp/swarm/results/lane-2.md 2>&1 &
PID2=$!

# $REMOTE_HOST lane (via local machine jump)
cat /tmp/swarm/prompts/lane-3.md | ssh -o ConnectTimeout=10 others@$LOCAL_IP "ssh -o ConnectTimeout=10 $REMOTE_HOST 'cd $PROJECT_ROOT && claude -p --model haiku'" > /tmp/swarm/results/lane-3.md 2>&1 &
PID3=$!

echo "Launched: PID $PID1 (local), $PID2 (mbp), $PID3 ($REMOTE_HOST)"
```

### 4. Monitor Progress
```bash
# Check which lanes are still running
for pid in $PID1 $PID2 $PID3; do
  kill -0 $pid 2>/dev/null && echo "PID $pid: running" || echo "PID $pid: done"
done

# Check output sizes
ls -la /tmp/swarm/results/
```

### 5. Wait for Completion
```bash
wait $PID1 $PID2 $PID3
echo "All lanes complete"
```

### 6. Synthesize (if --synthesize)
```bash
echo "# Swarm Synthesis" > /tmp/swarm/synthesis-prompt.md
echo "" >> /tmp/swarm/synthesis-prompt.md
echo "Synthesize these independent agent reports into a single coherent summary." >> /tmp/swarm/synthesis-prompt.md
echo "Resolve any contradictions. Highlight consensus findings." >> /tmp/swarm/synthesis-prompt.md
echo "Output a structured report with: Summary, Key Findings, Contradictions, Recommendations." >> /tmp/swarm/synthesis-prompt.md
echo "" >> /tmp/swarm/synthesis-prompt.md
for f in /tmp/swarm/results/lane-*.md; do
  echo "---" >> /tmp/swarm/synthesis-prompt.md
  echo "## $(basename $f .md)" >> /tmp/swarm/synthesis-prompt.md
  cat "$f" >> /tmp/swarm/synthesis-prompt.md
  echo "" >> /tmp/swarm/synthesis-prompt.md
done

cat /tmp/swarm/synthesis-prompt.md | claude -p --model opus > /tmp/swarm/results/synthesis.md
```

## Output Format

```
Swarm | {task} | {N} lanes
═══════════════════════════

## Lanes
| # | Name | Machine | Model | Status | Output |
|---|------|---------|-------|--------|--------|
| 1 | quality-audit | local | opus | DONE (45s) | 2.1 KB |
| 2 | security-scan | mbp | sonnet | DONE (32s) | 1.8 KB |
| 3 | test-analysis | $REMOTE_HOST | haiku | DONE (18s) | 1.2 KB |

## Synthesis
{Combined findings from all lanes}

## Contradictions
{Where agents disagreed, if any}

## Recommendations
{Prioritized actions from combined analysis}

## Artifacts
- /tmp/swarm/results/lane-1.md
- /tmp/swarm/results/lane-2.md
- /tmp/swarm/results/lane-3.md
- /tmp/swarm/results/synthesis.md
```

## Predefined Swarm Patterns

### "Full Audit" (3 lanes)
```
Lane 1 (local, opus): [full-audit] on $PROJECT_ROOT/services/
Lane 2 (mbp, sonnet): [security-scan] + [secret-scan] + [threat-model]
Lane 3 ($REMOTE_HOST, haiku): [test-run] + [coverage] + [ci-monitor]
Synthesize: Combined audit report
```

### "Research Sprint" (3 lanes)
```
Lane 1 (local, opus): [deep-research] on primary topic
Lane 2 (mbp, sonnet): [competitive-intel] on same topic
Lane 3 (local, sonnet): [anthropic-watch] + [industry-watch]
Synthesize: Research brief with competitive context
```

### "Ship Check" (2 lanes)
```
Lane 1 (local, opus): [ship-check] + [pre-mortem]
Lane 2 (mbp, sonnet): [test-run] + [ci-monitor] + [smoke]
Synthesize: Go/no-go recommendation
```

### "Governance Assessment" (3 lanes)
```
Lane 1 (local, opus): [governance-maturity] + [gap-analysis]
Lane 2 (mbp, sonnet): [evidence-pack] --scope full
Lane 3 (local, sonnet): [nist-map] + [iso-crosswalk] + [soc2-check]
Synthesize: Assessment report with evidence
```

## Legacy Fixed-Size Topologies

The old `dual-agent`, `tri-agent`, `quad-agent`, and `poly-agent` skills are archived aliases. Preserve their intent by choosing the simplest swarm shape that adds real value:

| Legacy request | Swarm pattern |
| --- | --- |
| `dual-agent`, two-agent advisory + implementation | Use a 2-lane plan: advisory/review lane plus implementation lane. If the implementer is external or asynchronous, package the work with `[delegate]`. |
| `tri-agent`, three-agent pipeline | Use 3 lanes only when the third role is distinct: triage, research, or adversarial review. Otherwise use the 2-lane pattern. |
| `quad-agent`, four-agent pipeline | Use 4 lanes only for Research -> Design -> Implement -> Validate or parallel investigation with synthesis. Require clear handoff checkpoints. |
| `poly-agent`, N-agent dispatch, manifest dispatch | Use a manifest-style swarm: declare lanes, sync points, output contract, context budget, and fault policy before launching. Keep lane summaries under 400 words. |

Do not add agents for symmetry. Each extra lane must reduce risk, add independent evidence, or unlock parallel execution that a single agent cannot do cleanly.

## Rate-limit discipline

Per `~/.agents/rules/staggered-subagent-deploy-rate-limit.md`:

- **Default stagger**: 400ms between lane launches (jittered ±50ms)
- **Default concurrency cap**: 5
- **Override env vars**: `STAGGER_MS` (set to 0 to disable), `SWARM_CONCURRENCY`
- **On 429 / spend-cap**: stop further spawns to that provider, post bus `BLOCKED` identifying limiter (RPM/ITPM/OTPM/SPEND_CAP), retry with exponential backoff (1s, 2s, 4s, 8s, cap 60s)
- **Override logging**: every `STAGGER_MS=0` or `CONCURRENCY_OVERRIDE` use posts a bus STATUS

## Constraints

- Max 5 concurrent lanes (API rate limits)
- Each lane consumes its own Claude Max quota allocation
- Prompts must be self-contained -- agents cannot access this session's context
- Use `nohup` for lanes expected to run >5 minutes
- Always verify SSH connectivity before launching remote lanes (`[tailscale-status]`)
- Kill orphaned agents if a swarm is cancelled: `ssh <machine> "pkill -f 'claude -p'"`
- Results in /tmp/swarm/ are ephemeral -- save important outputs to docs/ or _state/

## Lexicon

This skill uses the canonical swarm lexicon (`~/.agents/rules/swarm-lexicon.md`).
Key terms: swarm, wave, batch, lane, orchestrator, fan-out, fan-in,
machine map. Conflicts between this skill's local vernacular and the lexicon
resolve in favor of the lexicon.

## Skill Chains
- For inference for lanes that do not need Claude -> `[reasoning-router]` (`python ~/bin/reasoning_router.py route`)

### Mandatory (MUST pass before lane dispatch)

- **`[tailscale-status]`** MUST confirm SSH connectivity for any remote lane
- **`[swarm-manifest]`** MUST be generated for N≥3 lanes (lane allocation, budget, pre-flight)

### Advisory

| After this skill... | Consider... |
|--------------------|-------------|
| Swarm complete | `[retrospective]` (review swarm effectiveness) |
| Synthesis done | `[decision-log]` (record findings) |
| Audit swarm | `[evidence-pack]` (bundle results) |
| Research swarm | `[research-ingest]` (persist to CLP) |
| Lane needs opencode runtime | `[cross-runtime-bridge]` (`python ~/bin/cross_runtime_bridge.py delegate "<task>" --workdir <dir> --auto`) |
| Pre-ship swarm | `[commit]` + `[pr-summary]` (act on findings) |

## Authority

- **T1 (TRUSTED)**: May dispatch swarm with `[tailscale-status]` passed
- **T2 (Active/High)**: May dispatch swarm with `[tailscale-status]` + `[swarm-manifest]` passed
- **T3 (Medium)**: MUST get operator approval AND all mandatory chains passed
- **T4 (Probationary)**: BLOCKED — cannot invoke this skill (spawns uncontrolled agent fleets)
- **Operator**: Override any restriction
