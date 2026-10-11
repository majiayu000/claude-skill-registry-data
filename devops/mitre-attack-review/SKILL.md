---
name: mitre-attack-review
description: Review a repository, architecture, workflow, or local folder with a focus on MITRE ATT&CK-style adversary behavior. Use when Codex needs to map plausible attacker actions, techniques, and objectives to a system, identify likely kill-chain paths, or organize threats in ATT&CK-oriented language.
---

# MITRE ATT&CK Review

## Overview

Use this skill to analyze a system through the lens of adversary behavior. Focus on what an attacker could realistically do, which goals they could pursue, and which MITRE ATT&CK-style techniques are most plausible given the system design, components, trust boundaries, and operating model.

Prefer a grounded mapping of likely attacker behavior over a broad laundry list of ATT&CK techniques.

## Workflow

### 1. Establish the review scope

Choose the smallest meaningful slice before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious entrypoints, trust boundaries, privileged workflows, data paths, and integrations

If the folder or codebase is large, choose one of these scopes and say which one you chose:

- one external attack path
- one privileged workflow
- one deployment or runtime boundary
- one end-to-end kill-chain candidate

### 2. Identify attacker entrypoints and objectives

Identify:

- externally reachable surfaces
- internal trust assumptions attackers could abuse
- privileged components, secrets, tokens, or admin tooling
- high-value data and sensitive operations
- likely attacker objectives such as credential access, persistence, lateral movement, collection, exfiltration, or disruption

### 3. Map plausible adversary behaviors

Generate likely ATT&CK-style behaviors around:

- initial access
- execution
- persistence
- privilege escalation
- defense evasion
- credential access
- discovery
- lateral movement
- collection
- command and control
- exfiltration
- impact

Do not force every tactic. Only include tactics supported by the system context.

### 4. Review the key system points

For each important point in the attacker path, capture:

- file path or architectural component
- attacker opportunity
- likely technique pattern or ATT&CK-style label
- why it is plausible in this system
- preconditions or dependencies
- likely impact if successful

Prioritize:

- exposed services, APIs, import paths, and admin tools
- script execution, plugin, template, or deserialization surfaces
- secret handling, tokens, credentials, and trust material
- automation, CI/CD, and scheduled jobs
- weak segmentation or broad service permissions

### 5. Surface ATT&CK-oriented findings

Call out issues that materially increase adversary opportunity, especially:

- over-trusted internal boundaries
- broad privilege or over-scoped service accounts
- weak credential handling
- hidden execution surfaces
- poor containment between components or tenants
- missing visibility around attacker-relevant actions
- easy persistence or hard-to-detect misuse paths

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. Likely attacker objectives
3. ATT&CK-style behavior map
4. Key findings and open questions

## Output Rules

- Use ATT&CK-oriented language, but stay practical and readable.
- You do not need official ATT&CK IDs unless the user explicitly asks for them.
- Prefer plausible attacker paths over exhaustive framework coverage.
- Be explicit about evidence quality:
  - `confirmed` when code or architecture directly supports the path
  - `inferred` when the attacker path is plausible but not fully proved
  - `not verified` when runtime or infrastructure details are missing

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for signals such as `auth`, `token`, `secret`, `key`, `admin`, `exec`, `shell`, `script`, `upload`, `download`, `plugin`, `template`, `deserialize`, `callback`, `webhook`, `internal`, `worker`, `job`, `cron`, `config`, `env`
- focus on files that expose entrypoints, privileged actions, trust boundaries, secrets, automation, or remote execution opportunities

## Example Requests

- Review this repo using MITRE ATT&CK concepts.
- Map likely attacker behaviors for this architecture.
- Inspect this codebase and identify plausible credential access and lateral movement paths.
