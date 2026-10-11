---
name: mcp-a2a
description: Use this skill when the user is combining the Model Context Protocol or Agent2Agent with a Microsoft Teams bot on Teams SDK 2.1 — using a remote MCP server's tools in the agent, exposing the Teams bot as an MCP server (`find_user`, `notify`, `ask`, `request_approval`) with `@modelcontextprotocol/sdk`, bot-to-bot hand-off over A2A with `@a2a-js/sdk`. Triggers on "Teams MCP", "MCP server Teams", "expose Teams as MCP", "MCP client Teams bot", "A2A Teams", "human in the loop Teams".
---

# MCP and A2A with a Teams bot

The Teams SDK has **no MCP or A2A plugins any more** — the old packages for them are deprecated on npm. You use the protocol SDKs directly and mount them next to the bot:

| Package | Role |
|---|---|
| `@modelcontextprotocol/sdk` | MCP client (`Client`) and MCP server (`McpServer`) |
| `@a2a-js/sdk` | A2A client and server |
| `openai` | The model loop that uses the tools (`ai-agents`) |

The reference samples are `examples/mcp-server`, `examples/ai-mcp` and `examples/a2a` in `microsoft/teams.ts`.

## 1. Use a remote MCP server's tools in the agent

Connect once at startup, list the tools, wrap each as a `RunnableToolFunction` for `runTools()` (`ai-agents`):

```ts
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import type { RunnableToolFunction } from 'openai/lib/RunnableFunction';

export async function loadMcpTools(url: string): Promise<RunnableToolFunction<Record<string, unknown>>[]> {
  const client = new Client({ name: 'teams-bot', version: '0.0.0' });
  await client.connect(new StreamableHTTPClientTransport(new URL(url), {
    requestInit: { headers: { Authorization: `Bearer ${process.env.MCP_SERVER_TOKEN ?? ''}` } },
  }));

  const { tools } = await client.listTools();
  return tools.map((tool) => ({
    type: 'function',
    function: {
      name: tool.name,
      description: tool.description ?? '',
      parameters: (tool.inputSchema as Record<string, unknown>) ?? { type: 'object' },
      function: async (args: Record<string, unknown>) => {
        const result = await client.callTool({ name: tool.name, arguments: args });
        return JSON.stringify(result.content);
      },
      parse: (raw: string) => JSON.parse(raw) as Record<string, unknown>,
    },
  }));
}
```

Then pass the result as `tools` to `runTools`. Rules of thumb: connect at startup, not per turn; give each tool a unique name across local and MCP tools; treat the server's tool output as untrusted text; keep tokens in the environment.

## 2. Expose the Teams bot as an MCP server

An MCP server inside the bot lets an outside agent reach real people in Teams — look a user up, notify them, ask a question, request an approval. Tools are registered on an `McpServer`, with Zod schemas, and the transport is mounted on the **same Express server** that hosts `/api/messages`.

```ts
import { randomUUID } from 'node:crypto';
import http from 'node:http';
import express from 'express';
import { z } from 'zod';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { isInitializeRequest } from '@modelcontextprotocol/sdk/types.js';
import { App, ExpressAdapter } from '@microsoft/teams.apps';
import * as endpoints from '@microsoft/teams.graph-endpoints';

const expressApp = express();
const app = new App({ httpServerAdapter: new ExpressAdapter(expressApp) });   // the Express app that also serves /mcp

function createMcpServer(): McpServer {
  const server = new McpServer({ name: 'teams-bot', version: '0.0.0' });

  server.registerTool(
    'find_user',
    {
      description: 'Find users in this tenant by name, email or UPN. Returns up to 5 matches with their object ids.',
      inputSchema: { query: z.string().describe('Name, email or UPN fragment') },
      outputSchema: { matches: z.array(z.object({ id: z.string(), displayName: z.string().nullable() })) },
    },
    async ({ query }) => {
      const result = await app.graph.call(endpoints.users.list, {
        ConsistencyLevel: 'eventual',
        $search: `"displayName:${query}" OR "userPrincipalName:${query}"`,
        $select: ['id', 'displayName'],
        $top: 5,
      });
      const matches = (result.value ?? []).map((u) => ({ id: u.id!, displayName: u.displayName ?? null }));
      return { structuredContent: { matches }, content: [{ type: 'text', text: JSON.stringify(matches) }] };
    },
  );

  server.registerTool(
    'notify',
    {
      description: 'Send a notification to a Teams user. No answer expected.',
      inputSchema: { userId: z.string().describe('Entra object id'), message: z.string() },
      outputSchema: { notified: z.boolean() },
    },
    async ({ userId, message }) => {
      const conversationId = await getOrCreateConversation(userId);
      await app.send(conversationId, message);
      return { structuredContent: { notified: true }, content: [{ type: 'text', text: 'notified' }] };
    },
  );

  return server;
}

// the 1:1 conversation with a user: reuse a stored id, or open one proactively
async function getOrCreateConversation(userId: string): Promise<string> {
  const stored = await loadConversation(userId);
  if (stored) return stored;
  const conversation = await app.api.conversations.create({
    tenantId: process.env.TENANT_ID!,
    members: [{ id: userId, role: 'user', name: userId }],
  });
  if (!conversation.id) throw new Error('No conversation id returned');
  await saveConversation(userId, conversation.id);
  return conversation.id;
}
declare function loadConversation(userId: string): Promise<string | undefined>;
declare function saveConversation(userId: string, conversationId: string): Promise<void>;

// the MCP route is YOUR route: the Teams SDK does not authenticate it
function requireMcpToken(req: express.Request, res: express.Response, next: express.NextFunction) {
  if (req.headers.authorization !== `Bearer ${process.env.MCP_TOKEN ?? ''}` || !process.env.MCP_TOKEN) {
    res.status(401).end();
    return;
  }
  next();
}

const transports = new Map<string, StreamableHTTPServerTransport>();

expressApp.post('/mcp', requireMcpToken, express.json(), async (req, res) => {
  const sessionId = req.headers['mcp-session-id'] as string | undefined;
  let transport = sessionId ? transports.get(sessionId) : undefined;

  if (!transport && isInitializeRequest(req.body)) {
    // one transport and one McpServer per client session
    transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
      onsessioninitialized: (id) => { transports.set(id, transport!); },
    });
    await createMcpServer().connect(transport);
  }
  if (!transport) {
    res.status(400).json({ error: 'unknown MCP session' });
    return;
  }
  await transport.handleRequest(req, res, req.body);
});

async function main() {
  await app.initialize();                      // registers /api/messages on expressApp
  http.createServer(expressApp).listen(Number(process.env.PORT) || 3978);
}
main().catch(console.error);
```

Notes:

- `app.graph` calls Graph as the bot's own identity; `User.Read.All` (application) needs admin consent.
- `app.initialize()` first, then the server starts — the Teams SDK does not own the lifecycle here (`sdk-patterns`).
- `app.send(conversationId, …)` to a user who never wrote to the bot needs the conversation created first (above) and the app installed for that user.
- Run the token check before the body parser, so unauthenticated callers cost nothing.

### Human in the loop: `ask` and `request_approval`

Pattern: the tool sends a card, records the pending request **before** sending, and returns a request id; a second tool (`wait_for_reply`, `wait_for_approval`) waits on a promise with a timeout; the card's action handler resolves it.

```ts
import { randomUUID } from 'node:crypto';
import { AdaptiveCard, ExecuteAction, SubmitData, TextBlock, TextInput } from '@microsoft/teams.cards';

type Pending = { status: 'pending' | 'answered'; reply?: string; resolve: () => void; done: Promise<void> };
const pendingAsks = new Map<string, Pending>();

function newPending(): Pending {
  let resolve!: () => void;
  const done = new Promise<void>((r) => { resolve = r; });
  return { status: 'pending', resolve, done };
}

export async function ask(conversationId: string, question: string): Promise<string> {
  const requestId = randomUUID();
  pendingAsks.set(requestId, newPending());                  // before sending: a fast reply must not be lost
  const card = new AdaptiveCard(
    new TextBlock(question, { weight: 'Bolder', wrap: true }),
    new TextInput().withId('reply').withIsMultiline(true).withIsRequired(true),
  ).withActions(
    new ExecuteAction({ title: 'Send' })
      .withData(new SubmitData('ask_reply', { request_id: requestId }))
      .withAssociatedInputs('auto'),
  );
  await app.send(conversationId, card);
  return requestId;
}

export async function waitForReply(requestId: string, timeoutSeconds = 30) {
  const entry = pendingAsks.get(requestId);
  if (!entry) throw new Error(`No ask with id ${requestId}`);
  if (entry.status === 'pending') {
    await Promise.race([entry.done, new Promise<void>((r) => setTimeout(r, timeoutSeconds * 1000))]);
  }
  return { status: entry.status, reply: entry.reply ?? null };
}

app.on('card.action.ask_reply', async ({ activity }) => {
  const { request_id: requestId, reply } = activity.value.action.data as { request_id?: string; reply?: string };
  const entry = requestId ? pendingAsks.get(requestId) : undefined;
  if (entry?.status === 'pending') {
    entry.status = 'answered';
    entry.reply = reply ?? '';
    entry.resolve();                                           // wakes waitForReply
    return { statusCode: 200, type: 'application/vnd.microsoft.activity.message', value: 'Reply recorded' } as const;
  }
  return { statusCode: 200, type: 'application/vnd.microsoft.activity.message', value: 'That request is no longer valid.' } as const;
});
```

Register `ask` and `waitForReply` as MCP tools the same way as `notify`. An approval is the same shape with two `ExecuteAction` buttons (`approved` / `rejected` in the extra data). Keep pending state in a shared store if more than one instance runs.

## 3. Bot-to-bot hand-off with A2A

A2A (`@a2a-js/sdk`) lets two bots — each with its own agent — pass a user between them: the sender calls the peer's A2A endpoint with the user's identity and a summary, and the peer opens a proactive 1:1 chat with the user.

What is stable across SDK versions is the wiring: the agent card at `/.well-known/agent-card.json`, JSON-RPC at `/a2a`, a request handler with an executor, all on the same Express app as the bot:

```ts
import express from 'express';
import { DefaultRequestHandler, InMemoryTaskStore } from '@a2a-js/sdk/server';
import type { AgentExecutor, ExecutionEventBus, RequestContext } from '@a2a-js/sdk/server';
import { agentCardHandler, jsonRpcHandler, UserBuilder } from '@a2a-js/sdk/server/express';
import { Client as TeamsApiClient } from '@microsoft/teams.api';
import { App, ExpressAdapter } from '@microsoft/teams.apps';
import type { AgentCard } from '@a2a-js/sdk';

declare const agentCard: AgentCard;                      // built per the A2A version you pin; see examples/a2a/src/types.ts

class HandoffExecutor implements AgentExecutor {
  constructor(private readonly teams: App) {}

  execute = async (_ctx: RequestContext, bus: ExecutionEventBus): Promise<void> => {
    // 1. read the hand-off (user id, tenant, serviceUrl, summary) from the inbound data part
    // 2. open a 1:1 with that user against THEIR service URL
    const api = new TeamsApiClient('https://smba.example.com/teams/', this.teams.api.http);
    void api;
    // 3. send the greeting with this.teams.send(conversationId, …)
    // 4. publish an acknowledgement on the bus so the sender's call resolves
    bus.finished();
  };

  cancelTask = async (): Promise<void> => {};
}

const expressApp = express();
const app = new App({ httpServerAdapter: new ExpressAdapter(expressApp) });

const handler = new DefaultRequestHandler(agentCard, new InMemoryTaskStore(), new HandoffExecutor(app));
expressApp.use('/.well-known/agent-card.json', agentCardHandler({ agentCardProvider: handler }));
expressApp.use('/a2a', jsonRpcHandler({ requestHandler: handler, userBuilder: UserBuilder.noAuthentication }));
```

- **Pin the major version of `@a2a-js/sdk`.** The agent card and message part shapes differ between the 0.3 and 1.x lines, and the official guide and sample were written against different ones. Copy the shapes from `examples/a2a` for the version in your `package.json`, not from memory.
- `UserBuilder.noAuthentication` is for a lab. A peer endpoint that is reachable from the internet needs real authentication.
- Never trust the hand-off payload: validate every field with a type guard before opening a conversation, and refuse hand-offs back to the sender to avoid ping-pong.

## Common pitfalls

- **The MCP endpoint is open** — nothing in the Teams SDK protects `/mcp` or `/a2a`; add authentication yourself.
- **404 on `/api/messages`** — `app.initialize()` was never awaited, or the adapter wraps a different server than the one that listens.
- **A tool fires twice** — it exists locally and through an MCP wrapper under the same name.
- **`wait_for_*` returns `pending` forever** — the pending entry was created after the card was sent, or the action handler looks it up with another id.
- **A notification fails with 403** — the app is not installed for that user, or the stored conversation id is stale.