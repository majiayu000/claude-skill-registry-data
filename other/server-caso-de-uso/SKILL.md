---
name: server-caso-de-uso
description: Como escrever um caso de uso em server/src/domain/use-cases — interface XInput, classe com um único execute, injeção pela porta (inclusive portas de serviço e AuthEventLogger), ownership check que vira 404, "agora" lido uma vez, e onde cada validação mora. Use ao criar ou alterar qualquer arquivo .use-case.ts.
---

# Caso de uso

## Quando usar esta skill

Ao criar ou alterar `server/src/domain/use-cases/<agregado>/<verbo>-<agregado>.use-case.ts`.

## Onde o código mora

Uma pasta por agregado, um arquivo por verbo:

```
domain/use-cases/
  expense-category/      create · delete · get · list-expense-categories · update
  fixed-revenue/         create · delete · get · list-fixed-revenues · terminate · update
  installment-expense/   create · delete · get · list-installment-expenses · terminate · update
  one-time-expense/      create · delete · list-one-time-expenses · update
  one-time-revenue/      create · delete · list-one-time-revenues · update
  recurring-expense/     create · delete · get · list-recurring-expenses · terminate · update
  user/                  get-user
  data-import/           import-entries
  auth/                  register-with-password · login-with-password · start-session ·
                         refresh-session · revoke-session · revoke-all-sessions · authenticate-request
```

Verbos usados: `create`, `get`, `list`, `update`, `terminate`, `delete`. Listagem pluraliza no nome
do arquivo e da classe (`list-one-time-revenues.use-case.ts` → `ListOneTimeRevenuesUseCase`).
A pasta `auth/` não é um agregado: os nomes descrevem a ação (`RegisterWithPasswordUseCase`,
`StartSessionUseCase`, …). O antigo `create-user.use-case.ts` **foi removido** — usuário só nasce
pelo cadastro com senha.

## Anatomia canônica — create

`domain/use-cases/one-time-revenue/create-one-time-revenue.use-case.ts`:

```ts
export interface CreateOneTimeRevenueInput {
  userId: string;
  description: string;
  amount: number;
  competenceMonth: number;
  competenceYear: number;
}

export class CreateOneTimeRevenueUseCase {
  constructor(private readonly repository: OneTimeRevenueRepository) {}

  public async execute(input: CreateOneTimeRevenueInput): Promise<OneTimeRevenue> {
    const competence = MonthlyCompetence.create(input.competenceMonth, input.competenceYear);

    if (competence.isPastMonth()) {
      throw new PastCompetenceError();
    }

    const revenue = OneTimeRevenue.create({
      userId: input.userId,
      description: input.description,
      amount: input.amount,
      competenceMonth: input.competenceMonth,
      competenceYear: input.competenceYear,
    });

    return this.repository.create(revenue);
  }
}
```

## Anatomia canônica — update com ownership e cross-agregado

`domain/use-cases/installment-expense/update-installment-expense.use-case.ts`:

```ts
export interface UpdateInstallmentExpenseInput {
  id: string;
  userId: string;
  description?: string;
  categoryId?: string;
}

export interface InstallmentExpenseDetails {
  expense: InstallmentExpense;
  installments: Installment[];
}

export class UpdateInstallmentExpenseUseCase {
  public constructor(
    private readonly installmentExpenseRepository: InstallmentExpenseRepository,
    private readonly categoryRepository: ExpenseCategoryRepository,
  ) {}

  public async execute(input: UpdateInstallmentExpenseInput): Promise<InstallmentExpenseDetails> {
    const expense = await this.installmentExpenseRepository.findById(input.id);

    if (!expense || expense.userId !== input.userId) {
      throw new InstallmentExpenseNotFoundError(input.id);
    }

    if (input.categoryId !== undefined) {
      const category = await this.categoryRepository.findById(input.categoryId);
      if (!category || category.userId !== input.userId) {
        throw new ExpenseCategoryNotFoundError(input.categoryId);
      }
    }

    const updatedExpense = expense.updateDetails({
      description: input.description,
      categoryId: input.categoryId,
    });

    const persistedExpense = await this.installmentExpenseRepository.update(updatedExpense);
    const installments = await this.installmentExpenseRepository.findInstallmentsByExpense(
      persistedExpense.id,
    );

    return { expense: persistedExpense, installments };
  }
}
```

## Anatomia canônica — autenticação (portas de serviço, log e "agora")

`domain/use-cases/auth/register-with-password.use-case.ts` (arquivo completo):

```ts
import { User } from "@src/domain/entities/user.entity";
import { PasswordCredential } from "@src/domain/entities/password-credential.entity";
import { EmailAlreadyExistsError } from "@src/domain/errors/domain-error";
import { PasswordHasher } from "@src/domain/ports/password-hasher";
import { UserRepository } from "@src/domain/ports/user.repository";
import { PasswordPolicy } from "@src/domain/value-objects/password-policy.value-object";
import { AuthEventLogger } from "@src/domain/ports/auth-event-logger";

export interface RegisterWithPasswordInput {
  name: string;
  email: string;
  password: string;
}

export class RegisterWithPasswordUseCase {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly passwordHasher: PasswordHasher,
    private readonly logger: AuthEventLogger,
  ) {}

  public async execute(input: RegisterWithPasswordInput): Promise<User> {
    PasswordPolicy.assert(input.password);
    const user = User.create({ name: input.name, email: input.email });

    // Falha rápida antes de pagar o Argon2; a corrida entre dois cadastros é resolvida pelo
    // índice único, que o repositório traduz para o mesmo erro.
    const existingUser = await this.userRepository.findByEmail(user.email);
    if (existingUser) {
      throw new EmailAlreadyExistsError(user.email);
    }

    const hash = await this.passwordHasher.hash(input.password);
    const credential = PasswordCredential.create({
      userId: user.id,
      passwordHash: hash.hash,
      pepperId: hash.pepperId,
      createdAt: user.createdAt,
      updatedAt: user.createdAt,
    });

    const created = await this.userRepository.createWithPasswordCredential(user, credential);
    this.logger.info("auth.register", { userId: created.id });
    return created;
  }
}
```

E o início do `execute` de `refresh-session.use-case.ts`, que mostra "agora" lido **uma vez** e
repassado a todo predicado, fábrica e escrita:

```ts
public async execute(input: RefreshSessionInput): Promise<SessionTokens> {
  const now = new Date();
  if (!input.refreshToken) {
    throw new InvalidRefreshTokenError();
  }

  const tokenHash = this.refreshTokenGenerator.hash(input.refreshToken);
  const found = await this.sessionRepository.findTokenByHash(tokenHash);
  if (!found || !found.session.isActive(now)) {
    throw new InvalidRefreshTokenError();
  }
```

Regras específicas da fatia de auth:

- Dependências externas além do banco entram por **portas de serviço** de `domain/ports/`
  (`PasswordHasher`, `AccessTokenService`, `RefreshTokenGenerator`) — nunca `argon2`/`jose`/`crypto`
  direto.
- Evento de segurança é logado **no caso de uso**, pela porta `AuthEventLogger` (campo `logger`),
  com nome `auth.<evento>` (`auth.register`, `auth.login.succeeded`/`failed`,
  `auth.password.rehashed`/`rehash_failed`, `auth.refresh.conflict`,
  `auth.refresh.reuse_detected` em `warn`, `auth.session.revoked`). O contexto leva **só
  identificadores** (`userId`, `sessionId`, `reason`, `authMethod`, `pepperId`): nunca senha,
  hash, token nem o e-mail digitado.
- Durações chegam como `SessionPolicy` em **milissegundos** (declarada em
  `start-session.use-case.ts`; o container converte os segundos de `authConfig.session`). Use
  `Pick<SessionPolicy, …>` quando só parte interessa.
- Login: todo caminho executa exatamente um Argon2 (`verify` ou `verifyAgainstDummy` para usuário
  inexistente) e todo fracasso é o mesmo `InvalidCredentialsError`. O rehash depois do login é
  **tolerante a falha** (loga `auth.password.rehash_failed` e o login segue).
- O CAS (`rotate`) é do repositório; o caso de uso decide entre renovar, conflito (dentro da
  janela, `RefreshTokenConflictError`) ou reuso (revoga a família + `warn`). Se o CAS perde,
  **relê** o token para distinguir a aba vizinha de reuso.
- Operação idempotente sem alvo (logout sem sessão) retorna em silêncio, sem lançar.

## Anatomia canônica — list com filtro opcional

```ts
public async execute(input: ListOneTimeRevenuesInput): Promise<OneTimeRevenue[]> {
  if (input.competenceYear !== undefined && input.competenceMonth !== undefined) {
    return this.repository.findByUserAndCompetence(
      input.userId,
      input.competenceYear,
      input.competenceMonth,
    );
  }
  return this.repository.findAllByUser(input.userId);
}
```

## Regras

1. **Um `export interface XUseCaseInput`** por arquivo, nomeado como a classe sem o sufixo `UseCase`
   - `Input` (`CreateOneTimeRevenueUseCase` → `CreateOneTimeRevenueInput`).
2. **Uma classe com exatamente um método público: `public async execute(input): Promise<...>`.**
   Sempre `async`, sempre recebendo **um único objeto** de input.
3. **A saída é entidade de domínio, array de entidades, um valor de domínio ou `void` — nunca
   DTO.** Quando o retorno agrega filhos ou não é entidade, declare uma segunda interface exportada
   ao lado do input (`InstallmentExpenseDetails`, `RecurringExpenseDetails`,
   `InstallmentExpenseWithInstallments`, `SessionTokens`). `AuthenticateRequestUseCase` devolve
   `AccessTokenClaims | null` — `null` em qualquer falha, sem dizer o motivo.
4. **Dependências entram pelo construtor tipadas pela porta**, nunca pela classe concreta.
   Nome do campo: `repository` quando há uma só; por papel quando há várias
   (`installmentExpenseRepository`, `categoryRepository`, `sessionRepository`,
   `passwordHasher`, `logger`). Configuração (ex.: `policy: SessionPolicy`) também entra pelo
   construtor, já convertida — o caso de uso nunca lê `env`.
   Métodos `private` auxiliares são aceitos (`rehash`, `rejectRotated`, `resolveSession`); o que
   não pode é um segundo método **público**.
5. **Ownership check é a primeira regra de negócio**, sempre neste idioma:
   ```ts
   const x = await this.repository.findById(input.id);
   if (!x || x.userId !== input.userId) {
     throw new XNotFoundError(input.id);
   }
   ```
   Acesso de outro usuário vira **404, nunca 403**.
6. **Validação cross-agregado** (a categoria existe e é do usuário?) fica aqui, antes de construir
   a entidade.
7. **Divisão de responsabilidade de validação**: forma/formato → entidade (`Entity.create`);
   regra temporal e cross-agregado → caso de uso.
8. Escrita composta faz **re-leitura** para devolver o estado canônico
   (`findInstallmentsByExpense(persisted.id)`, `findVersions(created.id)`).
9. "Agora" é um `new Date()` local ao `execute`, **lido uma vez** no topo e passado a todas as
   regras do domínio (predicados, fábricas e o repositório) — duas leituras podem cair em lados
   diferentes de uma borda (`expiresAt`, janela de graça). Não existe abstração de relógio: os
   testes usam `vi.useFakeTimers()`/`vi.setSystemTime`. O mês corrente sai de `MonthlyCompetence.current(referenceDate)` (UTC), nunca de
   `getUTCFullYear()`/`getUTCMonth()` no caso de uso:
   ```ts
   const referenceDate = new Date();
   if (!InstallmentExpense.hasFutureInstallments(allInstallments, referenceDate)) {
     throw new NoFutureInstallmentsError();
   }
   const current = MonthlyCompetence.current(referenceDate);
   ```
   **A regra que recusa a ação é um predicado da entidade** (`hasPastInstallments`,
   `hasFutureInstallments`, `isExpiredAt`), e o service usa o **mesmo** predicado para projetar
   `canDelete`/`canTerminate`/`isExpired` no DTO — assim a interface nunca oferece o que o caso de
   uso recusaria. Não reescreva a regra no service nem consulte o repositório para ela.
10. Nada de `@injectable()`/`@inject()` — o projeto **não usa decorators**. A fiação é manual no
    `container.ts` (skill `server-di-container`).

## Checklist para criar um caso de uso

- [ ] Arquivo em `domain/use-cases/<agregado>/<verbo>-<agregado>.use-case.ts`.
- [ ] `export interface XInput` com `userId` e, para operações sobre um item, `id` (os de auth
      que ainda não têm dono — register, login, refresh — recebem as credenciais/token).
- [ ] Construtor recebendo portas com `private readonly`.
- [ ] `public async execute(input)` único, devolvendo entidade.
- [ ] Ownership check antes de qualquer outra regra.
- [ ] Regras de tempo via `MonthlyCompetence` (ou `now` lido uma vez), lançando erro do catálogo.
- [ ] Evento de segurança logado pela porta `AuthEventLogger`, só com identificadores.
- [ ] Re-leitura quando a escrita envolve filhos.
- [ ] Registrado no `container.ts` e injetado no service.
- [ ] Teste unitário com dublês `vi.fn()` das portas (skill `server-testes`).

## Não faça

- Não retorne DTO nem chame `.toISOString()` aqui — isso é do service.
- Não adicione um segundo método público (`executeAll`, helpers) — extraia para outro use case.
- Não acesse o Prisma nem o Express diretamente.
- Não lance 403 para recurso de outro usuário.
- Não use decorators do tsyringe.
- Não chame `new Date()` mais de uma vez no mesmo `execute` para a mesma decisão.
- Não importe `application/ports/logger.interface.ts` no domínio: use `AuthEventLogger`.
- Não diferencie "e-mail inexistente" de "senha errada" (resposta, tempo ou log com o e-mail).

## Inconsistências conhecidas

- `InstallmentExpenseDetails` e `RecurringExpenseDetails` estão **duplicadas** em vários arquivos de
  use case da mesma pasta. Ao criar um agregado novo, declare a interface uma vez e importe do
  arquivo onde nasceu (é o que `delete-one-time-revenue.use-case.ts` já faz com os erros).
- `LoginWithPasswordUseCase.rehash`, `RevokeSessionUseCase` e `RevokeAllSessionsUseCase` chamam
  `new Date()` no ponto de uso (uma única leitura cada, então não violam a regra 9).
- Os casos de uso de auth usam `constructor` sem `public`; as fatias de despesa usam
  `public constructor`. Ambos convivem.
- Ordem de argumento de competência varia entre portas (`(userId, year, month)` vs
  `(id, month, year)`). Para métodos novos, use **`(…, year, month)`**.
