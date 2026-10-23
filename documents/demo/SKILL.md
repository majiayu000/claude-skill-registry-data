---
name: demo
description: Run analyzer View commands against realistic synthetic data in moto or a fake Bedrock (no AWS account needed) and show exactly what a user would see, as text and optionally as the notebook HTML. Use to check how a new or changed report reads, to reproduce an output bug, or to prepare pages for the docs screenshots.
argument-hint: "<service> [python to run, e.g. ui.summary(\"s3://demo-lake/\")] [--html path] [--theme light|dark]"
allowed-tools: Bash(.venv/bin/python .claude/skills/demo/demo.py:*), Bash(python .claude/skills/demo/demo.py:*)
---

# Demo

`demo.py` starts moto, fills it with demo data built to set off most findings, builds the service's View in
text mode, and runs the Python you pass. `ui`, `core`, `mod` and the module under its own name (`s3`,
`dynamodb`, `bedrock_kb`) are in scope. moto has no Bedrock, so for `bedrock_kb` the seeder also hands the
analyzer fake Bedrock clients (see "Bedrock" below).

```bash
.venv/bin/python .claude/skills/demo/demo.py s3 'ui.summary("s3://demo-lake/")'
.venv/bin/python .claude/skills/demo/demo.py dynamodb 'ui.scan("orders", where={"status": "failed"}); ui.more()'
.venv/bin/python .claude/skills/demo/demo.py dynamodb 'ui.table_info("sessions")' --html <scratchpad>/t.html --theme dark
.venv/bin/python .claude/skills/demo/demo.py s3 'print(core.summarize("s3://demo-lake/raw/").object_count)'
.venv/bin/python .claude/skills/demo/demo.py bedrock_kb 'ui.use("support-docs"); ui.ask("How long do refunds take?")'
```

Arguments: `$ARGUMENTS`. The first word is the service. The rest is the code to run, plus any flags. If only a
service is given, run a short tour:

- s3: `ui.overview(); ui.bucket_info("demo-lake"); ui.summary("s3://demo-lake/")`
- dynamodb: `ui.tables(); ui.table_info("orders"); ui.schema("orders")`
- bedrock_kb: `ui.kbs(); ui.use("support-docs"); ui.kb_info(); ui.search("How long do refunds take?"); ui.files();
  ui.file("warranty.pdf")` (the explorer window needs a browser: see `kb_explorer_shots.py`)
- bedrock_chat: `ui.use("support-docs"); ui.ask("How long do refunds take?"); ui.settings(); ui.request();
  ui.ask_all(["How long do refunds take? | refund-policy.pdf", "What does error E1234 mean?"]); ui.code()` (the same
  fake Bedrock as bedrock_kb, which also streams answers; the window itself needs a browser: see `chat_shots.py`)
- sagemaker_env: `ui.instance(); ui.disk(); ui.running(); ui.envs()`
- opensearch: `ui.overview(); ui.indexes("vectors-prod"); ui.index_info("vectors-prod/support-docs");
  ui.search("how do I get my money back?", index="vectors-prod/support-docs")`
- lambda_functions: `ui.functions(regions="all"); ui.function_info("orders-etl"); ui.errors("orders-etl");
  ui.performance("orders-etl")` (the explorer window needs a browser: see `lambda_explorer_shots.py`)
- agent: `ui.ask("Which Lambda failed in the last 24 hours?"); ui.tools()` (a scripted stand-in for the model, on the
  Lambda data: see `--help`)
- other services: `ui.help()` and then the service's overview command

`--help` describes the demo data. Most useful:

- **S3**, bucket `demo-lake` (versioned):
  - `raw/events/` has about 1,000 small files, and `raw/backfill/` duplicates a week of them.
  - `curated/` has parquet files and `customers.csv` with metadata and tags.
  - `exports/` holds one of those parquet files uploaded again in parts: same content, different ETag.
  - `logs/app/` is 1–3 years old, `archive/` is in GLACIER, and `reports/monthly/` holds small STANDARD_IA files.
  - `reports/` also holds an overwritten file and 3 deleted ones.
  - `tmp/` has an unfinished multipart upload.
  - The bucket policy shares `curated/` with another account.
  - Buckets `demo-models` (holding a `model.tar.gz`) and `demo-scratch` (empty) are also there.
- **DynamoDB**:
  - `orders` has pk/sk, the GSI `by-status`, USER#/ORDER# keys, nested maps, sets, one mixed-type attribute,
    empty strings and a ~330 KB item.
  - `sessions` is provisioned far above its seeded CloudWatch usage and has throttles.
  - `counters` has a numeric key.
- **Bedrock** (knowledge base IDs are fixed, so calls can be copied):
  - `support-docs` (OpenSearch Serverless) has two data sources. `docs-s3` reads moto's `support-docs-bucket`
    and has a failed sync, 2 failed documents, 1 ignored one, and two files changed after its last sync.
    `help-center` is a WEB source with semantic chunking, a model parser and the RETAIN deletion policy.
  - `sales-playbooks` was never synced, `hr-policies` doesn't chunk, and `legacy-faq` is FAILED.
  - Retrieval ranks a small corpus of support passages. SEMANTIC matches concepts but not error codes, and
    HYBRID also matches exact words, so `compare("what does error E1234 mean?")` shows a difference.
    `holiday-shipping.md` isn't indexed yet, so a question about it misses in `evaluate()`.
  - `ask()` (the default engine) cites every sentence but the last one, so answers come out partly grounded.
    `engine="converse"` returns exact token counts.
  - `models()` lists Claude, Llama, Nova and Mistral text models, on demand or through `us.` profiles.
- **SageMaker** (moto has no Studio, so the seeder hands the analyzer fake sagemaker / sts / cloudwatch clients and a
  fake machine root):
  - This code "runs" in the JupyterLab space `churn-analysis` on an `ml.g5.2xlarge`: 2 days up, idle GPU, a domain
    without idle shutdown, and a home volume 88% full with Jupyter trash, a Hugging Face cache, checkpoints and
    year-old parquet files (sparse files, so nothing big is written).
  - `running()`: notebook instances `old-experiment` (9 days, no auto-stop) and `team-reporting` (auto-stop), stopped
    `archive-2024` and `sandbox`, a Code Editor app in space `forecasting`, endpoints `churn-v1` (no traffic),
    `churn-v2` (busy) and a serverless one, and a spot training job.
  - `envs()`: the image's conda (`/opt/conda`, with mamba), `scratch` made in `/opt/conda/envs` since the app started
    (it goes when the app stops), `py310` in `~/.conda/envs` with its kernel, and a kernel whose environment is gone.
    `new_env("3.11")` "makes" an environment without downloading anything (the seeder replaces `_run`).

- **OpenSearch** (moto for the domains; fake Serverless, CloudWatch and Bedrock, and fake clusters from
  `tests/fake_opensearch.py` behind each endpoint):
  - `vectors-prod` holds `support-docs` (faiss, cosine, 1,024 dims, 1.8M documents reported, 1.5% without a vector,
    a few repeated passages, graphs bigger than the nodes' k-NN memory), `product-search` (lucene), `legacy-faq`
    (nmslib, inner product, unnormalized vectors) and `app-logs-2026.10` (no vectors).
  - `search-legacy` is Elasticsearch 7.10 and open to the internet; `rag-dev` runs on one t3.medium.
  - Serverless: `kb-support` (a Bedrock knowledge base's index), `kb-sandbox` (no standby replicas) and `app-logs`
    (VPC only).
  - The embedding model knows four topics (refunds, shipping, accounts, billing), so a question about one of them
    finds its articles.
- **Lambda** (moto for the functions, triggers, CloudWatch numbers and logs; the seeder hands the analyzer Lambda and
  Logs clients that answer what moto lacks: account limits, provisioned concurrency, reserved concurrency, log sizes,
  and the deployment packages):
  - us-east-1: `orders-etl` (python3.9, SQS and S3 triggers, errors rising for three days, a run near its 60 s
    timeout, KeyErrors, AccessDenied and timeouts in its last 24 hours of logs, logs costing more than its compute and
    kept forever, a `.env` file and bundled boto3 in its package), `churn-scoring` (arm64, EventBridge, 4 copies of
    provisioned concurrency it never needs), `report-api` (nodejs20.x, a public function URL, throttled at reserved
    concurrency 10, and logging JSON for its last three hours: a WARN now and then, three unhandled TypeErrors),
    `feature-backfill` (python3.10, never called, no triggers) and `support-agent-actions` (a Bedrock agent's action
    group). orders-etl's cold starts log an INIT_START line.
  - eu-west-1: `gdpr-export` (SQS). `regions="all"` reads every region moto lists.
  - The run `c0ffee00-1d2e-4f3a-9b8c-7d6e5f4a3b2c` is one of orders-etl's KeyErrors.

## Reading the output

This output is what a data scientist sees in the notebook. When you run a demo to review a command, check it
against the product rules in CLAUDE.md:

- Does the answer come first?
- Are all values in human units?
- Does every finding name a next step?
- Do the Next calls use this report's real arguments, and do they run as written?
- Are estimates and partial results labelled?

Say what you'd change, with the line of output that shows it.

moto is not real AWS. Don't report these as bugs:

- table sizes show as 0 B
- S3's CloudWatch sizes are approximate
- timestamps show "just now" unless the seed backdates them
- IAM isn't enforced, so a missing-permission path can't be shown here (tests cover it with a stubbed error)
- Bedrock's scores, answers and latencies come from the fake clients, not from a model. Judge how they're
  presented, not the retrieval quality. The fake checks each request against botocore's service model, so a
  malformed call still fails as it would against AWS.

## HTML and screenshots

`--html PATH` also writes the notebook rendering of every report to a standalone page. Put it in the scratchpad
unless the user names a place, and give them the path. `--theme light|dark` sets the page theme, and `--look NAME`
the reports' theme (`set_theme`'s names: console, the default, soft, editorial, brand, classic). The
docs screenshots are `docs/images/<command>-{light,dark}.webp` (Bedrock's are `bedrock-<command>-...`).

`shots.py`, next to `demo.py`, makes them: for every figure in the guides it runs the figure's command against
a scene in moto, renders the notebook HTML, screenshots it in headless Chrome (984 CSS px wide at 1.5x, so
1476 px), trims the empty space below, writes the light and dark WebP and sets the `height=` of both images
in the guide's Markdown. It needs Pillow (`pip install pillow`) and Chrome (`$CHROME`, or Playwright's headless shell).

```bash
.venv/bin/python .claude/skills/demo/shots.py --list                 # every figure and the command behind it
.venv/bin/python .claude/skills/demo/shots.py summary what-if        # remake these
.venv/bin/python .claude/skills/demo/shots.py                        # remake all of them (about 2 minutes)
```

The S3 and DynamoDB scenes are the "acme" ones the guides are written around (`acme-ml-data`, `acme-app`),
at production scale: moto holds the files a figure opens, and the scene adds the listing, CloudWatch numbers and
DescribeTable counts around them. Bedrock's figures use `seed_bedrock_kb()`. After remaking a figure, look at it,
and check that its caption and `alt` text in the guide still say what it shows (counts in them come from the
scene). A new figure goes in `FIGURES` in `shots.py` and in the guide as a `<figure>` like the others.

The S3 explorer (`s3_explorer.py`) is a live ipywidgets app, not a report, so `shots.py` can't draw it.
`explorer_shots.py` starts JupyterLab in a temporary folder, runs the explorer on the acme scene, clicks its buttons
when a figure needs that, and screenshots it the same size, light and dark, for `docs/s3_explorer.md`.
`explorer-tour`, the one README shows too, is an animated WebP: a drawn pointer clicks from the list of buckets to a
Parquet file and a Word file. To change what a figure shows, edit its `Figure` and `Step`s in `FIGURES`. The browser
maps the system UI font, which the widgets' buttons use, to Liberation Sans, so the figures come out the same on any
Linux machine. It needs `pip install jupyterlab playwright` on top of the dev requirements:

```bash
.venv/bin/python .claude/skills/demo/explorer_shots.py              # every explorer figure (about four minutes)
.venv/bin/python .claude/skills/demo/explorer_shots.py explorer-tour   # just the animation
```

To click around the explorer yourself, start `jupyter lab` and seed the scene in the first cell the same way
(`mock_aws().start()`, then `core = S3Analyzer(**shots.seed_s3_docs())`, then `S3Explorer(core=core)`).

The chat window (`bedrock_chat/window/`) is ipywidgets, which only draw in a browser connected to a kernel, so its figures
(`chat-*`, in `docs/bedrock_chat.md`) come from `chat_shots.py`: it starts JupyterLab on a notebook that opens the
window on the fake Bedrock, types and clicks through it with Playwright, and writes the WebP files and the figures'
heights the same way. It needs `pip install jupyterlab playwright` on top of the dev requirements, and Chromium (`$CHROME`, or
Playwright's).

```bash
.venv/bin/python .claude/skills/demo/chat_shots.py                   # every chat figure, light and dark
.venv/bin/python .claude/skills/demo/chat_shots.py chat-request      # just this one
```

The knowledge base explorer (`bedrock_kb/explorer/`'s `explore()`) is ipywidgets too, so its figures (`kb-explorer*`, in
`docs/bedrock_kb.md`) come from `kb_explorer_shots.py`, which works like `chat_shots.py` and reuses its plumbing: it
opens the window on support-docs, clicks warranty.pdf and one of its chunks, asks it a question, opens a failed file,
searches, and opens the Syncs tab. `--out <folder>` writes PNGs there instead, to look at them first.

```bash
.venv/bin/python .claude/skills/demo/kb_explorer_shots.py                     # every explorer figure, light and dark
.venv/bin/python .claude/skills/demo/kb_explorer_shots.py kb-explorer-chunks  # just this one
```

The Lambda explorer (`lambda_functions`' `explore()`) works the same way: `lambda_explorer_shots.py` opens it on
demo.py's Lambda functions, reads the Functions tab, opens orders-etl's Overview (scrolled to how it's wired), its Logs
over the last 24 hours with a failed run open, searches them for AccessDenied, opens the Errors and Code tabs, and
picks report-api for its JSON logs. Its figures are `lambda-explorer*`, in `docs/lambda_functions.md`.

```bash
.venv/bin/python .claude/skills/demo/lambda_explorer_shots.py                       # every figure, light and dark
.venv/bin/python .claude/skills/demo/lambda_explorer_shots.py lambda-explorer-logs  # just this one
.venv/bin/python .claude/skills/demo/lambda_explorer_shots.py --out /tmp/look       # PNGs to look at, docs left alone
```

## Real AWS

Use `--live` (with optional `--region` / `--profile`) only when the user explicitly asks for it. It runs against
their real account with their credentials. The analyzers are read-only, but scans and reads are billed, so say
what the command will read before you run it.

## Adding demo data

A new command often needs data that sets off its findings. Add it to `seed_<service>()` in `demo.py`:

- Keep it deterministic (`random.Random(7)`) and small, so the demo runs in a few seconds.
- Backdate S3 objects with `put(..., age_days=N)`.
- Update the module docstring's list of demo data.

A new analyzer needs its own `seed_<service>()` and an entry in `SEEDERS`.
