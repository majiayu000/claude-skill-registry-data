---
name: imagegen-swarm
description: "Indie devs, creators, sellers: pool AI image quotas into one batch that keeps going if one runs out. Use when the user asks to generate an image, draw, edit an image, use reference images, make a video, or do text-to-image or text-to-video. Also use when the request names Codex, Grok, Grok Imagine, Gemini, nano banana, Antigravity, Jimeng, Dreamina, Muse, Lovart, gpt-image, or a pay-per-image API. Jimeng and Grok can make video. An optional pay-per-image API line (OpenAI or Gemini API) runs when a job names api, or when no enabled subscription engine can take that job. Jimeng can edit from up to 10 reference images. Antigravity Gemini edits up to 3 reference images. The optional paid Gemini API allows 3 references for gemini-2.5-flash-image and 14 for later Gemini image models. For a shared character, brand, mascot, or cover series, ask before enabling series mode. Not for crop, resize, convert, or other ordinary local image processing."
version: 1.4.4
allowed-tools: Bash Read Write WebFetch Env
metadata:
  openclaw:
    emoji: "🖼️"
    homepage: https://github.com/Ekko237/imagegen-swarm
    requires:
      bins:
        - node
      anyBins:
        - python3
        - python
      config:
        - $HOME/.lovart/env
        - $HOME/.lovart/state.json
        - $HOME/.config/imagegen-swarm/api.json
        - $HOME/.config/imagegen-swarm/api-key
        - $HOME/.config/imagegen-swarm/api-spend.jsonl
        - $HOME/.config/imagegen-swarm/engine-off
        - $HOME/.config/imagegen-swarm/muse-browser
        - $HOME/.config/imagegen-swarm/models
        - $HOME/.config/imagegen-swarm/smoke-last.json
        - $HOME/.config/image-gen/engine-off
        - $HOME/.config/image-gen/muse-browser
        - $HOME/.codex/auth.json
        - $HOME/.codex/generated_images
        - $HOME/.gemini/antigravity-cli/brain
        - $HOME/.grok/sessions
    envVars:
      - name: PYTHON
        required: false
        description: Python used for imgtool.py, Muse, and the Lovart client. Defaults to python3, or python on Windows.
      - name: CODEX_BIN
        required: false
        description: Path to the Codex CLI when it is not on PATH.
      - name: CODEX_HOME
        required: false
        description: Codex home directory. Generation reads only its generated_images subdirectory, to hash older files and reject a reused image. It does not read auth, config, or session files. check.mjs only tests whether auth.json exists.
      - name: AGY_BIN
        required: false
        description: Path to the Antigravity CLI. Defaults to $HOME/.local/bin/agy.
      - name: DREAMINA_INSTALL_DIR
        required: false
        description: Directory containing the user-installed dreamina binary.
      - name: LOVART_ACCESS_KEY
        required: false
        description: Lovart access key. Read from the environment or from the file $HOME/.lovart/env. That file is read as text and is not executed.
      - name: LOVART_SECRET_KEY
        required: false
        description: Lovart secret key. Read from the environment or from the file $HOME/.lovart/env. That file is read as text and is not executed.
      - name: LOVART_ENV
        required: false
        description: Lovart credentials file. Defaults to $HOME/.lovart/env and is read as text. Group or other write access is refused. Read access produces a warning.
      - name: LOVART_BASE_URL
        required: false
        description: "Lovart API base URL. Defaults to https://lgw.lovart.ai."
      - name: LOVART_LV
        required: false
        description: Optional Lovart wrapper path. An existing wrapper takes precedence over scripts/lovart_agent.py.
      - name: LOVART_AGENT_SKILL
        required: false
        description: Read only by an optional user-made lv wrapper to locate scripts/lovart_agent.py. The bundled scripts do not read it; check.mjs passes it through to its probes.
      - name: OPENAI_API_KEY
        required: false
        description: Optional pay-per-image key when api.json uses the OpenAI provider. api.json may name a different variable with key_env; that variable is read the same way.
      - name: GEMINI_API_KEY
        required: false
        description: Optional pay-per-image key when api.json uses the Gemini provider.
      - name: IMAGE_GEN_API_CONFIG
        required: false
        description: Override path for the pay-per-image api.json config.
      - name: IMAGE_GEN_API_LEDGER
        required: false
        description: Override path for the pay-per-image spend ledger.
      - name: IMAGE_GEN_ENGINE_OFF
        required: false
        description: Directory of empty per-engine marker files. Defaults to $HOME/.config/imagegen-swarm/engine-off. One empty file named for the engine pauses that engine.
      - name: IMAGE_GEN_MEMORY_GB
        required: false
        description: RAM budget in GB used to size engine lanes.
      - name: IMAGE_GEN_MUSE_PROFILE
        required: false
        description: Muse browser profile directory. Defaults to $HOME/.config/imagegen-swarm/muse-browser. Created only by muse-image.py --login.
      - name: IMAGE_GEN_MUSE_REMOTE_DIR
        required: false
        description: Cloud save directory under /home/hatch/. Defaults to /home/hatch/workspace/image-gen for the legacy profile and /home/hatch/workspace/imagegen-swarm otherwise.
      - name: IMAGE_GEN_MUSE_APPROVAL
        required: false
        description: Default and legacy accept narrowly scoped exact-file Allow once cards. Strict requires a fully decoded single-image save.
      - name: IMAGE_GEN_GROK_MODE
        required: false
        description: Pin scoped or legacy. Default and scoped use the job tool allowlist only and fail closed on a refusal. Set legacy to opt in to the workspace-sandboxed --always-approve path, with Bash and web tools still denied.
      - name: IMAGE_GEN_SMOKE_CACHE
        required: false
        description: Optional override for the local smoke readiness cache path.
      - name: IMAGE_GEN_SMOKE_SCRIPTS_DIR
        required: false
        description: Offline smoke fixture directory. Fixture runs save their result beside the test output instead of updating account readiness.
      - name: HTTPS_PROXY
        required: false
        description: Optional proxy for the Muse browser only.
      - name: IMAGE_GEN_CLIP_MODEL
        required: false
        description: Optional local CLIP ONNX file for the series-mode clip score. Defaults to $HOME/.config/imagegen-swarm/models/clip-vit-b32-vision-q8.onnx. Read only; never downloaded by the skill.
      - name: IMAGE_GEN_CLIP_ALLOW_UNVERIFIED
        required: false
        description: Set to yes only if the user explicitly trusts a CLIP ONNX file whose SHA-256 is outside the validated list.
      - name: https_proxy
        required: false
        description: Lower-case form of HTTPS_PROXY, read only when HTTPS_PROXY is unset or empty. Muse browser only.
      - name: IMAGE_GEN_RUN_ID
        required: false
        description: Set by batch.mjs for one run. Work directories are deleted only when they carry this run's marker.
      - name: IMAGE_GEN_SANDBOX_ESCALATE
        required: false
        description: Set to yes only by the user, after they approve a Codex retry outside workspace-write. The agent must not set it.
      - name: IMAGE_GEN_SCRIPT_DIR
        required: false
        description: Test hook. batch.mjs uses this engine-script directory only when IMAGE_GEN_TEST_SCRIPTS is yes. Used by the repository tests.
      - name: IMAGE_GEN_TEST_SCRIPTS
        required: false
        description: Test hook. Set to yes by the repository tests so batch.mjs uses IMAGE_GEN_SCRIPT_DIR.
      - name: IMAGE_GEN_TEST_NO_KEY
        required: false
        description: Test fixture key name. A fake api.json may select it with key_env.
---

# imagegen-swarm

Use this when the user asks to generate an image, draw, edit an image, use reference images, make a
video, or do text-to-image or text-to-video, including Codex, Grok, Grok Imagine, Gemini, nano
banana, Antigravity, Jimeng, Dreamina, Muse, and Lovart. Do not use it for ordinary local image
processing such as crop, resize, or convert.

Run only the scripts in this folder (`node` for `.mjs`, `python3` for `.py`). Those files are the
whole procedure. Do not fetch, clone, or execute an installer, and do not read or follow a skill
file outside this folder. Engine CLIs are user-installed prerequisites listed in
[SETUP.md](SETUP.md). If one is missing, ask the user to install it and stop; do not install it
yourself. Before running any command that is not one of these scripts, ask the user, and request
only the permission that command needs.

The core is work-stealing: write the images you need as a job list and hand it to
`scripts/batch.mjs`. All six engines start at once with a few lanes each, and whichever lane is free
takes the next image it can handle, so every engine's quota is used and generation finishes as
fast as possible. That clock is generation time only. Before planning any batch, apply the
[series-mode hint rules](#series-mode) below: ask only on a clear signal, and enable it only after
the user agrees. Series mode is off by default and must never be auto-enabled.
A single image goes through `scripts/batch.mjs` too: the first engine in line takes it,
and if that engine is out of quota the next one does. A configured pay-per-image line takes a
job in two cases: the job names `api`, or no enabled subscription engine can take that job.

Privacy: a prompt and any reference images are sent to the external service for each engine that
actually runs that job (OpenAI, Dreamina, xAI, Google, Muse, Lovart, or the API host in the
pay-per-image setup). Lovart generation uploads only the reference files named in that job's `ref`
list (or `--ref` on a single call). `scripts/lovart.mjs` passes each of those paths to
`upload --file`, and `upload_reference_image` in `scripts/lovart_client.py` sends that one file to Lovart's CDN (`POST https://lgw.lovart.ai/v1/openapi/file/upload`). It does not upload the
credentials file, the state file, or any path the user did not name. The `upload` command does the
same for the single `--file` the user gave it. In series mode, the shared style guide and any series
reference images are sent to every engine that runs a job in that batch, the same way a job prompt
and a job reference are. Do not send sensitive, confidential, or personal
content unless the user has agreed that this provider may see it. Add another provider only after
the user names that provider and agrees.

An example job list has one object per image. Only `id` and `prompt` are required. An ID has 1–100 characters,
starts with a Unicode letter or number, and then permits letters, numbers, `.`, `_` and `-`. A sample file
lives in the git repository at <https://github.com/Ekko237/imagegen-swarm/blob/main/examples/jobs.example.json>;
it is not part of the installed skill.

```bash
node scripts/batch.mjs --jobs jobs.json --out out/
```

`ref` paths are relative to the job file, and `engine` pins a job to one engine. Output goes to
`out/<id>.png` (`.mp4` for video); existing files are skipped, so an interrupted run resumes where
it stopped.

- Lanes scale with your RAM. The baseline is 8 GB (measured on an M1: 12 images at once with no
  slowdown and about 30% memory left): gemini and codex 6 each, jimeng and grok 4, lovart 2. Other
  machines scale proportionally, at least 1 and at most 1.5× per engine (4 GB → 12 lanes in total,
  16 GB or more → 34); muse always gets 1. Lanes take work in that order and the first log line
  shows the counts. Set `IMAGE_GEN_MEMORY_GB=4` (for example) to size lanes for a smaller memory
  budget. `--engines` limits the engines; `--lanes gemini=3,muse=0` overrides lane counts.
- Tail stealing: once the queue is empty, an idle lane may duplicate an image that is still running.
  It does that only after the holder has run longer than 1.5× its own median time for this batch
  (the built-in typical time until this batch has samples). A fast engine does not redo an image a
  slower engine just started. At most one duplicate runs. Whichever finishes first is kept; the
  other is cancelled (SIGINT to the process group, or a cancel file for Muse) or ignored if it
  finishes later. The results file in the output directory lists every attempt with start, finish and outcome (done,
  cancelled, failed, style_redo, style_rejected).
- An engine that reports exhausted quota, no login or no install is shut down immediately, and the
  image it held goes back to the queue. A plain rate limit (HTTP 429, `rate limit`, or
  `RESOURCE_EXHAUSTED` without an explicit quota or credit failure) backs off and is shut down only
  after three consecutive rate-limit failures. A missing reference or output file, or any other
  generic "not found", does not shut the engine down.
- If a job sets an aspect ratio, an image whose ratio is off by more than 3% is discarded and redone
  by another engine.
- A failed image (refusal, timeout, …) is retried on an engine that has not tried it yet, up to
  `--tries` engines (default 3). An image no engine can take counts as failed.
- Every start, finish, retry and shutdown prints one JSON line; the last line is the summary, and
  the results file in the output directory records which engine made each image and how long it
  took. The summary `keep` object counts this run only: `generated` (the engine returned an image
  file), `kept` (that file was saved as the job output), `redone` (the file was dropped because the
  aspect ratio was off by more than 3% and the job went back on the queue), `duplicates` (a tail-steal
  copy returned a file and was dropped), `style_redos` (the file was dropped because its series style
  score was below the threshold, including a last discard that was not queued again), and `resumed`
  (the output was already on disk and was skipped). `generated` adds up as `kept` + `redone` +
  `duplicates` + `style_redos`. An engine error is not an image, so it is not in those counts.
  `elapsed_seconds` is generation time only: it ends when the last engine attempt finishes, before
  the style score. `delivery_seconds` is the wall clock from the start of the batch until the
  summary, so in series mode it includes style screening and style redos. Exit code is
  non-zero if anything failed.
- At the end of a run, batch deletes only the temporary files it created and the work directories
  that contain this run's marker (`IMAGE_GEN_RUN_ID`). Directories left by another run are left in
  place.
- Pay-per-image last resort `api`: on only when the user has completed the pay-per-image setup in
  [SETUP.md](SETUP.md). The config file is `$HOME/.config/imagegen-swarm/api.json` unless
  `IMAGE_GEN_API_CONFIG` points at another file. It holds `provider`, `model`, `price_per_image`
  (an estimated USD amount, not the provider invoice), `budget_per_batch`, `budget_per_month`, and
  `lanes` (default 4). The key is not in the file. The user placing that file is their consent to
  spend at most those estimated budgets, at `price_per_image`. For one image, the paid line starts
  only when `api` can take it and either the job sets `"engine": "api"` or no enabled subscription
  engine can take it. A subscription engine can take an image when it is in this batch's engine
  list, is not shut down, has not already tried the image, the job does not name a different
  engine, and the image's ratio, reference count, and video fit that engine. Exhausted quota, no
  login, and no install shut an engine down. An image those engines cannot take because of ratio,
  reference count, or video also goes to the paid line. The paid line does not tail-steal, and it
  does not take an image a subscription engine can still take. Before a paid image is started, this process
  reserves it. Every charged attempt stays reserved even if its image is later discarded for
  style, aspect ratio, duplication, or losing a steal race. Only a known uncharged failure
  releases a reservation; uncertain failures keep their slot for this batch. (Confirmed charged
  attempts plus unknown attempts and images still in flight) times
  `price_per_image` is compared with `budget_per_batch`. The ledger total read when this process
  started, plus that same reservation, is compared with `budget_per_month`. If either comparison
  would pass the cap, the line stops and does not start that image. The cap is this estimate. A
  provider can bill a different amount for an image that already started. A second batch process
  does not see a reservation until the API script appends a confirmed charge to the ledger.
  Only an attempt for which the provider returned image bytes appends one JSON line to
  `$HOME/.config/imagegen-swarm/api-spend.jsonl` (`IMAGE_GEN_API_LEDGER` overrides that path),
  before local screening can reject it. Attempt IDs deduplicate confirmed charges. The parent
  never writes unknown outcomes to the ledger. API failures before the request is sent and
  provider HTTP error responses report `charged: false`; unknown request failures keep their
  in-memory reservation, without consuming future batches' month budget.
  Before requeueing or retrying, batch checks both caps again. If another paid image would
  exceed either cap and no subscription engine can take the job, it fails with "stopped by the
  paid budget". The summary and `out/batch-results.json` retain `paid.images` and `paid.usd`
  for confirmed charged images and `paid.month_usd` for the month ledger total. `paid.uncertain`
  counts unknown attempts whose reservations were kept (0 when none). `paid.discarded`
  counts confirmed charged attempts without a kept image, and
  `paid.stopped_by_budget` counts jobs stopped by budget; those failed results also have
  `stopped_by_budget: true`. Ask the user and wait for a
  yes before any paid generation they did not ask for. Leave the pay-per-image file and both
  budgets as the user set them, leave `api` out of `--engines` unless they asked for it, and do not
  add paid jobs beyond the list they gave you. Tell them the estimated cost (`price_per_image`
  times the images that would use the paid line) first.
- When the user names an engine, run only that one with `--engines`.
- To pause an engine, ask the user to create an empty marker file named for that engine inside the
  `engine-off` directory from SETUP.md (or set `IMAGE_GEN_ENGINE_OFF` to a folder they already
  created). Do not create that directory yourself. Batch, check, and evals skip an engine whose
  marker exists. The user deletes the marker to turn the engine back on. A marker left in the
  previous `image-gen` folder still counts.

## What is stored, and when

The agent does not create these directories. The user creates them by running the matching steps in
[SETUP.md](SETUP.md). Generation only reads or writes them after that.

| Path | Created | What is stored | Why |
|---|---|---|---|
| `$HOME/.config/imagegen-swarm/api.json` | User setup | Provider, model, estimated price, budgets. No API key | Turns on the paid line and caps the estimate |
| `$HOME/.config/imagegen-swarm/api-key` | User setup, only if they choose a key file. Mode 600 | The API key | Read at request time. The config file never holds it |
| `$HOME/.config/imagegen-swarm/api-spend.jsonl` | The directory is user setup. Confirmed returned image bytes append one line per attempt | Time, provider, model, estimated price | Compare this batch's reservation with the monthly cap |
| `$HOME/.config/imagegen-swarm/engine-off/<engine>` | User, to pause one engine | Empty file named for that engine | Skip that engine until the user deletes the file |
| `$HOME/.config/imagegen-swarm/muse-browser` | `scripts/muse-image.py --login` only | Browser profile and Muse session | Stay signed in. Generation does not create this directory |
| `$HOME/.lovart/env` | User setup, mode 600 | `LOVART_ACCESS_KEY`, `LOVART_SECRET_KEY`, optional `LOVART_BASE_URL` | Read as text to sign Lovart requests. Other lines in the file are ignored. The file is not executed |
| `$HOME/.lovart/state.json` | Not created by setup. Updated only when `$HOME/.lovart` already exists | Project and thread ids | Resume a Lovart project. A missing directory skips the save |
| `CODEX_HOME/generated_images` | Codex itself, not this skill | Older generated images | Hash them and reject a reused file. Nothing else under `CODEX_HOME` is read |
| `CODEX_HOME/auth.json` | `codex login` | Login state. `scripts/check.mjs` only tests that the file exists | Report whether Codex is logged in |

`scripts/check.mjs` passes its probes only `PATH`, `HOME`, temporary-directory variables, proxy and
CA settings, and the variables named in the frontmatter above. It does not copy the whole
environment into those probes. A batch keeps the environment of the process that launched it, and
Lovart generation does the same, adding the three credential names when they were read from the
credentials file. That file is read as text; only the three names in the table are kept.

## Network and credentials

Every outbound connection the bundled scripts make, and every secret they read. Nothing here runs
until the user asks for an image or runs a readiness or smoke check. Each engine is optional: its files
and variables matter only if the user set that engine up. ClawHub lists every `requires.config`
entry as required; all of them are optional per engine.

| Script | Talks to | When | Credential it reads | What is sent |
|---|---|---|---|---|
| `codex-image.mjs` | OpenAI, through the user's `codex` CLI | A job runs on codex | None; `codex` uses its own login | Prompt, reference images |
| `grok-image.mjs` | xAI, through the user's `grok` CLI | A job runs on grok | None; `grok` uses its own login | Prompt, one reference image |
| `gemini-image.mjs` | Google, through the user's `agy` (Antigravity) CLI | A job runs on gemini | None; `agy` uses its own login | Prompt, up to 3 reference images |
| `jimeng-image.mjs`, `jimeng.mjs` | Dreamina, through the user's `dreamina` CLI | A job runs on jimeng | None; `dreamina` uses its own login | Prompt, reference images |
| `muse-image.py` | `https://muse.ai` in a local Playwright Chromium | A job runs on muse, `--login`, `--list-chats` | Browser session in the Muse profile directory (`IMAGE_GEN_MUSE_PROFILE`) | Prompt, reference images; optional proxy from `HTTPS_PROXY` / `https_proxy` |
| `lovart.mjs` → `lovart_agent.py` → `lovart_client.py` | `https://lgw.lovart.ai/v1/openapi/...` (or `LOVART_BASE_URL`): `file/upload`, `chat`, `chat/status`, `chat/result`, `project/*`, `mode/*`; then the artifact URLs that Lovart returns | A job runs on lovart | `LOVART_ACCESS_KEY` / `LOVART_SECRET_KEY` from the environment or the file `$HOME/.lovart/env` (`LOVART_ENV`); the access key goes in the `X-Access-Key` header; the secret key only signs each request (HMAC-SHA256) and is never sent | Prompt, the reference files named for the job, project and thread ids |
| `api-image.mjs` | `https://api.openai.com` (`/v1/images/generations`, `/v1/images/edits`) or `https://generativelanguage.googleapis.com` (`/v1beta/interactions`), or `base_url` from `api.json` | A job runs on the optional paid line | `OPENAI_API_KEY` / `GEMINI_API_KEY`, the variable named by `key_env`, or the mode-600 `key_file` from `api.json` | Prompt, reference images, the key as the provider's auth header |
| `check.mjs` | Same CLIs and hosts: `grok models`, `agy models`, `dreamina user_credit`, `scripts/muse-image.py --list-chats`, Lovart `mode/query`, and `GET /v1/models` (OpenAI) or `/v1beta/models` (Gemini) | The user runs the check | Same as the engine it probes. For Codex it only tests that `CODEX_HOME/auth.json` exists | No prompts or images in probe-only mode. The paid-line check sends only the key |
| `smoke.mjs` or `check.mjs --live` | The checks above and the selected engines | The user starts generation smoke | Same credentials as the engine | A fixed red-circle prompt with no references |

`batch.mjs`, `imgtool.py`, `lovart_state.py`, and the other helper modules make no network calls.
Engine CLIs keep their own logins; the scripts never read their contents or copy them. Local files read for
generation: `$HOME/.gemini/antigravity-cli/brain/<conversation>/.system_generated/logs` (the
transcript of the agy conversation this job started, to find its output), `$HOME/.grok/sessions`
(media file names and hashes, to reject a reused image), and `CODEX_HOME/generated_images` (hashes
only). `IMAGE_GEN_SCRIPT_DIR` and `IMAGE_GEN_TEST_SCRIPTS` are test hooks used by the repository
tests only.

## Engines

| Engine | Script | Can do | Aspect ratio | Time per image (generation time only) | Quota |
|---|---|---|---|---|---|
| codex | `codex-image.mjs` | image, reference images | `--aspect`, chosen by the model | ~30 s | Codex plan usage |
| jimeng | `jimeng-image.mjs` | image, edit (≤10 references), text-to-video, image-to-video | `--aspect`, real parameter | 30–50 s | Dreamina credits (~3 per image) |
| grok | `grok-image.mjs` | image, edit, reference-to-video | `--ratio`, real parameter | ~45 s | X / Grok plan usage |
| gemini | `gemini-image.mjs` | image, edit (≤3 references) | `--aspect`, real parameter | 20–45 s | Antigravity (Gemini) quota |
| muse | `muse-image.py` | image, reference images | `--aspect`, written into the task | 1–2 min | Muse weekly limit |
| lovart | `lovart.mjs` | image, reference images | `--aspect`, written into the prompt | ~35 s | Lovart credits |
| api (optional) | `api-image.mjs` | image, edit (OpenAI ≤16 references, Gemini 3 or 14 by model) | `--aspect`, real parameter | ~30 s | pay per image, your own budget |

Each engine script also works on its own (run `.mjs` with node, `.py` with python3). Shared flags:
`--prompt` or `--prompt-file`, `--out <png>`, repeatable `--ref`, `--timeout`; one image per call,
one JSON line, non-zero exit on failure. `batch.mjs` builds these flags from each job: an aspect
ratio only goes to engines that truly support it (jimeng eight ratios, gemini and muse seven, grok
five), jobs with too many references skip engines with a lower limit (jimeng 10, gemini 3, grok 1),
and video only goes to jimeng and grok (only jimeng does video without a reference).

## Engine notes

- **codex**: calls Codex's built-in `image_gen`. Always uses the official OpenAI provider (`-c
  model_provider="openai"`; `--model` defaults to `gpt-6-luna`, `--effort` to `low`), so it still
  works when the local Codex config points at a custom gateway. Runs in the `workspace-write`
  sandbox. Do not pass `--escalate-sandbox` unless the user has agreed, and do not set
  `IMAGE_GEN_SANDBOX_ESCALATE`. A retry leaves `workspace-write` only when the log says the sandbox
  blocked the write and the user has set `IMAGE_GEN_SANDBOX_ESCALATE=yes` for that new attempt. The
  only Codex path generation reads is the `generated_images` subdirectory of `CODEX_HOME`: it lists
  that directory and hashes files so a failed call cannot reuse an older image. It does not open
  auth, config, sessions, or any other file there. See [references/codex.md](references/codex.md).
- **grok**: `grok-image.mjs` is the whole procedure. No `--ref` → text to image; `--ref` → edit
  (keeps the source aspect ratio); `--video --ref` → 6 s 720p video (`--out` must be .mp4, `--ratio`
  cannot be auto). The first attempt uses the workspace sandbox and `dontAsk`, scoped to the
  job's imagine tool and `Write`. A tool refusal fails closed; it does not automatically retry
  with `--always-approve`. Set `IMAGE_GEN_GROK_MODE=legacy` to opt in to those flags inside the
  workspace sandbox. Both modes deny Bash, WebFetch, and WebSearch. `auto` and `scoped` use the
  same allowlist. Success JSON reports the mode in `grok_mode`.
  Video needs Grok data sharing set to Opt in; on a "zero data retention" error, tell the user
  rather than changing the setting.
- **jimeng**: uses the official Dreamina CLI (`dreamina`), which the user installs from the pinned
  binaries in [SETUP.md](SETUP.md). No `--ref` → text to image (2K); `--ref` → edit; `--video` →
  text-to-video without references, or image-to-video from the first reference (default
  seedance2.0fast, 720p, 5 s; change with `--model`). Submit, polling and download go through
  `scripts/jimeng.mjs` for those image and video commands only. That wrapper accepts `text2image`,
  `image2image`, `image_upscale`, `text2video`, `image2video`, `frames2video`, `multiframe2video`,
  and `multimodal2video`, plus the prompt, ratio, resolution, image, and model flags those commands
  need. It rejects every other Dreamina command, including login and account commands. If a model
  returns `AigcComplianceConfirmationRequired`, the user must authorize it once on the Dreamina
  website.
- **gemini**: uses the Antigravity CLI's (`agy`) built-in `generate_image`, called by its
  image-generator subagent. `--aspect` accepts 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9. Output includes
  `tool_prompt` and `prompt_verbatim`; `false` means the subagent rewrote the prompt, so mention it
  when delivering. A long prompt clipped in the session log does not discard an image that was
  generated; the script reads the full session transcript when Antigravity wrote one beside the log.
- **muse**: Muse has no API, so the script drives its own headless browser in one pass: open a side
  chat, send the task, wait, download from the cloud computer's file library, then delete that side
  chat. The browser profile is the directory named by `IMAGE_GEN_MUSE_PROFILE`, or
  `$HOME/.config/imagegen-swarm/muse-browser`. That directory is created only when the user runs
  `scripts/muse-image.py --login`. That login waits at most one hour for the composer
  (`LOGIN_WAIT_MS`), above the 15 minute generation default. Generation and `--list-chats` do not create it. Renaming the
  side chat is best-effort: if the current side-chat row cannot be identified, or the rename dialog
  fails or times out, the script logs one warning, closes any dialog, and keeps generating. It does
  not rename a row it cannot prove is this side chat. It deletes a side chat only when this run
  recorded that chat's id, on success and on failure. If the id was never recorded, it does not
  delete any chat. If deleting the side chat fails after the PNG is saved, the job still succeeds
  (exit 0) and the success JSON gains a `warnings` list; the key appears only when cleanup produced a warning.
  Generation failures still exit 1. Before Muse is started, batch creates the output directory and uses its real
  path, and `muse-image.py` creates that file's parent again. A relative `--out` is resolved against
  the current working directory, like the other engine scripts (before 1.3.4 Muse resolved it
  against `$HOME`); `~` still means the local home. The cloud directory is
  `/home/hatch/workspace/imagegen-swarm`, or `/home/hatch/workspace/image-gen` when the legacy browser
  profile is selected. `IMAGE_GEN_MUSE_REMOTE_DIR` overrides it with an absolute directory under
  `/home/hatch/`, using only letters, digits, underscores, dots, slashes and hyphens and containing no
  `..`. Create the directory first on a new environment or handle its creation approval
  manually. The script never auto-approves directory creation. Default and `legacy` accept
  an `Allow once` text card only when every parsed path identifies this run's exact PNG
  and the card passes the command and metacharacter checks. `IMAGE_GEN_MUSE_APPROVAL=strict`
  requires a fully decoded single-image save. The live extractor currently returns
  `request: null`. A refused card stops the job without a click.
  See [references/muse.md](references/muse.md).
  Ask the user before approving a stopped request. `IMAGE_GEN_MUSE_PROFILE` must resolve
  under `$HOME/.config/imagegen-swarm` or be the legacy default
  `$HOME/.config/image-gen/muse-browser`. Anything else is refused. One process at a time can use
  the browser. An existing profile in the previous `image-gen` folder is still used until the user
  moves it.
- **lovart**: An existing `lv` wrapper takes precedence over the bundled `lovart_agent.py`.
  The script queries billing before generation. Pass `--require-free` to require unlimited mode and a
  whitelisted model. Without `--require-free`, a mode or model that spends credits
  triggers a warning and generation proceeds with credits. Lovart JSON includes `auth` and `billing_mode`. HTTP calls
  are in `scripts/lovart_client.py` and the local project list is in `scripts/lovart_state.py`,
  split from the readable v1.1.1 client so each file stays small enough to review. It opens a fresh
  thread every call (concurrent jobs on one thread return 409). A passing `query-mode` does not
  prove there are credits. Default model `generate_image_nano_banana_pro`; change it with `--model`.
  If the client reports a pending confirmation, stop and ask the user; do not confirm a charge
  yourself. A chat waits at most one hour (`MAX_CHAT_SECONDS` in `scripts/lovart_client.py`), above
  the 300 second batch default; a shorter `--timeout` is left as given. During an image call, if the remote project's current name is empty, `Untitled`, or a
  short prefix of the project id, the client renames that project to the first 30 characters of
  the prompt. A project that already has another name is left unchanged. `project-add` and
  `project-rename` update `$HOME/.lovart/state.json` and, when access keys are present, also send
  a rename to Lovart. Do not run those two commands unless the user asked to add or rename that
  project. Image generation does not pass them. It uploads only the reference files for that call.
  See [references/lovart.md](references/lovart.md).
- **api**: `provider` is `openai` or `gemini`. openai calls `/v1/images/generations`
  (`/v1/images/edits` with `image[]` when there are references); point `base_url` at any
  OpenAI-compatible gateway to use it instead. `gpt-image-1`, `gpt-image-1-mini` and `gpt-image-1.5`
  only do 1:1, 3:2 and 2:3; from `gpt-image-2` on, the size is computed from the ratio (about 1.57
  MP, multiples of 16, no more than 3:1). gemini calls `/v1beta/interactions` with the ratio and
  `image_size` in `response_format`. The key comes from an environment variable (`OPENAI_API_KEY` /
  `GEMINI_API_KEY` by default, change with `key_env`) or a `key_file` with mode 600, never from the
  config itself. 401/403, 402, exhausted quota or budget shut the line down; a plain 429 backs off.
  The ledger records confirmed returned images at the price you configured, including discarded
  images; unknown failures are reserved only within the current batch. Your provider's bill is the real
  number. Reference limits for the paid Gemini line match the model: `gemini-2.5-flash-image`
  takes 3, and later Gemini image models take 14, unless `max_refs` in the config says otherwise.

Every engine checks that the returned image is new from this run and differs from the reference
images after decoding, and converts non-PNG output to PNG.

## Series mode

Series mode is off by default. Never enable it automatically. When planning a batch, a clear signal
means the user mentions the same character, the same brand, the same mascot, a set of covers, or a
series, OR every task shares the same style reference image. On that signal, first ask one sentence:
“Should this batch share one style? If so I'll turn on series mode.” / “这批要统一风格吗？要的话我打开系列图模式”。
Enable it only if the user agrees. Otherwise leave generation unchanged. Without a clear signal,
do not remind them; for example, 50 font images in different styles need no reminder.

After agreement, write `series.style` from the user's own style description and put the shared
reference image(s), if supplied, in `series.ref`. Do not invent a style for them. Each job's prompt
still describes its subject. The default queue does not lock a style, and mixing engines makes
that drift more likely.

The CLI has a narrower informational hint: if there is no `--series` flag, the jobs file has no
`series` key (a plain array counts as no key), there are at least 4 jobs, and every job has the same
non-empty reference list, batch emits exactly one bilingual `series_hint` JSON event to stderr.
Reference paths use `path.resolve` relative to the jobs file; lists must match in order and
duplicate count. Symlinks are not resolved, and prompts are not compared. Empty path strings do
not qualify. Any explicit `series` value, including `false` or `null`, suppresses the hint.
The final summary and `out/batch-results.json` include `series_hint: true` only when a hint was
emitted; otherwise the field is omitted. This hint never enables series mode, prompts, or waits,
and does not change engines, provider calls or arguments, environment, or exit codes.

After the user agrees, turn it on with `--series`, or with `"series": true`, a `series` object, or a style string in the
jobs file. The job `prompt` stays the subject. Do not copy the style guide into every prompt. Batch
appends the same style guide to every image and video prompt, for every engine:

```
STYLE GUIDE (apply to every image in this series; do not change the subject):
<the style text>
```

```bash
node scripts/batch.mjs --jobs jobs.json --out out/ --series --style-file style.txt --style-ref anchors/hero.png
```

This command generates each job through the engine queue and appends the style guide from
`style.txt` to its prompt. It scores each returned image locally against `anchors/hero.png`
(method `auto`, see below), with no network call for scoring.
Low-score images are discarded and requeued up to `max_retries`. Every charged paid image
counts toward both the batch and month caps, even if discarded. Before a redo, both caps are
checked again. If another paid image would exceed either cap and no subscription engine can
take the job, the redo stops and the job is reported as stopped by the paid budget.

```json
{
  "series": {
    "style": "the same illustrated heroine, flat gouache, muted teal and cream, thick ink outlines, no text",
    "ref": ["anchors/hero.png"],
    "threshold": 0.72,
    "method": "auto",
    "max_retries": 2,
    "engines": ["jimeng", "gemini"],
    "prefer": "consistent"
  },
  "jobs": [
    {"id": "cover-1", "prompt": "the heroine at a rainy window", "aspect": "3:4"},
    {"id": "cover-2", "prompt": "the heroine on a night train", "aspect": "3:4"}
  ]
}
```

`ref` paths are relative to the job file. A sample file lives in the git repository at
<https://github.com/Ekko237/imagegen-swarm/blob/main/examples/series.jobs.example.json>; it is not part of the
installed skill.

Style reference images are placed in front of the job's own references, and only as far as that
engine's limit (Jimeng 10, Gemini 3, Grok 1; Codex, Muse, and Lovart take the references they are
given; the paid line uses its configured limit). A video job does not take a style image, because
that slot is the motion source. When the slot is already full, that engine gets the style text
only. The first time this happens, the log has `style_text_only` (no style image attached) or
`style_refs_partial` (some of the style images attached). The summary lists those engines.

After an engine writes an image, batch scores it locally (`imgtool.py style`), with no network
call. The method (`series.method` or `--style-method`) is one of:

| Method | Needs | What it compares |
|---|---|---|
| `auto` (default) | — | `clip` when its optional backend is installed, otherwise `structure`. Chosen once per batch; the log line `lanes` and the summary show the method used and why |
| `structure` | Pillow | 0.4 × grayscale SSIM + 0.5 × a 4×4 grid of gradient-orientation histograms (HOG-like) + 0.1 × the palette score, at 64×64. Layout, linework and rendering |
| `clip` | numpy, onnxruntime and a CLIP ViT-B/32 ONNX file the user installed (SETUP.md, Series consistency) | cosine similarity of CLIP image embeddings. Closest to "same subject" |
| `palette-histogram` (or `palette`) | Pillow | the 1.3.x score: 0.8 × cosine of an 8-bin RGB histogram + 0.2 × cosine of a 4×4 luminance grid |

Never download the CLIP model, or install numpy or onnxruntime, for the user. If they ask for the
clip method, point them to SETUP.md and let them do it. An explicit `clip` request without the
backend stops before any engine starts; `auto` falls back to `structure`.

Every score is from 0 to 1 and the default threshold is 0.72 for every method (`--style-threshold`
or `series.threshold`). `structure` and `clip` are calibrated so that 0.72 is each one's measured
operating point; `palette-histogram` is unchanged. Measured on 4,947 labeled real-image pairs
(docs/series-consistency-validation.md in the git repository), at 0.72:

| Method | Different subjects kept | Same subjects rejected | AUC |
|---|---:|---:|---:|
| `palette-histogram` | 6% | 76% | 0.69 |
| `structure` | 31% | 26% | 0.79 |
| `clip` (int8 model) | 11% | 10% | 0.96 |

The palette score rejected most real same-subject pairs and could not tell two different subjects
with the same colors apart. `structure` is a coarse layout screen; it cannot tell two characters
drawn by the same artist apart. `clip` is the only one that tracks the subject, and it is still
wrong about one time in ten.

With style reference images, every output is scored against each reference and the highest of
those scores is used. With text only, the first kept image becomes the visual anchor and is not
scored. Later images are scored against that file.

A score below the threshold deletes the file and queues the job again, up to `max_retries` (default
2, `--style-retries`). Those discards are `keep.style_redos`, including a last discard that is not
queued again. The job then fails. The same engine may run the redo. While `prefer` is
`consistent` (the default), a lane leaves the job for the engine with the highest mean score so
far when that engine has a free lane. `engines` (`--series-engines`) limits the series to that
list. `prefer: "off"` keeps the full swarm and still screens.

`elapsed_seconds` stays generation time. `delivery_seconds` is the wall clock through the summary,
including style screening and style redos. Both are on the summary line and in
`out/batch-results.json`, with each kept image's `style_score` (calibrated), `style_raw_score` and
`style_components` (for `structure`: `ssim`, `hog`, `palette`; for `clip`: `clip_cosine`; for
`palette-histogram`: `histogram`, `luminance_grid`). Redo events and failed jobs carry the
components too. The summary's `series` has `method` (used), `method_requested`, `method_reason`
when `auto` decided, `components` (the weights) and `threshold`.

No method guarantees the same face, character, or logo. Look at every kept image before
delivering it. An output that already exists is skipped and is not scored. Grok and Jimeng treat a
reference as an edit, so one style reference turns a text-to-image call into an edit. A Grok edit
keeps the source aspect ratio.

| Option | Jobs file | CLI | Default |
|---|---|---|---|
| style text | `series.style`, or `series` as a string | `--style` or `--style-file` | required when series mode is on |
| reference images | `series.ref` | `--style-ref`, repeatable | none |
| threshold | `series.threshold` | `--style-threshold` | 0.72 |
| method | `series.method` | `--style-method auto`, `structure`, `clip`, or `palette-histogram` | `auto` |
| retries | `series.max_retries` | `--style-retries` | 2 |
| engines | `series.engines` | `--series-engines` | every engine in this batch |
| routing | `series.prefer` | `--series-prefer consistent` or `off` | `consistent` |

## When no script engine can take the image

If the api line is configured, in this batch's engine list, and has budget left, `batch.mjs` already
uses it when the job names `api` or when no enabled subscription engine can take the image.
Otherwise, generate in the ChatGPT, Gemini or Grok web app in a new browser tab, download and check
the image, then close the tab. An engine error is different from running out of quota; if the engine
the user named fails, report it instead of switching to the web.

## Checks

- `node scripts/check.mjs`: current login probes and recent smoke readiness of all seven routes.
- `node scripts/smoke.mjs --engines <list>`: test selected routes one at a time with one square PNG.
  `--timeout <seconds>` caps each engine (default 300). Progress prints as each row runs.
  The run folder keeps `SMOKE_TABLE.txt` after a timeout or SIGINT/SIGTERM.
  Confirm Muse billing before selecting it. Jimeng and the paid API are skipped by default.
  Lovart's default smoke requires unlimited mode and the whitelisted default model.
  With the api line configured, it checks the key against the free model-list endpoint and shows
  this month's spend and budget.
- After changing a script, run `node tests/reliability.test.mjs`, `node tests/series.test.mjs` and
  `node tests/series-consistency.test.mjs` from the git repository first (no paid images; series
  tests use mock engines, procedural images and six small licensed fixtures). `reliability.test.mjs` runs `batch.mjs` for real to check when the paid line does and
  does not take an image. Those tests are not part of the installed skill.
- Look at every image before delivering it; sample frames from videos.
- The fixed image tasks live in the git repository at `tests/evals/`, not in the installed skill.
  `node tests/evals/run.mjs <outdir> [--only id,id]` checks status, aspect ratio, prompt passthrough
  and Muse cleanup; a judge scores each image 1–5 using the rubric in `tests/evals/evals.json`.
  `api-t2i` and `api-edit` cost real money each run, so ask the user first; they are skipped when
  the api line is not configured.
