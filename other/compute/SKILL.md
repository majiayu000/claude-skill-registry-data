---
name: compute
description: Plan, profile, schedule, and recover large CPU/GPU experiments and data batches on shared machines. Use before scaling training, inference, rendering, extraction, or evaluation; excludes ordinary small builds and remote model API fan-out.
---

# Compute — measure, admit, run, recover

Use existing schedulers and profilers. This workflow selects and verifies them;
it is not a scheduler and does not reserve capacity by itself. Do not build a
new queue or deploy a cluster merely to execute a batch.

## Resolve placement and the execution backend

Read `~/.clade/compute-policy.md` when present, then the project's execution
instructions and the site's acceptable-use policy. Keep private hostnames,
paths, budgets, and incident notes in that user-owned file, outside public
repositories. Current user instructions supersede older personal preferences;
they do not implicitly waive site restrictions or grant administrator access.
If the profile is missing, use known authorized resources and record defaults;
do not invent remote hosts, reservations, or permission to displace others.
The profile is optional: a standalone local machine can use a bounded local
runner after the same preflight. No specific host, quota value or scheduler is
required by Clade itself.

Resolve the site's effective limits for the chosen user, group/project/account,
partition/queue and service class (such as QOS), using its documented precedence.
Check CPU/GPU/RAM, concurrent and submitted job counts, wall time/compute credits,
and storage bytes/inodes where applicable. Record scope, source, current usage
and remaining allowance; include other jobs/sessions charged to that scope.
Do not give each host or worker a fresh copy of a fleet-wide allowance. Derive
this run's budget from the effective remaining quotas, its actual allocation,
project/user caps, physical headroom and enforced cgroup/OS limits together.
An idle host or free VRAM is not an allocation. Personal preferences and
dedicated-host permission cannot relax site restrictions or other binding caps.
If quota details are hidden, use the site's authoritative admission system and
record what remains unknown; missing visibility is not unlimited entitlement.
If neither authorized limits nor authoritative admission can be established,
keep that lane PREPARED/BLOCKED instead of guessing a fleet-wide allowance.

Before starting even a compute smoke run, state its host, backend, resource
limits, and scratch location. Follow the profile's host tiers; within a tier,
choose by current headroom, data locality, and measured end-to-end throughput.
Use fallback hosts only under the profile's conditions. A shell on a machine
is not a reason to run the batch there.

Read [backend selection](references/backend-selection.md) for the applicable
backend. Inspect what is actually installed and usable: command/version,
controller connectivity, node state, user access, resource enforcement, and
durable restart support. An installed Slurm client, empty queue, live Ray
dashboard, or `tmux` session is not proof of readiness. If site policy requires
a broken backend, park that lane with evidence; do not bypass it.

## Preflight and local staging

Capture a timestamped snapshot on each candidate host:

- CPU affinity/cgroup quota and load; available RAM, swap pressure and effective
  ancestor cgroup limits; other users' workload totals without their secrets.
- GPU model, utilization, free VRAM, active allocations/processes and driver
  health. A failed probe means unknown capacity, never an idle GPU.
- Source, scratch and checkpoint mount types, local disk space/inodes, and
  network/I/O pressure. Resolve symlinks: a path named `ssd` may still be NFS.
- Scheduler allocations plus work outside it. Recheck at admission; the
  snapshot is not a reservation. Coordinate our simultaneous sessions through
  the existing scheduler or one shared admission mechanism covering every
  applicable quota scope, including aggregate user/project limits across hosts.

For NFS/network-backed random I/O or many small files, stage the required inputs
to verified host-local SSD/NVMe before compute. Bound transfers independently
of workers: avoid all hosts flooding one shared disk/link. Use resumable copies
or packed shards with an input manifest/checksums; validate before use. Reserve
space for outputs, checkpoints and temporary expansion. If it does not fit,
stage bounded chunks. Do not move the whole dataset to RAM or silently revert
to random NFS access. Measure staging, reads, writes and final sync separately.

## Smoke and profile before scale

Run the real pipeline on representative small, typical, largest and malformed
inputs, with the same environment, mounts and backend intended for the batch.
Check output correctness first, then measure a warmed-up sustained sample:

- Stage wall times, items/s, p50/p95 item duration and scheduler overhead.
- Peak **process-tree/cgroup** RAM, peak VRAM, CPU/GPU duty cycle, I/O wait,
  disk/network throughput, and output/scratch growth.
- For a bottleneck, use a short relevant trace: `pidstat`/`iostat`, Python
  profiling, PyTorch Profiler or Nsight Systems. Avoid an expensive full-run
  trace. Confirm profiler overhead with an unprofiled timing sample.

Increase concurrency in bounded steps only while useful throughput improves
within the resource budget. Account for parent/worker memory, model replicas,
prefetch buffers and library thread pools. Set BLAS/OpenMP/framework threads
explicitly so outer workers do not multiply inner threads without a budget.
Do not use GPU for a CPU-only tool or infer acceleration from utilization.

Choose worker count from the effective budget above, measured peak RAM with
headroom, VRAM, scratch, and observed storage/network limits. With no execution
headroom, submit only a request that can eventually fit, within submission
limits; report QUEUED only with backend acceptance. Preserve personal shared-host
caps; dedicated-host permission changes only the owner's cap for that run.
Record the measurements and selected limits.
For RAM, subtract shared overhead and reserve first, then divide by measured
per-worker peak: `floor((budget - shared - reserve) / worker_peak)`. Recheck the
aggregate at that concurrency; neither RSS sums nor this estimate are a limit.

## Partition and admit work

Keep more bounded shards than execution slots; size by measured cost (pages,
pixels, tokens, bytes or prior time), not just equal file counts. Separate
outliers/resource classes so one huge item does not stall a whole barrier.
Use dynamic assignment of ready shards with bounded in-flight work and
backpressure between CPU decode, GPU inference, and output stages. Prefer data
locality when transfer cost exceeds rebalancing benefit. Rebalance remaining
work, not already running stateful jobs; avoid speculative duplicate side
effects. Multi-GPU training needs coherent allocation, not independent workers.

Submit through the selected backend with explicit CPU/RAM/GPU/time requests
and OS-enforced limits where supported. Keep one authority for admission;
nested Ray/Dask/Parallel workers must fit inside its allocation. Full hosts
leave work pending in a durable queue, with its job ID and reason recorded.
Respect pending-job/submission caps too; retain excess shards in the durable
manifest instead of flooding the scheduler. If even one shard exceeds a hard
per-job limit, reduce/repartition it or report BLOCKED; waiting cannot fix it.
Pressure during execution stops new admissions, checkpoints at safe boundaries
and requeues unfinished work. Do not evict other users or run a busy retry loop.
Use bounded backoff and a real backend/timer wake-up; a note saying "queued" is
not a queue. Separate remote API quotas from local compute capacity.

## Prove recovery before unattended execution

Use stable task/shard IDs tied to the input manifest, code revision, environment
and parameters. Store pending/running/validated/failed status durably, with
attempt ownership, logs, retry limit and exact resume command. A scheduler
restart retries work; it does not restore application state automatically.

Write results/checkpoints to temporary files on local disk, flush and atomically
rename on the same filesystem after validation. Replicate validated generations
to durable storage with checksums and a completion marker committed last. Retain
the previous good generation until the new copy is verified. Never consume a
partly copied checkpoint or treat file existence as success. Bound and record
the amount of work that can be lost between durable checkpoints.

For training, capture optimizer/scheduler/scaler, RNG, sampler/data cursor and
step as well as model weights when required by the framework's resume contract.
Make outputs idempotent; reclaim abandoned work only after verifying its owner
is gone. For at-least-once execution, validate before skipping completed shards.

On a tiny **task-owned** fixture, interrupt a worker, restart through the actual
backend, and verify: completed outputs are unchanged; incomplete work resumes
or retries; a partial/corrupt checkpoint is rejected; output counts/checksums
match; no duplicate owner commits results. Test a resource-full pending state
and release as well. Never reboot a shared host for this test.

Prove restart persistence separately (persistent units, enabled boot/timer
activation, user lingering when needed, mounts/environment available after
login loss). A transient `systemd-run`, `nohup`, or `tmux` is not reboot recovery.
After an actual incident recheck uptime, mounts, driver, limits and the durable
manifest before resuming. Respect any private cooldown/health conditions.
Report reboot recovery as UNVERIFIED unless actually observed; interruption
testing alone cannot prove power-loss recovery.

## Evidence and stopping conditions

Keep private execution evidence under the task's existing evidence directory or
`~/.clade/compute/<run-id>/`: preflight timestamps, selected backend/version and
placement, code/input IDs, resource requests and enforced limits, staging checks,
effective quota scopes/usage and admission decisions,
smoke/profiling measurements, worker/shard tuning, queue IDs, recovery test and
resume command, checkpoint locations, output validation and final job status.

Do not scale after failed correctness, unknown mandatory resources, inadequate
space, or failed recovery. Park a broken scheduler/driver with its observed
error and continue independent preparation. Do not reset nodes, reboot, install
system packages or alter shared scheduling policy by inference. Distinguish
PREPARED, QUEUED, RUNNING, COMPLETE and BLOCKED; a submitted job is not completed
inference. Completion includes validated outputs and verified durable sync.
If the backend cannot accept work, report PREPARED/BLOCKED with the saved
submission plan; call it QUEUED only after a real durable queue accepts it.
