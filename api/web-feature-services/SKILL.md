---
name: web-feature-services
description: Como escrever services de feature no web do Smaug — objeto const de arrow functions async, apiClient, payload como tipo inline, retorno anotado, endpoints literais sem /api e mapeamento verbo→método HTTP.
---

# Service de feature

## Quando usar esta skill

Ao criar/alterar `web/features/<f>/services/<Feature>Service.ts`. É a **única** camada do front que
fala com a rede.

## Anatomia canônica

`web/features/despesas/services/DespesasService.ts`:

```ts
import { apiClient } from "@/infra/api-client";
import type {
  OneTimeExpense,
  InstallmentExpense,
  RecurringExpense,
  RecurringExpenseVersion,
} from "../types";

export const DespesasService = {
  // One-time expenses
  getOneTime: async (): Promise<OneTimeExpense[]> => {
    const { data } = await apiClient.get("/expenses/one-time");
    return data;
  },
  createOneTime: async (payload: {
    description: string;
    amount: number;
    categoryId: string;
    competenceYear: number;
    competenceMonth: number;
  }): Promise<OneTimeExpense> => {
    const { data } = await apiClient.post("/expenses/one-time", payload);
    return data;
  },
  updateOneTime: async (
    id: string,
    payload: {
      description: string;
      amount: number;
      categoryId: string;
      competenceYear: number;
      competenceMonth: number;
    },
  ): Promise<OneTimeExpense> => {
    const { data } = await apiClient.put(`/expenses/one-time/${id}`, payload);
    return data;
  },
  deleteOneTime: async (id: string): Promise<void> => {
    await apiClient.delete(`/expenses/one-time/${id}`);
  },
```

## Regras

1. **Export é um `const` objeto de arrow functions async**, nomeado `<Feature>Service` em PascalCase,
   igual ao nome do arquivo. Sem classe, sem `default`, sem barril.
2. Importa `{ apiClient }` de `@/infra/api-client` (alias, mesmo de dentro da feature) e os tipos por
   caminho relativo `from "../types"`.
3. **Tipo de retorno sempre anotado explicitamente**: `Promise<T>`, `Promise<T[]>`, `Promise<void>`.
4. **O payload é um tipo estrutural inline no parâmetro**, e o parâmetro se chama **`payload`**
   (`data` só em `AuthService.register`). Para update/patch a assinatura é `(id: string, payload: {...})`.
5. **Endpoints são strings literais, sem `/api`**, em kebab-case, com template literal para ids:
   `/expenses/one-time`, `/expenses/installment`, `/expenses/recurring/${id}/terminate`,
   `/revenues/fixed`, `/auth/login`, `/users/me`. Não existe arquivo de constantes de rota. O `/api`
   do repasse é o `baseURL` do `apiClient` (skill `web-infra`) — escrevê-lo no service daria
   `/api/api/...`.
6. Mapeamento verbo→método:

   | Operação                                  | Método                                            |
   | ----------------------------------------- | ------------------------------------------------- |
   | criar                                     | `post`                                            |
   | substituição total                        | `put`                                             |
   | atualização parcial / operação de domínio | `patch`                                           |
   | excluir                                   | `delete`, devolvendo `Promise<void>` sem `return` |

   Ações de domínio viram sub-rota: `terminateRecurring` → `patch("/expenses/recurring/${id}/terminate")`.

7. **Nomes de método**: `getX`, `createX`, `updateX`, `deleteX` (o service usa `delete`; o hook
   renomeia para `remove`), mais verbos de domínio como `addRecurringVersion`, `terminateRecurring`.
8. Seções separadas por comentário de linha: `// One-time expenses`, `// Installment expenses`,
   `// Recurring expenses`.
9. Genérico no `apiClient` só quando a resposta tem forma diferente do tipo de domínio exportado, e
   essa forma é uma **`interface` local não exportada** no próprio arquivo do service:

   ```ts
   interface ExpenseQueryResponse { ... }

   const [revRes, expRes] = await Promise.all([
     apiClient.get<RevenueQueryResponse>("/revenues", { params }),
     apiClient.get<ExpenseQueryResponse>("/expenses", { params }),
   ]);
   ```

10. Transformação pesada fica em **funções privadas acima do objeto exportado**
    (`fetchMonth`, `toEntries`, `groupByMonth` em `HistoricoService.ts`) — o objeto exportado
    permanece fino.
11. **O service não trata erro**: deixa o axios rejeitar. Quem traduz é o hook, via
    `getApiErrorMessage` (skill `web-infra`).

## O service de autenticação

`web/features/auth/services/AuthService.ts` segue a mesma anatomia — e **não sabe de sessão**: devolve
o corpo e quem guarda o token é o hook (`useAuth`/`useRegister`, via `setSession`):

```ts
export const AuthService = {
  register: async (data: RegisterInput): Promise<AuthSessionResponse> => {
    const { data: session } = await apiClient.post("/auth/register", data);
    return session;
  },

  login: async (payload: LoginInput): Promise<AuthSessionResponse> => {
    const { data } = await apiClient.post("/auth/login", payload);
    return data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post("/auth/logout");
  },

  logoutAll: async (): Promise<void> => {
    await apiClient.post("/auth/logout-all");
  },

  getMe: async (): Promise<User> => {
    const { data } = await apiClient.get("/users/me");
    return data;
  },
};
```

- Passa pelo `apiClient` como todo service: o Bearer entra sozinho (`logoutAll`, `getMe`) e o cookie
  `smaug_refresh` vai sozinho pela mesma origem (`logout`).
- 401 em `/auth/*` **não** dispara renovação no interceptor — o service só propaga; quem decide é o
  hook.
- A renovação (`POST /auth/refresh`) **não** é método do service: vive em `infra/auth-refresh.ts`,
  com axios puro, porque o próprio interceptor do `apiClient` depende dela.

## Checklist

- [ ] `export const <Feature>Service = { ... }` com arrow functions async.
- [ ] Todo método com tipo de retorno anotado.
- [ ] Payload como tipo inline no parâmetro `payload`.
- [ ] Endpoint literal correto (confira o método HTTP contra `server/src/presentation/routes/`).
- [ ] Transformação complexa em função privada acima do objeto.
- [ ] Teste `<Feature>Service.test.ts` assertando **assinatura da requisição**, corpo e código de
      erro (skill `web-testes`) — `PUT` vs `PATCH` e `/:id` vs `/:id/terminate` são invisíveis para
      o TypeScript e é exatamente isso que o teste protege.

## Não faça

- Não use `try/catch` para engolir erro — o hook precisa dele.
- Não construa mensagem de erro aqui.
- Não use classe nem `export default`.
- Não leia cookie/sessão nem monte `Authorization`: o Bearer é injetado pelo interceptor do
  `apiClient`, e a sessão é guardada pelo hook.
- Não coloque `/api` no caminho.

## Inconsistências conhecidas

- `DadosService.downloadExport` usa `const response = await apiClient.get(...)` (precisa do
  `response.headers` além do corpo); os demais desestruturam `const { data }`. **A desestruturação é a
  forma padrão — use `response` só quando precisar de algo além do corpo.**
- `AuthService.register` recebe o parâmetro `data` (não `payload`) e por isso renomeia na
  desestruturação (`const { data: session }`). Em código novo, chame o parâmetro de `payload`.
- `AuthService` tipa o payload com interfaces nomeadas de `../types` (`RegisterInput`,
  `LoginInput`) em vez de tipo inline — reaproveitadas pelos hooks e pelo formulário. Nos demais
  services, siga o tipo inline.
