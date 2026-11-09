---
name: litellm-usage
description: Shows a DataStream Corp bootcamp participant how to call the Opsfleet LiteLLM gateway from their own scripts, notebooks and Strands agents — keyless via `shared/litellm_gateway.py` (`make_model`, `GatewayModel`, `StsIdentityAuth`) or with the plain OpenAI SDK / httpx — plus checking remaining budget, choosing a model from `llm models` and its known quirks. Triggers on "call the LLM from my script", "use the gateway in a notebook", "OpenAI SDK with LiteLLM", "LITELLM_BASE_URL", "where is my API key", "how much budget do I have left", "check my spend", "which model should I use", "which model is cheapest", "is sonnet more expensive", "model quirks", "<thinking> tags in answer", "[reasoning] block", "reasoningContent is not supported in multi-turn", "model skipped a row", "keyless", "X-Amz-Sts-Identity-Url", "can I call Bedrock directly", "empty response from the model". Do NOT use for gateway errors during `test`/`invoke` (use bootcamp-debugger) or for wiring a model into the deployed agent beyond MODEL_ID (use agent-feature-builder).
---

# LiteLLM Usage

There is **no direct Bedrock** in the bootcamp: the participant role and
every role it creates carry an explicit deny on `bedrock:InvokeModel` /
`Converse`. All model traffic goes to the Opsfleet LiteLLM gateway, which
bills a **per-participant budget** (default $5) inside your company team's
budget (`bootcamp-<company>`).

Auth is **keyless**: each request carries header `X-Amz-Sts-Identity-Url`, a
presigned STS `GetCallerIdentity` URL (valid <= 15 min) signed with your own
AWS credentials. The gateway replays it, sees role
`bootcamp-participant-<name>` (or `awsworkshop-<name>-*` for your runtimes),
and injects your LiteLLM key server-side. No key ever exists in your code,
`.env` or notebook — never ask for one and never hardcode one. Participants
may call only the model routes (`/v1/chat/completions`, `/v1/completions`,
`/v1/embeddings`, `/v1/models`, `/v1/model/info`, `/v1/messages`,
`/v1/responses`, also without `/v1`) and `/key/info`; every other route
(admin, spend, `/bedrock/...` pass-through) answers 403.

## Get the URL, models and budget

```bash
uv run bootcamp.py llm
# LITELLM_BASE_URL=https://...
# MODELS=<every model your instructor enabled>
# MODEL_ID=<your .env MODEL_ID, else the class default>
# BUDGET=$0.123400 spent of $5
```

`uv run bootcamp.py llm models` lists each model with its Bedrock id, price
per million tokens and NOTES (`YOURS`, `class default`, `suggested`, the
instructor's note, `falls back to X`). `LITELLM_BASE_URL` is not a secret; you may add it to `.env` so scripts
pick it up via `load_dotenv`.

## The one rule: sign with the participant role

The identity URL must be signed by your **participant role**, not your base
IAM-user profile (that yields `401 role is not a bootcamp participant`).
Pick one:

- Reuse the CLI's role assumption in Python:
  ```python
  from bootcamp_cli.aws import make_session
  from bootcamp_cli.config import load_settings

  session = make_session(load_settings())  # assumes bootcamp-participant-<PARTICIPANT>
  ```
- Or an AWS profile with `role_arn = arn:aws:iam::<ACCOUNT_ID>:role/bootcamp/bootcamp-participant-<name>`
  and `source_profile = bootcamp` (see bootcamp-operator), exported as
  `AWS_PROFILE=bootcamp-<name>` for that script, then `boto3.Session()`. Your
  plain profile (`bootcamp`, the `AWS_PROFILE` in `.env`, your IAM user) is not the
  participant role and gets a 401.

Run scripts from your clone's root (the folder with `bootcamp.py`) with `uv run python my_script.py` (or a
notebook kernel from `uv run --with jupyter jupyter lab`).

## Strands agent (recommended)

```python
import sys

sys.path.insert(0, "shared")
import litellm_gateway
from strands import Agent

model = litellm_gateway.make_model("<MODEL_ID>", base_url="<LITELLM_BASE_URL>")
print(Agent(model=model, callback_handler=None)("Say hi in five words."))
```

Use a name from `llm models` (e.g. the `MODEL_ID` line of `uv run bootcamp.py llm`).
`make_model(model_id=None, base_url=None, **params)` reads `MODEL_ID`,
`LITELLM_BASE_URL` (and optional `LITELLM_API_KEY`) from env when omitted
(`MODEL_ID` must then be set: `bootcamp.py` sets it, a plain script does not);
`params` go to the OpenAI call (e.g. `temperature=0`, `max_tokens=500`).
It uses `boto3.Session()` default credentials, so export
`AWS_PROFILE=bootcamp-<name>` first, or build the model yourself:

```python
model = litellm_gateway.GatewayModel(
    "<LITELLM_BASE_URL>",  # api_key=None -> keyless
    session=session,
    model_id="<MODEL_ID>",
    params={"max_tokens": 500},
)
```

`GatewayModel(base_url, api_key=None, session=None, model_id=..., params=...)`
builds a fresh **async** httpx client with `StsIdentityAuth(session)` per
request (what Strands needs).

## Plain OpenAI SDK (sync)

For the sync SDK, attach `StsIdentityAuth(session)` to a sync client:

```python
import sys

sys.path.insert(0, "shared")
import httpx
from openai import OpenAI  # installed with strands-agents[openai]
from litellm_gateway import StsIdentityAuth

client = OpenAI(
    base_url="<LITELLM_BASE_URL>/v1",
    api_key="keyless",  # placeholder; the gateway ignores it
    http_client=httpx.Client(auth=StsIdentityAuth(session), timeout=600),
)
reply = client.chat.completions.create(
    model="<MODEL_ID>", messages=[{"role": "user", "content": "One fact about SQLite."}]
)
print(reply.choices[0].message.content, reply.usage)
```

Bedrock Guardrail on a call (your own only: the gateway answers 403 for a guardrail not tagged with your name):
`extra_body={"guardrailConfig": {"guardrailIdentifier": "<guardrail_id>", "guardrailVersion": "1"}}` (ids from
`uv run bootcamp.py status` after `ENABLE_GUARDRAILS=true` + `deploy`). A blocked prompt returns
`finish_reason="content_filter"` and the guardrail's blocked message; masked PII shows as `{EMAIL}` / `{PHONE}`.

## Raw httpx (budget, models)

```python
with httpx.Client(base_url="<LITELLM_BASE_URL>", auth=StsIdentityAuth(session), timeout=30) as c:
    print([m["id"] for m in c.get("/v1/models").json()["data"]])
    info = c.get("/key/info").json()["info"]
    print(f"${info['spend']:.4f} of ${info['max_budget']}")
```

## Choosing a model

The instructor picks the class's models, so run `uv run bootcamp.py llm models`
first; gateway names are the real Bedrock model names. `MODEL_ID` in `.env` is
optional (empty = class default); switch with `MODEL_ID=<model>` in `.env` or
per command (`MODEL_ID=<model> uv run bootcamp.py ...`; Phase 2: then `deploy`).

- Prefer the `class default` and `suggested` models.
- Where enabled, newer Claude (5.5 class) and newer GPT (5.6 / 6) models are
  the best choice; a Sonnet-class model for hard multi-step routing.
- Nova Lite / Nova 2 Lite are acceptable cheap options.
- Avoid tiny models: `gpt-oss-20b` cannot complete the tool-use tasks.
- Fallbacks: when a model errors or keeps answering empty, the gateway answers
  with its fallback (`falls back to X` in `llm models`), billed at the
  fallback's price. The class default usually has one, so an answer may come
  from another model during a Bedrock hiccup; if quality suddenly changes,
  check the model in the response.

Cost depends on the model. With `gpt-6-luna` or `claude-haiku-5-5`: Phase 1 ~$0.04-0.25, Phase 2 with the
optional pages ~$0.05-0.30 (default budget $5); `claude-sonnet-5-5` ~20x more. On `nova-2-lite` Task 4 is ~$0.04, one
10-item `eval` ~$0.04 for its `rubric_judge`. AgentCore's built-in
evaluators bill the class AWS account, not your budget. Phase 1 scripts print a
`[budget] $x of $y used ...` line after each run (warns at 75 %).

Budget tips: stage 4 `test` invokes the agent several times (memory recall
polls up to 12x) — prefer `test --only N`. Mix models: a stronger orchestrator,
cheap specialists. Set `max_tokens`. Re-check with `uv run bootcamp.py llm`
after an experiment to see what it cost. Out of budget → ask the instructor
(they edit `roster.json` and run `uv run instructor.py keys`).

## Known model quirks

On the Phase 1 skills / database tasks:

| Model | Quirk | What to do |
|---|---|---|
| `gpt-oss-120b` / `gpt-oss-20b` | Reasoning model: emits reasoning blocks (Phase 1 prints a dim `[reasoning]` block). Strands warns "reasoningContent is not supported in multi-turn" (harmless; filtered in `phase1/common.py`). Numbers may contain narrow no-break spaces (U+202F). 20b fails the headcount task | `PHASE1_SHOW_REASONING=0` hides the block; normalise U+202F before string-matching numbers; don't use 20b |
| `nova-lite` (v1) | Passes the tasks but may leave inline `<thinking>...</thinking>` tags in the final answer | Strip them before displaying, or pick another model |
| `nova-2-lite` | Fastest, but may skip a requested Total row in the headcount report | Be explicit about required rows in instructions / skills |
| `claude-haiku-4-5`, `claude-sonnet-4-6` | Reliable; sonnet-4-6 can return `ServiceUnavailable` under load | Hence its fallback to haiku-4-5 |
| Llama 4 Maverick / Scout, `mistral-small` | No tool use through Bedrock Converse | Not usable for these agents (not enabled) |
| `qwen3-32b` | Tool-call errors | Not enabled |

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `401 role is not a bootcamp participant` | Signed with base profile | Use the participant session/profile above |
| `401 presigned URL expired or window too long` | Clock skew | Resync your OS clock |
| `401 send a LiteLLM key or an X-Amz-Sts-Identity-Url header` | Client without `StsIdentityAuth` | Add `auth=StsIdentityAuth(session)` / use `GatewayModel` |
| `404` on `/chat/completions` | Base URL missing `/v1` for the OpenAI SDK | Use `<LITELLM_BASE_URL>/v1` |
| `403 participants may not call /...` | Route outside the participant allowlist (admin, spend, provider pass-through) | Use a model route or `/key/info`; budget via `uv run bootcamp.py llm` |
| `403 guardrail ... is not tagged Participant=<you>` | `guardrailConfig` names someone else's (or an untagged) guardrail | Use your own `guardrail_id` from `status` |
| `429 Budget has been exceeded` | Your or the team budget spent | Instructor raises it |
| `eval` / online-evaluation cost not in `llm` spend | AgentCore's built-in judges bill the class AWS account, not LiteLLM; only `rubric_judge` goes through the gateway | Evaluate only via `uv run bootcamp.py eval` (max 25 answers per run), prefer `exact_numbers` / `rubric_judge` while iterating |
| `502` with type `empty_upstream_response` | Bedrock ended the stream without a single token (typically while a model's latency is degraded); the gateway proxy held the reply, retried once and fell back to the model's fallback (if `llm models` lists one), and every attempt was empty. `GatewayModel` also raises `EmptyModelResponseError` if a reply still has no output | Re-run, or use another model from `llm models` |
| `AccessDenied ... bedrock:InvokeModel` | Tried Bedrock directly | By design — use the gateway |

## Output shape

Give a runnable snippet that (1) builds a participant-role session, (2)
creates the client/model, (3) makes one call — plus the `uv run` command to
run it and a reminder to check `uv run bootcamp.py llm` for spend.
