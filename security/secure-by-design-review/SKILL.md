---
name: secure-by-design-review
description: Review a repository, architecture, or local folder with a focus on secure-by-design principles. Use when Codex needs to assess whether a system’s structure, defaults, trust boundaries, workflows, and operational assumptions reduce security risk by design, not just through after-the-fact controls.
---

# Secure By Design Review

## Overview

Use this skill to build a focused, evidence-based review of whether a system is secure by design. Look beyond isolated bugs and ask whether the architecture, defaults, and operating model make the secure path the normal path.

Prefer structural observations over long vulnerability lists. Focus on the design decisions that make the system easier or harder to operate safely.

## Workflow

### 1. Establish the review scope

Choose the smallest meaningful scope before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious trust boundaries, entrypoints, admin paths, storage systems, and external integrations

If the folder or codebase is large, choose one of these scopes and say which one you chose:

- one core user or data flow
- one subsystem or service boundary
- one external integration
- one privileged or administrative workflow

### 2. Identify the design assumptions

Identify the assumptions the system appears to rely on, such as:

- trusted internal networks or trusted upstream systems
- operator discipline instead of enforced controls
- manual review instead of safe defaults
- shared credentials or shared mutable state
- hidden knowledge needed to avoid insecure behavior
- deployment or runtime assumptions that are not enforced in code

Separate explicit controls from tribal knowledge.

### 3. Evaluate secure-by-design principles

Review whether the system embodies these kinds of principles:

- secure defaults
- least privilege
- explicit trust boundaries
- defense in depth
- fail-safe behavior
- minimized attack surface
- strong separation of duties
- safe handling of secrets and sensitive data
- secure observability and auditability
- safe recovery and operational resilience

Look for places where the system depends on “people remembering to do the secure thing” instead of making it automatic.

### 4. Review the key design points

For each important design point, capture:

- file path or architectural component
- design decision or default behavior
- why it matters to secure-by-design posture
- what assumptions it relies on
- what can go wrong if the assumption fails
- whether the current design prevents, contains, or amplifies failure

Prioritize areas such as:

- authentication and authorization boundaries
- storage and transit of sensitive data
- administrative and support workflows
- secrets and key management
- defaults, configuration, and deployment assumptions
- background jobs, integrations, and privileged automation

### 5. Surface secure-by-design findings

Call out issues that materially affect design trustworthiness, especially:

- insecure defaults or opt-in security
- broad privilege with weak isolation
- excessive trust in internal callers, operators, or environment
- controls enforced only by documentation or convention
- dangerous workflows without review, confirmation, or containment
- hidden side effects or unclear ownership of security-critical state
- weak auditability or inability to safely investigate incidents
- weak failure handling that turns routine issues into security exposure
- architecture choices that make least privilege, tenant isolation, or recovery difficult

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. Secure-by-design posture summary
3. Key design observations
4. Findings and open questions
5. Recommended design improvements

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for security and design signals such as `auth`, `role`, `permission`, `token`, `secret`, `key`, `config`, `admin`, `internal`, `verify`, `tls`, `encrypt`, `audit`, `log`, `retry`, `fallback`, `default`, `allow`, `deny`, `policy`, `trust`
- framework-specific files such as `middleware`, `guards`, `providers`, `security`, `config`, `auth`, `policies`, `clients`, `workers`, `jobs`

Prioritize these signals:

- files that establish trust or privilege boundaries
- code that sets defaults or fallback behavior
- code that handles sensitive operations or privileged workflows
- code where the secure path appears optional, manual, or weakly enforced

## Output Rules

Be explicit about evidence quality:

- say `confirmed` when the code directly shows the design choice
- say `inferred` when the design assumption is likely but not fully proved in the inspected files
- say `not verified` when deployment controls, managed services, or organizational processes are missing

Do not reduce the review to a generic bug list.

When presenting observations, prefer real functions, files, and components over abstract slogans.

## Example Requests

- Review this repo for secure-by-design weaknesses.
- Inspect this architecture and explain whether the secure path is the default path.
- Assess this service with a focus on least privilege, safe defaults, and trust boundaries.
- Review this folder and identify where the design depends too much on operator discipline.
