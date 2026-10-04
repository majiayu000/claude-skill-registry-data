---
name: super-admin-portal-skill
description: Use this skill when developing, testing, debugging, or modifying code inside the Super Admin Portal frontend (apps/super-admin-portal). It applies to SaaS platform-level configurations, multi-tenant provisioning, system metrics, audit logs, and global user management.
---

# Super Admin Portal Development Skill

Use this skill when modifying, running, or analyzing the **Super Admin Portal** frontend application.

## Overview

- **Location**: [apps/super-admin-portal/](file:///c:/projects/git/product/production/apps/super-admin-portal)
- **Local Port**: `3000` (runs on `http://localhost:3000` alongside landing page)
- **Key Target Role**: `Role.SUPER_ADMIN`
- **Authentication Entrypoint**: `http://localhost:3001/auth/internal/login` (Platform-wide controls)
- **Related Backend Services**:
  - `tenant-service` (Port `8083`, API path `/api/v1/tenants/**`)
  - `user-service` (Port `8082`, API path `/api/v1/users/**`)
  - `analytics-service` (Port `8091`, API path `/api/v1/analytics/**`)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/super-admin-portal/src/app/dashboard/layout.tsx) - Configures the system-wide control panel framing and analytics connections.
- **Sub-routes (`src/app/dashboard/`)**:
  - `tenants`: Interface for tenant listing, SaaS subscription states, new tenant provisioning, and sandbox isolations.

---

## Development Workflow

### How to Run Locally

To spin up the Super Admin Portal, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\super-admin-portal\superadminrun.bat
```

### Credentials for Testing
- **Test Email**: `superadmin@hariventures.com`
- **Password**: `Password@123`
- **MFA Flow**: Requires Google Authenticator MFA setup upon first login attempt.

---

## Code Patterns & Best Practices

1. **Multi-Tenant SaaS Operations**: Super admin commands have the highest privilege. Ensure that tenant provisioning updates publish correct events via `tenant-service` to configure Mongo databases dynamically.
2. **Access Control Warning**: Changes here must verify that only users with `Role.SUPER_ADMIN` are permitted to view dashboard widgets.
