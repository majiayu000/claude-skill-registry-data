---
name: B2A
slug: b2a
version: 1.0.0
description: Sell to AI agents with machine-readable products, agent-optimized APIs, structured pricing, and discovery strategies for the agentic economy.
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User building products/services for AI agents as customers. Covers making products agent-discoverable, designing for autonomous purchasing, payment integration, and competing when buyers compare cold data instead of responding to storytelling.

## Quick Reference

| Topic | File |
|-------|------|
| Technical implementation | `infrastructure.md` |
| Agent discovery & SEO | `discovery.md` |
| Retail/ecommerce specifics | `retail.md` |

## The Paradigm Shift

| B2C/B2B | B2A |
|---------|-----|
| Humans browse, compare, feel | Agents query, parse, decide |
| Emotional storytelling wins | Structured data wins |
| UX optimized for eyes | APIs optimized for parsing |
| Brand = trust + emotion | Brand = verified track record |
| Loyalty = relationship | Loyalty = switching cost |
| Marketing = persuasion | Marketing = engineering |

## Core Rules

### 1. Machine-Readable First
- Products must be structured objects, not prose descriptions
- JSON-LD, Schema.org, OpenAPI with typed fields
- If an agent has to "interpret" text to extract price/specs, you lose
- Normalize units: `shipping_days_max: 2`, not "fast shipping"

### 2. Comparability Is Everything
Agents compare ruthlessly. Win by being comparable:
- Standardized attributes across your catalog
- Same fields as competitors (price_currency, availability_stock)
- SLAs with concrete numbers, not promises
- "Better" must be objectively measurable

### 3. Discovery ≠ SEO
Agents don't Google. They query registries and APIs:
- Publish in skill stores / capability directories
- `/.well-known/ai-plugin.json` or MCP tools
- Metadata must declare capabilities, not market them
- The new PageRank = ranking in agent skill stores

### 4. Trust Is Verified, Not Told
Agents don't believe claims. They verify:
- Uptime/latency/SLA history via API, not badges
- Reviews from other agents (programmatic reputation)
- Certifications as queryable data, not PDF downloads
- Track record > marketing copy

### 5. Zero-Friction Trial or Death
Agents don't "consider"—they test or discard:
- Onboarding < 1 API call
- Sandbox with rate limits, not "talk to sales"
- Must work perfectly first time (no second chances)
- Errors must be machine-readable, not HTML pages

### 6. Payments for Agents
The agent needs to transact autonomously:
- Stripe Agent Toolkit, Mastercard Agent Pay, or similar
- Pre-authorized budgets (agent has $X to spend)
- Programmatic receipts and confirmations
- Escrow for trust between unknown parties

### 7. Metrics That Matter

| Metric | What It Measures |
|--------|-----------------|
| Agent Conversion Rate | % queries → purchase |
| Decision Latency | Time from first query to commit |
| Comparison Survival | % times reaching final shortlist |
| Repeat Agent Retention | % agents that return |
| API Error Rate | Failures causing agent to discard |

Traditional metrics (page views, bounce rate) are meaningless.

## Common Traps

| Trap | Why It Fails |
|------|--------------|
| Pretty website, no API | Agents don't see your UI |
| "Contact us for pricing" | Agents need programmatic pricing |
| Marketing copy in descriptions | Agents parse data, skip prose |
| HTML error pages | Agents need JSON errors |
| Manual onboarding | Agents won't wait |
| Trust badges instead of APIs | Unverifiable = untrusted |
| Optimizing for humans first | Delays agent-readiness |

## Honest Limitations

What an AI helping you with B2A cannot do:
- **Create track record** — You have to actually deliver 99.9% uptime
- **Know internal rankings** — How Claude/GPT rank skills is opaque
- **Predict agent decisions** — Each agent has its own heuristics
- **Guarantee discovery** — Skill stores may have hidden placement deals
- **Prevent gaming** — Competitors lying about specs is real

## Readiness Checklist

```
□ Products exposed via structured API (not scraping required)
□ Pricing programmatically queryable
□ Inventory/availability real-time
□ Authentication supports client_credentials (not interactive)
□ Errors return JSON with semantic codes
□ Onboarding works in < 5 API calls
□ Payment rails support autonomous agents
□ SLA metrics exposed via API
□ Listed in relevant skill registries
```
