---
name: application-security-review
description: "Use when reviewing application code, APIs, dependencies, or configuration for security weaknesses, especially around identity, authorization, untrusted input, sensitive data, or external integrations to map trust boundaries, test relevant controls safely, and report evidence-based risks with practical mitigations. Trigger for a requested security review or a high-risk software change; this is not an authorization to exploit systems or alter production."
---

# Application Security Review

## Overview

This skill applies when reviewing application code, APIs, dependencies, or configuration for security weaknesses, especially around identity, authorization, untrusted input, sensitive data, or external integrations. Its intended outcome is to map trust boundaries, test relevant controls safely, and report evidence-based risks with practical mitigations.

## When to Use

### Preserved source section: When to Use

Use this skill for a security-focused review of application code or configuration. For MCP server and tool-specific risks, load `mcp-server-integration-safety` as well. Treat this as a bounded review, not a penetration-test mandate.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Trace end-to-end paths.** Follow high-risk data from source to use. Verify that checks occur at the enforcement boundary and cannot be bypassed through alternate routes, stale state, or untrusted identifiers.
5. **Gather proportionate evidence.** Prefer source inspection, existing tests, safe static checks, and non-destructive local probes. Never dump secret values into reports. Do not interpret a clean scan as proof that the application is secure.

### Source boundary statements from: Safety and Stop Conditions

- Do not access, print, transmit, or commit secret material.
- Do not run exploit payloads against a system without explicit scope and approval.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The authorized repository, service, change, and review scope.
- Relevant architecture, data flows, identity model, deployment settings, and dependency manifests.
- The intended users, assets, trust boundaries, and impact if confidentiality, integrity, or availability fails.
- Any restrictions on running tests, sending requests, accessing secrets, or using production systems.

## Instructions

### Preserved source section: Procedure

1. **Set the boundary.** Confirm which code, environments, and checks are in scope. Use local or test systems by default. Ask before active probing, destructive tests, production access, or handling real credentials.
2. **Map the path of sensitive data.** Identify entry points, identities, privilege transitions, storage, outbound calls, and trust boundaries. Note assumptions that are not supported by inspected code or configuration.
3. **Review control families.** Check authentication separately from authorization; validate and constrain input; review output encoding, query construction, file handling, secret exposure, session/CSRF controls, rate limits, dependency risk, logging, and security-relevant defaults as applicable.
4. **Trace end-to-end paths.** Follow high-risk data from source to use. Verify that checks occur at the enforcement boundary and cannot be bypassed through alternate routes, stale state, or untrusted identifiers.
5. **Gather proportionate evidence.** Prefer source inspection, existing tests, safe static checks, and non-destructive local probes. Never dump secret values into reports. Do not interpret a clean scan as proof that the application is secure.
6. **Rank findings.** Describe the affected asset, preconditions, plausible impact, evidence, and confidence. Separate confirmed vulnerabilities from hardening suggestions and unknowns.
7. **Recommend the smallest safe mitigation.** Tie each recommendation to the failure mechanism. If asked to fix issues, change only the authorized scope and add regression coverage; otherwise provide findings without editing.
8. **Re-check after remediation.** Verify the original weakness is addressed and nearby behavior remains correct. Report any untested path or residual risk.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs

- The intended users, assets, trust boundaries, and impact if confidentiality, integrity, or availability fails.

### Source conditional guidance from: Procedure

7. **Recommend the smallest safe mitigation.** Tie each recommendation to the failure mechanism. If asked to fix issues, change only the authorized scope and add regression coverage; otherwise provide findings without editing.

### Source conditional guidance from: Safety and Stop Conditions

- Stop if the authorized boundary is unclear or a check could affect real users, data, or service availability.
- If evidence is insufficient, label the point unverified instead of asserting a vulnerability or declaring the system safe.

## Output Format

### Preserved source section: Finding Format

For each actionable issue, provide: severity with rationale, affected path or component, attacker prerequisites, concise evidence, impact, and a specific remediation. Use line references where available. Avoid publishing exploit details beyond what the authorized audience needs to verify and fix the issue.

## Validation Checklist

Not specified in source skill.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

7. **Recommend the smallest safe mitigation.** Tie each recommendation to the failure mechanism. If asked to fix issues, change only the authorized scope and add regression coverage; otherwise provide findings without editing.

## Stop Conditions

### Preserved source section: Safety and Stop Conditions

- Stop if the authorized boundary is unclear or a check could affect real users, data, or service availability.
- Do not access, print, transmit, or commit secret material.
- Do not run exploit payloads against a system without explicit scope and approval.
- If evidence is insufficient, label the point unverified instead of asserting a vulnerability or declaring the system safe.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

Not specified in source skill.
