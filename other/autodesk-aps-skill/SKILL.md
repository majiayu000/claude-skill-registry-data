---
name: autodesk-aps-skill
description: >-
  Autodesk Platform Services (APS/Forge) REST APIs — OAuth, Data Management,
  Model Derivative, Viewer, Design Automation, Webhooks; Revit, Fusion 360,
  AutoCAD add-in development.
license: Apache-2.0
compatibility: opencode
category: CAD & Hardware Design
---

# Autodesk Platform Services (APS) Integration

Provenance: extracted from autodesk-specialist-subagent. Domain knowledge for APS, Revit, Fusion 360, and AutoCAD API integration.

## API surface (one line each)

- **Data Management** — BIM 360 / ACC / A360 data access (buckets, objects, hubs/projects/folders tree)
- **Model Derivative** — translate 70+ CAD formats to SVF/SVF2 for viewing
- **Viewer** — embed 3D/2D viewers (Viewer client SDK)
- **Design Automation** — run Revit/AutoCAD/Inventor workloads in the cloud (Activity+AppBundle+WorkItem model)
- **Webhooks** — event-driven automation · **Reality Capture** — photos → 3D

Docs: aps.autodesk.com (developer portal + per-API guides), tutorials at aps.autodesk.com/tutorials, samples at github.com/Autodesk-Forge.

## Authentication

- **2-legged** (client credentials, server-to-server): POST `developer.api.autodesk.com/authentication/v2/token` with `application/x-www-form-urlencoded` `grant_type=client_credentials` + scopes (`data:read data:write bucket:create bucket:read`).
- **3-legged** (user context, authorization code): authorize URL `…/authentication/v2/authorize` with `response_type=code`, then token exchange; scopes like `data:read data:write user-profile:read`. Public webview-friendly endpoints use `-public` client variants.

## MCP servers (house wiring)

No Autodesk MCP pack ships with this repo (**official-only policy** — the former `mcp.autodesk.com` endpoints do not resolve). Use the Autodesk Platform Services REST APIs directly via this skill: OAuth, Data Management, Model Derivative, Viewer, Design Automation, Webhooks. If an official Autodesk MCP server becomes available and its connection details are verified from Autodesk's own documentation, install it per those docs.

## Desktop add-ins (Revit / Fusion 360 / AutoCAD)

Revit: .NET add-ins via `IExternalCommand`/`IExternalApplication`, Revit API in the add-in context, transaction scope required for model changes. Fusion 360: Python/C++ API scripts and add-ins. AutoCAD: .NET `ObjectARX`-managed API or LISP. House rule: prefer APS cloud APIs over desktop automation unless the workflow needs the desktop app alive.

> Removed 2026-09: per-API code walkthroughs (Data Management/Model Derivative/Viewer/Design Automation/Webhooks examples), full config.json listings, webhook event catalogs, desktop add-in tutorials — vendor docs the model can fetch; kept the API map, auth endpoints, MCP wiring, and the cloud-over-desktop preference.
