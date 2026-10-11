---
name: stride-tampering
description: Generate Tampering threats for a system, repo, architecture, or data flow. Use when Codex needs to identify how data, messages, state, code, configuration, or control flow could be modified without authorization while stored, processed, or transmitted.
---

# STRIDE Tampering

## Overview

Use this skill to generate threat ideas specifically in the Tampering category of STRIDE. Focus on unauthorized modification of data, code, configuration, control signals, or state.

Prefer threats tied to real write paths, mutable state, and integrity assumptions over generic "data could be changed" statements.

## Workflow

### 1. Establish the modeling scope

Choose one concrete slice first:

- one API write path
- one messaging or event flow
- one storage or cache path
- one deployment or config path
- one administrative or operational workflow

### 2. Identify mutable assets

Look for:

- database records, files, objects, queues, caches, and logs
- configs, feature flags, templates, policies, and infrastructure definitions
- binaries, packages, scripts, containers, and CI artifacts
- tokens, claims, headers, requests, responses, and callbacks
- workflow state, approvals, and task transitions

### 3. Generate Tampering threats

Generate threats around:

- unauthorized modification of stored data
- in-flight message or request manipulation
- cache poisoning or stale-state overwrite
- client-side parameter tampering
- configuration or infrastructure tampering
- artifact, dependency, or build-pipeline tampering
- privilege-sensitive state transitions without integrity checks
- weak validation of signed, versioned, or sequenced data

### 4. Stress integrity assumptions

For each mutable boundary, ask:

- Who is allowed to write or update this?
- What prevents an attacker from modifying it directly or indirectly?
- Is integrity checked with signatures, hashes, versioning, or transactional controls?
- Can stale or reordered updates overwrite valid state?
- Are admin tools, imports, or background jobs bypassing normal validation?

### 5. Deliver concise threats

For each threat, capture:

- threat title
- component or boundary affected
- tampering scenario
- likely impact
- why the system may be vulnerable
- suggested mitigations or validation questions

## Output Rules

Default to a short list of concrete Tampering threats.

Do not drift into Information Disclosure or Denial of Service unless modification of integrity is the main issue.

## Example Requests

- Generate Tampering threats for this workflow.
- Review this repo and identify where state or config tampering is plausible.
- Use this architecture to find places where messages could be modified in transit.
