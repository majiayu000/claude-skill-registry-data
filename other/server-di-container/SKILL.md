---
name: server-di-container
description: Como registrar dependências no container do server do Smaug (infrastructure/config/container.ts) — fiação manual sem decorators, ritmo de três blocos por fatia, a fatia de auth (adapters com authConfig, SessionPolicy em ms, cookie do controller), tokens string, registerInstance e o bloco export consumido por routes/index.ts.
---

# Container de injeção de dependências

## Quando usar esta skill

Sempre que adicionar um repositório, caso de uso, service ou controller — nenhum deles é instanciado
fora daqui.

## Onde o código mora

`server/src/infrastructure/config/container.ts`. É o **composition root** de todo o backend.

## O ponto mais importante

**O projeto não usa decorators do tsyringe.** `grep -rn "injectable\|@inject(" server/src` retorna
zero. Apesar de `tsyringe` e `reflect-metadata` serem dependências, a fiação é **100% manual** com
`new`, nesse arquivo. O container tsyringe só é realmente resolvido para o token `"Logger"`
(em `main.ts`, nos dois middlewares de log/erro, em `routes/index.ts` para os rate limiters, e no
próprio `container.ts`, logo após o registro, para injetar o logger nos casos de uso de auth).

Portanto: **não escreva `@injectable()` nem `@inject("Token")` em classe nenhuma.**

## Cabeçalho do arquivo

```ts
import "reflect-metadata";
import { container } from "tsyringe";
// ~70 imports agrupados por fatia: repositório → porta → use cases → service → controller

// O singleton de infrastructure/database/config.ts, que monta o driver adapter do provider
// (o Prisma 7 não constrói client sem adapter).
const prismaClient = getPrismaClient();

container.registerInstance<PrismaClient>("PrismaClient", prismaClient);
container.registerSingleton<Logger>("Logger", PinoLogger);
container.register<RepositoryFactory>("RepositoryFactory", { useValue: getRepository });

const logger = container.resolve<Logger>("Logger");
```

Só três APIs do container são usadas: `registerInstance`, `registerSingleton`, `register`.
**Tokens são string literal igual ao nome do tipo** — `"PrismaClient"`, `"Logger"`,
`"OneTimeRevenueService"`, `"InstallmentExpenseController"`. Sem `Symbol`, sem objeto `TOKENS`.

## Anatomia canônica — uma fatia

Ritmo de três blocos, repetido por fatia. Exemplo real (fatia `one-time-revenue` de `container.ts`):

```ts
const oneTimeRevenueRepository: OneTimeRevenueRepository = new PrismaOneTimeRevenueRepository(
  prismaClient,
);
const createOneTimeRevenueUseCase = new CreateOneTimeRevenueUseCase(oneTimeRevenueRepository);
const updateOneTimeRevenueUseCase = new UpdateOneTimeRevenueUseCase(oneTimeRevenueRepository);
const deleteOneTimeRevenueUseCase = new DeleteOneTimeRevenueUseCase(oneTimeRevenueRepository);
const listOneTimeRevenuesUseCase = new ListOneTimeRevenuesUseCase(oneTimeRevenueRepository);
const oneTimeRevenueService = new OneTimeRevenueService(
  createOneTimeRevenueUseCase,
  updateOneTimeRevenueUseCase,
  deleteOneTimeRevenueUseCase,
  listOneTimeRevenuesUseCase,
);
const oneTimeRevenueController = new OneTimeRevenueController(oneTimeRevenueService);

container.registerInstance<OneTimeRevenueRepository>(
  "OneTimeRevenueRepository",
  oneTimeRevenueRepository,
);
container.registerInstance<OneTimeRevenueService>("OneTimeRevenueService", oneTimeRevenueService);
container.registerInstance<OneTimeRevenueController>(
  "OneTimeRevenueController",
  oneTimeRevenueController,
);
```

## Anatomia — a fatia de autenticação

Vem logo depois da fatia `user` (reaproveita `userRepository` e `getUserUseCase`). Ordem: adapters
→ repositórios → `SessionPolicy` → use cases → service → controller. Trecho real de `container.ts`:

```ts
const MS_PER_SECOND = 1000;

const passwordHasher: PasswordHasher = new Argon2PasswordHasher(authConfig.password);
const accessTokenService: AccessTokenService = new JoseAccessTokenService(authConfig.accessToken);
const refreshTokenGenerator: RefreshTokenGenerator = new CryptoRefreshTokenGenerator();
const passwordCredentialRepository: PasswordCredentialRepository =
  new PrismaPasswordCredentialRepository(prismaClient);
const authSessionRepository: AuthSessionRepository = new PrismaAuthSessionRepository(prismaClient);
// O AuthConfig fala em segundos (como o env); os casos de uso, em milissegundos.
const sessionPolicy: SessionPolicy = {
  refreshTokenTtlMs: authConfig.session.refreshTokenTtlSeconds * MS_PER_SECOND,
  maxLifetimeMs: authConfig.session.maxLifetimeSeconds * MS_PER_SECOND,
  reuseGraceMs: authConfig.session.refreshReuseGraceSeconds * MS_PER_SECOND,
};
const registerWithPasswordUseCase = new RegisterWithPasswordUseCase(
  userRepository,
  passwordHasher,
  logger,
);
// … loginWithPassword, startSession, refreshSession, revokeSession, revokeAllSessions
const authenticateRequestUseCase = new AuthenticateRequestUseCase(
  accessTokenService,
  authSessionRepository,
);
const authService = new AuthService(
  registerWithPasswordUseCase,
  loginWithPasswordUseCase,
  startSessionUseCase,
  refreshSessionUseCase,
  revokeSessionUseCase,
  revokeAllSessionsUseCase,
  getUserUseCase,
);
const authController = new AuthController(authService, {
  name: "smaug_refresh",
  ...authConfig.cookie,
});

container.registerInstance<PasswordCredentialRepository>(
  "PasswordCredentialRepository",
  passwordCredentialRepository,
);
container.registerInstance<AuthSessionRepository>("AuthSessionRepository", authSessionRepository);
container.registerInstance<AuthService>("AuthService", authService);
container.registerInstance<AuthController>("AuthController", authController);
```

Pontos da fatia:

- **Adapters também são anotados pelo tipo da porta** (`const passwordHasher: PasswordHasher`),
  como repositórios — e, como casos de uso, **não são registrados** no container.
- Cada adapter recebe **só a sua fatia** de `authConfig` (importado de `env.ts`):
  `authConfig.password`, `authConfig.accessToken`. Nenhum adapter lê `env`.
- A conversão segundos → milissegundos acontece **aqui**, uma vez, no `SessionPolicy`.
- O `logger` (resolvido do container) é passado onde o caso de uso pede `AuthEventLogger`: o
  `Logger` satisfaz a porta estruturalmente.
- O nome do cookie (`"smaug_refresh"`) é literal aqui; `secure` e `path` vêm de
  `authConfig.cookie`. O controller recebe tudo pronto (`RefreshCookieConfig`).

## Regras

1. **A variável do repositório é anotada com o tipo da PORTA**
   (`const xRepository: XRepository = new PrismaXRepository(prismaClient);`). É isso que impede o
   resto do grafo de enxergar a classe do Prisma. Use cases, service e controller têm tipo inferido.
2. Ordem dentro da fatia: repositório → use cases (na ordem create, update/get, delete, list) →
   service → controller.
3. **Só repositório, service e controller são registrados no container.** Casos de uso e
   adapters **nunca** são registrados — eles só existem como const locais. (O
   `authenticateRequestUseCase` é exportado, mas não registrado.)
4. `registerInstance<T>("T", instancia)` para tudo que já foi construído;
   `registerSingleton<Logger>("Logger", PinoLogger)` só para o logger;
   `register<RepositoryFactory>(..., { useValue: getRepository })` só para a factory legada.
5. **A ordem das fatias importa** — uma fatia posterior reutiliza const de uma anterior:
   `PrismaClient/Logger/RepositoryFactory` (+ `const logger`) → `user` → **`auth`** (usa
   `userRepository` e `getUserUseCase`) → `one-time-revenue` → **`expense-category`**
   (necessária para as três fatias de despesa) → `one-time-expense` → `installment-expense` →
   `recurring-expense` → `fixed-revenue` → `revenue-query` → `expense-query` → `data`.
6. O arquivo termina com um bloco `export { ... }` — é isso que `presentation/routes/index.ts`
   importa:
   ```ts
   export {
     container,
     userController,
     authController,
     authenticateRequestUseCase,
     oneTimeRevenueController,
     oneTimeExpenseController,
     installmentExpenseController,
     recurringExpenseController,
     fixedRevenueController,
     fixedRevenueRepository,
     revenueQueryController,
     expenseQueryController,
     expenseCategoryController,
     expenseCategoryRepository,
     dataController,
   };
   ```
   Exporte o **controller** de toda fatia nova. Fora controllers, só sai o que alguma montagem
   precisa: `authenticateRequestUseCase` (o `authenticate`/`authenticateIfPresent` de
   `routes/index.ts` o recebem). O `userRepository` **saiu** do export junto com o antigo
   middleware de identificação por cabeçalho, que foi removido. `fixedRevenueRepository` e
   `expenseCategoryRepository` seguem exportados sem consumidor em `routes/index.ts`.
7. O sufixo `.ts` aparece em parte dos imports deste arquivo (ele é um dos 16 de bootstrap: os
   de `infrastructure/` — logger, database, `env.ts`, adapters de auth — levam `.ts`; os de
   repositório, porta, use case, service e controller, não). Siga o padrão dos vizinhos ao
   acrescentar a fatia.

## Checklist para acrescentar uma fatia

- [ ] Imports da fatia agrupados no topo, na ordem repositório → porta → use cases → service → controller.
- [ ] Bloco de `new` posicionado **depois** de qualquer fatia da qual dependa (ex.: `expense-category`).
- [ ] Repositório (e adapter, se houver) anotado com o tipo da porta.
- [ ] Configuração vinda de `authConfig` (ou equivalente), já convertida para o que o domínio
      espera — nunca `env` lido dentro da classe.
- [ ] Três `registerInstance` (repositório, service, controller).
- [ ] Controller acrescentado ao bloco `export { ... }` final.
- [ ] Montagem correspondente em `presentation/routes/index.ts`.
- [ ] `tests/unit/infrastructure/config/container.test.ts` continua passando.

## Não faça

- Não escreva `@injectable()` / `@inject()`.
- Não registre casos de uso no container.
- Não use `Symbol` nem objeto de tokens.
- Não faça `container.resolve(...)` em controller, service ou caso de uso — a única resolução em
  runtime é `container.resolve<Logger>("Logger")`, no `container.ts`, no `main.ts`, nos dois
  middlewares de log/erro e em `routes/index.ts` (rate limiters).
- Não exporte repositório "por via das dúvidas": rota recebe caso de uso ou controller.
- Não instancie service ou repositório em rota, controller ou teste de integração.

## Um client só

O `container.ts` não constrói `PrismaClient`: usa `getPrismaClient()` de
`infrastructure/database/config.ts`, o mesmo singleton preguiçoso do `/health` e do
`database.provider.ts`. É ali que mora a escolha do driver adapter
(`infrastructure/database/prisma-adapter.ts`). Não construa um `PrismaClient` próprio no container nem em
repositório — no Prisma 7, sem `adapter`, ele nem constrói.
