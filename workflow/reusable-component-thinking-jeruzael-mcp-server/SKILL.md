---
name: reusable-component-thinking
description: Identify repeated patterns in Exorex projects and turn them into reusable, documented, versioned assets. Use when Codex needs to extract reusable modules, templates, workflows, automations, UI patterns, backend modules, database templates, documentation templates, sales assets, deployment checklists, or service-package foundations from client work instead of rebuilding from scratch.
---

# Reusable Component Thinking

Use this skill to convert repeated work into reusable business and technical assets.

## Core Principle

If the same thing is built twice, turn it into a reusable component before building it a third time.

Reusable does not mean vague or over-generic. A good component solves a clear repeated problem, separates reusable core logic from client-specific details, and is easy to customize.

## Component Candidates

Look for repeated needs such as:

- login, registration, roles, profiles, dashboards
- booking/request forms, approvals, status tracking, notifications
- payments, reports, file uploads, customer records
- lead capture, auto-replies, reminders, document generation
- proposals, quotations, scopes, handovers, deployment checklists
- reusable UI layouts, API patterns, database structures, and automation flows

Read `references/component-library.md` for category lists, component-card format, folder structure, and starter library recommendations.

## Workflow

1. Identify repetition:
   - Have we built this before?
   - Will we likely build it again?
   - Do multiple clients need it?
   - Is this a common business process?
2. Extract the core pattern:
   - Remove client name, branding, custom pricing, one-off rules, and hardcoded assumptions.
   - Keep the reusable workflow, data model, interface, or document structure.
3. Define customization points:
   - labels, fields, rules, roles, copy, integrations, pricing, branding, notifications, and reporting.
4. Build or package the component:
   - code module, UI template, backend module, database template, automation flow, prompt, document, checklist, or deployment template.
5. Document it with a component card.
6. Test it in a sample or real project before promoting it to the official library.
7. Version it and improve it after every use.

## Review Rules

Before calling something reusable:

- Confirm the component has a clear purpose and best-use case.
- Confirm client-specific data is not embedded in the core component.
- Confirm dependencies and limitations are documented.
- Confirm it has at least one practical customization example.
- Confirm it has a version.
- Confirm it is tested enough for its reuse risk.
- Do not reuse weak code, unclear workflows, or bad processes just because they exist.

## Naming Convention

Use:

`[Category]_[ComponentName]_v[Version]`

Examples:

- `App_BookingRequestModule_v1.0`
- `Backend_AuthenticationModule_v1.0`
- `Automation_LeadCaptureToGoogleSheets_v1.0`
- `Docs_ClientDiscoveryTemplate_v1.0`
- `Deployment_DockerComposeFastAPI_v1.0`

## Output Contract

When using this skill, provide:

1. Repeated pattern identified.
2. Proposed reusable component name and category.
3. Component card or starter implementation plan.
4. Customization points and dependencies.
5. Test/validation plan.
6. Recommended library location and version.
