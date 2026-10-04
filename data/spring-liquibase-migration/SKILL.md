---
name: spring-liquibase-migration
description: Use this skill when adding, generating, reviewing, or fixing Liquibase database migrations in Spring Boot projects. It should configure Spring Boot Liquibase, create master changelog files, write safe YAML/XML/SQL changesets, add rollback blocks, use preconditions, follow existing changelog style, and avoid modifying already executed changesets.
---

# Spring Liquibase Migration Skill

This skill helps agents create production-safe Liquibase migrations for Spring Boot projects.

Use this skill when the user asks to add Liquibase to Spring Boot, configure changelogs, generate or review database migrations, convert JPA entities into migrations, add rollback/preconditions, or fix Liquibase issues.

## Core principles

Always follow these rules unless the user explicitly asks otherwise:

1. Never modify already executed changesets.
2. Always create a new changeset for schema changes.
3. Prefer small, focused changesets.
4. Prefer YAML changelogs by default unless the existing project uses XML, SQL, or JSON.
5. Follow the project's existing changelog style.
6. Use a master changelog that includes smaller migration files.
7. Use stable, descriptive changeset IDs.
8. Add rollback blocks for production migrations.
9. Add preconditions when object existence or database state is uncertain.
10. Do not use `spring.jpa.hibernate.ddl-auto=update` for Liquibase-managed schemas.
11. Prefer `spring.jpa.hibernate.ddl-auto=validate` when JPA is used.
12. Avoid destructive changes unless rollback/data-safety has been considered.
13. Do not generate fake database credentials.
14. Do not remove data without warning.
15. Do not assume a database type when it can be detected from project configuration.

## Recommended changeset ID style

Use this format:

```txt
YYYY-MM-DD-001-short-description
YYYY-MM-DD-002-short-description
```

Examples:

```txt
2026-05-21-001-create-users-table
2026-05-21-002-add-email-index-to-users
2026-05-21-003-create-roles-table
```

If the project already has an ID convention, follow the existing convention.

## Recommended author style

Use the author already used in the project if available. If no author exists, use `system`, `developer`, or a user-provided name. Do not invent personal names.

## Required default structure

When creating Liquibase from scratch, prefer:

```txt
src/main/resources/
  db/
    changelog/
      db.changelog-master.yaml
      changes/
        2026-05-21-001-create-users-table.yaml
        2026-05-21-002-add-email-index-to-users.yaml
```

Master changelog:

```yaml
databaseChangeLog:
  - include:
      file: db/changelog/changes/2026-05-21-001-create-users-table.yaml
  - include:
      file: db/changelog/changes/2026-05-21-002-add-email-index-to-users.yaml
```

Spring Boot config:

```yaml
spring:
  liquibase:
    enabled: true
    change-log: classpath:db/changelog/db.changelog-master.yaml
  jpa:
    hibernate:
      ddl-auto: validate
```

## Required project files when adding Liquibase

When adding Liquibase to a Spring Boot project, create or update:

- `pom.xml` or `build.gradle`
- `src/main/resources/application.yml` or `application.properties`
- `src/main/resources/db/changelog/db.changelog-master.yaml`
- at least one migration file in `src/main/resources/db/changelog/changes/`
- documentation if the project has docs

## Maven dependency

```xml
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
```

## Gradle dependency

```gradle
implementation 'org.liquibase:liquibase-core'
```

## Preferred changelog format

Default to YAML:

```yaml
databaseChangeLog:
  - changeSet:
      id: 2026-05-21-001-create-users-table
      author: system
      changes:
        - createTable:
            tableName: users
            columns:
              - column:
                  name: id
                  type: UUID
                  constraints:
                    primaryKey: true
                    nullable: false
      rollback:
        - dropTable:
            tableName: users
```

Use XML only if the existing project uses XML. Use SQL only if the existing project uses SQL formatted changelogs.

## Preconditions

Use preconditions when creating a table/column/index that may already exist, adding foreign keys to uncertain data, applying database-specific changes, or running risky/destructive changes.

Common safe pattern:

```yaml
preConditions:
  - onFail: MARK_RAN
  - not:
      - tableExists:
          tableName: users
```

For destructive changes, prefer `HALT` instead of `MARK_RAN`.

## Rollback rules

Add rollback for createTable, addColumn, createIndex, addForeignKeyConstraint, createSequence, seed data, rename operations, and custom SQL when possible. Do not write fake rollback. If rollback is not safely possible, say so explicitly and explain why.

## Database type rules

PostgreSQL: UUID, BOOLEAN, BIGINT, TEXT, VARCHAR, TIMESTAMP, JSONB only if PostgreSQL-specific is acceptable.

MySQL/MariaDB: UUID usually CHAR(36) or BINARY(16), BOOLEAN/TINYINT(1), DATETIME/TIMESTAMP, JSON only if supported. Avoid PostgreSQL-specific types.

Unknown DB: prefer portable Liquibase types: UUID, VARCHAR(255), TEXT, BOOLEAN, BIGINT, DECIMAL(19,2), TIMESTAMP.

## Entity-to-migration rules

When generating migrations from JPA entities, inspect `@Entity`, `@Table`, `@Id`, `@GeneratedValue`, `@Column`, `@Enumerated`, relationship annotations, `@JoinColumn`, `@JoinTable`, indexes and unique constraints. Ignore DTOs, `@Transient`, and computed fields. Do not create unsafe one-step non-null migrations for non-empty production tables.

## Review checklist

Check ID uniqueness, author consistency, small changesets, rollback, preconditions, database-specific types, master changelog include, destructive data loss, Hibernate ddl-auto, indexes, foreign keys, and constraint names.

## Common mistakes to prevent

- Editing old changesets.
- Using `ddl-auto=update` with Liquibase.
- One huge changeset containing unrelated changes.
- Missing rollback.
- Missing preconditions.
- Database-specific SQL without checking DB type.
- Duplicate changeset IDs.
- Forgetting master changelog include.
- Adding a non-null column to a non-empty table without default/backfill strategy.
- Dropping columns/tables without data safety plan.

## Output style

When creating or modifying migrations, list files changed, explain each changeset, mention rollback behavior, mention preconditions, mention production safety concerns, and suggest commands such as `mvn test`, `mvn spring-boot:run`, `./gradlew bootRun`, or Liquibase plugin commands only if configured.

## Suggested prompt

```txt
Use $spring-liquibase-migration.

Add Liquibase to this Spring Boot project and create production-safe YAML migrations. Use a master changelog, small focused changesets, rollback blocks, preconditions where needed, and set Hibernate ddl-auto to validate. Follow existing project style if present.
```
