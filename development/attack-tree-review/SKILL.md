---
name: attack-tree-review
description: Review a repository, architecture, or local folder and construct an attack tree for a chosen attacker goal. Use when Codex needs to model how an attacker could achieve a concrete objective, break the goal into sub-goals and attack paths, map evidence from code or design to each branch, or explain threats in a tree structure rather than a flat list.
---

# Attack Tree Review

## Overview

Use this skill to turn a codebase or design into an evidence-based attack tree. Start from one concrete attacker goal, then decompose it into the major paths, required sub-goals, preconditions, and enabling weaknesses that could allow the attacker to succeed.

Prefer one strong attack tree for a meaningful root goal over several shallow trees. Make uncertainty explicit and label inferred branches clearly.

## Workflow

### 1. Choose the root attacker goal

Pick the smallest useful attacker objective first.

Good root goals include:

- gain unauthorized access to customer data
- execute privileged actions in the system
- modify critical business state
- exfiltrate secrets or credentials
- disrupt service availability
- compromise the tenant, environment, or admin plane

If the user does not specify a root goal, infer the most meaningful goal from the repo and state that choice clearly.

### 2. Establish the review scope

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious entrypoints, trust boundaries, privileged workflows, storage paths, and integrations related to the chosen goal

If the repo is large, narrow scope to:

- one request path
- one privileged workflow
- one data path
- one integration
- one deployment/runtime boundary

### 3. Decompose the goal into major branches

Break the root goal into a few major attacker strategies. These usually map to distinct paths such as:

- steal or spoof identity
- bypass authorization
- tamper with trusted data or state
- abuse an integration or callback
- gain code execution
- misuse operator or automation workflows
- exploit weak storage, transport, or configuration controls

Use AND/OR reasoning where it helps:

- `OR` when multiple independent paths can achieve the goal
- `AND` when the attacker must complete multiple prerequisite steps

### 4. Trace evidence-backed sub-goals

For each branch, trace the code or architecture that supports it. Capture:

- file path or architectural component
- attacker sub-goal
- why the branch is plausible
- direct evidence from code or workflow
- required preconditions
- likely impact if the branch succeeds

Prioritize branches that:

- cross trust boundaries
- involve secrets, tokens, or privileged identities
- affect sensitive data or admin actions
- rely on weak defaults, shared state, or operator discipline
- create broad blast radius if exploited

### 5. Build the attack tree

Represent the attack tree in a compact structure. Prefer one of:

- an indented tree
- a Mermaid mindmap or flowchart
- a short ordered tree with explicit `AND` / `OR` annotations

For each node, include:

- node title
- type: root / branch / leaf
- evidence quality: `confirmed`, `inferred`, or `not verified`
- brief note on why it matters

### 6. Surface the most important paths

After building the tree, call out:

- the shortest attacker paths
- the branches with the highest impact
- the branches with weak or missing controls
- key choke points where one control would collapse many branches

### 7. Deliver a concise report

Default to this structure:

1. Root goal and scope
2. Attack tree
3. Key attack paths
4. Findings and open questions
5. Recommended control points

## Output Rules

- Prefer one well-supported tree over many speculative branches.
- Be explicit about evidence quality:
  - `confirmed` when code or architecture directly supports the branch
  - `inferred` when the branch is plausible but not fully proved
  - `not verified` when deployment or runtime details are missing
- Keep the tree readable. Do not explode it into dozens of low-value leaves unless the user asks for depth.
- Prefer real files, functions, components, and workflows over generic labels.

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for signals such as `auth`, `token`, `secret`, `key`, `admin`, `permission`, `role`, `upload`, `download`, `callback`, `webhook`, `exec`, `subprocess`, `verify=False`, `config`, `internal`, `worker`, `job`, `storage`, `queue`, `cache`
- follow the files most relevant to the chosen root goal

Prioritize these signals:

- files that connect untrusted input to sensitive operations
- code that establishes trust or privilege
- storage, transport, and integration boundaries
- administrative, support, or automation paths

## Example Requests

- Build an attack tree for this repo with the goal of stealing customer data.
- Inspect this codebase and create an attack tree for unauthorized admin access.
- Use this architecture to generate an attack tree for service disruption.
- Review this folder and build an attack tree for compromising the tenant environment.
