---
name: research-resource
description: "Use when registering predefined compute resources, probing short-term availability, choosing placement, allocating capacity, or releasing an allocation."
---

# research-resource

## Purpose

Use this skill to place an Experiment on a compute resource that the user has already defined. The
resource registry and allocation lifecycle are management state. Availability probes are short-lived
observations. Resource policy is part of the user's mutable working state.
Under User-First Reconcile-After, execution and terminal Evidence come before
any advisory placement reconciliation.

The harness recommends, the agent decides, and the user defines which servers exist.

## Storage and authority

Resolve the managed root once:

```bash
export RESEARCH_ROOT="${RESEARCH_ROOT:-.research}"
```

With the default root, persistent management data is in `.research/state/`, Run evidence is in
`.research/experiments/`, and human views are in `.research/interface/`.

| Data | Location | Meaning |
| --- | --- | --- |
| Resource registry | Resource aggregates in `$RESEARCH_ROOT/state/research.sqlite3` through bounded queries | Persistent authority |
| Allocation lifecycle | ResourceAllocation aggregates in the same database | Persistent occupancy authority |
| Folded current state | `$RESEARCH_ROOT/state/current.json` | Rebuildable projection |
| Availability snapshots | `$XDG_RUNTIME_DIR/trustworthy-research/<workspace-hash>/resource_snapshots/` | Short-lived local projection |
| Human resource views | `$RESEARCH_ROOT/interface/` | Read-only generated projection |

When `XDG_RUNTIME_DIR` is unset, `ResearchPaths` selects a per-user temporary fallback. Snapshots do
not belong in `$RESEARCH_ROOT/state/`, and they do not survive as allocation facts.

Never edit `research.sqlite3`, `events.jsonl`, `current.json`, or interface
files. The CLI validates a command and commits it through the state writer.

## Authority boundary

- The user names each server and confirms its connection and capacity fields.
- `lib.resource_alloc` validates, measures, ranks, and records. It does not launch a command or drive
  a remote session.
- The server's execution skill owns remote connection, scheduler submission, and job verification.
- An open ResourceAllocation aggregate reserves capacity. Conversational memory does not.
- A missing or stale snapshot means availability is `unknown`. It never means free.
- A reconciliation suggestion cannot allocate, overbook, rebind, or release an
  allocation. Only the validated allocation lifecycle can change occupancy.

## Commands

All commands accept `--research-root`; the `RESEARCH_ROOT` environment variable is the default.

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" register
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" list

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  snapshot --server <name> --probe

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  snapshot --server <name> --from-nvidia-smi <file>

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  recommend --pkg <package> --exp <experiment> --gpu-count 1

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  allocate --server <name> --pkg <package> --exp <experiment> \
  --gpu-count 1 --reason "<reason>"

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  link --alloc <allocation-id> --run-id <run-id>

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  release --alloc <allocation-id> --outcome <terminal-status>

python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" status
```

Every mutation rejects before its event is appended. Unknown resources, stale allocation ids,
overbooking, and double release return an error without changing state.

## Register a resource

Ask for the typed fields that affect placement:

- `name`;
- `kind`: `local`, `ssh`, or `slurm`;
- `control`: direct access or an existing tmux gateway;
- declared GPU type, count, and memory;
- scheduler account, partitions, and maximum duration when applicable;
- stable execution presets exposed during Package review;
- working directory and environment;
- data-locality and capability tags;
- the execution skill that owns remote work.

Use `notes` only for details that do not affect ranking. Promote a recurring decision input to a
typed field.

Example:

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" register <<'EOF'
{"name":"local","kind":"local",
 "gpus":[{"type":"a6000","count":2,"mem_gb":48}],
 "presets":[{"id":"local","label":"Local","mode":"direct"}],
 "tags":["dataset-local"]}
EOF
```

See [registry schema](references/registry-schema.md) for the full record.

For Bunya, register one physical `slurm` Resource with both
`bunya-sbatch` and `bunya-interactive` presets. Do not register two physical
Resources for the same cluster. Interactive mode first reuses a valid existing
allocation and requests one only when none exists.

## Record Package placement

Before the initial Package bootstrap, or when the user adds an Experiment,
show the active preset range and confirm one ordered preset list and capacity
profile chain for every selected Experiment.
If the user already gave the exact choices, use them without reopening the
decision.

Store the result in `Package.resourcePolicy`, not `Experiment.spec`. Every
profile carries its own `config_ref`, GPU type and count, per-GPU memory, host
RAM, and minimum duration. Create the referenced config before activation.
Omitted presets and profiles are forbidden fallbacks.

`Package.resourcePolicy` is current user-owned working state. A later change
uses the typed Package plan transaction and versions the policy without
rewriting a frozen Run or finalized Evidence. Activation is only the initial
bootstrap path; old phase, readiness, reopen, and Scope gates do not decide
placement.

Keep these three facts separate:

- the Resource registry defines stable servers, presets, and scheduler maps;
- `Package.resourcePolicy` defines the reviewed per-Experiment allowlist and
  fallback order;
- probes, queue state, and the chosen allocation are run-time observations.

At run time, reuse a compatible open interactive allocation first. If none
exists, request the first reviewed profile. When Slurm rejects that request,
inspect the live partition, QoS, GRES, memory, and duration constraint, then
try only the next reviewed profile or preset. Stop when the allowlist is
exhausted; never invent a hardware downgrade.

## Probe before placement

For the local machine:

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  snapshot --server local --probe
```

For a remote resource, collect this command through the resource's execution skill:

```bash
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu \
  --format=csv,noheader,nounits
```

Save the output locally, then normalize it with `--from-nvidia-smi`. Do not create an extra remote
connection when the registered control path requires an existing tmux gateway.

A snapshot expires after 600 seconds. Recommendation may still include an unprobed resource, but its
availability is `unknown` and ranks below confirmed idle capacity.

## Recommend and allocate

Build the requirement from the selected Experiment:

- `gpu_count`;
- optional `gpu_type` and `min_mem_gb`;
- `min_hours` from the expected-duration class;
- required data-locality tags.

`recommend` returns candidates and blocked reasons. Ranking prefers confirmed free capacity, then
lower start latency, then the smallest sufficient memory class.

Allocate only after choosing a candidate:

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  allocate --server local --pkg <package> --exp <experiment> \
  --gpu-count 1 --gpu-ids 0 --reason "evaluation"
```

Keep the returned `alloc_id`.

For a local canonical Run:

```bash
CUDA_VISIBLE_DEVICES=0 python3 -m lib.experiments.launch \
  --workspace . \
  --research-root "$RESEARCH_ROOT" \
  --pkg <package> \
  --exp <experiment> \
  --server local \
  --alloc <allocation-id> \
  --tmux-session <name> \
  -- bash scripts/run_experiment.sh
```

The launcher verifies the open allocation and binds the authorized Run. For a remote job, launch
through the registered execution skill, then bind the scheduler job id:

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  link --alloc <allocation-id> --job-id <job-id>
```

Manual `--run-id` linking accepts only an existing open Run that was authorized
for the same allocation, Package, and Experiment. It cannot attach an
allocation to an unrelated or invented Run id.

If the human interface needs a resource summary, record the state-backed package observation through
`research-op`. Do not write a tracker page or interface data file.

After a Run, reconcile only the observed allocation and callback facts. A
proposed policy change waits for explicit user acceptance and cannot change the
allocation that was bound to the completed Run.

## Release

Release capacity only after terminal evidence is verified and the allocation
still belongs to the same Package and Experiment:

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" \
  release --alloc <allocation-id> --outcome COMPLETED
```

Accepted canonical terminal outcomes include `COMPLETED`, `FAILED`, `HALTED`, and `SKIPPED`.
Resource release is separate from the user's terminal Package decision, and an
advisory reconciliation cannot substitute for either the verified evidence or
that decision.

Before ending the session:

```bash
python3 lib/resource_alloc/cli.py --research-root "$RESEARCH_ROOT" status
```

A linked Run that is terminal while its allocation remains open is a leak. Release it or record the
specific blocker.

## Failure routing

- Capacity rejection: run `recommend` again. Do not edit state to free a GPU.
- Stale snapshot: probe again before claiming confirmed availability.
- Changed hardware or scheduler policy: ask the user to confirm an updated Resource record.
- Remote submission failure: keep the allocation open while a bounded retry is justified, or release
  it with the verified outcome.

## References

- [registry schema](references/registry-schema.md)
- [worked example](references/worked-example.md)
