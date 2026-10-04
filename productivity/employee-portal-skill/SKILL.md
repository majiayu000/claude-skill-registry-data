---
name: employee-portal-skill
description: Use this skill when developing, testing, debugging, or modifying code inside the Employee Portal frontend (apps/employee-portal). It applies to handling employee workflows such as leave tracking, tasks logging, QA/bug reporting, agile planning, development environments, settings, and team communication.
---

# Employee Portal Development Skill

Use this skill when modifying, running, or analyzing the **Employee Portal** frontend application.

## Overview

- **Location**: [apps/employee-portal/](file:///c:/projects/git/product/production/apps/employee-portal)
- **Local Port**: `3005` (runs on `http://localhost:3005`)
- **Key Target Role**: `Role.EMPLOYEE`
- **Authentication Entrypoint**: `http://localhost:3001/auth/internal/login` (MFA/TOTP required)
- **Related Backend Services**:
  - `employee-service` (Port `8088`, `/api/v1/employee/**`)
  - `hr-service` (Port `8086`, `/api/v1/hr/**`)
  - `notification-service` (Port `8090`, `/api/v1/notifications/**`)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/employee-portal/src/app/(portal)/layout.tsx) - Configures page framing, sidebar, notification hub connections.
- **Sub-routes (`src/app/(portal)/`)**:
  - `agile`: Agile/sprint planning boards, backlog.
  - `ai`: HR chatbot and assistant interfaces.
  - `communication`: In-app team communication tools.
  - `deployment`: Environment deployment and version monitoring.
  - `development`: Pull request workflows and review tools.
  - `hr`: Employee leaves, attendance logs, benefits.
  - `productivity`: Personal notes, timers, focus tools.
  - `projects`: Project overview boards.
  - `qa`: Bug reporting interfaces.
  - `tasks`: Detailed tasks check-in log and time entries.
  - `workspace`: Personal developer/employee dashboard.

---

## Development Workflow

### How to Run Locally

To spin up the Employee Portal, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\employee-portal\employeerun.bat
```

### Credentials for Testing
- **Test Email**: `employee@hariventures.com`
- **Password**: `Password@123`
- **MFA Flow**: Initial login prompts for Google Authenticator setup using a TOTP QR code.

---

## Code Patterns & Best Practices

1. **Routing Conventions**: Next.js App Router. Make sure to adhere to structural rules defined in standard Next.js guides.
2. **State & Shared Hooks**: Leverage `@hariventure/types` and shared layout components.
3. **MFA and Authentication**: Ensure JWT tokens are correctly passed in API requests via headers.
