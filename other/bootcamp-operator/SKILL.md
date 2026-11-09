---
name: bootcamp-operator
description: Explains how to drive the DataStream Corp bootcamp CLI (`uv run bootcamp.py ...`) as a participant — Phase 1 task scripts, Phase 2 stages with `up N`, redeploying edited code with `deploy`, `test [N]` / `test --only N`, `status`, `invoke` (`--actor`, `--stream`, `--local`), `traces`, `scores`, `eval`, `memory`, `tools`, `token`, `llm`, `doctor`, `down`, `forget`, `--verbose`, how long each step takes, what `[CHALLENGE]` lines mean, and where the runtime logs live. Triggers on "how do I run phase 1", "how do I run t3", "what does up 4 do", "how do I get to stage N", "I fell behind", "catch up", "I edited agent.py, now what", "how do I redeploy", "what does status print", "where are my logs", "aws logs tail", "show my traces", "eval scores", "how long does up take", "what does SKIP mean", "[CHALLENGE]", "--verbose", "how do I talk to my agent", "how do I tear down", "clean up my resources", "what's my workflow". Do NOT use for diagnosing a failed `test` line or an error message (use bootcamp-debugger), for writing agent code (use agent-feature-builder), MCP tools (use mcp-tool-author) or calling the LLM from your own scripts (use litellm-usage).
---

# Bootcamp Operator

This skill drives one entry point, `bootcamp.py`, always run with `uv run`
from the folder that holds it (the root of your participant clone). Every command assumes your
participant role `bootcamp-participant-<PARTICIPANT>` (tag-isolated) from
the base `AWS_PROFILE` in `.env`, so you never pass credentials yourself.
The platform (instructor) owns the account, the LiteLLM gateway and the
Terraform; you own the code under `phase1/` and `phase2/app/`.
The gateway runs 08:00-22:00 Israel time (Asia/Jerusalem) every day: outside
that window every model call (Phase 1 scripts, `llm`, `doctor`, Phase 2 `test`/`invoke`)
answers `503`, so plan your work inside it.

## One-time setup

```bash
uv sync                     # in your clone (the folder with bootcamp.py)
cp .env.example .env        # Windows: copy .env.example .env
```

`.env` keys: `PARTICIPANT` (your roster name; ships blank, required), `AWS_PROFILE`
(the profile holding your IAM user's access key; ships as `bootcamp`, the profile from
`aws configure --profile bootcamp`; blank = environment-variable credentials), `BOOTCAMP_REGION`
(default: `AWS_REGION`, then `us-east-1`), `MODEL_ID` (optional: a model from
`uv run bootcamp.py llm models`; empty = class default). Leave `BOOTCAMP_ROLE_ARN` empty. Optional (stage >= 4,
default `false`): `ENABLE_CODE_INTERPRETER=true` gives the agent a `run_python`
tool, `ENABLE_BROWSER=true` a `browse_web` tool (AWS-managed AgentCore sandboxes),
`ENABLE_GUARDRAILS=true` a Bedrock Guardrail (prompt-attack filter, email/phone
masking, tool-output screening); apply with `deploy`. Optional experiments,
also applied with `deploy` (re-applies your current stage):
`GUARDRAIL_PROMPT_ATTACK_STRENGTH` (`NONE|LOW|MEDIUM|HIGH`, default `MEDIUM`)
and `GUARDRAIL_PII_TYPES` (default `EMAIL,PHONE`, or `none`), both need
`ENABLE_GUARDRAILS=true`; `MEMORY_EPISODIC=true` (stage >= 3) adds an
`Episodes` memory strategy; `TRUST_ACTOR_HEADER=true` is the deliberately
insecure Task 4 experiment (agent trusts an actor header, stage 4 checks
WARN instead of FAIL): set it back to `false` and `deploy`. Then:

```bash
uv run bootcamp.py doctor   # pre-flight before day 1: tools, .env, role, gateway call, budget, network (creates nothing)
uv run bootcamp.py llm      # proves role assumption + gateway; prints URL, models, budget
```

## Command reference

| Command | What it does |
|---|---|
| `phase1 tN ["prompt"] [--starter] [--session NAME]` | Runs the reference solution `phase1/tN_*.py` with your role creds + `LITELLM_BASE_URL`; with `--starter` it runs your challenge file `phase1/starter/tN_*.py` (where you do the Phase 1 work). t3/t4: `--session NAME` saves the chat under that session id (a new name starts fresh; the run prints `[session] ...`). No prompt = interactive chat (`quit` to exit). `t0` downloads your local DB copy and checks AWS + gateway. Prints `[tool] name: input` per tool call (`PHASE1_SHOW_TOOLS=0` hides) and a `[budget] $x of $y used ...` line after the run (`PHASE1_SHOW_BUDGET=0` hides; warns at 75 %). |
| `doctor` | Pre-flight before day 1 (seconds, creates nothing, exit 1 on any `✘`): OS, Python, uv, Terraform >= the participant stack's `required_version`, AWS CLI v2, disk; your AWS login, `PARTICIPANT`, assuming `bootcamp-participant-<you>`, your gateway secret, one tiny LiteLLM call and your remaining budget, direct Bedrock denied (expected), and HTTPS reachability of Cognito, api.weather.gov and GitHub. Each failure prints a `fix:` line. |
| `llm` | Gateway URL, allowed models, your `MODEL_ID`, `$spent of $budget`. |
| `up N` | Builds zips (stage >= 1: MCP server, >= 2: weather Lambda, >= 4: agent, >= 6: evaluator Lambdas), `terraform apply` for stages 0..N, then smoke-tests stage N only. A lower N switches later stages **off**. `--skip-test` skips the check. |
| `deploy` | Re-applies at your **current** stage: rebuilds zips whose sources changed and rolls the runtimes; after an MCP change it also re-syncs the Gateway's tool list (~10-20 s). Also picks up a new `MODEL_ID` and the `ENABLE_CODE_INTERPRETER` / `ENABLE_BROWSER` / `ENABLE_GUARDRAILS` flags. Does not run tests. |
| `test [N]` | Checks every stage 0..N (default: current stage). `test --only N` runs one stage. |
| `status` | Prints `KEY=value` ids: `STAGE`, `POOL_ID`, `MCP_RUNTIME_ID`, `GATEWAY_ID`, `GATEWAY_URL`, `MEMORY_ID`, `AGENT_RUNTIME_ID`, `AGENT_LOG_GROUP`, `POLICY_ENGINE_ID`, ... (client secret hidden). Prints `No stack provisioned for '<name>' ...` when nothing is up. |
| `invoke "prompt" [--actor X] [--stream] [--session last\|ID] [--json]` | Calls your deployed agent as a signed-in Cognito user: usually 20 s-2 min, up to ~5 min (then it gives up). `--actor` defaults to `alice-chen` (story users `alice-chen` / `jordan-lee`; any other name creates a test user; the pages use fresh ones such as `trace-test` (Task 5), `online-eval` (Task 6) and `mallory` (guardrail attacks) so old memories don't skew results). `--stream` prints the answer as it is generated, tool calls inline. Omit `--session` for a fresh session (its id is printed to stderr); `--session last` reuses your previous invoke's warm session (faster, keeps the conversation). Prints the answer plus one compact `key: value` line per extra reply field (`actor_id`, `memories`, `tools_used`); `--json` prints the raw reply. |
| `traces [SESSION_ID] [--hours H] [--args]` | Span tree (name, duration, tokens) of your latest `invoke` on this machine, or the given session. `--args` adds each tool call's input (e.g. the SQL sent to `query_db`). Stage 5+; spans arrive 2-10 min after an `invoke`. |
| `scores [--hours H] [--limit N]` | Your recent online-evaluation results: time (UTC), evaluator, score, label, actor (or `test` / the prompt's first words), session. Stage 6+; they arrive 15-30 min after the session goes idle. |
| `eval [--dataset F] [--limit N] [--min-pass R] [--evaluators S] [--variants A,B] [--last]` | Offline evaluation (stage 4+, Task 6 Part B): syncs `phase2/evals/golden.yaml` (or a `.csv`) to your managed dataset `awsworkshop_<you>_golden` (new version only when the file changed), asks each item in a fresh session/actor, then one AgentCore batch evaluation scores those sessions against the ground truth. Prints `[PASS]/[FAIL]` per item, pass rate, averages, LiteLLM spend, and the judge's reason for failures; exits 1 below `--min-pass` (0.8). ~5-10 min. `--last` reprints the saved run. `--evaluators builtin|custom|all|<name>` adds your stage-6 custom evaluators (`exact_numbers`, and `rubric_judge`: an `evaluators.yaml` rubric graded through LiteLLM, one judge call per item on your budget); `--variants A,B` asks every item once per prompt variant (`phase2/app/agent/prompt_variants.py`) and prints a side-by-side comparison (about twice the time). Limits: at most 25 answers per run (`--limit` x variants) and 50 items in the golden file; the built-in judges bill the class AWS account, not your LiteLLM budget. |
| `memory [--actor X]` | What AgentCore Memory holds for one actor (default `alice-chen`, stage 3+): short-term (newest sessions and their event counts) and long-term (records per strategy namespace: UserFacts, UserPreferences, SessionSummaries). Records appear 1-2 min after a turn. No model calls. |
| `token [--actor X]` | Prints a Cognito M2M bearer token for manual MCP / gateway calls; `--actor X` prints that user's access token instead (what the agent runtime accepts). |
| `tools [--search Q] [--top-k K]` | Your Gateway's tools per target (`DataStreamDatabase`, `Weather`) and their prompt-token cost: every tool vs semantic search; `--search` shows what the Gateway's semantic tool search returns for a need (stage 2+). |
| `down` | `terraform destroy` of everything you own, plus your runtime and evaluation-result log groups, your golden dataset and batch evaluations. |
| `forget [--force]` | After the instructor ran `instructor.py reset <you> --force`: refreshes your local terraform state against AWS (dropping the deleted resources) and deletes your workspace once it is empty; refuses, listing what still exists, otherwise. `--force` deletes the workspace without checking (only when the instructor confirmed your stack is gone). Then start again with `up 0`. |

Global flags work anywhere on the command line: `--confirm`
(`uv run bootcamp.py up 4 --confirm`) to review the Terraform plan, and
`--verbose` (or `BOOTCAMP_VERBOSE=1`) for the full Terraform output and debug
logs. By default output is summarised, with progress lines and the expected
duration up front.

Usual durations: `up 0` ~6 min (includes ~5 min Cognito DNS wait), `up 1`
~1.5, `up 2` ~1, `up 3` ~11, `up 4` ~5.5, `up 5` ~0.5, `up 6` ~1, `up 7` ~4.5
(policy engine), `deploy` ~1.5 (up to ~10 while the runtime is still updating),
`down` ~10.5 min (source: `bootcamp_cli/progress.py` `EXPECTED_MINUTES`);
`invoke` usually 20 s to 2 min, up to ~5 min. Each new session cold-starts the
agent's runtime microVM (and every Gateway tool call one for the MCP server),
so use `--session last` for follow-up questions.

## Stages (`up N`)

| N | Adds | `test --only N` checks |
|---|---|---|
| 0 | Cognito pool, scope `datastream/mcp.access`, M2M client, domain, user client + story users `alice-chen` / `jordan-lee` (passwords in SSM) | token issued + story users sign in + keyless LiteLLM identity + direct Bedrock denied (first run waits ~5 min for Cognito DNS) |
| 1 | Code bucket + your DB copy in S3, MCP runtime (`phase2/app/mcp_server`) | `tools/list` + a SELECT (extra no-argument tools must return JSON rows) |
| 2 | Gateway (semantic tool search), OAuth2 credential provider, targets `DataStreamDatabase` (MCP) and `Weather` (Lambda, `phase2/app/weather_lambda`) | `DataStreamDatabase___query_db` listed + SELECT; `Weather___get_us_forecast` answers; semantic search ranks the weather tool first |
| 3 | Memory with `UserFacts`, `UserPreferences`, `SessionSummaries` strategies | memory `ACTIVE` with all three; `[CHALLENGE]` lines: `memories` in the reply, preference recalled (2-5 min, waits for extraction) |
| 4 | Agent runtime (`phase2/app/agent`, user-JWT authorizer) (+ optional Code Interpreter / Browser tools, Bedrock guardrail) | agent answers; identity only from the verified token; fact recalled across sessions, no cross-user leak (up to ~4 min); plus `code interpreter tool` / `browser tool` / `guardrail ...` when enabled |
| 5 | Observability (account-level) | spans in `aws/spans` (WARN only, lags ~10 min) |
| 6 | Online evaluation config + custom evaluators (`exact_numbers` and `rubric_judge` Lambdas, both scoring live traffic) | config and custom evaluators `ACTIVE`; rubric judge scores a sample turn through LiteLLM |
| 7 | Cedar policy engine on the gateway | SELECTs allowed, DELETE denied, disguised writes never run; weather tool still permitted |

Stages 1-4 and 6 also print a challenge line for the Phase 2 extension you add
yourself: `[CHALLENGE] PASS|SKIP|FAIL stage N <name>: <detail>` (1:
`list_tables tool`, 2: `describe_table via the Gateway` and `get_us_alerts
Lambda tool`, 3: `memories in the reply` and `preference recalled`, 4:
`tools_used in the reply`, 6: `your own rubric`). SKIP = not added yet,
never a failure; FAIL = present but broken, and counts toward the exit code.

Fell behind? `up N` lands you at the start of guide task N+1; copy the ids
the guide wants from `status`.

## Typical inner loop (Phase 2)

Phase 2 has no starter files: `up N` deploys a working reference, and each
challenge on the site says which real file under `phase2/` to edit in place
(`git diff` shows the changes, `git checkout -- <file>` resets one), then
`deploy` and the check to run (`test --only N`, `invoke`, `traces`, `eval`).
`phase2/evals/golden.yaml` needs no deploy: `eval` reads it locally.

```bash
# 1. edit phase2/app/agent/agent.py: try it on this machine first (stage 3+, no deploy, seconds per change)
uv run bootcamp.py invoke "How many employees are in Engineering?" --actor alice-chen --local
# 2. ship it (also for phase2/app/mcp_server/mcp_server.py, which has no local mode)
uv run bootcamp.py deploy
uv run bootcamp.py test --only 4      # or --only 1 / --only 2 for MCP changes
uv run bootcamp.py invoke "How many employees are in Engineering?" --actor alice-chen
```

`invoke --local` starts `agent.py` on `localhost:8080` with the runtime's environment (from your stack's
outputs) and your own AWS credentials, against your real Memory, Gateway and model; the first run installs the
agent's packages (~1 min), its output goes to `.build/local-agent/agent.log`, and it stops after the answer. Until
`up 4`, the Task 3 `[CHALLENGE]` checks run the agent the same way.

Every `test` at stage 4 and every `invoke` spends LLM budget — run the
narrowest `--only` you need and check `llm` now and then. Cost depends on the
model. With `gpt-6-luna` or `claude-haiku-5-5`: Phase 1 ~$0.04-0.25, Phase 2 with the
optional pages ~$0.05-0.30 (default budget $5); `claude-sonnet-5-5` ~20x more. On `nova-2-lite` Task 4 is ~$0.04, one
10-item `eval` ~$0.04 for its `rubric_judge`.

Evaluations are the exception: AgentCore's built-in judges (`eval` and the
stage-6 online evaluation, which scores every live request) bill the class AWS
account, not your LiteLLM budget. Run them only through `uv run bootcamp.py
eval` (never AgentCore evaluation APIs via boto3 / the AWS CLI / your own
scripts), keep runs small (default 10, max 25 answers, golden file <= 50 items),
re-run only after a change worth measuring, never in a loop, and don't load-test
your agent. Iterate with `--evaluators exact_numbers` (no model) or
`rubric_judge` (your LiteLLM budget). Without a reference answer (online),
`exact_numbers` fails answers that only promise to look ("Let me route
this..."); other answers without numbers (greetings, preference
acknowledgements) score `N/A`.

## Logs and traces

Start with the CLI, which already runs as your participant role:

```bash
uv run bootcamp.py traces              # span tree of your latest invoke (stage 5+)
uv run bootcamp.py traces <SESSION_ID> # the id `invoke` printed
uv run bootcamp.py traces --args       # plus tool inputs (the SQL actually sent)
uv run bootcamp.py tools               # Gateway tools per target; prompt tokens: every tool vs semantic search
uv run bootcamp.py scores              # online-eval results (stage 6+)
uv run bootcamp.py eval --last         # your latest offline evaluation run
uv run bootcamp.py memory --actor X    # what memory holds for X (sessions + records per namespace)
```

Runtime logs: `/aws/bedrock-agentcore/runtimes/<RUNTIME_ID>-DEFAULT`
(`status` prints `AGENT_LOG_GROUP`; for the MCP server use `MCP_RUNTIME_ID`).
You can read only your own log groups (`/aws/bedrock-agentcore/runtimes/awsworkshop_<name>_*`,
evaluation results `awsworkshop_<name>_*`, vended logs, CodeBuild) plus the
shared `aws/spans` (span names, timings, token counts). AccessDenied on
another participant's log group is by design.

The raw `aws` CLI with your base profile (`bootcamp`) runs as your IAM user
`bootcamp-<name>`, not the participant role, so add a participant-role profile once:

```ini
# ~/.aws/config  (source_profile = your AWS_PROFILE from .env)
[profile bootcamp-<name>]
role_arn = arn:aws:iam::<ACCOUNT_ID>:role/bootcamp/bootcamp-participant-<name>
source_profile = bootcamp
role_session_name = bootcamp-<name>
region = us-east-1
```

```bash
aws logs tail "<AGENT_LOG_GROUP>" --since 15m --follow --profile bootcamp-<name>
aws logs tail "/aws/bedrock-agentcore/runtimes/<MCP_RUNTIME_ID>-DEFAULT" --since 15m --profile bootcamp-<name>
```

Console alternative: AgentCore console → **Observability** → Agent: your
`awsworkshop_<name>_agent` → Sessions / Traces (stage 5+). Other AgentCore pages:
Agents (runtimes), Gateways, Memory, Evaluations, Policy.

## Your data

- Phase 1: `phase1/datastream_corp.db`, local SQLite. Delete it and rerun
  `phase1 t0` to reset. t0 adds Phase-1-only rows (an empty Research department, 6 terminated
  employees); Phase 1 headcount means active employees (1,201 of 1,207).
- Phase 2: `s3://awsworkshop-<name>-code-<ACCOUNT_ID>-<region>/db/datastream_corp.db`.
  Each MCP microVM copies it to `/tmp` once and queries it **read-only**;
  writes return `Error: the database is read-only; ...`. Only you can read it.

## Safe teardown

```bash
uv run bootcamp.py up 3     # switch off stages 4..7 but keep Cognito/MCP/gateway/memory
uv run bootcamp.py down     # end of day: destroy everything you own
```

Avoid `down` mid-workshop: a new Cognito domain re-triggers the ~5 min DNS
wait. `down` only touches resources tagged/named for your `PARTICIPANT`;
your LiteLLM key and budget belong to the instructor and survive it.

## What NOT to touch

- `terraform/` and `bootcamp_cli/` — platform-owned. Change
  behaviour through `.env`, `phase1/` and `phase2/app/` only.
- Terraform state under `terraform/participant/terraform.tfstate.d/` —
  never move or delete by hand; `down` is the teardown path, and `forget`
  drops it only after an instructor `reset`.
- Never run `terraform` directly; `bootcamp.py` passes the stage, model and
  gateway URL variables for you.

## Output shape

Answer with the exact command(s) to run next, in order, in one `bash`
block, then one line on what success looks like (e.g. `[PASS] stage 4 ...`).
