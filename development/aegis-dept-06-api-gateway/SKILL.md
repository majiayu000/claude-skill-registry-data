---
name: aegis-dept-06-api-gateway
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 6: Distributed Gateway Hubs & Cross-Service API Routers"
---

# Department 6: Distributed Gateway Hubs & Cross-Service API Routers

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Ruchi` — Principal API Platform Gateway Architect  
> **Tech Stack:** Express.js, REST, WebSocket (socket.io), TypeScript, Zod  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Ruchi` *(Director)* | Principal API Platform Gateway Architect | Designs unified edge routing distribution maps and public API entry gateways. |
| 2 | `@Daniela` | Microservice Inter-Service Contract Specialist | Establishes RPC network connection parameters and message communication contracts. |
| 3 | `@Mary_Meeker` | Network Payload Scaling Analyst | Monitors transaction request flows to dynamically scale internal gateway load bounds. |
| 4 | `@Amy_Hood` | External Webhook Lifecycle Cost Specialist | Audits transaction API costs to guarantee optimized outbound request data weights. |
| 5 | `@Susan_Wojcicki` | Content Delivery Network Routing Engineer | Configures edge network proxies to accelerate binary media payload delivery scripts. |
| 6 | `@Meg_Whitman` | Container Microservice Node Orchestrator | Manages automated cluster rollover parameters during continuous delivery updates. |
| 7 | `@Angela_Ahrendts` | Third-Party Platform Hook Protocol Designer | Standardizes ingress communication maps for handling external developer platform hooks. |
| 8 | `@Sheryl_Sandberg` | Cross-Department Contract Alignment Coordinator | Harmonizes endpoint request-response interface properties across isolated codebase tracks. |
| 9 | `@Kim_Swift` | High-Velocity Stream Processing Programmer | Optimizes event broadcasting message loops to maintain real-time web socket data syncs. |

---

## Key Codebase Files & Directories

- `server/routes/`
- `server/middleware/`
- `server/services/`
- `src/utils/apiClient.ts`

---

## Mandatory Coding Rules

1. API versioning: all public endpoints must be under /api/v1/ prefix
2. Request/response contracts must be defined with Zod schemas
3. Webhook handlers must validate signatures before processing payloads
4. CDN: static assets must be served via edge with Cache-Control headers
5. WebSocket: rooms must be scoped per-tenant — no cross-tenant data leaks
6. Rate limiting: tier-based — 100/min for standard, 1000/min for premium
7. CORS: whitelist only known origins — never use wildcard in production
8. Payload compression: responses > 1KB must use gzip encoding

---

## Standard Operating Procedures

### API Contract Tests
```bash
npx vitest run server/routes/
```

### WebSocket Load Test
```bash
npm run test:ws:load
```

### OpenAPI Spec Validation
```bash
npx swagger-cli validate openapi.yaml
```

---

## Aegis V4.1 Governance (All Departments)

1. **Single Purpose File Law:** Every source file must have a single responsibility and remain under 350 lines.
2. **Canonical 5-Way File Standard:** View (`.view.tsx`), Logic (`.logic.ts`), Styles (`.styles.ts`), Data (`.data.ts`), Config (`.config.ts`).
3. **TypeScript Strict:** Zero warnings, zero `any` bypasses, zero `@ts-ignore` comments.
4. **Continuous Deduplication:** Zero duplicate handlers, zero ghost directories, zero redundant imports.
5. **Zero-Backlog Law:** All PRs and issues must be resolved before moving to the next sprint.
6. **Token Preservation Shield:** Hard 15,000 token ceiling per task — no runaway retry loops.
7. **Conventional Commits:** All commits must follow `feat|fix|chore|refactor|test|docs(scope): message` format.
