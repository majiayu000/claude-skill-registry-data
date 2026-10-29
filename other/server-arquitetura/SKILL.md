---
name: server-arquitetura
description: Arquitetura do backend Smaug (server/) — camadas Clean Architecture, regra de dependência, alias @src, nomenclatura de arquivos e o roteiro end-to-end para adicionar um agregado novo. Leia antes de criar qualquer arquivo em server/src.
---

# Arquitetura do server

## Quando usar esta skill

Ao adicionar um recurso novo ao backend, ao mover código entre camadas, ou sempre que a dúvida
for "em que pasta isso vai".

## Camadas

```
server/src/
  domain/          entities, value-objects, use-cases, ports (repositórios e serviços de auth), errors
  application/     services (orquestram use cases), dtos (Zod + response), ports (Logger), csv
  infrastructure/  repositórios Prisma, adapters de auth (argon2/jose/crypto), servidor Express,
                   container, env + authConfig (Zod), Pino
  presentation/    controllers, routes, middlewares (authenticate, origem, rate limit, validação, log, erro)
```

Regras de dependência (validadas por `.dependency-cruiser.js`, severidade `error`):

- **`domain` e `application` nunca importam `infrastructure` nem `presentation`.**
- `auth-crypto-only-in-infra`: `argon2` e `jose` só são importados em `server/src/infrastructure/`
  (ficam atrás das portas `PasswordHasher`/`AccessTokenService`).
- `http-middleware-libs-only-in-presentation`: `cookie-parser` e `express-rate-limit` só são
  importados em `server/src/presentation/`.

**Furo conhecido**: o `.dependency-cruiser.js` não tem `options.tsConfig`, então o depcruise **não
resolve o alias `@src/*`** — e todo import de `server/src` é por alias. As regras de camada
(`no-domain-to-infra`, `no-application-to-infra`) na prática não pegam esses imports; só as regras
que miram `node_modules/` (as duas de auth acima) funcionam de verdade. Não conte com o
`validate:deps` para flagrar um `domain → infrastructure`: a disciplina é sua e da revisão.

Fluxo de uma requisição:

```
route → middleware (authenticate, validateRequest) → controller → service → use case → port → repositório Prisma
                                                                                   ↓
                                                                          entidade de domínio
```

O domínio não conhece Express, Prisma nem Zod. `MonthlyCompetence`, entidades e use cases usam só
tipos nativos do TypeScript (princípio III da constituição).

## Convenções de arquivo e import

**Nomes**: kebab-case + sufixo de papel.

| Papel              | Arquivo                                 | Classe/função                        |
| ------------------ | --------------------------------------- | ------------------------------------ |
| Entidade           | `one-time-revenue.entity.ts`            | `OneTimeRevenue`                     |
| Value object       | `monthly-competence.value-object.ts`    | `MonthlyCompetence`                  |
| Porta              | `one-time-revenue.repository.ts`        | `interface OneTimeRevenueRepository` |
| Repositório Prisma | `prisma-one-time-revenue.repository.ts` | `PrismaOneTimeRevenueRepository`     |
| Caso de uso        | `create-one-time-revenue.use-case.ts`   | `CreateOneTimeRevenueUseCase`        |
| Service            | `one-time-revenue.service.ts`           | `OneTimeRevenueService`              |
| DTO                | `one-time-revenue.dto.ts`               | schemas + tipos                      |
| Controller         | `one-time-revenue.controller.ts`        | `OneTimeRevenueController`           |
| Rotas              | `one-time-revenue.routes.ts`            | `createOneTimeRevenueRoutes()`       |
| Middleware         | `authenticate.middleware.ts`            | `authenticate()` (factory)           |
| Porta de serviço   | `password-hasher.ts` (sem sufixo)       | `interface PasswordHasher`           |
| Adapter            | `argon2-password-hasher.ts`             | `Argon2PasswordHasher`               |

Casos de uso de listagem pluralizam: `list-one-time-revenues.use-case.ts` →
`ListOneTimeRevenuesUseCase`.

**Imports**: sempre pelo alias `@src/*`. Não existe **nenhum** import relativo em `server/src/`.

```ts
import { OneTimeRevenue } from "@src/domain/entities/one-time-revenue.entity";
```

**Sufixo `.ts` no import**: `allowImportingTsExtensions` está ligado, mas o sufixo só aparece nos
16 arquivos de bootstrap/infraestrutura (`main.ts`, `container.ts`, `config/env.ts`,
`http/server.ts`, `logging/logger.ts`, `database/config.ts`, `database.provider.ts`,
`in-memory.repository.ts`, os três adapters de `infrastructure/auth/`, `routes/index.ts`,
`health.controller.ts`, e os middlewares de log, erro e rate limit). Em código de feature,
**importe sem extensão**. Na dúvida, copie o vizinho do mesmo arquivo.

**Barris**: só existe um — `presentation/routes/index.ts`. Não crie outros.

## Anatomia de um agregado (gabarito: `recurring-expense`)

Uma fatia completa tem exatamente estes arquivos:

```
domain/entities/recurring-expense.entity.ts
domain/entities/recurring-expense-version.entity.ts
domain/ports/recurring-expense.repository.ts
domain/use-cases/recurring-expense/{create,get,list-recurring-expenses,update,terminate,delete}-recurring-expense.use-case.ts
domain/errors/domain-error.ts                        (os erros novos entram aqui)
application/dtos/recurring-expense.dto.ts
application/services/recurring-expense.service.ts
infrastructure/database/repositories/prisma-recurring-expense.repository.ts
presentation/controllers/recurring-expense.controller.ts
presentation/routes/recurring-expense.routes.ts
infrastructure/config/container.ts                   (a fatia é acrescentada)
presentation/routes/index.ts                         (a montagem é acrescentada)
tests/unit/... espelhando cada arquivo acima + tests/integration/presentation/recurring-expense.test.ts
```

A fatia de autenticação foge do gabarito em três pontos, porque o que ela precisa de fora não é
só persistência: portas de **serviço** em `domain/ports/` sem sufixo `.repository`
(`password-hasher.ts`, `access-token-service.ts`, `refresh-token-generator.ts`,
`auth-event-logger.ts`), os adapters correspondentes em `infrastructure/auth/`, e a configuração
tipada `authConfig` (`infrastructure/config/auth-config.ts`, exportada por `env.ts`) que o
container injeta nos adapters e no HTTP — **nenhum adapter lê `env`**.

## Checklist — adicionar um agregado novo, na ordem

1. **Prisma**: modelo em `server/prisma/schema.prisma` + migration nos dois dialetos
   (`npm run --prefix server migrate:new -- <nome>`, depois `migrate:deploy` aplica; não existe
   script de seed).
2. **Entidade** (e entidade de versão, se o agregado for versionado) — skill `server-entidade-dominio`.
3. **Erros** de domínio no catálogo — skill `server-erros-dominio`.
4. **Porta** em `domain/ports/` — skill `server-repositorio`.
5. **Casos de uso**, um arquivo por verbo — skill `server-caso-de-uso`.
6. **DTO** (schemas Zod + `XResponseDto`) — skill `server-servico-dto`.
7. **Service** orquestrando os use cases e mapeando para DTO — mesma skill.
8. **Repositório Prisma** implementando a porta — skill `server-repositorio`.
9. **Controller** + **rotas** — skill `server-http`.
10. **Container**: acrescente a fatia e exporte o controller — skill `server-di-container`.
11. **`routes/index.ts`**: monte o sub-router **antes** dos catch-alls `/revenues` e `/expenses`.
12. **Testes**: unit espelhando cada arquivo + um arquivo de integração — skill `server-testes`.
13. **Frontend**: se houver código de erro novo, acrescente à tabela de `web/infra/api-error.ts`.
14. `npm run validate:deps && npm run --prefix server typecheck && npm run --prefix server test`.

## Contrato HTTP

Rotas montadas na raiz, **sem prefixo `/api`** (o `/api` existe só no web, que repassa para a API
pelo route handler `web/app/api/[...path]/route.ts`):

```
/health                    aberta, 200 ou 503 com status "degraded"
/auth                      aberta: register, login, refresh, logout, logout-all (este exige Bearer)
/users                     \  GET /users/me
/expenses/categories        |
/expenses/one-time          |
/expenses/installment       |  atrás de authenticate(authenticateRequestUseCase):
/expenses/recurring         |  Authorization: Bearer <access token> → req.userId/req.sessionId
/revenues/one-time          |
/revenues/fixed             |
/data                      /
/revenues                  catch-all de consulta — DEPOIS dos específicos (também autenticado)
/expenses                  catch-all de consulta — DEPOIS dos específicos (também autenticado)
```

Um único `authenticateMiddleware` é criado em `routes/index.ts` e reaproveitado nas montagens.
O sub-router de `/auth` liga `cookieParser()` e `requireTrustedOrigin(env.CORS_ORIGIN)` só para
si, e recebe os rate limiters (`createAuthRateLimiters`) e os dois middlewares de autenticação por
opções.

## Ambiente

`infrastructure/config/env.ts` chama `dotenv.config()`, faz `safeParse` no import e chama
`process.exit(1)` se falhar. Obrigatórias sem default: `DATABASE_PROVIDER`
(`postgresql|sqlite|memory`), `DATABASE_URL`, `NODE_ENV`, e as de autenticação `JWT_SECRET`,
`JWT_KEY_ID`, `PASSWORD_PEPPERS` (`id:base64,…`), `PASSWORD_PEPPER_CURRENT_ID`; `TRUST_PROXY` é
obrigatória fora de `development`/`test` (`"true"` é recusado). Com default: `PORT` (3000),
`LOG_LEVEL` (`info`), `CORS_ORIGIN` (`http://localhost:3001`, normalizado sem barra final), os TTLs
(`ACCESS_TOKEN_TTL_SECONDS` 600, `REFRESH_TOKEN_TTL_SECONDS` 604800,
`SESSION_MAX_LIFETIME_SECONDS` 2592000, `REFRESH_REUSE_GRACE_SECONDS` 30), o custo do Argon2
(`ARGON2_MEMORY_KIB`/`TIME_COST`/`PARALLELISM`, com pisos OWASP fora de `test`), o cookie
(`AUTH_COOKIE_SECURE`, ligado fora de dev/test; `AUTH_COOKIE_PATH` `/api/auth`) e os
`AUTH_RATE_LIMIT_*`. As regras entre variáveis ficam em `checkAuthEnv` (`auth-config.ts`), e
`env.ts` exporta também `authConfig` (`buildAuthConfig(env)`), a configuração já montada que o
container injeta. Lista comentada em `server/.env.example`.

## Não faça

- Não importe `infrastructure`/`presentation` a partir de `domain` ou `application`.
- Não use tipo gerado do Prisma, tipo do Express ou schema do Zod dentro de `domain/`.
- Não crie barril novo (`index.ts` de re-export).
- Não use import relativo em `server/src/`.
- Não instancie service/repositório fora do `container.ts`.
- Não leia `env` dentro de adapter, use case ou middleware: receba a fatia de `authConfig` pelo
  construtor/factory.
- Não importe `argon2`/`jose` fora de `infrastructure/` nem `cookie-parser`/`express-rate-limit`
  fora de `presentation/`.
