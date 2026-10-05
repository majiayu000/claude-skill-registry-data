---
name: ml-agents
description: "ML-Agents 4.1.0 (local patched package) — the brain contract, local patches, training/deploy workflow, ONNX inference, and the silent-failure modes specific to this project."
globs: ["**/Agent_*.cs", "**/Reward_*.cs", "**/Systems_SumoMatchManager.cs", "**/Training/**", "**/*.onnx", "**/configs/*.yaml"]
---

# Unity ML-Agents — PoSumo

`com.unity.ml-agents` **4.1.0**, a **LOCAL `file:` package** at
`Training/ml-agents/com.unity.ml-agents` carrying required local patches. Python side is
`mlagents` / `ml-agents-envs` **1.2.0.dev0**, installed **editable** (`pip install -e`)
against that same tree — so the source patches ARE the installed copy, and there is no
second copy under `site-packages` to keep in sync.

Read `AGENTS.md` for biomechanics and reward engineering. This skill covers the
ML-Agents integration itself.

---

## 1. Never "upgrade" these

| Pin | Version | Why |
|---|---|---|
| `com.unity.ml-agents` | 4.1.0 local | re-fetching **loses the local patches below** |
| `torch` | 2.5.1 +cpu | 2.6+ breaks ONNX checkpoint export. 4.1.0 permits `<=2.8.0`, but the export problem is ours, not theirs |
| `setuptools` | 69.5.1 | 70+ removes `pkg_resources` and breaks `mlagents-learn` |
| `numpy` | 1.23.5 | pinned by mlagents |
| Python | 3.10.11 | hard range >=3.10.1, <=3.10.12 |

Never `pip install --upgrade` in `Training/venv`. A genuinely new dependency goes in with
`-c Training/constraints.txt`, which pins torch / numpy / setuptools / protobuf / onnx —
that is how gymnasium and pettingzoo were added for 4.1.0 without disturbing anything.

**Comms API version must be EQUAL on both sides** or the handshake is refused:
`Academy.k_ApiVersion` (C#) and `UnityEnvironment.API_VERSION` (Python) are both **1.5.0**.
They moved together 1.4.0 → 1.5.0 in 4.1.0, so C# and Python upgrade together or not at all.

## 2. Local patches — re-apply if the source is re-fetched

**Patch 1 is RETIRED. Do not re-apply it.** 4.1.0 fixed it upstream and better
(`Match3ActuatorComponent` guards with `#if UNITY_6000_3_OR_NEWER` and calls
`gameObject.GetEntityId().GetHashCode()`). The old local patch used a plain
`gameObject.GetHashCode()` unconditionally; re-applying it overwrites a correct upstream
fix with a worse one. Numbering below is kept so older commits still line up.

**Patch 2 — `Plugins/Google.Protobuf_MLAgents.dll`**
Renamed from `Google.Protobuf_Packed.dll` (file, `.meta`, **and internal assembly name**,
rewritten with Mono.Cecil) because `com.unity.ai.inference` ships an editor-only DLL with
the identical original name, and player builds resolve the reference to the wrong one. All
7 asmdefs reference the new name. Still required at 4.1.0 / ai.inference 2.6.1.

**Patch 3 — `Runtime/Grpc/Unity.ML-Agents.CommunicatorObjects.asmdef`**
`defineConstraints` must be `["UNITY_EDITOR || UNITY_STANDALONE"]`. Upstream ships it
EMPTY, so the assembly compiles for Android and demands `Google.Protobuf_MLAgents.dll`,
whose `.meta` carries `Exclude Android: 1` — the Android build then dies with dozens of
`CS0400: The type or namespace name 'Google' could not be found`.

> **This patch was undocumented and was silently lost in the 4.1.0 upgrade.** Nothing
> warns you: the Editor and every training env compile clean, because both are
> `UNITY_EDITOR || UNITY_STANDALONE`. **Only a player build for a mobile target exercises
> it.** Verify an Android build after any ml-agents re-fetch — a green console proves
> nothing here.

**Patch 4 — `mlagents_envs/environment.py::_check_communication_compatibility`**
`StrictVersion` replaced with a manual tuple parse; the original crashes worker
auto-restarts. Still required at 4.1.0, which still does
`from distutils.version import StrictVersion`.

### Upgrade procedure

Clone upstream to a scratch dir, apply patches 2, 3 and 4 to that **staging** copy, and
only then swap it over `Training/ml-agents` — so the Editor never watches a half-patched
package. **Diff the staged tree's `.asmdef` files against the outgoing one before
swapping**: an asmdef carries no version number, and a lost `defineConstraints` entry is
invisible until a platform you rarely build for fails.

The Cecil rename cannot be compiled against directly in the MCP `execute_code` sandbox
(`Mono.Cecil` resolves at runtime but is not a compile-time reference) — drive it by
**reflection** off `System.Reflection.Assembly.Load("Mono.Cecil")`. Carry the existing
`.dll.meta` forward rather than taking upstream's, to keep the plugin GUID stable. Then
`pip install -e` both python packages with `--no-deps`.

The whole `Training/ml-agents` tree is **tracked in this repo** (~2300 files), so a botched
upgrade is recoverable with `git checkout` rather than a re-clone.

Diff with `--strip-trailing-cr`: of 163 differing `Runtime/*.cs` files between 4.0.0 and
4.1.0, only **25** were real changes — the rest were CRLF-only.

## 3. The brain contract (`Agent_Biped`)

- **13 continuous actions** (`ActionCount`), always.
- **`ObservationCount = 42`**, or **45** when `extendedObservations` is on (the standard
  for all four shipped fighters, `decisionPeriod` 3).
- Layout: 5 body + 26 joint (13 x angle/speed) + 4 feet + **1 task flag** + 4
  opponent-or-target + 2 edge distances.
- Two **opt-in** blocks lengthen the vector and are OFF for every shipped brain:
  `contactObservations` (+4) and `staminaObservation` (+1).
- **Append order is fixed: base → contact → stamina → extended.** That order *is* the
  input layer's layout and must never change once a brain has trained on it.
- All observations pass through `San()` NaN/Inf sanitization.
- `Agent_Biped` configures its own `BehaviorParameters` and `DecisionRequester` in
  `Awake` — nothing to wire in the Inspector.

> **Obs count and decision period MUST match what the assigned `.onnx` was trained with.**
> A mismatch does not error. Inference is silently garbage: a fighter that twitches or
> stands still, which reads as a bad policy rather than a wiring bug.

**Prose in the repo lies about the count.** `MANIFEST.md`, `ROSTER.md` and the tooltip on
`Agent_CharacterDefinition.extendedObservations` still say 44 (the pre-merge value). The
constant in `Agent_Biped` is the truth.

### Two modes, one policy

`Mode.Walk` (falling ends the episode) and `Mode.Sumo` (refereed externally; shaping only,
±1 comes from the referee). One brain per fighter trained on **both tasks at once**, told
apart by the task flag. `BeginWalkIn` / `EndWalkIn` switch `mode` and point the four
"opponent" slots at a virtual target — **there is no model swap**; `walkModel` and
`DeployWalk` no longer exist.

`Mode.Recover` was deleted 2026-08-02. Adding get-up training back means a new mode plus
its own reward branch, not a revert. Enum values `Walk = 0`, `Sumo = 1` were unaffected
because `Recover` was last.

## 4. Training scenes and the walk lane

Four unified scenes, `SCN_TRAIN_<NAME>` — one per fighter. Each holds two populations
under ONE behavior name: **4 sumo agents** on two self-play arenas, and **6 walk agents**
on a lane 60 m below.

Walk agents are over-provisioned 6-vs-4 **on purpose**: self-play periodically freezes one
team as the ghost and DISCARDS its experience, and walk agents sit on a team like anyone
else, so an even split would quietly halve the walk sample rate.

### Two silent failures unique to the walk lane

**A walker's `facingSign` must point AT its target.** Progress and graduation are measured
in the facing-local frame (`xLocal = (Torso.x - arenaCenterX) * facingSign`, graduating at
`xLocal > -0.3`), so a walker whose target is 5 m right but whose `facingSign` is `-1`
reads its start line as *5 m past the finish*. It banks the hardcoded +3, ends the episode
on its first decision, respawns, and repeats forever — never a step of travel, never a step
of learning, and a torrent of free reward. The ragdoll just looks untrained and the console
is silent. It cost 2.6M steps before being caught.

> **Tell on TensorBoard:** mean reward pinned just under the graduation bonus with
> near-zero variance (one fighter sat at `2.999 ± 0.015`). That is not a policy converging,
> it is one terminal firing every episode. After any walk-lane change, assert every walker
> spawns at `xLocal < -0.3`; if `StepCount` stays 0 while `CompletedEpisodes` climbs by one
> per decision period, this is why.

**Verify a scene's character assignment by reading the saved `.unity` file, not a script
log.** A wiring pass once reported "4 walkers -> Matt" while the scene on disk still held
`character: {fileID: 0}`, and the env trained the wrong policy for 1.5M steps. Grep for
`character: {fileID: 11400000` and check the guid.

## 5. Workflow

```
Character asset + Training/configs/<Name><Phase><NN>.yaml   (behaviors: key == behaviorName)
  → PoSumo → Build <Name> Training Env   → Builds/<Name>Env/<Name>Env.exe
  → train                                 → Training/results/<name>_<phase><nn>/
  → PoSumo → Deploy <Name> Brain          → Assets/Agents/<Name>_v01/<Name>.onnx
```

Each config's header comment records **why** its hyperparameters and shaping differ. Keep
that habit — it is the project's training log.

### Wrappers

| Script | Use for |
|---|---|
| `Training\Start-Training.ps1` | one run, foreground |
| `Training\Start-StaminaExtension.ps1` | 2+ concurrent runs; `-Phase`, `-InitializeFromPhase`, `-Minutes` |
| `Training\Run-GaitCampaign.ps1` | unattended multi-hour, sequential batches (memory-bound: 4 fighters x 4 envs ≈ 17 GB against ~8-10 GB typically free) |

All three enforce an explicit `--base-port` and start TensorBoard exactly once.
`Start-StaminaExtension.ps1` carries two guards, each of which cost a wasted launch: a
`--resume` into a config whose `max_steps` equals the checkpoint's step count **exits
immediately having trained nothing and looks exactly like a successful short run**; and a
warm start into an existing run id silently resumes that run instead of loading the trunk
you asked for, so it refuses.

By hand:

```powershell
Training\venv\Scripts\mlagents-learn.exe Training/configs/<cfg>.yaml --run-id=<id> `
  --results-dir=Training/results --env=Builds/<Env>/<Env>.exe --num-envs=6 --no-graphics `
  --base-port=5005
```

### Flags

- **`--base-port` always explicit.** The trainer takes `--num-envs` consecutive ports from
  there; two runs on the default 5005 collide and the second hangs waiting for a handshake
  the first already answered. Space concurrent runs by at least `--num-envs`.
- **`--num-envs` is a CPU budget, not a throughput dial.** 4-8 on a 12-core box, leaving
  cores for torch threads and TensorBoard. ML-Agents' own docs are explicit that changing
  it with every hyperparameter held fixed **still changes the resulting model**, because it
  changes how experience is batched. The four shipped brains trained at **3**; a later run
  at 6 is a different run, not a faster one. Record it in the config header.
- **`--resume`** for parameter-only tweaks; **`--force`** or a new run-id for
  physics / observation / action changes.
- **`--initialize-from=<run>` resolves BY BEHAVIOR NAME**, so a cross-character fine-tune
  needs the source weights staged under the new name. `network_settings` must match the
  trunk exactly (512 x 3 here).

> **Kill TensorBoard *before* launching with `--force`, and restart it after.** It holds
> Windows handles on the run dirs, and a `--force` fired while it is live leaves the old
> contents **in place, silently, with no error**. The surviving checkpoints then outrank
> the new run's numerically for a long while, so `DeployLatestCheckpoint` ships a brain
> from the run you thought you deleted. `Deploy` is safe because it reads the top-level
> `<Behavior>.onnx`, which a run rewrites only when it finishes.

### Stopping

`Training\Stop-Training.ps1` — trainer first, then orphaned players matched by path under
`Builds/`, then TensorBoard, then optionally `-Prune`. **Killing env workers first
accomplishes nothing — the trainer respawns them.** It closes the trainer's window rather
than killing it and waits 60 s, because the final-checkpoint write on a large trunk is not
instant and killing through it truncates the `.pt`.

## 6. Do not use the Unity Editor while a run is training

Measured twice, and it is the single most expensive mistake available here. Entering Play
mode alongside 8 env players took one run from **4.2M steps/hour to 69 steps in 80
minutes** — trainers and env players all present in the process list the whole time.
Another run's env players died 2 minutes after launch during a brain deploy plus Play mode.
**Neither errored, and both look identical to a healthy run until you diff the step count.**

Deploying a brain, refreshing assets and building an env are all Editor work. Stop training
first, or accept the run.

```powershell
powershell -Command "@(Get-Process mlagents-learn -EA SilentlyContinue).Count"
# then compare the newest numbered .pt against itself 5 minutes later
```

## 7. Deploy

*PoSumo → Deploy \<Name\> Brain*, or `DeployBrain.DeployLatestCheckpoint(...)` to try a
brain from a still-running run (the trainer only writes the unnumbered `<Behavior>.onnx`
on shutdown).

Models are **overwritten in place** at `Assets/Agents/<Name>_v01/<Name>.onnx` so the
`.meta` GUID and every reference to it survive. `DeployBrain` does this and also sets the
character asset's `inferenceModel`. Copying a checkpoint does not require stopping a
headless run. The tool prints `DEPLOY RESULT:`.

**Inference runs through `com.unity.ai.inference` 2.6.1** (`Unity.InferenceEngine.ModelAsset`),
not through ML-Agents. It is the package whose editor-only `Google.Protobuf_Packed.dll`
collided with ML-Agents' copy — patch 2 above. A minor-version move there is exactly when
that patch could stop holding. **If inference goes silently wrong — a fighter that stands
still or twitches rather than erroring — suspect this before suspecting the brain.**

## 8. Judging a run

**Judge self-play fight runs on ELO, not mean reward.** They move in opposite directions
when a policy learns to farm shaping instead of winning bouts: one re-tune climbed to
reward ~36 while its ELO fell 1198 → 1140. Mean reward is measured against a moving
opponent pool and is **not comparable across runs**; ELO is.

Accept on the **shape** of the ELO curve, not a threshold:

| Curve | Verdict |
|---|---|
| monotonic slide | regression — reject |
| oscillation within a point or two of the start | noise — fine; flat ELO against a pool that is itself retraining means the policy kept pace |
| pinned just under a graduation bonus, near-zero variance | **broken episode**, not convergence — see §4 |

A fighter with large, easily-farmed shaping is the one that fails this. The fix is its
character sheet's shaping-to-win ratio, not more training.

This ELO is the **self-play** ELO in TensorBoard. `Systems_CareerStats` keeps a separate
game-ladder Elo (start 1000, K 24, zero-sum across four fighters). **Do not compare the two
numbers.**

Behavioural claims are reported as a `MatchTestHarness.Run(n)` tally (`HARNESS RESULT:`) or
a Game-view screenshot, never as an impression. The EditMode suite covers only
`Systems_CareerLadder` and `Reward_Context.San` — **a green unit run is not evidence that a
body, reward, scene or brain change works.**

## 9. `Training/results/` hygiene

It **is** the TensorBoard logdir, so it is a curated list, not a dumping ground — only runs
that back a deployed brain. It is **gitignored and absent from a fresh clone**; the
deployed `.onnx` files under `Assets/Agents/` are the only brains that ship. Anything about
resuming or `--initialize-from` assumes you re-ran training locally to recreate it.

- prune a deployed run to its final `<Behavior>.onnx`, `checkpoint.pt`,
  `configuration.yaml`, `run_logs/` and tfevents — the numbered per-step checkpoints are
  ~140 MB per run and nothing deploys from them;
- a checkpoint kept only as an `--initialize-from` source is weights, not history — park it
  in `Training/trunks/` (gitignored, outside the logdir);
- staging dirs must sit *inside* `results/` at launch (`--initialize-from` resolves
  relative to `--results-dir`) but hold no history, so they appear as empty TensorBoard
  runs — delete them once the run is stepping;
- superseded runs are deleted outright.

`Training/README.md` maps every kept config to the run and deployed brain it produced.

## 10. What invalidates every brain

Any of these means a retrain, not a tweak:

- collider shape or mass changes,
- observation count, observation **order**, or decision period,
- action count (e.g. adding a neck joint would add a 14th action *and* change the obs
  vector, since `CollectObservations` loops over `ActionCount`),
- joint ranges, torque budgets, or the fatigue model,
- a referee rule that changes how a round ends.

The recovery is usually cheap: rebuild each env, warm-start from the shipped checkpoint,
and run a short corrective pass at a reduced learning rate (1-3M steps against trunks of
12-45M) rather than retraining from scratch — **provided `Training/results/` still exists.**

**Change a losing condition in BOTH referees.** `Systems_GameMatchManager` (game) and
`Systems_SumoMatchManager` (training) have silently diverged before — by 2 m of mat, for
months — and policies then never learn the new rule is fatal. Note
`Systems_SumoMatchManager` does **not** read `GameTuning`: it carries its own copy of the
ring, spawn gap and timeout in every training scene, so a change must be written into those
scenes too. **Grep the `.unity` files to learn what an existing env trains against; the
`.cs` is only what a NEW scene inherits.**

## 11. Telemetry

`Systems_Telemetry` spawns itself via `[RuntimeInitializeOnLoadMethod]` in **Editor and
development builds only**, publishing the same numbers as JSON on
`http://127.0.0.1:<port>/metrics` and into ML-Agents' `StatsRecorder` (so per-fighter
stamina lands on TensorBoard beside reward and ELO).

TensorBoard answers "how did this run go"; the HTTP endpoint answers "what is this env
doing right now" — the question you actually have when a headless run has gone quiet.

- **Port walks upward from 8787** (12 attempts) so each concurrent env gets its own. The
  bound port is logged as `TELEMETRY RESULT:`.
- Raw `TcpListener`, not `HttpListener` — the latter needs a `netsh http add urlacl`
  reservation to bind as non-admin on Windows.
- **The socket thread never touches a Unity API.** The main thread rebuilds the JSON on a
  2 Hz timer into a reused `StringBuilder` and swaps it under a lock. A background
  `FindObjectsByType` would be an immediate crash.

> **It only started working in training envs on 2026-08-07.** `Spawn` bails unless
> `Debug.isDebugBuild || Application.isEditor`, and `BuildTrainingEnv` used
> `BuildOptions.None` — so every env player was a non-development build and the endpoint
> never opened. It now passes `BuildOptions.Development`. **Envs built before that date
> must be rebuilt**, or `curl` connects to nothing. Expect that failure shape from this
> gate generally: no error, no log line, just a refused connection.

## 12. Always run TensorBoard alongside training

```powershell
Training\venv\Scripts\python.exe -m tensorboard.main --logdir Training/results --port 6006 --reload_interval 15
```

Watch cumulative reward, **policy entropy** (collapse means premature convergence, often to
a degenerate crouch — see `AGENTS.md` on the walk-in gait), value loss, and the per-fighter
stamina stats. A second bind on 6006 fails quietly enough that you notice an hour later
with no graphs, which is why the wrappers start it exactly once.
