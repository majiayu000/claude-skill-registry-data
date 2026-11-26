---
name: colab-lane
description: Run production GPU jobs on Google Colab (G4 = RTX PRO 6000 Blackwell 96 GB by default; H100/A100/L4/T4 also available on a paid plan) from a local machine, with the signed-in `colab` CLI and the `colab-lane` wrapper (tools/wolkeschieber in this repository). Use when a lane needs to run, compile or benchmark something on a cloud GPU (CUDA, torch, nonce/prescreen kernels, Rust builds). Jobs run until done, then results are downloaded and the runtime is stopped. Covers spend, auth, disconnect handling and the exact failure semantics.
---

# Wolkefahrplan (colab-lane)

## Standard path: `colab-lane` (on PATH)

The wrapper is `tools/wolkeschieber/colab-lane` in this repository; put it on PATH. It needs Google's `colab` CLI,
signed in by a person. Unit prices, machine shapes and region behaviour below are what we measured in November 2026
on one paid account; re-measure before relying on them.

```bash
colab-lane -n myjob-1 -u k.cu -u input.bin -d /content/out.json -- 'nvcc -O3 -arch=native -o k k.cu && ./k > out.json'
#  -g G4 (default) | H100 | A100 | L4 | T4 | cpu
#  -t hard limit in whole minutes (default 0 = none)   -p poll seconds (default 60, min 5)
#  -n session name, [A-Za-z0-9_-] only                 -u upload (repeat)   -d download (repeat)
```

What it does:
1. Validates every flag **before** anything billable starts, then starts the runtime and prints the GPU.
2. Uploads the `-u` files and launches CMD **detached** on the VM, so a dropped connection or a sleeping
   Mac does not kill the job. CUDA and cargo are on PATH. The job also waits for background children it
   spawns, so `foo &` inside CMD does not make the job look finished early.
3. Polls every `-p` seconds, streaming new output to `./colab-out/<name>/stream.log` (and your stdout).
4. On any exit: signals the remote job, downloads the `-d` files into `./colab-out/<name>/`, then stops
   the runtime (retried three times), and sends a macOS notification.

### Exit codes

| code | meaning |
|---|---|
| job's own | the job finished; its exit code is yours |
| 2 | bad usage, refused before any runtime was created |
| 3 / 4 / 5 | could not start / upload failed / launch failed — runtime stopped |
| 7 | the Google sign-in has expired; **runtime kept** so it is not abandoned while unreachable |
| 98 | runtime confirmed gone from the server (true Colab disconnect) |
| 124 | `-t` time limit hit |
| 130 | interrupted (Ctrl-C, SIGTERM, SIGHUP, session teardown) |
| 1 instead of 0 | the job succeeded but a download or the stop failed — read stderr |

**If stop fails after three tries** the state file is kept and the exact recovery command is printed:
`colab --auth=oauth2 --config <state> stop -s <name>`. That is the one case needing your attention.

## Rules

1. **Spend:** G4 ≈ 10 compute units/hour, A100 ≈ 6.7, T4 ≈ 1.15, CPU ≈ 0.08. Check with
   `colab --auth=oauth2 usage`. Spend needs the operator's go-ahead. Say the hours
   and units up front for anything you expect to exceed ~6 hours.
2. **Use a unique `-n` per job.** Two concurrent jobs sharing a name collide on the server side; the local
   state file and output directory are already per-run.
3. **Never touch sessions you did not create.** Other agents' jobs and the operator's notebooks may share the account and show
   as `[?]`. To audit only your own, use `colab --auth=oauth2 --config <your state file> sessions` — a bare
   `sessions` call cannot tell your leaked runtime from someone else's live one.
4. **Never** run `colab repl`, `colab auth`, `colab drivemount`, or a bare `colab ssh` (no `-- CMD`): they
   need a person at the keyboard or create a billable runtime.
5. If anything prints "To authorize colab-cli, visit this URL", stop and ask the operator. Agents cannot sign in.
6. **Do not edit the installed `colab-lane` script in place while jobs run** — a running bash script reads its own
   file as it goes. Write a new file and `mv` it over.

## Checkpointing (read this before a long job)

`-d` files are downloaded **when the job ends**, not during polling, and a runtime that Colab takes away
takes `/content` with it. So `-d` alone does **not** protect a long job:

- Progress you want to keep as it happens should go to **stdout** — that is streamed to
  `./colab-out/<name>/stream.log` every poll and survives any outcome.
- For large intermediate artefacts, have the job push them out itself (to Drive, GCS or a git remote)
  rather than relying on `-d`.
- Treat exit 98 as "the work since launch is gone"; rerun from whatever the job itself persisted.

## Flags and subcommands worth using (verified 2026-11-13)

- **`colab-lane -m`** (passes `--high-mem`): a high-RAM machine shape for CPU, T4 or A100 — ignored for L4
  and TPUs, which have one shape. **Measured on a T4: 50 GB RAM and 8 vCPUs, versus 12.7 GB and 2 vCPUs
  standard, at the same 1.15 units/hr.** For a build that needs memory rather than compute this is far
  better value than an A100 at 6.73/hr; note 50 GB still falls short of a ~53 GB `env -i` build, where
  `-g A100 -m` is the fit.
- **`--tpu V5E1|V6E1`** exists alongside `--gpu`; untried here, only relevant for JAX/XLA work.
- **`colab log -s NAME -o summary.ipynb`** (also `.md`, `.txt`, `.jsonl`, with `-t execution`) exports a
  session's history as a ready-made evidence artefact for a lane report.
- **`colab url -s NAME`** prints a URL that attaches the Colab web UI to an **existing** CLI session, so a
  human can watch a running job without allocating a second runtime. Verified: it connects to the same VM.
- **`colab run script.py`** works as a shebang — `#!/usr/bin/env -S colab run --gpu T4` makes an executable
  `.py` rent a GPU, run and clean up. Short-lived runtimes appearing and vanishing are usually this.

### `google.colab.ai` is UI-only — do not plan a lane around it

Colab's paid plans include key-free LLM access (`from google.colab import ai`), but it is **unusable from
the CLI**. Measured three ways on the same runtime:

| How the code ran | Result |
|---|---|
| Detached bash job (`colab-lane`) | `AttributeError: 'NoneType' object has no attribute 'kernel'` |
| `colab exec` (kernel channel) | `TimeoutException: Requesting secret MODEL_PROXY_API_KEY timed out. Secrets can only be fetched when running from the Colab UI.` |
| `colab exec` **with a browser frontend attached via `colab url`** | same timeout — the UI answers only its own kernel session |
| A cell typed into the attached notebook | **works**: `['google/gemini-3.1-pro-preview', 'google/gemini-3.5-flash-lite', 'google/gemini-3.6-flash', 'google/gemini-3.8-flash']` and `'pong'` |

Note the models are 3.x Flash-class, not the 4-series — so even in the UI it is no substitute for Carbon or
Argon.

### europe-west4 runtimes are unreachable from our machine

Three for three on 2026-11-13: every runtime whose proxy host was `*.europe-west4.prod.r.colab.dev`
(`m-s-euw4b3`, `m-hm-euw4c0`, `m-hm-euw4b0`) failed its first upload with
`ConnectTimeoutError ... connect timeout=None`, after ~3.5 minutes of retries. Every `us-*` and `ass1*`
runtime in the same period worked. The runtime allocates fine; it is the **proxy host** that cannot be
reached, so `upload`, `exec` and `ssh` are all affected and the runtime is useless.

**`colab-lane` now handles this itself** (since 2026-11-14 00:48): after `colab new` it reads the endpoint
from its state file and, if it contains `euw4`, stops the runtime and redraws — up to four attempts, then
exit 3. It also **skips the `-d` downloads when a job never launched**, because attempting them against a
dead proxy cost ~7 minutes of billed runtime per bad draw (~1.2 units on a G4) (measured). A failed-upload teardown now takes ~26 seconds.

Evidence for the region rule is six for six: three test runtimes (`m-s-euw4b3`, `m-hm-euw4c0`,
`m-hm-euw4b0`) and three production jobs, all
allocating normally and then failing their first upload. `asso*` and `us-*` have always worked.

## Telling a lost runtime from a live one

A runtime can disappear mid-job. **A disappearance looks identical whether Colab took it or a human
stopped it** — on 2026-11-13 I read the signals below as a Colab-side loss on an A100 verifier, and its
owner had in fact stopped it deliberately because its queue had been superseded. Ask the owner before
calling it a loss. How to check, without trusting any single signal:

- `colab --auth=oauth2 sessions` lists live endpoints. Compare the `endpoint` field in **your** state file
  (`$TMPDIR/colab-<name>-XXXXXX`) against that list — the endpoint, not the session name.
- A state file pruned to `{}` (2 bytes) means the CLI dropped the entry as stale: the runtime is gone.
- A gone runtime is **not** a leak — it bills nothing and needs no stop. The thing to fix is the supervisor
  still polling it, and any backstop pointing at the dead endpoint.
- On the pre-fix wrapper a loss needed three *consecutive* failed polls, and an external watchdog that
  killed hung `colab exec` calls kept resetting the count, so the wrapper polled a dead runtime for hours.

## Gotchas when using the raw CLI

- `--auth=oauth2` goes **before** the subcommand. Feed `</dev/null`.
- zsh does not split `$C`. Use a function: `C(){ colab --auth=oauth2 "$@" </dev/null; }`.
- A runtime accepts only **one ssh connection** (HTTP 429 for a second), and an ssh that launches a
  background job stays open until the job ends — which is why `colab-lane` launches and polls through
  `colab exec` instead. Do not hold an ssh open on a colab-lane runtime.
- `colab ssh -- CMD` has a minimal PATH: `export PATH=/usr/local/cuda/bin:$PATH` before `nvcc`.
- `colab` calls have no internal timeout and can block on a half-open socket; `colab-lane` wraps every call
  in `timeout`. Do the same in your own scripts.
- In `colab exec`, IPython echoes the value of a trailing expression (`sys.stdout.write(...)` prints its
  character count). End with `print(..., end='')` or an assignment.

## Runtime facts (measured 2026-11-13)

- **G4:** NVIDIA RTX PRO 6000 Blackwell Server Edition, 96 GB, compute capability 12.0 (`-arch=native`
  or `sm_120`), 48 vCPUs, 176 GB RAM, ready in ~3 s.
- **H100:** included in the plan we used, but frequently answers "Service Unavailable" — capacity, not
  permission. Retry; do not conclude it is blocked.
- **T4:** 15 GB, ~23-25 fp16 TFLOPS. **CPU:** 2 vCPUs, 12.7 GB RAM.
- All runtimes: CUDA 13.0 at `/usr/local/cuda/bin/nvcc`, torch 2.14.1+cu130, Ubuntu 24.04, Python 3.13,
  working directory `/content`.
- **Long runs are fine:** a job ran 148 minutes with no disconnect, well past Colab's ~90 min idle limit for
  browser notebooks. Colab still caps total runtime lifetime (~24 h).

## Verification status (2026-11-13)

Tested on real runtimes: happy path with upload/compile/run/download/stop; multi-argument CMD quoting;
partial lines and background children in the log; `-t` enforcement (exit 124); SIGTERM teardown in 4 s;
an upload that failed mid-run (runtime still stopped); and every flag-validation refusal. After an
adversarial review by Gemini 4 Carbon, the following were fixed: a local network outage being
misread as "runtime lost" and skipping the stop; failing polls bypassing `-t` forever; a second signal
aborting teardown; `sleep` deferring signals for a whole poll interval; unbounded `colab` calls; `started`
being set after the create call; a single un-retried stop that still exited 0; unanchored session matching;
lost partial/`\r` log lines; `$*` quoting; AppleScript injection through `-n`; and bash 3.2 array expansion.
**Not** covered: per-poll checkpoint download (see Checkpointing), and Jupyter iopub rate limits on very
chatty jobs (each poll reads at most 200 KB).
