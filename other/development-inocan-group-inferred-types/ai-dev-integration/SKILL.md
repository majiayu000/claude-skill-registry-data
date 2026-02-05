---
name: ai-dev-integration
description: Expert guidance for developing and integrating AI systems using LLM APIs, SDKs, and Model Context Protocol (MCP). Covers API selection, SDK patterns, MCP development, production patterns, security, cost optimization, and architecture decisions for building production-ready AI integrations.
---

# AI Development & Integration

## Purpose

Guide developers in building production-ready AI integrations with comprehensive coverage of LLM APIs, SDKs, and the Model Context Protocol (MCP). Provide decision frameworks for choosing the right integration approach, implementing secure and cost-effective solutions, and avoiding common pitfalls.

## When to Use This Skill

Invoke this skill when addressing:

- **API selection decisions**: Choosing between OpenAI, Anthropic Claude, Google Gemini, Ollama, or other providers
- **Integration architecture**: Designing systems that use LLMs for chat, document processing, analysis, or other tasks
- **MCP vs direct API**: Deciding whether to build an MCP server or use direct API calls
- **MCP development**: Creating MCP servers with FastMCP (Python) or TypeScript SDK
- **Production readiness**: Implementing error handling, rate limiting, caching, monitoring, or security measures
- **Multi-provider strategies**: Building systems with fallback logic or provider switching
- **Cost optimization**: Reducing token usage, implementing caching, or tracking expenses
- **Security concerns**: Preventing prompt injection, handling PII, or implementing auth
- **Streaming implementations**: Building real-time chat or processing systems
- **Agent frameworks**: Deciding if CrewAI, LangChain, AutoGen, or similar tools are needed

## Core Decision Frameworks

### API Selection Decision Tree

**When to use OpenAI:**
- Need GPT-4 Turbo or GPT-4o specific capabilities
- Require DALL-E image generation or Whisper transcription
- Building on existing OpenAI integrations
- Cost-sensitive applications with GPT-3.5-turbo
- Need function calling with streaming

**When to use Anthropic Claude:**
- Require 200K+ token context windows (Claude 3.5 Sonnet/Opus)
- Need strong reasoning and analysis capabilities
- Building tool-heavy integrations (MCP compatible)
- Prefer thoughtful, nuanced responses
- Require strong security and reduced hallucinations

**When to use Google Gemini:**
- Need multimodal inputs (images, video, audio in same context)
- Require 2M+ token context window (Gemini 1.5 Pro)
- Building Google Cloud integrations
- Need competitive pricing on long-context tasks

**When to use Ollama (local):**
- Privacy requirements prevent cloud API usage
- Need offline operation or airgapped environments
- Want to avoid per-token costs
- Acceptable with lower quality for simpler tasks
- Have GPU resources for inference

**Multi-provider strategy**: Implement when requiring high availability, cost optimization through provider switching, or different models for different task types.

### MCP vs Direct API Integration

**Use MCP when:**
- Building tool-heavy integrations requiring multiple capabilities (database access, file operations, API calls)
- Creating reusable tool packages for multiple projects
- Giving Claude extended capabilities beyond simple completions
- Need standardized tool discovery and lifecycle management
- Building integrations specifically for Claude (MCP is Anthropic-specific)
- Want to separate tool implementation from application logic

**Use direct API when:**
- Need simple completions without extensive tooling
- Building one-off integrations for specific tasks
- Using language models other than Claude (MCP is Claude-specific)
- Require maximum control over request/response handling
- Need custom streaming or token-level processing
- Integration complexity doesn't justify MCP overhead

**Architecture pattern comparison:**

```
MCP Architecture:
Application → MCP Client → MCP Server → Tools/Resources
Benefits: Standardized, reusable, discoverable tools
Complexity: Higher initial setup, server lifecycle management

Direct API Architecture:
Application → SDK/HTTP Client → LLM API → Response
Benefits: Simple, direct control, any LLM provider
Complexity: Lower initial setup, manual function calling
```

For detailed MCP development guidance, consult `references/mcp-development.md`.

### SDK Integration Best Practices

**Error handling pattern (all SDKs):**
1. Implement exponential backoff for rate limits
2. Catch provider-specific exceptions
3. Log errors with request IDs for debugging
4. Implement circuit breakers for repeated failures
5. Provide user-friendly error messages

**Streaming vs batch processing:**
- **Use streaming**: Chat applications, real-time UIs, long-running generations where partial results are valuable
- **Use batch**: Background processing, bulk operations, when final result is needed before showing anything

**Rate limiting strategies:**
1. Token bucket algorithm for smooth request distribution
2. Provider-specific limits (consult `references/api-comparison.md`)
3. Implement queuing for burst handling
4. Track usage per user/tenant for fair distribution

**Context window management:**
1. Track token counts before sending (use tiktoken for OpenAI, Anthropic tokenizer for Claude)
2. Implement sliding window for conversations
3. Summarize old messages to preserve context
4. Chunk large documents with overlap
5. Use references/pointers instead of full content when possible

For detailed SDK patterns and code examples, consult `references/sdk-patterns.md`.

## MCP Development Essentials

### FastMCP vs TypeScript SDK Selection

**Choose FastMCP (Python) when:**
- Primary codebase is Python
- Integrating with data science/ML tooling (pandas, numpy, scikit-learn)
- Need rapid prototyping with minimal boilerplate
- Team expertise is Python-focused
- Integrating with FastAPI, Django, or Flask backends

**Choose TypeScript SDK when:**
- Primary codebase is Node.js/TypeScript
- Need tight integration with JavaScript ecosystem
- Building full-stack applications with shared types
- Team expertise is TypeScript-focused
- Require advanced type safety and IDE support

### Tool Design Patterns

**Effective tool design:**
1. **Single responsibility**: Each tool does one thing well
2. **Clear parameters**: Use Pydantic/Zod schemas for validation
3. **Descriptive names**: Tool name clearly indicates purpose
4. **Helpful descriptions**: Explain when and why to use the tool
5. **Error context**: Return actionable error messages

**Anti-patterns to avoid:**
1. **God tools**: Tools that do too many things (split them up)
2. **Vague parameters**: Unclear what values are valid or expected
3. **Silent failures**: Tools that fail without informative errors
4. **State dependencies**: Tools that require specific call order (make them independent)
5. **Inconsistent interfaces**: Similar tools with different parameter patterns

### Security Considerations for MCP Servers

**Authentication and authorization:**
1. Implement authentication for sensitive tools
2. Use environment variables for credentials, never hardcode
3. Apply principle of least privilege to database/API access
4. Validate all user inputs rigorously
5. Audit tool access and usage

**Data access controls:**
1. Scope database queries to authorized data only
2. Implement row-level security where applicable
3. Sanitize outputs to prevent leaking PII
4. Use read-only connections when write access isn't needed
5. Rate limit expensive operations

For comprehensive MCP security guidance, consult `references/mcp-development.md`.

## Production Patterns

### Caching Strategies

**LLM response caching:**
1. Cache identical prompts with same parameters
2. Use semantic similarity for near-duplicate queries
3. Implement TTL based on data freshness requirements
4. Cache embeddings for reuse across requests
5. Provider-specific caching (Anthropic prompt caching, OpenAI response caching)

**Cost-effective caching:**
- Cache expensive operations (embeddings, long completions)
- Invalidate caches when underlying data changes
- Use Redis/Memcached for distributed caching
- Monitor cache hit rates for optimization

### Monitoring and Observability

**Key metrics to track:**
1. Request latency (p50, p95, p99)
2. Token usage per request and total
3. Error rates by type and provider
4. Cost per request and daily/monthly totals
5. Cache hit rates

**Implement:**
1. Structured logging with request IDs
2. Distributed tracing for multi-service flows
3. Alerting on error rate spikes or cost anomalies
4. Dashboard for real-time monitoring

### Cost Optimization Techniques

**Token reduction strategies:**
1. Remove unnecessary whitespace and formatting
2. Use shorter system prompts when possible
3. Implement prompt compression techniques
4. Cache common responses
5. Use cheaper models for simpler tasks

**Intelligent routing:**
1. Route simple queries to GPT-3.5-turbo or Claude Haiku
2. Use expensive models (GPT-4, Claude Opus) only when needed
3. Implement confidence scoring to determine model selection
4. A/B test model performance vs cost tradeoffs

For cost tracking tools, use `scripts/cost-calculator.py`.

### Prompt Injection Prevention

**Input validation:**
1. Sanitize user inputs before inclusion in prompts
2. Use structured inputs (JSON) instead of free text when possible
3. Implement content filtering for malicious patterns
4. Separate user content from instructions clearly
5. Use XML tags or delimiters to demarcate user content

**System prompt hardening:**
1. Be explicit about ignoring instructions in user content
2. Use Anthropic's Constitutional AI principles for Claude
3. Implement output validation to detect leaked instructions
4. Test with adversarial prompts regularly

### PII and Sensitive Data Handling

**Data minimization:**
1. Avoid sending PII to LLM APIs when possible
2. Anonymize or pseudonymize data before processing
3. Use on-premise models (Ollama) for highly sensitive data
4. Implement data retention policies

**Compliance considerations:**
1. Review provider data processing agreements (DPAs)
2. Understand data residency requirements
3. Implement audit logging for compliance
4. Consider zero data retention options (where available)

For comprehensive production checklist, consult `references/production-checklist.md`.

## Integration Architectures

### Synchronous vs Asynchronous Patterns

**Synchronous (request-response):**
- **Use for**: Chat interfaces, real-time interactions, simple queries
- **Pattern**: User waits for completion, streaming for UX
- **Implementation**: Direct API calls, WebSocket for streaming
- **Pros**: Simple, immediate feedback
- **Cons**: User blocked during processing, scaling challenges

**Asynchronous (queue-based):**
- **Use for**: Batch processing, long-running tasks, high volume
- **Pattern**: Queue request, process in background, notify on completion
- **Implementation**: Celery, RQ, AWS SQS, Google Cloud Tasks
- **Pros**: Scalable, resilient, non-blocking
- **Cons**: Added complexity, eventual consistency

**Hybrid approach:**
1. Streaming response for initial results (synchronous UX)
2. Queue follow-up processing (asynchronous backend)
3. WebSocket/SSE for progress updates
4. Best of both worlds for complex workflows

### Webhook Handling

**Best practices:**
1. Validate webhook signatures for security
2. Respond quickly (< 3s), queue actual processing
3. Implement idempotency to handle duplicates
4. Retry failed webhooks with exponential backoff
5. Monitor webhook delivery success rates

### State Management Across Conversations

**Conversation state strategies:**
1. **Stateless**: Include full history in each request (simple, scales horizontally)
2. **Session storage**: Store conversation in Redis/database (better for long conversations)
3. **Hybrid**: Recent messages in request, older messages summarized/retrieved as needed

**State storage considerations:**
1. Choose storage based on conversation length expectations
2. Implement conversation expiration for cleanup
3. Consider multi-tenant isolation requirements
4. Use conversation IDs for tracking and debugging

## When to Consider Agent Frameworks

### Decision Criteria

**Use simple API calls when:**
- Single-task workflows (chat, completion, classification)
- No need for multi-step reasoning or tool orchestration
- Direct control over prompts and responses is required
- Minimal dependencies are preferred

**Consider agent frameworks when:**
- Multi-agent collaboration is needed (CrewAI)
- Complex tool orchestration across multiple steps (LangChain)
- Need for autonomous task breakdown and execution (AutoGen)
- Building agent-to-agent communication patterns
- Require pre-built integrations and abstractions

**Framework selection guidance:**
- **CrewAI**: Multi-agent workflows with role-based collaboration
- **LangChain**: Tool chaining, retrieval-augmented generation (RAG)
- **AutoGen**: Autonomous agents with code execution
- **Haystack**: NLP pipelines and document processing

**Note**: For detailed agent framework guidance, consult the `ai-agent-frameworks` skill (if available).

**Signs you need orchestration:**
1. Tasks require multiple sequential LLM calls with dependencies
2. Need to coordinate between different tools and APIs
3. Workflows vary based on intermediate results
4. Building complex autonomous behaviors

**Signs simple API calls suffice:**
1. Single prompt → single response pattern
2. Predictable, linear workflows
3. Minimal tool usage or simple function calling
4. Performance and control are critical

## Template Resources

### MCP Server Templates

**Python template**: `scripts/mcp-template-python/`
- FastMCP-based server structure
- Example tool implementations
- Environment configuration
- Testing setup with pytest

**TypeScript template**: `scripts/mcp-template-typescript/`
- MCP SDK server structure
- Example tool implementations
- Build configuration with tsup
- Testing setup with vitest

### Cost Estimation Tool

**Usage**: `python scripts/cost-calculator.py`

Calculate estimated costs for different providers based on:
- Input/output token counts
- Model selection
- Request volume
- Compare costs across providers

Helps make informed decisions about provider selection and budget planning.

## Additional Resources

- `references/api-comparison.md`: Detailed provider comparison matrix (features, pricing, rate limits, capabilities)
- `references/mcp-development.md`: Comprehensive MCP development guide (FastMCP/TypeScript SDK, tool patterns, security, debugging)
- `references/sdk-patterns.md`: Code examples for error handling, streaming, rate limiting, context management
- `references/production-checklist.md`: Pre-deployment validation, monitoring setup, security audit, performance optimization

## Workflow Recommendations

**For new integrations:**
1. Start with decision frameworks above to select provider and architecture
2. Review `references/api-comparison.md` for detailed provider evaluation
3. Implement basic integration using patterns from `references/sdk-patterns.md`
4. Add production hardening using `references/production-checklist.md`
5. Use `scripts/cost-calculator.py` to validate cost assumptions

**For MCP development:**
1. Decide if MCP is appropriate using decision framework above
2. Choose FastMCP or TypeScript SDK based on team expertise
3. Start from template in `scripts/mcp-template-python/` or `scripts/mcp-template-typescript/`
4. Review `references/mcp-development.md` for tool design patterns and security
5. Test thoroughly before deployment

**For production deployments:**
1. Complete all items in `references/production-checklist.md`
2. Implement monitoring and cost tracking
3. Set up alerting for errors and cost anomalies
4. Document operational runbooks
5. Plan for scaling and disaster recovery
