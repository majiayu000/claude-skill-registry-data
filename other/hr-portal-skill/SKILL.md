---
name: hr-portal-skill
description: Use this skill when developing, testing, debugging, or modifying code inside the HR Portal frontend (apps/hr-portal). It applies to handling HR administration tasks such as employee roster management, contract seeding, leave request approvals, attendance monitoring, payroll calculation, and recruitment pipelines.
---

# HR Portal Development Skill

Use this skill when modifying, running, or analyzing the **HR Portal** frontend application.

## Overview

- **Location**: [apps/hr-portal/](file:///c:/projects/git/product/production/apps/hr-portal)
- **Local Port**: `3003` (runs on `http://localhost:3003`)
- **Key Target Role**: `Role.HR`
- **Authentication Entrypoint**: `http://localhost:3001/auth/internal/login` (MFA/TOTP required)
- **Related Backend Services**:
  - `hr-service` (Port `8086`, API path `/api/v1/hr/**`)
  - `user-service` (Port `8082`, API path `/api/v1/users/**`)
  - `notification-service` (Port `8090`, API path `/api/v1/notifications/**`)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/hr-portal/src/app/dashboard/layout.tsx) - Configures page layout, sidebar navigation, and notification streams.
- **Sub-routes (`src/app/dashboard/`)**:
  - `attendance`: Daily check-in registers, timesheet corrections, and shift planning.
  - `employees`: Roster listing, contract updates, user creation and department role assignment.
  - `leaves`: Dashboard for tracking company-wide leave balances, pending leave requests, and approval histories.
  - `payroll`: Processing payslips, salary tier settings, tax calculations.
  - `recruitment`: Hiring pipelines, open job requisitions, candidate profile trackers.

---

## Development Workflow

### How to Run Locally

To spin up the HR Portal, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\hr-portal\hrrun.bat
```

### Credentials for Testing
- **Test Email**: `hr@hariventures.com`
- **Password**: `Password@123`
- **MFA Flow**: Requires Google Authenticator MFA setup upon first login attempt.

---

## Code Patterns & Best Practices

1. **Roster Modification**: HR portal acts as the creator of new employee entries, publishing Kafka events (`EMPLOYEE_ONBOARDED`) in the backend. When editing employee profiles, ensure correct field updates align with `@hariventure/types`.
2. **Access Control**: Confirm client components utilize appropriate session validation for `Role.HR`.
