---
name: acp-engineering
description: Speak both ACPs — Agent Client Protocol sessions and Agent Communication Protocol runs, done right.
version: 1
triggers: acp, agent client protocol, agent communication protocol, agent sessions
category: How Milo works
blurb: Work with both ACP flavours — editor agent sessions and agent-to-agent runs — the correct way.
archetype: knowledge
example: Set up an ACP session so another agent can drive this app.
---

# ACP Engineering

"ACP" is two protocols — and we speak both: the **Agent Client Protocol** (editors ↔ agents, stdio sessions) and the **Agent Communication Protocol** (agent ↔ agent REST runs). Implement them cleanly, test them like contracts.

## When to use
- Exposing an app/service as an ACP agent (either flavor).
- Building editor integrations or agent-to-agent run loops.
- Reviewing hand-rolled protocol implementations before production.

## Method
1. **Know which ACP you mean** — always disambiguate in docs and code:
   - *Agent Client Protocol (agentclientprotocol.com)*: `initialize` → `session/new` → `session/prompt` with streamed `session/update` chunks; permissions; stdio JSON-RPC.
   - *Agent Communication Protocol (agentcommunicationprotocol.dev)*: REST — `GET /agents`, `POST /runs` (sync/async/stream), `GET /runs/:id`, cancel; message parts with content types.
2. **Protocol adapters stay thin**: one core, protocol sits at the edge (`agent-commands`-style mapping); no business logic in the wire layer.
3. **Session/run lifecycle correctness**: handle unknown sessions, cancels, errors, and reconnects; never leak state across sessions.
4. **Streaming discipline**: order updates; bounded chunk sizes; backpressure awareness; clear terminal states (stopReason / run status).
5. **Minimal-but-honest implementations**: hand-rolled okay for reference; label spec versions supported; note unimplemented modes (e.g., stream) — never fake compliance.
6. **Production upgrade path**: official SDKs when the surface grows; keep the adapter tests so swaps are safe.
7. **Security**: remote ACP endpoints require auth (tokens/mTLS); validate all inputs; cap output sizes; sandbox any tool execution triggered via prompts (see guardrails skill).
8. **Contract tests**: scripted client covering handshake, happy path, error path, cancel — in CI, per protocol.

## Quality gates
- [ ] Disambiguated naming in docs/code ("ACP-client" vs "ACP-comm").
- [ ] Lifecycle tests: session/run happy + error + cancel.
- [ ] Spec version + supported subset documented.
- [ ] Remote endpoints authenticated; inputs validated.

## Red lines
- No unauthenticated remote endpoints; no pretending unsupported features work.

## Related
`mcp-engineering` · `agent-interoperability` · `multi-surface-webapp` (shipped ACP adapters).
