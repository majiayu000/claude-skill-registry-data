---
name: server-repositorio
description: Como escrever a porta de repositório em domain/ports e o repositório Prisma em infrastructure/database/repositories no server do Smaug — mapper toDomain com tipo estrutural inline (ou XRecord do domínio), orderBy explícito, filtro OR de competência, $transaction e compare-and-set com updateMany + P2002.
---

# Porta e repositório

## Quando usar esta skill

Ao criar/alterar `server/src/domain/ports/*.repository.ts` ou
`server/src/infrastructure/database/repositories/prisma-*.repository.ts`.

As portas de **serviço** de autenticação (`password-hasher.ts`, `access-token-service.ts`,
`refresh-token-generator.ts`, `auth-event-logger.ts`) também moram em `domain/ports/`, mas não são
repositório: ver "Portas que não são repositório" no fim.

## Porta — `domain/ports/<agregado>.repository.ts`

```ts
import { OneTimeRevenue } from "@src/domain/entities/one-time-revenue.entity";

export interface OneTimeRevenueRepository {
  findById(id: string): Promise<OneTimeRevenue | null>;
  findAllByUser(userId: string): Promise<OneTimeRevenue[]>;
  findByUserAndCompetence(
    userId: string,
    competenceYear: number,
    competenceMonth: number,
  ): Promise<OneTimeRevenue[]>;
  create(revenue: OneTimeRevenue): Promise<OneTimeRevenue>;
  update(revenue: OneTimeRevenue): Promise<OneTimeRevenue>;
  delete(id: string): Promise<void>;
}
```

Regras da porta:

1. **Interface**, nunca classe abstrata. Nome `<Agregado>Repository`, **sem prefixo `I`**.
2. Devolve **entidades de domínio**, jamais linha do Prisma.
3. Todo método devolve `Promise`. Busca de um item devolve `T | null` — **não lança, não usa `undefined`**.
4. `update(entity)` recebe a **entidade inteira** (já atualizada por copy-on-write), não um patch.
5. Escrita composta passa os filhos explicitamente:
   `create(expense: InstallmentExpense, installments: Installment[])`.
6. Vocabulário de método em uso: `findById`, `findAllByUser` / `listByUser`,
   `findByUserAndCompetence`, `findActiveForCompetence`, `findByCategoryId`, `findByIdWithVersions`,
   `create`, `update`, `delete`, `terminate`, `addVersion`, `findVersions`, `findVersionForMonth`,
   `countLinkedExpenses`, `deleteFutureInstallments`,
   `findInstallmentsByExpense`, `findInstallmentsByCompetence`; na autenticação, `findByEmail`,
   `findByUserId`, `createWithPasswordCredential`, `findSessionById`, `findTokenByHash`, `rotate`,
   `revokeSession`, `revokeAllForUser`, `deleteStaleForUser`.
   O `UserRepository` **não tem mais `create`**: usuário só nasce junto com a credencial
   (`createWithPasswordCredential(user, credential)`).
7. Escrita que pode perder corrida devolve `Promise<boolean>` (`rotate`: `false` = outra
   requisição chegou antes) em vez de lançar; conflito de unicidade que tem significado de negócio
   vira o `DomainError` correspondente **dentro do repositório** (`EmailAlreadyExistsError`).
8. "Agora" chega por parâmetro (`now: Date`) quando a escrita depende do tempo — o repositório não
   chama `new Date()` para regra (ver `server-caso-de-uso`).
9. JSDoc só quando o nome não basta, e **em português**:
   `/** Quantidade de despesas (avulsas, parceladas e versões de recorrentes) ligadas à categoria. */`

## Repositório Prisma — `infrastructure/database/repositories/prisma-<agregado>.repository.ts`

```ts
import { PrismaClient } from "@prisma/client";
import { OneTimeRevenue } from "@src/domain/entities/one-time-revenue.entity";
import { OneTimeRevenueRepository } from "@src/domain/ports/one-time-revenue.repository";

export class PrismaOneTimeRevenueRepository implements OneTimeRevenueRepository {
  constructor(private readonly prisma: PrismaClient) {}

  public async findById(id: string): Promise<OneTimeRevenue | null> {
    const record = await this.prisma.oneTimeRevenue.findUnique({ where: { id } });
    if (!record) return null;
    return PrismaOneTimeRevenueRepository.toDomain(record);
  }

  public async findAllByUser(userId: string): Promise<OneTimeRevenue[]> {
    const records = await this.prisma.oneTimeRevenue.findMany({
      where: { userId },
      orderBy: [{ competenceYear: "desc" }, { competenceMonth: "desc" }, { createdAt: "desc" }],
    });
    return records.map(PrismaOneTimeRevenueRepository.toDomain);
  }

  public async update(revenue: OneTimeRevenue): Promise<OneTimeRevenue> {
    const record = await this.prisma.oneTimeRevenue.update({
      where: { id: revenue.id },
      data: {
        description: revenue.description,
        amount: revenue.amount,
        updatedAt: revenue.updatedAt,
      },
    });
    return PrismaOneTimeRevenueRepository.toDomain(record);
  }

  private static toDomain(record: {
    id: string;
    userId: string;
    description: string;
    amount: number;
    competenceMonth: number;
    competenceYear: number;
    createdAt: Date;
    updatedAt: Date;
  }): OneTimeRevenue {
    return OneTimeRevenue.create({
      id: record.id,
      userId: record.userId,
      description: record.description,
      amount: record.amount,
      competenceMonth: record.competenceMonth,
      competenceYear: record.competenceYear,
      createdAt: record.createdAt,
      updatedAt: record.updatedAt,
    });
  }
}
```

## Regras do repositório

1. `export class Prisma<Agregado>Repository implements <Agregado>Repository`. **Sem `@injectable()`** —
   o projeto não usa decorators.
2. `constructor(private readonly prisma: PrismaClient) {}` — o client é **injetado**, nunca importado
   como singleton dentro do repositório.
3. Todos os métodos públicos são `public async` e devolvem entidade.
4. **O mapper linha→entidade é `private static to…`**, chamado como `Classe.toDomain(record)` ou
   passado point-free em `.map(Classe.toDomain)` (funciona por ser `static`).
   - Um agregado por arquivo → `toDomain`.
   - Vários → `toExpenseDomain` / `toInstallmentDomain` / `toVersionDomain` / `toRevenueDomain`.
   - Sentido inverso (entidade→linha) → `private static toVersionData(...)`.
5. **O parâmetro `record` é tipado com um objeto estrutural inline**, nunca com o tipo gerado do
   Prisma. É isso que mantém o domínio livre de Prisma e faz a regra `no-domain-to-infra` valer na
   prática.
6. `create` lista **todas** as colunas explicitamente (inclusive `id`, `createdAt`, `updatedAt`, que
   vêm da entidade); `update` lista **apenas as colunas mutáveis** + `updatedAt`.
7. `orderBy` é sempre explícito em consultas de lista — tipicamente
   `[{ competenceYear: "desc" }, { competenceMonth: "desc" }, { createdAt: "desc" }]`.
8. Reconstrução usa `Entity.create({ ...record })`. Exceções, que usam `Entity.rehydrate(record)`:
   `RecurringExpense` e `RecurringExpenseVersion` (o `create()` rejeita competência passada) e
   `AuthSession` / `RefreshToken` (a fábrica — `start`/`issue` — calcula datas a partir de "agora"
   e não reconstrói uma linha). Para essas duas, o `record` é tipado com a interface
   **`AuthSessionRecord` / `RefreshTokenRecord` exportada pela entidade**, em que `status`,
   `authMethod` e `revokedReason` são `string` (o schema não usa enum): a linha do Prisma satisfaz
   o tipo estruturalmente, e é o `rehydrate` que valida e estreita para a união fechada.
9. Filtro "a partir de uma competência" usa o idioma `OR`:
   ```ts
   OR: [{ competenceYear: { gt: year } }, { competenceYear: year, competenceMonth: { gt: month } }];
   ```
10. Filtrar por dono através de relação: `installmentExpense: { userId }`.
11. Escrita composta: `create` aninhado + `include` ordenado
    (`installments: { create: installments.map(...) }` / `include: { installments: { orderBy: [{ installmentNumber: "asc" }] } }`).
    Atualização em lote: `this.prisma.$transaction(items.map((i) => this.prisma.installment.update({ ... })))`.
12. Filtrar em memória é aceitável quando a regra vive na entidade:
    `records.map(toExpenseDomain).filter((e) => e.isActiveForMonth(month, year))`.
13. Escrita em várias tabelas que precisa ser atômica usa `$transaction` **interativa**
    (`async (tx) => { … }`), como `createWithPasswordCredential` (usuário + credencial) e
    `revokeSession` (sessão **antes** dos tokens — a mesma ordem do `rotate`, para não haver
    deadlock).
14. **Compare-and-set**: `updateMany` com o estado esperado no `where`, conferindo `count`. Se não
    casou, lance um erro-sentinela privado para desfazer a transação e traduza para `false`; um
    `P2002` (UNIQUE de `parent_token_id`) também vira `false`. Trecho de
    `prisma-auth-session.repository.ts`:

    ```ts
    /** Sinal interno de `rotate`: um compare-and-set não casou e a transação precisa ser desfeita. */
    class RotationLostError extends Error {}

    public async rotate(currentTokenId: string, next: RefreshToken, now: Date): Promise<boolean> {
      try {
        await this.prisma.$transaction(async (tx) => {
          const session = await tx.authSession.updateMany({
            where: { id: next.sessionId, status: "ACTIVE", expiresAt: { gt: now } },
            data: { lastUsedAt: now },
          });
          if (session.count !== 1) throw new RotationLostError();

          const current = await tx.refreshToken.updateMany({
            where: {
              id: currentTokenId,
              sessionId: next.sessionId,
              status: "ACTIVE",
              expiresAt: { gt: now },
            },
            data: { status: "ROTATED", rotatedAt: now },
          });
          if (current.count !== 1) throw new RotationLostError();

          await tx.refreshToken.create({
            data: {
              ...PrismaAuthSessionRepository.toTokenData(next),
              sessionId: next.sessionId,
              parentTokenId: currentTokenId,
            },
          });
        });
        return true;
      } catch (error) {
        if (
          error instanceof RotationLostError ||
          PrismaAuthSessionRepository.isUniqueViolation(error)
        ) {
          return false;
        }
        throw error;
      }
    }
    ```

15. **P2002 com significado de negócio**: o `meta` do erro muda por driver adapter (o SQLite
    informa as colunas, o PostgreSQL o nome do índice), então a detecção procura o nome da coluna
    no `meta` serializado. De `prisma-user.repository.ts`:

    ```ts
    private static isEmailConflict(error: unknown): boolean {
      return (
        error instanceof Prisma.PrismaClientKnownRequestError &&
        error.code === "P2002" &&
        `${JSON.stringify(error.meta)}`.includes("email")
      );
    }
    ```

## Checklist

- [ ] Porta em `domain/ports/`, devolvendo entidades e `T | null`.
- [ ] Classe Prisma `implements` a porta, com `PrismaClient` injetado.
- [ ] `private static toDomain(record: { ...inline... })`.
- [ ] `orderBy` explícito em toda lista.
- [ ] `create` com todas as colunas; `update` só com as mutáveis.
- [ ] `$transaction` para escrita em lote.
- [ ] Registrado no `container.ts` com a variável **anotada pelo tipo da porta**.
- [ ] Teste do repositório: unitário (client dublado) em
      `tests/unit/infrastructure/database/repositories/`, ou — quando o comportamento depende do
      banco de verdade (transação, CAS, UNIQUE) — integração com SQLite próprio em
      `tests/integration/infrastructure/database/repositories/` (como os de auth). Concorrência
      roda nos dois providers: `prisma-auth-session.concurrency.test.ts` liga o PostgreSQL quando
      há `POSTGRES_TEST_DATABASE_URL` (job `migrations` do CI, com client postgresql).

## Não faça

- Não importe `@prisma/client` fora de `infrastructure/`.
- Não tipe o `record` com `Prisma.OneTimeRevenueGetPayload<...>` nem com o model gerado.
- Não use `@injectable()`.
- Não faça `prisma.$queryRaw` de regra de negócio — a regra vive no domínio.
- Não devolva `undefined` de um `findById`; devolva `null`.
- Não faça "ler, conferir e depois gravar" fora de transação para regra de concorrência: use o
  compare-and-set com `updateMany` + `count`.
- Não deixe o `P2002` de uma unicidade de negócio vazar como erro cru (viraria 500).

## Contexto adicional

`domain/ports/repository.interface.ts` (`Repository<T, ID>`) e
`infrastructure/database/database.provider.ts` (`RepositoryFactory`, `PrismaRepository<T>`,
`InMemoryRepository<T>`) são o caminho **genérico legado**, usado só pelo switch de
`DATABASE_PROVIDER`. **Nenhum agregado os utiliza** — não os use para código novo.

## Portas que não são repositório

A autenticação precisa de serviços externos além de persistência. As portas ficam em
`domain/ports/` **sem** sufixo `.repository` e são implementadas por adapters em
`infrastructure/auth/` (os únicos que podem importar `argon2`/`jose` — regra
`auth-crypto-only-in-infra`):

| Porta (`domain/ports/`)      | Interface               | Adapter (`infrastructure/auth/`)                     |
| ---------------------------- | ----------------------- | ---------------------------------------------------- |
| `password-hasher.ts`         | `PasswordHasher`        | `Argon2PasswordHasher` (`argon2-password-hasher.ts`) |
| `access-token-service.ts`    | `AccessTokenService`    | `JoseAccessTokenService`                             |
| `refresh-token-generator.ts` | `RefreshTokenGenerator` | `CryptoRefreshTokenGenerator`                        |
| `auth-event-logger.ts`       | `AuthEventLogger`       | nenhum: o `Logger` de `application/ports` satisfaz   |

`AuthEventLogger` é a porta mínima de log que o domínio enxerga (o domínio não pode importar
`application/ports/logger.interface.ts`); o container passa o próprio `Logger`, que a satisfaz
estruturalmente. Os adapters recebem a fatia de `authConfig` pelo construtor e **não leem `env`**.
