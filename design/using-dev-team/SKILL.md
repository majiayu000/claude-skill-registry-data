---
name: ring:using-dev-team
description: |
  7 specialist developer agents for backend (Go/TypeScript), DevOps, frontend,
  design, QA, and SRE. Dispatch when you need deep technology expertise.

trigger: |
  - Need deep expertise for specific technology (Go, TypeScript)
  - Building infrastructure/CI-CD → ring:devops-engineer
  - Frontend with design focus → ring:frontend-designer
  - Test strategy needed → ring:qa-analyst
  - Reliability/monitoring → ring:sre

skip_when: |
  - General code review → use default plugin reviewers
  - Planning/design → use brainstorming
  - Debugging → use ring:systematic-debugging

related:
  similar: [ring:using-ring]
---

# Using Ring Developer Specialists

The ring-dev-team plugin provides 7 specialized developer agents. Use them via `Task tool with subagent_type:`.

See [CLAUDE.md](https://raw.githubusercontent.com/LerianStudio/ring/main/CLAUDE.md) and [ring:using-ring](https://raw.githubusercontent.com/LerianStudio/ring/main/default/skills/using-ring/SKILL.md) for canonical workflow requirements and ORCHESTRATOR principle. This skill introduces dev-team-specific agents.

**Remember:** Follow the **ORCHESTRATOR principle** from `ring:using-ring`. Dispatch agents to handle complexity; don't operate tools directly.

---

## Blocker Criteria - STOP and Report

<block_condition>
- Technology Stack decision needed (Go vs TypeScript)
- Architecture decision needed (monolith vs microservices)
- Infrastructure decision needed (cloud provider)
- Testing strategy decision needed (unit vs E2E)
</block_condition>

If any condition applies, STOP and ask user.

**always pause and report blocker for:**

| Decision Type | Examples | Action |
|--------------|----------|--------|
| **Technology Stack** | Go vs TypeScript for new service | STOP. Check existing patterns. Ask user. |
| **Architecture** | Monolith vs microservices | STOP. This is a business decision. Ask user. |
| **Infrastructure** | Cloud provider choice | STOP. Check existing infrastructure. Ask user. |
| **Testing Strategy** | Unit vs E2E vs both | STOP. Check QA requirements. Ask user. |

**You CANNOT make technology decisions autonomously. STOP and ask.**

---

## Common Misconceptions - REJECTED

See [shared-patterns/shared-anti-rationalization.md](../shared-patterns/shared-anti-rationalization.md) for universal anti-rationalizations (including Specialist Dispatch section).

**Self-sufficiency bias check:** If you're tempted to implement directly, ask:
1. Is there a specialist for this? (Check the 7 specialists below)
2. Would a specialist follow standards I might miss?
3. Am I avoiding dispatch because it feels like "overhead"?

**If any answer is yes → You MUST DISPATCH the specialist. This is NON-NEGOTIABLE.**

---

## Anti-Rationalization Table

See [shared-patterns/shared-anti-rationalization.md](../shared-patterns/shared-anti-rationalization.md) for universal anti-rationalizations (including Specialist Dispatch section and Universal section).

---

### Cannot Be Overridden

<cannot_skip>
- Dispatch to specialist (standards loading required)
- 6-gate development cycle (quality gates)
- Parallel reviewer dispatch (not sequential)
- TDD in Gate 0 (test-first)
- User approval in Gate 5
</cannot_skip>

**These requirements are NON-NEGOTIABLE:**

| Requirement | Why It Cannot Be Waived |
|-------------|------------------------|
| **Dispatch to specialist** | Specialists have standards loading, you don't |
| **6-gate development cycle** | Gates prevent quality regressions |
| **Parallel reviewer dispatch** | Sequential review = 3x slower, same cost |
| **TDD in Gate 0** | Test-first ensures testability |
| **User approval in Gate 5** | Only users can approve completion |

**User cannot override these. Time pressure cannot override these. "Simple task" cannot override these.**

---

## Pressure Resistance

See [shared-patterns/shared-pressure-resistance.md](../shared-patterns/shared-pressure-resistance.md) for universal pressure scenarios (including Combined Pressure Scenarios and Emergency Response).

**Critical Reminder:**
- **Urgency ≠ Permission to bypass** - Emergencies require MORE care, not less
- **Authority ≠ Permission to bypass** - Ring standards override human preferences
- **Sunk Cost ≠ Permission to bypass** - Wrong approach stays wrong at 80% completion

---

## Emergency Response Protocol

See [shared-patterns/shared-pressure-resistance.md](../shared-patterns/shared-pressure-resistance.md) → Emergency Response section for the complete protocol.

**Emergency Dispatch Template:**
```
Task tool:
  subagent_type: "ring:backend-engineer-golang"
  model: "opus"
  prompt: "URGENT PRODUCTION INCIDENT: [brief context]. [Your specific request]"
```

**IMPORTANT:** Specialist dispatch takes 5-10 minutes, not hours. This is NON-NEGOTIABLE even under CEO pressure.

---

## Combined Pressure Scenarios

See [shared-patterns/shared-pressure-resistance.md](../shared-patterns/shared-pressure-resistance.md) → Combined Pressure Scenarios section.

---

## 7 Developer Specialists

<dispatch_required agent="{specialist}" model="opus">
Use Task tool to dispatch appropriate specialist based on technology need.
</dispatch_required>

| Agent | Specializations | Use When |
|-------|-----------------|----------|
| **`ring:backend-engineer-golang`** | Go microservices, PostgreSQL/MongoDB, Kafka/RabbitMQ, OAuth2/JWT, gRPC, concurrency | Go services, DB optimization, auth/authz, concurrency issues |
| **`ring:backend-engineer-typescript`** | TypeScript/Node.js, Express/Fastify/NestJS, Prisma/TypeORM, async patterns, Jest/Vitest | TS backends, JS→TS migration, NestJS design, full-stack TS |
| **`ring:devops-engineer`** | Docker/Compose, Terraform/Helm, cloud infra, secrets management | Containerization, local dev setup, IaC provisioning, Helm charts |
| **`frontend-bff-engineer-typescript`** | Next.js API Routes BFF, Clean/Hexagonal Architecture, DDD patterns, Inversify DI, repository pattern | BFF layer, Clean Architecture, DDD domains, API orchestration |
| **`ring:frontend-designer`** | Bold typography, color systems, animations, unexpected layouts, textures/gradients | Landing pages, portfolios, distinctive dashboards, design systems |
| **`ring:qa-analyst`** | Test strategy, Cypress/Playwright E2E, coverage analysis, API testing, performance | Test planning, E2E suites, coverage gaps, quality gates |
| **`ring:sre`** | Structured logging, tracing, health checks, observability | Logging validation, tracing setup, health endpoint verification |

**Dispatch template:**
```
Task tool:
  subagent_type: "ring:{agent-name}"
  model: "opus"
  prompt: "{Your specific request with context}"
```

**Note:** `ring:frontend-designer` = visual aesthetics. `frontend-bff-engineer-typescript` = business logic/architecture.

---

## When to Use Developer Specialists vs General Review

### Use Developer Specialists for:
- ✅ **Deep technical expertise needed** – Architecture decisions, complex implementations
- ✅ **Technology-specific guidance** – "How do I optimize this Go service?"
- ✅ **Specialized domains** – Infrastructure, SRE, testing strategy
- ✅ **Building from scratch** – New service, new pipeline, new testing framework

### Use General Review Agents for:
- ✅ **Code quality assessment** – Architecture, patterns, maintainability
- ✅ **Correctness & edge cases** – Business logic verification
- ✅ **Security review** – OWASP, auth, validation
- ✅ **Post-implementation** – Before merging existing code

**Both can be used together:** Get developer specialist guidance during design, then run general reviewers before merge.

---

## Dispatching Multiple Specialists

If you need multiple specialists (e.g., backend engineer + DevOps engineer), dispatch in **parallel** (single message, multiple Task calls):

```
✅ CORRECT:
Task #1: ring:backend-engineer-golang
Task #2: ring:devops-engineer
(Both run in parallel)

❌ WRONG:
Task #1: ring:backend-engineer-golang
(Wait for response)
Task #2: ring:devops-engineer
(Sequential = 2x slower)
```

---

## ORCHESTRATOR Principle

Remember:
- **You're the orchestrator** – Dispatch specialists, don't implement directly
- **Don't read specialist docs yourself** – Dispatch to specialist, they know their domain
- **Combine with ring:using-ring principle** – Skills + Specialists = complete workflow

### Good Example (ORCHESTRATOR):
> "I need a Go service. Let me dispatch `ring:backend-engineer-golang` to design it."

### Bad Example (OPERATOR):
> "I'll manually read Go best practices and design the service myself."

---

## Available in This Plugin

**Agents:** See "7 Developer Specialists" table above.

**Skills:** `ring:using-dev-team` (this), `ring:dev-cycle` (6-gate workflow), `ring:dev-refactor` (codebase analysis)

**Commands:** `/ring:dev-cycle` (execute tasks), `/ring:dev-refactor` (analyze codebase)

**Note:** Missing agents? Check `.claude-plugin/marketplace.json` for ring-dev-team plugin.

---

## Development Workflows

All workflows converge to the 6-gate development cycle:

| Workflow | Entry Point | Output | Then |
|----------|-------------|--------|------|
| **New Feature** | `/ring:pre-dev-feature "description"` | `docs/pre-dev/{feature}/tasks.md` | → `/ring:dev-cycle tasks.md` |
| **Direct Tasks** | `/ring:dev-cycle tasks.md` | — | Execute 6 gates directly |
| **Refactoring** | `/ring:dev-refactor` | `docs/refactor/{timestamp}/tasks.md` | → `/ring:dev-cycle tasks.md` |

**6-Gate Development Cycle:**

| Gate | Focus | Agent(s) |
|------|-------|----------|
| **0: Implementation** | TDD: RED→GREEN→REFACTOR | `backend-engineer-*`, `frontend-bff-engineer-typescript` |
| **1: DevOps** | Dockerfile, docker-compose, .env | `ring:devops-engineer` |
| **2: SRE** | Health checks, logging, tracing | `ring:sre` |
| **3: Testing** | Unit tests, coverage ≥85% | `ring:qa-analyst` |
| **4: Review** | 3 reviewers IN PARALLEL | `ring:code-reviewer`, `ring:business-logic-reviewer`, `ring:security-reviewer` |
| **5: Validation** | User approval: APPROVED/REJECTED | User decision |

**Key Principle:** All development follows the same 6-gate process.

---

## Integration with Other Plugins

- **ring:using-ring** (default) – ORCHESTRATOR principle for all agents
- **ring:using-pm-team** – Pre-dev workflow agents
- **ring:using-finops-team** – Financial/regulatory agents

Dispatch based on your need:
- General code review → default plugin agents
- Specific domain expertise → ring-dev-team agents
- Feature planning → ring-pm-team agents
- Regulatory compliance → ring-finops-team agents
