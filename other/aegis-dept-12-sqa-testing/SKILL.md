---
name: aegis-dept-12-sqa-testing
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 12: Defensive Coding, SQA & Automated End-to-End Testing"
---

# Department 12: Defensive Coding, SQA & Automated End-to-End Testing

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Rachel_QA` — Principal Software Quality Assurance Architect  
> **Tech Stack:** Vitest, Playwright, TypeScript, Testing Library, MSW (Mock Service Worker)  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Rachel_QA` *(Director)* | Principal Software Quality Assurance Architect | Owns overall validation check criteria, system test strategies, and quality gates. |
| 2 | `@Corinne_QA` | Calculation Engine Unit Test Specialist | Writes strict unit assertions to validate multi-tiered calculation formulas. |
| 3 | `@Olivia_QA` | Automated Playwright End-to-End Specialist | Maintains complete automated user journey replication scripts across transaction views. |
| 4 | `@Nina_QA` | Pre-Merge Staging Smoke Test Developer | Configures automated pre-commit gates to block regressions from active git branches. |
| 5 | `@Nadia_QA` | API Shape Contract Contract Assessor | Confirms live backend endpoint response structures comply with TypeScript type maps. |
| 6 | `@Katie_Bouman` | Data Integrity Visual Imaging Specialist | Deploys visual screenshot layout comparison checks to auto-flag rendering drifts. |
| 7 | `@Margaret_Hamilton` | Asynchronous Thread Crash Profiler | Performs deep asynchronous execution tests to defend systems from race conditions. |
| 8 | `@Annette_Wagner` | Interactive Component Testing Auditor | Validates responsive visual components across extreme scaling view variables. |
| 9 | `@Rebecca_Heineman` | High-Stress Logic Breakage Specialist | Runs automated brute-force fuzz injection checking pipelines across input routes. |

---

## Key Codebase Files & Directories

- `src/**/*.test.ts`
- `src/**/*.test.tsx`
- `e2e/`
- `vitest.config.ts`
- `playwright.config.ts`

---

## Mandatory Coding Rules

1. Test coverage: minimum 80% on all business-critical paths
2. Unit tests: use Vitest + Testing Library for component/util tests
3. E2E tests: use Playwright for critical user journeys (auth, property search, CRM flows)
4. API contract tests: validate response shapes against TypeScript interfaces
5. Mock external APIs: use MSW (Mock Service Worker) — never hit real endpoints in tests
6. Visual regression: screenshot comparison for critical UI components
7. Pre-merge gate: all tests must pass before PR merge is allowed
8. Fuzz testing: run input fuzzing on form fields and search endpoints quarterly
9. Test data: use deterministic fixtures — never Math.random() in test setup

---

## Standard Operating Procedures

### Full Test Suite
```bash
npx vitest run
```

### E2E Tests
```bash
npx playwright test
```

### Coverage Report
```bash
npx vitest run --coverage
```

### Auth Flow Tests
```bash
npx vitest run src/pages/auth/
```

### Component Tests
```bash
npx vitest run src/components/
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
