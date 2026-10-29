---
name: ml-agents
description: "Unity ML-Agents reinforcement learning — Agent lifecycle, observation/action contracts, reward shaping, self-play and ELO, trainer YAML, headless sweeps, and the version handshake. Load when writing Agent subclasses, changing observations or rewards, or running mlagents-learn."
globs: ["**/Agent_*.cs", "**/Sensor_*.cs", "**/Reward_*.cs", "**/*Agent.cs", "Config/*.yaml", "**/*.onnx"]
---

# ML-Agents — Reinforcement Learning in Unity

`com.unity.ml-agents` (C#) trains policies against a Python trainer (`mlagents`) over
a gRPC handshake. The Unity side collects observations and applies actions; the
Python side owns the optimizer, the checkpoints and the `.onnx` export.

## The version handshake is the first thing to check

The two halves negotiate a **communication API version**. If those differ the
handshake is refused and the trainer exits — often with a message that reads like a
port problem.

| Half | Where | This project |
|---|---|---|
| C# | `Packages/manifest.json` → `com.unity.ml-agents` | 4.1.0, comms API 1.5.0 |
| Python | `.venv` → `pip show mlagents` | 1.1.0, comms API 1.5.0 |

Package version equality is not the requirement — **comms API equality is**. Upgrading
one side alone breaks training with no code change anywhere.

## Agent Lifecycle

```
Awake()               → base.Awake() registers the RPC communicator. Call it.
OnEpisodeBegin()      → reset THIS agent's state
CollectObservations() → write the observation vector
OnActionReceived()    → apply actions; this is your FixedUpdate
EndEpisode()          → terminal; triggers OnEpisodeBegin on the next step
```

`DecisionRequester.DecisionPeriod` sets how many physics ticks pass between
decisions. With `TakeActionsBetweenDecisions = true`, `OnActionReceived` still fires
every tick with the last decision's actions — which is what makes force application
smooth instead of impulsive.

### Multi-agent resets do not belong in OnEpisodeBegin

When N agents share one episode, N independent `OnEpisodeBegin` calls run in
arbitrary order and can half-reset shared state. Leave `OnEpisodeBegin` empty and let
one director reposition everything after ending the episode:

```csharp
// Agent_FootballPlayer.cs — deliberately empty
public override void OnEpisodeBegin() { }

// Systems_EpisodeDirector owns the reset for all 22 players, together.
```

## Observations

The observation vector is a **contract**. Change its size and every existing `.onnx`
fails to load — there is no migration, and `--initialize-from` will not help.

```csharp
public override void CollectObservations(VectorSensor sensor)
{
    Sensor_FootballState.Collect(sensor, _observationBuffer, /* ... */);
}
```

Rules that hold regardless of the game:

- **Normalize to [−1, 1] yourself.** Divide positions by a range constant
  (`OBSERVATION_RANGE`), speeds by a top speed. Then set `normalize: false` in the
  trainer YAML — running normalization on top of pre-normalized input fights
  self-play, because the input distribution shifts as the opponent improves.
- **Reuse a buffer.** `CollectObservations` runs every decision for every agent.
  `private readonly float[] _observationBuffer = new float[OBSERVATION_SIZE];`
- **Keep `OBSERVATION_SIZE` a single const** and set
  `BrainParameters.VectorObservationSize` from it in code. A scene-authored size that
  disagrees with what you emit is a silent shape mismatch.
- **Zero, don't omit, what an agent must not see.** Defenders observe a zeroed
  play-call slice rather than a shorter vector — same shape, no leak.

## Actions

```csharp
// Only the brain that needs them gets the extra outputs.
behaviorParameters.BrainParameters.ActionSpec = _hasQuarterbackActions
    ? new ActionSpec(4, new[] { PLAY_CALL_SLOTS, 2 })   // 4 continuous + 2 discrete branches
    : ActionSpec.MakeContinuous(2);
```

- **Clamp continuous actions to [−1, 1]** on arrival and scale to real units
  yourself. The policy is not obliged to stay in range.
- **Do not hand a brain dimensions it must ignore.** Dead outputs are dimensions the
  optimizer spends samples learning to zero.
- **Apply in `FixedUpdate` only** — `OnActionReceived` is called from the physics
  loop. Never apply forces from `Update`.
- **`Heuristic` must fill every segment.** It is the manual-control and no-trainer
  path; a partial fill leaves stale actions.

## Rewards

Split dense from terminal and keep both out of the Agent class:

```
Assets/Scripts/Reward/Reward_Progress.cs   — per-tick, small, dense
Assets/Scripts/Reward/Reward_Terminal.cs   — per-episode, large, sparse
```

- `AddReward` accumulates; `SetReward` overwrites. Prefer `AddReward`.
- **Dense rewards need a baseline reset.** Rewarding a delta across an episode
  boundary pays out the jump from the old state to the new one. Seed the baseline on
  the first tick of a new episode and return without paying:

```csharp
if (_lastSeenEpisode != _play.EpisodeIndex)
{
    _lastSeenEpisode = _play.EpisodeIndex;
    _previousBallY = ballY;
    return;
}
```

- **Give the do-nothing policy a cost.** Without a per-decision time cost, standing
  still is a local optimum in any zero-sum game.
- Keep terminal magnitudes ~1.0 and dense ones ~0.01–0.05, so an episode's dense
  total cannot dwarf its terminal signal.

## Self-Play

```yaml
self_play:
  save_steps: 50000
  team_change: 250000              # 5x save_steps — the documented default ratio
  swap_steps: 25000
  window: 10
  play_against_latest_model_ratio: 0.5
  initial_elo: 1200.0
```

Set `BehaviorParameters.TeamId` per side. Both sides may share one behavior name or
use several — this project runs four (`OffenseLine`, `OffenseSkill`, `DefenseLine`,
`DefenseCover`) off one YAML anchor.

**Judge on `Self-play/ELO`, never mean reward.** Reward is zero-sum across the two
teams and hovers near 0 however strong the policies become. A flat reward curve in a
self-play run is the expected shape, not a failure.

## Telemetry — instrument outcomes, not just reward

Mean reward cannot tell you *how* episodes ended. `StatsRecorder` averages within a
summary window, so writing 1 for the outcome that occurred and 0 for the others turns
each series into a rate:

```csharp
StatsRecorder stats = Academy.Instance.StatsRecorder;
stats.Add("Play/TackleRate", outcome == Systems_PlayOutcome.Tackle ? 1f : 0f);
stats.Add("Play/TimeExpiredRate", outcome == Systems_PlayOutcome.TimeExpired ? 1f : 0f);
stats.Add("Play/NetYards", netYards);
```

Also record what the policy *chose*, not only what happened. A policy that collapses
to one action is invisible in outcome rates alone — every rate still looks plausible
while most of the action space goes unused.

## Trainer Configuration

Config and run-id are paired 1:1 by name: `Config/<Name><Phase><NN>.yaml` ↔
`--run-id=<name>_<phase><nn>`.

```yaml
behaviors:
  OffenseLine: &football_brain
    trainer_type: ppo
    hyperparameters:
      batch_size: 2048
      buffer_size: 20480              # ~10x batch_size
      learning_rate: 3.0e-4
      beta: 5.0e-3                    # entropy — keeps exploration alive in self-play
      learning_rate_schedule: constant # a decay to 0 freezes the policy while
                                       # opponents keep improving
    network_settings:
      normalize: false                # observations are already in [-1, 1]
      hidden_units: 512
      num_layers: 2
    time_horizon: 150                 # long enough that terminal credit reaches
                                       # back to the start of an episode
    threaded: false                   # deterministic ordering
  OffenseSkill:
    <<: *football_brain               # YAML anchors keep brains in lockstep
```

`time_horizon` shorter than an episode means terminal reward never reaches the
decisions that set it up. Size it against your episode length in *decisions*, not
ticks.

## Running

```powershell
.venv\Scripts\Activate.ps1

# In-editor smoke test: start the trainer FIRST, then press Play.
mlagents-learn Config\FootballBase03.yaml --run-id=football_base03

# Headless sweep — envs take CONSECUTIVE ports from --base-port.
mlagents-learn Config\FootballBase03.yaml --run-id=football_base03 `
  --env=Builds\FootballEnv\PoFootball.exe --no-graphics `
  --base-port=5010 --num-envs=6

tensorboard --logdir results
```

Operational rules that cost real runs when ignored:

- **Overlapping port ranges hang the handshake with no error.** Each env takes a
  consecutive port from `--base-port`. Two concurrent sweeps need disjoint ranges.
- **Record `--num-envs` in the run's `MANIFEST.md`.** It changes how experience is
  batched, so two runs with the same YAML and different `--num-envs` are not
  comparable.
- **Kill TensorBoard before `--force`.** It holds Windows file handles and the wipe
  silently no-ops, leaving you resuming a run you thought you had cleared.
- **Shut down in order: trainer → envs → TensorBoard.**
- **4–8 envs**, leaving cores for torch.
- `time_scale` in `engine_settings` speeds the clock only; physics stays at
  `dt = 0.02`. It is not a dynamics change.

## Promoting a brain

```
Assets/Agents/<Name>_v<NN>/
    <name>.onnx
    <Name>_Character.asset
    MANIFEST.md          — run-id, config, --num-envs, steps, final ELO
```

**Overwrite `.onnx` in place** to preserve the `.meta` GUID. Deleting and re-adding
regenerates the GUID and breaks every reference to it.

## Failure Modes

| Symptom | Cause |
|---|---|
| Trainer exits at startup, port-ish error | Comms API mismatch between C# and Python |
| Handshake hangs forever | Overlapping `--base-port` ranges across sweeps |
| `.onnx` refuses to load | Observation size or ActionSpec changed since export |
| Reward flat near 0 in self-play | Expected — read `Self-play/ELO` instead |
| Reward great, behaviour bad | Reward is being farmed; instrument outcome rates |
| Agents freeze at episode start | Reset raced across N agents' `OnEpisodeBegin` |
| Agent ignores half its actions | A Rigidbody constraint is discarding them |
| Fatigue/load reads zero under load | Measured from the action vector, not applied force |
| `--force` appears to do nothing | TensorBoard is holding the results directory |

## Related

- [[unitask]] — async without coroutines, for anything outside the physics loop
- [[vcontainer]] — injecting scene-instantiated Agents (see [[messagepipe]] for the
  event side)
- [[physics]] — the `FixedUpdate` and fixed-Δt discipline actions depend on
