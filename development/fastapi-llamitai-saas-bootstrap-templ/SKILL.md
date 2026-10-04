---
name: fastapi
description: Resolve a concrete FastAPI or Pydantic framework API question in backend/. Use when dependency lifetime, parameter parsing, response schemas or streaming behavior is unclear; backend-change owns implementation and project architecture.
---

# FastAPI framework reference

Use this skill for an unresolved framework API question, including a question
that arises during backend implementation. Read `backend/AGENTS.md` for the
project contracts; the installed version and code determine which framework
APIs exist.
Do not load this skill for routine backend edits with an established pattern.

1. Identify the exact framework symbol or behavior in question. Check the
   installed version in `backend/pyproject.toml` and its lock, then a matching
   installed use in `backend/src/`.
2. Consult only the relevant reference below. Treat its examples as generic
   FastAPI syntax, not the application's module or response design. For
   version-sensitive behavior, verify against the installed package or official
   framework documentation.
3. State the framework answer and how it fits the project contract. For a code
   change, use `backend-change` for implementation and its selected checks.

| Question | Reference |
| --- | --- |
| Dependency declaration, `yield` or scope | [dependencies.md](references/dependencies.md) |
| Path parameters, router APIs or operation metadata | [path-operations.md](references/path-operations.md) |
| Pydantic validation and model behavior | [pydantic.md](references/pydantic.md) |
| `response_model`, filtering or serialization | [responses.md](references/responses.md) |
| JSON Lines, bytes or SSE when explicitly in scope | [streaming.md](references/streaming.md) |
| A related tool choice needed to answer the API question | [other-tools.md](references/other-tools.md) |

Project routes use `add_api_route()`; endpoints return `ApiJSONResponse` with
declared `response_model` and status code. ORM is SQLAlchemy in the shared
database package, blocking calls use `asyncio.to_thread`, Next.js serves the
frontend, and local startup uses `just backend dev`. Generic examples in the
references do not change these choices or introduce a new product capability.
