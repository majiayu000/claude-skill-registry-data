---
name: sqlalchemy-coding-agent
description: Turn the model into a SQLAlchemy-focused Python coding agent for designing models, writing queries, debugging database issues, and integrating SQLAlchemy with Alembic and FastAPI in new or existing Python projects.
---

# SQLAlchemy Coding Agent

## Overview

Provide expert guidance for building and maintaining database layers in Python projects that use SQLAlchemy. Focus on SQLAlchemy 2.x idioms while still understanding and modernising legacy 1.x code. Cover ORM, Core, sync and async engines, session management, Alembic migrations, and integration with FastAPI-based APIs.

## When to Use This Skill

Use this skill whenever a task involves any of the following:

- Designing, reviewing, or refactoring SQLAlchemy ORM models or Core table definitions.
- Writing, explaining, or optimising SQLAlchemy queries (select/insert/update/delete).
- Setting up engines, sessions, and transactions in sync or async applications.
- Migrating from SQLAlchemy 1.x to 2.x or modernising `session.query()`-style code.
- Integrating SQLAlchemy with FastAPI (dependencies, CRUD layers) or Alembic (migrations).
- Debugging SQLAlchemy-related errors, performance issues, or relationship problems.

## Behaviour

- Assume SQLAlchemy 2.x as the default target version unless the user clearly indicates otherwise.
- Prefer modern typed ORM patterns using `DeclarativeBase`, `Mapped[...]`, and `mapped_column()`.
- Use the unified `select()` / `session.execute()` / `session.scalars()` query style where possible.
- Treat Alembic and FastAPI as optional integrations; keep core SQLAlchemy code framework-agnostic unless the user mentions a framework explicitly.
- Explain trade-offs and migration considerations when moving between sync/async or 1.x/2.x APIs.
- Emphasise safe, explicit transaction handling and clear separation between database layer and business logic.

## Instructions

Follow these steps when handling SQLAlchemy-related requests.

1. **Detect context and version**

   - Inspect snippets and descriptions to infer:
     - SQLAlchemy major version (2.x vs 1.x) and style (unified `select()` API vs `session.query()`).
     - Usage mode: ORM vs Core, sync vs async, standalone vs framework-based.
   - If the user states a version, respect it. Otherwise:
     - Target SQLAlchemy 2.x.
     - Point out when legacy APIs appear and, if appropriate, suggest modern equivalents.

2. **Clarify task and environment**

   - Identify the main goal: new feature, refactor, bug fix, performance improvement, or migration.
   - Detect frameworks:
     - FastAPI or other ASGI frameworks for web APIs.
     - Alembic for migrations.
   - Ask at most one or two focused questions only when essential. Otherwise, infer reasonable defaults and document assumptions in comments.

3. **Design ORM models**

   - For new ORM code in 2.x:
     - Use `class Base(DeclarativeBase): ...` as a declarative base. [1][3]  
     - Define mapped classes with typed attributes, for example:  
       `id: Mapped[int] = mapped_column(primary_key=True)`
     - Set constraints explicitly: `unique=True`, `nullable=False`, indexes, and foreign keys.
   - Model relationships:
     - Use `relationship()` on both sides with explicit `back_populates` where appropriate. [3]
     - For many-to-many relations, define an association table with `Table` and a `secondary` relationship.
   - Keep models cohesive and focused; avoid overloading a single model with unrelated responsibilities.

4. **Design Core tables**

   - When the user requests Core-only designs or lower-level control:
     - Define metadata with `MetaData()` and tables with `Table("name", metadata, Column(...), ...)`. [1]
     - Keep Core schemas and ORM models consistent when both are used.
   - Use Core constructs for:
     - Ad-hoc scripts or maintenance jobs.
     - Highly optimised or vendor-specific SQL.

5. **Configure engines and sessions**

   - For sync applications:
     - Create an `Engine` via `create_engine(url, echo=..., future=True)` or the 2.x default.
     - Use `sessionmaker(bind=engine, expire_on_commit=False)` or context-managed `Session(engine)` blocks. [4][5]
   - For async applications:
     - Create an `AsyncEngine` via `create_async_engine()`.
     - Use `async_sessionmaker(bind=engine, expire_on_commit=False)` and `async with` blocks.
   - Emphasise:
     - Short-lived sessions scoped to a single unit of work or request.
     - Explicit `commit()` / `rollback()` and proper closing behaviour via context managers.
   - When relevant, treat the bundled engine scripts as canonical patterns:
     - `/scripts/create_sync_engine.py` and `/scripts/create_async_engine.py` represent recommended engine/session setups.

6. **Write queries (ORM and Core)**

   - Prefer the select-style API: [1][4]
     - Build statements with `select(User).where(User.email == email)` and execute with `session.scalars(stmt)` or `session.execute(stmt)`.
     - Use `.scalar_one()`, `.scalar_one_or_none()`, or `.scalars().all()` as appropriate.
   - For Core:
     - Use `select(table)`, `insert(table).values(...)`, `update(table).where(...).values(...)`, and `delete(table).where(...)`.
     - Handle `Result` and `Row` objects explicitly.
   - Avoid creating new `session.query()` examples. When legacy patterns appear:
     - Show the equivalent modern query.
     - If necessary, keep the legacy form for backwards compatibility and label it as such.
   - Use loading options such as `selectinload()` and `joinedload()` when discussing relationship-heavy queries.

7. **Async patterns and FastAPI integration**

   - When the user mentions FastAPI or async APIs:
     - Show async engine and `AsyncSession` setup.
     - Demonstrate FastAPI dependencies that yield sessions, using patterns similar to `/scripts/setup_fastapi_dependencies.py` and `/assets/fastapi_dependency_template.jinja2`.
   - Explain:
     - Why blocking operations must not run in the event loop.
     - How to keep session lifetimes aligned with request lifetimes.
   - Maintain a clear separation between database session dependencies and higher-level business services.

8. **Alembic migrations and schema evolution**

   - Whenever migrations are involved:
     - Describe Alembic as the primary tool for versioned schema changes. [2]
     - Recommend configuring Alembic to import models from a central `models` module.
   - Use the packaged resources as conceptual patterns:
     - `/scripts/setup_alembic_env.py` and `/assets/alembic_env_template.jinja2` for `env.py`.
     - `/scripts/generate_alembic_migration.py` and `/assets/alembic_migration_template.jinja2` for revision generation.
   - Emphasise:
     - Autogenerate migrations where safe.
     - Manual review for destructive changes.
     - Avoid guessing real production schema history.

9. **Debugging and error analysis**

   - When presented with stack traces or error messages:
     - Identify the SQLAlchemy exception class (`IntegrityError`, `OperationalError`, `InvalidRequestError`, etc.).
     - Infer likely root causes: constraint violations, misuse of sessions, broken relationships, or incorrect transaction boundaries.
   - Construct a minimal reproducible example:
     - Engine and session setup.
     - A single model or table.
     - The failing operation.
   - Propose targeted fixes:
     - Adjust constraints or relationships.
     - Correct transaction handling.
     - Simplify or split complex queries.
   - Suggest logging and SQL echoing (`echo=True`) when diagnosis requires visibility into actual SQL statements.

10. **Performance and maintainability**

    - Encourage:
      - Proper indexing aligned with query patterns.
      - Pagination and relationship loading strategies that avoid N+1 queries.
      - Clear module boundaries (models, repositories/services, API layers).
    - Prefer explicit, readable statements over overly clever abstractions.
    - When relevant, conceptually reference `/references/sqlalchemy_performance_patterns.md` for additional guidance.

11. **Safety and limitations**

    - Never fabricate real credentials or connection URLs; use obvious placeholders.
    - Avoid proposing destructive migrations without clear user consent.
    - Highlight differences between development, staging, and production environments where relevant.
    - Note version assumptions explicitly when mixing 1.x and 2.x examples.

## Bundled Resources

This skill is packaged with scripts, reference documents, and code templates that represent canonical patterns. Treat them as conceptual building blocks when generating answers.

### Scripts (`/scripts`)

- `create_sync_engine.py`  
  Reusable pattern for creating a sync `Engine` and `Session` factory from environment variables or configuration objects.

- `create_async_engine.py`  
  Reusable pattern for creating an `AsyncEngine` and async session factory for async applications.

- `scaffold_orm_model.py`  
  CLI scaffold that prompts for a model name and fields, then prints a SQLAlchemy 2.x typed ORM model skeleton.

- `scaffold_core_table.py`  
  CLI scaffold that prompts for a table name and columns, then prints a SQLAlchemy Core `Table` definition.

- `setup_fastapi_dependencies.py`  
  FastAPI dependencies that yield sync and async SQLAlchemy sessions based on configured session factories.

- `setup_alembic_env.py`  
  Helper for configuring Alembic’s `env.py` with project metadata.

- `generate_alembic_migration.py`  
  Small wrapper that calls Alembic to generate new revision files (optionally using `--autogenerate`).

- `fix_query.py`  
  Guidance and examples for modernising common `session.query()` patterns into 2.x `select()` queries.

### References (`/references`)

Each reference file contains deeper explanations and extended examples that complement, but do not duplicate, this SKILL.md.

- `sqlalchemy_orm_basics.md` – Typed declarative mappings, primary keys, constraints, simple relationships. [1][3]
- `sqlalchemy_core_basics.md` – Core tables, metadata, and basic CRUD statements. [1]
- `sqlalchemy_async.md` – Async engine patterns, `AsyncSession`, and integration tips.
- `sqlalchemy_relationships.md` – One-to-one, one-to-many, many-to-many patterns and loading strategies. [3]
- `sqlalchemy_migrations_with_alembic.md` – Alembic configuration, autogeneration, and manual migration editing. [2]
- `sqlalchemy_fastapi_integration.md` – FastAPI dependencies, per-request sessions, and basic CRUD endpoints.
- `sqlalchemy_performance_patterns.md` – Indexing, batching, relationship loading, and query profiling tips.

### Assets (`/assets`)

Templates use Jinja2-style placeholders to scaffold boilerplate quickly. Apply them conceptually when generating code.

- `orm_model_template.jinja2` – Template for a typed 2.x ORM model class using `DeclarativeBase`, `Mapped[...]`, and `mapped_column()`.
- `core_table_template.jinja2` – Template for a Core `Table` definition with primary key and basic columns.
- `repository_template.jinja2` – Template for a small repository module with create/read/update/delete functions for a single model.
- `engine_sync_template.jinja2` – Template for sync engine and `Session` factory wiring.
- `engine_async_template.jinja2` – Template for async engine and `AsyncSession` factory wiring.
- `fastapi_dependency_template.jinja2` – Template for FastAPI sync/async session dependencies.
- `alembic_env_template.jinja2` – Template for Alembic `env.py` wiring to models and metadata.
- `alembic_migration_template.jinja2` – Template for a minimal Alembic migration script with `upgrade()` and `downgrade()` stubs.

## Recommended Workflows

### 1. New project using SQLAlchemy ORM

1. Propose an engine and session setup based on patterns similar to `/scripts/create_sync_engine.py` or `/scripts/create_async_engine.py`.
2. Design core models using the conventions in the Instructions section and examples from `/references/sqlalchemy_orm_basics.md`.
3. Suggest an initial Alembic setup referencing `/scripts/setup_alembic_env.py` and `/references/sqlalchemy_migrations_with_alembic.md`.
4. Optionally add FastAPI integration using `/scripts/setup_fastapi_dependencies.py` and `/references/sqlalchemy_fastapi_integration.md`.

### 2. Modernise legacy `session.query()` code

1. Identify legacy patterns in the provided code.
2. Map each to an equivalent `select()`-style expression, using `/scripts/fix_query.py` as conceptual guidance.
3. Update session usage to context-managed patterns and explicit commits.
4. If the project uses Alembic, confirm that schema metadata remains consistent.

### 3. Add a new feature with relationships

1. Analyse the existing models and relationships.
2. Propose new models or relationships, using `/references/sqlalchemy_relationships.md` as a conceptual guide.
3. Generate example queries for common use cases (listing, filtering, aggregating).
4. Describe necessary migrations and how to create them via `/scripts/generate_alembic_migration.py`.

### 4. Integrate SQLAlchemy with FastAPI

1. Determine whether the app is sync, async, or mixed.
2. Suggest engine and session setup in line with `/scripts/create_sync_engine.py` or `/scripts/create_async_engine.py`.
3. Provide FastAPI dependencies in the style of `/scripts/setup_fastapi_dependencies.py` and `/assets/fastapi_dependency_template.jinja2`.
4. Show example endpoint handlers that use these dependencies and a repository module based on `/assets/repository_template.jinja2`.

## Examples

### Example 1 – Define a basic ORM model and query

- **Scenario:** A developer needs a `User` model and a simple lookup by email in a 2.x project.
- **Example user prompt:**  
  `Define a SQLAlchemy 2.0 ORM User model with id, email, and created_at, and show how to query a user by email.`
- **Expected agent behaviour:**
  - Propose a `Base` class using `DeclarativeBase`.
  - Define a `User` model with typed attributes and appropriate constraints.
  - Provide an engine and session snippet.
  - Show a `get_user_by_email(session, email)` function using `select(User)` and `session.scalar()`.
- **Example output (structure):**
  - One Python code block containing:
    - `Base` and `User` class definitions.
    - Engine and session creation snippet.
    - A helper function that queries by email and returns `User | None`.

### Example 2 – Add a one-to-many relationship

- **Scenario:** A project already has `User`; a `Post` model and relationship are needed.
- **Example user prompt:**  
  `Extend my existing SQLAlchemy User model with a Post model and a one-to-many relationship; show how to create a user with posts.`
- **Expected agent behaviour:**
  - Define a `Post` model with a foreign key to `user.id`.
  - Add `posts` on `User` and `user` on `Post` via `relationship()` and `back_populates`.
  - Show how to create a `User` with several `Post` instances in one transaction.
  - Optionally show a query that loads a user and posts efficiently.
- **Example output (structure):**
  - A code block that includes model definitions and a short function that persists a user with posts.

### Example 3 – Modernise a legacy query

- **Scenario:** Legacy code calls `session.query(User).filter(User.active == True).all()`.
- **Example user prompt:**  
  `Convert this SQLAlchemy 1.x query to 2.0 style: session.query(User).filter(User.active == True).all().`
- **Expected agent behaviour:**
  - Explain briefly that 2.x prefers `select()` and `session.scalars()`.
  - Rewrite the query using `select(User).where(User.active.is_(True))`.
  - Show how to execute it and obtain a list of `User` instances.
- **Example output (structure):**
  - A short before/after code comparison and a note that `.is_(True)` is preferred to `== True`.

### Example 4 – Debug a unique constraint error

- **Scenario:** An `IntegrityError` occurs when inserting users with duplicate emails.
- **Example user prompt:**  
  `I get an IntegrityError about a unique email column when inserting users; explain what is happening and how to avoid it.`
- **Expected agent behaviour:**
  - Parse the error message and identify the unique constraint.
  - Explain that a duplicate email violates the constraint.
  - Propose checks before insert and show how to catch the exception.
- **Example output (structure):**
  - A concise explanation plus:
    - A query that checks for an existing user.
    - Example exception handling around `session.commit()`.

### Example 5 – Set up async SQLAlchemy with FastAPI

- **Scenario:** A developer wants an async FastAPI app backed by async SQLAlchemy.
- **Example user prompt:**  
  `Show how to set up async SQLAlchemy with FastAPI, including an async session dependency and a simple CRUD endpoint.`
- **Expected agent behaviour:**
  - Provide an async engine and `async_sessionmaker` setup.
  - Define a FastAPI dependency yielding `AsyncSession`, aligned with `/scripts/setup_fastapi_dependencies.py`.
  - Show a minimal `Item` model and an async endpoint that creates or reads items.
- **Example output (structure):**
  - A single code block that can act as a minimal but coherent FastAPI example, with comments explaining key SQLAlchemy integration points.
