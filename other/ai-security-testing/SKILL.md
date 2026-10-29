---
name: ai-security-testing
description: "Test AI systems: model endpoints for jailbreaks and leakage, model files for malicious pickle code, and agentic apps/MCP surfaces for reachable capability. Use when the target is an LLM API, a chatbot, a downloaded model artefact, or an agent built on CrewAI/LangGraph/OpenAI Agents. Not for classic web or network testing (use toolchain-router)."
---

# AI security testing

Four different targets, four different questions. Pick the row before picking the tool; most wasted AI-testing effort is a model probe aimed at an agent, or a static scan aimed at a live endpoint.

| Target | Question | Tool |
| --- | --- | --- |
| Model endpoint / chatbot | Can a prompt get past the guardrail, leak the system prompt, or invoke a tool it should not? | [garak](../garak/SKILL.md), `promptmap`, `deepteam`, `pyrit_scan` |
| Local model file (`.pkl`, `.pt`, `.h5`, `.gguf`) | Will loading this execute code? | [model-file-audit](../model-file-audit/SKILL.md) |
| Agentic application source | What can the agent reach — tools, files, network, other agents? | [agentic-radar](../agentic-radar/SKILL.md) |
| Installed agent surface on a host | What MCP servers, skills and configs exist, and are any of them hostile? | [snyk-agent-scan](../snyk-agent-scan/SKILL.md) |

## Prerequisites on this host

```sh
redteam-check | grep -A9 'ai / llm'
```

`garak`, `pyrit_scan`, `deepteam`, `promptmap`, `picklescan`, `fickling`, `agentic-radar`, `skill-scanner`, `snyk-agent-scan`. Nothing here needs a GPU; `garak` and `pyrit` are the only large installs (~6.4G and ~1.1G of wheels). Endpoint testing needs a reachable model — a local llama.cpp/Ollama server or an API key in the environment.

Not installed, deliberately: `modelscan` (tensorflow base dependency), `AI-Infra-Guard` (Docker-only release), `aisbom`/`power-pwn` (not on the reachable package index).

## Endpoint testing

```sh
# enumerate probes and pick a family
garak --list_probes
garak --model_type rest -m <probe> --generations 3 --report_prefix ./garak-run
garak --model_type openai --model_name gpt-4o-mini -m encoding,injection  # needs OPENAI_API_KEY

# an injection oracle: a second model judges whether the first obeyed
promptmap -u https://target.example/chat -m gpt-4o-mini -o results/

# jailbreak and injection simulation with guardrail output
deepteam
```

Rules for endpoint work:

1. **One variable per run.** Change the probe family, not the probe family and the temperature.
2. **Baseline first.** Record the refusal text for a benign prompt; a "jailbreak" that returns the same refusal is a false positive.
3. **Cap generations.** Rate limits and cost scale linearly with `--generations`; three is enough for a first pass.
4. **Judge with a different model than the target** where possible; a model grading itself is not evidence.

## Model file audit

```sh
picklescan -p model.pkl
picklescan -hf some-org/some-model          # scan before download-and-load
fickling --check-safety model.pkl
fickling model.pkl                          # decompile to readable Python
```

Decision rule: any `dangerous` global in `picklescan` output, or any `__reduce__` reaching `os`, `subprocess`, `eval`, `exec`, `builtins`, means the file is code, not data. Do not load it in a process that holds credentials. `fickling` exists to show you what a malicious pickle would do, not only to flag it.

## Agentic application review

```sh
agentic-radar scan crewai -i ./agent-src -o ./radar        # frameworks: langgraph, crewai, n8n, openai-agents, autogen
agentic-radar scan langgraph -i ./src --export-graph-json graph.json
```

Read the map before running the app: which tools are bound, which filesystem and network paths they reach, whether prompts are concatenated from untrusted input, and whether a sub-agent can spawn another. Static review is cheap; a live agent with shell access is not.

## Host surface inventory

```sh
snyk-agent-scan scan --json > surface.json
skill-scanner --help         # per-skill verdict with rules + optional model judge
```

`skill-scanner` matters when a skill or MCP server arrives from a marketplace: a tool description is untrusted input that the agent will read.

## Reporting

For each finding record: target, probe or payload, model/version, observed response, expected behaviour, and whether it reproduced. Severity depends on what the model could reach, not on how clever the prompt was. A jailbreak on a chatbot with no tools is informational; a jailbreak on an agent holding a shell is critical.

## OPSEC and telemetry

- Endpoint probes are ordinary HTTP requests; the provider sees them, logs them, and may ban the key.
- Never send real customer data, real credentials, or real internal hostnames as test payloads.
- Model-file scanning is offline. Uploading a suspicious artefact to a public scanner leaks your target's code.
- Agentic review reads source; keep the analysed tree out of shared caches.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `garak` exits with a target error | model unreachable or wrong `--model_type` | test the endpoint with `curl` first |
| Every probe "passes" | target returns a generic refusal for everything, including benign prompts | baseline check — the harness is broken, not the model |
| `picklescan` clean but file still suspicious | payload behind a custom unpickler or non-pickle format | `fickling` decompile, or read the archive members |
| `agentic-radar` finds no workflows | source is not a supported framework | check `--help` for supported layouts |
| `snyk-agent-scan` misses a server | config outside the scanned paths | pass `--storage-file`, or name the path explicitly |

## Verification

```sh
garak --version
picklescan -p /tmp/evil.pkl        # expect: dangerous import ... FOUND
fickling /tmp/evil.pkl | head -3   # expect: the decompiled call
agentic-radar --help
python3 -c "import pickle,os; pickle.dump(type('E',(),{'__reduce__':lambda s:(os.system,('id',))})(), open('/tmp/e.pkl','wb'))"
```

## Related skills

- [garak](../garak/SKILL.md), [model-file-audit](../model-file-audit/SKILL.md), [agentic-radar](../agentic-radar/SKILL.md), [snyk-agent-scan](../snyk-agent-scan/SKILL.md)
- [web-traffic-js-reversing](../web-traffic-js-reversing/SKILL.md) when the AI product ships a web client worth reading