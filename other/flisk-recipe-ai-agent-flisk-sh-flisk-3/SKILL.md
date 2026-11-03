---
name: flisk-recipe-ai-agent
description: Recipe for "build me an AI agent with MCP tools and a database" with Flisk - an agent service with sessions, an MCP tools server and a backend with a database in one stack, started with `flisk up`. Use with the flisk-build skill when the user asks for an AI agent, chatbot, assistant, MCP server or tools for an agent.
license: MIT
compatibility: Requires the flisk CLI, Docker and Tilt on the local machine. Does not deploy.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Recipe: an AI agent with MCP tools and a database

**Parts:** an agent that keeps a conversation per session, an MCP server with the agent's tools, and a backend that stores the data the tools read and write.

## Steps

```bash
flisk doctor
flisk project --yes
flisk resource assistant --type agent --stack ai --yes
flisk resource tools-mcp --type mcp --stack ai --yes
flisk resource notes-api --type backend --stack ai --feature drizzle --yes
flisk up ai --dry-run
flisk up ai --json &          # wait for {"ok":true}
flisk networks --stack ai --raw
```

Keep the agent on the default session storage (a named volume). In Flisk 1.4.2 an agent created with `--durability postgres` fails its image build (`TS7016: Could not find a declaration file for module 'pg'`); use the `notes-api` backend for the database instead.

## App code

- `notes-api`: a `notes` table (`src/schema.ts`) and `GET /notes`, `POST /notes`. Keep `/health` and `/health/db`.
- `tools-mcp`: tools such as `list_notes` and `add_note` that call `notes-api`.
- `assistant`: the agent contract is already in place: `/health`, `/ready`, `POST /turn` and `GET /session` with an `x-session-id` header. Put the agent's logic in the turn handler. If the user gives a model API key, list its name under `secrets.required` in `service.json` and put the value in the project `.env`.

## Done when

Each answers 200 on `api.<project>.localhost:<port>`: `/api/assistant/health`, `/api/assistant/ready`, `/api/tools-mcp/health`, `/api/notes/health`, `/api/notes/health/db`. Then send one turn:

```bash
curl -s -X POST -H 'x-session-id: demo' -H 'content-type: application/json' \
  -d '{"input":"hello"}' http://api.<project>.localhost:<port>/api/assistant/turn
```

Tell the user the three URLs, how to talk to the agent (the `curl` above), and that `flisk agent sessions assistant --session-id demo` shows the saved conversation.
