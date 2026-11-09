---
name: agent-feature-builder
description: Helps a DataStream Corp bootcamp participant extend the Phase 2 AgentCore agent in `phase2/app/agent/agent.py` safely — add a Strands `@tool`, add a specialist sub-agent (agents-as-tools), tweak the orchestrator or specialist system prompts, use AgentCore Memory with actor/session ids, switch to another gateway model (`llm models`), turn on the optional Code Interpreter / Browser tools, keep the read-only SQL guard, then try it with `invoke --local` (no deploy) and ship with `deploy` + `test --only 4` + `invoke`. Triggers on "add a tool to my agent", "add a specialist", "new sub-agent", "add an hr_agent", "change the system prompt", "make the agent remember", "memory per user", "actor id", "session id", "switch model", "use sonnet", "use a cheaper model", "code interpreter", "run python in a sandbox", "browser tool", "browse a web page", "ENABLE_CODE_INTERPRETER", "ENABLE_BROWSER", "ENABLE_GUARDRAILS", "guardrail", "prompt injection", "prompt variant", "A/B test my prompt", "stream the answer", "my new tool isn't called", "extend the executive assistant", "build a feature on the bootcamp agent". Do NOT use for adding tools to the MCP server / database layer (use mcp-tool-author), for failing tests or errors (use bootcamp-debugger), or for LLM calls outside the agent (use litellm-usage).
---

# Agent Feature Builder

The deployed agent is `phase2/app/agent/agent.py` plus
`answers.py`, `sandbox_tools.py`, `guardrail.py` and `prompt_variants.py` next to it, zipped by `uv run bootcamp.py deploy`
together with the linux/arm64 wheels from `phase2/app/agent/requirements.txt`
and `shared/*.py` (`litellm_gateway.py`, `sql_guard.py`, `nws_weather.py`). Shape:

- `invoke()` (the async `@app.entrypoint`) reads the actor from the verified
  user token (`actor_from`), then `run_agent()` opens the AgentCore Gateway MCP
  client with an M2M token, builds the **orchestrator** `Agent`
  (`build_orchestrator`) and iterates `stream_async`: `{"delta": text}` and
  `{"tool": name}` events, then the reply object. With `"stream": true` in the
  payload those events go out as server-sent events (`invoke --stream`);
  otherwise `last_event()` returns only the reply.
- `build_specialists(gateway, results)` returns `@tool` sub-agents. Each finds
  its tools with the Gateway's semantic search, `search_tools(gateway, (need,
  top_k))` (`DATA_TOOLS`, `WEATHER_TOOLS`), never `list_tools_sync()`:
  `data_agent` (the top 3 database tools + `ReadOnlyGuardHook`) and `weather_agent`
  (the top-ranked tool, `Weather___get_us_forecast` from the Gateway's Lambda
  target, which runs `shared/nws_weather.py`, + `nws_weather.WEATHER_PROMPT`: US locations
  only, a few trimmed forecast lines instead of raw NWS JSON; non-US places get
  "I can only look up US weather (National Weather Service)."). Each returns `consult(agent, query, "data")`: the answer,
  or "The data specialist failed: ..." when the specialist raises or answers
  with nothing (never an empty string), appended to `results`.
- `orchestrator_prompt()` tells the orchestrator to report a failed specialist
  and never invent numbers or placeholders such as `[count]`; keep that line.
- The reply is `{"response": final_answer(...), "actor_id": ..., "session_id": ..., "variant": ...}`
  (add reply fields there, in `run_agent`):
  if the model returns empty text, the last specialist answer (or a "Sorry,
  the model returned an empty answer ..." message) is sent instead.
- `make_model()` → LiteLLM gateway (keyless; `guardrail.make_model(...)` when
  guardrails are on); `memory_session_manager()` →
  AgentCore Memory keyed by `actor_id` + `session_id`.
- All ids come from env vars Terraform sets (`MODEL_ID`, `GATEWAY_URL`,
  `MEMORY_ID`, ...). Never hardcode ids, URLs or keys.

## Rules that keep the agent deployable

1. **Prototype in Phase 1 first.** `phase1/t7_agents_as_tools.py` has the
   same orchestrator shape and runs locally in seconds:
   `uv run bootcamp.py phase1 t7 "..."`. Port to `agent.py` once it works.
2. **Every sub-agent that gets `gateway_tools` keeps
   `hooks=[ReadOnlyGuardHook()]`.** Stage 7 Cedar also blocks writes at the
   gateway and the MCP server's database is read-only — defence in depth,
   not a reason to drop the hook.
3. **Tools fail soft.** Catch errors and return an error string so the model
   can recover. An exception raised in `invoke()` or at import time makes the
   runtime return HTTP 424.
4. **Docstring = routing.** First line says what, `Args:` says each input;
   the orchestrator prompt names the tool and when to use it.
5. **New dependency?** Add to `phase2/app/agent/requirements.txt`. The build
   is wheel-only for linux/arm64 + Python 3.13 — pure-Python packages are safest.
6. **Do not edit `shared/litellm_gateway.py`**, `terraform/` or
   `bootcamp_cli/`. New env vars need Terraform, so ask the instructor instead.

## Worked example: an `hr_agent` specialist + a plain tool

Goal: HR questions go to a dedicated specialist that knows the schema, and
the orchestrator can compute tenure without spending a model call on maths.

```python
# phase2/app/agent/agent.py
from datetime import date

HR_PROMPT = (
    "You are an HR analyst for DataStream Corp. Use the database tools with SELECT only. "
    "Inspect the schema first (SELECT name FROM sqlite_master WHERE type='table'). "
    "Answer with numbers and a one-line summary."
)


@tool
def years_since(iso_date: str) -> str:
    """Compute whole years between a past ISO date (YYYY-MM-DD) and today, e.g. an employee's tenure.

    Args:
        iso_date: The start date, formatted YYYY-MM-DD.
    """
    try:
        start = date.fromisoformat(iso_date)
        today = date.today()
        years = today.year - start.year - ((today.month, today.day) < (start.month, start.day))
        return f"{years} full year(s) since {iso_date}"
    except ValueError as error:
        return f"years_since failed: {error}"


def build_specialists(gateway: MCPClient, results: list[str]) -> list:
    # ... existing data_agent, weather_agent, consult() and remember() unchanged ...

    @tool
    def hr_agent(query: str) -> str:
        """Answer HR questions: headcount by department, hiring dates, tenure, salaries, managers.

        Args:
            query: An HR or people-analytics question.
        """
        agent = Agent(
            model=make_model(),
            system_prompt=f"{HR_PROMPT}\n{guardrail.prompt_hint()}",
            tools=[*search_tools(gateway, DATA_TOOLS), years_since],
            hooks=[ReadOnlyGuardHook(), *guardrail.hooks()],
            callback_handler=None,
        )
        return consult(agent, query, "hr")

    return [data_agent, weather_agent, hr_agent, years_since]
```

Then teach the orchestrator to route to it in `orchestrator_prompt()`:

```python
"Route HR and people questions (headcount, tenure, salaries) to hr_agent, other database"

"questions to data_agent and weather questions to weather_agent; use years_since for date maths; "
```

Try it on this machine first (stage 3+; seconds per change), then ship and verify:

```bash
uv run bootcamp.py invoke "Who is the longest-serving engineer and how many years have they been here?" --local
uv run bootcamp.py deploy
uv run bootcamp.py test --only 4
uv run bootcamp.py invoke "Who is the longest-serving engineer and how many years have they been here?"
```

Confirm routing in the trace (stage 5+, spans arrive 2-10 min after the
invoke): `uv run bootcamp.py traces --args` (or AgentCore console → Observability →
Agent: your agent → Sessions) should show an `hr_agent` tool span with
`DataStreamDatabase___query_db` calls inside it.

## Optional sandbox tools: Code Interpreter and Browser

Set in `.env` (stage >= 4):

```.env
ENABLE_CODE_INTERPRETER=true   # orchestrator tool run_python(code)  -> AWS-managed aws.codeinterpreter.v1
ENABLE_BROWSER=true            # orchestrator tool browse_web(url)   -> AWS-managed aws.browser.v1
```

Then apply and verify:

```bash
uv run bootcamp.py deploy
uv run bootcamp.py test --only 4
```

- The platform sets `CODE_INTERPRETER_ENABLED` / `BROWSER_ENABLED` on the runtime and grants the agent role the
  session APIs; `phase2/app/agent/sandbox_tools.py` turns them into tools (`optional_tools()`) and prompt hints
  (`prompt_hints()`). Each call starts a fresh sandbox session and stops it afterwards.
- Give a **specialist** the sandbox too: `tools=[*search_tools(gateway, DATA_TOOLS), run_python]` (import from
  `sandbox_tools`; keep `ReadOnlyGuardHook`). E.g. an `analysis_agent` that queries rows, then computes statistics in `run_python`.
- `browse_web` returns title, final URL and the first 4000 chars of visible text via raw CDP (no Playwright). Need
  clicks/forms? Add more CDP calls in `read_page()` (`Input.dispatchMouseEvent`, `Runtime.evaluate`) rather than
  adding Playwright to `requirements.txt` (large arm64 driver).
- Using a tool without its flag → the agent role lacks permission → `AccessDeniedException` in `AGENT_LOG_GROUP`.

```bash
uv run bootcamp.py test --only 4    # adds "code interpreter tool" / "browser tool" checks when enabled
uv run bootcamp.py invoke "Open https://example.com and use the code interpreter to count the words in its first paragraph."
```

## Optional: Bedrock Guardrail (prompt injection, PII)

`ENABLE_GUARDRAILS=true` in `.env` + `deploy` (stage >= 4) creates `awsworkshop-<you>-guardrail` and sets
`GUARDRAIL_ID` / `GUARDRAIL_VERSION` on the runtime. `phase2/app/agent/guardrail.py` then attaches it to every model
call (`make_model()` returns `guardrail.make_model(...)`, which sends `guardrailConfig` through LiteLLM; the gateway
refuses a guardrail not tagged with your name), adds `ToolOutputGuard` (screens tool results with the same
guardrail, a blocked database result row by row so only poisoned rows/values are replaced, and tags them
`<untrusted_tool_output>`) and one hardening line to the prompts. Keep both in any specialist
you add: `hooks=[ReadOnlyGuardHook(), *guardrail.hooks()]` and `f"{PROMPT}\n{guardrail.prompt_hint()}"`.
Bedrock checks only the user's text for prompt attacks, never tool results, so a new tool that reads untrusted data
(web pages, tickets, documents) must go through the hook. Emails/phone numbers come back as `{EMAIL}` / `{PHONE}`.
Tune it in `.env`, then `deploy`: `GUARDRAIL_PROMPT_ATTACK_STRENGTH` (`NONE|LOW|MEDIUM|HIGH`, default `MEDIUM`,
which can block a harmless request naming a tool together with a URL) and `GUARDRAIL_PII_TYPES` (comma list of
Bedrock PII entity types masked in answers, default `EMAIL,PHONE`, or `none`; unknown types and `NONE` + `none` are
rejected; the stage-4 guardrail check expects `EMAIL`).

## Prompts

- Orchestrator: `orchestrator_prompt(actor_id, sandbox_tools)` — keep the actor
  name and the trailing `{prompt_hints(sandbox_tools)}` in it;
  list every specialist by its exact function name with a "when" clause.
- Specialists: one short prompt each; put them in module-level constants.
- Prompt-only change? Still `deploy` — the prompt lives in the zip.

## Memory (actor / session)

- `--actor` → the CLI signs in as that Cognito user and sends its access
  token → the runtime's JWT authorizer validates it → `actor_from()` reads the
  `username` claim. Never take identity from a header or the payload: any
  caller could then read anyone's memories (stage 4 `identity` check).
  Experiment: `TRUST_ACTOR_HEADER=true` + `deploy` makes the runtime forward
  `X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id` and the agent trust it,
  i.e. exactly that hole; stage 4 then prints `[WARN] stage 4
  TRUST_ACTOR_HEADER=true: ...` instead of FAIL. Set it back to `false` and
  `deploy`.
- `--session` → conversation (short-term) memory: events per actor + session,
  reloaded when a session continues.
- Long-term records are extracted asynchronously (~1–2 min) by three
  strategies, each in its own per-actor namespace: `UserFacts` (semantic),
  `UserPreferences` (user preference), `SessionSummaries` (summary, one
  namespace per session). `long_term_retrieval()` searches all three before
  each model call and the hits arrive as `<user_context>`.
- `MEMORY_RELEVANCE_SCORE = 0.3` (facts, summaries) is tuned on purpose;
  preferences use `ALWAYS` (no threshold) because they apply to every
  question. If you change either, re-check with `test --only 3` (preference
  challenge) and `test --only 4` (fact recall).
- Inspect what was stored: `uv run bootcamp.py memory --actor <name>`.
- Recalled memories are context, not data: the orchestrator prompt forbids
  answering company numbers from memory (always `query_db`). Keep that rule
  when you edit the prompt; test data questions with a fresh `--actor`, since
  an actor's old answers otherwise tempt the model to skip the tool.
- `MEMORY_EPISODIC=true` + `deploy` (stage >= 3) adds a fourth strategy,
  `Episodes` (episodic). Any other new strategy needs Terraform
  (`task3_memory.tf`) and a new env var, so ask the instructor; then add an
  entry in `long_term_retrieval()`. Extraction quota is shared, keep it light.

```bash
uv run bootcamp.py invoke "Remember: I prefer answers as bullet lists." --actor bob-lee
# wait ~2 min, new session:
uv run bootcamp.py invoke "Summarise Engineering headcount." --actor bob-lee
```

Custom `--session` ids must be at least 33 characters.

## Switching models

Pick a model from `uv run bootcamp.py llm models` (prices, class default,
suggestions, quirks), set `MODEL_ID=<model>` in `.env` (empty = class
default), then `uv run bootcamp.py deploy` — only the runtime env changes. To
mix, pass a model per agent: `litellm_gateway.make_model("<stronger model>",
LITELLM_BASE_URL)` for the orchestrator, keep a cheap one for specialists. See
litellm-usage for choosing a model, cost and known model quirks.

## Common pitfalls

- Tool added to `build_specialists` but not returned in the list → never offered.
- Specialist built without `ReadOnlyGuardHook` → writes reach the gateway
  (`Tool Execution Denied` at stage 7) and, if they get past Cedar, the
  database answers `Error: the database is read-only; ...`.
- Empty answers (`Sorry, the model returned an empty answer ...` or "The data
  specialist failed: ...") mean Bedrock streamed no tokens even after the
  gateway's retry and the model's fallback (if `llm models` lists one): re-run,
  or set `MODEL_ID` to another model from `llm models` + `deploy`.
- Testing a prompt change? Use a fresh `--actor`: long-term memory of an
  existing actor can answer correctly and hide a regression.
- Before shipping a prompt/model change, run `uv run bootcamp.py eval`: it
  replays `phase2/evals/golden.yaml` (11 questions with known answers, the
  first 10 by default (`--limit`), fresh actor per item) and fails below an 80%
  pass rate (`--min-pass`). Add an item there for every new
  capability you build, but keep the file small (at most 50 items; a run
  scores at most 25 answers, `--limit` x `--variants`).
- Evaluations only through `uv run bootcamp.py eval`: AgentCore's built-in
  judges bill the class AWS account (not LiteLLM), so never call AgentCore
  evaluation APIs (`StartBatchEvaluation`, `Evaluate`,
  `CreateOnlineEvaluationConfig`) from boto3 / the AWS CLI / a script, never
  run `eval` in a loop, never load-test the agent (online evaluation scores
  every request). Re-run after a change worth measuring; while iterating prefer
  `--evaluators exact_numbers` (no model) or `rubric_judge` (LiteLLM budget).
- Comparing two prompts? Put the change in `phase2/app/agent/prompt_variants.py`
  as variant `B` (A = the shipped prompt), `deploy`, then
  `uv run bootcamp.py eval --variants A,B --evaluators all`: both variants get
  the same golden questions and evaluators; the table shows pass rate and mean
  scores per variant and the change vs A. Promote a winner by moving its lines
  into `orchestrator_prompt`.
- Domain-specific quality bar? Deterministic checks go in the code-based
  evaluator `phase2/app/code_evaluator/handler.py` (a Lambda, no judge model;
  `deploy` at stage 6+, then `eval --evaluators exact_numbers`). Judgement calls
  go in a rubric of `phase2/evals/evaluators.yaml`, graded by the `rubric_judge`
  Lambda (`phase2/app/rubric_judge/handler.py`) with a judge model called through
  LiteLLM (billed to your key): `TF_VAR_judge_rubric=<name>`, `deploy`, then
  `eval --evaluators rubric_judge`. Never AgentCore's managed LLM-as-a-judge
  evaluators: they call Bedrock directly, which participant roles cannot.
- Raising in `invoke()` or at import time (e.g. reading a missing env var at
  module level) → HTTP 424; a tool should return an error string instead. Check
  `AGENT_LOG_GROUP` (bootcamp-debugger).
- Heavy work at import time slows cold starts; build agents inside `invoke()`.

## Output shape

Give: (1) a diff of `phase2/app/agent/agent.py` (and `requirements.txt` if
needed), (2) the `deploy` → `test --only 4` → `invoke` commands, (3) one
prompt that should trigger the new feature and what to look for in the trace.
