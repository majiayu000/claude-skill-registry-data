---
name: stride-elevation-of-privilege
description: Generate Elevation of Privilege threats for a system, repo, architecture, or data flow. Use when Codex needs to identify how attackers could gain capabilities beyond their intended permissions by abusing authorization gaps, unsafe trust boundaries, privileged execution paths, or identity and state confusion.
---

# STRIDE Elevation Of Privilege

## Overview

Use this skill to generate threat ideas specifically in the Elevation of Privilege category of STRIDE. Focus on how a low-privilege or untrusted actor could gain higher privileges, broader access, or stronger capabilities than intended.

Prefer threats tied to real privilege boundaries, role checks, administrative paths, and execution contexts over generic "broken access control" comments.

## Workflow

### 1. Establish the modeling scope

Choose one concrete slice first:

- one admin or operator workflow
- one role-sensitive API path
- one tenant boundary
- one background job or automation path
- one deployment, plugin, or scripting surface

### 2. Identify privilege boundaries

Look for:

- user roles, scopes, claims, groups, and tenant boundaries
- admin panels, support tools, debug endpoints, and internal APIs
- scheduled jobs, service accounts, and automation identities
- plugins, scripts, templates, and code execution surfaces
- OS, container, database, and cloud permission boundaries

### 3. Generate Elevation of Privilege threats

Generate threats around:

- missing or inconsistent authorization checks
- IDOR-style access to higher-privilege objects or actions
- privilege confusion across tenants, roles, or delegated flows
- background jobs or internal services performing actions on behalf of users too broadly
- unsafe deserialization, template injection, or script execution that reaches privileged context
- admin-only features reachable through hidden routes or parameter switches
- support impersonation or break-glass paths with weak controls
- policy mismatches between application, database, and infrastructure layers

### 4. Stress privilege assumptions

For each privileged action, ask:

- Who should be allowed to do this, and where is that enforced?
- Is authorization enforced once, or consistently at every sensitive boundary?
- Can identifiers, claims, or tenant context be swapped or confused?
- Are internal, batch, or support paths running with more power than they need?
- Can control over low-trust input eventually reach code or actions in a privileged context?

### 5. Deliver concise threats

For each threat, capture:

- threat title
- component or boundary affected
- elevation scenario
- likely impact
- why the system may be vulnerable
- suggested mitigations or validation questions

## Output Rules

Default to a short list of concrete Elevation of Privilege threats.

Do not drift into Spoofing unless impersonation is only the first step toward a privilege increase.

## Example Requests

- Generate Elevation of Privilege threats for this architecture.
- Review this repo and identify where low-privilege users might gain admin capabilities.
- Use this data flow to find privilege-boundary mistakes between services and jobs.
