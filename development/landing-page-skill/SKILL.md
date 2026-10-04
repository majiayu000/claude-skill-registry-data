---
name: landing-page-skill
description: Use this skill when developing, testing, debugging, or modifying the public Landing Page and auth hub (apps/landing-page). It applies to the public marketing entrypoint, routing logins for internal and client roles, managing multi-factor authentication (MFA/TOTP) setup forms, and password resets.
---

# Landing Page & Auth Hub Development Skill

Use this skill when modifying, running, or analyzing the **Landing Page** and Authentication application.

## Overview

- **Location**: [apps/landing-page/](file:///c:/projects/git/product/production/apps/landing-page)
- **Local Port**: `3000` (runs on `http://localhost:3000`)
- **Key Target Roles**: Public visitors, plus auth entry point for all roles (Internal and Client)
- **Related Backend Services**:
  - `auth-service` (Port `8081`, API path `/api/v1/auth/**`)
  - `notification-service` (Port `8090`, API path `/api/v1/notifications/**` - handles OTP emails)

---

## Folder Structure & Key Paths

- **Layout File**: [layout.tsx](file:///c:/projects/git/product/production/apps/landing-page/src/app/layout.tsx) - Standard viewport wrappers, styling imports, and base layout.
- **Sub-routes (`src/app/`)**:
  - `auth`: Entrypoint layouts for internal and client logins.
    - `auth/internal/login`: Internal user login page (redirects to MFA setup if not configured).
    - `auth/client/login`: Client login page.
  - `dashboard`: Quick info or platform navigation dashboards.

---

## Development Workflow

### How to Run Locally

To spin up the Landing Page, run the startup script:
```powershell
# Run the bat script which starts docker, Maven JAR dependencies, and the dev server
.\apps\landing-page\landingrun.bat
```

---

## Code Patterns & Best Practices

1. **Authentication Flow Coordination**: The landing page manages the `totp` library for setting up Authenticator app key/QR codes. If modifying the login flow, ensure state transitions handle MFA checks correctly against `auth-service` headers.
2. **SEO & Accessibility**: The landing page is the primary public face of the enterprise platform. Maintain clean semantic elements and metadata properties.
