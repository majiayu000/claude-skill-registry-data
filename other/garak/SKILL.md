---
name: garak
description: "Probe a live LLM endpoint with garak's vulnerability scanners: jailbreaks, prompt injection, leakage, encoding and toxicity, with per-probe pass/fail reporting. Use when you have a reachable model (local server or API key) and need repeatable evidence of guardrail behaviour. Not for static model-file inspection (use model-file-audit) or agent source review (use agentic-radar)."
---

# garak

garak is NVIDIA's LLM vulnerability scanner. It sends a probe's prompt set to a generator you name, records every response, and runs detectors that decide whether the target failed. It talks to anything with an HTTP API - OpenAI-compatible servers, Ollama, Hugging Face, or an arbitrary REST endpoint described in JSON. Nothing in a run needs a GPU; the cost is in tokens and time.

On this host: `garak` v0.17.1 at `~/.local/bin/garak`, 233 probe entries, and the offline `test` generator that needs no model at all.

## When to use

| Question | Probe family | Shape |
| --- | --- | --- |
| Does a prompt get past alignment? | `dan`, `promptinject`, `latentinjection` | `-S probes.dan` |
| Is the system prompt or training data exposed? | `leakreplay`, `sysprompt_extraction` | `-S probes.leakreplay` |
| Can encoding or smuggling carry a payload? | `encoding`, `smuggling`, `badchars` | `-S probes.encoding` |
| Are API keys or secrets recoverable? | `apikey` | `-S probes.apikey` |
| Does the model emit working malicious output? | `malwaregen`, `exploitation`, `xss` | `-S probes.malwaregen` |
| Does the model invent packages that attackers can register? | `packagehallucination` | `-S probes.packagehallucination` |
| Is output toxic or biased? | `realtoxicityprompts`, `lmrc` | `-S probes.realtoxicityprompts` |
| Is my harness working at all? | `test` with `-m test` | offline smoke run |

Pick the smallest family that answers the question. `-S 'probes.dan,-probes.dan.DanInTheWildFull'` selects a module and excludes one noisy class; `tier:1` limits the run to the shallow probes.

## Prerequisites

- `garak --version` prints `v0.17.1`. Installed with pipx at `~/.local/bin/garak`; no global `garak` in `/usr/bin`.
- A reachable target. Three options: a local server (`ollama`, `llamacpp`-style OpenAI-compatible), a hosted API with the provider's key in the environment (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`), or a `rest` generator pointing at any URL.
- For `rest`, the API key variable is `REST_API_KEY` unless you override `key_env_var` in the generator options. For `openai.OpenAICompatible` it is `OPENAICOMPATIBLE_API_KEY`; a local server usually accepts any non-empty value.
- Disk and patience: every prompt and response is written to the run's `.jsonl`; a full `dan` run is large.
- CPU is enough. The default detectors are local heuristics plus a small intent model that garak loads itself; no GPU, no extra service.
- Nothing here is allowed to point at a third party without written authorization. A scan is a stream of hostile prompts that a provider will log and may ban.

## Core invocations

```sh
# 1. version, plugin inventory, per-plugin documentation
garak --version
garak --list_generators
garak --plugin_info probes.dan.DanInTheWild
garak --plugin_info generators.rest.RestGenerator

# 2. offline smoke run: proves the harness works before you touch a target
garak -m test -S probes.encoding.InjectBase64 -g 1 --report_prefix /tmp/garak-smoke

# 3. local OpenAI-compatible server (llama.cpp, vLLM, LM Studio):
#    the class is openai.OpenAICompatible, the URL goes in the options, -n is the model id
cat > /tmp/oai.json <<'JSON'
{"openai": {"OpenAICompatible": {"uri": "http://127.0.0.1:8080/v1/"}}}
JSON
OPENAICOMPATIBLE_API_KEY=dummy garak -m openai.OpenAICompatible -G /tmp/oai.json \
  -n local-model -S probes.dan --generations 1 --report_prefix /tmp/garak-local

# 4. hosted model; key comes from the environment, never from the command line
OPENAI_API_KEY=... garak -m openai -n gpt-4o-mini -S probes.promptinject -g 3 \
  --report_prefix /tmp/garak-openai

# 5. Ollama by model name
garak -m ollama -n llama3.2 -S probes.leakreplay --report_prefix /tmp/garak-ollama

# 6. arbitrary REST endpoint, described in JSON (uri is mandatory here)
cat > /tmp/rest.json <<'JSON'
{"rest": {"RestGenerator": {
  "uri": "http://127.0.0.1:8099/chat",
  "method": "post",
  "headers": {"Content-Type": "application/json"},
  "req_template_json_object": {"messages": [{"role": "user", "content": "$INPUT"}]},
  "response_json": true,
  "response_json_field": "$.text"
}}}
JSON
garak -m rest -G /tmp/rest.json -S probes.encoding -g 1 --report_prefix /tmp/garak-rest

# 7. narrow a run: one module, exclude a class, tier 1 only
garak -m test -S 'probes.dan,-probes.dan.DanInTheWildFull,tier:1' -g 1 \
  --report_prefix /tmp/garak-tier1

# 8. select by taxonomy tag instead of module name
garak -m test -S 'tag:owasp:llm01' -g 1 --report_prefix /tmp/garak-llm01

# 9. speed up a remote target without changing the probe set
garak -m openai -n gpt-4o-mini -S probes.encoding --parallel_attempts 8 \
  --parallel_requests 2 --report_prefix /tmp/garak-par

# 10. reproducibility: fixed seed, fixed generations
garak -m test -S probes.badchars -g 1 --seed 42 --report_prefix /tmp/garak-seeded

# 11. override run parameters or detector thresholds
garak -m rest -G /tmp/rest.json -S probes.encoding --eval_threshold 0.8 \
  --probe_options '{"encoding": {"InjectBase64": {"payloads": ["default"]}}}' \
  --report_prefix /tmp/garak-opts

# 12. keep only what you need for a report
garak -m test -S probes.encoding.InjectBase64 -g 1 --narrow_output \
  --report_prefix /tmp/garak-narrow

# 13. inspect a finished run instead of re-scanning
ls /tmp/garak-narrow.report.jsonl /tmp/garak-narrow.report.html
```

Note on names: the target flag is `-t/--target_type/--model_type/-m` and the model flag is `-n/--target_name/--model_name`. There is no `--probe_spec`; the selection flag is `-S/--spec`. `--probes/-p` still exists but prints a deprecation notice in this build, as does `-m`.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-m, --model_type` | generator module and optional class | `openai`, `ollama`, `rest`, `huggingface`, `test` |
| `-n, --model_name` | model name or endpoint URL | not used by `rest`; put `uri` in the options JSON |
| `-S, --spec` | unified selection | `probes.<mod>[.<Class>]`, `buffs.*`, `tag:<prefix>`, `tier:<N>`; `-` excludes |
| `-g, --generations` | generations per prompt | cost multiplier; 1-3 for a first pass |
| `--report_prefix` | output basename | writes `.report.jsonl` and `.report.html` |
| `--list_probes` | list probes; `-v` for markdown detail | 233 entries here, inactive ones marked |
| `--plugin_info` | docs and defaults for one plugin | fastest way to get a probe's goal and detector |
| `-G, --generator_option_file` | JSON generator options | where `rest` gets `uri`, headers and JSON template |
| `--generator_options` | same as inline JSON | no short form |
| `--parallel_attempts` | concurrent probe attempts | the only safe speedup for remote targets |
| `--eval_threshold` | minimum score for a hit | lower it to see near misses |
| `-d, --detectors` | override the probe's detector | `all` is noisy; prefer the default |
| `--taxonomy` | group results by MISP taxonomy | `owasp`, `avid-effect` |
| `--seed` | reproducible sampling | pair with a fixed `--config` for a repeatable run |

## Workflow

1. **Prove the harness offline.** Run `-m test` with one probe. If that fails, the problem is garak, not the target.
2. **Prove the target with one benign request.** `curl` the endpoint with a harmless prompt and read the exact response shape before configuring `response_json_field`.
3. **Baseline the refusal.** Send one benign and one obviously hostile prompt by hand. A target that answers everything with a canned refusal will "pass" every probe and tell you nothing.
4. **Select narrowly.** One probe family per run. Changing family, temperature and model in the same run makes the result unattributable.
5. **Cap cost.** `-g 1` for triage, `-g 3` to confirm a hit. Watch `--parallel_attempts` against rate limits.
6. **Read the report, then the transcript.** The summary gives pass/fail counts and confidence intervals; the `.jsonl` gives the exact prompt, the exact response and the detector's reason.
7. **Re-run only confirmed hits.** A 1 percent attack success rate on 256 prompts is two prompts; read them before calling it a finding.

## OPSEC and telemetry

- Every probe is an ordinary HTTP request to the target. The provider sees the prompt text, your source address, and the key.
- Hosted providers log and may ban an API key used for jailbreak-style traffic. Use a dedicated key with a hard spend cap, never a customer key.
- Reports are sensitive: `.report.jsonl` contains the full hostile prompts and the model's full responses. Treat a report directory like a credential.
- garak writes its own log to `~/.local/share/garak/garak.log`; it persists prompts between runs.
- Payloads are deliberately hostile. Do not paste real customer data, real internal hostnames or live credentials into probe options.
- The `apikey` probe family exists to test whether a model regurgitates secrets. Running it against a production endpoint with a live key in the prompt is a self-inflicted exposure.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `No REST endpoint URI definition found` | `rest` was given `-n` instead of a `uri` in options | put `uri` in the `-G` JSON |
| `all plugins in 'probes.test' are marked inactive` | the whole `test` module is inactive by design | name one active class, e.g. `-S probes.encoding.InjectBase64` |
| Every probe passes with identical text | target returns a canned refusal for everything | baseline by hand; the harness is measuring the wall, not the model |
| `Put the OpenAI API key in the OPENAI_API_KEY environment variable` | hosted class without a key | export it for the process; use `openai.OpenAICompatible` for a local server |
| HTTP 429 mid-run | `--parallel_attempts` too high for the tier | drop to 1-2, or use a model with higher limits |
| Response parsed as empty string | wrong `response_json_field` JSONPath | inspect one response body, then set the path |
| Run takes hours locally | `huggingface` pipeline loading weights on CPU | use a served endpoint instead of in-process inference |
| Detector crashes on one response | malformed or truncated output | `--skip_unknown`, and check the `.jsonl` entry |

## Verification

```sh
garak --version
# garak LLM vulnerability scanner v0.17.1 ...

garak --list_probes | grep -c 'probes:'
# 233 probe and class lines

garak -m test -S probes.encoding.InjectBase64 -g 1 --report_prefix /tmp/gv
# "garak run complete in ...", encoding.DecodeMatch PASS, report .jsonl + .html written

ls -l /tmp/gv.report.jsonl /tmp/gv.report.html
# both exist; the jsonl has one JSON object per attempt
```

Evidence to keep: the exact command line, the report prefix, the model name and version, and the per-probe attack success rate with its confidence interval.

## Related skills

- [ai-security-testing](../ai-security-testing/SKILL.md) for choosing between garak, `promptmap`, `deepteam` and `pyrit`
- [model-file-audit](../model-file-audit/SKILL.md) when the model is a file on disk, not an endpoint
- [agentic-radar](../agentic-radar/SKILL.md) when the target is an agent with tools rather than a bare model
- [web-traffic-js-reversing](../web-traffic-js-reversing/SKILL.md) when the endpoint is undocumented and the web client shows the request shape
