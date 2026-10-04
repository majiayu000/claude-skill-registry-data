---
name: md-portal-skill
description: Use this skill when developing, testing, debugging, or modifying code inside the Managing Director Portal frontend (apps/md-portal). It applies to high-level dashboards, budget monitoring, project health overview, workforce capacity metrics, and the Analytics Copilot AI assistant interface.
---

# Managing Director Portal Development Skill

Use this skill when modifying, running, or analyzing the **MD Portal** frontend application.

## Overview

- **Location**: [apps/md-portal/](file:///c:/projects/git/product/production/apps/md-portal)
- **Local Port**: `3006` (runs on `http://localhost:3006`)
- **Key Target Roles**: `Role.MANAGING_DIRECTOR`, `Role.CEO`
- **Authentication Entrypoint**: `http://localhost:3001/auth/internal/login` (MFA/TOTP required)
- **Related Backend Services**:
  - `analytics-service` (Port `8091`, API path `/api/v1/analytics/**`)
  - `ai-service` (Port `8092`, API path `/api/v1/ai/**`)
  - `employee-service` (Port `8088`, API path `/api/v1/employee/**`)
  - `hr-service` (Port `8086`, API path `/api/v1/hr/**`)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/md-portal/src/app/dashboard/layout.tsx) - Configures executive page framing, Analytics Copilot panel, and notification components.
- **Sub-routes (`src/app/dashboard/`)**:
  - `budget`: High-level charts tracking budget allocation, spending, and margin performance.
  - `projects`: Summary views of project statuses, risk logs, and delivery milestones.
  - `workforce`: Employee distribution by department, skill matrix, and contractor allocations.

---

## Development Workflow

### How to Run Locally

To spin up the MD Portal, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\md-portal\mdrun.bat
```

### Credentials for Testing
- **Test Email (MD)**: `md@hariventures.com`
- **Test Email (CEO)**: `ceo@hariventures.com`
- **Password**: `Password@123`
- **MFA Flow**: Requires Google Authenticator MFA setup upon first login attempt.

---

## Code Patterns & Best Practices

1. **Analytics & AI Copilot**: The MD Portal contains the Analytics Copilot chat panel, which leverages backend `ai-service` to run Gemini pipeline generation. Make sure to preserve layout context state and handle RAG response loading states.
2. **Charts & Graphs**: Utilizes charting libraries (e.g. Recharts or Chart.js) to display data from the read-optimized `analytics-service`. Keep UI components clean and responsive for executive viewing.
