---
name: kit-attack-surface
description: Map the attack surface of the user's own codebase by inventorying every entry point (HTTP routes, webhooks, CLI arguments, message consumers, file and environment input, scheduled jobs), the authentication and authorization applied to each, and the data an attacker controls, as a red-team reconnaissance step for authorized security testing. Use when the user asks to map the attack surface, list entry points, find unauthenticated endpoints, or prepare a penetration test of their own application. Do not use for scanning or probing hosts or third-party systems, for finding specific vulnerabilities in code (use kit-security-audit), or for designing new features (use kit-threat-model); this skill reads code and does not send network traffic.
---

# Attack surface mapping

This skill works from the source code of the user's own project. It does not scan, probe, or send traffic to any host. If the user asks to scan a system, confirm that it is theirs or in an authorized scope, and leave active testing to them.

## 1. Inventory entry points

- HTTP: every route with its method and path from the router registration, including framework defaults (health checks, metrics, admin panels, debug or docs endpoints such as `/docs`, `/graphql`, `/actuator`).
- Other inputs: webhooks, message queue consumers, WebSocket handlers, CLI arguments and flags, files read from user-controlled paths, uploads, environment variables and configuration that users can set, scheduled jobs that process external data.
- Outbound calls whose URL or target depends on input (SSRF candidates) and interpreters that receive input (SQL, shell, templates, deserializers).

## 2. Record controls for each

- Authentication (which middleware or decorator, or none), authorization (role, ownership, and tenant checks, or none), input validation, rate limiting, and CSRF protection where cookies are used.
- What the caller controls: path and query parameters, body fields, headers, file names and contents.
- Mark entry points that are unauthenticated, that accept identifiers without an ownership check, or that reach an interpreter.

## 3. Prioritize

Rank entry points for testing by exposure (internet-facing, unauthenticated), sensitivity of the data or action, and missing controls. Note third-party and infrastructure surfaces that are out of scope for code review (CDN, cloud consoles) without probing them.

## 4. Report

Give a table of entry points (location `file:line`, input, authentication, authorization, notes), the prioritized list with suggested test cases for the user's authorized testing, and gaps in what could be determined from code.

## Examples

- Use: "Map the attack surface of this API." "Which routes have no auth?" "Prepare a pentest plan for our app."
- Skip: "Scan 203.0.113.10 for open ports." "Find the SQL injection in orders.ts." (kit-security-audit)
