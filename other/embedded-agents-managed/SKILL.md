---
name: embedded-agents-managed
description: "Only when Managed Agents is asked for, or an agent needs a hosted sandbox: Claude runs the loop in the cloud and calls functions in your app."
---

# Embedded agents on Claude Managed Agents

**Keep the Messages API unless one of two reasons holds.** The owner asks for Anthropic to run the loop and keep the conversation, or an agent needs a hosted sandbox to run code. Otherwise apply the `embedded-agents-messages-api` skill: it is as fast, and the conversation stays in the app's own hands. One tool call took 3.4 s there and 3.8 s here, the medians of five runs each (observed `2026-11-25`).

**Build no agent without its card.** Apply the `embedded-agents-design` skill first: the card fixes the agent's job, its exact tools, what code enforces and what waits for a person's click. A change to a tool, a prompt or a limit updates the card in the same change.

**Anthropic runs the loop; the app runs the tools.** The app resolves the caller and opens the conversation's event stream. It runs its own functions when the model asks, and posts the results. Every connection goes out from the app, so it works on localhost with no public address.

**Read the product's own agent instructions before changing its embedded agents.** Read `reference/playbook.md` before changing the wrapper's contract; it holds the measurement behind each choice. Everything here about the platform was observed `2026-11-25`, with Sonnet 5.5, `@anthropic-ai/sdk` 1.14.0 and beta `managed-agents-2026-04-01`, on the direct Claude API. It is a beta: rerun the live suite on every SDK upgrade.

## 1. First use: install the wrapper

**Search for `askAgent` before installing another wrapper.** An agent is the same directory on all three runtimes, so a product that has one can move its agents here unchanged. An agent with MCP servers stays where it is (§ 2).

1. **Install the missing dependencies at exact versions.** Run `npm i @anthropic-ai/sdk@1.14.0 zod server-only` and `npm i -D vitest`. Use Next.js App Router on Node.
2. **Copy the wrapper, route and tests, changing only import paths.**

   | From this skill | To the app |
   |---|---|
   | `templates/agent.ts` | `src/lib/agent.ts`: the wrapper |
   | `templates/route.ts` | `src/app/api/agents/route.ts`: list, stream, transcript, delete |
   | `templates/agent.test.ts` | `tests/unit/agent.test.ts`: the contract, inside `npm test`, no model call |
   | `templates/agents.live.test.ts` | `tests/live/agents.live.test.ts`: every agent against the real model |

   Vitest needs the same `@` alias as `tsconfig.json`. The live test gets its own Vitest config (include `tests/live/**/*.live.test.ts`, `testTimeout: 180_000`, `fileParallelism: false`, and `process.loadEnvFile('.env')` in a `try`) and a script, `agents:live`. It costs money, so it stays out of the gate.
3. **Supply `getCaller(request)` from `src/lib/caller.ts`, even on localhost.** It returns `{ id }` from the session, or `null`. The id is the app's own opaque id, because it names the owner of each conversation. Where people belong to workspaces, it names the workspace and the person, and `getCaller` returns `null` once they lose access; otherwise a former member still reads the conversation.
4. **Create the Console resources once per workspace.** Run `node <skill dir>/scripts/setup-managed.mjs --name <app>` and save the lines it prints: `CLAUDE_AGENT_ID`, `CLAUDE_ENVIRONMENT_ID`, and `CLAUDE_SEARCH_ENVIRONMENT_ID` with `--search-hosts`. It takes the key from `.env`, or from the file `--env` names, and never from the shell. The app and its live tests take an exported `ANTHROPIC_…` variable over `.env`, so unset any you don't mean. Development and production use separate workspaces and keys; apply the `environments` skill.

**Instructions and tools stay in the repository.** The Console holds one placeholder agent. Each new conversation is created with its own model, instructions and tools, so nothing drifts from the code.

## 2. Add an agent

**Give each agent one directory, with `AGENTS.md` as its whole instructions.** Run `node <skill dir>/scripts/new-agent.mjs <name> [--knowledge]`, then fill in the role, sources, answer format and refusals. `listAgents()` finds it, and no agent name appears in code.

- **Put reference files in `knowledge/` and skills in `.claude/skills/<name>/`.** The app serves both with its own tools: `list_files`, `search_files`, `read_file`, `load_skill` and `read_skill_file`. None of it is uploaded. Name those tools in `AGENTS.md`.
- **Move an agent that needs an MCP server to another runtime.** This wrapper refuses a directory with `.mcp.json`, which `new-agent.mjs --mcp` creates. Apply `embedded-agents-messages-api` or `embedded-agents-agent-sdk`.
- **Put facts about the caller in `context`, never user text.** The wrapper adds them after `AGENTS.md` when the conversation starts, and they stay as they were then. Check anything that can change, such as a role or a plan, in the tool.

## 3. Tools that act for the caller

**Build caller tools on every request, around the caller from the session.** Build them in the route and pass them to `openSession`:

```ts
const tools = [
  agentTool({
    name: 'list_invoices',
    description: "List the signed-in subscriber's invoices.",
    input: {},
    run: async () => JSON.stringify(await listInvoices(caller)), // closes over the caller
  }),
];
const run = await openSession({ agent, prompt, sessionId, owner: caller.id, tools, signal });
```

- **Identity is closed over, never a parameter.** No tool takes an email, user, customer or account id. Test the permission in the function the tool calls; apply the `saas-authorization` skill.
- **Let local tools read, show or propose and let the app confirm actions.** Two listeners on one conversation can both run the same call. What can't be taken back is only proposed, and a click runs it once. A tool that writes directly must do no harm when it runs twice.
- **Give proposals a scope that exists before the conversation does.** The session id comes back only after the tools are built. Use a conversation id the app makes itself, or the agent's name where a person has one chat with it. For confirm cards, stream `withCards(run, …)` from `embedded-agents-design` in place of `run`.
- **Validate tool input in the app.** The platform does not check it against the schema. The wrapper does: the model is told which fields are wrong, and `run` never sees them.
- **Control which failures reach the model.** A refusal or a planned failure throws `ToolError(text)`. Any other exception reaches the model as a fixed sentence, and an unknown tool name gets an error.

## 4. Hosted tools, off by default

**Turn on code or search for one agent in its `hosted.json`, never both.** Write `["code"]` or `["search"]`. Code that can reach the network is a way out for data, so the wrapper refuses the pair. List the tool on the agent card as a `wrapper` row.

- **Code runs `bash` in a sandbox with no network.** The setup script makes that environment: no allowed hosts, MCP servers or package managers. Put no credential and no app file in it.
- **Search reaches only the hosts you name.** It needs its own environment: run the setup script again with `--search-hosts a.com,b.com`, bare names with no protocol. With no hosts named, search refuses.
- **Keep search off for an agent that sees a person's private data.** The query leaves.
- **Start new conversations after removing a hosted tool.** An open one keeps what it started with.

## 5. The chat UI

**Keep the session id beside the conversation and send only the new message.** The history lives on the server, so a client cannot forge an earlier turn.

| Call | Does |
|---|---|
| `GET /api/agents` | Lists the agents, for the picker |
| `POST /api/agents` `{ agent, prompt, sessionId? }` | Streams one turn; no id starts a conversation |
| `GET /api/agents?sessionId=…` | Returns `{ messages: [{ role, text }] }` |
| `DELETE /api/agents?sessionId=…` | Deletes the conversation, stopping a running turn first |

- **Read `{ sessionId }`, then `{ text }` chunks, then one last event.** Append chunks as they arrive. `{ done, agent, sessionId, metadata }` ends the reply; `{ error, agent, sessionId }` ends it too, so show it. Where the agent proposes, `{ cards }` comes as well, so read until the stream closes.
- **Start a new conversation on `error_max_budget_usd`.** A conversation whose budget is spent accepts no more messages.
- **Reload the transcript after `error_disconnected` and on page load.** The answer may have finished after the stream broke.
- **Send one message at a time per conversation.** A second one interrupts a tool call the first is waiting on.
- **Render agent output as plain text or sanitized markdown.** Never raw HTML: it is untrusted text, like anything a user typed.

## 6. The boundary, and the test for each layer

**Pin every layer of the boundary with a test.** `agent.test.ts` holds these; add the app's own.

1. **The route takes one known agent from one signed-in caller.** It refuses another origin, a malformed session id, an unknown agent and any history.
2. **A conversation opens only for its owner.** Its metadata names the owner, the agent and the app. Another person's conversation answers 404, exactly like one that doesn't exist.
3. **The tool list is the boundary.** The model can call the caller's tools, the file and skill tools the directory needs, and the one hosted tool it asked for. A reopened conversation runs only the tools it started with.
4. **Every file path is resolved, symlinks included, before a read.** The file tools refuse anything outside `knowledge/` or the skill's directory, and any `.env` file.
5. **The wrapper runs only its own turn.** It ignores events from before its message, and stops when another message starts.
6. **Turn, budget and time limits end the run.** The response that crosses `maxTurns` runs no local tool. A timed-out or abandoned turn is interrupted.

## 7. Before it leaves localhost

- **Set a per-person limit on new conversations and messages.** `maxBudgetUsd`, $1 by default (an assumption), caps one whole conversation, not one message. Anthropic checks it between model requests, so one request can pass it: a 1-cent cap ended at 2 cents. No money cap covers one message in an open conversation; an agent whose card needs one belongs on another runtime.
- **Delete conversations when the person asks and when the account closes.** They stay in Anthropic's workspace until then. Call `deleteSession` and `deleteOwnerSessions`, once for each id the person has, and stop new messages for that account first.
- **Say on the privacy page that Anthropic holds the conversation and the tool results.** Apply the `legal-pages` skill.
- **Log ids, never content.** The route logs the agent, the session, the status and the vendor's request id.
- **Prove a full run streams on the real host.** The app holds the stream while a run lasts, so the host's time limit must cover it. Run a slow tool and a closed tab there, and include the agents' files in the deployment's trace. Only localhost has been tested.
- **Run `npm run agents:live` before releasing any agent, prompt, tool or model change.** Record the run in the product's test-coverage map, and check that each agent's card in the automation doc matches its code.

## 8. Limits

**A conversation keeps the instructions, tools and budget it started with.** A new prompt or tool reaches new conversations only.

**What it leaves out stays out.** There is no reconnecting, event polling, webhooks, remote MCP, vaults, uploaded skills, memory, multi-agent runs or schedules. A broken stream ends the turn; the next message interrupts a tool call left unanswered and continues.

**The app's limits cannot stop what is already running.** A local tool that has started finishes after a timeout, and a hosted call can start before the app sees it.

**It costs tokens, plus $0.08 for each hour a session runs.** Waiting for a local tool is not billed. Search is $10 for 1,000 searches (both from the [price page](https://platform.claude.com/docs/en/about-claude/pricing), read `2026-11-25`).

Each rule's origin, the case that taught it, is in `receipts.md` beside this file; read it when a rule's edge is unclear.

## How you can tell it worked

A signed-in person finishes a turn that calls a local tool, and reloads its transcript. In the live suite a second turn remembers the first, another owner gets no conversation, and an abandoned tool call is recovered.

## Running the scripts

**Run both scripts from the app's repository root.** `<skill dir>` is this skill's installation location. `new-agent.mjs` writes the agent's directory there. `setup-managed.mjs` creates the Console resources whose ids the env file lacks and prints those ids; it edits no file and deletes nothing. A new base agent starts over: conversations made with the old one answer 404. Archiving one is permanent, so the script never does.
