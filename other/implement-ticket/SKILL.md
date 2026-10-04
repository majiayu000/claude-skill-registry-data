---
name: implement-ticket
description: >
  Scaffolds and implements code from any source of instructions: a Jira ticket, a technical-scoping
  document, a macro-scoping document, a markdown spec, or a free-form description.
  Use this skill whenever a user wants to start coding a feature or a task — regardless of whether
  a formal ticket exists.
  Trigger on: "implémente IDF-XXXX", "code IDF-XXXX", "on démarre IDF-XXXX", "développe ce ticket",
  "implémente ça", "code ce qui est dans ce doc", "voici la spec", "je veux que le système fasse X",
  "commence le développement", "mets en place cette feature", or any instruction to write code
  from a spec, ticket, or description.
  Requires Jira MCP when the source is a Jira ticket. Always requires workspace file access and terminal.
---

## Purpose

Transform any source of instructions into working, scaffolded code that follows the exact
architecture conventions of this codebase — entity, domain DTOs, repository, service, controller,
module, UI components, tests, and TypeORM migration when relevant.

This skill **never writes code without showing a plan first** and waiting for explicit user validation.

---

## Step 0 — Detect and normalise the input source

Before anything else, identify the nature of the user's input:

| Source type                | How to detect                                                                   | What to do                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Jira ticket                | Message contains a key matching `IDF-\d+`                                       | Delegate to the `jira-read` skill (Mode 1) to fetch and display the ticket, then continue here with the result |
| Technical-scoping document | Structured markdown with sections like API contracts, data model, security      | Read it as-is; extract entities, endpoints, business rules, audience                                           |
| Macro-scoping document     | Structured markdown with sections like Objectifs, Hors périmètre, Règles métier | Extract functional intent; warn that technical detail may be missing                                           |
| Markdown file in repo      | User provides a path to a `.md` file                                            | Read the file; then treat as technical or macro spec based on content                                          |
| Free-form description      | Plain text with no recognised structure                                         | Ask up to 3 targeted clarifying questions before continuing                                                    |

**When the source is a Jira ticket:** load `.claude/skills/read-ticket/SKILL.md` and execute
Mode 1 to fetch and display the ticket. Once the ticket is displayed, continue directly to the
output below — do not wait for a separate user instruction.

**Output of this step:** a normalised context containing:

- Domain name (or candidate name)
- What the system must do
- Audience(s) targeted: `young` / `agents` / `partners` (one or more)
- Known acceptance criteria (or derived from context)

If the source is a macro-scoping document with no technical spec, warn the user:

> "⚠️ Je ne dispose que d'un cadrage macro sans spec technique. Je vais faire des choix d'implémentation par défaut — confirme pour continuer ou fournis le document de technical-scoping."

---

## Step 1 — Explore the repository for scope

Once the input is normalised, explore the codebase to determine:

1. **Does the domain already exist?**

   - Search `libs/` for a folder matching the domain name (e.g. `libs/grants/`, `libs/offers/`)
   - If not found: this is a **new domain** — note it and continue (see "New domain" section below)

2. **Which layers are actually needed for this ticket?**

   - Detect from the normalised context which of the following apply:
     - `entity` — data model changes or new table
     - `domain` — new commands, queries, views (always needed when API changes)
     - `repository` — new data access queries
     - `service` — new business logic
     - `controller` — new or modified endpoints
     - `module` — new feature module or existing module update
     - `app.module.ts` — new module registration
     - `ui-agents` — agents back-office UI (react-admin)
     - `ui-partners` — partners back-office UI (react-admin)
     - `ui-young` — young persons' UI (Next.js + MUI/Tailwind)
     - `tests` — unit test stubs
     - `migration` — TypeORM migration (only when entity is created or modified)

3. **What is the audience?**
   Look for explicit audience signals in the content: mentions of "jeune", "agent", "partenaire",
   page or route names, Keycloak realm names (`REALM_YOUNG`, `REALM_AGENT`, `REALM_PARTNER`).
   If ambiguous, ask the user before continuing.

4. **Does the operation need a transaction?**

   Determine whether the service method writes to **multiple tables atomically**:

   - If yes → use `this.dataSource.transaction(async (manager) => { ... })` scoped in the service
   - If no (read, or single-table write) → call the repository directly, no transaction

   Wrapping reads or single-table writes in a transaction acquires unnecessary locks, holds
   the connection longer and writes to the PostgreSQL WAL for no benefit. Only use a transaction
   when atomicity across multiple operations is genuinely required.

   If the ticket is ambiguous, ask: "Cette opération écrit-elle dans plusieurs tables de façon atomique, ou s'agit-il d'une écriture simple ?"

5. **Does the ticket touch a known tech debt area?**

   Cross-reference the normalised context against the **Known Tech Debt** table in `AGENTS.md`.
   For each matching area, read the linked documentation file before writing any code there.

   If one or more matches are found, include a **"⚠️ Zones de dette concernées"** section in the
   plan presented to the user (Step 2), listing which docs were read and which constraints apply.

---

## Step 2 — Present the implementation plan

**This step is mandatory. Never skip it. Never write code before receiving explicit confirmation.**

Present a structured plan in this exact format. Include the new-domain warning line only when Step 1 detected a new domain.

```
## Plan d'implémentation — [Nom du domaine] ([Source: IDF-XXXX / spec / description libre])

> ⚠️ Nouveau domaine détecté — une validation du TL est recommandée avant de merger.

### Couches concernées

| Layer         | Fichier(s)                                                          | Action   |
|---------------|---------------------------------------------------------------------|----------|
| Entity        | libs/databases/young-db/src/entities/{name}.entity.ts               | CREATE   |
| Domain interfaces | libs/{d}/{d}-domain/src/interfaces/commands/create-{d}-command.interface.ts | CREATE   |
|               | libs/{d}/{d}-domain/src/interfaces/views/{d}-view.interface.ts              | CREATE   |
| API DTOs      | libs/{d}/{d}-api/src/commands/create-{d}.command.ts                         | CREATE   |
|               | libs/{d}/{d}-api/src/views/{d}.view.ts                                      | CREATE   |
| Domain errors | libs/{d}/{d}-domain/src/errors/{name}.error.ts                      | CREATE   |
| Repository    | libs/{d}/{d}-api/src/infrastructure/sql/{d}.repository.ts           | CREATE   |
| Mapper        | libs/{d}/{d}-api/src/infrastructure/sql/{d}.mappers.ts              | CREATE   |
| Service       | libs/{d}/{d}-api/src/services/{d}.service.ts                        | CREATE   |
| Controller    | libs/{d}/{d}-api/src/controllers/{d}.controller.ts                  | CREATE   |
| Module opts   | libs/{d}/{d}-api/src/{d}-feature.options.ts                         | CREATE   |
| Module        | libs/{d}/{d}-api/src/{d}-feature.module.ts                          | CREATE   |
| Registration  | apps/idf-young-api/src/app/app.module.ts                            | MODIFY   |
| UI agents     | libs/{d}/{d}-ui/src/components/List{D}.tsx                          | CREATE   |
| Tests         | libs/{d}/{d}-api/src/services/{d}.service.spec.ts                   | CREATE   |
| Migration     | libs/databases/young-db/src/migrations/[generated after build]      | GENERATE |

### Audience cible
[jeunes / agents IDF / partenaires]

### Stratégie transactionnelle
[Transaction `DataSource.transaction()` — écriture multi-tables atomique]
[Pas de transaction — lecture / écriture mono-table]

### ⚠️ Zones de dette concernées
> (include this section only if Step 1.4 detected matches)
[list the detected areas and the constraints retained after reading the relevant doc]

### Critères d'acceptance détectés
1. [AC1]
2. [AC2]
...
```

Wait for the user to say "OK", "go", "valide", "c'est bon", or equivalent.

If the user asks to adjust the scope (remove a layer, add one, change a path), update the plan
and present it again before proceeding.

---

## Step 3 — Implement layer by layer

**Before writing any layer, read `apps/idf-young-documentation/docs/coding-standards/architecture.md`.**
This document is the single source of truth for layer conventions, naming patterns, and code examples.

Implement in this strict order. Only implement the layers that were validated in the plan.
After each layer, briefly confirm what was created and any decision made.

### Layer 1 — Entity

Location: `libs/databases/young-db/src/entities/{name}.entity.ts`

**Always use `EntitySchema<T>` — never `@Entity()` class decorators.**

Pattern: dual export — the TypeScript interface and the EntitySchema constant share the same name.

```typescript
// Interface
export interface MyDomainEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  archivedAt: Date | null;
  name: string;
}

// Schema (same identifier, same file)
export const MyDomainEntity = new EntitySchema<MyDomainEntity>({
  name: 'my-domains', // table name: plural kebab-case
  columns: {
    id: { type: 'uuid', generated: 'uuid', primary: true },
    createdAt: { type: 'timestamptz', createDate: true, nullable: false },
    updatedAt: { type: 'timestamptz', updateDate: true, nullable: false },
    archivedAt: { type: 'timestamptz', nullable: true },
    name: { type: 'text', nullable: false },
  },
  relations: {
    owner: {
      type: 'many-to-one',
      target: () => SomeOtherEntity,
      joinColumn: { name: 'ownerId' },
      eager: false,
    },
  },
});
```

Column type reference: `'uuid'`, `'timestamptz'`, `'text'`, `'integer'`, `'boolean'`, `'jsonb'`.
All timestamps use `'timestamptz'` (timezone-aware). PKs are always `uuid` auto-generated.

Register the entity and database migration in `libs/databases/young-db/src/main.ts` (entities array).

### Layer 2 — Domain interfaces + API DTOs

⚠️ **Architecture rule — read before writing any view, query, or command.**

The domain layer must be framework-free: **no `class-validator`, `class-transformer`, or `@nestjs/swagger` imports in `*-domain`**.
Decorated classes (`.view.ts`, `.query.ts`, `.command.ts`) live in the `*-api` layer and implement interfaces defined in `*-domain`.
The frontend imports **only the domain interfaces**, never the api classes — this prevents backend dependencies from leaking into the frontend bundle.

#### 2a — Interface in domain (consumed by frontend)

Location: `libs/{d}/{d}-domain/src/interfaces/`

```typescript
// search-my-domain-query.interface.ts
import type { PageQueryInterface } from '@idf-subventionjeunes-web/commons-domains';

// my-domain-view.interface.ts
export interface MyDomainViewInterface {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  name: string;
}

// create-my-domain-command.interface.ts
export interface CreateMyDomainCommandInterface {
  name: string;
  description?: string;
}

export interface SearchMyDomainQueryInterface extends PageQueryInterface {
  // add filter/sort fields as needed
}
```

Export from `*-domain/src/interfaces/views/`, `interfaces/commands/`, `interfaces/queries/`.
Expose through the domain library's `index.ts`.

#### 2c — Error classes in domain

Location: `libs/{d}/{d}-domain/src/errors/`

Business errors belong in the domain layer — plain TypeScript, zero framework dependency.

```typescript
// unknown-my-domain.error.ts
import { DomainBaseError } from '@idf-subventionjeunes-web/commons-domains';

export class UnknownMyDomainError extends DomainBaseError {
  constructor(id: string) {
    super(404, 'my-domain.unknown-error');
  }
}
```

**Rules:**

- Extend `DomainBaseError` from `commons-domains`
- Never add `@ApiProperty` on error classes — Swagger error documentation belongs on the controller via `@ApiResponse`
- File naming: `unknown-my-domain.error.ts` → kebab-case, suffix `.error.ts`
- Export from the domain library's `index.ts`

#### 2b — Decorated class in api (never imported by frontend)

Location: `libs/{d}/{d}-api/src/`

**Command** (write operation input):

```typescript
// create-my-domain.command.ts  →  libs/{d}/{d}-api/src/commands/
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

import type { CreateMyDomainCommandInterface } from '@idf-subventionjeunes-web/my-domain-domains';
import { Expose } from 'class-transformer';
import { IsString, MaxLength, IsOptional } from 'class-validator';

export class CreateMyDomainCommand implements CreateMyDomainCommandInterface {
  @Expose() @ApiProperty() @IsString() @MaxLength(255) name!: string;

  @Expose() @ApiPropertyOptional() @IsString() @IsOptional() description?: string;
}
```

**Query** (search/filter input):

```typescript
// search-my-domain.query.ts  →  libs/{d}/{d}-api/src/queries/
import { PageQuery } from '@idf-subventionjeunes-web/commons-api';
import type { SearchMyDomainQueryInterface } from '@idf-subventionjeunes-web/my-domain-domains';

export class SearchMyDomainQuery extends PageQuery implements SearchMyDomainQueryInterface {
  // add filter/sort fields as needed
}
```

**View** (response DTO):

```typescript
// my-domain.view.ts  →  libs/{d}/{d}-api/src/views/
import { ApiProperty } from '@nestjs/swagger';

import type { MyDomainViewInterface } from '@idf-subventionjeunes-web/my-domain-domains';
import { Expose } from 'class-transformer';

export class MyDomainView implements MyDomainViewInterface {
  @Expose() @ApiProperty() id!: string;
  @Expose() @ApiProperty() createdAt!: Date;
  @Expose() @ApiProperty() updatedAt!: Date;
  @Expose() @ApiProperty() name!: string;
}
```

### Layer 3 — Repository

Location: `libs/{d}/{d}-api/src/infrastructure/sql/{d}.repository.ts`

Repositories inject `DataSource` directly — they do **not** receive a `QueryRunner`.

> **Write methods — `insert` / `update` over `save`:** Prefer explicit `insert()` (create) and `update()` (modify)
> over TypeORM's `save()`. The `save()` method performs a SELECT before each write to decide between INSERT and
> UPDATE — this is unnecessary overhead and makes the intent ambiguous. Use `save()` only when you genuinely
> need upsert semantics and are aware of the extra query.

**Standard repository — reads and write methods:**

```typescript
import { Injectable } from '@nestjs/common';

import { MyDomainEntity } from '@idf-subventionjeunes-web/databases';
import { DataSource } from 'typeorm';

@Injectable()
export class MyDomainSqlRepository {
  constructor(private readonly dataSource: DataSource) {}

  async findById(id: string): Promise<MyDomainEntity | null> {
    return this.dataSource.manager.findOne(MyDomainEntity, { where: { id } });
  }

  async findAll(): Promise<MyDomainEntity[]> {
    return this.dataSource.manager.find(MyDomainEntity);
  }

  async create(data: Omit<MyDomainEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<MyDomainEntity> {
    const result = await this.dataSource.manager.insert(MyDomainEntity, data);
    return this.dataSource.manager.findOneOrFail(MyDomainEntity, { where: { id: result.identifiers[0].id } });
  }

  async update(id: string, data: Partial<Omit<MyDomainEntity, 'id' | 'createdAt' | 'updatedAt'>>): Promise<MyDomainEntity | null> {
    await this.dataSource.manager.update(MyDomainEntity, { id }, data);
    return this.dataSource.manager.findOne(MyDomainEntity, { where: { id } });
  }
}
```

**When a DB error must be translated into a named domain error** (e.g. unique constraint violation),
return `Promise<Result<>>` via `Result.async` so the service can handle it without catching exceptions:

```typescript
import { Result } from '@idf-subventionjeunes-web/commons-domains';
import { isUniqueConstraintViolation } from '@idf-subventionjeunes-web/commons-api'; // or a local helper

async create(data: Omit<MyDomainEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<Result<MyDomainAlreadyExistsError, MyDomainEntity>> {
  const insertResult = await Result.async(
    this.dataSource.manager.insert(MyDomainEntity, data),
    (e) => isUniqueConstraintViolation(e) ? new MyDomainAlreadyExistsError() : undefined,
  );
  if (isErr(insertResult)) return insertResult;
  const entity = await this.dataSource.manager.findOneOrFail(MyDomainEntity, { where: { id: insertResult.success.identifiers[0].id } });
  return Ok(entity);
}
```

**Rules:**

- Prefer `insert()` for creates, `update()` for updates — avoid `save()` unless upsert is genuinely needed
- Return `T | null` directly for reads (service checks for null and returns `Err`)
- Return `Result<NamedDomainError, T>` via `Result.async` only when a specific DB error must be surfaced as a domain concept (e.g. uniqueness violation) — see [result-pattern.md](apps/idf-young-documentation/docs/coding-standards/result-pattern.md#usage-in-a-repository--infrastructure-layer)
- Never wrap infrastructure panics in `Result` — let them throw and be caught by the global exception filter

### Layer 3b — Mapper

Location: `libs/{d}/{d}-api/src/infrastructure/sql/{d}.mappers.ts`

Pure functions (no injection, no side effects) converting between persistence types (`*Entity`) and domain interfaces (view interfaces). The repository returns raw entities; the mapper transforms them — the service calls the mapper.

```typescript
// my-domain.mappers.ts
import { MyDomainEntity } from '@idf-subventionjeunes-web/databases';
import type { MyDomainViewInterface } from '@idf-subventionjeunes-web/my-domain-domains';

const toMyDomainView = (entity: MyDomainEntity): MyDomainViewInterface => ({
  id: entity.id,
  createdAt: entity.createdAt,
  updatedAt: entity.updatedAt,
  name: entity.name,
});

export const MyDomainSqlMappers = {
  toMyDomainView,
};
```

**Rules:**

- Exported as a named object `{Domain}SqlMappers` (e.g. `MyDomainSqlMappers`, `GrantsSqlMappers`)
- Functions inside are plain functions, not class methods
- Never import NestJS in a mapper file
- Use manual field mapping for plain interfaces; use `plainToInstance` only in the controller when the target is a decorated `.view.ts` class with `@Expose()`

### Layer 4 — Service

Location: `libs/{d}/{d}-api/src/services/{d}.service.ts`

Services do **not** receive a `QueryRunner`. They call repositories directly.

Use one of the two patterns below depending on the transaction strategy validated in the plan.

**Pattern A — No transaction** (reads, single-table writes):

```typescript
import { Injectable } from '@nestjs/common';

import { Ok, Err, Result } from '@idf-subventionjeunes-web/commons-domains';
import type { MyDomainViewInterface } from '@idf-subventionjeunes-web/my-domain-domains';

import { CreateMyDomainCommand } from '../commands/create-my-domain.command';
import { UnknownMyDomainError } from '../errors/unknown-my-domain.error';
import { MyDomainSqlMappers } from '../infrastructure/sql/my-domain.mappers';
import { MyDomainSqlRepository } from '../infrastructure/sql/my-domain.repository';

@Injectable()
export class MyDomainService {
  constructor(private readonly repository: MyDomainSqlRepository) {}

  async findOne(id: string): Promise<Result<UnknownMyDomainError, MyDomainViewInterface>> {
    const entity = await this.repository.findById(id);
    if (!entity) return Err(new UnknownMyDomainError(id));
    return Ok(MyDomainSqlMappers.toMyDomainView(entity));
  }

  async create(command: CreateMyDomainCommand): Promise<Result<never, MyDomainViewInterface>> {
    const entity = await this.repository.save({ name: command.name });
    return Ok(MyDomainSqlMappers.toMyDomainView(entity));
  }
}
```

**Pattern B — Transaction** (multi-table atomic writes):

The repository must accept an `EntityManager` so it can participate in the caller-owned transaction.

```typescript
import { Injectable } from '@nestjs/common';

import { Ok, Err, Result } from '@idf-subventionjeunes-web/commons-domains';
import type { MyDomainViewInterface } from '@idf-subventionjeunes-web/my-domain-domains';
import { DataSource } from 'typeorm';

import { CreateMyDomainCommand } from '../commands/create-my-domain.command';
import { UnknownMyDomainError } from '../errors/unknown-my-domain.error';
import { MyDomainSqlMappers } from '../infrastructure/sql/my-domain.mappers';
import { MyDomainSqlRepository } from '../infrastructure/sql/my-domain.repository';
import { OtherSqlRepository } from '../infrastructure/sql/other.repository';

@Injectable()
export class MyDomainService {
  constructor(
    private readonly dataSource: DataSource,
    private readonly repository: MyDomainSqlRepository,
    private readonly otherRepository: OtherSqlRepository,
  ) {}

  async create(command: CreateMyDomainCommand): Promise<Result<UnknownMyDomainError, MyDomainViewInterface>> {
    return this.dataSource.transaction(async (manager) => {
      const entity = await this.repository.create(manager, { name: command.name });
      await this.otherRepository.doSomething(manager, entity.id);
      return Ok(MyDomainSqlMappers.toMyDomainView(entity));
    });
  }
}
```

In Pattern B the repository write method accepts an `EntityManager` as first argument:

```typescript
async create(manager: EntityManager, data: Omit<MyDomainEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<MyDomainEntity> {
  const result = await manager.insert(MyDomainEntity, data);
  return manager.findOneOrFail(MyDomainEntity, { where: { id: result.identifiers[0].id } });
}
```

Key rules:

- Return `Result<E, A>` using `Ok(value)` / `Err(error)` — error type first, value type second
- Never `throw` in services for business errors — use `Err(new SomeDomainError())`
- **No transaction by default** — reads and single-table writes call the repository directly; wrapping them in a transaction adds lock overhead and WAL writes for no benefit
- **Use `DataSource.transaction()` only** when multiple tables must be written atomically; the service injects `DataSource` and passes an `EntityManager` to repositories
- Read `apps/idf-young-documentation/docs/coding-standards/result-pattern.md` for the full reference: `Result<E, A>` type, `Ok`/`Err` constructors, `Result.async`, `Result.collect`, and the definitive table of where `throw` is and is not acceptable

### Layer 5 — Controller

Location: `libs/{d}/{d}-api/src/controllers/{d}.controller.ts`

```typescript
import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ApiCreatedResponse, ApiOkResponse, ApiTags, ApiBadRequestResponse } from '@nestjs/swagger';

import { Authorizations, RealmPolicy, AgentPolicy, REALM_AGENT, ROLE_AGENT_ADMIN, HttpMappers } from '@idf-subventionjeunes-web/commons-api';
import { isErr } from '@idf-subventionjeunes-web/commons-domains';
import { plainToInstance } from 'class-transformer';

import { CreateMyDomainCommand } from '../commands/create-my-domain.command';
import { MyDomainService } from '../services/my-domain.service';
import { MyDomainView } from '../views/my-domain.view';

@ApiTags('my-domain')
@Controller('my-domain')
export class MyDomainController {
  constructor(private readonly myDomainService: MyDomainService) {}

  @Post()
  @Authorizations(new RealmPolicy([REALM_AGENT]), new AgentPolicy([ROLE_AGENT_ADMIN]))
  @ApiCreatedResponse({ type: MyDomainView })
  @ApiBadRequestResponse()
  async create(@Body() command: CreateMyDomainCommand): Promise<MyDomainView> {
    const result = await this.myDomainService.create(command);
    if (isErr(result)) throw HttpMappers.toNestError(result.failure);
    return plainToInstance(MyDomainView, result.success, { excludeExtraneousValues: true });
  }

  @Get()
  @Authorizations(new RealmPolicy([REALM_AGENT]), new AgentPolicy([ROLE_AGENT_ADMIN]))
  @ApiOkResponse({ type: [MyDomainView] })
  async search(@Query() query: SearchMyDomainQuery): Promise<MyDomainView[]> {
    const result = await this.myDomainService.search(query);
    if (isErr(result)) throw HttpMappers.toNestError(result.failure);
    return plainToInstance(MyDomainView, result.success, { excludeExtraneousValues: true });
  }
}
```

Tell the user:

> "Le controller ne gère **pas** le périmètre transactionnel — il appelle le service et unwrappe le `Result`. La gestion de la transaction appartient au service (voir Layer 4).
>
> ⚠️ Tu verras `transaction.read(this.datasource)(...)` dans de nombreux controllers existants — c'est de la dette connue. Ne pas reproduire ce pattern. Voir [`transaction-wrapper.md`](apps/idf-young-documentation/docs/technical-limitations/major-issues/transaction-wrapper.md)."

Authorization policy reference:

| Audience   | Realm constant  | Role policy                                |
| ---------- | --------------- | ------------------------------------------ |
| Agents IDF | `REALM_AGENT`   | `new AgentPolicy([ROLE_AGENT_ADMIN, ...])` |
| Young      | `REALM_YOUNG`   | `new YoungPolicy()`                        |
| Partners   | `REALM_PARTNER` | `new PartnerPolicy()`                      |

Non-CRUD custom routes must be prefixed with `__`:

```typescript
@Post('__import')
@Post('__validate')
```

**RGPD rule:** any endpoint that exposes or mutates personal data (name, email, IBAN, date of birth,
identity document, address) **must** have `@Authorizations()`. Never use `@OptionalAuth()` on such
endpoints without an explicit security justification reviewed by the TL.

### Layer 6 — Feature module

Location: `libs/{d}/{d}-api/src/{d}-feature.module.ts`

**Always use `ConfigurableModuleBuilder`**, even if the module has no options yet. This keeps every
module consistently configurable and avoids a breaking refactor later.

The builder is always isolated in a separate `*-feature.options.ts` file:

```typescript
// my-domain-feature.options.ts
import { ConfigurableModuleBuilder } from '@nestjs/common';

// If the module has no options yet, use an empty interface:
export interface MyDomainModuleOptions {}

export const { ConfigurableModuleClass, MODULE_OPTIONS_TOKEN } = new ConfigurableModuleBuilder<MyDomainModuleOptions>().build();
```

```typescript
// my-domain-feature.module.ts
import { Module } from '@nestjs/common';

import { MyDomainController } from './controllers/my-domain.controller';
import { MyDomainSqlRepository } from './infrastructure/sql/my-domain.repository';
import { ConfigurableModuleClass } from './my-domain-feature.options';
import { MyDomainService } from './services/my-domain.service';

@Module({
  controllers: [MyDomainController],
  providers: [MyDomainService, MyDomainSqlRepository],
  exports: [MyDomainService],
})
export class MyDomainFeatureModule extends ConfigurableModuleClass {}
```

Add `@Global()` **only** if the module's services must be available across all other modules without
explicit imports (rare — check with the TL).

Create a `*-feature.options.ts` for every new feature module, even if it has no options yet — use an empty interface.

### Layer 7 — Registration in app.module.ts

Location: `apps/idf-young-api/src/app/app.module.ts`

**Simple module** (no external config):

```typescript
import { MyDomainFeatureModule } from '@idf-subventionjeunes-web/my-domain-api';

// Add to the imports array:
MyDomainFeatureModule,
```

**Module with config:**

```typescript
MyDomainFeatureModule.registerAsync({
  imports: [ConfigurationModule],
  useFactory: (config: ConfigurationService) => ({
    someKey: config.get('SOME_ENV_VAR'),
  }),
  inject: [ConfigurationService],
}),
```

Also update `tsconfig.base.json` paths if this is a brand-new Nx library (new `{domain}-api`,
`{domain}-domain`, `{domain}-ui` libs).

### Layer 8 — UI (if in scope)

**Determine the audience first.** If ambiguous, ask the user before generating any UI file.

**Agents / partners back-office (react-admin + MUI):**

Location: `libs/{d}/{d}-ui/src/components/`

Standard files: `List{D}.tsx`, `Create{D}.tsx`, `Edit{D}.tsx`, `{D}Form.tsx`

```tsx
import { Datagrid, DateField, List, TextField } from 'react-admin';

import { EnhancedList } from '@idf-subventionjeunes-web/commons-ui';
import { Container } from '@mui/material';

export const ListMyDomain = () => (
  <Container>
    <EnhancedList sort={{ field: 'updatedAt', order: 'DESC' }} exporter={false}>
      <Datagrid rowClick="edit" size="medium">
        <TextField source="name" sortable={false} />
        <DateField source="createdAt" />
      </Datagrid>
    </EnhancedList>
  </Container>
);
```

**Young persons' UI (Next.js + MUI + Tailwind):**

Location: `libs/young/young-ui/src/` or the relevant young-facing lib.
Follow existing page/component patterns already present in that directory.

### Layer 9 — Unit tests

Location: `libs/{d}/{d}-api/src/services/{d}.service.spec.ts`

```typescript
import { Test, TestingModule } from '@nestjs/testing';

import { createMock } from '@golevelup/ts-jest';

import { MyDomainSqlRepository } from '../infrastructure/sql/my-domain.repository';
import { MyDomainService } from './my-domain.service';

describe('MyDomainService', () => {
  let service: MyDomainService;
  let repository: jest.Mocked<MyDomainSqlRepository>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [MyDomainService],
    })
      .useMocker(createMock)
      .compile();

    service = module.get<MyDomainService>(MyDomainService);
    repository = module.get(MyDomainSqlRepository);
  });

  afterEach(() => jest.restoreAllMocks());

  describe('create', () => {
    describe('Happy path', () => {
      it('should create and return the entity view', async () => {
        // Arrange
        repository.save.mockResolvedValue({ id: 'uuid-1', name: 'Test', createdAt: new Date(), updatedAt: new Date(), archivedAt: null });
        // Act
        const result = await service.create({ name: 'Test' });
        // Assert
        expect(isErr(result)).toBe(false);
      });
    });

    describe('Error path', () => {
      it('should return Err when ...', async () => {
        // Add relevant error cases from the ticket's AC
      });
    });
  });
});
```

Generate one describe block per service method. Derive error test cases from the ticket's
acceptance criteria and Definition of Done.

---

## Step 4 — TypeORM migration (only when entity is created or modified)

**Never write migration files by hand.** Always use the CLI.

### Step 4.1 — Register the entity

Make sure the new or modified entity is listed in the `entities` array in
`libs/databases/young-db/src/main.ts`. If it is missing, add it before building.

### Step 4.2 — Build `young-db`

```bash
pnpm exec nx build young-db
```

This must succeed before the migration can be generated.

### Step 4.3 — Generate the migration

```bash
pnpm exec nx run young-db:generate-migration --args="--name=AddShortDescription"
```

Replace `AddShortDescription` with a PascalCase description of the change
(e.g. `AddGrantsTable`, `AddArchivedAtToOffers`). TypeORM uses this name as the migration class name — kebab-case is not valid here.

### Step 4.4 — Review

Show the generated migration file to the user. Ask them to review it before continuing.
A generated migration that creates or alters a column on existing data must be checked carefully
for nullable defaults and data compatibility.

---

## New domain checklist

When a domain does not already exist in `libs/`, the following must also be created:

⚠️ **Do not use `nx g` to create libs.** Nx generators do not produce the structure expected by this project. **Copy an existing lib** (e.g. `libs/tips/`) as a starting point, then adapt the names in `project.json`, `tsconfig.json` and `src/index.ts`.

- [ ] `libs/{d}/{d}-domain/` — copy from an existing `-domain` lib, adapt `project.json`, `tsconfig.json`, `src/index.ts`
- [ ] `libs/{d}/{d}-api/` — copy from an existing `-api` lib, adapt names
- [ ] `libs/{d}/{d}-ui/` (if UI is in scope) — copy from an existing `-ui` lib, adapt names
- [ ] Path aliases in `tsconfig.base.json` for each new library
- [ ] ⚠️ Notify the user that **TL validation is recommended before merging** a new domain:

> "⚠️ Ce ticket crée un nouveau domaine (`{domain}`). Les choix d'architecture (découpage, nommage, relations) ont un impact long terme. Une validation du TL est recommandée avant de merger vers `main`."

The skill creates the domain anyway — this is a warning, not a blocker.

---

## Step 5 — Automated check loop

Once all layers from the plan are implemented, run the `check-work` skill automatically
on all files created or modified during this session.

### How the loop works

1. Load `.claude/skills/check-work/SKILL.md` and execute it on the implementation scope.
2. If the report contains **Must** findings:
   a. **Architecture violations** (layer separation, EntitySchema, framework imports in domain)
   and **result-pattern violations** (unexpected `throw`, missing `isErr` guard): fix
   automatically without asking for confirmation — these have a single correct answer.
   b. **Must findings that imply a design decision** (e.g. a missing migration on a newly
   added column, or a missing test that requires understanding the intent): present the
   finding to the user and ask for a decision before writing anything.
3. After each round of corrections, re-run `check-work` on the updated files.
4. **Repeat until 0 Must findings, up to a maximum of 3 iterations.**
5. If Must findings remain after 3 iterations, stop and present them to the user:
   > "⚠️ Après 3 passes, les findings suivants n'ont pas pu être résolus automatiquement. Décision necessaire :"
   > [list the unresolved Must findings]

### Output

Once the loop exits cleanly (0 Must findings or user decision received), present the final report:

```
### Rapport check-work final

| Critère AC | Statut | Notes |
|------------|--------|-------|
| [AC1]      | ✅     | ...   |
| [AC2]      | ⚠️     | ...   |

**Must : 0 | Should : N | Could : N**
```

List any remaining Should/Could items the user may want to address.
Then suggest triggering the `create-pr` skill to open the pull request.

---

## Rules

- Never write code before the plan is validated by the user (Step 2).
- Always use `EntitySchema<T>` — never `@Entity()` class decorators.
- Never add `@Injectable()` or `@Module()` in a `-domain/` library.
- Every endpoint touching personal data (name, email, IBAN, DOB, identity document, address)
  must have `@Authorizations()`. Omitting it is a blocker, not a warning.
- Non-CRUD routes must be prefixed with `__`.
- No PII in logs, error messages, or exception objects — ever.
- Migrations are always CLI-generated, never hand-written.
- New domains require a TL warning — but the skill creates them regardless.
- **Never `transaction.read/write` in a controller** — this is known debt, do not reproduce it. Transaction scope belongs to the service (`DataSource.transaction()`).
- If the source is a Jira ticket and the `jira-read` skill returns an error or the Jira MCP is unavailable, ask the user to paste the ticket content manually.

## Golden rules

- Show the plan, wait for "go", then build.
- One layer at a time, confirm as you go.
- Detect the audience — if unsure, ask.
- The domain layer has zero NestJS framework code.
- Migrations are tools, not code you write.
- A new domain is an architectural decision — flag it, don't block on it.
- Transactions (`DataSource.transaction()`) belong to the **service**, never the controller. Do not reproduce the `transaction.read/write` pattern — it is known debt.
