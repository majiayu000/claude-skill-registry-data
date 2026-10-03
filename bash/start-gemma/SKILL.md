---
name: start-gemma
description: Start, restart, or switch between the local Gemma 4 llama.cpp services (E2B / 12B / 26B-A4B / 31B), letting the user choose which one. Use when the user says /start-gemma, asks to start or restart Gemma, wants to switch which Gemma model is serving, reports that port 8002/8003/8004/8005 is unavailable, or asks which Gemma is currently running.
metadata:
  hermes:
    tags: [llama-cpp, systemd, mtp, gemma, gfx1151, rocm]
---

# Start Gemma

Four Gemma 4 services exist, each on its own port. They are **not** all runnable at once — see the memory rules below.

| model | unit | port | ~RAM | pi provider | runtime |
|---|---|---|---|---|---|
| `e2b` | `gemma-mtp.service` | 8002 | ~5 GB | `local-gemma-e2b` | `atomic-llama-cpp-turboquant` |
| `12b` | `gemma4-12b-mtp.service` | 8004 | ~11 GB | `local-gemma-12b` | upstream b10200 |
| `26b` | `gemma4-26b-mtp.service` | 8005 | ~17 GB | `local-gemma-26b` | `llama-turboquant` |
| `31b` | `gemma4-31b-mtp.service` | 8003 | ~30 GB | `local-gemma-31b` | upstream b10200 |

All four run Flash Attention on, MTP speculative decoding on, and ctx 262144.

## Ask the user which model

If the user did not name one, ask. Do not guess — starting the wrong one may stop the model they are using. `status` is always safe:

```bash
/home/chihmin/.claude/skills/start-gemma/scripts/start-gemma.sh status
```

## Start a model

```bash
/home/chihmin/.claude/skills/start-gemma/scripts/start-gemma.sh 26b
```

The helper:

1. sets the `performance` power profile;
2. checks `free -g` available RAM against the model's requirement;
3. stops the other Gemma services if headroom is short (`--keep-others` to suppress);
4. restarts the unit and polls `/health` for up to 30 minutes;
5. every 2 minutes while loading, reports RSS and process state, and explains a JIT stall if it sees one;
6. verifies the served alias, and the live `--flash-attn` / `--spec-type` / ctx flags from `/proc/<pid>/cmdline`;
7. prints the pi provider name and a final status table.

Options: `--keep-others`, `--no-wait`. Other verbs: `status`, `stop-all`.

## Memory rules (the important part)

**System RAM is the binding constraint, not GTT.** This is a UMA APU — GTT allocations come out of system RAM. GTT showing 22 GB free while `free -g` available is 9 GB means you cannot start another model. `earlyoom` sends SIGTERM at 3 GB free.

Roughly what fits alongside `qwen-mtp` (port 8001, ~15 GB, usually left running):

- e2b + 12b + 26b together — yes, this is the normal steady state
- 31b + anything substantial — no; the 31B alone needs ~30 GB
- 31b and 12b/26b together — no

**Load order matters.** Start the biggest model *first*, while RAM is free, then bring the smaller ones back. Starting the 26B into 12 GB of available RAM stalls it for tens of minutes; starting it into 23 GB takes 20 seconds.

## A slow start is usually JIT, not a hang

A llama-server that has not become healthy after several minutes is normally **compiling ROCm kernels**, not hung. Diagnose:

```bash
ps -o rss=,stat=,etime=,time= -p <pid>     # R state + CPU time ≈ elapsed
amdgpu_top -d | grep GTT                   # flat => weights already resident
```

One core at 100% with GTT flat means kernel JIT. It is one-time: results land in `~/.cache/comgr` and later restarts are fast (the 26B went from 40+ minutes cold to under 30 seconds warm). **Do not kill it** — unless RSS is *shrinking*, which means it is losing the fight for memory; then stop another model and start again.

## After switching

`pi` and the piweb model picker read `~/.pi/agent/models.json` **at process start**. All four Gemma entries already exist, so switching models needs no config change — but a model whose service is stopped will simply fail to connect. Only if you *edit* `models.json` do you need:

```bash
sudo systemctl restart piweb-worker.service
```

Note that llama.cpp ignores the `model` field in requests and serves whatever it loaded, so pointing a client at the wrong port yields the wrong model silently rather than an error.

## Performance, to help the user choose

Measured on this box (calibrated 20K prompt / pi agent end-to-end):

| model | prefill TPS @20K | decode TPS @20K | pi "reply OK" wall |
|---|---|---|---|
| e2b | 1329 | 57.9 | 25 s |
| 26b | 1017 | 29.3 | 33 s |
| 12b | 668 | 37.6 | 50 s |
| 31b | 245 | 11.5 | **135 s** |

The 31B is slow enough to be painful as an interactive agent backend — pi's ~29K-token system prompt alone costs it about two minutes of prefill before the first token. It also has a known tendency to generate without terminating on open-ended coding prompts. Prefer the 26B or 12B unless the user specifically wants the 31B.

Full profiling report: https://gist.github.com/AyaSakura-comp/861f5ea619da7463295f0ab1ac2d895c
