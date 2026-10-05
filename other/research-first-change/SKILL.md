---
name: research-first-change
description: Require current source, documentation, version, and rationale evidence before API, framework, dependency, security, integration, MCP, or external-service changes. Use when implementation depends on behavior that may have changed or should be sourced before coding.
---

# Research First Change

## Purpose

Ground external-knowledge decisions in current evidence before changing code, dependencies, integration behavior, or security posture.

## Inspect First

- package manifests, lockfiles, docs/specs, dependency policy, security docs, and existing research evidence
- official docs, source repos, changelogs, or standards for the technology being changed
- local version constraints and compatibility notes

## Procedure

1. Decide whether research is required.
   - Require it for dependency additions/upgrades, framework APIs, shadcn/ui or MCP setup, auth/security behavior, migrations with external tooling, and production integrations.
   - Prefer official docs or primary sources.

2. Capture evidence.
   - Use `assets/templates/research-evidence.md.tmpl` when durable documentation is useful.
   - Record source URLs, accessed date, relevant version, decision, alternatives considered, and compatibility impact.
   - When trajectory tracing exists, record dependency, security, MCP, or external API risk surfaces and the research intervention.

3. Validate evidence.
   - Run `scripts/check_research_evidence.py <repo>` when an artifact exists.
   - Add or update target repo `scripts/check-research-evidence` when dependency, API, framework, security, integration, or MCP changes are part of the ongoing repo workflow.
   - Confirm claims are tied to sources and local repo constraints.

4. Route implementation.
   - Use `$dependency-governance` for package policy.
   - Use `$openspec-sdd` or `$prompt-to-spec-converter` when research changes product behavior.
   - Use `$security-baseline` for security-sensitive findings.

## Validation

- Confirm evidence cites current primary sources and version constraints.
- Run `./scripts/check-research-evidence` when present.
- Confirm the implementation plan names the commands that will prove compatibility.
- Record a no-research-needed rationale for purely local changes.

## Completion Criteria

- External-knowledge decisions have source, version, rationale, and validation evidence before code changes depend on them.
