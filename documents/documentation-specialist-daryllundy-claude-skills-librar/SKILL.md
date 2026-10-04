---
name: documentation-specialist
description: Technical documentation writing including README files, API docs, architecture
  docs, runbooks, and code comments. Use when asked to write a README, generate API
  documentation, document a codebase, write a runbook or operational guide, create
  an Architecture Decision Record (ADR), add docstrings to functions, or update outdated
  documentation.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: productivity
  tags:
  - documentation
  - readme
  - api-docs
  - runbooks
  - docstrings
  - technical-writing
---

# Documentation Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write a README`, `document this API`, `add docstrings`.
- The requested work fits this skill's lane: Writing READMEs, API documentation, runbooks, docstrings, architecture docs.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Fixing the code being documented.

## First actions
1. `Glob('**/README*', '**/docs/**', '**/CONTRIBUTING*', '**/CHANGELOG*')` — find existing docs
2. `Read` the main README and any existing docs to match style and completeness level
3. Identify audience: end users, developers, ops team, or all three

## Decision rules
- If documentation already exists for the topic: update the existing source of truth instead of creating a competing doc.
- If audience is unclear: infer it from the repository context and state that assumption in the document.
- If docs and implementation disagree: treat the code and tested behavior as the source of truth and call out the mismatch.

## Output contract
- README: must include Purpose, Prerequisites, Installation, Quick Start, Configuration reference
- Runbooks: must include Trigger conditions, Diagnostic steps, Resolution steps, Escalation path
- API docs: must include endpoint, method, auth, request/response schema, error codes, example

## Constraints
- NEVER document features that don't exist yet without clearly marking them as "planned"
- Scope boundary: fixing the code being documented belongs to other skills

## Reference
- `references/legacy-agent.md`: documentation patterns by type, docstring standards by language, README templates
