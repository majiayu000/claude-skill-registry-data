---
name: server-erros-dominio
description: Como criar e usar erros de domínio no server do Smaug — DomainError, código SCREAMING_SNAKE, this.name, onde declarar (catálogo vs co-localizado), catálogo dos 33 códigos de domínio + 4 de middleware e o pareamento obrigatório com web/infra/api-error.ts.
---

# Erros de domínio

## Quando usar esta skill

Ao lançar uma falha de regra de negócio, ao criar uma classe de erro nova ou ao mapear um erro
para status HTTP.

## Onde o código mora

- Catálogo compartilhado: `server/src/domain/errors/domain-error.ts` — **é aqui que erro novo entra**.
- Legado co-localizado: no fim do arquivo do caso de uso que lança (fatias `user` —
  `UserNotFoundError` em `get-user.use-case.ts` —, `one-time-revenue`, `fixed-revenue`). Não
  replique esse padrão em código novo. O `EmailAlreadyExistsError` morava em
  `create-user.use-case.ts` (removido) e **foi movido para o catálogo**.

## Anatomia canônica

```ts
export abstract class DomainError extends Error {
  public abstract readonly code: string;
}

export class ExpenseCategoryNotFoundError extends DomainError {
  public readonly code = "EXPENSE_CATEGORY_NOT_FOUND";

  public constructor(categoryId: string) {
    super(`Expense category with id "${categoryId}" not found`);
    this.name = "ExpenseCategoryNotFoundError";
  }
}
```

## Regras

1. Hierarquia de **um nível**: `DomainError extends Error`; toda classe concreta estende
   `DomainError` diretamente.
2. `public readonly code = "SCREAMING_SNAKE";` — **literal inline**. Não existe enum nem mapa de
   constantes, e não crie um.
3. O construtor chama `super(mensagem em inglês)` e em seguida `this.name = "NomeDaClasse";`
   (verbatim, igual ao nome da classe). Os testes assertam `code` e `name`.
4. Identificador na mensagem entre aspas duplas: `` `... with id "${expenseId}" not found` ``.
5. Sem `captureStackTrace`, sem `cause`, sem status HTTP na classe — o status é decidido no
   controller (`server-http`).
6. **Reuse o código antes de criar um novo.** `code` não é único por classe: `PAST_COMPETENCE` é
   compartilhado por 5 classes diferentes, e a mensagem é o que as diferencia.
7. Erro novo com código novo exige, **no mesmo PR**, uma entrada em `web/infra/api-error.ts` — senão
   o usuário vê o texto de fallback genérico.

## Catálogo — códigos já existentes (reuse antes de inventar)

Os 33 códigos distintos de `DomainError` (catálogo + co-localizados):

```
ALREADY_EXPIRED                        EFFECTIVE_DATE_AFTER_END
EFFECTIVE_DATE_BEFORE_START            EFFECTIVE_DATE_OUT_OF_RANGE
EMAIL_ALREADY_EXISTS                   END_DATE_BEFORE_START
EXPENSE_CATEGORY_HAS_LINKED_EXPENSES   EXPENSE_CATEGORY_NAME_ALREADY_EXISTS
EXPENSE_CATEGORY_NOT_FOUND             EXPORT_PERIOD_INVALID
EXPORT_PERIOD_TOO_LONG                 FIXED_REVENUE_NOT_FOUND
IMPORT_EMPTY_FILE                      IMPORT_MISSING_COLUMNS
IMPORT_NO_VALID_ROWS                   INSTALLMENT_EXPENSE_NOT_FOUND
INSTALLMENT_FINANCIAL_IMMUTABLE        INSTALLMENT_HAS_PAST_COMPETENCE
INVALID_CREDENTIALS                    INVALID_REFRESH_TOKEN
NO_FUTURE_INSTALLMENTS                 ONE_TIME_EXPENSE_NOT_FOUND
PAST_COMPETENCE                        PAST_EFFECTIVE_DATE
PAST_START_DATE                        PAST_TERMINATION_DATE
RECURRING_EXPENSE_ALREADY_EXPIRED      RECURRING_EXPENSE_NOT_FOUND
REFRESH_TOKEN_CONFLICT                 REVENUE_NOT_FOUND
UNALTERABLE_REVENUE                    USER_NOT_FOUND
VERSION_CONFLICT
```

Mais quatro códigos emitidos por middleware, que **não** são `DomainError` (o corpo é montado
direto no `res.status(...).json(...)`):

| Código               | Status | Middleware                                               |
| -------------------- | ------ | -------------------------------------------------------- |
| `VALIDATION_ERROR`   | 400    | `validate-request.middleware.ts`                         |
| `UNAUTHORIZED`       | 401    | `authenticate.middleware.ts`                             |
| `ORIGIN_NOT_ALLOWED` | 403    | `require-trusted-origin.middleware.ts`                   |
| `TOO_MANY_REQUESTS`  | 429    | `rate-limit.middleware.ts` (com cabeçalho `Retry-After`) |

Classes do catálogo, na ordem em que aparecem em `domain-error.ts` (27):
`ExpenseCategoryNotFoundError`, `ExpenseCategoryNameAlreadyExistsError`,
`ExpenseCategoryHasLinkedExpensesError`, `OneTimeExpenseNotFoundError`,
`OneTimeExpensePastCompetenceCreateError`, `OneTimeExpensePastCompetenceEditError`,
`OneTimeExpensePastCompetenceDeleteError`, `InstallmentExpenseNotFoundError`,
`InstallmentExpensePastStartError`, `InstallmentFinancialImmutableError`,
`InstallmentHasPastCompetenceError`, `NoFutureInstallmentsError`, `RecurringExpenseNotFoundError`,
`RecurringExpenseAlreadyExpiredError`, `PastCompetenceError`, `PastEffectiveDateError`,
`EffectiveDateOutOfRangeError`, `EndDateBeforeStartError`, `ExportPeriodInvalidError`,
`ExportPeriodTooLongError`, `ImportEmptyFileError`, `ImportMissingColumnsError`,
`ImportNoValidRowsError`, `InvalidCredentialsError`, `InvalidRefreshTokenError`,
`RefreshTokenConflictError`, `EmailAlreadyExistsError`.

Erros de autenticação (todos no catálogo):

| Classe                      | Código                   | Status | Observação                                                        |
| --------------------------- | ------------------------ | ------ | ----------------------------------------------------------------- |
| `EmailAlreadyExistsError`   | `EMAIL_ALREADY_EXISTS`   | 409    | cadastro; também vem do P2002 no `createWithPasswordCredential`   |
| `InvalidCredentialsError`   | `INVALID_CREDENTIALS`    | 401    | mesma resposta para e-mail inexistente e senha errada             |
| `InvalidRefreshTokenError`  | `INVALID_REFRESH_TOKEN`  | 401    | o controller **apaga** o cookie de refresh                        |
| `RefreshTokenConflictError` | `REFRESH_TOKEN_CONFLICT` | 409    | reuso dentro da janela de graça; o controller **mantém** o cookie |

**Pareamento com o web**: `web/infra/api-error.ts` tem uma entrada para **cada um** dos 33 + 4
códigos acima (a tabela `MESSAGES`). As chaves de erro por linha da importação CSV
(`INVALID_COMPETENCE`, `INVALID_AMOUNT`, …) são outra tabela, de outro contrato, e não contam aqui.

## Semântica de status

| Situação                                                                    | Erro                              | Status no controller             |
| --------------------------------------------------------------------------- | --------------------------------- | -------------------------------- |
| Recurso inexistente **ou de outro usuário**                                 | `*NotFoundError`                  | 404                              |
| Regra de negócio violada (competência passada, imutabilidade, já encerrado) | demais                            | 409                              |
| Bearer ausente/inválido, sessão revogada ou expirada                        | `UNAUTHORIZED` (middleware)       | 401                              |
| Credencial ou refresh token inválido                                        | `INVALID_*` (auth)                | 401                              |
| `Origin` não confiável nas rotas `/auth`                                    | `ORIGIN_NOT_ALLOWED` (middleware) | 403                              |
| Rate limit das rotas `/auth`                                                | `TOO_MANY_REQUESTS` (middleware)  | 429 + `Retry-After`              |
| Body/query fora do schema                                                   | `VALIDATION_ERROR` (middleware)   | 400                              |
| Qualquer erro não mapeado                                                   | `Error` cru                       | 500 via `errorHandlerMiddleware` |

Acesso cross-tenant **sempre vira 404**, nunca 403 — é o idioma do projeto (ver `server-caso-de-uso`).

## Checklist para criar um erro novo

- [ ] Verificou que nenhum código existente serve.
- [ ] Classe declarada em `domain/errors/domain-error.ts`, estendendo `DomainError`.
- [ ] `public readonly code = "..."` literal.
- [ ] `super(mensagem em inglês)` + `this.name = "NomeDaClasse";`.
- [ ] Controller mapeia com `if (error instanceof X) { res.status(n).json({ error: error.code, message: error.message }); return; }`.
- [ ] Entrada correspondente em pt-BR na tabela `MESSAGES` de `web/infra/api-error.ts`.
- [ ] Teste em `server/tests/unit/domain/errors/domain-error.test.ts` assertando `code` e `name`.
- [ ] Teste de integração cobrindo o status e `res.body.error`.

## Não faça

- Não crie enum ou mapa `ERROR_CODES` — o projeto usa literal inline.
- Não lance `DomainError` cru; sempre uma subclasse concreta.
- Não coloque status HTTP dentro da classe de erro.
- Não declare erro novo no fim de um use case (padrão legado).
- Não deixe o `errorHandlerMiddleware` "tratar" uma falha esperada: ele só produz 500 genérico.
  Falha que o cliente precisa entender é mapeada explicitamente no controller.

## Inconsistências conhecidas

- **Duas casas para erros**: catálogo vs fim do use case. Código novo vai no catálogo.
- Os erros co-localizados usam `constructor(...)` sem `public`; o catálogo usa `public constructor`.
  Siga o catálogo. Exceção dentro do próprio catálogo: `EmailAlreadyExistsError`, que veio movido
  de `create-user.use-case.ts`, manteve o `constructor` sem `public`.
- `PastEffectiveDateError` existe **duas vezes** (em `domain-error.ts` e em
  `use-cases/fixed-revenue/update-fixed-revenue.use-case.ts`). Ao importar, confira de qual módulo
  o controller correspondente está importando.
- `delete-one-time-revenue.use-case.ts` importa erros do arquivo do **update** — não estranhe, mas
  não copie.
