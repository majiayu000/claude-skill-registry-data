---
name: server-testes
description: Como escrever testes do server do Smaug — unit espelhando src, títulos em inglês it("should …"), dublês vi.fn das portas, describeControllerContract (com successBody/decorateResponse) para controllers, e integração com SQLite próprio + Supertest + Bearer obtido em POST /auth/register, Argon2 mínimo, relógio falso × exp do JWT e vi.mock("dotenv") nos testes sensíveis a env. Cobertura exigida 100%.
---

# Testes do server

## Quando usar esta skill

Ao escrever qualquer teste em `server/tests/`.

## Estrutura

`server/tests/unit/` **espelha `server/src/` 1:1**, e o nome do arquivo é o do fonte + `.test.ts`:

```
tests/
  helpers/       controller-contract.ts · http-mocks.ts · repository-mocks.ts · setup.ts ·
                 sqlite-test-database.ts · auth-session-fixtures.ts
  integration/
    presentation/                              um arquivo por recurso (+ auth*.test.ts)
    infrastructure/database/repositories/      repositórios que dependem do banco real (auth)
  unit/
    application/{csv,dtos,services}/
    domain/{entities,errors,use-cases/<agregado>,value-objects}/
    infrastructure/{auth,config,database,database/repositories,http,logging}/
    presentation/{controllers,middlewares}/
```

Config: `server/vitest.config.ts` (o único do pacote). Alias `@src`, `environment: "node"`,
`globals: true`, cobertura **100/100/100/100** com `src/**/ports/**` excluído (são interfaces).
O `test.env` do config fixa os **segredos de teste** que o `env.ts` exige no import (`JWT_SECRET`,
`JWT_KEY_ID`, `PASSWORD_PEPPERS`, `PASSWORD_PEPPER_CURRENT_ID`) — o CI não tem `server/.env`.
Os `ARGON2_*` mínimos **não** ficam lá (há testes que importam o `env.ts` com
`NODE_ENV=development`, onde o piso OWASP os recusaria): quem faz hash os fixa no próprio arquivo.
`test:unit` e `test:integration` filtram **por caminho** (`vitest run tests/unit`), não por project.

```bash
npm run --prefix server test               # unit + integração
npm run --prefix server test:unit
npm run --prefix server test:integration
npx vitest run tests/unit/domain/entities/user.entity.test.ts --root server   # arquivo único
```

## Convenções de escrita

1. **Títulos em inglês**: `it("should <verbo> ... when <condição>")`. 969 dos 994 `it` do pacote
   começam com `should`.
2. **`describe` é o nome da classe sob teste, verbatim**: `describe("InstallmentExpense")`,
   `describe("CreateInstallmentExpenseUseCase")`, `describe("authenticate")`.
   Quando um segundo conjunto de casos precisa de outro fixture, abra **um segundo `describe`
   irmão com sufixo** — `describe("InstallmentExpense validation guards")` — em vez de aninhar.
   Aninhamento por método só existe no teste do value object.
3. **Imports nomeados do vitest**, mesmo com `globals: true`:
   ```ts
   import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
   ```
   Fonte via `@src`; helpers por caminho relativo (`../../../../helpers/repository-mocks`).
4. **AAA separado por linha em branco, sem comentários `// Arrange`.** O "act" é uma linha só,
   normalmente atribuída a `const result`.
5. Literais compartilhados viram `const` SCREAMING_SNAKE no módulo:
   ```ts
   const BASE_DATE = new Date("2026-03-01T00:00:00.000Z");
   const USER_ID = "user-1";
   const CATEGORY_ID = "category-1";
   const VALID_UUID = "3f2504e0-4f89-41d3-9a0c-0305e82c3301";
   ```
6. Input válido é um `const validProps = { ... } as const;` (entidade) ou `const input = { ... };`
   (use case) dentro do `describe`, e cada caso **espalha e sobrescreve um campo**:
   `InstallmentExpense.create({ ...validProps, totalAmount: 10.123 })`.
7. Builders locais são consts arrow: `const buildRevenue = (end?: {...}) => FixedRevenue.create({...});`
   Cada arquivo tem as suas fixtures. A única compartilhada é
   `tests/helpers/auth-session-fixtures.ts` (`NOW`, `at(seconds)`, `insertUser(prisma)`,
   `startSession`, `issueToken`), usada pelos testes de repositório de auth.
8. Como o domínio lê `new Date()`, todo teste com data usa o par:

   ```ts
   beforeEach(() => {
     vi.useFakeTimers();
     vi.setSystemTime(BASE_DATE);
   });

   afterEach(() => {
     vi.useRealTimers();
   });
   ```

   e prova o `updatedAt` com `vi.advanceTimersByTime(1)`. Entidades e casos de uso de auth
   recebem `now` por parâmetro: passe datas derivadas de uma constante (`at(30)`) e teste as
   **bordas** (`now == expiresAt`, janela de graça inclusiva).

9. **Argon2 real é lento**: teste de adapter (`argon2-password-hasher.test.ts`) e qualquer
   integração que faça hash usam os parâmetros mínimos (`memoryCost`/`ARGON2_MEMORY_KIB` 1024,
   `timeCost` 1, `parallelism` 1). Use case e service usam dublê do `PasswordHasher`.
10. **Log nunca vaza segredo**: teste que exercita evento `auth.*` asserta que o contexto não tem
    senha, hash, token nem e-mail (`auth-logs.test.ts` captura a saída do Pino com `vi.mock("pino")`).

## Dublês de repositório

Três estilos coexistem; **prefira o (a)** e crie a factory quando ela não existir.

**(a) Factory compartilhada — `tests/helpers/repository-mocks.ts`**

```ts
export type Mocked<T> = {
  [K in keyof T]: T[K] extends (...args: infer A) => infer R ? Mock<(...args: A) => R> : T[K];
};

export function createFixedRevenueRepositoryMock(): Mocked<FixedRevenueRepository> {
  return { findById: vi.fn(), findByIdWithVersions: vi.fn(), ... } as unknown as Mocked<FixedRevenueRepository>;
}
```

Uso — repositório e use case construídos **uma vez no escopo do describe**, resetados por teste:

```ts
const repository = createFixedRevenueRepositoryMock();
const useCase = new TerminateFixedRevenueUseCase(repository);

beforeEach(() => {
  vi.clearAllMocks();
  vi.useFakeTimers();
  vi.setSystemTime(BASE_DATE);
  repository.update.mockImplementation(async (revenue) => revenue);
});
```

Vantagem: o call site fica sem cast — `repository.findById.mockResolvedValue(buildRevenue());`

**(b) Tipo mapeado inline + reconstrução no `beforeEach`** (fatias de despesa). Custa um cast em
cada arranjo: `(categoryRepository.findById as ReturnType<typeof vi.fn>).mockResolvedValue(category)`.

**(c) Objeto literal no escopo do describe** (services e middlewares). Colaborador não exercitado
entra como descartável anônimo: `{ execute: vi.fn() } as unknown as CreateInstallmentExpenseUseCase`.

Outras regras de mock:

- `vi.fn()` por método da porta. **`vi.mock()` de módulo só em `infrastructure/`, `main.test.ts`
  e nos dois casos de integração abaixo**: `vi.mock("dotenv", () => ({ default: { config: vi.fn() } }))`
  quando o teste depende de uma variável **ausente** (ex.: `TRUST_PROXY` em
  `auth-rate-limit.test.ts` — senão o `dotenv.config()` do `env.ts` a repõe do `server/.env`
  local e o teste passa/falha conforme a máquina), e `vi.mock("pino", …)` para capturar log.
- `mockResolvedValue` / `mockRejectedValue` para arranjar; `mockImplementation(async (x) => x)` para
  update pass-through.
- Reset com `vi.clearAllMocks()` no `beforeEach`.
- `vi.spyOn(Classe.prototype as unknown as {...}, "metodoPrivado")` só quando não há outro caminho,
  e sempre com `mockRestore()` explícito ao final.

## Vocabulário de `expect`

| Intenção                 | Idioma                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Primitivo                | `expect(x).toBe(...)` — nunca `toEqual` para escalar                                                          |
| Objeto/array             | `expect(result.expense).toEqual(createdExpense)`                                                              |
| Data                     | `expect(x.createdAt.toISOString()).toBe(BASE_DATE.toISOString())`                                             |
| Throw síncrono           | `expect(() => X.create({...})).toThrow("Amount must have at most 2 decimal places")` — **string da mensagem** |
| Rejeição assíncrona      | `await expect(useCase.execute(input)).rejects.toThrow(ExpenseCategoryNotFoundError)` — **classe**             |
| Efeito colateral ausente | `expect(repository.create).not.toHaveBeenCalled()` — em quase todo caso de erro                               |
| Argumento frouxo         | `expect(repo.create).toHaveBeenCalledWith(expect.any(InstallmentExpense), expect.any(Array))`                 |
| Metadado de erro         | `it("should expose the error codes")` assertando `.code` e `.name`                                            |

## Teste de controller — use `describeControllerContract`

`tests/helpers/controller-contract.ts` gera a bateria padrão. **Um arquivo de teste de controller
não tem `describe`, `it` nem `beforeEach` próprios** — é uma única chamada.

API:

```ts
export interface MethodContract {
  /** Método do controller exercitado. */
  method: string;
  /** Método do service ao qual o controller delega. */
  delegatesTo: string;
  /** Campos do request usados na chamada. */
  request?: Partial<Request>;
  /** Argumentos esperados na chamada ao service. */
  expectedArgs?: unknown[];
  /** Status HTTP do caminho feliz. */
  successStatus: number;
  /** Retorno do service; `undefined` significa resposta sem corpo (`res.send()`). */
  successResult?: unknown;
  /** Corpo esperado quando o controller não devolve o retorno do service inteiro. */
  successBody?: unknown;
  /** Erros de domínio tratados pelo controller e o status que produzem. */
  mappedErrors?: Array<{ error: Error & { code?: string }; status: number }>;
}

export function describeControllerContract(
  title: string,
  setup: () => {
    controller: ControllerMock;
    service: ServiceMock;
    /** Acrescenta ao `res` o que o controller usa além de `status`/`json`/`send` (ex.: `cookie`). */
    decorateResponse?: (res: ResponseMock) => void;
  },
  contracts: MethodContract[],
): void;

export function createServiceMock(methods: string[]): ServiceMock;
```

Uso real (`tests/unit/presentation/controllers/installment-expense.controller.test.ts`):

```ts
const expense = { id: "expense-1", description: "Notebook" };

describeControllerContract(
  "InstallmentExpenseController",
  () => {
    const service = createServiceMock(["create", "get", "list", "update", "terminate", "delete"]);
    return {
      service,
      controller: new InstallmentExpenseController(
        service as unknown as InstallmentExpenseService,
      ) as unknown as ControllerMock,
    };
  },
  [
    {
      method: "create",
      delegatesTo: "create",
      request: { body: { description: "Notebook", totalAmount: 1000 } },
      expectedArgs: ["user-1", { description: "Notebook", totalAmount: 1000 }],
      successStatus: 201,
      successResult: expense,
      mappedErrors: [
        { error: new InstallmentExpensePastStartError(), status: 409 },
        { error: new ExpenseCategoryNotFoundError("cat-1"), status: 404 },
      ],
    },
    {
      method: "delete",
      delegatesTo: "delete",
      request: { params: { id: "expense-1" } },
      expectedArgs: ["user-1", "expense-1"],
      successStatus: 204, // sem successResult ⇒ espera res.send()
      mappedErrors: [
        /* ... */
      ],
    },
  ],
);
```

Ele gera três tipos de teste por contrato: caminho feliz, um por erro mapeado
(`should respond with <status> for <ErrorName>`) e `should forward unexpected errors to next`.
O `"user-1"` de `expectedArgs` vem do `userId` default de `createRequestMock` (e `"session-1"` do
`sessionId` default).

Quando o controller **não devolve o retorno do service inteiro** ou usa mais do que
`status`/`json`/`send` no `res`, use `successBody` e `decorateResponse`. Uso real
(`tests/unit/presentation/controllers/auth.controller.test.ts`):

```ts
const decorateResponse = (res: ResponseMock): void => {
  Object.assign(res, { cookie: vi.fn(() => res), clearCookie: vi.fn(() => res) });
};

describeControllerContract(
  "AuthController",
  () => {
    const service = createServiceMock([
      "register",
      "loginWithPassword",
      "refresh",
      "logout",
      "logoutAll",
    ]);
    return { service, controller: buildController(service), decorateResponse };
  },
  [
    {
      method: "register",
      delegatesTo: "register",
      request: { body: registerBody },
      expectedArgs: [registerBody],
      successStatus: 201,
      successResult: result, // { response, refreshToken, refreshTokenExpiresAt }
      successBody: response, // só o corpo vai no res.json
      mappedErrors: [{ error: new EmailAlreadyExistsError("ana@exemplo.com"), status: 409 }],
    },
    // …
  ],
);
```

O que o contrato não cobre (atributos do cookie, `clearCookie` só no 401, `Max-Age`) vai num
`describe` irmão com sufixo — `describe("AuthController refresh cookie")` — escrito à mão.

Helpers auxiliares em `tests/helpers/http-mocks.ts`: `createResponseMock()` (com `status`/`json`/
`send`/`setHeader` encadeáveis) e `createRequestMock(overrides)` (defaults `params/query/body/headers`
vazios, `method: "GET"`, `originalUrl: "/"`, `userId: "user-1"`, `sessionId: "session-1"`). Em
`tests/helpers/setup.ts`: `withEnv(vars, fn)` para isolar `process.env`.

## Teste de integração

`tests/integration/presentation/<recurso>.test.ts`. **Um arquivo `.db` por arquivo de teste.**
Boilerplate a copiar:

```ts
import type { PrismaClient } from "@prisma/client";
import { sqliteTestDatabase } from "../../helpers/sqlite-test-database";

const testDb = sqliteTestDatabase("installment-expense"); // prisma/sqlite/test-installment-expense.db
const PASSWORD = "correct-horse-battery-staple";

beforeAll(async () => {
  vi.resetModules();

  process.env.DATABASE_PROVIDER = "sqlite";
  process.env.DATABASE_URL = testDb.url;
  process.env.NODE_ENV = "test";
  process.env.PORT = "3000";
  process.env.LOG_LEVEL = "error";
  // Argon2 mínimo: o cadastro do beforeAll faz hash, e o custo de produção só deixaria o teste lento.
  process.env.ARGON2_MEMORY_KIB = "1024";
  process.env.ARGON2_TIME_COST = "1";
  process.env.ARGON2_PARALLELISM = "1";
  process.env.AUTH_RATE_LIMIT_REGISTER_PER_IP = "1000";

  testDb.push();
  prisma = testDb.client();

  const { createHttpServer } = await import("@src/infrastructure/http/server");
  app = createHttpServer();

  const createUserRes = await request(app).post("/auth/register").send({
    name: "Installment User",
    email: "installment-user@example.com",
    password: PASSWORD,
  });
  userId = createUserRes.body.user.id;
  accessToken = createUserRes.body.accessToken;
});
```

O usuário nasce por `POST /auth/register` (senha com 12+ caracteres), que já devolve o access
token: `body.user.id` e `body.accessToken`. `AUTH_RATE_LIMIT_REGISTER_PER_IP` alto evita o 429
quando o arquivo cadastra vários usuários (o limite padrão é 10/h por IP, e todo o Supertest sai do
mesmo IP). Os segredos (`JWT_*`, `PASSWORD_PEPPERS`) já vêm do `test.env` do `vitest.config.ts`.

`sqliteTestDatabase(name)` (`tests/helpers/sqlite-test-database.ts`) devolve `url` (absoluta: CLI,
client do teste e app abrem o mesmo arquivo), `push()` (apaga o arquivo e roda `db push` pelo wrapper
— sem flag de reset, que o CLI do Prisma 7 recusa quando há um agente de IA no ambiente), `client()`
(`PrismaClient` com o mesmo driver adapter da aplicação) e `remove()` (o arquivo e os
`-journal`/`-wal`/`-shm`). O `client()` vem **depois** do `push()`, que apaga o arquivo.

Ordem obrigatória: `vi.resetModules()` → env → `testDb.push()` → **`await import()` dinâmico** do
app (import estático avaliaria o container contra o ambiente de dev) → seed **por HTTP**, nunca via
Prisma.

```ts
afterAll(async () => {
  await prisma.$disconnect();
  testDb.remove();
});

beforeEach(async () => {
  await prisma.installment.deleteMany(); // tabela filha primeiro
  await prisma.installmentExpense.deleteMany();
});
```

Supertest com Bearer:

```ts
const authHeaders = () => ({ Authorization: `Bearer ${accessToken}` });
const res = await request(app).post("/expenses/installment").set(authHeaders()).send({ ... });
expect(res.status).toBe(409);
expect(res.body.error).toBe("NO_FUTURE_INSTALLMENTS");
```

Rotas de `/auth` com cookie: o `Origin` ausente passa pelo `requireTrustedOrigin`; para testar o
403, mande `Origin` diferente do `CORS_ORIGIN`. O refresh vai como `Cookie: smaug_refresh=…`,
extraído do `set-cookie` da resposta anterior.

**Relógio falso × `exp` do JWT.** O access token tem `exp` (padrão 600 s) e a sessão tem vida
máxima (`SESSION_MAX_LIFETIME_SECONDS`). Se o teste emite o token num instante e depois avança o
relógio falso (`vi.setSystemTime(APRIL)`), o token e a sessão expiram e toda chamada vira 401
`UNAUTHORIZED`. Duas saídas: emitir o token **depois** do `vi.setSystemTime`, ou subir os TTLs no
próprio arquivo antes do import do app, como `lancamentos-read-api.test.ts`:

```ts
// O relógio falso salta de março para abril: token e sessão precisam sobreviver ao salto.
process.env.ACCESS_TOKEN_TTL_SECONDS = String(365 * 24 * 60 * 60);
process.env.SESSION_MAX_LIFETIME_SECONDS = String(365 * 24 * 60 * 60);
```

**Teste que depende de variável ausente** (ex.: sem `TRUST_PROXY`) apaga a variável do
`process.env` **e** faz `vi.mock("dotenv", () => ({ default: { config: vi.fn() } }))` no topo
— senão o `dotenv.config()` do `env.ts` a repõe do `server/.env` local. Ver
`auth-rate-limit.test.ts`. Esses arquivos guardam o `process.env` anterior num `previousEnv` e o
restauram no `afterAll`.

Arquivos de integração de auth: `auth.test.ts` (fluxos), `auth-refresh-reuse.test.ts` (janela de
graça e reuso), `auth-rate-limit.test.ts` / `auth-rate-limit-proxy.test.ts` (429 sem e com
`TRUST_PROXY=loopback`), `auth-logs.test.ts` (eventos e redação). Os repositórios de auth têm
testes de integração próprios em `tests/integration/infrastructure/database/repositories/`; o de
concorrência (`prisma-auth-session.concurrency.test.ts`) roda no SQLite quando o client gerado é
SQLite e no PostgreSQL quando há `POSTGRES_TEST_DATABASE_URL` (job `migrations` do CI, com client
postgresql) — com o client errado ele falha alto em vez de pular.

Formato do arquivo: o **primeiro teste é um passeio completo pelo ciclo de vida**
(`"should create, list, get, update, terminate, and delete ..."`), seguido de um teste por código
de erro. Estado dependente de tempo usa `vi.useFakeTimers()` + `vi.setSystemTime(...)` **dentro do
`it`**; linha em competência passada é inserida direto pelo Prisma (contornando a guarda da API),
com `id` explícito e legível (`"installment-no-future-1"`).

Pré-requisito: um client do Prisma já gerado (SQLite). Os arquivos `.db` ficam em
`server/prisma/sqlite/` e são apagados no `afterAll`.

## Checklist

- [ ] Arquivo espelhando o caminho do fonte, com `.test.ts`.
- [ ] `describe` = nome da classe; `it("should …")` em inglês.
- [ ] Imports nomeados do vitest; fonte por `@src`.
- [ ] Fake timers quando houver data.
- [ ] Caso de erro assertando também `not.toHaveBeenCalled()` no repositório.
- [ ] Controller coberto por `describeControllerContract`, não por testes escritos à mão.
- [ ] Integração com `.db` próprio, env de Argon2 mínimo + rate limit alto, import dinâmico do app,
      usuário e token por `POST /auth/register` e seed por HTTP com `Authorization: Bearer`.
- [ ] Relógio falso compatível com o `exp` do token (emitir depois, ou TTLs altos no arquivo).
- [ ] `npm run --prefix server test` verde e cobertura 100% (thresholds falham o run).

## Não faça

- Não escreva teste de controller manualmente quando `describeControllerContract` cobre o caso.
- Não use import estático do app no teste de integração.
- Não compartilhe arquivo `.db` entre arquivos de teste.
- Não semeie dados de integração direto no Prisma quando a API pode criá-los (a exceção é estado
  em competência passada, que a API recusa de propósito).
- Não use `it("deve …")` no server — português é a convenção do `web/` e do `e2e/`.
- Não crie usuário direto no Prisma em teste de rota (a API exige credencial); a exceção são os
  testes de repositório (`insertUser`).
- Não ponha `ARGON2_*` no `test.env` do `vitest.config.ts`.
- Não rode Argon2 com parâmetros de produção em teste.
