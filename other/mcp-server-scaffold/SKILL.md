---
name: mcp-server-scaffold
description: Scaffold and govern an MCP server as a bounded tool seam. Defines which tools the agent may call, enforces the principle that agents call tools and tools call infrastructure. Trigger when adding or reviewing an MCP server in an agent system.
---

# MCP Server Scaffold

> **Agents call tools. Tools call infrastructure. This boundary is the governance seam. Do not collapse it.**

An MCP server is a contract between an agent and the capabilities it is allowed to use. Its value is not in what it exposes — it is in what it deliberately withholds.

## When to use

- Adding a new MCP server to an agent system
- Reviewing an existing MCP server for scope creep or security gaps
- Deciding which capabilities to expose to an agent (and which to explicitly deny)
- Governing an agent that has been given "too much access"

## Procedure

1. **Define the tool seam** — before writing any server code, list:
   - What capabilities does the agent legitimately need?
   - What capabilities does the underlying system have that the agent must NOT access?
   - What is the minimum viable tool surface?

2. **Author the tool manifest** — for each tool:
   ```
   Tool: <name>
   Description: <one sentence — what it does and when to call it>
   Input schema: <typed fields with constraints>
   Output schema: <typed fields>
   Side effects: <what it changes in the world — none / read-only / write / external-call>
   Auth required: <yes/no and mechanism>
   Rate limit: <calls/minute or none>
   ```

3. **Enforce least-privilege at the server** — the MCP server holds the credentials and enforces the scope. The agent receives only the tool interface. Key rules:
   - Read tools and write tools are separate, explicitly named operations.
   - No tool exposes raw SQL, raw shell execution, or raw filesystem access.
   - No tool accepts arbitrary code or query strings from the agent without validation.

4. **Add input validation at the boundary** — every tool validates its inputs before executing. Reject malformed inputs with a structured error, not an exception trace.

5. **Log every tool invocation** — at minimum: tool name, caller identity, input summary (no secrets), output summary, timestamp, and latency. These logs are your audit trail.

6. **Test the refusal surface** — confirm that:
   - A call to a non-existent tool returns a clean error, not a server crash.
   - An out-of-scope request (e.g. an agent trying to read data it is not authorised for) is rejected with a clear error.
   - Invalid inputs are rejected before any side effect occurs.

7. **Document the scope boundary** — in the MCP server's README or SKILL.md, explicitly state what the server does NOT expose and why. Scope boundaries that are not documented drift.

8. **Run the Adversarial Gate** — common MCP failure modes: overly broad tool descriptions that invite misuse, missing input validation that allows prompt injection via tool arguments, write tools with no confirmation step, no rate limiting on expensive operations.

## Outputs

- Tool manifest (one entry per tool)
- MCP server skeleton with input validation and structured error responses
- Refusal surface test cases
- Scope boundary documentation

## Guardrails

- **No raw database access through an MCP tool.** Tools call repositories or services; repositories call databases.
- **Tool descriptions are part of the attack surface.** Vague descriptions invite misuse by the agent. Be precise.
- **No secrets in tool outputs.** If a tool must return an identifier, return the identifier — not the credential.
- **Scope creep is the default failure mode.** When in doubt, add a new tool rather than broadening an existing one.
