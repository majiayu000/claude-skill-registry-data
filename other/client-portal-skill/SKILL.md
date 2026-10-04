---
name: client-portal-skill
description: Use this skill when developing, testing, debugging, or modifying code inside the Client Portal frontend (apps/client-portal). It applies to handling client workflows such as ticketing (support/bug reports), billing/invoicing view, milestone progress tracking, document storage, meetings/calendar, and approvals.
---

# Client Portal Development Skill

Use this skill when modifying, running, or analyzing the **Client Portal** frontend application.

## Overview

- **Location**: [apps/client-portal/](file:///c:/projects/git/product/production/apps/client-portal)
- **Local Port**: `3009` (runs on `http://localhost:3009`)
- **Key Target Role**: `Role.CLIENT`
- **Authentication Entrypoint**: `http://localhost:3001/auth/client/login` (Note: separate from internal auth)
- **Related Backend Services**:
  - `client-service` (Port `8089`, API path `/api/v1/client-portal/**`, `/api/v1/tickets/**`, `/api/v1/client/**`)
  - `notification-service` (Port `8090`, API path `/api/v1/notifications/**`)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/client-portal/src/app/dashboard/layout.tsx) - Configures page framing, sidebar, notification hub connections.
- **Sub-routes (`src/app/dashboard/`)**:
  - `activity`: Feed showing recent updates, notifications, and events.
  - `approvals`: Form submissions, change requests, or contract approvals.
  - `assistant`: Client AI assistant interface.
  - `billing`: Invoice history, payment statuses, and PDF generation links.
  - `calendar`: Upcoming meetings and project milestone dates.
  - `documents`: Document repository shared with the client.
  - `infrastructure`: Client resource configurations or hosting details.
  - `meetings`: Virtual meeting link creation and schedules.
  - `milestones`: Read-only gantt/timeline charts of project milestones.
  - `project`: Overview of active project details, scope, and status.
  - `tickets`: Jira-like ticket creation and messaging threads for customer support.

---

## Development Workflow

### How to Run Locally

To spin up the Client Portal, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\client-portal\clientrun.bat
```

### Credentials for Testing
- **Test Email**: `client@hariventures.com`
- **Password**: `Password@123`

---

## Code Patterns & Best Practices

1. **Security & Isolation**: The Client Portal is external-facing. Ensure all data retrieval is scoped strictly to the client's tenant/clientId.
2. **Next.js conventions**: Uses Next.js App Router.
3. **Invoicing**: Leverages the legacy backend `client-service` to serve PDF files.
