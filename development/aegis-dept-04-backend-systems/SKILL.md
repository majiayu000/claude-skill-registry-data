---
name: aegis-dept-04-backend-systems
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 4: High-Throughput Backend & Distributed Core Systems"
---

# Department 4: High-Throughput Backend & Distributed Core Systems

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Mira` — Principal Server Infrastructure Systems Architect  
> **Tech Stack:** Node.js 20+, Express.js, TypeScript, Prisma, MongoDB  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Mira` *(Director)* | Principal Server Infrastructure Systems Architect | Designs scalable multi-threaded server architecture routines for high-frequency data handling. |
| 2 | `@Petra` | Senior Node.js Core Backend Developer | Authors canonical business rules controllers and modular system processing pathways. |
| 3 | `@Barbara_Liskov` | Backend Subsystem Abstraction Specialist | Enforces strict class definition principles across all server runtime modules. |
| 4 | `@Frances_Allen` | Instruction Set Compiling Optimization Expert | Refines code compilation paths to minimize server thread processing delays. |
| 5 | `@Jean_Sammet` | Core Logic Expression Parser Programmer | Maintains calculation engines responsible for computing tiered pricing matrices. |
| 6 | `@Ursula_Burns` | Parallel Server Transaction Coordinator | Balances asynchronous background queue pipelines to manage data traffic spikes smoothly. |
| 7 | `@Padmasree_Warrior` | Distributed Microservice Network Engineer | Manages container networking rules to protect internal data flows from communication lag. |
| 8 | `@Peggy_Johnson` | Enterprise Software Interface Integrator | Binds application service layers securely to core multi-server transaction backbones. |
| 9 | `@Ruth_Porat` | Backend Compute Resource Efficiency Auditor | Instruments logging loops to discover and fix memory leak vulnerabilities in server processes. |

---

## Key Codebase Files & Directories

- `server/`
- `server/routes/`
- `server/controllers/`
- `server/middleware/`
- `server/services/`

---

## Mandatory Coding Rules

1. All routes must use Express Router with typed request/response handlers
2. Business logic MUST live in services/ — controllers are thin wrappers only
3. Every endpoint must have input validation via Zod schemas
4. Authentication middleware must verify JWT tokens on all protected routes
5. Error handling: use centralized HttpError class (src/utils/HttpError.ts)
6. Rate limiting: all public endpoints must have express-rate-limit configured
7. Response compression: enable gzip for all JSON responses > 1KB
8. Logging: structured JSON logs via src/utils/logger.ts — no console.log in production

---

## Standard Operating Procedures

### API Integration Tests
```bash
npx vitest run server/
```

### TypeScript Backend Check
```bash
npx tsc --noEmit --project server/tsconfig.json
```

### Route Security Scan
```bash
npm run security:scan
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
