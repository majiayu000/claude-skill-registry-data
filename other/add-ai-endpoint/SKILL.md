---
name: add-ai-endpoint
description: Scaffold a Claude API powered endpoint with system prompt, structured output, token tracking, and rate limiting. Use when adding AI features like chatbot, matching, or text generation.
---

# add-ai-endpoint

Scaffolds a new AI-powered API endpoint backed by the Anthropic Claude API. Handles system prompt design, structured output parsing, token usage tracking, and per-user rate limiting.

## Inputs to gather

- **Feature name** — e.g., "property-description-generator", "lead-scorer", "followup-writer"
- **Input shape** — what the endpoint receives (e.g., leadId, propertyId, free text)
- **Output shape** — what it returns (e.g., generated text, score object, match list)
- **System prompt context** — domain knowledge the AI needs (Saudi real estate, Arabic language, REGA rules)
- **Model** — claude-sonnet-4-6 (fast/cheap) or claude-opus-4-6 (best quality)

## Steps

1. **Check AI service layer exists.** Read `apps/api/libs/ai-service.ts`. If it doesn't exist, create it:
   ```typescript
   // Anthropic client singleton, retry logic, token tracker
   import Anthropic from "@anthropic-ai/sdk";
   const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
   ```

2. **Create the route file** at `apps/api/routes/ai-{feature}.ts`:
   - Import `authenticateToken` middleware
   - Validate input with zod
   - Build messages array with system prompt + user content
   - Call `client.messages.create()` with structured output
   - Parse response, return JSON
   - Track token usage: `prompt_tokens`, `completion_tokens` in `ai_usage` table

3. **Design the system prompt.** Must include:
   - Role: "You are a Saudi real estate expert assistant for عقاركم platform"
   - Language: "Always respond in Saudi Arabic (العربية السعودية)"
   - Domain constraints: REGA compliance, FAL license awareness, SAR currency
   - Output format: specify JSON schema if structured output needed

4. **Add rate limiting.** In the route:
   - Check `ai_usage` table: user's token count today
   - If > daily limit (default 50K tokens), return 429
   - Track usage after successful call

5. **Register the route** in `apps/api/index.ts`:
   ```typescript
   import aiFeatureRoutes from "./routes/ai-{feature}";
   app.use("/api/ai", aiFeatureRoutes);
   ```

6. **Create react-query hook** using `/add-react-query` for the frontend.

7. **Add API key to `.env`:**
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

## Verification checklist

- [ ] Endpoint returns correct structured output
- [ ] System prompt produces Arabic responses
- [ ] Token usage is tracked per request
- [ ] Rate limiting rejects over-limit requests with 429
- [ ] Error handling: API timeout, invalid response, rate limit
- [ ] `/typecheck` passes

## Anti-patterns

- Don't hardcode API keys — always use environment variables
- Don't stream responses for simple endpoints — use non-streaming for structured output
- Don't skip token tracking — you'll have no cost visibility
- Don't use opus for high-volume endpoints — use sonnet for speed/cost
- Don't let unauthenticated users hit AI endpoints (except chatbot)
