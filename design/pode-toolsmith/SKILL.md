---
name: pode-toolsmith
description: Design, implement, and validate production-grade PowerShell tools using Pode, Pode.Web, and Podex (htmx+Mustache+Tailwind), including security, caching, OpenAPI, and testable structure.
metadata:
  short-description: Build advanced Pode-based tools end-to-end.
  maturity: production
  owner: you
  tags:
    - powershell
    - pode
    - pode-web
    - htmx
    - podex
    - openapi
    - security
---

# Pode Toolsmith Skill

## Purpose

Use this skill to build or enhance **production-grade Pode tools** across three stacks:

- **Pode** for APIs/services, background tasks, OpenAPI, SSE/WebSockets.
- **Pode.Web** for PowerShell-defined dashboards and UI components.
- **Podex** for hypermedia-first apps (htmx + Mustache + Tailwind).

Deliver **runnable, minimal-surprise** output: plan, file structure, code artifacts, and validation steps.

## Explicit invocation

Run `$pode-toolsmith`.

## Trigger phrases (examples)

- “Build a Pode API that exposes X.”
- “Create a PowerShell dashboard for Y.”
- “Modern htmx app on Pode with minimal JS.”
- “Add auth, caching, and OpenAPI to my Pode service.”

## Inputs to gather or infer

Collect from the prompt when available; otherwise infer defaults and proceed.

1. **Tool type**: API/service, dashboard/UI, hypermedia app, or hybrid.
2. **Hosting target**: local dev, Windows service, container, IIS/Azure Functions, LAN tool.
3. **Auth model**: none, Basic over HTTPS, AD/LDAP, session auth, allowlisting.
4. **Data source**: AD, SQL, REST, filesystem, RVTools, Veeam, etc.
5. **Non-functional needs**: caching TTLs, concurrency, response time, audit logs, retention.
6. **Compliance**: logging/PII rules, network boundaries, TLS requirements.

## Decision matrix (pick the default stack)

1. **Choose Pode** when:
   - API-first, integrations, automation endpoints, OpenAPI docs, background tasks, SSE/WebSockets.
2. **Choose Pode.Web** when:
   - UI should be built in PowerShell without HTML/CSS/JS, needs tables/forms/charts/themes.
3. **Choose Podex** when:
   - Modern web app feel with minimal JS using **htmx** partial updates + Mustache templates,
     with a small Node/Tailwind toolchain acceptable.

If multiple stacks fit, pick one default and provide a short “If you prefer X instead…” alternative.

## Operating procedure (no open ends)

### Step 1 — Clarify by inference (do not stall)

Infer missing details; proceed with safe defaults. Ask questions only if a missing detail blocks
correctness or security (example: auth model for exposed endpoints).

### Step 2 — Inspect the workspace

- Read `AGENTS.md` (if present) and project conventions.
- Scan existing server/app files, routes, modules, and assets.
- Detect whether Pode / Pode.Web / Podex already exists.

### Step 3 — Validate environment (fast gate)

Run or instruct:

- `scripts/Test-PodeToolingEnvironment.ps1 -Stack <Pode|PodeWeb|Podex>`

If prerequisites are missing, provide exact install commands and proceed with the best viable subset.

### Step 4 — Design (make choices explicit)

Produce a high-level architecture that includes:

- Endpoints/routes
- Auth + middleware order (CORS/headers, auth, rate limiting, CSRF, sessions)
- Data flow (services layer + IO boundaries)
- UI strategy (Pode.Web components or htmx fragments)
- Caching strategy + invalidation
- Logging + correlation IDs
- Error model and HTTP status mapping
- Test strategy (smoke + Pester)

### Step 5 — Implement in slices with gates

For each slice:

- Ensure scripts parse (`Parser::ParseFile`).
- Confirm cmdlets exist (`Get-Command`).
- Add Pester tests or smoke tests.
- For UI: render without blocking (use background jobs/runspaces if needed).

### Step 6 — Deliverables (always output)

- **File tree**
- **Run instructions**
- **Security notes**
- **Validation commands** (Pester, linting, smoke calls)
- **Next 3 improvements** likely to be valuable

## Expected output bundle

Provide these artifacts in the final response:

1. **Plan** (short, ordered steps)
2. **Scaffold changes** (added/updated files)
3. **Implementation snippets** (key routes/services)
4. **Validation commands** (Pester + smoke)
5. **Operational notes** (logging, caching, rate limiting)

## Reference guides included

- `references/Codex-Skills-Notes.md`
- `references/Pode-Patterns.md`
- `references/PodeWeb-Patterns.md`
- `references/Podex-Patterns.md`
- `references/Security-Checklist.md`
- `references/Testing-Guide.md`
- `references/Operations-Checklist.md`

## Templates included

- `assets/templates/PodeApiServer.ps1.mustache`
- `assets/templates/PodeWebApp.ps1.mustache`
- `assets/templates/PodexRoute.ps1.mustache`
- `assets/templates/appsettings.example.json`
- `assets/templates/README.template.md`

## Safety and correctness rules

1. **Never invent cmdlets**: verify with `Get-Command`, fall back to documented patterns.
2. **Security-first defaults**:
   - HTTPS for any authentication.
   - Prefer allowlisting + rate limiting for LAN tools.
   - Sessions + CSRF for form flows.
3. **Predictable caching**:
   - Document TTL, keys, and invalidation.
   - Provide a bypass (example: `-NoCache`).
4. **No silent failure**:
   - Log errors with correlation IDs.
   - Return structured error bodies for APIs.
5. **Reproducibility**:
   - Pin module versions in docs.
   - Provide a clean bootstrap step.
6. **Accessibility**:
   - Ensure UI outputs include labels, accessible colors, and focus order.

---

## Quick-start (when invoked)

1. Determine stack (Pode / Pode.Web / Podex).
2. Run `Test-PodeToolingEnvironment -Stack <Stack>`.
3. Scaffold with `New-PodeToolScaffold -Stack <Stack> -Path <...>`.
4. Implement the smallest working feature.
5. Add tests and run `Invoke-PodeToolSelfTest`.
6. Package deliverables and provide run/validation steps.
