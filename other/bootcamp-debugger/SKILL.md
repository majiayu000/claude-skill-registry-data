---
name: bootcamp-debugger
description: Triage playbook for a DataStream Corp bootcamp participant whose `uv run bootcamp.py test`, `up N`, `invoke` or Phase 1 script failed. Maps every `[FAIL]`/`[WARN] stage N ...` line, LiteLLM gateway error and AWS AccessDenied to cause and fix, and shows how to read runtime logs and traces. Triggers on "test failed", "[FAIL] stage", "stage 2 failing", "Failed to resolve amazoncognito.com", "NXDOMAIN", "agent returned HTTP 424", "HTTP 403", "auth_error", "role is not a bootcamp participant", "participants may not call", "presigned URL expired", "Budget has been exceeded", "budget exceeded", "model not available", "ServiceUnavailable", "Tool Execution Denied", "Destructive SQL requires human approval", "AccessDenied", "explicit deny", "bedrock:InvokeModel not authorized", "memory not ACTIVE", "memory not recalled", "code interpreter tool failed", "browser tool failed", "StartCodeInterpreterSession", "StartBrowserSession", "my agent doesn't answer", "empty answer", "empty_upstream_response", "HTTP 502", "<thinking> tags in answer", "reasoningContent is not supported in multi-turn", "database is read-only", "[CHALLENGE] FAIL", "No stack provisioned", "no spans", "no evaluation results", "This run would score", "the limit is 1 to 25 per run", "The golden file has", "where are the logs". Do NOT use for "how do I run X" questions (use bootcamp-operator) or for writing new features (use agent-feature-builder / mcp-tool-author).
---

# Bootcamp Debugger

This skill reads `bootcamp.py` output, `traces` / `scores`, runtime logs
(`aws logs tail`) and the AgentCore Observability console to tell the participant the one
next command. Participants are developers; the platform owns infra. A fix
is either **your code / your `.env`**, **wait and re-test**, or **ask the
instructor** — never edit `terraform/` or `bootcamp_cli/`.

## Procedure

1. Get the failing line. If the user didn't paste one, run the narrowest check
   (`uv run bootcamp.py doctor` first when the laptop itself is suspect: tools, login, role, gateway, network):
   ```bash
   uv run bootcamp.py status            # STAGE=? and the ids
   uv run bootcamp.py test --only <N>   # one stage, cheap
   ```
2. Stages build on each other: if stage 1 fails, stage 2/4/7 failures are
   noise. Fix the **lowest** failing stage first (`uv run bootcamp.py test`).
3. Match the line in the tables below. If it names a runtime (stage 1, 4),
   read its logs (see *Logs*) before guessing.
4. Need more detail from `up` / `deploy`? Re-run with `--verbose` anywhere
   (`uv run bootcamp.py up 4 --verbose`) or `BOOTCAMP_VERBOSE=1` for full
   Terraform output and debug logs.

## `test` lines by stage

| Line / symptom | Cause | Fix |
|---|---|---|
| stage 0 pauses ~5 min "waiting ...s for DNS" | Brand-new Cognito domain; intentional | Wait. Do not ctrl-C and retry. |
| stage 0 `ConnectionError ... Failed to resolve 'ds-<10 hex>-<acct>.auth.<region>.amazoncognito.com'` | Resolver cached NXDOMAIN (queried too early) | Flush DNS — macOS `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`; Windows `ipconfig /flushdns`; Linux `resolvectl flush-caches` — or wait ~15 min, then `test --only 0` |
| stage 0 `HTTPError 400 ... invalid_client/invalid_scope` | Stale outputs after a partial apply | `uv run bootcamp.py up 0` |
| stage 1 tools/list error right after `up 1` | Runtime still warming (check retries ~60 s) | `test --only 1` again in 1–2 min |
| stage 1 `result=Error executing query: no such table` / S3 `NoSuchKey` in logs | DB object missing from your bucket (deleted by hand); the MCP server never writes to it | Re-seed: `aws s3 cp .build/datastream_corp.db s3://awsworkshop-<name>-code-<acct>-<region>/db/datastream_corp.db --profile bootcamp-<name>`, then `deploy` |
| stage 1/2 FAIL whose detail names your new no-argument tool (`<tool>: tool error` / not JSON rows) | The checks call every extra tool without arguments; it must return `{"data": [...]}` | Return `execute(...)`'s result (see mcp-tool-author), `deploy` |
| `Error: the database is read-only; this tool can only run queries that read data.` | By design: every Phase 2 query runs on a read-only connection | Not a bug; Phase 2 tools can only read |
| stage 1 `ImportError`/`ModuleNotFoundError` in MCP logs | New dep missing from `phase2/app/mcp_server/requirements.txt` or no arm64 wheel | Add it (wheel-only, linux/arm64, py3.13), `deploy` |
| stage 2 `tools=[...]` without `DataStreamDatabase___query_db` | Gateway target failed/not synced (MCP runtime wasn't serving when the target was created) | `aws bedrock-agentcore-control list-gateway-targets --gateway-identifier <GATEWAY_ID> --profile bootcamp-<name>` → if `FAILED`, `uv run bootcamp.py up 2` |
| stage 2 `gateway weather tool` FAIL: `Error: unknown tool` / `bad arguments` | The Lambda's `TOOLS` and `tools.json` disagree (name or argument names) | Same `name` in both, argument names = `inputSchema.properties`; `deploy` |
| stage 2 weather detail ends "api.weather.gov failed, but the Gateway reached your Lambda" | NWS outage or timeout; the Gateway → Lambda path works (PASS) | Nothing to fix; logs: `/aws/lambda/awsworkshop-<name>-weather` |
| stage 2 weather FAIL with `AccessDenied`/`Lambda` in the detail | Gateway role cannot invoke the function, or the function failed to start | `up 2`; read `/aws/lambda/awsworkshop-<name>-weather` (an `ImportError` means a dependency is missing from `phase2/app/weather_lambda/requirements.txt`) |
| stage 2 `gateway semantic tool search` FAIL (weather tool not first) | Tool descriptions too vague, or search not ready right after `up 2` | Re-run in a minute; sharpen the description in `tools.json` / the MCP docstring; `uv run bootcamp.py tools --search "..."` |
| stage 2: new MCP tool missing from the Gateway | `deploy` re-syncs the tool list (`gateway_tool_sync`, ~10-20 s); a failed sync fails `deploy` with Terraform's error block | `deploy` again; fallback: manual `synchronize-gateway-targets` (mcp-tool-author) |
| stage 2/7 `401`/`403` from gateway | Token not from your Cognito client, or expired | Use `uv run bootcamp.py token` (fresh); never reuse another participant's token |
| stage 3 `status=CREATING` | Memory provisioning takes a few minutes | `test --only 3` in 2–3 min |
| stage 4 `RuntimeError: model returned empty text (upstream timeout?) - re-run or try another MODEL_ID (`llm models`)`; `invoke` answers "Sorry, the model returned an empty answer ..." | Bedrock ended the stream without a single token (typically while a model's latency is degraded); the gateway proxy held the reply, retried once and fell back to the model's fallback (if `llm models` lists one), and every attempt was empty | Re-run; if it repeats, set `MODEL_ID` in `.env` to another model from `uv run bootcamp.py llm models` and `deploy` |
| Answer says "The data specialist failed: ..." (or weather) | That specialist raised (e.g. the gateway's `502` after its retries) or answered with nothing; `consult` reports it instead of letting the orchestrator invent numbers | Re-run; `traces --args <SESSION_ID>` shows the specialist's tool calls; runtime logs show the exception |
| `invoke` gives up after ~5 min (`No answer from your agent within 300s`) | Agent run too long (cold starts, slow model, many tool calls); it may still finish server-side | `traces <SESSION_ID>` a few minutes later (stage 5+) to see the slow span; use `--session last` for follow-ups (warm microVM); simplify the prompt or switch `MODEL_ID` |
| stage 4 `RuntimeError: agent returned HTTP 424` | Agent code crashed or the LLM call failed inside the runtime | Read `AGENT_LOG_GROUP` (below); match the traceback in the LiteLLM / code tables |
| `invoke --local` (or a Task 3 `[CHALLENGE]` before `up 4`): `Your local agent exited` / `did not start within 300s` | `agent.py` crashed on start (import error, syntax error, missing variable) or its packages failed to install | Read `.build/local-agent/agent.log` (the CLI prints its last lines); fix `agent.py` and re-run |
| `invoke --local`: `Port 8080 is already in use` | Another local agent (or any server) listens on 8080 | Stop it (`lsof -i :8080`), then re-run |
| `invoke --local`: `needs your Gateway and Memory: run up 3 first` | The local agent needs stage 3 (memory and its `awsworkshop-<you>-local` workload identity) | `uv run bootcamp.py up 3` |
| stage 4 `HTTP 403` / `401` on `invoke` | The agent accepts only a *user* token from your pool's user client (not `token`'s M2M token) | Use `invoke --actor <user>` (it signs in for you); `up 4` if you hand-edited the authorizer |
| stage 0 `story users sign in` FAIL; `NotAuthorizedException` / `ParameterNotFound` on `invoke --actor` | Story user's stored password missing or changed | `up 0` (re-creates the users and their SSM passwords); or pick any other name for a test user |
| stage 4 `identity from the verified token only` FAIL | The agent takes the actor from somewhere other than the token (header, payload), or the authorizer allows the M2M client | Restore `actor_from()` / `token_claims()` in `agent.py`, then `deploy`; `allowed_clients` in `terraform/` is platform-owned (revert any local edit, else ask the instructor) |
| `the agent failed mid-stream` on `invoke --stream` | The entrypoint raised after streaming began | Same as HTTP 424: read `AGENT_LOG_GROUP` |
| stage 4 `memory recall ... not recalled after 4 min` | Long-term extraction is async; or actor id lost | `test --only 4` once more; if still failing, check you didn't break `actor_from()` / `MEMORY_RELEVANCE_SCORE` |
| stage 4 `code interpreter tool` / `browser tool` FAIL, answer lacks `57938` / the live `syncToken` | Model answered without calling `run_python` / `browse_web`, or the tool errored | Check `status` shows `CODE_INTERPRETER_ENABLED=True` / `BROWSER_ENABLED=True` (else set the flag in `.env` + `deploy`); search `AGENT_LOG_GROUP` for `code_interpreter_client` / `browser_client` lines and a `Traceback` (`aws logs tail ... --filter-pattern`, see *Logs*; works on every OS); retry once (LLM routing varies) |
| `AccessDeniedException ... StartCodeInterpreterSession` / `StartBrowserSession` in agent logs | Tool used while its flag is off (agent role has no permission), or `.env` flag not applied | Set `ENABLE_CODE_INTERPRETER=true` / `ENABLE_BROWSER=true`, `deploy` |
| stage 4 `guardrail blocks injection + masks PII` FAIL: `injection obeyed=True` or `emails leaked=[...]` | Guardrail not attached to that call (agent code without `guardrail.py`'s model and hooks, or a new specialist lacks `*guardrail.hooks()` or builds its model without `make_model()`, which returns `guardrail.make_model(...)` when enabled) | `status` shows `GUARDRAILS_ENABLED=True`; keep `make_model()` and the hooks as shipped; `deploy`; retry once (LLM output varies) |
| Agent answer says a tool output "was withheld: the guardrail could not screen it" | The screening call through the gateway failed (fails closed by design) | Search `AGENT_LOG_GROUP` for `tool output screening failed`; usually budget (`429`) or a transient gateway error: retry |
| LiteLLM `403 guardrail ... is not tagged Participant=<you>` | Your script/agent named a guardrail that isn't yours | Use your own `guardrail_id` (`status`); the gateway allows only guardrails tagged with your name |
| Answer shows `{EMAIL}` / `{PHONE}` or "Blocked by the DataStream guardrail" | The guardrail masked PII (a long number, e.g. 9 digits, can look like a phone number) / blocked a prompt attack | By design with `ENABLE_GUARDRAILS=true` |
| browser tool `CDP ... failed` / websocket timeout | Page slow or blocks headless browsers | Retry, or try another URL; the sandbox has public internet but sites may block bots |
| stage 5 `[WARN] spans_found=0` / `traces` prints `No spans ...` | Spans lag 2-10 min | `test --only 5` or `traces` later; WARN never fails the run |
| stage 6 `status=CREATING` / not `ACTIVE` | Still provisioning, or eval role missing | Wait and retry; persistent → instructor |
| `scores` prints `No evaluation results ...` | Results arrive 15-30 min after the session goes idle (stage 6+) | Wait and re-run `scores` |
| `eval` item `[FAIL] ... not scored` / `LogEventMissingException` | The batch evaluation read the session before its telemetry was queryable (the CLI already waited and retried twice) | Re-run `eval` |
| `eval` item `[FAIL]` with a low Correctness | The answer disagrees with `expected` (or `expected` itself is wrong) | Read the explanation under the table; check the SQL with `traces <session> --args`; fix the prompt or the golden file |
| `eval`: `AccessDenied ... StartBatchEvaluation` / `CreateDataset` | Your participant role lacks the offline-evaluation permissions | Ask the instructor to run `instructor.py up` |
| `eval`: `This run would score N answers; the limit is 1 to 25 per run` | `--limit` x number of `--variants` is above 25 (or `--limit` < 1); the built-in judges bill the class AWS account, so `eval` caps each run | Lower `--limit` (e.g. `--limit 12 --variants A,B`) or compare fewer variants; never work around it with direct AgentCore API calls |
| `eval`: `The golden file has N items; keep it to 50 at most` | The golden file is larger than `eval` accepts | Trim `phase2/evals/golden.yaml` (or your `--dataset`) to the items that matter, at most 50; pick with `--limit` |
| `eval --evaluators custom`: `No custom evaluators yet` | Below stage 6 | `uv run bootcamp.py up 6` (or `deploy` at stage 6+) |
| `eval --variants`: `the agent applied variant A, not C` | The variant is not in `phase2/app/agent/prompt_variants.py`, or the deployed agent predates it | Add it to `VARIANTS`, then `deploy` |
| `rubric_judge` scores `-`, or `test` stage 6 `rubric judge through LiteLLM` FAILs with `JUDGE_HTTP_ERROR 401/429` | The judge call was refused by the gateway: budget exhausted (429) or the Lambda role is not mapped to you | `uv run bootcamp.py llm` (remaining budget); `aws logs tail /aws/lambda/awsworkshop-<you>-rubric-judge --since 1h` |
| `rubric_judge`: `RUBRIC_INVALID` / `JUDGE_REPLY_INVALID` | `TF_VAR_judge_rubric` names no entry of `evaluators.yaml`, or the judge did not reply with JSON | Fix the name or the rubric's wording, then `deploy` |
| `exact_numbers` scores `-` or an error | The Lambda found no answer in the trace | `aws logs tail /aws/lambda/awsworkshop-<you>-code-evaluator --since 1h` |
| stage 7 `SELECTs allowed=False` | Policy too strict or gateway still updating | `test --only 7` in 1 min; persistent → instructor |
| stage 7 `DELETE denied=False` / `disguised writes blocked=False` | Policy engine not attached yet | `up 7` again |
| stage 7 `cedar permits the weather tool` FAIL (stage 2 weather passes) | Gateway still attaching the policy engine, or `weather_tools_policy` not applied | `test --only 7` in 1 min; persistent: `up 7` |
| stage 7: your new MCP tool vanished from `tools/list` | Cedar default deny: only `query_db`, (if defined) `list_tables` / `describe_table`, and the `Weather___*` tools from `tools.json` are permitted | By design; stay at `up 6` while developing, or ask the instructor for a permit |
| `[CHALLENGE] SKIP stage N ...` | You haven't added that Phase 2 extension yet | Not a failure |
| `[CHALLENGE] FAIL stage N ...` | Extension present but broken; counts toward the exit code | Read the detail; fix your code, `deploy`, `test --only N` |
| `status` prints `No stack provisioned for '<name>'` | Nothing is up for that `PARTICIPANT` | `uv run bootcamp.py up 0` (check the `PARTICIPANT` spelling first) |

## Wrong-looking answers (no error line)

| Symptom | Cause | Fix |
|---|---|---|
| A check or answer failed: my code or the model? | Models are not deterministic; a weaker model misses steps | Rerun the same prompt on the reference (Phase 1: drop `--starter`). Fails there too = the model: rerun, or switch `MODEL_ID` (`llm models`) |
| Phase 2 agent states company numbers without calling `query_db` (`tools_used` lacks it) | Long-term memory recalled an earlier answer for that actor | Use a fresh `--actor` (any name other than the story users `alice-chen` / `jordan-lee` becomes a test user; the pages use `trace-test`, `online-eval`, `mallory`); `deploy` the current prompt, which forbids answering data questions from memory |
| `WHERE status='Active'` (or another value) returns 0 rows | SQLite string comparison is case-sensitive and the stored values are lowercase | Run `describe_table` (it shows sample values) and match their case, or use `LOWER(col)` |
| Stage 7: Cedar denies a harmless read | Cedar `like` patterns match text, they cannot parse SQL. Denied: mixed case (`sElEcT`), leading whitespace (the agent's guard strips it, direct `tools --sql` calls don't), a write keyword plus whitespace anywhere (`last_update `, `LIKE '%delete %'`), `--` or `/*` comments | Start with `SELECT` / `WITH` / `EXPLAIN` (UPPER, lower or Title case) and a space, tab, newline or CR, no comments; avoid a write keyword followed by whitespace (e.g. `last_update,` or `(last_update)`). `PRAGMA table_info(<table>)` (no `=` / `;`) is permitted |
| `tools` prints `WARNING: ...` about token measurement (exit 0) | The prompt-token comparison needs a model call and the model errored; the tool list above it is valid | Rerun later or with another `MODEL_ID` |
| Guardrail blocks a harmless request (`ENABLE_GUARDRAILS=true`) | At the default `MEDIUM` prompt-attack strength, naming a tool together with a URL looks like an attack | Rephrase without the tool name, or set `GUARDRAIL_PROMPT_ATTACK_STRENGTH=LOW` in `.env`, then `deploy` |
| `[WARN] stage 4 TRUST_ACTOR_HEADER=true: ...` (identity / recall checks) | You turned on the deliberately insecure Task 4 experiment: the agent trusts the `X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id` header, so any caller can pick an identity | Expected while experimenting; set `TRUST_ACTOR_HEADER=false`, then `deploy` |
| `deploy` rejects the guardrail settings | `GUARDRAIL_PII_TYPES` names an unknown Bedrock PII type, or `GUARDRAIL_PROMPT_ATTACK_STRENGTH=NONE` with `GUARDRAIL_PII_TYPES=none` (a guardrail that does nothing) | Use Bedrock entity names (`EMAIL,PHONE,NAME,...`), or set `ENABLE_GUARDRAILS=false` |
| stage 4 guardrail check FAILs after changing `GUARDRAIL_PII_TYPES` | The check expects emails masked | Keep `EMAIL` in the list |
| `exact_numbers` FAILs an answer without a number (no reference, e.g. online) | By design: an answer that only promises to look ("Let me route this...", "One moment, I'll check") fails; other answers without numbers (greetings, preference acknowledgements) score `N/A` | Make the agent answer or say plainly that it can't; not an evaluator bug |

## LiteLLM gateway errors (Phase 1 output, runtime logs, `llm`)

| Error | Cause | Fix |
|---|---|---|
| `401 auth_error: role is not a bootcamp participant: arn:...` | Called with your base profile, not the participant role (plain `python script.py`, `BOOTCAMP_ROLE_ARN=none`) | Run via `uv run bootcamp.py ...`, or see litellm-usage for scripts |
| `401 auth_error: presigned URL expired or window too long` | Laptop clock skew | Resync clock — macOS `sudo sntp -sS time.apple.com`; Windows `w32tm /resync`; Linux `sudo timedatectl set-ntp true` |
| `401 auth_error: send a LiteLLM key or an X-Amz-Sts-Identity-Url header` | Client built without `StsIdentityAuth` | Use `litellm_gateway.make_model()` / `GatewayModel(...)`, or `httpx.Client(auth=StsIdentityAuth(session))` |
| `403 participants may not call /...` | Your script called a LiteLLM route outside the participant allowlist (admin, spend, `/bedrock/...` pass-through) | By design: only model routes (`/v1/chat/completions`, `/v1/models`, ...) and `/key/info`; `uv run bootcamp.py llm` shows your budget |
| `No LiteLLM key for participant '<you>' in region ...` | You're not in the roster yet, or `BOOTCAMP_REGION` is wrong | Check `BOOTCAMP_REGION` in `.env`; else ask the instructor to add you and run `instructor.py up` |
| `429 ... Budget has been exceeded` (key or team) | Your $ budget (default $5) or your company team's budget (`bootcamp-<company>`) is spent | `uv run bootcamp.py llm` to confirm; ask the instructor to raise it in `roster.json` + `instructor.py keys` |
| `key not allowed to access model` / `Invalid model name` | `MODEL_ID` typo, or a model your class doesn't enable | Use a name exactly as `uv run bootcamp.py llm models` lists it (or leave `MODEL_ID` empty for the class default); Phase 2 then `deploy` |
| `ServiceUnavailable` / `429` / `model unavailable` | Upstream capacity for that model | Switch `MODEL_ID` in `.env`, then `deploy` (Phase 2) |
| `503` from the gateway (any command or script); `the class gateway runs 08:00-22:00 (Asia/Jerusalem)` | The gateway is off outside its daily hours (08:00-22:00 Israel time; `uv run bootcamp.py doctor` names the window); inside them it is restarting | Work within the gateway's hours; inside them retry in a minute, and tell the instructor if it persists |
| `502` with type `empty_upstream_response` | Bedrock ended the stream without a single token (typically while a model's latency is degraded); the gateway proxy held the reply, retried once and fell back to the model's fallback (if `llm models` lists one), and every attempt was empty | Re-run; or another model from `llm models` (Phase 2: then `deploy`) |
| Phase 1 t7 `[fallback] Empty final answer (try another MODEL_ID)` | Orchestrator returned empty text; the last specialist result is shown instead | Re-run, or set `MODEL_ID` to another model from `llm models` |
| `<thinking>...</thinking>` in the answer, a dim `[reasoning]` block, `reasoningContent is not supported in multi-turn`, a skipped report row | Model quirks (Nova Lite, gpt-oss, Nova 2 Lite); see litellm-usage "Known model quirks" | Strip/hide as described there, or pick another model from `llm models` |

## Expected "errors" (by design)

- **`Tool Execution Denied`** at stage 7 for INSERT/UPDATE/DELETE/REPLACE/DROP
  — the Cedar policy is working. Any new MCP tool other than `list_tables` /
  `describe_table` is hidden until a permit exists.
- **`Error: the database is read-only; ...`** — a write that got past the
  guard and Cedar (e.g. mixed-case `dElEtE`) is refused by the read-only DB.
- **`Destructive SQL requires human approval and is blocked in production.`**
  — the agent's `ReadOnlyGuardHook`. Keep it.
- **`AccessDenied ... explicit deny`** on `bedrock:InvokeModel`/`Converse` —
  no direct Bedrock; all model calls go through LiteLLM.
- **`AccessDenied`** on a resource or log group named for another
  participant, or on `iam:*` — tag isolation. You can only touch
  `awsworkshop-<you>-*` and read your own log groups plus `aws/spans`.
- **`AccessDenied` on `AssumeRole`** — your base profile isn't trusted for
  `bootcamp-participant-<name>`: check `PARTICIPANT` spelling and that `aws sts get-caller-identity
  --profile bootcamp` shows your IAM user `bootcamp-<name>` (a revoked or deleted access key fails here),
  then ask the instructor.

## Logs and traces

```bash
uv run bootcamp.py traces [SESSION_ID]   # span tree of your latest invoke, stage 5+ (spans lag 2-10 min)
uv run bootcamp.py traces --args         # plus tool inputs, e.g. the SQL the agent really sent
uv run bootcamp.py scores                # online-eval results, stage 6+ (lag 15-30 min)
uv run bootcamp.py status | grep -E 'AGENT_LOG_GROUP|MCP_RUNTIME_ID'
# Windows PowerShell: uv run bootcamp.py status | Select-String 'AGENT_LOG_GROUP|MCP_RUNTIME_ID'
aws logs tail "<AGENT_LOG_GROUP>" --since 15m --profile bootcamp-<name>
aws logs tail "/aws/bedrock-agentcore/runtimes/<MCP_RUNTIME_ID>-DEFAULT" --since 15m --profile bootcamp-<name>
aws logs tail "<AGENT_LOG_GROUP>" --since 30m --filter-pattern Traceback --profile bootcamp-<name>
```

`bootcamp-<name>` is the participant-role profile (setup: see
bootcamp-operator); your plain profile (`bootcamp`, your IAM user's access key) runs as
that IAM user, not the participant role. You can read only your own log groups
plus `aws/spans`. Look for the
first `Traceback`, `KeyError: '<ENV_VAR>'`, `ImportError`, or an
`openai.AuthenticationError`/`BadRequestError` (= LiteLLM table above).

Console traces: AgentCore console → **Observability** → Agent: your
`awsworkshop_<name>_agent` → Sessions → pick the session id that `invoke`
printed → spans show each model call and tool call with latency and errors.

## Output shape

```markdown
**Failing stage:** <0..7 or "LiteLLM" / "IAM">
**Likely cause:** <one sentence, quoting the matching row>
**Next command:**
\`\`\`bash
<single command>
\`\`\`
**Why:** <one sentence>
```

If nothing matches, say so, show the last 50 log lines, and suggest asking
the instructor with that output.
