---
name: server-http
description: Como escrever controllers, rotas e middlewares em server/src/presentation no Smaug — métodos async (req,res,next), req.userId! preenchido pelo authenticate (Bearer), cadeia instanceof mapeando erro de domínio para status, cookie de refresh no AuthController, factory createXRoutes com .bind, validateRequest e ordem de montagem em routes/index.ts.
---

# Camada HTTP: controller, rota e middleware

## Quando usar esta skill

Ao criar/alterar `server/src/presentation/controllers/*.controller.ts`,
`presentation/routes/*.routes.ts` ou `presentation/middlewares/*.middleware.ts`.

## Anatomia canônica — controller

`presentation/controllers/one-time-revenue.controller.ts`:

```ts
import { Request, Response, NextFunction } from "express";
import { OneTimeRevenueService } from "@src/application/services/one-time-revenue.service";
import { PastCompetenceError } from "@src/domain/use-cases/one-time-revenue/create-one-time-revenue.use-case";
import {
  RevenueNotFoundError,
  PastCompetenceEditError,
} from "@src/domain/use-cases/one-time-revenue/update-one-time-revenue.use-case";

export class OneTimeRevenueController {
  constructor(private readonly service: OneTimeRevenueService) {}

  public async create(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const result = await this.service.create(req.userId!, req.body);
      res.status(201).json(result);
    } catch (error) {
      if (error instanceof PastCompetenceError) {
        res.status(409).json({ error: error.code, message: error.message });
        return;
      }
      next(error);
    }
  }

  public async delete(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      await this.service.delete(req.userId!, req.params.id as string);
      res.status(204).send();
    } catch (error) {
      if (error instanceof RevenueNotFoundError) {
        res.status(404).json({ error: error.code, message: error.message });
        return;
      }
      if (error instanceof PastCompetenceEditError) {
        res.status(409).json({ error: error.code, message: error.message });
        return;
      }
      next(error);
    }
  }
}
```

## Regras do controller

1. **Classe com métodos `async` normais — não propriedades arrow.** É por isso que a rota precisa de
   `.bind(controller)`.
2. Assinatura sempre `(req: Request, res: Response, next: NextFunction): Promise<void>`. Nunca
   `return res...`.
3. Uma dependência no construtor, chamada `service` (o `AuthController` recebe também a
   `RefreshCookieConfig` — ver abaixo; o `UserController` ainda chama a sua de `userService`).
4. `req.userId!` com non-null assertion — o campo (e `req.sessionId`) é declarado por module
   augmentation em `authenticate.middleware.ts` e garantido pelo `authenticate` da montagem. É a
   única exceção aceita ao banimento de `!`. `req.sessionId` só é lido pelo `AuthController.logout`,
   **sem** `!`: lá o middleware é o `authenticateIfPresent`, que pode não preenchê-lo.
5. `req.params.id as string` (o Express 5 tipa `params` de forma frouxa).
6. **Mapeamento erro→status é manual, por método**, com cadeia de `if (error instanceof X)`,
   **cada um terminando em `return;`**, e `next(error)` como último recurso (vira 500).
7. Corpo de erro é sempre `{ error: error.code, message: error.message }` — o campo `error` carrega
   o **código**, não o texto humano.
8. Tabela de status:

   | Operação                        | Status                                               |
   | ------------------------------- | ---------------------------------------------------- |
   | create                          | 201 + `res.json(result)`                             |
   | get / list / update / terminate | 200 + `res.json(result)`                             |
   | delete                          | 204 + `res.send()` (sem corpo)                       |
   | erro "não encontrado"           | 404                                                  |
   | violação de regra de negócio    | 409                                                  |
   | body/query inválido             | 400 (vem do `validateRequest`)                       |
   | Bearer ausente/inválido         | 401 `UNAUTHORIZED` (vem do `authenticate`)           |
   | credencial/refresh inválido     | 401 (mapeado no `AuthController`)                    |
   | `Origin` não confiável          | 403 `ORIGIN_NOT_ALLOWED` (`requireTrustedOrigin`)    |
   | limite de tentativas            | 429 `TOO_MANY_REQUESTS` + `Retry-After` (rate limit) |

9. O controller **não** toca em repositório nem em entidade: só service + classes de erro.
10. `health.controller.ts` é a única exceção: função exportada `healthController(_req, res)`,
    devolvendo 200 ou **503 com `status: "degraded"`**. Parâmetro não usado leva prefixo `_`.

## Cookie de refresh — só no `AuthController`

O refresh token anda em cookie, e cookie é detalhe HTTP: o `AuthService` devolve
`{ response, refreshToken, refreshTokenExpiresAt }` sem saber de cookie, e o controller grava/apaga.
Os atributos que variam por ambiente (`name`, `secure`, `path`) chegam **pelo construtor**
(`RefreshCookieConfig`, montada no container a partir de `authConfig.cookie`); nada aqui lê `env`.
Trecho de `presentation/controllers/auth.controller.ts`:

```ts
export class AuthController {
  constructor(
    private readonly service: AuthService,
    private readonly cookie: RefreshCookieConfig,
  ) {}

  public async refresh(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const result = await this.service.refresh(this.readRefreshCookie(req));
      this.setRefreshCookie(res, result);
      res.status(200).json(result.response);
    } catch (error) {
      if (error instanceof InvalidRefreshTokenError) {
        this.clearRefreshCookie(res);
        res.status(401).json({ error: error.code, message: error.message });
        return;
      }
      // Conflito dentro da janela: outra aba já renovou; o cookie novo dela vale, não se apaga nada.
      if (error instanceof RefreshTokenConflictError) {
        res.status(409).json({ error: error.code, message: error.message });
        return;
      }
      next(error);
    }
  }

  private setRefreshCookie(res: Response, result: AuthSessionResult): void {
    res.cookie(this.cookie.name, result.refreshToken, {
      ...this.cookieAttributes(),
      maxAge: Math.max(0, result.refreshTokenExpiresAt.getTime() - Date.now()),
    });
  }

  /** Mesmos atributos da emissão: o navegador só apaga o cookie se `Path` coincidir. */
  private clearRefreshCookie(res: Response): void {
    res.clearCookie(this.cookie.name, this.cookieAttributes());
  }

  private cookieAttributes(): CookieOptions {
    return {
      httpOnly: true,
      secure: this.cookie.secure,
      sameSite: "strict",
      path: this.cookie.path,
    };
  }
}
```

Regras: o cookie (`smaug_refresh`) é sempre `HttpOnly` + `SameSite=Strict` + `Path` + `Max-Age`;
`clearCookie` repete os mesmos atributos; `INVALID_REFRESH_TOKEN` apaga o cookie, já
`REFRESH_TOKEN_CONFLICT` (409) **mantém**; `logout`/`logoutAll` apagam e respondem 204. O corpo de
sucesso de register (201), login e refresh (200) é `{ accessToken, tokenType: "Bearer", expiresIn,
user }` — o refresh token **nunca** vai no corpo.

## Anatomia canônica — rotas

`presentation/routes/one-time-revenue.routes.ts` (arquivo completo):

```ts
import { Router } from "express";
import { OneTimeRevenueController } from "@src/presentation/controllers/one-time-revenue.controller";
import { validateRequest } from "@src/presentation/middlewares/validate-request.middleware";
import {
  createOneTimeRevenueSchema,
  updateOneTimeRevenueSchema,
} from "@src/application/dtos/one-time-revenue.dto";

export function createOneTimeRevenueRoutes(controller: OneTimeRevenueController): Router {
  const router = Router();

  router.post("/", validateRequest(createOneTimeRevenueSchema), controller.create.bind(controller));
  router.get("/", controller.list.bind(controller));
  router.put(
    "/:id",
    validateRequest(updateOneTimeRevenueSchema),
    controller.update.bind(controller),
  );
  router.delete("/:id", controller.delete.bind(controller));

  return router;
}
```

Regras:

1. **Uma factory por feature**: `export function create<Feature>Routes(controller): Router`. Só
   export nomeado, sem `default`.
2. `const router = Router();` → registra → `return router;`.
3. Handler é sempre `controller.<metodo>.bind(controller)`.
4. **Os schemas vêm de `@src/application/dtos/<feature>.dto`**, não são declarados aqui.
5. `validateRequest(schema)` antes de handler de escrita; `validateQuery(schema)` antes de consulta.
   Não há validação de `:id`.
6. Ação de domínio vira sub-rota: `router.post("/:id/terminate", controller.terminate.bind(controller))`.
7. Middleware que depende de configuração ou de outro objeto chega **por parâmetro** da factory,
   não por import do container: `createAuthRoutes(controller, options)` recebe `authenticate`,
   `authenticateIfPresent`, `trustedOrigin` e `rateLimiters` (`AuthRoutesOptions`), e liga
   `cookieParser()` + `requireTrustedOrigin(trustedOrigin)` **só no próprio sub-router**:

   ```ts
   export function createAuthRoutes(
     controller: AuthController,
     options: AuthRoutesOptions,
   ): Router {
     const router = Router();
     const { authenticate, authenticateIfPresent, trustedOrigin, rateLimiters } = options;

     // O cookie de refresh só existe para /auth: o parser fica neste sub-router.
     router.use(cookieParser());
     router.use(requireTrustedOrigin(trustedOrigin));

     router.post(
       "/register",
       rateLimiters.register,
       validateRequest(registerSchema),
       controller.register.bind(controller),
     );
     router.post(
       "/login",
       rateLimiters.loginPerIp,
       rateLimiters.loginPerEmail,
       validateRequest(loginSchema),
       controller.login.bind(controller),
     );
     router.post("/refresh", rateLimiters.refresh, controller.refresh.bind(controller));
     router.post("/logout", authenticateIfPresent, controller.logout.bind(controller));
     router.post("/logout-all", authenticate, controller.logoutAll.bind(controller));

     return router;
   }
   ```

   O rate limiter vem **antes** do `validateRequest` (tentativa inválida também conta).

## `routes/index.ts` — o único barril do projeto

```ts
const router = Router();
const authenticateMiddleware = authenticate(authenticateRequestUseCase);

router.get("/health", healthController);
router.use(
  "/auth",
  createAuthRoutes(authController, {
    authenticate: authenticateMiddleware,
    authenticateIfPresent: authenticateIfPresent(authenticateRequestUseCase),
    trustedOrigin: env.CORS_ORIGIN,
    rateLimiters: createAuthRateLimiters(
      container.resolve<Logger>("Logger"),
      authConfig.rateLimits,
    ),
  }),
);
router.use("/users", authenticateMiddleware, createUserRoutes(userController));
router.use(
  "/expenses/categories",
  authenticateMiddleware,
  createExpenseCategoryRoutes(expenseCategoryController),
);
// … /expenses/one-time, /expenses/installment, /expenses/recurring,
//   /revenues/one-time, /revenues/fixed — todos com authenticateMiddleware
router.use("/data", authenticateMiddleware, createDataRoutes(dataController));
router.use("/revenues", authenticateMiddleware, createRevenueQueryRoutes(revenueQueryController));
router.use("/expenses", authenticateMiddleware, createExpenseQueryRoutes(expenseQueryController));

export default router;
```

**A ordem é funcional, não estética**: `/health` e `/auth` ficam abertos (é por `/auth/register`
que se cria o primeiro usuário; `/auth/logout-all` exige Bearer dentro do próprio sub-router); os
prefixos específicos vêm antes; os catch-alls `/revenues` e `/expenses` **ficam por último**, senão
engolem `/revenues/one-time` e companhia. **Um único** `authenticateMiddleware` é criado no topo e
reaproveitado em todas as montagens protegidas, inclusive `/users` (que hoje só tem
`GET /users/me`). Os controllers e o `authenticateRequestUseCase` são os consts exportados por
`container.ts`.

## Middlewares (`presentation/middlewares/`, os 6)

Todos são **funções exportadas** — sem classe, sem decorator. Dois são handlers diretos
(log e erro), os demais são factories que devolvem um handler.

- **`authenticate.middleware.ts`** — a autenticação do projeto. Duas factories que recebem o
  `AuthenticateRequestUseCase` (não um repositório) e leem `Authorization: Bearer <token>`:
  - `authenticate(useCase)` exige token válido de sessão ativa; qualquer falha vira
    `401 { error: "UNAUTHORIZED", message: "Authentication required" }`, **sem** dizer o motivo
    nem logar o token.
  - `authenticateIfPresent(useCase)` preenche quando há Bearer válido e segue de qualquer forma
    (só o `POST /auth/logout`, que aceita cookie ou token já expirado).

  Declara a module augmentation dos dois campos:

  ```ts
  declare module "express-serve-static-core" {
    interface Request {
      userId?: string;
      sessionId?: string;
    }
  }
  ```

- **`require-trusted-origin.middleware.ts`** — `requireTrustedOrigin(allowedOrigin)`: `Origin`
  diferente de `CORS_ORIGIN` → `403 ORIGIN_NOT_ALLOWED`; `Origin` ausente segue (cliente que não é
  navegador). Só no sub-router `/auth`.
- **`rate-limit.middleware.ts`** — `createAuthRateLimiters(logger, limits)` devolve
  `{ register, loginPerIp, loginPerEmail, refresh }` (express-rate-limit, store em memória, chave
  pelo IP — e por IP + e-mail normalizado no `loginPerEmail`). O 429 segue o formato de erro do
  projeto (`TOO_MANY_REQUESTS`) com `Retry-After`, e loga `auth.rate_limited` em `warn`. O IP só é
  o do cliente com `TRUST_PROXY` configurado (ver `server.ts`).
- **`validate-request.middleware.ts`** — `validateRequest(schema)` e `validateQuery(schema)`.
  Achatam os issues do Zod em `Record<string, string[]>` (chave `issue.path.join(".") || "_root"`)
  e respondem
  `400 { error: "VALIDATION_ERROR", message: "Invalid request body", details: formatted }`.
  `validateRequest` **sobrescreve `req.body = result.data`** (o controller recebe dado já coagido).
- **`request-logger.middleware.ts`** — resolve o `Logger` do container, cronometra com
  `process.hrtime.bigint()` e loga no evento `res.on("finish")`.
- **`error-handler.middleware.ts`** — handler de 4 argumentos, **sempre o último** do app. Loga e
  devolve `500 { error: "Internal Server Error" }`. **Ele não conhece `DomainError`**: toda falha
  que o cliente precisa entender tem que ser mapeada no controller.

Montagem em `infrastructure/http/server.ts` (a ordem importa):

```ts
if (authConfig.trustProxy !== null) {
  app.set("trust proxy", authConfig.trustProxy);
}

app.use(
  cors({
    origin: env.CORS_ORIGIN,
    credentials: true,
    exposedHeaders: ["Content-Disposition"],
  }),
);
app.use(express.json());
app.use(express.text({ type: "text/csv", limit: "5mb" }));
app.use(requestLoggerMiddleware);
app.use(routes);
app.use(errorHandlerMiddleware); // sempre por último
```

O `cookieParser()` **não** é global: fica no sub-router `/auth`, o único que lê cookie.

## Checklist

- [ ] Controller como classe, com métodos `async (req,res,next): Promise<void>`.
- [ ] `req.userId!` e `req.params.id as string`.
- [ ] Cadeia `instanceof` cobrindo **todos** os erros que o service pode lançar, cada um com `return;`.
- [ ] `next(error)` no fim de todo `catch`.
- [ ] Status conforme a tabela; delete devolve 204 com `res.send()`.
- [ ] Rota com factory `create<Feature>Routes(controller)` e `.bind(controller)`.
- [ ] Schemas importados do DTO.
- [ ] Montagem em `routes/index.ts` **antes** dos catch-alls, com o `authenticateMiddleware`
      já existente (não crie outro `authenticate(...)`).
- [ ] Código de erro novo (inclusive de middleware) pareado em `web/infra/api-error.ts`.
- [ ] Teste de controller via `describeControllerContract` (skill `server-testes`).
- [ ] Teste de integração cobrindo cada status (skill `server-testes`).

## Não faça

- Não transforme métodos do controller em propriedades arrow (quebraria o padrão do `.bind`).
- Não declare schema Zod no arquivo de rota.
- Não deixe erro de negócio cair no `errorHandlerMiddleware` — vira 500 genérico.
- Não monte um prefixo novo depois dos catch-alls `/revenues` / `/expenses`.
- Não instancie controller ou service na rota: importe o const do `container.ts`.
- Não leia `env`/`authConfig` dentro de controller ou middleware: receba por construtor ou
  parâmetro de factory (só `routes/index.ts` e `server.ts` leem a configuração).
- Não ponha o refresh token no corpo da resposta, nem cookie fora do `AuthController`.
- Não diferencie o motivo do 401 do `authenticate` (token ausente, expirado, sessão revogada…):
  a resposta é sempre a mesma.
- Não importe `cookie-parser`/`express-rate-limit` fora de `presentation/` (regra
  `http-middleware-libs-only-in-presentation`).

## Inconsistências conhecidas

- **`PUT /:id` nas receitas vs `PATCH /:id` nas despesas.** Para recurso novo, escolha pelo
  semântico (substituição total → `PUT`; parcial → `PATCH`) e mantenha coerente com o
  `web/features/*/services` correspondente, que os testes de service assertam por assinatura.
- O construtor do `UserController` chama a dependência de `userService`, não `service`.
- `AuthController.logout`/`logoutAll` não têm cadeia `instanceof`: a revogação é idempotente e
  não lança erro de domínio.
- `validateQuery` grava `validatedQuery` no request, mas **nenhum controller lê**;
  `ExpenseQueryController` re-parseia `req.query` com o próprio schema. Não replique a dupla
  validação: escolha uma.
