---
name: restart-qwen-mtp
description: Start, restart, or verify the production Qwen 3.6 35B-A3B MTP systemd service, including all-FlashHead, draft-only FlashHead, and dense F16-KV variants on port 8001.
metadata:
  hermes:
    tags: [llama-cpp, systemd, mtp, qwen, flashhead, gfx1151, rocm]
---

# Start or restart Qwen MTP / FlashHead

Qwen is a **systemd service**, not a standalone background process:

```text
service  qwen-mtp.service
port     8001
alias    qwen3.6-35b-q4
unit     /etc/systemd/system/qwen-mtp.service
logs     /tmp/qwen35-server.log and journalctl -u qwen-mtp.service
```

Never start another `llama-server` on port 8001 while systemd owns the service.

## Select and restart a variant

The helper selects the requested variant, writes the final systemd drop-in, restarts the service, waits for health, and verifies the live executable, GGUF, self-contained HIP library, F16 KV, model alias, denied environment variables, and performance power profile:

```bash
HELPER=/home/chihmin/.pi/agent/skills/restart-qwen-mtp/scripts/restart-qwen-mtp.sh

$HELPER                  # all-FlashHead, the default (draft + approximate target)
$HELPER flashhead        # explicit all-FlashHead
$HELPER draft-flashhead  # FlashHead draft, dense target verifier
$HELPER f16-baseline     # dense draft and target LM heads, F16 target/draft KV
$HELPER --help
$HELPER --print-config f16-baseline  # inspect without changing systemd
```

Aliases: `all-flashhead`/`all` select `flashhead`; `partial`/`draft` select `draft-flashhead`; `f16`/`baseline`/`dense` select `f16-baseline`. With no argument the helper always selects all-FlashHead.

For a stopped service whose effective configuration is already correct and must not be re-selected:

```bash
sudo powerprofilesctl set performance
sudo systemctl daemon-reload
sudo systemctl start qwen-mtp.service
```

Then perform all verification steps below.

## Current verified FlashHead deployment

Draft + target FlashHead was verified at source commit `15bd9b0028` and deployed immutably at:

```text
/home/chihmin/llama-mtp-deploy/gfx1151-all-flashhead-15bd9b0028/
```

Target retrieval is approximate and explicitly activated by `LLAMA_FLASHHEAD_TARGET=1`. Use `draft-flashhead` to keep exact dense target verification with the same binary.

Required components:

```text
binary  /home/chihmin/llama-mtp-deploy/gfx1151-all-flashhead-15bd9b0028/bin/llama-server
HIP     /home/chihmin/llama-mtp-deploy/gfx1151-all-flashhead-15bd9b0028/bin/libggml-hip.so.0.11.1
GGUF    /home/chihmin/models/Qwen3.6-35B-A3B-selective-Q4_0-proof/
          Qwen3.6-35B-A3B-UD-Q4_K_M-selective-Q4_0-flashhead.gguf
probes  LLAMA_FLASHHEAD_PROBES=256
target  LLAMA_FLASHHEAD_TARGET=1 (all-FlashHead only)
KV      F16 target and draft KV
batch   -b 4096 -ub 2048
context -c 260000 -np 1
```

Do not point production directly at the mutable `llama-mtp-opt/build/bin` worktree. Do not mix the FlashHead GGUF with an older deployed binary: unsupported extra tensors can be ignored and silently run the dense head. GPU Top-K and I32 CONCAT live in the matching `libggml-hip.so`, so that library must come from the same deployment directory as the executable.

## Managed variant systemd drop-in

The selector manages:

```text
/etc/systemd/system/qwen-mtp.service.d/zz-flashhead.conf
```

Despite the historical filename, this one file can contain either the FlashHead or dense F16-baseline `ExecStart`. The helper backs up changed content before overwriting it. The `zz-` prefix is required because the file must sort after `selective-q4-proof.conf`; otherwise that drop-in's dense `ExecStart` wins silently.

Current known-good FlashHead content:

```ini
# Draft + target FlashHead, verified commit 15bd9b0028.
[Service]
Environment=LLAMA_FLASHHEAD_PROBES=256
Environment=LLAMA_FLASHHEAD_TARGET=1
Environment=LD_LIBRARY_PATH=/home/chihmin/llama-mtp-deploy/gfx1151-all-flashhead-15bd9b0028/bin:/opt/rocm-7.2.2/lib
ExecStart=
ExecStart=/home/chihmin/llama-mtp-deploy/gfx1151-all-flashhead-15bd9b0028/bin/llama-server -m /home/chihmin/models/Qwen3.6-35B-A3B-selective-Q4_0-proof/Qwen3.6-35B-A3B-UD-Q4_K_M-selective-Q4_0-flashhead.gguf --port 8001 --host 0.0.0.0 -ngl 99 -fit off -fa 1 -c 260000 -np 1 -b 4096 -ub 2048 --mmproj /home/chihmin/models/mmproj.gguf --alias qwen3.6-35b-q4 --spec-type mtp --spec-draft-n-max 3 --log-file /tmp/qwen35-server.log
```

Before changing this root-owned file, preserve rollback:

```bash
stamp=$(date +%Y%m%d-%H%M%S)
sudo cp /etc/systemd/system/qwen-mtp.service.d/zz-flashhead.conf \
  /etc/systemd/system/qwen-mtp.service.d/zz-flashhead.conf.bak-$stamp
```

After an approved change:

```bash
sudo powerprofilesctl set performance
sudo systemctl daemon-reload
sudo systemctl restart qwen-mtp.service
```

Do not alter `optimized.conf` or `selective-q4-proof.conf` when enabling FlashHead; the final drop-in is intentionally removable.

## Mandatory verification

Wait up to five minutes for model loading:

```bash
for i in $(seq 1 300); do
  curl -fsS --max-time 2 http://127.0.0.1:8001/health && break
  systemctl is-active --quiet qwen-mtp.service || break
  sleep 1
done
```

Verify effective systemd configuration and live mappings, not just filenames in the drop-in:

```bash
systemctl show qwen-mtp.service -p MainPID -p ExecStart -p Environment -p DropInPaths
pid=$(systemctl show -p MainPID --value qwen-mtp.service)
readlink -f /proc/$pid/exe
grep -m1 'libggml-hip' /proc/$pid/maps
curl -fsS http://127.0.0.1:8001/v1/models | jq '.data[0] | {id, context: .meta.n_ctx}'
```

The executable and `libggml-hip` mapping must both resolve under:

```text
/home/chihmin/llama-mtp-deploy/gfx1151-all-flashhead-15bd9b0028/bin/
```

The cheap proof that FlashHead tables engaged is mandatory:

```bash
grep 'FlashHead tables found' /tmp/qwen35-server.log | tail -1
# load_arch_tensors: FlashHead tables found - 7760 clusters of 32, 4096 static tokens
```

Confirm F16 KV and prohibited environment variables:

```bash
grep 'llama_kv_cache: size' /tmp/qwen35-server.log | tail -2
tr '\0' '\n' </proc/$pid/environ | \
  grep -E '^(LLAMA_FLASHHEAD_PROBES|LLAMA_FLASHHEAD_TARGET|LD_LIBRARY_PATH|GPU_MAX_HW_QUEUES|ROCP_TOOL_ATTACH)=' || true
```

Expected:

- `LLAMA_FLASHHEAD_PROBES=256` is present.
- `LLAMA_FLASHHEAD_TARGET=1` is present for all-FlashHead and absent for draft-only/baseline.
- The startup journal warns `approximate target-side FlashHead is enabled` for all-FlashHead.
- `LD_LIBRARY_PATH` begins with the immutable deployment's `bin/`.
- KV lines report `K (f16)` and `V (f16)`.
- `GPU_MAX_HW_QUEUES` and `ROCP_TOOL_ATTACH` are absent.
- `powerprofilesctl get` reports `performance`.

Run a short non-streaming inference and inspect new log lines. Health alone proves model load, not execution:

```bash
curl -fsS http://127.0.0.1:8001/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3.6-35b-q4","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":32,"temperature":0,"seed":42,"stream":false}' | jq '{usage, finish_reason: .choices[0].finish_reason}'

grep -Ei 'unknown op|fallback|error|assert' /tmp/qwen35-server.log | tail -20
```

No unknown-op, CPU-fallback, assertion, or server error should appear. Finally report Qwen/Gemma/display-manager states, KFD PIDs, and the power profile.

## Creating a future immutable FlashHead deployment

Only do this for a newly verified commit. Copy the exact executable and SONAME targets used by that build into a new commit-named directory, recreate the `.so.0` symlinks, and change every copied ELF RUNPATH to:

```text
$ORIGIN:/opt/rocm-7.2.2/lib
```

Then verify with an empty external library path:

```bash
env -u LD_LIBRARY_PATH ldd /path/to/new-deploy/bin/llama-server | grep -E 'lib(llama|mtmd|ggml)'
readelf -d /path/to/new-deploy/bin/llama-server | grep RUNPATH
```

Every llama/mtmd/ggml library must resolve inside the new deployment. Record source commit and source hashes in a manifest before changing the systemd drop-in. Never copy an entire stale build directory containing old versioned libraries.

## Select the dense F16-KV baseline

Use the selector rather than manually moving drop-ins:

```bash
/home/chihmin/.pi/agent/skills/restart-qwen-mtp/scripts/restart-qwen-mtp.sh f16-baseline
```

This chooses the dense selective-Q4 GGUF while deliberately keeping the same self-contained `gfx1151-all-flashhead-15bd9b0028` executable and HIP libraries. Only the GGUF and FlashHead environment change, preserving a controlled baseline along with `-b 4096 -ub 2048`, 260K context, one slot, MTP draft length 3, and F16 target/draft KV. Verification fails if the new process inherits either FlashHead environment variable or logs table activation.

To return to the default:

```bash
/home/chihmin/.pi/agent/skills/restart-qwen-mtp/scripts/restart-qwen-mtp.sh flashhead
```

## Guardrails

- Never set `GPU_MAX_HW_QUEUES=1` or `ROCP_TOOL_ATTACH` in production.
- Never start a standalone server on port 8001 while systemd owns Qwen.
- Preserve `-b 4096 -ub 2048`, F16 KV, 260K context, and one slot unless explicitly benchmarking another policy.
- Target FlashHead is approximate; use `draft-flashhead` whenever exact target-distribution behavior is required.
- Do not infer activation from the GGUF filename alone; require the load log, live executable, and live HIP mapping.
- Starting/restarting Qwen does not require starting Gemma or the display manager.
