---
name: local-llm-deployment
description: Choose, size, run and secure open-weight LLMs on local or self-hosted machines with Ollama (0.40.x) and llama.cpp (llama-server, GGUF, llama-quantize) - hardware and memory sizing, quantization choice, context length and KV cache, OpenAI-compatible endpoints, parallelism, Modelfile import, Hugging Face GGUF models, network exposure and authentication, model provenance and licence checks, and troubleshooting slow or out-of-memory runs. Use when the user wants to run a model locally, expose a local inference endpoint to tools or apps, pick a GGUF quantization, convert or quantize a model, or debug performance. Not for measuring model quality (llm-evaluation), hosted APIs, training or fine-tuning, GPU cluster serving (kubernetes-manifests, docker-development for container packaging), or generic Linux setup (linux-cli).
compatibility: macOS, Linux, Windows. Verified against Ollama docs on main and a local Ollama 0.40.3 install (read-only commands), and llama.cpp server/quantize docs on master as of 2026-10-15. Flag names change between llama.cpp builds - confirm with `llama-server --help` for the installed build.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "ollama, llama-cpp, gguf, quantization, local-llm, inference, openai-compatible"
  topics: "machine-learning, deployment, self-hosting"
---

# Local LLM Deployment

Local inference trades quality and speed for privacy, cost and control. The constraints are memory (weights plus KV cache), memory bandwidth, and context length; most "it is slow" or "it crashed" problems reduce to those. Decide the model and quantization from the memory budget, then verify with a measurement.

## Scope and boundaries

- This skill: running and serving open-weight models on your own hardware with Ollama or llama.cpp.
- `llm-evaluation`: deciding whether the model is good enough (quality evals, benchmarks via lm-eval). `docker-development`: packaging in containers. `linux-networking` / `linux-hardening`: firewalling and host security. `secrets-management`: keys. `mcp-server-development`: tools that call a local model.

## Non-negotiable rules

1. **Do not expose an inference server beyond localhost without authentication and network controls.** Ollama has no built-in authentication on its API; binding `OLLAMA_HOST=0.0.0.0` publishes it to the network. Put it behind a reverse proxy with auth/TLS or a private network/VPN, or use `llama-server --api-key`. Never port-forward it to the internet.
2. **Verify model provenance and licence before downloading or running.** Prefer official or well-known publishers, check the model card licence and use restrictions (some "open" weights restrict commercial use or require acceptance), and record the source and file hash. Prefer GGUF/safetensors. Never `torch.load` / unpickle weights from untrusted sources (pickle executes code), and do not enable remote-code flags for unreviewed repos.
3. **Ask before large downloads or disk-heavy actions.** State the model, source, and size first (a 70B Q4 file is tens of GB). Do not run `ollama rm`, delete caches, or overwrite models without the user asking.
4. **Do not pipe secrets, customer data or confidential documents into a model or server whose logging, telemetry and retention you have not checked.** Local does not automatically mean private: check where logs, prompts and caches are written, and who can reach the port.
5. **Do not run `curl | sh` installers silently**; prefer the platform package manager or the vendor's documented method, and tell the user what will be installed.
6. **State versions.** Ollama and llama.cpp change flags, defaults and model support quickly; cite the installed version (`ollama --version`, `llama-server --version`) and the docs you used.

## Workflow

### 1. Establish the target
Ask: hardware (RAM/VRAM, GPU vendor, Apple silicon unified memory, CPU only), OS, task (chat, coding, embeddings, long-document), required context length, concurrency (one user or several), latency target, and any licence/privacy constraints.

### 2. Size memory before choosing a model
Rule of thumb for the memory you need:

- **Weights** ~ parameters x bits-per-weight / 8. From the llama.cpp quantize README (Llama-3.1-8B): Q4_K_M 4.89 bits/weight = 4.58 GiB, Q5_K_M 5.70 = 5.33 GiB, Q6_K 6.56 = 6.14 GiB, Q8_0 8.50 = 7.95 GiB, F16 16.0 = 14.96 GiB.
- **KV cache** ~ 2 x layers x kv_heads x head_dim x context_tokens x bytes_per_element, times the number of parallel sequences. Long contexts and many parallel slots can exceed the weights. Models with grouped-query attention have far fewer kv_heads than attention heads, which shrinks this a lot.
- Add compute buffers and OS headroom (budget roughly 1-2 GiB plus the app you also run). For GPU offload, everything that does not fit in VRAM runs on CPU at a large speed penalty.
- Mixture-of-experts models need memory for all experts but compute only the active ones; speed is closer to the active parameter count, memory to the total.

### 3. Pick the quantization
| Type | Typical use |
|---|---|
| F16 / BF16 | Reference quality, conversion intermediate; largest |
| Q8_0 | Near-lossless; use when memory allows |
| Q6_K, Q5_K_M | Strong quality/size balance |
| Q4_K_M | Common default (also the default pick for `-hf` and for Hugging Face repos in Ollama when present) |
| Q3_K_*, Q2_K, IQ* | Squeeze into small memory; expect noticeable quality loss, test on your task. IQ types are "importance" quants and often benefit from an importance matrix |

Smaller quant of a bigger model often beats a larger quant of a smaller model at equal memory, but verify with your own prompts (`llm-evaluation`). The llama.cpp docs name perplexity and KL divergence as the usual accuracy-loss measures; they do not publish a quality table. Quantization names above are from the llama.cpp quantize README.

### 4a. Run with Ollama
Verified against a local Ollama 0.40.3 (`ollama --help`) and the Ollama docs.

```bash
ollama --version
ollama serve                         # starts the server (127.0.0.1:11434 by default); desktop installs run it for you
ollama pull <model>                  # downloads; ask first for large models
ollama run <model> "hello"           # interactive or one-shot
ollama list                          # local models
ollama ps                            # loaded models; PROCESSOR column shows GPU/CPU split
ollama stop <model>                  # unload
ollama show <model> --modelfile      # inspect Modelfile (also --parameters, --template, --license)
```
Server settings are environment variables set before `ollama serve` (or in the service definition). From the Ollama FAQ: `OLLAMA_HOST` (default 127.0.0.1:11434), `OLLAMA_CONTEXT_LENGTH` (default 4096), `OLLAMA_KEEP_ALIVE` (default 5m), `OLLAMA_NUM_PARALLEL` (default 1), `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` (default 512), `OLLAMA_FLASH_ATTENTION`, `OLLAMA_KV_CACHE_TYPE` (`f16` default, `q8_0`, `q4_0`; global). Per request, set context with `"options": {"num_ctx": N}`; in a session `/set parameter num_ctx N`. If answers ignore early parts of a long prompt, check the context length first: the default is small and truncation is silent from the user's view.

HF GGUF models run directly: `ollama run hf.co/<user>/<repo>[:<quant>]`; the quant tag is case-insensitive and Q4_K_M is chosen when present (Hugging Face Ollama integration docs). Private repos need your Ollama public key added to your HF account.

Importing local weights: write a `Modelfile` containing `FROM /path/model.gguf` (or a safetensors directory; split GGUF shards with `model-*.gguf`), then `ollama create my-model -f Modelfile`. Ollama does not quantize GGUF on import; quantize with llama.cpp first. The `ollama create --quantize` flag applies to safetensors imports (the help text's example is `nvfp4`). Modelfile instructions per docs: `FROM`, `PARAMETER`, `TEMPLATE`, `SYSTEM`, `LICENSE`, `MESSAGE`, `REQUIRES`, `CAPABILITY`. Defaults listed there include `num_ctx` 2048, `temperature` 0.8, `top_k` 40, `top_p` 0.9 (these model-level defaults can differ from the server-level `OLLAMA_CONTEXT_LENGTH`; set the context explicitly).

### 4b. Run with llama.cpp (llama-server)
The binary is `llama-server` (the old `./server` name is gone). Check `llama-server --help` for your build; the flags below are from the server README on master:

```bash
llama-server -m ./model-Q4_K_M.gguf -c 8192 -ngl all --host 127.0.0.1 --port 8081 --api-key "$LLAMA_API_KEY"
# or fetch from the Hub (downloads; ask first):
llama-server -hf <user>/<repo>:Q4_K_M -c 8192 --host 127.0.0.1 --port 8081
```
Key flags: `-m/--model`, `-hf/--hf-repo <user>/<model>[:quant]`, `-c/--ctx-size` (0 = from model), `-ngl/--gpu-layers` (number, `auto`, or `all`), `-np/--parallel` (slots), `-ctk/-ctv` (KV cache type), `-fa/--flash-attn on|off|auto`, `--jinja` / `--no-jinja` (Jinja chat template engine, required for tool calling; enabled by default on current master per the server README, but older builds need `--jinja` passed explicitly, so pass it when targeting tool use), `--host`, `--port`, `--api-key` (also env `LLAMA_API_KEY`), `-t/--threads`, `--metrics`, `--embedding`. Note two drift risks seen while verifying: the master README lists the default port as 9931 (older builds used 8080, and Docker examples still use 8080), and memory locking is documented via `-lm/--load-mode` rather than `--mlock`. **Always pass `--host` and `--port` explicitly** and confirm other flags against your build's `--help`. With `-c` and `-np`, the context is shared across slots, so per-conversation context shrinks as parallelism grows.

Health and endpoints: `GET /health` (503 while loading, 200 ready); OpenAI-style `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings` (needs a pooling type), `/v1/models`, `/v1/responses`.

Convert and quantize your own model (only from sources you trust):
```bash
python convert_hf_to_gguf.py <local_hf_dir> --outfile model-bf16.gguf --outtype bf16
llama-quantize model-bf16.gguf model-Q4_K_M.gguf Q4_K_M       # optional: --imatrix imatrix.dat
```
Options from the README: `--imatrix`, `--allow-requantize` (quality loss when requantizing; avoid), `--leave-output-tensor`, `--pure`, `--tensor-type`. Re-quantizing an already-quantized file compounds loss: quantize from the highest-precision source.

### 5. Use the API
Ollama exposes its native API (`/api/generate`, `/api/chat`, `/api/embed`, `/api/tags`, `/api/ps`; `/api/embeddings` is deprecated in favour of `/api/embed`) and an OpenAI-compatible API at `http://localhost:11434/v1/` (`/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models`, `/v1/responses` stateless). The local server ignores the API key value but clients need one. Documented gaps include `tool_choice`, `logit_bias`, `n`, logprobs, and image URLs (base64 only). Native `stream` defaults to true; set `"stream": false` for one JSON object.

```bash
curl -s http://localhost:11434/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"<model>","messages":[{"role":"user","content":"Say hi"}]}'
```
(The `/v1/models` and `/api/version` endpoints were checked against a running local 0.40.3; chat calls were not run in the skill authoring session.)

### 6. Measure and tune
- Throughput: `ollama run <model> --verbose` prints timings; llama.cpp prints timings per request and `llama-bench` is provided for benchmarking (confirm it exists in your build).
- Memory: `ollama ps` (GPU/CPU split), `nvidia-smi` or Activity Monitor/`vm_stat`. A split such as 48%/52% CPU/GPU means the model does not fit in VRAM and generation slows sharply.
- Slow first token on long prompts: prompt processing is compute-bound; reduce context, use flash attention, or a smaller model. Slow generation: memory-bandwidth-bound; a smaller quant or model helps.
- Out-of-memory: lower `-c`/`num_ctx`, reduce `-np`, quantize the KV cache (`-ctk q8_0` or `OLLAMA_KV_CACHE_TYPE=q8_0`, which per the Ollama FAQ only takes effect with flash attention enabled, so also set `OLLAMA_FLASH_ATTENTION=1`; lower precision can reduce quality), choose a smaller quant, or offload fewer layers.
- Quality problems after switching templates: wrong chat template produces degraded output; confirm the template (`ollama show --template`, or llama.cpp `--jinja`/`--chat-template-file`).

### 7. Operate safely
Run as an unprivileged user. Keep the server bound to localhost or a private interface, add auth/TLS at a proxy for any remote access, restrict firewall rules, and rate-limit. Do not mount sensitive directories into tool-using agents backed by the model. Treat the model's output as untrusted input (prompt injection from documents can steer tool calls). Log requests only if you have decided what to retain. Pin model digests and tool versions for reproducible results.

## Worked example: a 16 GiB laptop, coding assistant for one user

1. Budget: roughly 10-11 GiB for model plus cache, leaving headroom for the editor and OS.
2. Candidate: a 7-8B model at Q5_K_M (about 5.3 GiB for an 8B per the bits/weight table) leaves room for a 16K-32K context; a 14B at Q4_K_M (about 8-9 GiB) fits at shorter context. Check licence and pick the instruct variant.
3. Ask the user before pulling (state name, source, size). Run `ollama pull <model>`; start with `OLLAMA_CONTEXT_LENGTH=16384` and `OLLAMA_FLASH_ATTENTION=1`.
4. Confirm placement with `ollama ps`: expect `100% GPU` (or unified memory on Apple silicon); if split, reduce context or drop a quant level.
5. Point the editor/tool at `http://localhost:11434/v1/` with a dummy key; keep `OLLAMA_HOST` default.
6. Evaluate on 30 real coding tasks (see `llm-evaluation`) before relying on it; compare Q4_K_M vs Q5_K_M if memory allows.

## Anti-patterns

- `OLLAMA_HOST=0.0.0.0` on a laptop or server with a public IP and no auth.
- Choosing a model by parameter count alone without computing KV cache for the intended context.
- Assuming the default context is large enough; silent truncation looks like the model "forgetting".
- Re-quantizing an already quantized GGUF; mixing up Ollama's `--quantize` (safetensors) with llama.cpp's `llama-quantize` (GGUF).
- Using the old `./server` binary name or copying flags from old blog posts without checking `--help`.
- Pulling unvetted fine-tunes and merging pickled checkpoints.
- Judging quality from a handful of prompts.
- Running 8 parallel slots at 32K context and wondering why memory is exhausted.

## Verification checklist

- [ ] Hardware, task, context and concurrency requirements captured
- [ ] Memory estimate: weights + KV cache + headroom, vs available memory
- [ ] Model source and licence checked; user approved downloads (name, size)
- [ ] Versions recorded (Ollama / llama.cpp build) and flags confirmed with `--help`
- [ ] Context length set explicitly; `ollama ps` or server logs confirm GPU/CPU placement
- [ ] Server bound to localhost or protected by auth/TLS/network controls
- [ ] Quality checked on task-relevant prompts, not only speed
- [ ] No sensitive data sent before logging/retention was understood

## References

- [references/troubleshooting.md](references/troubleshooting.md) - symptom to cause table
- [references/scenarios.md](references/scenarios.md)
- [references/sources.md](references/sources.md)
