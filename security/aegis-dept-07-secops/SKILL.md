---
name: aegis-dept-07-secops
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 7: Application Defense & Cryptographic Integrity Gates (SecOps)"
---

# Department 7: Application Defense & Cryptographic Integrity Gates (SecOps)

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Sofia` — Principal Cyber Security Shield Architect  
> **Tech Stack:** TypeScript, bcrypt, jsonwebtoken, helmet, csurf, express-rate-limit  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Sofia` *(Director)* | Principal Cyber Security Shield Architect | Owns level 5 system defense layout protocols, session parameters, and encryption boundaries. |
| 2 | `@Katherine` | Identity Access Validation Token Engineer | Maintains fine-grained role-based access control (RBAC) security verification code pathways. |
| 3 | `@Radia` | Input Validation Sanitization Guard Specialist | Scrubs system template fields against persistent cross-site scripting (XSS) exploit vectors. |
| 4 | `@Ecem` | Staging Credential Environment Vault Guardian | Secures infrastructure encryption keys, server credentials, and active database .env files. |
| 5 | `@Joy` | Code Package Vulnerability Auditor | Scans third-party node configurations to intercept and drop outdated external libraries. |
| 6 | `@Shafi_Goldwasser` | Zero-Knowledge Authentication Proof Architect | Develops secure cryptographic validation procedures for remote data handshakes. |
| 7 | `@Dorothy_Denning` | Intrusion Detection System Sequence Developer | Programs real-time server traffic analytics engines to auto-block suspicious query paths. |
| 8 | `@Joan_Feigenbaum` | Decentralized Access Authorization Specialist | Secures authentication code operations across split deployment server instances safely. |
| 9 | `@Mary_Lou_Jepsen` | Runtime Process Stack Boundary Guard | Defends code execution spaces against memory overrun manipulations and trace vulnerabilities. |

---

## Key Codebase Files & Directories

- `server/middleware/auth.ts`
- `src/utils/permissions.ts`
- `src/utils/safeRedirect.ts`
- `src/utils/piiMasker.ts`
- `src/utils/loadSecrets.ts`

---

## Mandatory Coding Rules

1. All authentication must use JWT with RS256 signing — never HS256 in production
2. RBAC enforcement: every route must check permissions via src/utils/permissions.ts
3. XSS prevention: all user inputs must be sanitized before rendering or storage
4. CSRF: all state-changing endpoints must validate CSRF tokens
5. Secrets: never commit .env files — use src/utils/loadSecrets.ts for runtime loading
6. Password hashing: bcrypt with minimum 12 salt rounds
7. PII masking: all logs must run through src/utils/piiMasker.ts before output
8. Dependency scanning: npm audit must pass with 0 high/critical vulnerabilities
9. Safe redirects: all redirect URLs must pass src/utils/safeRedirect.ts validation

---

## Standard Operating Procedures

### Security Audit
```bash
npm audit --production
```

### Permission Tests
```bash
npx vitest run src/utils/permissions.test.ts
```

### PII Masker Tests
```bash
npx vitest run src/utils/piiMasker.test.ts
```

### Safe Redirect Tests
```bash
npx vitest run src/utils/safeRedirect.test.ts
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
