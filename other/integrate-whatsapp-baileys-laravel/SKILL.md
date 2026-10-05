---
name: integrate-whatsapp-baileys-laravel
description: Integrate WhatsApp through a secure Baileys sidecar with Laravel, including tests and reusable local Windows and Linux VPS setup documentation.
tags:
  - laravel
  - php
---

# Integrate WhatsApp With Baileys And Laravel

Build Baileys as a private Node.js sidecar and keep Laravel as the application, authorization, queue, and user-facing boundary.

## Required references

Read both references before changing the target project:

- [architecture-and-implementation.md](references/architecture-and-implementation.md) for package selection, service boundaries, security, reliability, and tests.
- [deployment-and-documentation.md](references/deployment-and-documentation.md) for Windows, VPS, process management, verification, and the required documentation artifact.

## Workflow

### 1. Inspect before designing

1. Read the target repository instructions and relevant existing documentation.
2. Detect the Laravel and PHP versions, Node package manager and lockfile, Node runtime policy, test framework, queue driver, process manager, deployment layout, and quality tools.
3. Search for existing WhatsApp clients, notification contracts, jobs, admin routes, configuration keys, Baileys services, and documentation. Extend a sound boundary instead of creating a competing integration.
4. Record assumptions. Default an unspecified VPS to Ubuntu/Debian, but label that assumption in the generated documentation.
5. Consult current official Baileys documentation and package metadata before choosing a package or API. Baileys changes frequently; do not rely on remembered package names, versions, exports, or migration behavior.

### 2. Agree on the smallest feature surface

Derive scope from the request. A normal outbound integration needs:

- one private Baileys session;
- connection status and QR or pairing-code lifecycle;
- connect and disconnect operations;
- text-message sending;
- Laravel configuration and a focused integration client;
- authorized admin controls only when the project needs them;
- queued delivery for business workflows when latency or retry behavior warrants it.

Do not add inbound message handling, media, groups, bulk messaging, chat storage, multi-session tenancy, webhooks, or a new admin UI unless requested or already required by project behavior.

### 3. Design before editing

Use this default boundary:

```text
authorized browser or application workflow
                -> Laravel
                -> private authenticated HTTP API
                -> Node.js Baileys sidecar
                -> WhatsApp Web socket
```

Keep the sidecar on the same host or a private network. Bind to loopback by default. Never point a public reverse proxy directly at it.

Before implementation, define:

- the sidecar directory and runtime;
- the package/version strategy and lockfile;
- the internal versioned endpoint contract;
- authentication and secret ownership;
- development and production auth-state storage;
- connection states and reconnect rules;
- sync versus queued send behavior;
- duplicate-delivery and retry policy;
- the exact test and smoke-check plan.

### 4. Implement the sidecar

Create or adapt a focused service such as `services/baileys/`. Keep socket state and HTTP transport separated when that materially improves testing; do not create ceremonial layers.

Require the sidecar to provide:

- explicit environment validation and a safe `.env.example`;
- loopback binding by default;
- authenticated, versioned endpoints for status, session operations, and sending;
- bounded JSON bodies and validated phone/message input;
- one connection attempt at a time and one active socket per session;
- credential persistence on every auth update;
- explicit handling for restart-required, logged-out, replaced, transient, and fatal disconnects;
- bounded reconnect backoff with jitter and no reconnect after deliberate logout;
- redacted structured logs, graceful shutdown, and useful exit codes;
- no secrets, QR values, auth state, or full message bodies in logs.

Treat file-based multi-file auth as development/demo storage. Follow the production decision rules in the architecture reference.

### 5. Implement the Laravel boundary

Use Laravel-native configuration and HTTP APIs:

- put environment reads in config files and add placeholders to `.env.example`;
- keep provider request mapping, authentication, timeouts, response parsing, and error translation in a focused client/service;
- add an interface only when multiple drivers or a meaningful domain boundary justify one;
- keep controllers limited to authorization, validated input, orchestration, and responses;
- authorize every admin/session action and retain CSRF protection for browser routes;
- use safe structured logs without tokens, QR data, message content, or unnecessary phone numbers;
- separate connection timeout from total request timeout;
- retry safe status reads only; never blindly retry message sends;
- queue business notifications when appropriate and make retry semantics explicit.

Preserve existing project conventions for routes, responses, translations, admin UI, and tests.

### 6. Verify behavior

Run the smallest meaningful set supported by the project:

1. Node syntax/type, lint, and unit/integration tests.
2. Laravel tests using `Http::fake()` for success, validation failure, unauthorized access, sidecar unavailability, and provider rejection.
3. Queue dispatch and job behavior tests when queued delivery exists.
4. Formatter/static analysis and affected frontend checks.
5. A local smoke check for health/status, connect, QR or pairing code, reconnect, send, disconnect, and restart persistence.

Do not claim an end-to-end WhatsApp send was verified unless a real test account was paired and the result was observed. Report skipped checks and why.

### 7. Write the mandatory project documentation

After implementation and verification, create or update `docs/BAILEYS_SETUP.md` in the target Laravel project. If the project already has a canonical WhatsApp setup document, update that file instead and report the chosen path.

The document must be project-specific, safe to commit, and contain complete local Windows and Linux VPS instructions. Use the required outline and completion rules in the deployment reference. Never place real tokens, session data, phone numbers, domains, usernames, or private paths in it.

### 8. Handoff

Report:

- architecture and scope implemented;
- files changed;
- chosen Baileys package and pinned version;
- development and production auth-state choices;
- tests and smoke checks run;
- documentation path;
- operational or compliance risks that remain.

State clearly that Baileys is unofficial and is not affiliated with Meta or WhatsApp. Do not imply guaranteed delivery, protocol stability, or freedom from account restrictions.
