---
name: stride-spoofing
description: Generate Spoofing threats for a system, repo, architecture, or data flow. Use when Codex needs to identify how users, services, devices, processes, or external systems could pretend to be another trusted identity, bypass identity checks, or exploit weak authentication and trust assumptions.
---

# STRIDE Spoofing

## Overview

Use this skill to generate threat ideas specifically in the Spoofing category of STRIDE. Focus on false identity, impersonation, weak trust establishment, and places where the system may accept an attacker as a trusted user, service, process, device, or dependency.

Prefer concrete threats tied to real components, actors, and trust boundaries over generic statements about authentication.

## Workflow

### 1. Establish the modeling scope

Choose the smallest useful slice first:

- one request path
- one service-to-service interaction
- one login or onboarding flow
- one external integration
- one device or workload identity path

Identify the main actors, systems, and trust boundaries before generating threats.

### 2. Identify identities and trust anchors

Look for:

- users, admins, operators, support staff, and tenants
- services, workloads, scheduled jobs, and agents
- devices, browsers, mobile apps, and endpoints
- third-party systems, webhooks, callbacks, or partner APIs
- API keys, passwords, tokens, cookies, certificates, SSH keys, signed URLs, or shared secrets
- identity assertions carried in headers, claims, session state, network location, or metadata

### 3. Generate Spoofing threats

Generate threats around:

- impersonating a user, tenant, or privileged operator
- impersonating an internal service or trusted dependency
- forging callback, webhook, or partner-system identity
- abusing shared credentials or default credentials
- session theft, token theft, replay, or credential reuse
- trust in weak identifiers such as IP address, hostname, email, or client-supplied IDs
- account-linking or identity-mapping confusion
- insecure bootstrap or enrollment flows

### 4. Stress the trust assumptions

For each important identity boundary, ask:

- What proves this actor is who it claims to be?
- Can that proof be stolen, replayed, guessed, or bypassed?
- Is the system trusting an upstream header, network zone, or internal hostname too much?
- Can one tenant, user, or service impersonate another through identifier confusion?
- Are there fallback or legacy paths with weaker identity checks?

### 5. Deliver concise threats

For each threat, capture:

- threat title
- component or boundary affected
- spoofing scenario
- likely impact
- why the system may be vulnerable
- suggested mitigations or validation questions

## Output Rules

Default to a short list of concrete Spoofing threats. Prefer this shape:

```text
Spoofing Threats
- <title> — <component or boundary>
  Scenario: <how spoofing happens>
  Impact: <what the attacker gains or bypasses>
  Mitigations / questions: <specific controls or follow-up>
```

Do not drift into Tampering or Elevation of Privilege unless spoofing is the first enabling step.

## Example Requests

- Generate Spoofing threats for this architecture.
- Review this repo and identify STRIDE Spoofing threats in the auth flows.
- Use this data flow diagram to find places where one service could impersonate another.
