---
name: deploy-kimi-k26-on-rtx-pro-6000
description: Deploy and serve Moonshot Kimi-K2.6 (1T MoE, MLA, 256K context, vision) in a user-chosen quantization — official INT4 QAT (moonshotai/Kimi-K2.6, compressed-tensors→Marlin; vLLM or SGLang) or NVFP4 (nvidia/Kimi-K2.6-NVFP4, ModelOpt FP4; vLLM only — SGLang NVFP4 is NaN-broken on sm_120) — on a Linux server (verified Ubuntu 26.04) with 8× NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB, sm_120) GPUs. The quantization and the engine are both chosen at deploy time with a hardware-based recommendation. Runs an official-image Docker container via nvidia-container-toolkit CDI (--device nvidia.com/gpu=all --ipc=host --network host, bind-mounted weights; --network host is required for NCCL's GPU-to-GPU transport / IB-RoCE GPUDirect RDMA, and the server binds 0.0.0.0 with off-box clients reaching it through an authenticated Caddy proxy that upstreams over loopback 127.0.0.1 — structural, no firewall), exposing an OpenAI-compatible API on :30000 behind one static systemd service `kimi-k26` (quant + engine selected via its EnvironmentFile — only one 595 GB variant fits the 8-GPU pool at a time). Use when deploying or serving Kimi-K2.6 INT4 or NVFP4 on RTX PRO 6000 Blackwell / sm_120 hardware (vLLM-in-Docker, or SGLang-in-Docker for INT4) — or troubleshooting NCCL /dev/shm "unhandled system error" in GPU containers, sm_120 "no kernel image" errors, a missing-`ninja` JIT build failure (-runtime image tag), FlashInfer CuTe-DSL MLIR ICE (llvm.mlir.global_dtors), a vLLM startup ValueError "larger than the available KV cache memory" (gpu-memory-utilization is NOT mem-fraction-static), an OOM→SIGQUIT crash from raising SGLang mem-fraction above 0.85, NVFP4 TRITON_MLA shared-memory OutOfResources at CUDA-graph capture (Required 102400 > limit 101376), NVFP4 "b12x fused MoE requires CUDA 13", NVFP4 offline trust_remote_code FileNotFoundError for a module under blobs/ (e.g. tool_declaration_ts.py), or a slow/hung MoE weight load.
---

# Deploy Kimi-K2.6 (INT4 QAT or NVFP4) on 8× RTX PRO 6000 Blackwell Server Edition (sm_120)

Serve **Kimi-K2.6** (1T MoE; MLA; 256K; MoonViT vision) in a **user-chosen quantization**, with an
**official-image Docker** container — OpenAI-compatible API on `:30000`, **TP=8**, weights bind-mounted
read-only from local NVMe, all in VRAM. Both the **quantization** and the **engine** are chosen at
deploy time (steps 2–3) with a hardware-based recommendation:
- **INT4 QAT** — [moonshotai/Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6); compressed-tensors → **Marlin** (auto); **vLLM or SGLang**; stock images, no patch. **Recommended on sm_120** (official, simplest, both engines verified).
- **NVFP4** — [nvidia/Kimi-K2.6-NVFP4](https://huggingface.co/nvidia/Kimi-K2.6-NVFP4); ModelOpt FP4 (`--quantization modelopt_fp4`); **vLLM only** (SGLang NVFP4 = NaN on sm_120). Needs a **patched CUDA-13 image** (`build_nvfp4_image.sh`) + **offline remote-code prep** (`prep_remote_code.sh`). On sm_120 it gives **no throughput win** (PCIe-comm-bound: Marlin ≈ native b12x, native is actually ~12% slower) — prefer it on **datacenter Blackwell (sm_100/B200)** where native FP4 (cutedsl) is tuned, or when you specifically need the NVFP4 checkpoint.

**Hardware target:** 8× **RTX PRO 6000 Blackwell Server Edition** (GB202, 96 GB, sm_120) — ~595 GB of
weights + KV cache need the full 8×96 GB pool; PCIe-only, no NVLink. Same-chip Workstation/Max-Q
variants should behave identically (unverified). The host needs only the NVIDIA driver (≥570, open
kernel module, incl. nvidia-persistenced), Docker, and nvidia-container-toolkit — **no CUDA
toolkit, no Python packages** (the download check uses stock python3 + curl).

**Why Docker-only (current best practice):** the official images ship precompiled sm_120 kernels with
their own CUDA + glibc, so the host-JIT failure class a native venv fights (glibc≥2.41 `rsqrt`
header conflict, `ninja`, JIT pre-warm against host CUDA) doesn't exist here, and the deploy
reproduces across hosts — both of those sm_120 fixes are empirically confirmed unnecessary
in-container (image glibc 2.39; the CuTe-DSL norm ICE does **not** reproduce). GPU access uses
**CDI** (`--device nvidia.com/gpu=all`, plain runc — not the legacy `--gpus` runtime hook). Treat
step 6 as the go/no-go gate before fronting traffic.

## Workflow

1. **Verify host** — `nvidia-smi`: GPU model/count/VRAM (this drives the **quantization + engine**
   recommendations in steps 2–3); persistence daemon active (`systemctl is-active nvidia-persistenced` — ships with the
   driver and still matters for containers: it keeps GPU state resident across container restarts;
   ad-hoc fallback `sudo nvidia-smi -pm 1`); ~650 GB free on local NVMe; GPU containers work via
   CDI (spec: `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`):
   ```bash
   docker run --rm --device nvidia.com/gpu=all --entrypoint nvidia-smi <engine-image>
   ```
   (Legacy alternative to CDI: `--gpus all` — see REFERENCE.md.)

2. **Choose the quantization** — ask with AskUserQuestion: *"Which Kimi-K2.6 quantization?"*, options
   **INT4 QAT** and **NVFP4** (the tool adds "Other"), marking one **(Recommended)** by the step-1 GPU:
   - **sm_120 (RTX PRO 6000 Blackwell — reference hardware) → recommend INT4 QAT.** Official, both
     engines verified, stock images (no patch). NVFP4 here buys **no throughput** — the box is
     PCIe-comm-bound (no NVLink), so Marlin-of-INT4 ≈ Marlin-of-NVFP4, and the *native* FP4 path
     (`flashinfer_b12x`) measured **~12% slower** than Marlin in a 2026-06-11 A/B; it also needs a
     patched CUDA-13 image + offline remote-code prep (step 4b). Pick NVFP4 only if you specifically
     need that checkpoint.
   - **Datacenter Blackwell (sm_100 / B200) → recommend NVFP4** — native FP4 (FlashInfer cutedsl) is
     tuned there; the FP4 tensor cores are the real win. (Not verified by this skill — upstream path.)
   - **Hopper / Ada / Ampere (pre-Blackwell, no FP4 tensor cores) → INT4 QAT** (NVFP4 would only dequant).
   Sets the checkpoint + flags — INT4: `moonshotai/Kimi-K2.6` (compressed-tensors→Marlin, auto-detected,
   no `--quantization`). NVFP4: `nvidia/Kimi-K2.6-NVFP4` (`--quantization modelopt_fp4`, fp8 KV,
   `--disable-custom-all-reduce`, `--moe-backend marlin|flashinfer_b12x`).

3. **Choose the engine** — AskUserQuestion *"Which engine?"*:
   - **NVFP4 → vLLM only** (don't ask; **SGLang NVFP4 = NaN on sm_120**, sgl #18954 — `serve_docker_sglang.sh`
     hard-refuses it).
   - **INT4 → SGLang vs vLLM**, mark one **(Recommended)** by hardware (both verified 5/5, 2026-06-11):
     - **sm_120 → recommend SGLang** — faster at every concurrency (+34% @ c1 … +29% @ c128 vs vLLM) and
       serves full 256K at mem-fraction 0.85; vLLM here needs util 0.95 and ~131K with bf16 KV.
     - **Other hardware → recommend vLLM** — model-card primary path, precompiled kernels, no JIT dep.
   The (QUANT, FRAMEWORK) pair is the whole deploy identity; it goes in the env file (step 7), not the
   service name.

3b. **NVFP4 only — choose the MoE backend** (skip entirely for INT4) — AskUserQuestion *"Which NVFP4
   MoE backend?"*:
   - **marlin (Recommended on sm_120)** — measured **faster at every concurrency** (~12% end-to-end;
     the box is PCIe-comm-bound, so the native-FP4 GEMM speedup never reaches the wire) and leaves
     **more KV** (b12x reserves extra workspace). The safe throughput pick.
   - **flashinfer_b12x** — the **native FP4 tensor-core** path (vLLM PR #40082; needs the CUDA-13
     patched image step 4b builds anyway). Pick it to exercise the FP4 tensor cores, or on hardware
     where native FP4 is tuned (datacenter Blackwell uses `flashinfer_cutedsl` instead). Confirm the
     dispatch after launch with `scripts/assert-native.sh kimi-k26` (NATIVE FP4 vs MARLIN fallback).
   Sets `MOE_BACKEND` in the env file (step 7); `serve_docker_vllm.sh` defaults to `marlin` if unset.
   (A/B numbers: the `llm-inference-benchmark` skill.)

3c. **Choose the KV-cache dtype** — AskUserQuestion *"Which KV-cache dtype?"*, options derived from
   the (engine, quant) just chosen; mark the first **(Recommended)**:
   - **SGLang + INT4** → **`fp8_e4m3` (Recommended)** — verified on the reference host: KV pool
     2× (116K→232K tokens, full-256K single request fits), verify 5/5 incl. vision, throughput
     parity through c64 and +13.5% at c128. | `auto` (bf16 — engine default, most conservative
     numerics, pool 116K) | `fp8_e5m2` (more exponent range, less mantissa — accepted by SGLang's Triton MLA backend, runtime-unverified here).
   - **vLLM + INT4** → **`fp8` (Recommended)** — ~2× KV pool, and **required to reach 256K-class
     context** on 96 GB GPUs (bf16 KV tops out ~131K `MAX_MODEL_LEN`). | `auto` (bf16 — the
     verified 0.95/131K config).
   - **vLLM + NVFP4** → **`fp8` (Recommended — effectively required)**: the NVFP4 checkpoint ships
     FP8 KV scales; `serve_docker_vllm.sh` already defaults it for `QUANT=nvfp4`. | `auto` (ignores
     the shipped scales; bigger KV bytes — only for debugging numerics).
   *(Why the vLLM rows list no `fp8_e5m2`: on sm_120 vLLM serves Kimi through the **TRITON_MLA**
   attention backend, whose KV menu is `{auto/bf16, fp8 = fp8_e4m3}` only — `fp8_e5m2`, `nvfp4`,
   `turboquant_*` belong to non-MLA backends and hard-fail backend validation at startup. Verified
   in-image, vLLM 0.22.1. SGLang uses a different MLA kernel, so its row is governed by its own
   supported set — see the SGLang+INT4 row.)*
   KV dtype changes numerics → re-run `verify.sh` after switching. Sets `KV_CACHE_DTYPE` in the env
   file (step 7). (Measured impact tables: the `llm-inference-benchmark` skill.)

4. **Download checkpoint** (~595 GB) into the HF hub cache, pinned to a commit. **Respect `HF_HOME`**
   (default `~/.cache/huggingface`; set `HF_HOME` to a big-NVMe cache root) — never hardcode paths. `hf`/Xet may deadlock → the script falls back to parallel curl, verifies size/count
   vs the paginated HF tree API (curl + python3 stdlib only), writes `refs/main`:
   ```bash
   bash scripts/download.sh moonshotai/Kimi-K2.6 <commit-sha>      # INT4
   bash scripts/download.sh nvidia/Kimi-K2.6-NVFP4 <commit-sha>    # NVFP4
   ```

4b. **NVFP4 only — build the patched image + fix offline remote-code** (skip entirely for INT4):
   ```bash
   bash scripts/build_nvfp4_image.sh                       # -> kimi-k26-nvfp4-vllm:cu130-mla
   bash scripts/prep_remote_code.sh nvidia/Kimi-K2.6-NVFP4 # de-symlink snapshot .py (run as cache owner, not root)
   ```
   Why: native FP4 MoE needs **CUDA 13**, and Kimi MLA on sm_120 can only use **TRITON_MLA**, whose
   grouped-decode kernel OOMs at graph capture (smem 102400 > 101376) until the `num_stages` patch; and
   offline `trust_remote_code` (transformers ≥5.10) can't resolve the custom module's relative imports
   from the symlinked cache (`FileNotFoundError: …/blobs/tool_declaration_ts.py`). Both fixes are baked
   into those two scripts. (REFERENCE.md → "NVFP4 on sm_120".)

5. **Pull the pinned image, then launch** (foreground; `DETACH=1` = `-d --restart unless-stopped`).
   `QUANT` selects the checkpoint + flags; the container is always `kimi-k26`:
   ```bash
   docker pull lmsysorg/sglang:v0.5.12.post1-cu130   # INT4+SGLang (FULL image; Marlin JIT needs ninja+nvcc)
   docker pull vllm/vllm-openai:v0.22.1              # INT4+vLLM   (NVFP4+vLLM uses the locally-built image)

   QUANT=int4  bash scripts/serve_docker_sglang.sh   # INT4 on SGLang (run the pre-launch gates first — REFERENCE.md)
   QUANT=int4  bash scripts/serve_docker_vllm.sh     # INT4 on vLLM
   QUANT=nvfp4 IMAGE=kimi-k26-nvfp4-vllm:cu130-mla bash scripts/serve_docker_vllm.sh   # NVFP4 on vLLM
   ```
   Container: CDI GPUs, `--ipc=host --network host` (host-net required for NCCL transport / IB-RoCE
   RDMA; server binds `0.0.0.0`, Caddy upstreams over loopback → see REFERENCE "Access model"), weights `:ro`, memlock/nofile ulimits,
   `HF_HUB_OFFLINE=1`. Load ~10–15 min from NVMe (~4–5 min warm cache); ready on "The server is fired up
   and ready to roll!" (SGLang) / "Application startup complete" (vLLM) — `docker logs -f kimi-k26`.

6. **Verify** — health, models, text, tool-call, and vision (sent as a base64 data URL):
   ```bash
   bash scripts/verify.sh
   bash scripts/assert-native.sh kimi-k26   # NVFP4: confirm the MoE backend (NATIVE FP4 vs MARLIN fallback)
   ```
   Vision debug (dumps content + reasoning_content for a red PNG): `python3 scripts/vision-probe.py --model kimi-k2.6`.
   Optional throughput check: use the **`llm-inference-benchmark`** skill — the canonical
   `bench_sweep.sh`, the sweep methodology, and this hardware's recorded baselines all live there.

7. **Productionize** — one static **`kimi-k26.service`** driven by **`/etc/kimi-k26.env`** (selects
   `FRAMEWORK`/`QUANT`/`IMAGE`). Only one 595 GB variant fits the 8-GPU pool, so the service name never
   changes — **switch quant/engine by editing the env file + `sudo systemctl restart kimi-k26`** (no
   disable/enable). Use the unit **or** `DETACH=1`'s restart policy, never both. The launcher goes on the
   **root disk** (`/usr/local/bin`) so the service never depends on a `/data` mount being present at boot.
   ```bash
   sudo install -m755 scripts/serve_docker_vllm.sh scripts/serve_docker_sglang.sh /usr/local/bin/  # launcher (root disk)
   sudo mkdir -p /var/lib/kimi-k26                          # service state dir (WorkingDirectory)
   sudo cp scripts/kimi-k26.env.example /etc/kimi-k26.env   # EDIT: FRAMEWORK, QUANT, IMAGE, HF_HOME (BARE values!)
   sudo cp scripts/kimi-k26.service /etc/systemd/system/kimi-k26.service
   sudo systemctl daemon-reload && sudo systemctl enable --now kimi-k26   # journalctl -u kimi-k26 -f
   ```
   ⚠ **Keep `/etc/kimi-k26.env` values bare** — systemd `EnvironmentFile` folds an inline `# comment`
   into the value (mangles `HF_HOME` → `LocalEntryNotFoundError`). fp8 KV: add `KV_CACHE_DTYPE` (vLLM
   `fp8`, SGLang `fp8_e4m3`) — verified, ~2× KV pool.
   TLS + Bearer-API-key reverse proxy (engine-agnostic): `scripts/setup_proxy.sh`. Access model: the
   `--network host` server binds **`0.0.0.0`**, so raw `:30000` answers unauthenticated on loopback/
   LAN/tailnet — the auth boundary is **Caddy `:443`** (off-box clients) + the router (no public IP),
   not the bind. **Caddy upstreams over loopback (`127.0.0.1`), never the LAN IP** — a LAN-IP upstream
   is a DHCP time-bomb (lease moves → Caddy 502s with an empty body; cost us two outages). **No host
   firewall** (setup_proxy retires any legacy `kimi-fw`/`kimi-netguard`). The Caddyfile sets `admin
   off`, so apply proxy changes with `sudo systemctl restart caddy`, not `reload`. See REFERENCE.md
   "Access model".

## Key facts (don't relearn these the hard way)
- **`--ipc=host` is non-negotiable** for TP=8: NCCL needs shared memory and Docker's default 64 MB
  `/dev/shm` breaks it. NCCL "unhandled system error"/SIGBUS right after the load ⇒ check this first.
- **INT4** auto-detects (compressed-tensors → Marlin MoE) — no `--quantization` flag.
- **NVFP4 is vLLM-only on sm_120** and needs `--quantization modelopt_fp4` + the patched CUDA-13 image
  (`build_nvfp4_image.sh`): native FP4 (`--moe-backend flashinfer_b12x`) requires **CUDA 13** ("b12x
  fused MoE requires CUDA 13") *and* the TRITON_MLA `num_stages` smem patch (else graph-capture OOM
  `102400 > 101376`). It genuinely dispatches the FP4 GEMM (no silent dequant) but measured **~12%
  slower than Marlin** on this PCIe-comm-bound box, so `--moe-backend marlin` is the throughput pick.
  **SGLang NVFP4 = NaN on sm_120** — don't. Offline load also needs `prep_remote_code.sh` or it dies
  with `FileNotFoundError …/blobs/tool_declaration_ts.py` (transformers ≥5.10 + symlinked cache).
- Tool calls: SGLang needs only `--tool-call-parser kimi_k2`; vLLM needs **both**
  `--tool-call-parser kimi_k2` **and** `--enable-auto-tool-choice` (missing ⇒ no `tool_calls`).
- **The memory knobs are NOT equivalent across engines** (measured): SGLang's
  `--mem-fraction-static` = weights+KV pool with transients *outside* it — 0.85 is the verified
  ceiling here, **0.90 OOM-crashes the server** (vision tower and big-batch transients allocate
  outside the pool). vLLM's `--gpu-memory-utilization` caps the *total* footprint — 0.85 leaves
  ~0.5 GB for KV (won't start); 0.95 is the working setting, and 256K context needs fp8 KV.
  FP8 KV (`KV_CACHE_DTYPE` env in both scripts) doubles the KV pool at zero throughput cost.
- Kimi-K2.6 is a **thinking model** (reasoning by default) → answer in `reasoning_content`/`content`;
  disable per request with `chat_template_kwargs:{"thinking":false}`.
- **Vision**: send images as **base64 data URLs**. Server-side `image_url` URL-fetch gets 403 from
  UA-filtering hosts (e.g. Wikimedia) — fixture issue, not a MoonViT failure. vLLM additionally wants
  `--mm-encoder-tp-mode data` (SGLang needs nothing extra). Debug an empty vision reply with
  `scripts/vision-probe.py` — it shows whether the answer landed in `reasoning_content` (a `<think>`-block
  artifact, fixed with more `max_tokens`) vs a real MoonViT failure.
- MoE weight load is CPU-bound and slow (~10–15 min); high CPU + 0% GPU + quiet logs = *normal loading*.
- `no kernel image is available` on sm_120 ⇒ the image predates Blackwell support — bump the tag.
- **Cutover: wait for the GPUs to actually free before relaunching.** When swapping variants/engines (or
  off an ad-hoc deployment), a ~595 GB / 8-GPU teardown takes 30–60 s; starting too soon OOMs the workers
  at *executor init* (`Engine core initialization failed`, before weight load) and a failed init can
  **leak GPU memory** that turns into a crash-loop. The serve scripts now wait (`WAIT_GPU_FREE`); if a
  loop already leaked, `nvidia-smi --query-compute-apps`, `kill -9` the orphan, confirm GPUs → 0, restart.
  To preserve the client contract across a migration, keep `MODEL_NAME` stable (it's the OpenAI `model` id).
- **Caddy proxy: loopback upstream + `restart`, never `reload`.** `setup_proxy.sh` points Caddy at
  `127.0.0.1:30000`, not the LAN IP — the engine binds `0.0.0.0` so loopback works, and it survives
  DHCP LAN-IP changes. A LAN-IP upstream is a silent **502-empty-body** time-bomb when the host's lease
  moves (`localhost:30000` keeps working, so it looks like the engine is fine). And the Caddyfile's
  `admin off` disables the `:2019` admin API, so `systemctl reload caddy` fails (`dial :2019: connection
  refused`) — apply Caddyfile/cert/key changes with **`sudo systemctl restart caddy`**.

## When startup crashes or hangs
See **[REFERENCE.md](REFERENCE.md)**: per-engine Docker paths (image pinning, CDI, NCCL/shm, the
SGLang pre-launch gates, the SGLang↔vLLM flag map, py-spy load-vs-hang diagnosis),
checkpoint-download gotchas, KV-cache/256K tuning, and productionization (systemd vs restart
policy, proxy, monitoring).
