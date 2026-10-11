---
name: mitre-defend-review
description: Review a repository, architecture, workflow, or local folder with a focus on MITRE D3FEND and defensive coverage concepts. Use when Codex needs to assess how well a system detects, prevents, contains, hardens against, or responds to attacker behavior, and where defensive coverage appears weak or missing.
---

# MITRE D3FEND Review

## Overview

Use this skill to analyze a system through the lens of defensive coverage. Focus on which protections, hardening choices, visibility points, containment measures, and response-enabling controls exist by design, and which attacker behaviors appear weakly defended.

Prefer practical defensive coverage analysis over a long catalog of possible controls.

## Workflow

### 1. Establish the review scope

Choose the smallest meaningful slice before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious trust boundaries, control points, observability paths, and privileged workflows

If the folder or codebase is large, choose one of these scopes and say which one you chose:

- one exposed service or ingress path
- one privileged workflow
- one identity or secret-handling path
- one end-to-end detection and containment path

### 2. Identify control surfaces

Identify where the system appears to:

- authenticate and authorize
- validate, sanitize, or constrain input
- limit privilege or isolate tenants/components
- protect secrets, tokens, and keys
- log, trace, alert, or audit sensitive behavior
- rate limit, retry safely, contain failures, or degrade safely
- verify integrity of code, config, artifacts, or data

### 3. Map defensive coverage

Review the system for defensive coverage themes such as:

- hardening and safe defaults
- identity assurance and least privilege
- integrity protection
- network and transport protection
- runtime containment and segmentation
- auditability and monitoring
- resilience, recovery, and operational containment

When helpful, describe controls in D3FEND-style language, but keep the output readable and practical.

### 4. Review the key design points

For each important control point, capture:

- file path or architectural component
- defensive purpose
- what attacker behavior it may prevent, detect, or contain
- what assumptions it relies on
- what gaps remain if the control fails or is bypassed

Prioritize:

- authentication and authorization gates
- secrets and trust material handling
- logging and audit paths
- configuration defaults and fallback behavior
- workflow approvals and privileged automation
- segmentation, isolation, and blast-radius controls

### 5. Surface defensive gaps

Call out issues that materially weaken defensive posture, especially:

- missing or optional controls on critical paths
- weak detection for sensitive or attacker-relevant actions
- poor isolation, broad privilege, or weak blast-radius containment
- weak secret handling or integrity enforcement
- controls documented by policy but not enforced in code or architecture
- poor incident investigation support
- failure paths that disable or bypass protection

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. Defensive posture summary
3. Key control points
4. Coverage gaps and open questions
5. Recommended defensive improvements

## Output Rules

- Use D3FEND-oriented or defensive-control language when it helps, but stay practical.
- You do not need official D3FEND artifacts or IDs unless the user explicitly asks for them.
- Prefer coverage and gap analysis over generic best-practice lists.
- Be explicit about evidence quality:
  - `confirmed` when code or architecture directly shows the control
  - `inferred` when a control likely exists but is not fully proved
  - `not verified` when runtime, infrastructure, or SOC processes are missing

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for signals such as `auth`, `role`, `permission`, `token`, `secret`, `key`, `verify`, `tls`, `encrypt`, `audit`, `log`, `alert`, `trace`, `policy`, `allow`, `deny`, `retry`, `limit`, `validate`, `sanitize`, `isolate`, `internal`, `admin`
- focus on files that establish controls, trust boundaries, observability, safe defaults, or containment

## Example Requests

- Review this repo using MITRE D3FEND-style defensive coverage analysis.
- Assess defensive gaps in this architecture.
- Inspect this codebase and identify where detection, hardening, or containment are weak.
