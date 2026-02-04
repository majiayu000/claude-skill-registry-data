---
name: n8n-integration-patterns
description: Decide when to use n8n workflows versus Next.js server actions for backend logic. Use when implementing complex multi-step workflows, AI agent pipelines, or external service integrations. Provides patterns for both runtime webhook integration and development-time architectural decisions.
---

# n8n Integration Patterns

Guide for deciding between n8n workflow automation and Next.js server actions when implementing backend features.

## Overview

This skill helps you make architectural decisions about where to implement backend logic:

- **Next.js Server Actions** - Most features should use this (default choice)
- **n8n Workflows** - Specific use cases benefit from visual workflow automation

The organization maintains an n8n instance at `https://n8n.reodorstudios.com` with comprehensive MCP integration for workflow development.

## Decision Framework

### Use Next.js Server Actions When

✅ **CRUD Operations** - Standard database create, read, update, delete
✅ **Simple Business Logic** - Authentication, authorization, data validation
✅ **Direct Database Queries** - Supabase client operations with RLS
✅ **Form Submissions** - User input processing with Zod validation
✅ **API Integrations** (Simple) - Single API call with straightforward response handling
✅ **Type Safety Required** - End-to-end TypeScript type checking needed
✅ **Fast Response Times** - Operations that must complete in <5 seconds

**Rationale**: Server actions provide excellent DX, full type safety from database → frontend, and tight integration with React components.

### Use n8n Workflows When

✅ **Complex Multi-Step Workflows** - 5+ steps with branching logic and error handling
✅ **AI Agent Pipelines** - Multiple AI interactions with tool usage and decision trees
✅ **External Service Orchestration** - Coordinating 3+ external APIs (Notion → AI → Slack → Database)
✅ **Long-Running Tasks** - Operations taking >10 seconds (batch processing, data transformations)
✅ **Scheduled Automation** - Cron-based tasks with complex schedules and dependencies
✅ **Webhook Chaining** - Receiving webhooks that trigger multi-step processes
✅ **Visual Workflow Design** - Non-developers need to understand/modify the logic
✅ **Rapid Prototyping** - Testing complex integrations without writing code

**Rationale**: n8n excels at orchestrating complex, multi-step processes with visual debugging, pre-built integrations, and easy modifications.

## Common Use Cases

### Scenario 1: User Profile Update

**Use Server Actions** ✅

```typescript
// server/profile.actions.ts
"use server";

export async function updateProfile(data: ProfileUpdate) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return await supabase.from("profiles").update(data).eq("id", user.id);
}
```

**Why**: Simple CRUD, requires RLS, needs type safety, fast response.

### Scenario 2: AI Content Pipeline

**Use n8n Workflow** ✅

```
Webhook Trigger
  → Fetch content from Notion (n8n Notion node)
  → AI Agent: Summarize content (OpenAI node)
  → AI Agent: Generate social posts (OpenAI node)
  → Store in database (Supabase node)
  → Post to Slack (Slack node)
  → Send confirmation email (Resend node)
  → Respond to webhook
```

**Why**: 6+ steps, multiple external services, AI interactions, long-running, benefits from visual debugging.

### Scenario 3: Simple AI Query

**Use Server Actions** ✅

```typescript
// server/ai.actions.ts
"use server";

export async function generateSummary(text: string) {
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: `Summarize: ${text}` }],
  });

  return response.choices[0].message.content;
}
```

**Why**: Single AI call, needs type safety, integrated with React components, fast response.

### Scenario 4: Complex Booking System

**Use n8n Workflow** ✅

```
Webhook: New Booking Request
  → Validate booking data
  → Check calendar availability (external API)
  → If available:
    → Create booking in database
    → Send confirmation email
    → Create calendar event
    → Notify admin on Slack
    → Trigger payment processing
  → If not available:
    → Find alternative slots (AI agent)
    → Send suggestions email
  → Respond to webhook
```

**Why**: Complex branching logic, multiple external services, error handling at each step, benefits from visual flow.

## Integration Patterns

### Pattern 1: Runtime Webhook Integration

Call n8n workflows from server actions when needed:

```typescript
// server/workflow.actions.ts
"use server";

import { env } from "@/lib/env";

interface N8nWebhookResponse {
  status: string;
  data?: any;
  error?: string;
}

export async function triggerN8nWorkflow<T = any>(
  workflowPath: string,
  data: any
): Promise<N8nWebhookResponse> {
  try {
    const response = await fetch(`${env.N8N_WEBHOOK_URL}/${workflowPath}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${env.N8N_WEBHOOK_SECRET}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      return {
        status: "error",
        error: `Workflow failed: ${response.statusText}`,
      };
    }

    const result = await response.json();
    return { status: "success", data: result };
  } catch (error) {
    console.error("n8n workflow error:", error);
    return {
      status: "error",
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

// Usage example
export async function processComplexOrder(orderId: string) {
  const supabase = await createClient();

  // Get order data from database
  const { data: order } = await supabase
    .from("orders")
    .select("*")
    .eq("id", orderId)
    .single();

  // Trigger n8n workflow for complex processing
  const result = await triggerN8nWorkflow("process-order", {
    orderId,
    orderData: order,
  });

  if (result.status === "error") {
    return { error: result.error, data: null };
  }

  return { error: null, data: result.data };
}
```

### Pattern 2: Environment Configuration

Add n8n configuration to your environment variables:

```typescript
// lib/env.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    // ... existing env vars
    N8N_WEBHOOK_URL: z.string().url().optional(),
    N8N_WEBHOOK_SECRET: z.string().optional(),
  },
});
```

```bash
# .env.local
N8N_WEBHOOK_URL=https://n8n.reodorstudios.com/webhook
N8N_WEBHOOK_SECRET=your-webhook-secret
```

### Pattern 3: Development-Time Alternative

During feature planning, consider both approaches:

```typescript
// Option A: Server Action (Simple AI query)
export async function generateBlogPost(topic: string) {
  const content = await openai.generate({ topic });
  const supabase = await createClient();
  return await supabase.from("posts").insert({ content });
}

// Option B: n8n Workflow (Complex content pipeline)
// When the flow involves:
// - Multiple AI generations (outline → content → social posts)
// - External research (web scraping, API calls)
// - Multi-platform publishing (blog, social, newsletter)
// - Content approval workflow
// → Build workflow in n8n repo instead
```

## n8n Workflow Development

The organization maintains a separate n8n repository with comprehensive tooling:

### Repository Location

```
/path/to/your/repo/reodor-studios/n8n/
```

### Development Workflow

1. **Design Workflow** - Describe requirements to Claude Code
2. **Build with MCP Tools** - Use n8n-mcp server for node documentation
3. **Validate** - Use validation tools before deployment
4. **Test** - Execute workflow in n8n instance
5. **Version Control** - Save workflow JSON to repo
6. **Integrate** - Call from server actions if needed

### Available MCP Tools

When developing n8n workflows, you have access to:

- `search_nodes` - Find n8n nodes by functionality
- `get_node_info` - Detailed node documentation
- `get_node_essentials` - Minimal config for operations
- `search_templates` - Find workflow examples
- `validate_workflow` - Check workflow before deployment
- `create_workflow` - Deploy to n8n instance

### n8n Skills

The n8n repo includes 7 specialized skills:

1. **n8n-expression-syntax** - Expression patterns
2. **n8n-mcp-tools-expert** - MCP tool usage
3. **n8n-workflow-patterns** - Proven architectures
4. **n8n-validation-expert** - Error fixing
5. **n8n-node-configuration** - Node setup
6. **n8n-code-javascript** - JavaScript patterns
7. **n8n-code-python** - Python patterns

## Real-World Examples

### Example 1: Newsletter System

**Server Actions** ✅ for subscriber management:

```typescript
// server/newsletter.actions.ts
export async function subscribeToNewsletter(email: string) {
  const supabase = await createClient();
  return await supabase.from("subscribers").insert({ email });
}
```

**n8n Workflow** ✅ for sending newsletters:

```
Cron Trigger (Weekly)
  → Fetch new blog posts (Supabase)
  → Generate newsletter content (AI)
  → Fetch subscribers (Supabase)
  → Send emails (Resend batch)
  → Track opens/clicks
  → Update analytics (Supabase)
```

### Example 2: User Onboarding

**Server Actions** ✅ for initial signup:

```typescript
export async function createUser(data: SignupData) {
  const supabase = await createClient();
  const { data: user } = await supabase.auth.signUp(data);
  await supabase.from("profiles").insert({ user_id: user.id });
  return user;
}
```

**n8n Workflow** ✅ for onboarding email sequence:

```
Webhook: New User Created
  → Wait 1 hour
  → Send welcome email
  → Wait 24 hours
  → Send feature guide email
  → Wait 3 days
  → Check if user is active
  → If inactive: Send re-engagement email
  → If active: Send pro tips email
```

## Testing and Debugging

### Server Actions Testing

```typescript
// Standard approach using Supabase client
const { data, error } = await myServerAction(params);
if (error) {
  toast.error(error.message);
  return;
}
// Process data
```

### n8n Workflow Testing

1. Test in n8n UI with manual execution
2. Use webhook testing tools (curl, Postman)
3. Check execution logs in n8n interface
4. Validate data transformations between nodes

```bash
# Test n8n webhook locally
curl -X POST \
  https://n8n.reodorstudios.com/webhook/test-workflow \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## Migration Considerations

### When to Migrate from Server Actions to n8n

Consider migration when:

- Server action becomes >200 lines
- Multiple external API calls with complex error handling
- Need for visual debugging of multi-step process
- Non-developers need to modify workflow logic
- Workflow needs scheduling/cron capabilities

### When to Migrate from n8n to Server Actions

Consider migration when:

- Workflow is simple (1-2 steps)
- Need tighter type safety
- Performance becomes critical (<100ms response time)
- Workflow rarely changes (set it and forget it)
- External services can be replaced with direct API calls

## Best Practices

### DO

✅ Default to server actions for standard features
✅ Use n8n for complex, multi-step orchestration
✅ Document workflow purpose in both code and n8n
✅ Secure n8n webhooks with authentication
✅ Version control n8n workflow JSON files
✅ Test workflows thoroughly before production
✅ Monitor n8n execution logs for errors

### DON'T

❌ Use n8n for simple CRUD operations
❌ Skip type validation when calling n8n webhooks
❌ Hardcode secrets in workflow configurations
❌ Deploy untested workflows to production
❌ Build complex AI agents in server actions (use n8n)
❌ Ignore n8n execution failures silently

## Summary

**Default Choice**: Next.js Server Actions for standard features

**Consider n8n When**:

- Complex multi-step workflows (5+ steps)
- AI agent pipelines with tool usage
- External service orchestration (3+ APIs)
- Long-running tasks (>10 seconds)
- Visual workflow design needed

**Integration**: Call n8n webhooks from server actions when needed

**Development**: Use n8n repo with MCP tools and specialized skills

For detailed n8n workflow development, see:

- n8n repository: `/Users/magnusrodseth/dev/capra/reodor-studios/n8n/`
- Technical documentation: `docs/technical/n8n-integration.md` (to be created)
- n8n instance: `https://n8n.reodorstudios.com`
