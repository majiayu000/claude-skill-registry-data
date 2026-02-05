---
name: Delegating to CDN Agent
description: Recognize Fastly CDN queries and delegate to specialized sub-agent to avoid context pollution
keywords: fastly, cdn, cache, vcl, backends, purge, origin, varnish, delegate, agent
when_to_use: When user mentions "fastly", "cdn", "cache purge", "vcl", "backends", or asks about CDN services. ALWAYS delegate to sub-agent.
version: 1.0.0
---

# Delegating to CDN Agent

## Core Principle

**Never handle Fastly CDN operations directly.** Always delegate to a specialized sub-agent to keep your context clean and costs low.

## Recognition Patterns

Delegate when user says:
- "query fastly for..."
- "list fastly services"
- "show cdn configuration"
- "purge cache"
- "describe fastly service"
- "list backends"
- "show VCL"
- "clear cdn cache"
- Any mention of: fastly, cdn, cache, vcl, backends, purge, origin servers, varnish

## ExampleJobInc-Specific Triggers

Also delegate when user mentions these ExampleJobInc domains:
- "pi.examplejobinc-cdn.com"
- "images.examplejobinc.com"
- "hls.examplejobinc.com"
- "assets.examplejobinc.com"
- "embed.examplejobinc.com"
- "crushinator" (image processing backend)

## How to Delegate

Use the Task tool with a specialized prompt:

```
Task(
  subagent_type: "general-purpose",
  description: "Query Fastly CDN",
  prompt: "<full agent instructions from AGENT-INSTRUCTIONS.md>"
)
```

## Agent Prompt Template

When delegating, include:
1. The complete agent instructions (see AGENT-INSTRUCTIONS.md)
2. The user's specific request
3. Clear output format requirements

**Example:**

```
You are a Fastly CDN specialist. Your job is to query Fastly using shell wrappers and return clean results.

<AGENT INSTRUCTIONS HERE>

USER REQUEST: List all Fastly services

Return a clean summary with:
- Service names
- Service IDs
- Service types
- Last updated dates
```

## After Agent Returns

1. **Present results cleanly** to user
2. **Offer follow-up** if relevant (e.g., "Would you like to see backends for pi.examplejobinc-cdn.com?")
3. **Don't expose mechanics** (API calls, tokens, CLI commands) to user

## Benefits

- ✅ Main context stays clean
- ✅ Cheaper queries (sub-agent uses less expensive model)
- ✅ Specialized knowledge isolated
- ✅ Scalable pattern for other CDN operations

## Example Flow

```
User: "list fastly services"

Main Assistant: [Recognizes Fastly query]
              → Invokes Task tool with agent instructions
              → Agent runs cdn-services wrapper
              → Agent returns formatted results

Main Assistant: "Found 8 Fastly services:

                1. pi.examplejobinc-cdn.com - Image processing CDN
                2. images.examplejobinc.com - Static images
                3. hls.examplejobinc.com - Video streaming
                ...

                Would you like details on any of these?"
```

## Common Query Types

**Service Management:**
- "list fastly services"
- "describe pi.examplejobinc-cdn.com service"
- "show cdn configuration"

**Backend Investigation:**
- "list backends for pi.examplejobinc-cdn.com"
- "show origin servers"
- "describe crushinator backend"

**VCL Configuration:**
- "list VCL configurations"
- "show VCL content for version 42"
- "view custom VCL"

**Cache Management:**
- "purge all cache for pi.examplejobinc-cdn.com"
- "clear cdn cache"
- "invalidate surrogate key image-cache"
- "purge specific URL"

## Red Flags

**DON'T:**
- ❌ Try to run fastly-* scripts yourself
- ❌ Attempt Fastly API calls directly
- ❌ Load detailed Fastly CLI knowledge
- ❌ Handle authentication directly
- ❌ Parse complex CDN configurations

**DO:**
- ✅ Immediately delegate on Fastly keywords
- ✅ Trust the sub-agent's results
- ✅ Present clean summaries to user
- ✅ Suggest relevant follow-up queries
- ✅ Warn about cache purge impact

## Cache Purge Safety

When user requests cache purging:
1. **Always delegate** to sub-agent (never do yourself)
2. **Confirm service** before agent purges
3. **Warn about impact** of full cache purges
4. **Prefer specific purges** (URL/key) over --all

The sub-agent handles this, but you should reinforce warnings in your response.

## ExampleJobInc Infrastructure Context

ExampleJobInc uses Fastly for:
- **Image CDN** (pi.examplejobinc-cdn.com) - Crushinator-powered image processing
- **Video CDN** (hls.examplejobinc.com) - HLS streaming
- **Static assets** (images.examplejobinc.com, assets.examplejobinc.com)
- **Website CDN** (www.examplejobinc.com)

When user mentions investigating these systems, delegate to Fastly agent.

## Version History

- 1.0.0 (2025-10-15): Initial delegation skill created to reduce context pollution
