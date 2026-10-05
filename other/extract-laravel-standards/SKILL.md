---
name: extract-laravel-standards
description: Audit completed Laravel projects and propose reusable updates to personal Laravel standards without importing project-specific details.
tags:
  - laravel
  - php
---

# Extract Laravel Standards

Use this skill after a Laravel project, feature set, or major module has been completed and the user wants to turn proven patterns into reusable personal standards.

## Workflow

1. Inspect the project structure, Laravel version, PHP version, test stack, formatter, static analysis, CI checks, queue setup, frontend stack, and deployment-sensitive configuration.
2. Identify repeated implementation patterns in controllers, Form Requests, Actions, Services, models, migrations, jobs, policies, Livewire components, tests, and quality tooling.
3. Compare findings against the currently installed Laravel standards before proposing any update.
4. Classify each finding as `NEW`, `UPDATE`, `DUPLICATE`, `CONFLICT`, `PROJECT_ONLY`, or `REJECT`.
5. Promote only conventions that are reusable across unrelated Laravel applications and improve correctness, security, testability, maintainability, consistency, or operational reliability.
6. Remove client names, company names, domains, URLs, credentials, internal identifiers, provider-specific payload quirks, business terminology, and accidental technical debt.
7. Create a proposal in `proposals/pending/` before editing any global skill files.
8. Display the proposed diff and wait for acceptance before moving accepted proposals into standards.
9. Never edit upstream third-party skills or copy external skill text wholesale.

## Proposal Format

Use this structure for each proposal:

~~~markdown
# <Project or Module> Laravel Standards Proposal

## Source Scope

- Audited area:
- Date:
- Verification reviewed:

## Findings

### NEW

- Finding:
- Reason:
- Suggested target file:

### UPDATE

- Existing standard:
- Proposed change:
- Reason:

### PROJECT_ONLY

- Pattern:
- Why it should not become global:

## Sanitization

- Removed identifiers:
- Removed business rules:
- Removed secrets or sensitive details:

## Proposed Diff

```diff
```
~~~

## Global Standard Eligibility

A convention may become global only when it is:

- consistently applied in completed work;
- supported by tests, quality checks, or production feedback;
- aligned with Laravel conventions;
- useful outside the source project;
- free of secrets and project-specific business rules.

Reject temporary workarounds, one-off provider details, accidental complexity, and rules that only make sense for one client or domain.
