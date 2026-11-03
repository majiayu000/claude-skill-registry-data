---
name: aegis-dept-08-devops-sre
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 8: DevOps CI/CD Pipelines & Site Reliability Automation (SRE)"
---

# Department 8: DevOps CI/CD Pipelines & Site Reliability Automation (SRE)

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Gwynne` — Principal Code Delivery Automation Director  
> **Tech Stack:** Git, GitHub Actions, Docker, Vercel, TypeScript, Husky, lint-staged  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Gwynne` *(Director)* | Principal Code Delivery Automation Director | Engineers master build verification pipelines, testing bars, and automated deployment blocks. |
| 2 | `@Lisa` | Cloud Edge Production Routing Configurator | Manages system deployment configurations inside distributed cloud edge infrastructure arrays. |
| 3 | `@Annie` | Docker Container Ecosystem Scaffolding Specialist | Containerizes core codebase folders into optimized multi-stage production environments. |
| 4 | `@Corinne` | Cross-Platform Environment State Unifier | Ensures environment variable consistency across local workspaces, staging, and live endpoints. |
| 5 | `@Rachel` | Repository Secret Disclosure Interceptor | Monitors git pull histories to identify and wipe accidentally tracked developer credentials. |
| 6 | `@Radia_Perlman` | Internal Topology Networking Programmer | Optimizes cloud server communication hops to completely minimize package transmission delays. |
| 7 | `@Sister_Mary_Keller` | Static Code Style Rule Engine Architect | Configures compiler validation tools to enforce style properties before repository integration. |
| 8 | `@Adele_Goldberg` | Sandboxed Local Dev Workspace Virtualizer | Builds lightweight local virtualization runtimes for reliable offline debugging loops. |
| 9 | `@Evelyn_Boyd_Granville` | Automated Zero-Downtime Rollback Coordinator | Authors automated safe deployment scripts to roll back software branches instantly if telemetry drops. |

---

## Key Codebase Files & Directories

- `.github/`
- `scripts/orchestrator/`
- `.husky/`
- `package.json`
- `vercel.json`

---

## Mandatory Coding Rules

1. All commits must use Conventional Commits format (feat/fix/chore/refactor)
2. Pre-commit: Husky + lint-staged must run prettier + eslint on staged files
3. Branch protection: main is protected — all changes via PR only
4. PR merge: resolve all review threads before merge (use aegis-unblock-pr.js)
5. Zero dangling branches: delete feature branches after merge
6. Docker: multi-stage builds — dev dependencies excluded from production image
7. Rollback: automated revert if post-deploy health check fails within 5 minutes
8. Secrets: GitHub Secrets for all tokens — never hardcode in CI configs

---

## Standard Operating Procedures

### TypeScript Pre-flight
```bash
npx tsc --noEmit --skipLibCheck
```

### Full Test Suite
```bash
npx vitest run
```

### Lint Check
```bash
npx eslint --max-warnings 0 .
```

### PR Unblock
```bash
node scripts/orchestrator/aegis-unblock-pr.js <pr_number>
```

### Branch Cleanup
```bash
git remote prune origin && git branch --merged main | grep -v main | xargs git branch -d
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
