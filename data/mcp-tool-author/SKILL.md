---
name: mcp-tool-author
description: Helps a DataStream Corp bootcamp participant add a new tool to their Phase 2 MCP server (`phase2/app/mcp_server/mcp_server.py`, FastMCP on AgentCore Runtime), explains how it surfaces through the AgentCore Gateway as `DataStreamDatabase___<tool>`, how `deploy` re-syncs the Gateway's tool list, how the stage 7 Cedar policy (default deny) hides it unless a permit exists, why the read-only database makes writing tools impossible, how to add a tool to the Gateway's Lambda target (`phase2/app/weather_lambda/handler.py` + `tools.json`, e.g. `get_us_alerts`), how semantic tool search picks tools, and how to redeploy and verify with `deploy` + `test --only 1/2`. Triggers on "add an MCP tool", "new tool on the MCP server", "add list_tables", "add a describe_table tool", "expose a new database tool", "my tool isn't in the gateway", "DataStreamDatabase___", "gateway doesn't list my tool", "Tool Execution Denied for my new tool", "cedar policy for my tool", "mcp_server.py", "lambda target", "add a weather tool", "get_us_alerts", "tools.json", "Weather___", "semantic tool search". Do NOT use for Strands `@tool`s inside the agent (use agent-feature-builder), for Phase 1's local `phase1/mcp_server.py` beyond a quick prototype, or for failing stage checks unrelated to a new tool (use bootcamp-debugger).
---

# MCP Tool Author

The Phase 2 MCP server is `phase2/app/mcp_server/mcp_server.py`: a FastMCP
app served as stateless streamable HTTP on AgentCore Runtime. It works on
**your own** SQLite copy (`DB_BUCKET`/`DB_KEY` env vars): each microVM
downloads it to `/tmp` once (`ensure_local_db()`), and every query runs on a
**read-only** connection (`connect_read_only(path)`: `mode=ro` plus
`PRAGMA query_only`). Nothing is ever written back to S3. Today it has one
tool, `query_db`.

Helpers to reuse: `execute(query, params=())` runs one statement and returns
the tool's JSON text (`{"data": [...]}`) or an error string; `run_sql(path,
query, params)` returns the rows as a dict; `lock` serialises access.

**Writing tools are impossible by design.** Any INSERT/UPDATE/DELETE returns
`Error: the database is read-only; this tool can only run queries that read data.`
Build tools that read.

`list_tables` and `describe_table` are the participant's Task 1 / Task 2
challenges (checked by `[CHALLENGE]` lines). Give hints (`sqlite_master`,
`pragma_table_info(?)`, the pattern below) rather than pasting a finished
solution, unless the participant asks for it. A good `describe_table` also
returns the distinct values of short text columns (e.g. `projects.status`:
`active` / `planning` / `completed`): SQLite string comparisons are
case-sensitive, so without them the model writes `WHERE status='Active'` and
gets 0 rows.

## How a tool travels

```
@mcp.tool() def my_tool  →  MCP runtime (stage 1)  tools/list: my_tool
                         →  Gateway target "DataStreamDatabase" (stage 2)
                            tools/list: DataStreamDatabase___my_tool
                         →  Cedar policy engine (stage 7, ENFORCE, default deny)
                         →  agent's data_agent finds it with the Gateway's semantic search
                            (search_tools(gateway, DATA_TOOLS): the top 3 matches)
```

The gateway prefixes every tool with `<target name>___` (three underscores).
The agent sees the prefixed name; its `ReadOnlyGuardHook` only inspects tools
whose name ends with `query_db`.

## Procedure

1. **Prototype locally (optional, fast).** Add a similar tool to
   `phase1/mcp_server.py` (it has only `query_db`, no `execute`/`lock`
   helpers) and run `uv run bootcamp.py phase1 t2 "..."`.
2. **Add the tool** to `phase2/app/mcp_server/mcp_server.py`, taking `lock`
   and passing user values as `?` parameters to `execute`:

   ```python
   @mcp.tool()
   def department_headcount(department: str) -> str:
       """Count the employees in one department (by name, e.g. "Engineering"), as JSON rows."""
       with lock:
           return execute(
               "SELECT d.name AS department, COUNT(e.id) AS headcount FROM departments d "
               "LEFT JOIN employees e ON e.department_id = d.id WHERE d.name = ? GROUP BY d.name",
               (department,),
           )
   ```

   Rules: typed args, a docstring whose first line says what it does and when
   to use it, return a string (use `execute` so it is `{"data": [...]}` JSON),
   never raise (`execute` already turns SQL errors into a string). Don't call
   `query_db` from another tool: decorated tools aren't plain functions.
   A tool **without arguments** is called by `test --only 1` / `--only 2` and
   must return JSON rows, or the required check fails.
3. **Deploy:** `uv run bootcamp.py deploy` (rebuilds the zip only if sources
   changed, rolls the MCP runtime). Terraform then re-syncs the Gateway's tool
   list automatically (`terraform_data.gateway_tool_sync`, ~10-20 s).
4. **Verify the runtime, then the gateway:**
   ```bash
   uv run bootcamp.py test --only 1
   uv run bootcamp.py test --only 2
   ```
   The detail lists `tools=[...]`. To call your tool by hand:
   ```bash
   uv run python - <<'EOF'
   from bootcamp import Context
   from bootcamp_cli import agentcore
   out = Context().participant_outputs()
   token = agentcore.get_token(out)
   print(agentcore.list_tools(out["mcp_server_url"], token))
   print(agentcore.list_tools(out["gateway_url"], token))
   print(agentcore.call_tool(out["gateway_url"], token, "DataStreamDatabase___department_headcount", {"department": "Engineering"}))
   EOF
   ```
   (This only *uses* `bootcamp_cli`; it doesn't edit it.)
5. **Gateway still shows only the old tools?** Fallback only (`deploy`
   normally syncs it): re-sync by hand with your participant-role profile
   (`bootcamp-<name>`, see bootcamp-operator):
   ```bash
   aws bedrock-agentcore-control list-gateway-targets --gateway-identifier <GATEWAY_ID> --profile bootcamp-<name>
   aws bedrock-agentcore-control synchronize-gateway-targets --gateway-identifier <GATEWAY_ID> \
     --target-id-list <TARGET_ID> --profile bootcamp-<name>
   ```
6. **Exercise via the agent:** `uv run bootcamp.py invoke "How many people work in Engineering?"`,
   then `uv run bootcamp.py traces` (stage 5+) to see which tool was called.

## A tool on the Lambda target instead (weather-like tools)

Not every tool belongs on the MCP server. The Gateway's second target,
`Weather`, is a **Lambda target**: `phase2/app/weather_lambda/handler.py`
(the Gateway invokes it with the tool's arguments as the event and the tool
name in `context.client_context.custom["bedrockAgentCoreToolName"]` as
`Weather___<tool>`). To add one (the Task 2 Part B challenge is
`get_us_alerts(area)`):

1. A function `(arguments: dict) -> str` in `handler.py`, registered in
   `TOOLS`. Reuse `nws_weather.make_client()` / `fetch_json`; return a few
   short lines, never raw JSON (every character is model input). `handler`
   wraps the text as an MCP result (`mcp_text`) so it reaches the model
   unquoted.
2. Its schema in `phase2/app/weather_lambda/tools.json` (same `name`;
   `inputSchema.properties` types: string/number/integer/boolean).
   Terraform builds the target's inline schema and the stage 7
   `weather_tools_policy` permit from this file, so there is nothing else to
   change and Cedar will not hide it.
3. New dependency? Add it to `requirements.in`, re-compile
   `requirements.txt` (`uv pip compile requirements.in --python-platform
   aarch64-manylinux2014 --python-version 3.13 --only-binary :all: -o
   requirements.txt`).
4. `uv run bootcamp.py deploy`, then `test --only 2` (`[CHALLENGE]` line for
   `get_us_alerts`). The weather specialist keeps only its top search result
   (`WEATHER_TOOLS = (..., 1)` in `agent.py`): raise it to 2 so it gets the new
   tool too. Logs: `/aws/lambda/awsworkshop-<name>-weather`.

Check how search ranks a tool and what it costs in prompt tokens:
`uv run bootcamp.py tools --search "active weather alerts in California"`.

## Stage 7: Cedar default deny

At stage 7 the gateway enforces these policies in `terraform/participant/`:

- `safe_query_policy.cedar` permits `DataStreamDatabase___query_db` only for
  a query starting with `SELECT`/`WITH`/`EXPLAIN` (UPPER, lower or Title
  case) and a space, tab, newline or CR, or with `PRAGMA table_info(` (no `=`
  or `;`); with no `--` / `/*` comment and no `INSERT`/`UPDATE`/`DELETE`/
  `REPLACE`/`DROP` in those cases followed by whitespace. It matches text, not
  SQL: mixed case (`sElEcT`), leading whitespace and a keyword inside a name
  (`last_update `, `LIKE '%delete %'`) are denied too.
- `schema_tools_policy.cedar` permits `___list_tables` and `___describe_table`,
  but only if `mcp_server.py` defines them (Terraform greps for
  `def list_tables(` / `def describe_table(`).
- `weather_tools_policy` (same template) permits every `Weather___<tool>` in
  `phase2/app/weather_lambda/tools.json`.

Every **other** new tool is denied by default: it disappears from
`tools/list` at stage 7 and a call fails with `Tool Execution Denied`. That is
the policy working, not a bug. Options:

1. Stay at stage <= 6 while developing (`uv run bootcamp.py up 6`).
2. Ask the instructor for a permit (`terraform/` is platform-owned).

Cedar's `like` patterns are case-sensitive, so a mixed-case write such as
`dElEtE` passes Cedar; the read-only database refuses it. The read-only
connection is the real guarantee; Cedar and the agent guard are extra layers.

## Common pitfalls

- Calling the runtime name (`my_tool`) on the gateway: use
  `DataStreamDatabase___my_tool`.
- f-string SQL with model-supplied values → injection. Use `?` parameters
  (`execute(sql, (value,))`); identifiers such as table names can't be
  parameters, so pass them to a table-valued function like `pragma_table_info(?)`.
- Forgetting `with lock:` around `execute`.
- New import missing from `phase2/app/mcp_server/requirements.txt` (wheel-only,
  linux/arm64, py3.13) → stage 1 fails; check the MCP runtime logs.
- Agent never calls the tool → sharpen the docstring and mention it in the
  `data_agent` prompt (see agent-feature-builder).

## Output shape

Give: (1) a diff of `phase2/app/mcp_server/mcp_server.py`, (2) the
`deploy` → `test --only 1` → `test --only 2` → verification snippet commands,
(3) the gateway tool name `DataStreamDatabase___<tool>`, (4) one line on
whether stage 7 will hide it and what to do.
