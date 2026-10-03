---
name: profile-kvoffload-replay-all
description: Run all four KV-offload benchmark variants (NoOffload, CPUOffload, SharedStorage, Certus-SPDK) against the same 12-turn ShareGPT replay and present throughput in one side-by-side table. Use when the user wants to compare offload backends end-to-end.
---

# profile-kvoffload-replay-all

Orchestrate the four KV-offload benchmark variants over the same replay workload
and present their throughput in a single comparison table. All real work is done
by `benchmarks/kv-offload-replay/profile_all.sh`; this skill collects inputs,
previews what will run, launches the orchestrator, and formats the result.

## Variants

| Variant | Backend | Image / binary |
|---|---|---|
| NoOffload | GPU-only baseline | `certus-offload` (OFFLOAD_MODE=none) |
| CPUOffload | vLLM OffloadingConnector → host RAM | `certus-offload` (default mode) |
| Tiered-CPU-FS | vLLM native CPU primary + FS secondary | `certus-offload` (SECONDARY_TIER=fs) |
| SharedStorage | `llmd_fs_backend` RAID0/XFS | `certus-sharedstorage` |
| Certus-SPDK | gRPC client + `certus-server-yaml` (SPDK NVMe) | `certus-grpc` + host server |

## Inputs

- **`--device-pci <DDDD:BB:DD.F>`** — NVMe PCIe address for the Certus-SPDK
  server (repeatable). Omit → Certus-SPDK is SKIPPED.
- **`--shared-fs <dir>`** — filesystem bind-mounted to `/mnt/fs-backend-bench`
  for SharedStorage. Omit → SharedStorage is SKIPPED.
- **`--model-fs <dir>`** — filesystem for the HF cache and gRPC podman store
  (default `/mnt/certus1`). HF cache lives at `<model-fs>/hf-cache`.
- **`--model <hf-id>`** — applied to all four variants. Default
  `NousResearch/Meta-Llama-3-8B`. NOTE: the baked dataset and drivers are built
  for Llama-3; `ibm-granite/granite-4.1-8b` renders empty prompts and fails.
- Tuning: `--num-convs 450`, `--output-tokens 150`, `--max-model-len 8192`,
  `--max-num-seqs 64`, `--gpu all`, `--memory-tier-size 32G`, `--cpu-bytes`,
  `--dram`. `--build` to build missing images. `--only`/`--skip` to subset.
  `--logdir` for output (default `<model-fs>/kvprofile-<runid>`).

## Workload (`--workload`)

The default (no `--workload`) replays the baked 450×12 ShareGPT set **in
process** (each variant embeds `AsyncLLM`). Other values: `sharegpt`
(turn-count-selected corpus), `long-doc-qa` (synthetic long-doc QA), and
`synthetic-agentic` (below).

### `--workload synthetic-agentic` — server mode

`synthetic-agentic` selects the [inference-perf](https://github.com/lenadankin/inference-perf/tree/synthetic_data_enabled)
agentic ReplayGraph DAG (tool loops, recursive sub-agent fan-out, mid-session
context compaction, a shared system-prompt prefix). inference-perf is an
**HTTP-only** load generator, so this workload **cannot** run through the
in-process drivers. `profile_all.sh` instead runs each backend in **server
mode**: one `vllm serve` (the KV backend is just its `--kv-transfer-config`
connector arm, via `benchmarks/synthetic-agentic/serve_vllm.sh`) driven by the
inference-perf client container over `:8000`. Workload ⟂ backend: the client only
sees `BASE_URL`; the connector is chosen entirely server-side.

- **Backend mapping:** NoOffload→`none`, CPUOffload→`cpu`, Tiered-CPU-FS→`tiered`,
  Certus-SPDK→`certus` (reuses the same host SPDK server + `/dev/shm` mailbox, now
  attached by `vllm serve` via `--ipc=host`). **SharedStorage has no serve_vllm
  arm and records SKIPPED.** `--only`/`--skip` subset as usual.
- **Determinism = fairness.** The workload is defined by
  `benchmarks/synthetic-agentic/configs/synthetic_agentic.yaml`; its fixed `seed`
  makes every backend replay a byte-identical request stream (no materialised
  trace). Session count is `num_sessions` in that YAML, **not** `--num-convs`
  (which is N/A here and reported as 0).
- **Client image.** Needs `synthetic-agentic-client:latest`
  (`benchmarks/synthetic-agentic/Dockerfile.inference-perf`). `--build`/`--rebuild`
  builds it; otherwise a missing image SKIPs the backend with that reason.
- **max-model-len.** Agentic sessions + compaction (trigger 8500) need
  >8192; the server-mode path defaults to 32768 (serve_vllm applies Llama-3 RoPE
  ×4), honouring a larger `--max-model-len`.
- **Optional generate-first (audit only).**
  `benchmarks/synthetic-agentic/generate_trace.sh` dumps a few deterministic
  session graphs for inspection — it is **not** an input to the run (generation is
  inline by seed). Skip it for a normal run; use it to diff exactly what replays.

## Steps for Claude

1. **Collect inputs** from the invocation. If `--model` was NOT supplied, ask via
   AskUserQuestion — options: `NousResearch/Meta-Llama-3-8B` (recommended /
   default), `ibm-granite/granite-4.1-8b`, custom HF id. Default to Llama-3.
   Do not prompt for anything else; other flags have working defaults.

2. **Preflight summary.** Before launching, state which of the four variants will
   run vs SKIP and why:
   - Check images: `podman image exists certus-offload` (covers NoOffload,
     CPUOffload and Tiered-CPU-FS), `certus-sharedstorage`; gRPC image in the model-fs store
     (`podman --root <model-fs>/podman/storage image exists localhost/certus-grpc`).
   - SharedStorage needs `--shared-fs` pointing at a real dir; Certus-SPDK needs
     `--device-pci` and a built `target/release/certus-server-yaml`.
   - If images are missing, note that `--build` will build them. The SharedStorage
     image build needs the `llmd_fs_backend` repo; the script auto-discovers it at
     `<model-fs>/llm-d-kv-cache/kv_connectors/llmd_fs_backend` (its location on this
     host), falling back to `$HOME/...`. Override with the `FS_BACKEND_DIR` env var.
     Offer to add `--build`.
   - For `--workload synthetic-agentic`, also check the inference-perf client image
     (`podman image exists synthetic-agentic-client:latest`) — missing ⇒ every
     backend SKIPs unless `--build`/`--rebuild` is passed. Note SharedStorage will
     SKIP (no serve_vllm arm), and Certus-SPDK still needs `--device-pci` + the
     built `certus-server-yaml` (server mode reuses that same host SPDK server).

3. **Launch** `benchmarks/kv-offload-replay/profile_all.sh` with the resolved
   flags. A full four-variant run takes ~15–60 min (each variant loads the model
   and replays 450 conversations), so run it in the background and monitor the
   log until it finishes. The script tees each variant to `<logdir>/<variant>.log`
   and never aborts the whole run on a single variant's failure.

4. **Report.** Read `<logdir>/results.json` and present the comparison table.
   Call out any SKIPPED/FAILED rows with the reason and the one-line fix (e.g.
   "SharedStorage SKIPPED — pass `--shared-fs /mnt/fs-backend-bench`"; "add
   `--build`"; "check `<logdir>/server.log`"). `tokens_per_sec` is computed
   uniformly as `generations × output_tokens ÷ wall` so variants are comparable
   even though each driver prints a different native metric.
   - **Server mode (`synthetic-agentic`)** differs: `generations`/`tokens_per_sec`
     are null (a session-graph DAG has no flat per-round generation count), so
     rank backends by `wall_s` and the `native_metric` throughput scraped from
     inference-perf, and point at the full inference-perf report under `<logdir>`
     (the richest comparable: throughput, TTFT, per-request latency). Per-backend
     server logs are `<logdir>/serve-<connector>.log`.

## Notes / prerequisites (not automated)

- The GPU must be free; the script reaps stale `*-bench` containers and warns if
  a GPU already has memory in use.
- The Certus-SPDK server lifecycle (start, poll `:50051`, teardown with SIGTERM
  then SIGKILL after ~8s — it ignores SIGTERM during SPDK teardown) is handled by
  the script. It requires host hugepages + the NVMe device unbound from the
  kernel driver.
- SharedStorage requires the RAID/XFS mount to exist; host RAID/XFS/hugepage
  setup (`tools/configure-bench.sh` and friends) is a prerequisite, out of scope.
  Building its image needs the `llmd_fs_backend` repo (auto-discovered under
  `<model-fs>/llm-d-kv-cache/...`, or set `FS_BACKEND_DIR`). The build compiles a
  torch C++ extension (~10–30 min) whose CUDA arch must match the GPU (A100 = sm_80).
- The HF cache lives on `--model-fs` (default `/mnt/certus1`), not `/home` — the
  small `/home` partition fills up mid-download otherwise.
