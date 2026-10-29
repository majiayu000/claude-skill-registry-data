---
name: server-entidade-dominio
description: Como escrever entidades e value objects em server/src/domain — private constructor, static create, campos public readonly, validação interna, update copy-on-write, rehydrate (inclusive com XRecord de strings), "agora" por parâmetro e os value objects MonthlyCompetence, EmailAddress e PasswordPolicy. Use ao criar ou alterar qualquer arquivo .entity.ts ou .value-object.ts.
---

# Entidade de domínio e value object

## Quando usar esta skill

Ao criar ou alterar `server/src/domain/entities/*.entity.ts` e
`server/src/domain/value-objects/*.value-object.ts`.

## Arquivo canônico

`server/src/domain/entities/one-time-revenue.entity.ts` — copie a estrutura dele.

## Anatomia canônica

```ts
import { randomUUID } from "crypto";
import { MonthlyCompetence } from "@src/domain/value-objects/monthly-competence.value-object";

export interface OneTimeRevenueProps {
  id?: string;
  userId: string;
  description: string;
  amount: number;
  competenceMonth: number;
  competenceYear: number;
  createdAt?: Date;
  updatedAt?: Date;
}

const MIN_DESCRIPTION_LENGTH = 1;
const MAX_DESCRIPTION_LENGTH = 255;
const MAX_DECIMAL_PLACES = 2;

export class OneTimeRevenue {
  public readonly id: string;
  public readonly userId: string;
  public readonly description: string;
  public readonly amount: number;
  public readonly competenceMonth: number;
  public readonly competenceYear: number;
  public readonly createdAt: Date;
  public readonly updatedAt: Date;

  private constructor(props: Required<OneTimeRevenueProps>) {
    this.id = props.id;
    this.userId = props.userId;
    this.description = props.description;
    this.amount = props.amount;
    this.competenceMonth = props.competenceMonth;
    this.competenceYear = props.competenceYear;
    this.createdAt = props.createdAt;
    this.updatedAt = props.updatedAt;
  }

  public static create(props: OneTimeRevenueProps): OneTimeRevenue {
    const description = props.description.trim();
    OneTimeRevenue.validateDescription(description);
    OneTimeRevenue.validateAmount(props.amount);

    const competence = MonthlyCompetence.create(props.competenceMonth, props.competenceYear);

    const now = new Date();
    return new OneTimeRevenue({
      id: props.id ?? randomUUID(),
      userId: props.userId,
      description,
      amount: props.amount,
      competenceMonth: competence.month,
      competenceYear: competence.year,
      createdAt: props.createdAt ?? now,
      updatedAt: props.updatedAt ?? now,
    });
  }

  public update(changes: { description?: string; amount?: number }): OneTimeRevenue {
    const newDescription =
      changes.description !== undefined ? changes.description.trim() : this.description;
    const newAmount = changes.amount !== undefined ? changes.amount : this.amount;

    if (changes.description !== undefined) {
      OneTimeRevenue.validateDescription(newDescription);
    }
    if (changes.amount !== undefined) {
      OneTimeRevenue.validateAmount(newAmount);
    }

    return new OneTimeRevenue({
      id: this.id,
      userId: this.userId,
      description: newDescription,
      amount: newAmount,
      competenceMonth: this.competenceMonth,
      competenceYear: this.competenceYear,
      createdAt: this.createdAt,
      updatedAt: new Date(),
    });
  }

  public getCompetence(): MonthlyCompetence {
    return MonthlyCompetence.create(this.competenceMonth, this.competenceYear);
  }

  private static validateAmount(amount: number): void {
    if (amount <= 0) {
      throw new Error("Amount must be greater than 0");
    }
    const decimalStr = amount.toString();
    const decimalIndex = decimalStr.indexOf(".");
    if (decimalIndex !== -1 && decimalStr.length - decimalIndex - 1 > MAX_DECIMAL_PLACES) {
      throw new Error("Amount must have at most 2 decimal places");
    }
  }

  private static validateDescription(description: string): void {
    if (
      description.length < MIN_DESCRIPTION_LENGTH ||
      description.length > MAX_DESCRIPTION_LENGTH
    ) {
      throw new Error("Description must be between 1 and 255 characters");
    }
  }
}
```

## Regras

1. **`export interface XProps`** acima da classe, com `id?`, `createdAt?` e `updatedAt?` opcionais
   e o resto obrigatório.
2. **Números mágicos viram `const` SCREAMING_SNAKE no módulo** (`MAX_DESCRIPTION_LENGTH`,
   `MAX_DECIMAL_PLACES`), nunca literais soltos dentro do método.
3. **Campos `public readonly`** — um por prop. Nunca getters, nunca guardar um objeto `props`.
4. **`private constructor(props: Required<XProps>)`** que só faz atribuição campo a campo. Nada de
   validação no construtor.
5. **`public static create(props: XProps): X` é a fábrica.** Ela normaliza (`trim()`; e-mail
   passa pelo VO `EmailAddress`), valida, resolve `id: props.id ?? randomUUID()` e
   `createdAt: props.createdAt ?? now`. Exceção nomeada: quando nascer a entidade é um **evento
   com tempo** e não "preencher props", a fábrica leva o nome do evento e recebe `now`
   explicitamente — `AuthSession.start(userId, authMethod, now, maxLifetimeMs)` e
   `RefreshToken.issue(session, tokenHash, parentTokenId, now, ttlMs)`, que calculam `expiresAt`
   a partir de `now`. Durações chegam em **milissegundos** (a conversão de segundos do env é do
   caso de uso / `SessionPolicy`).
6. **Validação mora na entidade**, em `private static validateX(...): void`, uma por regra, lançando
   `Error` com mensagem em inglês. Essa mensagem tem que ser **idêntica** à mensagem do schema Zod
   correspondente em `application/dtos/` — os testes assertam a string.
7. **Mutação devolve nova instância.** Nomes usados: `update`, `updateDetails`, `terminate`,
   `clearTermination`, e na autenticação `revoke(reason, now)` e `withNewHash(hash, now)`. Copie
   todos os campos e troque `updatedAt: new Date()` — ou `updatedAt: now` quando o método recebe
   `now` (as entidades de auth sempre recebem). Nunca mutar `this`.
   Predicados que dependem do tempo também recebem `now` por parâmetro, sem default:
   `AuthSession.isActive(now)`, `RefreshToken.isExpired(now)`,
   `RefreshToken.rotatedWithin(graceMs, now)`. Comparação de borda é explícita no JSDoc
   (em `now == expiresAt` já não vale).
8. **`static rehydrate(props)` só quando a fábrica não serve para reconstruir uma linha, e só para
   o repositório.** Existe em `RecurringExpense` e `RecurringExpenseVersion` (o `create()` rejeita
   competência passada) e em `AuthSession` e `RefreshToken` (`start`/`issue` calculam datas a
   partir de "agora"). Em todos os outros agregados o repositório chama
   `Entity.create({ ...record })`.
   Nas duas entidades de auth, o `rehydrate` recebe um **`XRecord`** exportado pela entidade, em que
   as colunas de estado são `string` (o schema não usa enum), e valida/estreita cada uma para a
   união fechada com `validateOneOf`. As uniões nascem de arrays `as const`. De
   `domain/entities/auth-session.entity.ts`:

   ```ts
   export const AUTH_SESSION_STATUSES = ["ACTIVE", "REVOKED"] as const;
   export type AuthSessionStatus = (typeof AUTH_SESSION_STATUSES)[number];

   /**
    * Linha como o banco a devolve: estado, método e motivo são `String` no schema (sem enum) e só
    * viram os tipos fechados depois de validados por `rehydrate`.
    */
   export interface AuthSessionRecord extends Omit<
     AuthSessionPersistenceProps,
     "authMethod" | "status" | "revokedReason"
   > {
     authMethod: string;
     status: string;
     revokedReason: string | null;
   }

   /** Só para o repositório: `start` calcula as datas a partir de "agora" e não reconstrói uma linha. */
   public static rehydrate(record: AuthSessionRecord): AuthSession {
     return new AuthSession({
       ...record,
       authMethod: AuthSession.validateOneOf(record.authMethod, AUTH_METHODS, "auth method"),
       status: AuthSession.validateOneOf(record.status, AUTH_SESSION_STATUSES, "session status"),
       revokedReason:
         record.revokedReason === null
           ? null
           : AuthSession.validateOneOf(
               record.revokedReason,
               SESSION_REVOCATION_REASONS,
               "session revocation reason",
             ),
     });
   }
   ```

   **`rehydrate` não é atalho para criar registro novo**: ele pula _todas_ as invariantes, não só a
   temporal. Quando um caso de uso precisa nascer uma entidade em competência passada — hoje só a
   importação de histórico — a entidade expõe `static createForImport(props)`, que dispensa
   exclusivamente a trava de tempo e mantém o resto da validação. As três fábricas compartilham um
   `private static build(props)`.

9. **Sem `toJSON` / `toPrimitives`.** Serialização é responsabilidade do service (`toResponseDto`).
10. **Nada de framework**: nem Prisma, nem Express, nem Zod, nem tsyringe dentro de `domain/`.
11. Tipo de persistência, quando precisa ser exportado para o repositório, é um alias explícito:
    `export type RecurringExpenseVersionPersistenceProps = Required<RecurringExpenseVersionProps>;`
    ou uma interface quando há campos nuláveis (`endMonth: number | null`,
    `revokedAt: Date | null`).
12. Entidade sem `id` próprio é aceita quando a chave é a do dono: `PasswordCredential` tem
    `userId` como PK (1:1 com `User`) e não gera UUID.
13. Segredo nunca entra em entidade: `RefreshToken` guarda só `tokenHash`, `PasswordCredential` só
    o hash PHC e o `pepperId`.

## Value objects

Há três em `domain/value-objects/`: `MonthlyCompetence` (o pivô de todo o domínio),
`EmailAddress` e `PasswordPolicy`.

### `MonthlyCompetence`

`domain/value-objects/monthly-competence.value-object.ts`:

```ts
const MIN_MONTH = 1;
const MAX_MONTH = 12;
const MIN_YEAR = 2000;
const MONTH_PAD_LENGTH = 2;

export class MonthlyCompetence {
  public readonly month: number;
  public readonly year: number;

  private constructor(month: number, year: number) {
    this.month = month;
    this.year = year;
  }

  public static create(month: number, year: number): MonthlyCompetence {
    if (!Number.isInteger(month) || month < MIN_MONTH || month > MAX_MONTH) {
      throw new Error("Month must be an integer between 1 and 12");
    }
    if (!Number.isInteger(year) || year < MIN_YEAR) {
      throw new Error("Year must be an integer >= 2000");
    }
    return new MonthlyCompetence(month, year);
  }
```

API pública: `static current(referenceDate = new Date())` (o mês corrente em UTC),
`static addMonths(c, offset)`, `static range(start, end)`, `isPastMonth(referenceDate = new Date())`,
`statusAt(referenceDate = new Date())` → `"PAST" | "CURRENT" | "FUTURE"`,
`isFutureOrCurrent(referenceDate = new Date())`, `isBefore(other)`, `isBeforeOrEqual(other)`, `isAfter(other)`, `isAfterOrEqual(other)`,
`equals(other)`, `toString()` → `"2026-09"`.

Regras do VO:

- Construtor recebe **argumentos posicionais** `(month, year)`, não um objeto de props.
- Toda comparação com "hoje" usa **UTC** (`getUTCFullYear()`, `getUTCMonth() + 1`).
- `referenceDate` é sempre um **parâmetro com default**, nunca lido implicitamente — é o que torna
  o VO 100% testável sem fake timers.
- Entidades guardam `month`/`year` achatados como `number` e expõem `getXCompetence()` que
  reconstrói o VO sob demanda.

### `EmailAddress`

A **única** normalização de e-mail do domínio (trim + minúsculas, formato, ≤ 254). `User.create`,
o cadastro, o login e o schema Zod (via `superRefine`) passam por ela. Guarda `value` e é usada
como `EmailAddress.create(raw).value`. De `domain/value-objects/email-address.value-object.ts`:

```ts
export class EmailAddress {
  public readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  public static create(raw: string): EmailAddress {
    const normalized = raw.trim().toLowerCase();
    EmailAddress.validateFormat(normalized);
    EmailAddress.validateLength(normalized);
    return new EmailAddress(normalized);
  }
```

### `PasswordPolicy`

Regra de tamanho da senha sem estado: **classe só com `static`**, sem instância nem construtor.
12 a 128 code points depois de NFKC (a mesma normalização que o hasher aplica), **sem `trim`**
— espaço é caractere de senha. De `domain/value-objects/password-policy.value-object.ts`:

```ts
export class PasswordPolicy {
  public static assert(password: string): void {
    const length = [...password.normalize("NFKC")].length;
    if (length < MIN_PASSWORD_LENGTH || length > MAX_PASSWORD_LENGTH) {
      throw new Error("Password must be between 12 and 128 characters");
    }
  }
}
```

O schema de **login** não aplica o mínimo, só o teto de 128 (senha antiga/curta tem que receber
`INVALID_CREDENTIALS`, não `VALIDATION_ERROR`).

## Checklist para criar uma entidade

- [ ] `export interface XProps` com `id?`/`createdAt?`/`updatedAt?`.
- [ ] Constantes de limite no módulo.
- [ ] Campos `public readonly` espelhando `Required<XProps>`.
- [ ] `private constructor` só com atribuições.
- [ ] `static create()` normaliza → valida → `randomUUID()` / `new Date()`.
- [ ] Um `private static validateX()` por regra, com mensagem igual à do Zod.
- [ ] Métodos de mutação devolvendo nova instância com `updatedAt: new Date()`.
- [ ] `static rehydrate()` **apenas** se a fábrica não reconstruir uma linha (regra de tempo ou
      datas calculadas de "agora"), e só para o repositório; coluna de estado em `string` →
      `XRecord` + validação no `rehydrate`.
- [ ] Tempo por parâmetro (`now: Date`) em fábricas de evento, mutações e predicados temporais.
- [ ] `static createForImport()` se algum caso de uso precisar nascer a entidade no passado.
- [ ] `getXCompetence()` se a entidade tiver competência.
- [ ] Teste unitário em `server/tests/unit/domain/entities/x.entity.test.ts` (skill `server-testes`).

## Não faça

- Não valide no construtor — valide em `create()`.
- Não devolva `this` de um método de update.
- Não exponha getters: os campos já são `public readonly`.
- Não use `node:crypto` (o padrão do projeto é `import { randomUUID } from "crypto"`).
- Não coloque regra de tempo ou checagem cross-agregado na entidade, salvo o caso já existente de
  `RecurringExpense` — isso é responsabilidade do caso de uso. Predicado temporal **puro**, com
  `now` recebido por parâmetro (`isActive(now)`, `isExpired(now)`), é permitido.
- Não leia `new Date()` dentro de método de entidade de auth: o caso de uso lê "agora" uma vez e
  repassa.
- Não normalize e-mail à mão: use `EmailAddress`.
- Não use `enum` do TypeScript para estado: array `as const` + tipo derivado.

## Inconsistências conhecidas

- **`public constructor` vs `constructor`**: 32 arquivos usam a forma explícita, 28 a implícita.
  Fatias novas (installment, recurring, expense-category) usam `public constructor` — **siga essa**.
- **Validação de 2 casas decimais está duplicada em 5 entidades.** Não replique por preguiça em
  código novo sem necessidade; se for extrair, extraia para o domínio (não para infra) e atualize
  as 5 de uma vez.
- `PasswordCredential.create` e `User.create` ainda caem em `new Date()` quando `createdAt`/
  `updatedAt` não vêm nas props, enquanto `AuthSession`/`RefreshToken` exigem `now`. Em código
  novo de auth, passe as datas explicitamente.
- **Guarda de competência passada** aparece na entidade (`RecurringExpense`) e no use case
  (revenue/expense avulsos, parcelado). Para agregado novo, **coloque no caso de uso** — é o lado
  majoritário e evita precisar de `rehydrate`.
