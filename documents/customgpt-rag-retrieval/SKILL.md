---
name: customgpt-rag-retrieval
description: Automatically retrieve relevant information from the organization's CustomGPT.ai knowledge base when answering questions about documented topics, policies, procedures, or technical specifications.
---

# CustomGPT.ai RAG Retrieval Skill

You have access to an enterprise knowledge base via CustomGPT.ai's RAG (Retrieval-Augmented Generation) system. Use this skill to ground your answers in authoritative organizational documentation.

## When to Use This Skill

**DO invoke RAG** when the user:

- Asks about **company policies, procedures, or guidelines**
  - "What's our code review policy?"
  - "How do we handle PII data?"

- Needs information from **internal documentation**
  - "What does the runbook say about deploying to prod?"
  - "Where is the API rate limit documented?"

- Asks about **internal systems, APIs, or configurations**
  - "How do I configure the auth middleware?"
  - "What's the schema for the user table?"

- References **"our documentation"** or **"company docs"**
  - "According to our docs, how should I..."
  - "What does our internal guide say about..."

- Asks about **security, compliance, or regulatory requirements**
  - "What are our GDPR requirements?"
  - "How do we handle SOC-2 compliance?"

- Needs **technical specifications** or **architecture decisions**
  - "What's our standard approach to error handling?"
  - "How is the payment service architected?"

## When NOT to Use This Skill

**DO NOT invoke RAG** for:

- **General programming questions**
  - "How do I write a for loop in Python?"
  - "What's the syntax for async/await?"

- **Public framework/library documentation**
  - "How do I use React hooks?"
  - "What's the Express middleware pattern?"

- **Local file operations**
  - "Read this file and explain it"
  - "What's in the package.json?"

- **Math, logic, or reasoning problems**
  - "Calculate the time complexity"
  - "Debug this algorithm"

- **Creative writing or brainstorming**
  - "Help me name this variable"
  - "Write a commit message"

## How to Invoke

When you determine RAG is appropriate:

1. **Formulate a clear query** based on the user's question
   - Be specific and focused
   - Include relevant context keywords

2. **Call the MCP tool**:
   ```
   mcp__customgpt__send_message(prompt: "your search query")
   ```

3. **Process the response**:
   - The tool returns an answer with citations
   - Sources include document names, page references, and excerpts

## Response Integration

When incorporating RAG results into your response:

### Always Cite Sources
Reference where the information came from:
> According to the Security Guidelines (Section 3.2): "All API tokens must be rotated every 90 days."

### Quote Accurately
When precision matters, use exact wording from sources.

### Acknowledge Gaps
If RAG returns no relevant results:
> I searched the knowledge base but didn't find specific documentation about [topic]. Based on general best practices...

### Combine Context
Integrate RAG results with the conversation context:
> Your documentation specifies [X], so applying that to your current code, you should...

## Example Interaction

**User**: "What is our rate limiting policy for the API?"

**Your process**:
1. Recognize this asks about company policy (RAG appropriate)
2. Invoke: `mcp__customgpt__send_message(prompt: "API rate limiting policy limits configuration")`
3. Receive response with citations
4. Format response:

> According to your API documentation:
>
> Rate limits are configured as follows:
> - **Standard tier**: 100 requests per minute
> - **Enterprise tier**: 1,000 requests per minute
> - Exceeding limits returns HTTP 429 with a `Retry-After` header
>
> **Source**: `api-guidelines.md` (Section 4.2 - Rate Limiting)

## Fallback Behavior

If RAG query fails or returns no results:

1. **Acknowledge** the knowledge base doesn't contain relevant information
2. **Offer** to answer from general knowledge (with appropriate caveats)
3. **Suggest** the user may want to add relevant documentation to their CustomGPT agent

Example:
> I couldn't find specific documentation about [topic] in your knowledge base. Would you like me to provide general guidance based on industry best practices? You might also want to add relevant documentation to your CustomGPT agent for future reference.

## Performance Notes

- RAG queries typically complete in 2-5 seconds
- For complex questions, consider breaking into multiple focused queries
- Results are cached by CustomGPT for improved performance on follow-up questions
