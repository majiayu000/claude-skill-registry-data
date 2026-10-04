---
name: teamlead-portal-skill
description: Use this skill when developing, testing, debugging, or modifying code inside the Team Lead Portal frontend (apps/teamlead-portal). It applies to operational/task management, middle management team oversight, task assignment lists, sprint boards, and team member leave approval workflows.
---

# Team Lead Portal Development Skill

Use this skill when modifying, running, or analyzing the **Team Lead Portal** frontend application.

## Overview

- **Location**: [apps/teamlead-portal/](file:///c:/projects/git/product/production/apps/teamlead-portal)
- **Local Port**: `3007` (runs on `http://localhost:3007`)
- **Key Target Role**: `Role.TEAM_LEAD`
- **Authentication Entrypoint**: `http://localhost:3001/auth/internal/login` (MFA/TOTP required)
- **Related Backend Services**:
  - `employee-service` (Port `8088`, API path `/api/v1/employee/**` - used for task logging/check-ins)
  - `hr-service` (Port `8086`, API path `/api/v1/hr/**` - used for leave management)
  - `notification-service` (Port `8090`, API path `/api/v1/notifications/**`)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/teamlead-portal/src/app/dashboard/layout.tsx) - Configures page routing, dashboard sidebar, and notifications for Middle Management roles.
- **Sub-routes (`src/app/dashboard/`)**:
  - `leaves`: Dashboard to review and approve/reject leave requests submitted by reporting employees.
  - `tasks`: Task board tracking task assignments, statuses (Backlog, Todo, In Progress, Done), and milestones.
  - `team`: Roster view showing check-in logs, task capacity, and active status of all reporting team members.

---

## Development Workflow

### How to Run Locally

To spin up the Team Lead Portal, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\teamlead-portal\teamleadrun.bat
```

### Credentials for Testing
- **Test Email**: `lead@hariventures.com`
- **Password**: `Password@123`
- **MFA Flow**: Requires Google Authenticator MFA setup upon first login attempt.

---

## Code Patterns & Best Practices

1. **Role hierarchy**: Team Lead acts as an intermediate approval role. Endpoints query reporting employees rather than platform-wide lists. Ensure queries match appropriate path prefixes.
2. **Component Reuse**: Verify task card widgets use components from the shared design system `@hariventure/ui` when editing board interfaces.
