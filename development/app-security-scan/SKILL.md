---
name: app-security-scan
description: DAST-first NightVision scan for an app you just built or changed. Use when a user, or a project or org agent-instructions rule, wants a local, private, staging, or internal web app/API security-scanned. Drives the NightVision MCP `run-app-security-scan` harness.
allowed-tools: Bash, Read, Grep, mcp__nightvision__auth-status, mcp__nightvision__preflight-app, mcp__nightvision__run-app-security-scan, mcp__nightvision__wait-for-scan, mcp__nightvision__get-scan-status, mcp__nightvision__summarize-scan-findings, mcp__nightvision__export-sarif
---

# NightVision App Security Scan

Run a real DAST scan against an app you just built or changed. Source Intelligence runs first when the backend language is supported, because it improves coverage and lets findings trace back to a source file and line (Code Traceback). DAST is the expected outcome on every run, not just a generated spec.

Requirements: this skill drives the NightVision MCP server's app-security-scan harness, so it needs a server build that provides `run-app-security-scan`, `preflight-app`, `wait-for-scan`, `summarize-scan-findings`, and `export-sarif` with the `project_path` argument. On an older server these tools are missing (the call returns an unknown-tool error) or `export-sarif` ignores `project_path` and silently drops source-linking. If any of the listed tools is unavailable, update the NightVision MCP server before using this skill; running `preflight-app` first is the cheapest way to confirm the harness is present.

## Best-supported languages and frameworks

Source Intelligence reads source code locally and deterministically to generate an OpenAPI spec for supported codebases. Source-linked results are strongest for the empirically verified languages and frameworks below:

- Python: Django REST Framework, Flask, Flask-RESTful, FastAPI, Starlette, Connexion
- JavaScript/TypeScript: Express, NestJS, Fastify, Hono
- Java: Spring Boot MVC and Data REST, JAX-RS/Jersey, Micronaut, Quarkus, Dropwizard
- C#: ASP.NET Core controllers and Minimal APIs, Web API 2
- Go: `net/http` (Go 1.22+ patterns), Gin, Echo, Fiber v2 and v3, chi, gorilla/mux
- PHP: Laravel
- Ruby: Rails

Django URLconf views, Grape, oRPC and httprouter extract with gaps; see `source-intelligence` for the full list, including frameworks that are not supported.

Treat frameworks outside this list as verify-first for source discovery. Still run DAST against reachable web apps and APIs as a WEB target when discovery is unsupported or produces no spec, but report that findings may not include source `file:line` traceback. Source-based discovery is REST/OpenAPI only.

## Workflow

1. Locate the app's source directory and pass it as `project_path`. Do not rely on the current working directory: a developer usually launches you from their home directory, not the repo, and Source Intelligence reads `project_path` to generate the spec that links findings to source. If you are not already in the repo, find it (the app's git root / where its source lives) and pass that absolute path. Running against the home directory is refused with `project_path_not_app_source`.
2. Know the app's URL. You are running on the developer's machine with the app's source in front of you, so you know how it serves. If it is not already running, start it with its own command (`npm run dev`, `docker compose up`, the framework dev server). Pass that URL as `target_url`. Do not ask the harness to guess it.
3. Call `run-app-security-scan` with `project_path`, `target_url`, the NightVision project, and the app-auth mode (see Auth). One call does preflight, Source Intelligence, target create/update, DAST start, and writes `.nightvision/manifest.json`. Always route the scan through this one harness call, even when the user already has a NightVision target or credential set up: pass their existing project and `auth`/`auth_id`, and the harness reuses and updates that target and refreshes Source Intelligence so its spec is not stale. Do not hand-assemble a scan from `create-target` / `start-scan` / `list-targets`; that path skips the fresh discovery and is how a scan silently exercises a stale spec. The one exception is the `verify-fix` skill's narrowed retest of a single finding, which reuses the target and spec this harness just refreshed.
4. Report the discovery result before you poll, so the user can see Source Intelligence ran and what it produced. The single harness call runs Source Intelligence, updates the target, and starts DAST in that order, but all of it is invisible from the outside: the user sees one tool call and then a long scan, which reads as "it skipped discovery and went straight to DAST". Do not let a 10+ minute scan be the first thing the user hears about. Read these fields off the result and state them in one or two sentences before the first poll:
   - `api_discovery.status` (`success`, `no_spec`, `skipped`, or `failed`) and `api_discovery.attached_spec_file` (the spec that was pushed to the target).
   - The endpoint count in that spec. Count the entries under `paths:` in the spec file (for example `grep -c '^  /' <attached_spec_file>`) and say how many endpoints DAST will exercise.
   - `target.action` (`created`, `updated`, or `reused`) and the resolved target's `type`, nested at `target.target.type` (the `target` block wraps the action and the resolved target object). Any non-`WEB` type means the spec is attached and findings can carry source `file:line` (the backend echoes a spec-attached target as `API` or `OPENAPI`, so do not match on `API` alone); type `WEB` means it is scanning without a spec. Prefer `api_discovery.status` for the coverage judgment; treat the target `type` as confirmation only.
   - The `scan_id`.
   - A target the harness creates is tagged "Agent created" in NightVision, so the dashboard can show which applications an AI coding agent set up.

   Anything other than `api_discovery.status: success` producing a spec-attached (non-`WEB`) target is a coverage problem: say so now, not after the scan burns 15 minutes against a stale or absent spec. This is the same failure the coverage floor in Reporting catches, only caught earlier.
5. It returns a `scan_id` quickly (`wait` defaults to false). DAST commonly runs longer than 10 minutes, so do not assume it finished.
6. Poll `wait-for-scan` or `get-scan-status` until a terminal status.
7. Export SARIF and summarize: call `export-sarif` with the SAME `project_path` you passed to the scan (it resolves the discovered spec from that repo's `.nightvision`, so findings carry endpoint + source file:line; without it the spec is looked up in the shell cwd and source-linking is silently lost) and `summarize-scan-findings`. Report the scan id, target, project, finding counts, and the top findings with endpoint, source file:line, evidence, and a suggested fix. If SARIF comes back `source_linked: false` but discovery produced a spec, you passed the wrong `project_path`. In a multi-language repo with several per-language specs and no canonical `openapi.yml`, `export-sarif` attaches the first spec and returns a warning; if the source-linking is for the wrong language, pass the right spec explicitly with `swagger_file`.
8. The manifest is the local record and stays in the repo. Treat the work as incomplete until `.nightvision/manifest.json` holds a `scan_id`, or you have reported a concrete blocker.

Resolve blockers the harness reports rather than working around them: `not_authenticated` / `invalid_or_expired_token` (auth), `target_url_required` (you did not pass the URL), `runtime_url_not_reachable` (the app is not up, start it), `nightvision_project_required`, `project_path_not_app_source` (you passed the home/root directory; pass the app's source directory). Use `dry_run: true` when the user only wants a readiness check without creating targets or starting a scan.

## Unattended mode

When a project agent-instructions rule triggers this after an app is built (no human watching): start the app yourself, rely on `NIGHTVISION_DEFAULT_PROJECT` and the environment's NightVision token (never prompt for them; a missing one is a blocker to report), and close the loop before ending your turn. Do not leave a scan running with nobody watching: poll to a terminal status, then export SARIF and summarize. If you cannot start the app or auth is missing, report that as the concrete blocker instead of silently skipping the scan.

## Auth

Two different things. NightVision account auth is the user's own NightVision token; never paste a shared token into your agent-instructions file (CLAUDE.md, AGENTS.md), a repo file, or a team config, each user authenticates as themselves. Target-app auth is how DAST logs into the app under test, passed to the scan as:

- `no_auth: true` to scan unauthenticated (say so; it may miss authenticated functionality).
- `auth` (named profile) or `auth_id` (credential UUID) for an existing NightVision app-auth credential.
- `app_auth` with `type: "playwright_script"` for any username/password, OAuth, MFA, or expiring-session login. Do not turn an expiring cookie or bearer token into a header/cookie credential.
- `app_auth` with `type: "headers"` or `"cookies"` only for stable, non-expiring credentials such as a service API key; set `credential_lifetime: "stable"`.

## Reporting

A terminal `FAILED` scan can still contain valid findings: check the finding count and summarize what it found before calling a run unusable. When the user wants something to share (a PDF, a report for a manager, CISO, or another team), hand off to the `scan-report` skill with the same `scan_id` and `project_path`. Never claim the app is secure or scanned unless NightVision results support it. If DAST could not run, report the blocker and the manifest path.

Coverage floor: a scan that "succeeded" but exercised no endpoints is a setup failure, not a clean bill of health. If a full scan returns zero findings, or only the "target is online" informational check, or the harness sets `coverage_suspect: true` on the scan result, treat it as suspect: the spec was stale, Source Intelligence did not run against current source, or the target was scanned as a bare WEB target. Do not report the app as secure. Re-run `run-app-security-scan` with `project_path` set to the app's source directory so discovery regenerates the spec, confirm the scan tested real endpoints, and only then report. A known-featureful app returning nothing is the tell.

## Remediation (find-to-fix)

When the user wants findings fixed and not just reported, use what each finding actually carries. It varies by class, so do not assume every finding gives you a source line or a parameter:

- Request-level findings (SQL injection, XSS, command injection, and similar) carry a source `file:line`, the endpoint, the vulnerable parameter, and the proof-of-concept payload. The `file:line` is the DAST-observable entry point (the endpoint handler), not always the sink: open it, follow the named parameter into the service or repository that uses it, find the sink, and apply the standard fix for the class (a parameterized query for SQL injection, output encoding for reflected XSS), matching the codebase's existing patterns.
- Response/config-level findings (missing security headers, weak authentication method, error or stack-trace disclosure) either have no source location, or the line they carry points at whatever handler the response was observed through, which is not where the fix goes. Fix these in the app's security configuration (the header/filter/security config), not at the reported line.

NightVision does not hand you a patch (`fixes`/`codeFlows` in the SARIF are empty), and not every finding maps to source, so treat this as a locate-and-fix aid. Always re-scan and confirm the finding is gone before calling it fixed: the `verify-fix` skill reruns just the check that found it, or use `run-app-security-scan` when the fix changed routes, parameters or auth. Remediation is a follow-on to the scan, not a replacement: scan first, and only change code when the user asks for fixes (running `ship-check` counts as asking, for code written in the same session).
