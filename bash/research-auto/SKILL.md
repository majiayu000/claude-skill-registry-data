---
name: research-auto
description: "Use when the user invokes /research-auto or asks to run an autonomous campaign over one active Package toward a measurable gate."
allowed-tools: Bash(python3 *), Read, Grep, Glob, Agent
---

# research-auto

Run repeated Experiment cycles inside one active Package. Use `research-run`
for a single known Experiment.

## Preconditions

- one active Project and Package;
- one current active Direction;
- at least one current ExperimentSpec with a structured numeric gate;
- `execution_mode == AUTONOMOUS`;
- declared compute, time, and external-action boundaries.

If any precondition is absent, return the smallest owning handoff. Do not create
parallel approval records or infer intent from the Control Panel.

## Context

Start each cycle from:

```bash
python3 -m lib.research_state.cli \
  --workspace <workspace> \
  context <package-id> \
  --experiment <experiment-id>
```

Use the packet’s current versions, Rules, decisions, evidence summary, and
`next_refs`. Fetch a referenced Run or note only when the current action needs
it. Do not carry the full prior transcript into the next cycle.

## Loop

```text
read compact packet
  -> choose one READY ExperimentSpec
  -> verify implementation and resource readiness
  -> launch through lib.experiments.launch
  -> monitor structured status
  -> finalize evidence
  -> evaluate the exact declared metric
  -> route: continue | revise plan | halt
```

The launcher freezes current authority. The campaign never supplies its own
Run context or weakens the verifier.

## Plan changes

Use one `RESEARCH_PLAN_UPDATE` transaction when evidence justifies a Direction
or ExperimentSpec revision. Include only changed nodes. The transaction must
preserve earlier versions, Runs, and Evidence.

Pause for the user when a proposed change alters the Project charter, increases
budget or external authority, requires a destructive action, or changes the
terminal Package decision.

## Deterministic routing

The helper exposes:

```bash
python3 skills/research-auto/scripts/conductor.py status ...
python3 skills/research-auto/scripts/conductor.py gate-eval ...
python3 skills/research-auto/scripts/conductor.py append-cycle ...
python3 skills/research-auto/scripts/conductor.py pack ...
```

Use the exact ExperimentSpec metric and operator. Never substitute another
measurement because it is the only one present.

Routes:

- `CONTINUE`: a current legal Experiment remains;
- `REVISE_PLAN`: evidence supports a typed Plan update;
- `HALT_GATE`: the declared success gate is met;
- `HALT_BUDGET`: budget is exhausted;
- `HALT_NO_CANDIDATE`: no legal Experiment remains;
- `HALT_BLOCKED`: required authority, evidence, or compute is unavailable.

## Completion

Stop when one route is durably recorded and no launched Run remains
unreconciled. The user still owns the terminal Package outcome.
