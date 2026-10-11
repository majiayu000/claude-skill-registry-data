---
name: stride-information-disclosure
description: Generate Information Disclosure threats for a system, repo, architecture, or data flow. Use when Codex needs to identify how sensitive data could be exposed through storage, transport, logs, APIs, metadata, configuration, backups, side channels, or trust-boundary mistakes.
---

# STRIDE Information Disclosure

## Overview

Use this skill to generate threat ideas specifically in the Information Disclosure category of STRIDE. Focus on unauthorized exposure of data, secrets, metadata, internal details, or tenant-isolated information.

Prefer threats tied to specific data classes, interfaces, and exposure paths over generic statements about confidentiality.

## Workflow

### 1. Establish the modeling scope

Choose one concrete slice first:

- one API or UI path
- one data storage or export path
- one integration or webhook flow
- one logging or observability path
- one administrative or support workflow

### 2. Identify sensitive data and exposure surfaces

Look for:

- PII, credentials, tokens, secrets, keys, and internal configs
- customer content, tenant data, financial data, health data, and proprietary IP
- logs, traces, metrics, analytics events, and debug output
- backups, snapshots, exports, caches, temp files, and object stores
- error messages, metadata, identifiers, and side-channel signals

### 3. Generate Information Disclosure threats

Generate threats around:

- overbroad API responses or object references
- cross-tenant leakage
- logs or telemetry containing sensitive values
- weak access controls on files, buckets, caches, or backups
- plaintext transport or weak encryption assumptions
- secrets exposed through config, client bundles, or stack traces
- sensitive metadata exposure even when payloads are protected
- support, admin, or export tooling revealing more than intended

### 4. Stress confidentiality assumptions

For each sensitive boundary, ask:

- Who can read this data now, and who should be able to?
- Is sensitive data copied into logs, queues, caches, or exports?
- Can one tenant or user learn about another through IDs, timing, or metadata?
- Are debug or error paths revealing internal details?
- Are downstream systems receiving more data than they need?

### 5. Deliver concise threats

For each threat, capture:

- threat title
- component or boundary affected
- disclosure scenario
- likely impact
- why the system may be vulnerable
- suggested mitigations or validation questions

## Output Rules

Default to a short list of concrete Information Disclosure threats.

Do not drift into Tampering or Repudiation unless confidentiality loss is the main issue.

## Example Requests

- Generate Information Disclosure threats for this SaaS architecture.
- Review this repo and identify where sensitive data may leak.
- Use this data flow to find cross-tenant exposure risks.
