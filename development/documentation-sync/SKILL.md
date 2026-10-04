---
name: documentation-sync
description: Keep project documentation in sync with code changes. Use when implementing features, modifying APIs, changing architecture, adding configuration, updating security, or making any change that affects user-facing or developer-facing documentation. Not for building an initial documentation suite from scratch (that is the documentation-creation skill).
---

# Documentation Synchronization Skill

## Profile keys consumed

- `framework.api_platform`
- `framework.graphql`
- `persistence.mapper`
- `persistence.engine`
- `architecture.bounded_contexts`
- `make.ci`
- `make.start`
- `quality.phpinsights.complexity`
- `quality.infection_msi`
- `capabilities.structurizr`

## Overview

This skill keeps the repository's `docs/` directory synchronized with
codebase changes, maintaining accuracy and completeness for both users
and developers.

## Core Principle

**Documentation is part of the definition of done.** No code change is
complete until the relevant documentation is updated — in the same
branch and PR as the code.

## When to Use This Skill

- **API changes**: adding/modifying REST or GraphQL endpoints
- **Database changes**: adding entities, modifying schema or mappings
- **Architecture changes**: design patterns, component structure
- **Configuration changes**: environment variables, config options
- **Security changes**: authentication, authorization
- **Testing changes**: new test strategies or test types
- **Performance changes**: optimizations, benchmarking
- **Feature implementation**: new user-facing features

## Documentation Map

The table below is the conventional `docs/` layout. Map each row to the
target repository's actual docs tree; when a file is absent, put the
content in the nearest equivalent — never create a parallel file when an
existing one covers the topic.

| File | Purpose | Update when |
| --- | --- | --- |
| `docs/api-endpoints.md` | REST/GraphQL endpoints, schemas | API changes |
| `docs/user-guide.md` | User-facing features | Feature changes |
| `docs/security.md` | Auth, authorization | Security changes |
| `docs/design-and-architecture.md` | System design, patterns, domain model | Architecture or domain changes |
| `docs/developer-guide.md` | Dev patterns, examples | Dev workflow changes |
| `docs/glossary.md` | Domain terminology | New domain concepts |
| `docs/advanced-configuration.md` | Env vars, config | Config changes |
| `docs/getting-started.md` | Setup, installation | Setup changes |
| `docs/operational.md` | Monitoring, logging | Ops changes |
| `docs/testing.md` | Test strategies | Test changes |
| `docs/performance.md` | Benchmarks, optimizations | Performance work |
| `docs/onboarding.md` | New dev onboarding | Process changes |
| `docs/versioning.md` | Version info | Version bumps |
| `docs/release-notes.md` | Changelog | Significant changes |

## Documentation Update Workflow

For each code change:

1. **Identify impact**: which docs need updates (use the map above)?
2. **Update content**: follow the scenario patterns below.
3. **Cross-reference**: ensure internal links remain valid; use relative
   links for files inside the repository.
4. **Validate examples**: run every code sample before committing.
5. **Review checklist**: complete the pre-commit checklist below.

## Update Scenarios

### REST endpoints

Applies to any REST API regardless of `framework.api_platform`; when
`framework.api_platform` is a version string, also regenerate the API
Platform OpenAPI spec. Update `docs/api-endpoints.md`
with: endpoint definition (method + path), request body example,
response example with status code, and an error table (status code +
meaning, e.g. 400 invalid input, 401 unauthorized, 409 conflict). Add
usage examples to `docs/user-guide.md`.

Regenerate the API spec whenever endpoint definitions change. The
profile `make` map defines no logical key for spec export, so locate
the repository's spec-export target in its Makefile (or the framework's
export command) and run it; note the gap if none exists. Reference
targets from the upstream service:

```bash # profile-example
make generate-openapi-spec   # exports to .github/openapi-spec/spec.yaml
make generate-graphql-spec   # exports to .github/graphql-spec/spec
```

### GraphQL operations

Applies when `framework.graphql` is true; otherwise skip with a note.
Update `docs/api-endpoints.md` with the operation definition (a fenced
`graphql` block for the query/mutation plus a `json` block for input
variables), regenerate the GraphQL spec (same Makefile-discovery rule
as above), and add client integration examples to `docs/user-guide.md`.

### Database schema

Update `docs/design-and-architecture.md` when adding or modifying
entities, fields, indexes, or relationships: list each field with type
and purpose, describe entity relationships, and record migration notes.
Phrase persistence details from the profile — `persistence.mapper`
decides whether you document ORM migrations (`doctrine-orm`) or
document-mapping changes (`doctrine-odm`), and `persistence.engine`
names the engine in connection examples. Update `docs/developer-guide.md`
with repository usage patterns.

### Domain model

Update the domain design section of `docs/design-and-architecture.md`
when introducing aggregates, commands, events, or changing context
boundaries: list new aggregates, command handlers, domain events, and
interactions between the contexts declared in
`architecture.bounded_contexts`. Always add new domain terms to
`docs/glossary.md` — define a term before using it anywhere else.

### Configuration

Update `docs/advanced-configuration.md` for every new environment
variable: name, type, default, required-or-not, a one-line description,
a usage example, and validation rules. Update `docs/getting-started.md`
when the variable is required for basic setup.

### Security

Update `docs/security.md` (auth flows, permission changes, security
considerations) and `docs/api-endpoints.md` (per-endpoint auth
requirements). Add client auth examples to `docs/user-guide.md`.

### Testing

Update `docs/testing.md` when adding test types: command, directory,
and purpose. Documented thresholds must come from the profile
`quality.*` keys — canonical defaults are complexity 94
(`quality.phpinsights.complexity`) and MSI 100 (`quality.infection_msi`),
and thresholds are raise-only: never document a lowered bar. See
[testing-workflow](../testing-workflow/SKILL.md) for how the suites run.

### Performance

Update `docs/performance.md` with the optimization name, measured
impact (metric: before → after), and any required configuration changes.

### Architecture patterns

Update the patterns section of `docs/design-and-architecture.md` when
adopting or deprecating a pattern: pattern description, implementation
example, benefits and trade-offs, and a migration path from the old
pattern. Update diagrams for structural changes; when
`capabilities.structurizr` is true, the architecture model (e.g.
`workspace.dsl`) must be synced in the same change.

## Documentation Quality Standards

### Consistency

- Follow the existing doc structure, heading levels, and formatting
- Use terminology from `docs/glossary.md`; define new terms first
- Fenced code blocks carry a language hint and blank lines around them
- Cross-reference related sections with relative links

### Completeness

- Document all public APIs: request/response schemas, auth
  requirements, every error code, and a curl example
- Cover error handling and edge cases, not just the happy path
- Provide both basic and advanced examples with realistic data and
  expected output

### Maintenance

- Remove outdated information; never leave stale content beside new
- Mark deprecations clearly with a migration path and removal timeline
- Update `docs/release-notes.md` for significant changes and
  `docs/versioning.md` for version bumps and breaking changes
- Validate all internal and external links; remove dead ones
- Keep architecture, sequence, and entity diagrams in sync

## Pre-Commit Checklist

- [ ] **Identify impact**: all affected docs listed
- [ ] **Update content**: scenario patterns applied
- [ ] **Cross-reference**: links verified
- [ ] **Test examples**: every sample executed (boot the service via
      the target mapped by `make.start` to verify endpoint examples;
      a `null` target means note the capability as absent)
- [ ] **Check consistency**: terminology matches the glossary
- [ ] **Update specs**: spec-export target run when API docs changed
- [ ] **Review changes**: complete, accurate, nothing stale

## Integration with Development

- **During development**: documentation is code — update docs in the
  same PR, test examples, validate links.
- **During code review**: reviewers check accuracy, example
  completeness, terminology consistency, and link validity.
- **During CI**: the target mapped by `make.ci` runs the automated doc
  checks (link validation, example syntax, spec generation and
  validation). Fix the docs when a check fails — never disable the
  check. See [ci-workflow](../ci-workflow/SKILL.md).

## Success Criteria

- All affected docs updated in the same PR as the code
- Code examples tested and working
- Links and references valid
- Terminology consistent with the glossary
- Release notes updated for significant changes
- Docs reflect actual code behavior
