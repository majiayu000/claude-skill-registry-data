---
name: surrealdartb
description: Use this skill when working with the SurrealDartB package in Dart/Flutter projects. This includes creating embedded SurrealDB databases, performing CRUD operations, managing schemas with code generation, working with vector embeddings for AI/ML applications, building type-safe queries with ORM features, and handling migrations. Invoke when user mentions SurrealDB, embedded databases, vector search, semantic similarity, or asks to implement database features in Dart/Flutter.
---

# SurrealDartB

## Overview

SurrealDartB is a Dart package providing embedded SurrealDB capabilities with comprehensive ORM, code generation, and AI/ML vector search features. The package enables local-first database applications with ACID transactions, schema migrations, and production-ready vector similarity search.

**Package Location:** `lib/`
**Test Location:** `test/`
**Examples:** `example/scenarios/`

## When to Use This Skill

Invoke this skill when:
- Setting up or configuring SurrealDartB in Dart/Flutter projects
- Implementing database operations (CRUD, queries, transactions)
- Working with vector embeddings for semantic search or AI applications
- Generating ORM code from model annotations
- Managing database schema migrations
- Building type-safe queries with WHERE conditions
- Implementing authentication or parameter management
- Troubleshooting common issues (vector DDL syntax, rollback bugs, etc.)

## Core Capabilities

### 1. Database Connection & CRUD Operations
**Reference:** `references/connection-crud.md`

Basic database lifecycle and CRUD operations including connection management, storage backends (memory/RocksDB), and core query methods.

### 2. Schema & Table Structures
**Reference:** `references/schema-tables.md`

TableStructure system, FieldDefinition, SurrealDB type system, and schema validation.

### 3. Vector/AI Features
**Reference:** `references/vectors.md`

Vector data types (F32/F64/I8/I16/I32/I64), indexing (HNSW/M-Tree/FLAT), similarity search, and distance metrics for AI/ML applications.

### 4. ORM & Type-Safe Queries
**Reference:** `references/orm-where.md`

WhereCondition system, field builders, and type-safe query construction.

## Advanced Features

### 5. Schema Migrations
**Reference:** `references/migrations.md`

Migration engine, introspection, DDL generation, and migration safety.

### 6. ORM Relationships
**Reference:** `references/orm-relationships.md`

Graph relations, edges, includes, FETCH/RELATE patterns.

### 7. Code Generation Annotations
**Reference:** `references/annotations.md`

@SurrealTable, @SurrealField, @SurrealRecord, @SurrealRelation and other annotation types.

### 8. Authentication
**Reference:** `references/authentication.md`

Credential types, signin/signup/authenticate methods (limited in embedded mode).

## Specialized Features

### 9. Transactions
**Reference:** `references/transactions.md`

Transaction support with known rollback limitation.

### 10. Parameters & Functions
**Reference:** `references/parameters-functions.md`

Parameter management (set/unset) and function execution (run, built-in functions).

### 11. Types & Exceptions
**Reference:** `references/types-exceptions.md`

RecordId, Datetime, Duration, and exception hierarchy.

## Troubleshooting

**Reference:** `references/troubleshooting.md`

Known issues, gotchas, and workarounds including:
- Vector field DDL syntax requirements
- Transaction rollback bug
- Schema validation errors
- Platform-specific considerations

## Usage Pattern

When helping users with SurrealDartB:

1. **Identify the feature area** from their request
2. **Reference the appropriate documentation** from the list above
3. **Provide concise code examples** using the documented APIs
4. **Note any gotchas** from troubleshooting reference
5. **Suggest related features** when applicable

## Reference Organization

References are organized by usage frequency to optimize context:

- **Core:** connection-crud, schema-tables, vectors, orm-where (most frequent)
- **Advanced:** migrations, orm-relationships, annotations, authentication (regular)
- **Specialized:** transactions, parameters-functions, types-exceptions (occasional)
- **Support:** troubleshooting (as needed)

Load references into context as needed based on the user's specific request.
