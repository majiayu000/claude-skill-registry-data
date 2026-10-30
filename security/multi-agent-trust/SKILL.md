---
name: multi-agent-trust
description: Detects agent-to-agent calls without authentication, authorization, or
  permission scoping. Use when writing code that calls other agents, spawns
  subagents, builds multi-agent pipelines, or passes messages between LLM
  agents. Also invoke when an orchestrator delegates tasks to worker agents or
  when agents share tools and permissions.
---

# Multi-Agent Trust Boundaries (LLM08:2025)

## What this checks

Detects agent-to-agent calls that lack authentication, authorization, or permission
scoping. When agents blindly trust messages from other agents, a compromised or
malicious agent can hijack the entire pipeline.

## Vulnerable patterns

- Inter-agent call dispatched with no authentication header or signed token
- Worker or subagent initialized with the orchestrator's full credentials and complete tool scope
- Output from one agent passed as input to the next without schema validation
- Receiver that trusts a sender identity claim with no cryptographic verification

## Fix immediately

Flag the vulnerable call site and explain the risk. Then suggest a fix that
establishes these properties:

1. **Authentication on every agent-to-agent call.** A shared secret, signed token,
   or mTLS credential is attached by the caller and verified by the receiver
   before any task runs. A sender-name field is not authentication.
2. **Least privilege per agent.** Each agent is initialized with the smallest
   set of tools, credentials, and scopes it needs to complete its task — never
   the orchestrator's full set. A compromised worker should not have the keys
   to compromise the rest of the pipeline.
3. **Schema validation on every received message.** Treat messages from other
   agents as untrusted input: validate against a schema, reject unexpected
   fields, and refuse to execute free-form instructions embedded in the payload.
4. **No blind execution of peer-supplied instructions.** Agent output that names
   a tool or action is routed through the same policy gate as a user request,
   not auto-dispatched.

Translate each principle to the transport, auth library, and validator of the
audited code. Use the framework's documented auth-middleware and schema-validation
APIs — do not roll your own.

## Verification

- [ ] For every outbound agent-to-agent call present, an auth header or signed token is attached
- [ ] For every agent-to-agent receiver handler present, the auth token is verified before processing
- [ ] Each agent is initialized with the minimum permissions needed for its task
- [ ] For every response received from another agent, the payload is validated against a schema before use
- [ ] No agent blindly executes instructions received from another agent

## References

- CWE-306 ([Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/306.html))
- CWE-272 ([Least Privilege Violation](https://cwe.mitre.org/data/definitions/272.html))
- [OWASP LLM08:2025 Excessive Agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP Agentic AI Top 10:2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
