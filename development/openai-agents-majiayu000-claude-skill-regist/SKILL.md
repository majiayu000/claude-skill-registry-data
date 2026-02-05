---
name: openai-agents
description: Use when integrating OpenAI GPT models for conversational AI. Covers chat completions, streaming responses, function calling, system prompts, token management, cost optimization, error handling, and building specialized agent personas for Physical AI tutoring.
---

# OpenAI Agents Skill

## Quick Start Workflow

When working with OpenAI APIs:

1. **Choose the right model**
   - GPT-4: Complex reasoning, code generation, long context
   - GPT-3.5-turbo: Fast, cost-effective, simple queries
   - Check token limits (GPT-4: 8K/32K, GPT-3.5: 16K)

2. **Design system prompts**
   - Define agent personality and role
   - Provide context about Physical AI domain
   - Set output format expectations
   - Include safety guardrails

3. **Implement streaming** for better UX
   - Stream responses token-by-token
   - Show "thinking..." indicator
   - Handle partial responses

4. **Add function calling** for tools
   - Define functions (search, calculator, etc.)
   - Parse function call requests
   - Execute and return results

### Agent Personas

#### Physical AI Tutor
```typescript
const TUTOR_PROMPT = `You are an expert tutor in Physical AI and Humanoid Robotics. 
- Explain concepts clearly with examples
- Reference specific textbook sections
- Encourage hands-on learning
- Use analogies for difficult topics
Always cite sources from the textbook context provided.`;
```

#### Code Reviewer
```typescript
const REVIEWER_PROMPT = `You are a ROS 2 code reviewer.
- Review Python/C++ robotics code
- Check for anti-patterns
- Suggest optimizations
- Verify thread safety
Provide specific, actionable feedback.`;
```

#### Quick Helper
```typescript
const HELPER_PROMPT = `You provide quick, concise answers about robotics.
- 2-3 sentence responses
- Focus on key points
- No code unless asked`;
```

### Standard Patterns

#### Basic Chat
```typescript
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'system', content: TUTOR_PROMPT },
    { role: 'user', content: userQuestion },
  ],
  temperature: 0.7,
  max_tokens: 1000,
});
```

#### With RAG Context
```typescript
const context = relevantChunks.map(c => c.text).join('\n\n');

const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    {
      role: 'system',
      content: `${TUTOR_PROMPT}\n\nContext:\n${context}`,
    },
    { role: 'user', content: userQuestion },
  ],
});
```

### Best Practices

For Physical AI chatbot:
- **Always include context** from RAG retrieval
- **Set temperature 0.7** for balanced creativity
- **Limit max_tokens** to control costs
- **Implement retry logic** for rate limits
- **Log all completions** for debugging
- **Stream responses** for better UX

## Knowledge Base

Comprehensive guides:
- **Streaming Setup** → `references/streaming.md`
- **Function Calling** → `references/function-calling.md`
- **Token Management** → `references/tokens.md`
- **Cost Optimization** → `references/cost-optimization.md`
- **Error Handling** → `references/error-handling.md`
