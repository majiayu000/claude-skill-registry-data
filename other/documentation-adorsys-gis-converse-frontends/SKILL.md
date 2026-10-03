---
name: documentation
description: Generates and maintains project documentation including API docs, docstrings, README updates, and changelogs.
---

# Documentation Skill

When generating or updating documentation, ensure accuracy, completeness, and consistency with the codebase.

## 1. Public API Documentation (JSDoc / Docstrings)

- Add documentation to all public functions, methods, classes, and interfaces
- Include: purpose, parameters (with types), return value, thrown exceptions/errors
- Use the project's established doc format (JSDoc, Google-style docstrings, KDoc, Javadoc, etc.)
- Include usage examples for non-obvious APIs
- Document default values for optional parameters
- Mark deprecated APIs with `@deprecated` and include the migration path
- Keep doc comments concise — one sentence for simple functions, detailed for complex ones

## 2. README Updates

- Update the README when new features, commands, or configuration options are added
- Keep the installation/setup section current with any new dependencies or steps
- Update the usage section with new CLI commands, API endpoints, or UI features
- Maintain the project description to accurately reflect current capabilities
- Ensure badges (CI status, coverage, version) are functional and up to date
- Do NOT add sections that duplicate information available elsewhere (e.g., full API reference)

## 3. API Documentation

- Document all endpoints: method, path, description, parameters, request/response bodies
- Include example requests and responses with realistic data
- Document all possible error responses with HTTP status codes and error body shapes
- Document authentication requirements per endpoint
- Note rate limits, pagination parameters, and query filters
- Keep API docs versioned alongside the code — prefer generated docs (OpenAPI/Swagger) when available

## 4. Complex Business Logic

- Add inline comments explaining the _why_ behind non-obvious decisions
- Document algorithms with a brief description of the approach and time/space complexity
- Explain business rules that are not self-evident from the code
- Document invariants and preconditions that callers must satisfy
- Reference external specifications, RFCs, or requirements documents by number/link

## 5. Changelog Maintenance

- Follow Keep a Changelog format (https://keepachangelog.com)
- Categorize entries: Added, Changed, Deprecated, Removed, Fixed, Security
- Write entries from the user's perspective, not the developer's
- Include the PR or issue number for traceability
- Keep an "Unreleased" section at the top for pending changes
- Date entries use ISO 8601 format (YYYY-MM-DD)

## 6. Architecture Documentation

- Update architecture docs when new services, modules, or integrations are added
- Document data flows for new features that cross service boundaries
- Keep component diagrams current (or flag them as outdated)
- Record significant design decisions as ADRs (Architecture Decision Records)

## Quality Standards

- Documentation must be accurate — verify all code references, paths, and commands
- Use consistent terminology throughout (define terms in a glossary if needed)
- Write for the audience: README for new developers, API docs for consumers, inline comments for maintainers
- Run documentation links and code examples to verify they work
- Use active voice and imperative mood for instructions
- Avoid jargon without explanation; define acronyms on first use
