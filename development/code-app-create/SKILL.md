---
name: code-app-create
description: >
  Create, scaffold, and initialize a new Power Apps code app from scratch. Guides through
  prerequisites, template selection, CLI initialization, local development, and first deployment.
  Use this skill whenever the user wants to create a new code app, scaffold a Power Apps project,
  start a code-first Power Apps application, or asks "how to create a code app", "init a new
  Power Apps project", "scaffold a code app", "npx power-apps init", "pac code init", or any
  variation involving starting a new Power Apps code app from zero. Also triggers when the user
  asks about Power Apps code app architecture, SDK layers, or prerequisites for code apps.
---

# Power Apps Code App — Create & Scaffold

Guide developers through creating a new Power Apps code app from zero to first deployment.
For complete command reference, architecture details, and configuration options, see
[references/setup-and-architecture.md](references/setup-and-architecture.md).

## Workflow

### Step 1 — Verify Prerequisites

Before anything else, confirm the developer has:
- **Node.js** (LTS version)
- **Git** installed
- **VS Code** (recommended IDE)
- **Power Apps Premium license** (required for end users)
- **Code apps feature enabled** in Power Platform Admin Center

The feature must be enabled at the environment level by an admin:
Power Platform Admin Center > Environments > [env] > Settings > Product > Features > "Code apps"

### Step 2 — Choose the CLI Approach

There are two CLI paths. The **npm CLI** (current, recommended) requires fewer prerequisites:

| Approach | Tool | Status | Key Commands |
|----------|------|--------|-------------|
| **npm CLI** | `@microsoft/power-apps` (v1.0.4+) | Current | `npx power-apps init`, `npx power-apps push` |
| PAC CLI | Power Platform CLI | Legacy | `pac code init`, `pac code push` |

Default to the npm CLI path unless the user explicitly needs PAC CLI.

### Step 3 — Scaffold the Project

```bash
# Clone the Vite template (same for both approaches)
npx degit github:microsoft/PowerAppsCodeApps/templates/vite my-app
cd my-app
npm install
```

The template provides a Vite-based SPA structure with TypeScript and the Power Apps SDK pre-configured.

### Step 4 — Initialize with Power Platform

**npm CLI (recommended):**
```bash
# Interactive mode (prompts for display name and environment)
npx power-apps init

# Direct mode (non-interactive)
npx power-apps init --displayName "My App" --environmentId <environment-id>
```

**PAC CLI (legacy):**
```bash
pac auth create                              # Authenticate with Entra ID
pac env select --environment <environment-id> # Select target environment
pac code init --displayname "My App"          # Initialize the app
```

This step authenticates with Microsoft Entra ID and binds the project to a specific Power Platform environment. It auto-generates `power.config.json` — never edit this file manually.

### Step 5 — Local Development

```bash
npm run dev
```

Open the "Local Play" URL in a browser that is signed into the **same Power Platform tenant**. The browser will request local network access permission (required since Dec 2025).

### Step 6 — Build & Deploy

**npm CLI:**
```bash
npm run build
npx power-apps push
```

**PAC CLI:**
```bash
npm run build | pac code push
```

After push, the CLI returns the app URL. Share it via the Power Apps portal, optionally adding `?hideNavBar=true` to hide the Power Apps header.

## Architecture at a Glance

Code apps have 3 layers at development time and 3 at runtime:

**Development:** `power.config.json` (auto-generated metadata) → Power Apps SDK (APIs + generated models/services) → CLI (build + publish)

**Runtime:** Your Code → Power Apps SDK (runtime APIs) → Power Apps Host (auth, app loading, error presentation)

When connectors are added or removed, the SDK automatically regenerates model and service files in `/generated/`. The developer works with typed TypeScript interfaces.

## Security Model

- Hosted code is **publicly accessible** — never store secrets, API keys, or sensitive data in app code
- Use data sources with proper auth/authz for sensitive operations
- Authentication is managed by the Power Apps host via Microsoft Entra ID
- Data Loss Prevention and Conditional Access policies are enforced at launch

## Key Limitations

Code apps currently do **not** support:
- Mobile or Power Apps for Windows
- Power BI data integration
- SharePoint forms
- Storage SAS IP restrictions
- Power Platform Git integration (no source control via platform)
- Solution Packager tool

## What NOT to Do

- Do not manually edit `power.config.json`
- Do not store credentials or API keys in app source code
- Do not use `pac code` commands when the npm CLI is available (unless explicitly needed)
- Do not skip the environment feature enablement step
