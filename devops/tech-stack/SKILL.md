---
name: tech-stack
description: >
  Advise on technology stack selection, architecture decisions, and tooling trade-offs — grounded in team context, scale requirements, and operational reality. Trigger when: the user asks "what tech should I use", "which framework", "should I use X or Y", "help me pick a database", "recommend a stack", or "what's best for building X?"; discussing starting a new project; comparing technologies or evaluating trade-offs; planning system architecture; reviewing an existing stack for improvements; onboarding to a new project and needing to understand the tech choices made. Key capabilities: structured recommendation format (recommended stack, alternatives considered, honest trade-offs, migration path); always clarifies requirements before recommending (team size, scale, budget, deployment environment, timeline); knows common stack patterns for web apps, mobile, data/AI, and microservices; applies boring/proven technology principle for core infrastructure. Also for: debugging architecture problems (wrong tool for the job), evaluating whether to replace an existing component, and stress-testing a proposed stack against failure modes. Ideal for: founders, solo devs, and small teams making high-leverage decisions early in a project's life. Never recommends the newest thing without weighing operational cost.
---

# Tech Stack Advisor Skill

## Process

1. **Clarify requirements first** — before recommending, ask about:
   - Team size and existing expertise
   - Scale expectations (users, data volume)
   - Budget constraints (open source vs paid)
   - Deployment environment (cloud, on-prem, edge)
   - Timeline and MVP vs long-term

2. **Structure recommendations** using this format:
   - **Recommended Stack** with brief rationale
   - **Alternatives Considered** and why not chosen
   - **Trade-offs** honestly stated
   - **Migration path** if they're switching from something existing

## Common Stack Patterns

### Web App (Full Stack)
- Modern: Next.js + TypeScript + PostgreSQL + Prisma + Vercel
- Enterprise: Java Spring Boot / .NET + React + Oracle/MSSQL
- Rapid MVP: Supabase + Next.js or Firebase + React

### Mobile
- Cross-platform: React Native or Flutter
- Native performance critical: Swift (iOS), Kotlin (Android)

### Data / AI
- Python stack: FastAPI + SQLAlchemy + Pandas/Polars + PostgreSQL
- ML serving: FastAPI + PyTorch/TensorFlow + Redis cache

### Microservices
- Node.js or Go for high-throughput services
- Kafka or RabbitMQ for event streaming
- Docker + Kubernetes for orchestration

## Principles
- Prefer boring, proven technology for core infrastructure
- Match stack to team's existing knowledge when possible
- Avoid over-engineering for early-stage projects
- Always consider operational complexity, not just development speed