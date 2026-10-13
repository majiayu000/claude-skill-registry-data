---
name: orchestrating-ai-agents
metadata:
  version: "2.0.0"
description: >
  Architecture and design guidance for AI agents, automation workflows, and tool
  orchestrations — topology selection, trust and permission boundaries, failure-mode and
  rollback design across the AI/automation ecosystem. Activates on agent architecture, how
  should I structure this agent system, multi-agent design, tool access design, agent security
  architecture, design an automation. Not for hands-on implementation or writing the code (use
  ai-agents-workflow) and not for no-code platform wiring (use workflow-automation).
---

## When to Use / When NOT

**Use when** — "what is the right architecture for a multi-agent research system." "how should I structure tool access and security for an agent platform."

**Do NOT use when** — "write the actual MCP server code for this" — route to ai-agents-workflow.

# AI Agents & Automation Workflow Skill

Build secure, modular, production-ready AI agents and automation workflows across the modern AI/automation ecosystem.

## Quick Start Decision Tree

**Choose your approach based on requirements:**

1. **Need direct Claude API integration?** → MCP Server (see [references/mcp-servers.md](references/mcp-servers.md))
2. **Need no-code workflow?** → Zapier/Make (see [references/tool-integrations.md](references/tool-integrations.md))
3. **Need multi-agent orchestration?** → CrewAI/LangChain (see [references/agent-frameworks.md](references/agent-frameworks.md))
4. **Need custom LLM routing logic?** → Multi-LLM patterns (see [references/multi-llm-patterns.md](references/multi-llm-patterns.md))
5. **Need web automation?** → Playwright + MCP (see [references/tool-integrations.md](references/tool-integrations.md))

## Core Workflow

### Step 1: Requirements Gathering

Ask the user:
- **Trigger**: What initiates the workflow? (API call, webhook, schedule, manual)
- **Data sources**: Which tools provide input? (GitHub, Notion, etc.)
- **LLM tasks**: What requires AI reasoning vs. deterministic logic?
- **Destinations**: Where do results go? (Notion, GitHub, Slack, etc.)
- **Security**: Authentication requirements, secrets management, rate limits
- **Deployment**: Where will this run? (local, Vercel, Cloudflare Workers, etc.)

### Step 2: Architecture Selection

Use the appropriate pattern:

**Pattern A: MCP Server** (Claude-native tool integration)
- Use when: Building reusable tools for Claude desktop/web
- See: [references/mcp-servers.md](references/mcp-servers.md)
- Init: `scripts/init_mcp_server.py`

**Pattern B: LangChain Agent** (Python ecosystem, single agent)
- Use when: Need tool calling with memory + Python integrations
- See: [references/agent-frameworks.md](references/agent-frameworks.md) § LangChain
- Init: `scripts/init_langchain_agent.py`

**Pattern C: CrewAI Workflow** (Multi-agent collaboration)
- Use when: Need role-based agents working together
- See: [references/agent-frameworks.md](references/agent-frameworks.md) § CrewAI
- Init: `scripts/init_crewai_workflow.py`

**Pattern D: Multi-LLM Orchestration** (Route tasks to best model)
- Use when: Need cost/speed/capability optimization
- See: [references/multi-llm-patterns.md](references/multi-llm-patterns.md)

**Pattern E: No-Code Integration** (Zapier/Make)
- Use when: Non-technical stakeholders need to modify
- See: [references/tool-integrations.md](references/tool-integrations.md) § No-Code Platforms

### Step 3: Security Baseline

**MANDATORY for all patterns:**
- Input validation (never trust external data)
- Secrets via environment variables (`.env` for local, secrets manager for prod)
- Rate limiting (prevent abuse)
- Auth/permissions (explicit scopes, least privilege)
- Error handling (no secret leakage in errors)

Run: `scripts/validate_workflow.py <path>` to check security baseline

See: [references/security-checklist.md](references/security-checklist.md)

### Step 4: Implementation

Build the workflow following the selected pattern. Use templates from `assets/` as starting points:

- `assets/mcp-templates/` - MCP server boilerplates
- `assets/workflow-templates/` - Zapier/Make workflow JSONs
- `assets/agent-configs/` - LangChain/CrewAI configurations
- `assets/deployment-configs/` - Vercel/Cloudflare deployment configs

### Step 5: Testing

Test integration points before deployment:
- Use `scripts/test_integration.py` for automated testing
- Verify error handling (simulate API failures)
- Check auth (try with invalid credentials)
- Validate rate limits (burst test)
- Test edge cases (empty responses, malformed data)

### Step 6: Deployment

Deploy according to pattern:
- **MCP**: Install locally or distribute .zip
- **LangChain/CrewAI**: Deploy to Cloud Run, Railway, Fly.io
- **Vercel**: Use `vercel deploy` with edge functions
- **Cloudflare Workers**: Use `wrangler publish`

See: [references/deployment.md](references/deployment.md)

## Integration Recipes

Common workflow patterns with implementation guides:

### Recipe 1: GitHub PR Review Agent
**Trigger**: GitHub webhook (PR opened)  
**Flow**: Fetch PR → Claude review → Post comments  
**Pattern**: MCP Server + GitHub API  
**See**: [references/tool-integrations.md](references/tool-integrations.md) § GitHub Integration

### Recipe 2: Notion Knowledge Base Query
**Trigger**: Slack message  
**Flow**: Query Notion DB → Vector search → LLM synthesis → Reply  
**Pattern**: LangChain + Notion API + Pinecone  
**See**: [references/agent-frameworks.md](references/agent-frameworks.md) § RAG Patterns

### Recipe 3: Multi-Agent Content Pipeline
**Trigger**: Schedule (daily)  
**Flow**: Research agent → Writer agent → Editor agent → Publisher  
**Pattern**: CrewAI workflow  
**See**: [references/agent-frameworks.md](references/agent-frameworks.md) § CrewAI

### Recipe 4: Smart LLM Router
**Trigger**: API request  
**Flow**: Classify task → Route to Claude/GPT/Gemini → Stream response  
**Pattern**: Multi-LLM orchestration  
**See**: [references/multi-llm-patterns.md](references/multi-llm-patterns.md)

## Tool Ecosystem Coverage

This skill provides integration guidance for:

**LLM Providers**: Claude (Anthropic), GPT (OpenAI), Gemini (Google)  
**Orchestration**: LangChain, LangGraph, CrewAI, AutoGen  
**No-Code**: Zapier, Make (Integromat)  
**Development**: Vercel, Cloudflare Workers, GitHub Actions  
**Data Sources**: Notion, GitHub, HubSpot, Airtable  
**Observability**: Sentry, LangSmith, Helicone  
**Browser Automation**: Playwright  
**Assets**: Cloudinary, Canva  
**Vector DBs**: Pinecone, Weaviate, Chroma  
**MCP Ecosystem**: All available MCP servers

## Error Handling Pattern

All implementations must follow this error structure:

```
❌ Error: <WHAT_FAILED>
📋 Cause: <WHY_IT_FAILED>
🔧 Fix: <HOW_TO_RESOLVE>
🔄 Retry: <SUGGESTED_ACTION>
```

Example:
```
❌ Error: GitHub API authentication failed
📋 Cause: Invalid or expired GITHUB_TOKEN
🔧 Fix: Generate new token at github.com/settings/tokens with 'repo' scope
🔄 Retry: Set GITHUB_TOKEN env var and restart
```

## Progressive Disclosure

- **Core patterns**: Read this SKILL.md first
- **Deep dives**: Load reference files as needed:
  - [references/mcp-servers.md](references/mcp-servers.md) - Full MCP server guide
  - [references/multi-llm-patterns.md](references/multi-llm-patterns.md) - LLM routing strategies
  - [references/tool-integrations.md](references/tool-integrations.md) - All tool APIs
  - [references/agent-frameworks.md](references/agent-frameworks.md) - LangChain/CrewAI deep dive
  - [references/deployment.md](references/deployment.md) - Deployment guides
  - [references/security-checklist.md](references/security-checklist.md) - Security requirements
- **Scripts**: Execute deterministically without loading into context
- **Assets**: Copy/modify templates for rapid development

## Quality Gates

Before marking any workflow complete, verify:

✅ All inputs validated (type checks, schema validation)  
✅ Secrets in environment variables only (no hardcoded tokens)  
✅ Auth explicitly configured (scopes documented)  
✅ Rate limits implemented (prevent API abuse)  
✅ Error messages follow cause→fix→retry pattern  
✅ README includes setup + `.env.example`  
✅ At least 1 happy-path test + 1 edge case test  
✅ Deployment instructions provided


## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Recommending an architecture before modeling auth, data flow, and failure modes** → an insecure, brittle design — model boundaries, trust, and failure modes before proposing components.
- **Reaching for multi-agent complexity where one tool-using agent suffices** → needless cost and failure surface — justify each agent and default to the simplest topology that meets the requirement.
- **Designing tool access without least-privilege boundaries** → over-permissioned agents by construction — scope each tool and credential to the narrowest role at design time.
- **Ignoring prompt-injection and tool-output trust in the design** → the implementation inherits the hole — treat external inputs as adversarial in the architecture, not as an afterthought.
- **No observability or HITL checkpoints designed in for consequential actions** → an unobservable, ungoverned runtime — bake telemetry and approval gates into the architecture.
- **An architecture with no rollback or failure path per stage** → no recovery when a step fails — define retry, dead-letter, and rollback for each stage.

## Evals

- ✅ **SHOULD TRIGGER** — "what is the right architecture for a multi-agent research system."
- ✅ **SHOULD TRIGGER** — "how should I structure tool access and security for an agent platform."
- ❌ **SHOULD NOT TRIGGER** — "write the actual MCP server code for this" — route to ai-agents-workflow.
