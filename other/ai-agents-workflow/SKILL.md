---
name: ai-agents-workflow
metadata:
  version: "2.2.0"
allowed-tools: bash view create_file str_replace web_search
description: >
  Builds and implements AI agents, automation workflows, and tool integrations — MCP servers
  (2025 async, OAuth, stateless spec), LangChain and CrewAI agents, multi-LLM orchestration,
  and no-code platforms. Activates on MCP server, build an agent, tool integration, API
  orchestration, multi-LLM routing, OAuth flow, webhook, connect services, deploy a workflow,
  integrate external APIs. Not for conceptual architecture overviews (use orchestrating-ai-
  agents), not for production n8n incident ops (use operating-n8n-production), and not for
  pure no-code platform wiring (use workflow-automation).
---

## Evals

- ✅ **SHOULD TRIGGER** — "Build a LangGraph agent with memory and tool use."
- ✅ **SHOULD TRIGGER** — "Write the Python code for a CrewAI agent that handles client intake."
- ✅ **SHOULD TRIGGER** — "Implement an MCP server for our ticketing system."
- ❌ **SHOULD NOT TRIGGER** — "Design how I should structure my multi-agent system before I build it" → route to orchestrating-ai-agents.
- ❌ **SHOULD NOT TRIGGER** — "Connect n8n to Base44 using no-code" → route to workflow-automation.

## When to Use / When NOT

**Use when** — "build an MCP server with OAuth that connects our CRM." "orchestrate a multi-LLM workflow with cost-based routing."

**Do NOT use when** — "explain the architecture patterns for multi-agent systems" — route to orchestrating-ai-agents.

# AI Agents & Automation Workflow Skill v2.0

Build secure, modular, production-ready AI agents and automation workflows across the modern AI/automation ecosystem with MCP Protocol 2025 compliance, Claude Skills integration, and enterprise security patterns.

## What's New in v2.0 (March 2026)

- **MCP November 2025 Spec**: Async operations, OAuth flows, stateless servers, capability declarations
- **Security Hardening**: April 2025 analysis compliance (prompt injection defense, tool sandboxing, consent flows)
- **Framework Updates**: LangGraph 1.0 stable, CrewAI multimodal + agentic RAG, market data
- **Code Execution Patterns**: On-demand tool loading for 100+ tool scenarios
- **Claude Skills Integration**: Description optimization, progressive disclosure, enterprise deployment
- **Interoperability**: Agent2Agent (A2A) protocol, cross-framework communication

## Quick Start Decision Tree

**Choose your approach based on requirements:**

1. **Need direct Claude API integration?** → MCP Server (see `references/mcp-servers.md`)
2. **Need no-code workflow?** → Zapier/Make (see `references/tool-integrations.md`)
3. **Need multi-agent orchestration?** → CrewAI/LangChain (see `references/agent-frameworks.md`)
4. **Need custom LLM routing logic?** → Multi-LLM patterns (see `references/multi-llm-patterns.md`)
5. **Need web automation?** → Playwright + MCP (see `references/tool-integrations.md`)
6. **Need 100+ tools with efficiency?** → Code Execution + MCP (see `references/code-execution-patterns.md`)

## Core Workflow

### Step 1: Requirements Gathering

Ask the user:
- **Trigger**: What initiates the workflow? (API call, webhook, schedule, manual)
- **Data sources**: Which tools provide input? (GitHub, Notion, etc.)
- **LLM tasks**: What requires AI reasoning vs. deterministic logic?
- **Destinations**: Where do results go? (Notion, GitHub, Slack, etc.)
- **Security**: Authentication requirements, secrets management, rate limits, consent flows
- **Scale**: How many tools? (determines if code execution pattern needed)
- **Deployment**: Where will this run? (local, Vercel, Cloudflare Workers, etc.)

### Step 2: Architecture Selection

Use the appropriate pattern:

**Pattern A: MCP Server** (Claude-native tool integration, MCP 2025 spec compliant)
- Use when: Building reusable tools for Claude desktop/web/API
- Features: Async operations, OAuth flows, stateless design
- See: `references/mcp-servers.md`
- Init: `scripts/init_mcp_server.py`

**Pattern B: LangChain Agent** (Python ecosystem, LangGraph 1.0 stable)
- Use when: Need tool calling with memory + Python integrations
- Features: Graph-based workflows, LangSmith observability
- See: `references/agent-frameworks.md` § LangChain
- Init: `scripts/init_langchain_agent.py`

**Pattern C: CrewAI Workflow** (Multi-agent collaboration, multimodal + agentic RAG)
- Use when: Need role-based agents working together
- Features: Independent from LangChain, native vector DB integration
- See: `references/agent-frameworks.md` § CrewAI
- Init: `scripts/init_crewai_workflow.py`

**Pattern D: Multi-LLM Orchestration** (Route tasks to best model)
- Use when: Need cost/speed/capability optimization
- See: `references/multi-llm-patterns.md`

**Pattern E: No-Code Integration** (Zapier/Make)
- Use when: Non-technical stakeholders need to modify
- See: `references/tool-integrations.md` § No-Code Platforms

**Pattern F: Code Execution + MCP** (100+ tools, on-demand loading)
- Use when: Need efficient context management with large tool sets
- Features: Filesystem-based discovery, search_tools pattern
- See: `references/code-execution-patterns.md`

### Step 3: Security Baseline (April 2025 Compliance)

**MANDATORY for all patterns:**
- Input validation (never trust external data, prevent SQL injection)
- Secrets via environment variables (`.env` for local, secrets manager for prod)
- Rate limiting (prevent abuse, per-user and per-endpoint)
- Auth/permissions (explicit scopes, least privilege)
- Error handling (no secret leakage in errors, structured cause→fix→retry)
- **Prompt injection defense**: Treat tool descriptions as untrusted
- **Tool sandboxing**: Implement least-privilege tool access
- **Consent flows**: Explicit user consent before tool invocation

Run: `scripts/validate_workflow.py <path>` to check security baseline

See: `references/security-checklist.md`

### Step 4: Implementation

Build the workflow following the selected pattern. Use templates from `assets/` as starting points:

- `assets/mcp-templates/` - MCP server boilerplates (2025 spec compliant)
- `assets/workflow-templates/` - Zapier/Make workflow JSONs
- `assets/agent-configs/` - LangChain/CrewAI configurations
- `assets/deployment-configs/` - Vercel/Cloudflare deployment configs
- `assets/security-templates/` - Consent flow implementations, input validation
- `assets/code-execution-templates/` - search_tools pattern, on-demand loading

### Step 5: Testing

Test integration points before deployment:
- Use `scripts/test_integration.py` for automated testing
- Verify error handling (simulate API failures)
- Check auth (try with invalid credentials)
- Validate rate limits (burst test)
- Test edge cases (empty responses, malformed data)
- **Security testing**: Prompt injection attempts, unauthorized tool access
- **Performance testing**: Token consumption with large tool sets

### Step 6: Deployment

Deploy according to pattern:
- **MCP**: Install locally or distribute .zip, register with claude.ai
- **LangChain/CrewAI**: Deploy to Cloud Run, Railway, Fly.io
- **Vercel**: Use `vercel deploy` with edge functions
- **Cloudflare Workers**: Use `wrangler publish`
- **Enterprise**: Organization-wide skill deployment (Dec 2025+)

See: `references/deployment.md`

## Progressive Disclosure

Load reference files as needed:

- `references/mcp-servers.md` - MCP server guide (2025 spec with async, OAuth, stateless)
- `references/agent-frameworks.md` - LangChain/CrewAI deep dive (2026 data with LangGraph 1.0, CrewAI multimodal)
- `references/multi-llm-patterns.md` - LLM routing strategies
- `references/tool-integrations.md` - All tool APIs
- `references/security-checklist.md` - Security requirements (April 2025 compliance with prompt injection defense)
- `references/code-execution-patterns.md` - On-demand tool loading for 100+ tool scenarios
- `references/claude-skills-integration.md` - Skills architecture best practices (description optimization, enterprise deployment)
- `references/interoperability.md` - Cross-framework communication (A2A protocol, MCP coordination)
- `references/deployment.md` - Deployment guides (Vercel, Cloudflare, Railway, Docker, enterprise)

## Quality Gates

Before marking any workflow complete, verify:

✅ All inputs validated (type checks, schema validation, SQL injection prevention)  
✅ Secrets in environment variables only (no hardcoded tokens)  
✅ Auth explicitly configured (scopes documented, least privilege)  
✅ Rate limits implemented (per-user, per-endpoint, prevent API abuse)  
✅ Error messages follow cause→fix→retry pattern  
✅ **Security baseline**: Prompt injection defense, tool sandboxing, consent flows  
✅ **MCP 2025 compliance** (if applicable): Async operations, OAuth flows, stateless design  
✅ README includes setup + `.env.example`  
✅ At least 1 happy-path test + 1 edge case test + 1 security test  
✅ Deployment instructions provided

## Version History

**v2.0.0** (March 2026):
- ✅ Optimized description for 90% activation (added "Use when..." triggers with 20+ keywords)
- ✅ Added MCP November 2025 spec features (async, OAuth, stateless, code execution)
- ✅ Integrated April 2025 security analysis findings (prompt injection, tool sandboxing, consent)
- ✅ Updated framework comparison with 2025-2026 data (LangGraph 1.0, CrewAI multimodal/RAG)
- ✅ Added code execution patterns for 100+ tool scenarios
- ✅ Added Claude Skills architecture best practices (progressive disclosure, enterprise deployment)
- ✅ Added interoperability standards (A2A protocol, MCP coordination)

**v1.0.0** (January 2026):
- Initial release with comprehensive automation workflow coverage


## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Passing unsanitized tool output back into the model as instructions** → prompt injection via tool result — treat tool output as data, validate and escape before re-prompting.
- **Placing secrets or OAuth tokens in agent context or traces** → credential leak — inject secrets server-side at call time, never into prompt or state, and redact in observability.
- **Executing tool calls with no sandbox or consent gate on consequential actions** → unbounded blast radius — sandbox tool execution and require HITL approval for irreversible or spendy actions.
- **An agent loop with no turn or cost ceiling** → runaway token spend or an infinite loop — set a hard max-turns and budget guard and circuit-break on repeated failure.
- **Stateful assumptions inside a stateless MCP server** → corrupted multi-client state — hold no per-connection global state, key state by request or session.
- **Shipping with no observability on tool calls and failures** → silent degradation — log every tool call, its latency, and its errors, and wire to instrumenting-agent-telemetry.

