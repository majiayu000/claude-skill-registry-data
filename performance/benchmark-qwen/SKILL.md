---
name: benchmark-qwen
description: Benchmark the production Qwen 3.6 35B-A3B MTP llama.cpp service and real Pi Agent latency. Measures cold-KV prefill TPS, Pi wall time, merge-sort decode TPS, MTP acceptance, exact-token HTTP workloads, and interleaved old/new A/B comparisons. Use when the user asks to benchmark Qwen, measure Pi Agent speed, output/decode TPS, prefill TPS, TTFT, kernel-launch impact, or quantify an optimization.
metadata:
  hermes:
    tags: [benchmark, qwen, llama-cpp, pi-agent, mtp, rocm, gfx1151]
---

# Benchmark Qwen

Benchmark the local Qwen MTP stack without confusing server compute time, streamed client time, complete Pi wall time, model loading, prompt cache, or stochastic output.

## Quick commands for the currently deployed service

Real Pi Agent sustained decode workload:

```bash
/home/chihmin/.pi/agent/skills/benchmark-qwen/scripts/benchmark-pi-agent.sh decode 3
```

The helper writes evidence under `/tmp/benchmark-qwen-<mode>-<timestamp>/` and prints `summary.json`. It:

1. records the effective Qwen executable and initial Qwen/Gemma state;
2. sets `performance` power profile;
3. stops Gemma to isolate ROCm;
4. restarts Qwen before every sample, waits for `/health`, then requires ten consecutive idle GPU samples;
5. times the complete `pi` process and captures Pi JSONL plus the corresponding server log;
6. parses exactly one server timing block;
7. reports all runs plus mean/median;
8. restores Qwen/Gemma and verifies ports 8001/8002 and the `performance` profile.

Use this helper only for the executable already configured in `qwen-mtp.service`. For old/new executable A/B, follow the isolated-variant procedure below.

# 1. Timing surfaces and metric definitions

Keep these surfaces separate in every report.

## 1.1 Server prefill TPS — authoritative model prefill metric

Parse llama-server's request timing:

```text
prompt eval time = 29886.10 ms / 28219 tokens (... 944.22 tokens per second)
```

Definitions:

```text
server prefill TPS = prompt_tokens / (prompt_eval_ms / 1000)
server prefill time = prompt_eval_ms
```

Use this for kernel/model prefill comparisons. Require equal `prompt_tokens` across variants. TTFT is not pure prefill time: it also contains request handling, first-token sampling, streaming, and client overhead.

## 1.2 Server decode TPS — authoritative server decode interval

Example:

```text
       eval time = 19449.49 ms / 1186 tokens (... 60.98 tokens per second)
```

Report both:

```text
llama-server TPS = N / eval_seconds
(N-1) estimate   = (N - 1) / eval_seconds
```

For the example:

```text
server TPS = 1186 / 19.44949 = 60.98
(N-1) TPS  = 1185 / 19.44949 = 60.93
```

The server value is the primary decode metric used in this project. The `(N-1)` value is only a standards-style estimate because llama-server's interval is not literally the timestamp from first streamed token to last streamed token.

## 1.3 Strict streamed decode throughput

For a direct streaming HTTP request, record timestamps for first and last non-empty content/reasoning token:

```text
strict streamed TPS = (N - 1) / (last_token_time - first_token_time)
TTFT                = first_token_time - request_start
HTTP elapsed        = response_end - request_start
```

The existing static-20K lab scripts also expose `completion_tokens / (response_end - first_token_time)` as `external_decode_tps`. Treat that as an external throughput indicator, not strict inter-token TPS and not a replacement for server TPS.

## 1.4 Whole Pi Agent wall time

Use `/usr/bin/time` around the complete process:

```bash
/usr/bin/time -f '%e' -o run.wall \
  pi --offline --provider local-llama --model qwen3.6-35b-q4 \
     --no-session --mode json -p "$PROMPT" \
  >run.jsonl 2>run.stderr
```

Pi wall time includes Pi startup, system prompt/tool/skill serialization, HTTP/JSON, prefill, sampling, decode, and response handling. It excludes model loading when the benchmark waits for server health before starting the timer.

Never label server TPS as Pi wall time or infer a Pi speedup from a direct HTTP test alone.

## 1.5 MTP acceptance and output length

Always parse and report:

```text
draft acceptance rate
accepted draft tokens / generated draft tokens
completion/output token count
finish_reason
```

Decode TPS is not directly comparable when one response is much shorter, takes a different reasoning path, invokes tools, or has materially different MTP acceptance. Prefer deterministic direct HTTP for kernel A/B and use Pi as the final end-to-end gate.

# 2. Real Pi Agent end-to-end procedure

## 2.1 Controlled workloads

### Decode mode (Primary Sustained Workload)

Prompt:

```text
Do not use any tools. Write a correct stable merge sort implementation in Python. Include type hints, a docstring, a short explanation of the algorithm and its time and space complexity, and five assert-based tests. Return one self-contained answer.
```

This generates sufficient output tokens to accurately measure sustained decode throughput. Generated code must be extracted and executed; fast invalid code is a failed sample.

This mode runs:

```bash
pi --offline \
  --provider local-llama \
  --model qwen3.6-35b-q4 \
  --no-session \
  --mode json \
  -p '<controlled prompt>'
```

`--no-session` clears Pi conversation state. It does **not** clear llama-server KV/prompt cache. Restart the server before every cold-KV sample.

## 2.2 Per-sample lifecycle

For each sample:

1. ensure no other GPU workload is running and Gemma is stopped;
2. set `powerprofilesctl set performance`;
3. restart the exact Qwen variant;
4. wait for `/health`;
5. wait for ten consecutive samples with GPU busy 0% and low idle power;
6. remove/truncate the request log before timing;
7. run the complete Pi command under `/usr/bin/time`;
8. save Pi JSONL, Pi stderr, wall time, server log, executable path/hash, Pi version, and launch argv;
9. require exactly one server request/timing block;
10. parse prefill, decode, output tokens, and MTP acceptance;
11. in decode mode, extract and execute the generated Python.

The parser deliberately rejects logs containing zero or multiple request timing blocks:

```bash
python3 /home/chihmin/.pi/agent/skills/benchmark-qwen/scripts/parse_server_log.py SERVER_LOG
```

## 2.3 Extracting the Pi answer

Pi JSON mode does not use a top-level `text` field. Extract text from `message_end`:

```python
import json

text = ""
for line in open("run-1.jsonl"):
    event = json.loads(line)
    if event.get("type") == "message_end":
        for part in event["message"].get("content", []):
            if part.get("type") == "text":
                text += part.get("text", "")
```

Extract the available fenced `python` block and execute it in an isolated temporary file. Do not require two code blocks; a valid self-contained response often has exactly one.

## 2.4 Evaluating Pi A/B

Compare:

- identical Pi prompt token count;
- server prefill time/TPS;
- server decode time/TPS and `(N-1)` estimate;
- output token count and MTP acceptance;
- complete Pi wall time;
- output validity and tool-call count.

Use at least three samples per variant and medians. Pi output is not guaranteed identical, even at temperature zero, when numerical kernels differ. A Pi result is a realistic final workload, not the first exactness gate.

# 3. How the static exact-20,000-token input is made

The static-20K experiment uses direct OpenAI-compatible HTTP so both variants receive exactly 20,000 chat-template prompt tokens. It does not use Pi's changing system prompt.

Current lab implementation:

```text
/tmp/bench_20k_prompt.py          # default 256 output tokens
/tmp/bench_20k_prompt_128.py      # short screening gate
/tmp/bench_20k_prompt_1024.py     # sustained/locked gate
```

Canonical calibrated Qwen prompt currently used by the experiments:

```text
/tmp/bench-20k-prompt-20260724-094754/qwen-prompt.txt
```

Do not trust the filename alone; verify `usage.prompt_tokens == 20000` on every run.

## 3.1 Calibration algorithm

1. Concatenate varied technical prose from local llama.cpp documentation.
2. Repeat it until it contains more than 20K content tokens.
3. Call `/tokenize` with `add_special=false`.
4. Start with approximately 19,970 content tokens.
5. Call `/detokenize` on that token prefix to obtain stable text.
6. Send it through `/v1/chat/completions` with `max_tokens=1`, `temperature=0`, and `cache_prompt=false`.
7. Read `usage.prompt_tokens`, which includes the model's chat template.
8. Correct the content-token prefix by `n += 20000 - actual_prompt_tokens` and retry.
9. Save the text only after the API reports exactly 20,000 prompt tokens.

Representative command:

```bash
python3 /tmp/bench_20k_prompt.py calibrate \
  8101 qwen3.6-35b-q4 /tmp/qwen-prompt-20000.txt
```

The saved artifact is text, not an assumed 20K token-id array. Therefore tokenizer/model/chat-template changes require recalibration.

## 3.2 Static benchmark request

The benchmark sends:

```json
{
  "model": "qwen3.6-35b-q4",
  "messages": [{"role": "user", "content": "<calibrated text>"}],
  "max_tokens": 128,
  "temperature": 0,
  "seed": 42,
  "cache_prompt": false,
  "stream": true,
  "stream_options": {"include_usage": true}
}
```

Use 128 output tokens for fast screening and 1,024 for sustained final validation. For the locked 1,024-token test, require:

```text
usage.prompt_tokens == 20000
usage.completion_tokens == 1024
finish_reason == length
```

> [!NOTE]
> **Prompt Cache Policy:**
> - When evaluating **Cold-KV Prefill + Decode**: Use `cache_prompt=false` with cold server restarts between samples.
> - When evaluating **Pure Decode Performance**: Enable `cache_prompt=true` (or warm up the prompt cache). This completely bypasses the prefill phase while preserving the full 20,000-token KV cache memory footprint across all decode steps.

## 3.3 Static experiment metrics

Record all of:

- API usage prompt/completion tokens and finish reason;
- server prefill ms/TPS;
- server decode ms/TPS;
- `(N-1)` decode estimate;
- streamed TTFT and total HTTP elapsed;
- MTP accepted/generated tokens and acceptance rate;
- sampled GPU busy, package power, and server CPU usage;
- executable, model hash/path, complete argv, environment overrides, and evidence directory.

The first streamed content timestamp divides approximate prefill and decode power samples, but it is not an invocation-accurate GPU boundary. Use rocprof traces for kernel attribution.

# 4. A/B against a previous commit or deployed version

## 4.1 Prefer immutable artifacts when available

If the previous version already exists under `/home/chihmin/llama-mtp-deploy/<name>/`, use that exact binary. Record:

```bash
readlink -f /path/to/llama-server
sha256sum /path/to/llama-server
/path/to/llama-server --version
cat /path/to/VERSION.txt 2>/dev/null || true
```

This is more reproducible than rebuilding an old commit with today's compiler or dependencies.

## 4.2 Build a previous commit without touching the dirty research tree

Never `git checkout` the active `/home/chihmin/llama-mtp-opt` worktree. It intentionally contains uncommitted research. Create a detached worktree:

```bash
REPO=/home/chihmin/llama-mtp-opt
OLD_COMMIT=<full-commit-sha>
OLD_SRC=/tmp/llama-qwen-ab-${OLD_COMMIT:0:12}

git -C "$REPO" worktree add --detach "$OLD_SRC" "$OLD_COMMIT"
cmake -S "$OLD_SRC" -B "$OLD_SRC/build" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS=gfx1151 \
  -DGGML_HIP_GRAPHS=ON \
  -DGGML_HIP_NO_VMM=ON \
  -DGGML_BUILD_TESTS=OFF \
  -DLLAMA_BUILD_TESTS=OFF \
  -DLLAMA_BUILD_EXAMPLES=OFF \
  -DLLAMA_BUILD_SERVER=ON
cmake --build "$OLD_SRC/build" -j "$(nproc)" --target llama-server
```

Record the old compiler/ROCm/CMake configuration and binary hash. If the old commit does not support the same model, MTP mode, or common argv, it is not a valid direct A/B.

For an uncommitted candidate, build from the active research worktree but identify it as:

```text
base commit + git diff hash + binary SHA256
```

Save `git diff --binary` or at least `git diff`, `git status --short`, `git rev-parse HEAD`, CMakeCache, and the resulting binary hash in the evidence directory.

## 4.3 Recommended isolated server A/B

Do not replace production binaries. Stop production Qwen/Gemma and manually launch one variant at a time on the same isolated port with identical argv:

```bash
MODEL=/home/chihmin/models/Qwen3.6-35B-A3B-selective-Q4_0-proof/Qwen3.6-35B-A3B-UD-Q4_K_M-selective-Q4_0.gguf
COMMON_ARGS=(
  -m "$MODEL" --port 8101 --host 127.0.0.1
  -ngl 99 -fit off -fa 1 -c 260000 -np 1
  -b 4096 -ub 2048
  --mmproj /home/chihmin/models/mmproj.gguf
  --alias qwen3.6-35b-q4
  --spec-type mtp --spec-draft-n-max 3
)

sudo -n powerprofilesctl set performance
sudo -n systemctl stop qwen-mtp.service gemma-mtp.service
"$VARIANT_BIN" "${COMMON_ARGS[@]}" --log-file "$RUN_LOG" &
SERVER_PID=$!
```

Wait for `/health`, then ten consecutive idle samples, run exactly one request, stop the process, and start the next variant. Use a trap that restores the original Qwen/Gemma states and verifies both health endpoints.

Start a fresh process for every cold sample. Recommended six-run interleaving:

```text
old1 → new1 → new2 → old2 → old3 → new3
```

Do not run `old1 old2 old3 new1 new2 new3`; that confounds variant with thermal/time drift. Do not run old and new simultaneously on this UMA GPU.

For direct static-20K A/B, reuse the same calibrated prompt and verify 20,000 tokens in every response. For Pi A/B, manually serve each variant on port 8001 because the local Pi provider points there, then run the exact same Pi command. The request timer starts only after model load, health, and idle stabilization.

A temporary later-sorting systemd drop-in is an alternative when manual port 8001 launch is impractical, but only if the original effective `ExecStart` and rollback path are captured first. Never edit/delete `optimized.conf` during a benchmark.

## 4.4 What must stay identical

Between old and new:

- model and mmproj files, verified by path/hash;
- server argv, context, `-np`, `-b`, `-ub`, FA, MTP draft depth, host/port/alias;
- environment variables except the single experimental switch being tested;
- ROCm libraries and power profile;
- prompt/chat template, temperature, seed, max tokens, cache state;
- Pi binary/version, provider, model, skill inventory, and controlled prompt for Pi tests;
- isolation and idle criteria.

When testing one environment-gated optimization in the same binary, baseline means the variable is absent, not set to `0`, unless the code explicitly parses `0` as false.

## 4.5 Exactness before performance

For kernel changes, first run deterministic baseline/candidate requests with:

```text
temperature=0
seed=42
cache_prompt=false
identical 20K prompt
complete response text/token sequence captured
per-token top-5 logprobs captured when supported
```

Require complete message/token and top-5-logprob equality for an exact candidate. Identical final text alone is insufficient.

If bit-exact match cannot be achieved due to accumulation/rounding differences in quantized or tiled kernels:
- Perform output tensor / logit / hidden state A/B evaluation.
- Require kernel output A/B **Cosine Similarity $\ge 0.99$** to pass the numerical correctness gate.

Only after this correctness gate passes should 20K/128 screening be run; only a winning short gate proceeds to three 20K/1024 samples and Pi Agent.

## 4.6 Summary statistics

Report every run, then mean and median. Use median as the primary comparison:

```text
relative change (%) = 100 * (candidate_median / baseline_median - 1)
```

Do not compare the best old run to the best new run. Also report prompt/output token counts and MTP acceptance beside TPS so different work is visible.

# 5. Validation and rejection rules

Reject or rerun a sample when:

- prompt token count differs between variants;
- static exact-20K usage is not exactly 20,000;
- the server log contains more than one request;
- the server was not restarted for a cold-cache claim;
- Gemma or another GPU workload was active during an isolation claim;
- power profile, DPM state, argv, model, or environment differs unexpectedly;
- output has fewer than two tokens for decode TPS;
- the locked test does not finish by `max_tokens` with the expected output count;
- a Pi run invokes a tool or performs a follow-up request;
- output lengths or MTP acceptance differ substantially and raw TPS is used as proof of a kernel regression/speedup;
- an exact candidate changes any required token/logprob;
- production services or profile are not restored and verified.

# 6. Reporting template

Always report:

- baseline and candidate commit/artifact, binary SHA256, and executable path;
- compiler/ROCm/build configuration for rebuilt commits;
- model/mmproj path and hash plus complete launch argv;
- prompt category/text artifact and actual prompt token count;
- temperature, seed, max tokens, cache state, and restart policy;
- run order and number of samples;
- every result plus mean and median;
- server prefill ms/TPS;
- server TPS and `(N-1)` decode estimate;
- streamed TTFT/elapsed when available;
- MTP acceptance and output-token count/finish reason;
- complete Pi wall time and generated-output validation for Pi tests;
- isolation, idle criterion, power profile, and restoration status;
- evidence directory and caveats.

# 7. Guardrails

- Never set `GPU_MAX_HW_QUEUES=1`.
- Never set `ROCP_TOOL_ATTACH` in production.
- Do not benchmark two active ROCm model runtimes when claiming isolation.
- Do not modify the dirty research worktree to obtain an old commit; use a detached worktree.
- Do not confuse `--no-session` with a cold llama-server cache.
- Do not claim decode improvement from a prefill-only patch.
- Do not infer kernel-launch reduction from TPS; capture launch counts with an invocation-attributed trace.
- Do not include model-load time unless explicitly measuring cold service startup.
- Do not deploy, commit, push, or permanently alter systemd/model/DPM as part of benchmarking without approval.
- Keep Qwen and Gemma active and healthy after the benchmark, with power profile `performance`.
