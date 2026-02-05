---
name: provider-integration-templates
description: OpenRouter framework integration templates for Vercel AI SDK, LangChain, and OpenAI SDK. Use when integrating OpenRouter with frameworks, setting up AI providers, building chat applications, implementing streaming responses, or when user mentions Vercel AI SDK, LangChain, OpenAI SDK, framework integration, or provider setup.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Provider Integration Templates

This skill provides complete integration templates, setup scripts, and working examples for integrating OpenRouter with popular AI frameworks: Vercel AI SDK, LangChain, and OpenAI SDK.

## What This Skill Provides

1. **Setup Scripts**: Automated installation and configuration for each framework
2. **Integration Templates**: Drop-in code templates for provider configuration
3. **Working Examples**: Complete implementation examples with best practices
4. **Validation Tools**: Scripts to verify integrations are working correctly

## Supported Frameworks

### Vercel AI SDK (TypeScript)
- Provider configuration with `createOpenAI()`
- API route templates with `streamText()` and `generateText()`
- Chat UI components with `useChat()` hook
- Tool calling with Zod schemas
- Streaming responses

### LangChain (Python & TypeScript)
- ChatOpenAI configuration for OpenRouter
- LCEL chain templates
- Agent templates with tool support
- RAG (Retrieval Augmented Generation) implementations
- Memory and context management

### OpenAI SDK (Python & TypeScript)
- Drop-in replacement configuration
- Chat completions with streaming
- Function calling support
- Embeddings integration

## Available Templates

### Vercel AI SDK Templates
- `templates/vercel-ai-sdk-config.ts` - OpenRouter provider setup
- `templates/vercel-api-route.ts` - API route with streaming
- `templates/vercel-chat-component.tsx` - Chat UI component
- `templates/vercel-tools-config.ts` - Tool calling setup

### LangChain Templates
- `templates/langchain-config.py` - Python ChatOpenAI setup
- `templates/langchain-config.ts` - TypeScript ChatOpenAI setup
- `templates/langchain-chain.py` - LCEL chain template
- `templates/langchain-agent.py` - Agent with tools
- `templates/langchain-rag.py` - RAG implementation

### OpenAI SDK Templates
- `templates/openai-sdk-config.ts` - TypeScript configuration
- `templates/openai-sdk-config.py` - Python configuration
- `templates/openai-streaming.ts` - Streaming example
- `templates/openai-functions.ts` - Function calling

## Setup Scripts

### Installation Scripts
```bash
# Vercel AI SDK setup
bash scripts/setup-vercel-integration.sh

# LangChain setup (Python)
bash scripts/setup-langchain-integration.sh --python

# LangChain setup (TypeScript)
bash scripts/setup-langchain-integration.sh --typescript
```

### Validation Scripts
```bash
# Validate integration is working
bash scripts/validate-integration.sh --framework vercel

# Test streaming functionality
bash scripts/test-streaming.sh --provider openrouter

# Check version compatibility
bash scripts/check-compatibility.sh
```

## How to Use This Skill

### 1. Setup Framework Integration

**Read the setup script** for your target framework:
```
Read: skills/provider-integration-templates/scripts/setup-vercel-integration.sh
```

**Execute the setup script** to install dependencies:
```bash
bash skills/provider-integration-templates/scripts/setup-vercel-integration.sh
```

### 2. Use Integration Templates

**Read the template** you need:
```
Read: skills/provider-integration-templates/templates/vercel-ai-sdk-config.ts
```

**Copy template to project**:
```bash
cp skills/provider-integration-templates/templates/vercel-ai-sdk-config.ts src/lib/ai.ts
```

**Customize with project-specific values**:
- Replace `YOUR_OPENROUTER_API_KEY` with actual key or env var
- Update model selection
- Configure streaming options

### 3. Review Working Examples

**Read complete examples**:
```
Read: skills/provider-integration-templates/examples/vercel-streaming-example.md
```

Examples show:
- Complete file structure
- Environment variable setup
- API route implementation
- Frontend component integration
- Error handling patterns

### 4. Validate Integration

**Run validation script**:
```bash
bash skills/provider-integration-templates/scripts/validate-integration.sh --framework vercel
```

**Test streaming**:
```bash
bash scripts/test-streaming.sh --provider openrouter --model anthropic/claude-4.5-sonnet
```

## Integration Patterns

### Pattern 1: Vercel AI SDK Chat Application

1. Read Vercel AI SDK config template
2. Copy to `src/lib/ai.ts`
3. Read API route template
4. Copy to `app/api/chat/route.ts`
5. Read chat component template
6. Copy to `components/chat.tsx`
7. Run validation script

### Pattern 2: LangChain LCEL Chain

1. Read LangChain config template (Python or TS)
2. Copy to `src/config/langchain.py`
3. Read LCEL chain template
4. Copy to `src/chains/chat_chain.py`
5. Customize prompts and models
6. Test with validation script

### Pattern 3: OpenAI SDK Drop-in Replacement

1. Read OpenAI SDK config template
2. Replace base URL with OpenRouter endpoint
3. Add `HTTP-Referer` and `X-Title` headers
4. Update API key to use OpenRouter key
5. Test existing OpenAI code (should work unchanged)

## Environment Variables

All templates use these standard environment variables:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=anthropic/claude-4.5-sonnet
OPENROUTER_SITE_URL=https://yourapp.com  # Optional: for rankings
OPENROUTER_SITE_NAME=YourApp  # Optional: for rankings
```

## Model Selection

Templates use configurable model selection. Common models:

- `anthropic/claude-4.5-sonnet` - Best reasoning, long context
- `anthropic/claude-4.5-sonnet` - Most capable, highest cost
- `meta-llama/llama-3.1-70b-instruct` - Fast, cost-effective
- `openai/gpt-4-turbo` - Strong general purpose
- `google/gemini-pro-1.5` - Long context, multimodal

Update model selection in templates based on use case.

## Best Practices

1. **Use Environment Variables**: Never hardcode API keys
2. **Enable Streaming**: Better UX for chat applications
3. **Add Error Handling**: Handle rate limits and API errors
4. **Set HTTP Headers**: Include site URL and name for rankings
5. **Test Before Deployment**: Use validation scripts
6. **Monitor Usage**: Track costs with OpenRouter dashboard

## Troubleshooting

**Issue**: API key not working
- Check key format: `sk-or-v1-...`
- Verify key in OpenRouter dashboard
- Check environment variable is loaded

**Issue**: Streaming not working
- Ensure `stream: true` in request
- Check framework version compatibility
- Verify response handler supports streaming

**Issue**: Model not found
- Check model ID format: `provider/model-name`
- Verify model is available on OpenRouter
- Check for typos in model name

## Progressive Disclosure

For detailed implementation guides, load these files as needed:

- `examples/vercel-streaming-example.md` - Complete Vercel AI SDK setup
- `examples/langchain-rag-example.md` - RAG implementation guide
- `examples/openai-sdk-example.md` - OpenAI SDK migration guide

---

**Template Version**: 1.0.0
**Framework Support**: Vercel AI SDK 4.x, LangChain 0.3.x, OpenAI SDK 1.x
**Last Updated**: 2025-10-31
