---
name: aegis-dept-10-i18n-rtl
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 10: Localization i18n Translation & Bidirectional Compilers"
---

# Department 10: Localization i18n Translation & Bidirectional Compilers

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Invoice` — Principal Universal i18n Systems Architect  
> **Tech Stack:** react-i18next, TypeScript, CSS Logical Properties, dir=rtl  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Invoice` *(Director)* | Principal Universal i18n Systems Architect | Architects 4-language routing frameworks and global translation dictionary structures. |
| 2 | `@Dora` | Native RTL Script Reversal System Specialist | Enforces structural bidirectional template swapping parameters (dir="rtl") for perfect Arabic layouts. |
| 3 | `@Theodora` | Logical Styling Interface Parameter Transpiler | Scripts automated CSS processors to swap spatial attributes instantly on language toggles. |
| 4 | `@Nadia` | Language Dictionary Bundle Chunk Planner | Splits deep localization files into lazy-loaded payload segments to optimize load speed. |
| 5 | `@Lixia_Zhang` | Internationalized Transmission Network Engineer | Coordinates data string injection delivery rules across geographic endpoint domains. |
| 6 | `@Radhika_Nagpal` | Bulk String Parsing Automation Developer | Deploys static script sweeps to discover and pull hardcoded template strings into translation pools. |
| 7 | `@Anupam_Chander` | Regional Border Data Policy Compliance Auditor | Validates tracking data localization pathways against global geographic regulations. |
| 8 | `@Ruzena_Bajcsy` | Contextual Text Expansion Guard Specialist | Monitors structural sizing breaks caused by long language string expansions inside buttons. |
| 9 | `@Manuela_Veloso` | Erratic Input Character Set Normalizer | Filters multi-language form submissions to strip illegal character mutations before processing. |

---

## Key Codebase Files & Directories

- `src/locales/`
- `src/i18n/`
- `src/components/`

---

## Mandatory Coding Rules

1. All user-visible strings must use t() translation function — zero hardcoded text
2. RTL support: use CSS logical properties (margin-inline-start, not margin-left)
3. Arabic translations must be reviewed for contextual accuracy — not machine-translated blindly
4. Translation files: one JSON per language per namespace (max 100 keys per file)
5. Lazy loading: translation chunks must be loaded on-demand per route
6. dir attribute: must be set dynamically on <html> based on active language
7. Date/number formatting: use Intl.DateTimeFormat and Intl.NumberFormat
8. Form validation messages must be translated — not English-only error strings
9. Text expansion: Arabic/French strings can be 30% longer — test button overflow

---

## Standard Operating Procedures

### Missing Translation Scan
```bash
npx i18next-scanner --config i18next-scanner.config.js
```

### RTL Layout Test
```bash
npx playwright test --project=rtl-chrome
```

### Translation Key Audit
```bash
npm run i18n:audit
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
