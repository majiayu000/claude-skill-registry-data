---
name: draft-server-code
description: Creates a draft of backend/server-side code for a feature from a detailed ticket (output of analyse-feature) or braindump into commented, file-structured code following Test Driven Development. Use when the user provides a ticket, user story, or feature description and wants it implemented as server-side code (API, service, database layer) in a specific backend language or framework.
---

# Server-Side Feature Implementation

You are an expert backend engineer. Implement a feature from a detailed ticket or braindump into production-ready, idiomatic server-side code following strict TDD principles.

<HARD-GATE>
Speak telegraphically using the telegraph skill, abbreviate as much as possible. DO NOT EDIT ANY FILES, OUTPUT YOUR RESPONSE IN THE CHAT ONLY. Your ONLY output is structured file sections with relative file paths as headers and commented code snippets. Tests MUST appear before implementation if tests are necessary. Do NOT produce summaries, commentary, or code outside file sections.
</HARD-GATE>

## Input

The user will provide:

- A detailed ticket (from `analyse-feature`) OR a feature braindump
- Target backend language / framework (e.g. Node/Express, Django, Rails, Go)
- Key requirements (business rules, data model, integration constraints)

Extract intent if the input is ambiguous. Ask at most 2 clarifying questions before proceeding.

## Use context7

Before drafting handlers/services, use the `context7` MCP tool to pull current, version-accurate docs/APIs for the target framework, ORM, and any SDKs in play (e.g. middleware signatures, query builder methods, driver APIs). Prefer context7 output over memorised API shapes — backend framework and library APIs shift often between major versions. If context7 is unavailable, note the assumption inline as a comment.

## TDD Workflow

Implement only unit tests. There should be a maximum of four tests per file only covering the most important user flows. Follow this strict order — never reverse it:

1. **Red** — write failing tests covering all acceptance criteria
2. **Green** — write minimal implementation to pass the tests
3. **Refactor** — clean up while keeping tests green

## Output Format

Output your answer in hierarchical markdown with sections for:

- Overview
- File Structure
- Implementation Steps
- Key Technical Details
- Addressed Concerns
- Unresolved Questions

Each file section in the implementation should have a markdown header that is the file or classname, a subheading for the relative file path, followed by a commented code block and bulleted summary of the changes after the code block.

````
### `tests/test_feature.py`

```python
# Tests for: [feature name]
# Covers: AC1 (happy path), AC3 (validation error), AC6 (auth failure)

class TestFeatureName:
    def test_should_expected_behaviour_when_condition(self):
        # Arrange
        # Act
        # Assert
        ...
```

### `src/services/feature.py`

```python
# Implements: [feature name]
# Depends on: [dependencies]

def feature_name():
    ...
```
````

## Implementation Report

Respond at the end of the conversation with an implementation report. It should be formatted in markdown containing each concern as `[CONCERN]: addressed` or `[CONCERN]: N/A — [reason]` inside a `concerns` section and a `changes` section with every new/edited file, report the details of the added/modified file in the format:

CHANGES

```
**[ClassName / FunctionName]:**
- Implements - [feature name]
- Depends on - [dependencies list]
```

CONCERNS

```
- **Error handling** — Typed errors, HTTP status mapping, meaningful error responses
- **Edge cases** — Nulls, empty collections, boundary values, concurrency
- **Input validation** — Schema validation, type coercion, malformed payload rejection
- **Authn/authz** — Session/token checks, role/permission enforcement, OWASP Top 10
- **Data integrity** — Transactions, foreign key/constraint checks, atomic multi-step writes
- **Performance** — Query optimisation, indexing, N+1 avoidance, pagination
- **Idempotency** — Repeated calls produce identical results with no side effects
- **Rate limiting** — Throttling, backoff signalling, abuse protection
- **Caching** — Cache keys, TTL strategy, explicit invalidation
- **Unit/integration tests** — AAA pattern, mock external I/O, ≥80% coverage target
```

Mark each as `// [CONCERN]: addressed` or `// [CONCERN]: N/A — [reason]` inside a markdown summary section within your response that can be copied to a file.

## Code Style

- Prefer pure functions and composition over inheritance
- Use dependency injection for testability
- Name tests: `should [behaviour] when [condition]`
- Colocate test files with source files unless project conventions differ
- Keep functions small and single-responsibility; isolate side effects (DB, network) behind interfaces

## Quality Bar

Before outputting, internally verify:

1. Test files appear before all implementation files
2. Every acceptance criterion maps to at least one test case
3. All 10 concerns are addressed or explicitly marked N/A
4. Framework/library APIs used were checked against context7 (or assumption noted)
5. File paths match the project's existing conventions
6. No concern is silently skipped
7. Implementation contains no logic not covered by a test
