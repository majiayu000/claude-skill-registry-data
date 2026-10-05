---
name: inngest
description: Inngest expert for serverless-first background jobs, event-driven workflows, and durable execution without managing queues or workers. 
category: Document Processing
source: antigravity
tags: [nextjs, pdf, api, ai, agent, llm, automation, workflow, template, design]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/inngest
---


# Inngest Integration

Inngest expert for serverless-first background jobs, event-driven workflows,
and durable execution without managing queues or workers.

## Principles

- Events are the primitive - everything triggers from events, not queues
- Steps are your checkpoints - each step result is durably stored
- Sleep is not a hack - Inngest sleeps are real, not blocking threads
- Retries are automatic - but you control the policy
- Functions are just HTTP handlers - deploy anywhere that serves HTTP
- Concurrency is a first-class concern - protect downstream services
- Idempotency keys prevent duplicates - use them for critical operations
- Fan-out is built-in - one event can trigger many functions

## Capabilities

- inngest-functions
- event-driven-workflows
- step-functions
- serverless-background-jobs
- durable-sleep
- fan-out-patterns
- concurrency-control
- scheduled-functions

## Scope

- redis-queues -> bullmq-specialist
- workflow-orchestration -> temporal-craftsman
- message-streaming -> event-architect
- infrastructure -> infra-architect

## Tooling

### Core

- inngest
- inngest-cli

### Frameworks

- nextjs
- express
- hono
- remix
- sveltekit

### Deployment

- vercel
- cloudflare-workers
- netlify
- railway
- fly-io

### Patterns

- step-functions
- event-fan-out
- scheduled-cron
- webhook-handling

## Patterns

### Basic Function Setup

Inngest function with typed events in Next.js

**When to use**: Starting with Inngest in any Next.js project

// lib/inngest/client.ts
import { Inngest } from 'inngest';

export const inngest = new Inngest({
  id: 'my-app',
  schemas: new EventSchemas().fromRecord<Events>(),
});

// Define your events with types
type Events = {
  'user/signed.up': { data: { userId: string; email: string } };
  'order/placed': { data: { orderId: string; total: number } };
};

// lib/inngest/functions.ts
import { inngest } from './client';

export const sendWelcomeEmail = inngest.createFunction(
  { id: 'send-welcome-email' },
  { event: 'user/signed.up' },
  async ({ event, step }) => {
    // Step 1: Get user details
    const user = await step.run('get-user', async () => {
      return await db.users.findUnique({ where: { id: event.data.userId } });
    });

    // Step 2: Send welcome email
    await step.run('send-email', async () => {
      await resend.emails.send({
        to: user.email,
        subject: 'Welcome!',
        template: 'welcome',
      });
    });

    // Step 3: Wait 24 hours, then send tips
    await step.sleep('wait-for-tips', '24h');

    await step.run('send-tips', async () => {
      await resend.emails.send({
        to: user.email,
        subject: 'Getting Started Tips',
        template: 'tips',
      });
    });
  }
);

// app/api/inngest/route.ts (Next.js App Router)
import { serve } from 'inngest/next';
import { inngest } from '@/lib/inngest/client';
import { sendWelcomeEmail } from '@/lib/inngest/functions';

export const { GET, POST, PUT } = serve({
  client: inngest,
  functions: [sendWelcomeEmail],
});

### Multi-Step Workflow

Complex workflow with parallel steps and error handling

**When to use**: Processing that involves multiple services or long waits

export const processOrder = inngest.createFunction(
  {
    id: 'process-order',
    retries: 3,
    concurrency: { limit: 10 },  // Max 10 orders processing at once
  },
  { event: 'order/placed' },
  async ({ event, step }) => {
    const { orderId } = event.data;

    // Parallel steps - both run simultaneously
    const [inventory, payment] = await Promise.all([
      step.run('check-inventory', () => checkInventory(orderId)),
      step.run('validate-payment', () => validatePayment(orderId)),
    ]);

    if (!inventory.available) {
      // Send event instead of direct call (fan-out pattern)
      await step.sendEvent('notify-backorder', {
        name: 'order/backordered',
        data: { orderId, items: inventory.missing },
      });
      return { status: 'backordered' };
    }

    // Process payment
    const charge = await step.run('charge-payment', async () => {
      return await stripe.charges.create({
        amount: event.data.total,
        customer: payment.customerId,
      });
    });

    // Ship order
    await step.run('ship-order', () => fulfillment.ship(orderId));

    return { status: 'completed', chargeId: charge.id };
  }
);

### Scheduled/Cron Functions

Functions that run on a schedule

**When to use**: Recurring tasks like daily reports or cleanup jobs

export const dailyDigest = inngest.createFunction(
  { id: 'daily-digest' },
  { cron: '0 9 * * *' },  // Every day at 9am UTC
  async ({ step }) => {
    // Get all users who want digests
    const users = await step.run('get-users', async () => {
      return await db.users.findMany({
        where: { digestEnabled: true },
      });
    });

    // Send to each user (creates child events)
    await step.sendEvent(
      'send-digests',
      users.map(user => ({
        name: 'digest/send',
        
