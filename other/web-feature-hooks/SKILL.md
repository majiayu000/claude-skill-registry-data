---
name: web-feature-hooks
description: Como escrever hooks de feature no web do Smaug com TanStack Query v5 — query key em const de módulo, staleTime 30_000, mutations create/update/remove, invalidateQueries + toast.success, onError com getApiErrorMessage e ação "Tentar novamente", e as variantes de Receitas/Despesas (hook de leitura com view-model, hook de mutations agrupadas com onSuccess(action), hook de assistente com React Hook Form) e os hooks de sessão useAuth/useRegister (bootstrap, safeDestination, logout).
---

# Hook de feature (TanStack Query)

## Quando usar esta skill

Ao criar/alterar `web/features/<f>/hooks/use*.ts`. Aqui mora a regra de negócio e o estado de
servidor; o componente só recebe o resultado.

Há quatro formatos em uso — escolha pelo que o hook faz:

| Formato                         | Exemplo                                                         |
| ------------------------------- | --------------------------------------------------------------- |
| Lista + CRUD num hook só        | `features/categorias/hooks/useCategories.ts` (arquivo canônico) |
| Leitura com view-model          | `useExpenseMonth`, `useInstallmentExpense`, `useRevenueMonth`   |
| Mutations agrupadas da feature  | `useExpenseMutations`, `useRevenueMutations`                    |
| Estado de assistente/formulário | `useExpenseWizard`, `useRevenueWizard`                          |

## Arquivo canônico — lista + CRUD

`web/features/categorias/hooks/useCategories.ts` (trecho; `update` e `remove` seguem o mesmo molde):

```ts
"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { CategoriasService } from "../services/CategoriasService";
import { toast } from "@/shared/hooks/useToast";
import { getApiErrorMessage } from "@/infra/api-error";

const QUERY_KEY = ["categories"];

export function useCategories() {
  const qc = useQueryClient();

  const query = useQuery({
    queryKey: QUERY_KEY,
    queryFn: CategoriasService.getAll,
    staleTime: 30_000,
  });

  const create = useMutation({
    mutationFn: (name: string) => CategoriasService.create(name),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: QUERY_KEY });
      toast.success("Categoria criada com sucesso!");
    },
    onError: (error, variables) =>
      toast.error(getApiErrorMessage(error, "Erro ao criar categoria."), {
        action: { label: "Tentar novamente", onClick: () => create.mutate(variables) },
      }),
  });

  // update, remove ...

  return { ...query, create, update, remove };
}
```

## Regras

1. **`"use client"` na primeira linha** de todo arquivo de hook.
2. **A query key é um `const` de módulo, nunca inline.** Em código novo, nome **`QK`**. Em inglês.
   Receitas e Despesas usam **um prefixo por natureza**, exportado pelo hook do mês e importado pelos
   demais, e acrescentam sufixos na própria query:
   ```ts
   export const QK = ["expenses"]; // useExpenseMonth.ts
   queryKey: [...QK, "month", competence.year, competence.month];
   queryKey: [...QK, "summary", year]; // useExpenseYearSummary
   queryKey: [...QK, "installment", id]; // useInstallmentExpense
   ```
   Assim uma única invalidação por `QK` atualiza lista, faixa de 12 meses e Fichas abertas.
   O Dashboard inlineia a chave parametrizada: `queryKey: ["dashboard", competence.year, competence.month]`.
3. **`const qc = useQueryClient();`** — sempre abreviado `qc`.
4. **`staleTime: 30_000`** em toda `useQuery` (com separador numérico, não `30 * 1000`).
   `enabled` só com motivo documentado em comentário — o único caso é `useDataExport`, que desliga a
   prévia enquanto o período é inválido. **Não use `select` nem `placeholderData`.**
5. `queryFn` é a referência nua do método do service (`queryFn: CategoriasService.getAll`) ou uma
   arrow quando há argumento (`queryFn: () => DespesasService.getMonth(competence)`).
6. `mutationFn` é referência nua quando o payload casa 1:1; caso contrário é arrow que
   **desestrutura o `id` e espalha o resto**, com o tipo inline no parâmetro:
   ```ts
   mutationFn: ({ id, ...p }: { id: string; endYear: number; endMonth: number }) =>
     DespesasService.terminateRecurring(id, p),
   ```
7. **Vocabulário dos nomes de mutation**: `create`, `update`, `remove` (nunca `delete` — palavra
   reservada), `addVersion`, `terminate`; quando a feature tem mais de um alvo para o mesmo verbo, o
   sufixo diz qual (`updateOneTime`, `terminateInstallment`). **Não existe `isCreating`.**
8. **`onSuccess` invalida e avisa**: `qc.invalidateQueries({ queryKey: QK })` e
   `toast.success("<mensagem pt-BR>")`. Sem update otimista, sem `setQueryData`. O texto do toast
   vem da spec da feature — Categorias termina em `!`; Receitas/Despesas usam o texto exato do PRD,
   sem `!` ("Despesa adicionada", "Parcelamento encerrado").
9. **`onError` é arrow concisa** (sem chaves) devolvendo `toast.error(...)`:
   ```ts
   onError: (error, variables) =>
     toast.error(getApiErrorMessage(error, "Erro ao <verbo> <substantivo>."), {
       action: { label: "Tentar novamente", onClick: () => x.mutate(variables) },
     }),
   ```
   O fallback **sempre** começa com `"Erro ao "` e termina com ponto. O rótulo da ação é
   **exatamente** `"Tentar novamente"`.
10. **Retorno**: `return { ...query, create, update, remove };` — o resultado da query é espalhado
    plano e as mutations ficam aninhadas. O consumidor lê `hook.data`, `hook.isLoading`,
    `hook.create.mutate(...)`, `hook.create.isPending`.
11. Defaults globais (retry 3, backoff exponencial, `gcTime`, `refetchOnWindowFocus: false`) vivem
    em `infra/query-client.ts` — não os repita no hook.
12. Hook de negócio **não** importa `next/navigation`; usa `@/infra/router-adapter`.

## Variantes de Receitas e Despesas

### Leitura com view-model

O hook espalha a query e acrescenta **campos derivados prontos para a tela**, calculados por uma
função pura exportada (testável sem React):

```ts
export function useExpenseMonth(competence: Competence) {
  const query = useQuery({
    queryKey: [...QK, "month", competence.year, competence.month],
    queryFn: () => DespesasService.getMonth(competence),
    staleTime: 30_000,
  });

  return {
    ...query,
    ledger: query.data ? toExpenseLedger(query.data) : undefined,
    errorMessage: query.error
      ? getApiErrorMessage(query.error, "Erro ao carregar despesas.")
      : null,
  };
}
```

- `errorMessage` já mapeado em pt-BR: o componente nunca chama `getApiErrorMessage`.
- `toExpenseLedger`, `toExpenseRow`, `toInstallmentSummary` são `export function` no mesmo arquivo.
- Situação de competência, `canDelete`, `canTerminate` e `isExpired` **vêm do servidor**; o hook
  repassa, não recalcula a partir de `new Date()`.

### Mutations agrupadas — `useExpenseMutations({ onSuccess })`

Todas as escritas da feature num hook só, consumido pelo assistente e pelas Fichas:

```ts
/** Invalidação por chave: o Dashboard soma as mesmas despesas e não pode ficar defasado. */
const DASHBOARD_QK = ["dashboard"];

export function useExpenseMutations({
  onSuccess,
}: { onSuccess?: (action: ExpenseAction) => void } = {}) {
  const qc = useQueryClient();

  const succeed = (action: ExpenseAction, message: string) => {
    qc.invalidateQueries({ queryKey: QK });
    qc.invalidateQueries({ queryKey: DASHBOARD_QK });
    toast.success(message);
    onSuccess?.(action);
  };
  // create, updateOneTime, remove, addVersion, terminate, terminateInstallment
}
```

- **Toda mutation invalida o prefixo da natureza e `["dashboard"]`** — por chave, sem importar a
  feature dashboard.
- **O `onSuccess` do chamador fica no hook, não no `.mutate(..., { onSuccess })`**: assim ele também
  roda quando o usuário repete a ação pelo "Tentar novamente" do toast, e o modal fecha.
- O chamador decide pelo `action` (a Ficha fecha ao remover e só sai da confirmação ao encerrar).
- Criação por tipo recebe uma união discriminada `{ kind, payload }`; o toast sai de um
  `Record<Kind, string>`.

### Estado de assistente — `useExpenseWizard`

O React Hook Form fica **dentro do hook**, não no componente:

```ts
const form = useForm<ExpenseWizardValues>({
  defaultValues: initialValues(options),
  resolver: zodResolver(
    expenseDetailsSchema(reference),
  ) as unknown as Resolver<ExpenseWizardValues>,
});
const mutations = useExpenseMutations({ onSuccess: onDone });
// ...
return {
  step,
  form,
  values: form.watch(),
  // Ler `formState.errors` durante o render é o que assina o proxy do RHF.
  errors: form.formState.errors,
  next,
  back,
  submit,
  isPending: mutations.create.isPending || mutations.updateOneTime.isPending,
};
```

- O schema é uma **fábrica** que recebe o `reference` do servidor (para a regra de competência
  passada). O cast do resolver existe porque o schema é uma união discriminada por `kind`, enquanto o
  formulário guarda todos os campos de uma vez para que trocar de tipo não perca o que foi digitado.
- Valide só ao sair da etapa (`await form.trigger()`), e monte o payload da API em `submit`.
- **Devolva `errors: form.formState.errors`**, lido no corpo do hook. Ler `form.formState.errors`
  só no componente, via `wizard.form`, não assina o proxy e os erros não aparecem.
- Prévias (divisão de parcelas, meses afetados) vêm de `@/shared/lib/preview`, espelho do domínio.

## Hooks compartilhados (não são de feature)

- **`shared/hooks/useCompetenceNavigation`** — estado de UI puro:
  `{ selected, status, isCurrent, current, navigate, select, goToCurrent }`. Com `persistKey`, guarda
  o mês em `sessionStorage` (Dashboard usa sem `persistKey`).
- **`useLedgerNavigation()`** (mesmo arquivo) — a versão de Receitas/Despesas: persiste em
  `LEDGER_COMPETENCE_KEY` e expõe `adoptReference(reference)`, chamado durante o render da tela com o
  `reference` da primeira resposta.
- **`shared/hooks/useSeriesActions`** — modo, abas, formulários e prévia da Ficha de série, comum a
  recorrente e fixa; recebe os schemas da feature por parâmetro.

## Outras exceções legítimas

- **`useDashboard`** — só query, devolve `useQuery` direto.
- **`useRegister`** — mutation **sem toast e sem invalidação** (o formulário renderiza o erro
  inline). O cadastro já abre a sessão: `onSuccess` faz `setSession(session.accessToken)` e
  `router.push("/dashboard")`. Devolve `{ ...mutation, isEmailTaken }`, derivado do código
  `EMAIL_ALREADY_EXISTS`, para o formulário oferecer o link "Entrar".
- **`useVersionHistory`** — desestrutura a query e deriva no cliente, devolvendo um nome de domínio
  (`groups`) em vez de `data`.
- **`useAuth`** (`features/auth/hooks/useAuth.ts`) — não usa TanStack Query: `useState` +
  `useEffect`, porque o bootstrap de sessão não pode ser cacheado. Roda no layout de `(app)` e no
  `LoginForm`. Devolve `{ user, isAuthenticated, isLoading, error, login, logout, logoutAll }`.

  **Bootstrap** — retoma a sessão ao abrir o app:

  ```ts
  async function resumeSession(): Promise<User | null> {
    if (getAccessToken()) return AuthService.getMe();
    if (hasSessionHint()) return (await refreshSession()).user;
    return null;
  }
  ```

  e guarda a regra mais importante do tratamento de erro do front:

  ```ts
  .catch((err) => {
    // Renovação recusada (401): `refreshSession` já apagou o indicador e mandou para o login.
    if (isInvalidSessionError(err)) {
      setAuthState({ user: null, isAuthenticated: false });
      return;
    }
    // Falha transitória (rede fora, 5xx): a sessão continua válida — perdemos
    // apenas os dados do perfil, que voltam no próximo carregamento.
    setAuthState({ user: null, isAuthenticated: true });
    setError("Não foi possível carregar seu perfil. Tente novamente em instantes.");
  })
  ```

  **`login(input, next = null)`** — `AuthService.login` → `setSession(session.accessToken)` →
  `router.push(safeDestination(next))`. O `next` chega **por parâmetro**, não por
  `useSearchParams`: no layout de `(app)` o hook de busca exigiria `<Suspense>`. `safeDestination`
  é `export function` no mesmo arquivo (testável sem React) e é a defesa contra redirecionamento
  aberto:

  ```ts
  export function safeDestination(next: string | null): string {
    if (!next || !next.startsWith("/") || UNSAFE_CHARS.test(next)) return DEFAULT_DESTINATION;
    const url = new URL(next, RESOLUTION_BASE);
    if (url.origin !== RESOLUTION_BASE) return DEFAULT_DESTINATION;
    return `${url.pathname}${url.search}${url.hash}`;
  }
  ```

  **`logout` / `logoutAll`** — sair **nunca falha para o usuário**: chamam a API num `try/catch`
  vazio e, no `finally`, `endLocalSession()` (`clearSession()` + estado vazio + `redirectToLogin()`,
  cuja troca de documento descarta o cache do React Query). `logoutAll` passa por `/auth/*`, que o
  `api-client` não renova; por isso, num 401, ele mesmo chama `refreshSession()` e repete **uma**
  vez antes de desistir.

## Checklist

- [ ] `"use client"` na primeira linha.
- [ ] `const QK = [...]` no módulo (prefixo exportado, se a feature tem várias queries).
- [ ] `useQuery` com `staleTime: 30_000`.
- [ ] Mutations nomeadas do vocabulário.
- [ ] `onSuccess`: invalidate (+ `["dashboard"]` se a feature entra nos totais) + `toast.success`.
- [ ] `onError`: `getApiErrorMessage(error, "Erro ao ….")` + ação `"Tentar novamente"` que re-dispara
      com `variables`.
- [ ] Derivações em função pura exportada; `errorMessage` pronto para a tela.
- [ ] Teste em `use<Coisa>.test.tsx` com `setup()` local (skill `web-testes`).
- [ ] Todo código de erro novo da API tem entrada em `infra/api-error.ts`.

## Não faça

- Não coloque `queryKey` inline (salvo query parametrizada).
- Não nomeie mutation de `delete`.
- Não faça update otimista nem `setQueryData`.
- Não chame `apiClient` direto — passe pelo service da feature.
- Não escreva a mensagem de erro à mão: use `getApiErrorMessage` com fallback.
- Não recalcule no cliente uma situação que o servidor já informa (competência, parcela, expiração).
- Não passe o `onSuccess` que fecha modal no `.mutate()` — o "Tentar novamente" o perderia.
- Não toque em sessão (`setSession`/`clearSession`/`refreshSession`) fora de `features/auth/hooks` —
  o resto do app só vê o efeito pelo `apiClient`.
- Não leia `?next=` com `useSearchParams` nem navegue para ele sem `safeDestination`.

## Inconsistências conhecidas

- **`QK` vs `QUERY_KEY`**: `useCategories.ts` usa `QUERY_KEY`; as demais features usam `QK`.
  **Em código novo, use `QK`.**
- `useVersionHistory.ts` e `shared/hooks/useDebounce.ts` não têm `"use client"` (funciona por
  acidente, pelo consumidor já ser client). **Sempre inclua a diretiva em hook novo.**
