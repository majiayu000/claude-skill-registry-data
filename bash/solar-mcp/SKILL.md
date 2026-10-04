---
name: solar-mcp
description: >
  Solar's own MCP server: read-only context as resources, verbs as tools behind
  a gate that validates authority and mandate in the handler and refuses on its
  own. Use it to connect any MCP client to Solar without opening the workspace.
---

# Solar MCP

A client connects from any folder, reads Solar's context as **resources**, and
calls **tools** that cannot execute until the handler says so. The refusal is
the point: it does not depend on the calling agent choosing to behave.

Runtime dependencies: `core/skills/solar-client/`, `core/skills/solar-app/`,
`core/skills/solar-router/`, `core/skills/solar-async-tasks/` and
`core/skills/solar-telegram/` (private sending implementation, not an agent tool).

## Required MCP

None. This *is* the server.

## CLI

Each client starts `solar mcp` as a stdio child; that child does not use a LaunchAgent.
Register once at user level; do not copy per-planet MCP configurations.
Python 3.11+ is required for registration; entries pin the interpreter for GUI launches.

```bash
solar mcp
solar mcp print --workspace /path/to/workspace
solar mcp install --workspace /path/to/workspace --dry-run
solar mcp install --workspace /path/to/workspace
solar mcp uninstall --dry-run
solar mcp uninstall
```

Client destinations, recovery and validation: [references/clients.md](references/clients.md).

## Approval workflow

1. Prepare the exact action, scope and destination. For Telegram include an explicit
   `chat_id` and final text; apply the relevant communication gate first.
2. Call the tool without `approval_id`. On clients advertising MCP form elicitation,
   the runtime presents the exact action for confirmation, creates the approval and
   executes internally. Do not ask the user to create or copy an identifier.
3. Do not ask for conversational confirmation immediately before that native prompt.
   An existing valid approval may be passed internally and does not prompt again.
4. Never manufacture consent with `approved=true`, an agent-authored note or a shell
   grant. If the client lacks elicitation, report the integration limitation and use
   a trusted operator/host approval path. Never bypass the gate.
5. Report success only from the execution result. On uncertain failure, check the
   resulting state before requesting another execution.

An explicit local instruction can provide A2-implicit authority, but MCP does not
carry the original user turn. Until a trusted host binds that instruction to the
exact call, this server requires native confirmation. Do not claim to verify
conversational authority from caller-supplied fields. See
[references/approvals.md](references/approvals.md) for trust boundaries and operator recovery.

## Resources (open)

| URI | What it serves |
|---|---|
| `solar://health` | Storage, gateway and continuity, as the console sees them |
| `solar://tasks` | Tasks in `state.sqlite`, by state, with recurrence |
| `solar://index` | Counts from the views in `state.sqlite` |
| `solar://delegations` | Written A3 mandates: mode and validity |
| `solar://gate` | What this server allowed and refused |

## Tools (gated)

| Tool | Authority | Passes when |
|---|---|---|
| `solar_task_status` | A0 | Always. Reading is not gated. |
| `solar_task_create` | A2 | Native client confirmation or an existing exact-call approval. Stores a draft through `solar-state` and refuses when the format is not `sqlite` |
| `solar_task_approve` | A2 | Same approval. Moves a draft, or a task already planned, to the queue. Refuses an A3 mandate. Does not change object, scope or effect |
| `solar_task_cancel` | A2 | Same approval. Cancels a queued task, or records the request for an active one. Does not change object, scope or effect |
| `solar_task_requeue` | A2 | Same approval. Moves an error task back to the queue and drops its `## Execution Error` section. Does not change object, scope or effect |
| `solar_telegram_send` | A2 | Same, for one exact message text. Sending outside the machine is never implicit |
| `solar_action_run` | A3 | The skill and action are registered **and** the mandate is live |

`tools/list` and `resources/list` are the catalog. A name that is not there
is not this server. An unknown resource URI is refused with the known list.

Approvals are server-side records: they name one tool and one set of arguments,
expire, bind the workspace, and are reserved before the first execution attempt. Tool arguments cannot mint one. A trusted client confirmation response can;
the MCP client is part of the trust boundary.

Action skills are opt-in, listed in `<runtime>/mcp/action-skills.json`:

```json
{"example-sync": {"actions": ["status"], "mandate": "example-sync-mandate",
                  "command": ["bash", "planets/<planet>/skills/example-sync/scripts/example_sync.sh"]}}
```

**Instruction skills never become tools.** They stay native to the harness; only
action verbs pass through here.

## Sending Telegram

`solar_telegram_send` is the route an agent has to Telegram, and the reason the
`solar-telegram` skill is no longer published to any client. The bot token is an
installation secret held by the process
(`<app data>/Solar/secrets/installation.env`, 0600): the server reads it and
hands it to `send_telegram.sh`, which refuses to look it up on its own.

The approval covers the exact text. Change a word and the call is refused with
`approval_scope_mismatch`, because the hash covers the arguments, not the tool
name alone. The chat must be the configured one or listed in
`TELEGRAM_ALLOWED_CHAT_IDS`.

## Clients in front of the gate

Client tool allowlists and native Solar confirmation serve different purposes.
A generic "allow this tool" card does not approve its exact destination and content.
The runtime uses [MCP form elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)
when supported. Clients must route that request to the human, never to the model.

## Where the guarantee ends

Inside: the Solar runtime and this server, with installation secrets the process
custodies. The two keys Solar sends with are no longer in a file the IDE indexes.

Outside, and said plainly rather than disguised:

- a process running as the user can read the 0600 store; this closes the
  mediated route, not the machine;
- a browser session already authenticated is untouched — `zoho-mail`,
  `whatsapp`, `linkedin-messages` and `linkedin-analytics` remain declarative,
  not coercive, until their send becomes a gated tool;
- the `.env` of a planet is the planet's. Solar does not mediate it.

## Runtime dependencies

Starting the stdio child does not start Solar services. Tools still depend on
Solar's configured workspace, runtime storage and (for sends) installation secrets.
Task verbs write only through `solar-state` and refuse when the runtime format is not `sqlite`. The supervised
orchestrator processes queued tasks separately. Console and background services
have their own startup/LaunchAgent lifecycle. A connected MCP child is not evidence
that the queue worker, console or transport is running.
