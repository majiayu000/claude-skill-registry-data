---
name: vercel-expert-developer
description: >-
  Vercel expertise: serverless functions (Node/Edge), Next.js deployment, CI/CD, Postgres/KV, performance and cost, Fluid Compute, Power Platform integration. Use when developing, deploying or optimizing on Vercel.
---

# Vercel Expert Developer

Expert guide for developing, deploying, and optimizing serverless applications on Vercel platform, with comprehensive knowledge of October 2025 capabilities including Fluid Compute, Active CPU pricing, and unified function architecture.

## When to Use This Skill

Use this skill when working on:
- Vercel Functions development (Node.js or Edge runtime)
- Next.js deployment and configuration
- Serverless architecture design
- CI/CD pipeline implementation
- Database integration (Postgres, KV, Blob)
- Performance and cost optimization
- Security and authentication patterns
- Power Platform integration (Dynamics 365, Power Automate)
- Monitoring and debugging setup

## Reference Documentation

This skill includes comprehensive reference documentation covering all aspects of Vercel development as of October 2025:

**Read the complete guide:** `references/Vercel_Serverless_Functions_Complete_Development_Guide_October_2025.md`

**Always read this reference document before providing Vercel guidance.** It contains:
- Current platform capabilities (Fluid Compute, Active CPU pricing, Node.js 22)
- Runtime configuration (Node.js vs Edge)
- Development workflows and best practices
- Deployment strategies (Git, CLI, GitHub Actions)
- Environment variables and secrets management
- Database integration patterns
- Performance optimization techniques
- Security best practices
- Cost optimization strategies
- Power Platform integration patterns
- Common patterns and anti-patterns
- October 2025 critical features and updates

## Workflow

When the user requests Vercel-related assistance:

1. **Read the reference document first** to ensure recommendations are based on October 2025 capabilities
2. **Identify the specific need**: development, deployment, optimization, integration, or troubleshooting
3. **Provide targeted guidance** based on the reference documentation
4. **Include code examples** from the reference when applicable
5. **Highlight critical updates**: Fluid Compute, Active CPU pricing, Node.js 22 default, deprecated features
6. **Consider cost implications** and suggest optimization strategies
7. **For Power Platform integration**: Reference the specific integration patterns in the guide

## Key Platform Changes (October 2025)

**Critical to know:**
- **Fluid Compute** (February 2025): 99.37% cold start elimination, 85-90% cost reduction
- **Active CPU Pricing** (June 2025): Pay only for execution time, not I/O waits
- **Node.js 18 deprecated** (September 2025): Upgrade to Node.js 22 required
- **Edge Functions terminology deprecated** (June 2025): Now "Vercel Functions with Edge Runtime"
- **OAuth 2.0 login** (September 2025): Email login deprecated, removal February 1, 2026
- **Vercel Drains** (October 2025): Unified log/trace/analytics export
- **WAF Rate Limiting GA** (October 2025): 300ms global propagation

## Quick Decision Framework

**Choose Node.js Runtime when:**
- Database operations required
- Complex business logic
- File system access needed
- Large dependencies (>4MB)
- Long-running processes (up to 800s)

**Choose Edge Runtime when:**
- Authentication/authorization middleware
- URL rewrites/redirects
- Geolocation-based routing
- Lightweight API endpoints
- Global low latency critical

**Note:** Vercel now recommends migrating from Edge to Node.js for improved performance and reliability (October 2025).

## Response Format

When providing guidance:
- Base all recommendations on the reference document
- Provide complete, working code examples
- Include configuration snippets (vercel.json, package.json)
- Explain cost implications when relevant
- Highlight security considerations
- Reference official documentation URLs when appropriate
- For complex topics, reference specific sections in the guide

## Power Platform Integration Focus

For Power Platform users, pay special attention to:
- Dynamics 365 webhook receiver patterns
- Power Automate HTTP endpoint configuration
- Authentication and signature verification
- Idempotent processing for retries
- Data integration and ETL workflows
- Streaming responses for long-running flows
- Rate limiting to prevent API throttling

These patterns are detailed in the reference documentation under "Power Platform Integration."

## Important Reminders

- Always read the reference document before providing guidance
- Verify recommendations against October 2025 capabilities
- Emphasize cost optimization opportunities (caching, Fluid Compute, regions)
- Highlight security best practices (environment variables, rate limiting, input validation)
- Consider the user's Power Platform background when providing examples
- Monitor for deprecated features (Node.js 18, email login, Edge Functions terminology)

---

**Platform Evolution:** Vercel releases monthly features. The reference document reflects October 2025 capabilities. For updates beyond this date, recommend checking vercel.com/changelog.
