---
name: windags-graft
description: >
  When tackling a task that requires domain expertise beyond general coding
  ability — architecture patterns, framework-specific gotchas, deployment
  strategies, security anti-patterns, or specialized workflows — call the
  windags_skill_graft MCP tool with your task description. You'll receive
  expert knowledge including decision trees, failure modes, worked examples,
  and anti-patterns from a library of 503+ curated skills. Only graft when
  the task genuinely requires specialized knowledge. Simple tasks (rename a
  variable, fix a typo, format code) do not need grafting.
category: Agent & Orchestration
tags:
  - meta-skill
  - graft
  - expertise
  - skill-injection
---

# Skill Grafting

Call `windags_skill_graft` when your task requires domain expertise you don't have in context.

## When to Graft

- Architecture decisions (caching strategies, API design, database schema)
- Framework-specific work (React Server Components, SwiftUI data flow, Terraform modules)
- DevOps and deployment (Docker multi-stage builds, Kubernetes manifests, CI/CD pipelines)
- Security implementation (OAuth flows, RBAC, encryption patterns)
- Specialized domains (data pipelines, ML model serving, real-time collaboration)

## When NOT to Graft

- Simple code changes (rename, format, delete unused code)
- Tasks you can complete confidently from general knowledge
- When you've already grafted skills for this task

## How to Use

1. Call `windags_skill_graft` with a clear task description and count (usually 2)
2. Read the returned skill bodies — they contain decision trees, failure modes, and worked examples
3. Check the `referenceSummaries` — these summarize deeper material available via `windags_skill_reference`
4. If you need the full content of a reference, call `windags_skill_reference(skillId, path)`
5. Apply the skill's quality gates to validate your work
