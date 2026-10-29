---
name: web-testes
description: Como escrever testes do web do Smaug — Vitest + Testing Library + MSW, títulos em pt-BR, harness de web/tests (renderWithProviders, createTestQueryClient, fixtures, spyOnToast, MSW em /api com auth simulada e loginAs), asserção de assinatura de requisição, thresholds por glob e as armadilhas já verificadas.
---

# Testes do web

## Quando usar esta skill

Ao escrever qualquer teste em `web/` — unitário, de componente, de hook, de service ou de página.

## Onde o teste mora

- **Unitário, de componente e de hook: ao lado do fonte** — `shared/components/Modal.test.tsx`,
  `features/despesas/hooks/useExpenseMutations.test.tsx`.
- **Integração de página: `web/tests/integration/<pagina>-page.test.tsx`** — porque importa de mais
  de uma feature, o que dentro de uma feature violaria a proibição de import cross-feature.

```bash
npm run --prefix web test            # uma passada
npm run --prefix web test:watch
npm run --prefix web test:coverage
```

## Vitest × Playwright — quem prova o quê

> MSW prova que o frontend se comporta corretamente **dado um contrato**; o E2E prova que o
> contrato é **real**.

Por isso os testes de integração de página **não repetem** os caminhos felizes que o E2E já cobre.
Eles cobrem o que o E2E não alcança barato: cada código de erro da API renderizando sua mensagem em
pt-BR, a ação "Tentar novamente" do toast de erro, o ramo `DeleteWarningModal` vs `ConfirmDialog`,
e as guardas de competência passada/futura.

## Convenções de escrita

**Títulos em pt-BR, minúsculos, verbo na 3ª pessoa do presente — nunca "deve"/"should".**
Aberturas mais usadas: `usa`, `não`, `fecha`, `devolve`, `mostra`, `exibe`, `rejeita`, `exige`,
`avisa`, `renderiza`, `propaga`, `aceita`, `expõe`, `envia`, `invalida`.

`describe` por tipo de teste, **sempre irmãos, nunca aninhados**:

| Tipo       | Padrão                  | Exemplo                                                                    |
| ---------- | ----------------------- | -------------------------------------------------------------------------- |
| Componente | `<Componente> <estado>` | `describe("Modal fechado")`, `describe("Modal com cabeçalho customizado")` |
| Hook       | `<useHook>: <operação>` | `describe("useExpenseMutations: create")`                                  |
| Service    | `<Service>.<método>`    | `describe("CategoriasService.getAll")`                                     |
| Página     | `página de <x>: <fase>` | `describe("página de categorias: exclusão")`                               |
| Harness    | `harness: <camada>`     | `describe("harness: axios + MSW + jsdom")`                                 |

## O harness (`web/tests/`)

| Arquivo                | Papel                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| `render.tsx`           | `renderWithProviders`, `renderHookWithProviders`, `createTestQueryClient`                                |
| `router.tsx`           | contextos reais do Next + `routerAdapterMock` / `searchParamsMock`                                       |
| `msw/`                 | `server`, `db` (store em memória), handlers por recurso, `mockApiError`/`mockNetworkError`/`mockPending` |
| `msw/handlers/auth.ts` | `/auth/*` e `GET /users/me`; exporta `openSession`, `issueAccessToken`, `authenticatedUser`              |
| `requests.ts`          | `recordRequests`, `signatures`, `bodyOf` — caminho gravado **sem** o prefixo `/api`                      |
| `fixtures/`            | factories determinísticas por entidade                                                                   |
| `toast.ts`             | `spyOnToast`, `drainToasts`                                                                              |
| `session.ts`           | `loginAs(user?)` → `User`, `logout()` (sessão real em memória + indicador + sessão MSW)                  |
| `time.ts`              | `NOW`, `NOW_COMPETENCE`, `freezeTime`, `freezeDateOnly`                                                  |
| `mocked.ts`            | `Mocked<T>`, `mockService`                                                                               |
| `harness.test.tsx`     | testes do próprio harness — **se quebrarem, comece por aqui**                                            |

`vitest.setup.ts` cobre as lacunas do jsdom 29 (`matchMedia` com `setMatchMedia`, `ResizeObserver`,
pointer capture, `scrollIntoView`) e o ciclo do MSW:

```ts
beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(() => {
  if (hasDom) cleanup();
  server.resetHandlers();
  resetDb();
  resetFixtureIds();
  drainToasts();
  // O módulo de sessão e o `document` do jsdom vivem por ARQUIVO, não por teste:
  // sem isto, o access token de um loginAs() vaza o Bearer para o teste seguinte.
  clearSession();
  vi.unstubAllEnvs();
});
```

`onUnhandledRequest: "error"` é o ponto central — sem ele uma requisição não prevista vaza para o
XHR real do jsdom.

### `createTestQueryClient`

```ts
export function createTestQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: Infinity, staleTime: 0, refetchOnWindowFocus: false },
      mutations: { retry: false },
    },
  });
}
```

### `renderWithProviders`

Opções: `queryClient`, `router`, `pathname` (default `"/dashboard"`), `searchParams`, `withToasts`
(default `false` — o `ToastContainer` real assina a fila global e o `setTimeout` de 5 s vazaria para
os testes vizinhos). Devolve `{ queryClient, router, ...rtlResult }`.

Componente puramente apresentacional usa `render` do RTL direto. Qualquer coisa que toque Query,
router ou toast usa o harness. Página de integração embrulha numa função local:

```ts
function renderPage(options = {}) {
  return renderWithProviders(<CategoriasPage />, { pathname: "/categorias", ...options });
}
```

### `setup()` local nos testes de hook

```ts
function setup() {
  const queryClient = createTestQueryClient();
  const invalidateQueries = vi.spyOn(queryClient, "invalidateQueries");
  const toast = spyOnToast();
  const rendered = renderHookWithProviders(() => useCategories(), { queryClient });
  return { ...rendered, queryClient, invalidateQueries, toast };
}
```

O teste também **redeclara o `QK` esperado** e o asserta — é assim que a query key vira contrato.
Hook que recebe `onSuccess` (`useExpenseMutations({ onSuccess })`) cria o `vi.fn()` no `setup()` e
asserta a `action` recebida, inclusive depois do "Tentar novamente".

## MSW

- **Default: estado.** `seedDb({ categories: [makeCategory({ name: "Moradia" })] })`. O store em
  memória (`tests/msw/db.ts`) é o que faz o teste de integração significar algo: criar uma categoria
  → o hook invalida → refetch → a linha nova aparece de verdade.
- **Erro**: `mockApiError(method, path, status, body)`, `mockNetworkError(method, path)`,
  `mockPending(method, path)`. O `path` é o da API (`"/auth/login"`, `"/expenses/categories"`):
  `url(path)` de `tests/msw/base.ts` acrescenta `API = "http://localhost:3001/api"` — a origem do
  jsdom (`environmentOptions.jsdom.url` no `vitest.config.ts`) mais o `/api` do repasse.
- **Autenticação simulada** (`handlers/auth.ts` + `db`): `db.passwords[userId]` é a senha que
  `POST /auth/login` confere; `db.session = { userId } | null` faz o papel do cookie `httpOnly`
  `smaug_refresh` (`null` → `POST /auth/refresh` responde 401 `INVALID_REFRESH_TOKEN`);
  `db.issuedTokens` numera os tokens `access-<userId>-<n>`, então cada renovação devolve um token
  diferente e observável. Só `GET /users/me` e `POST /auth/logout-all` conferem o Bearer
  (`authenticatedUser(request)`, 401 `UNAUTHORIZED` sem ele); os handlers de recurso não. Para
  simular token vencido num recurso, sobrescreva a rota com um 401 **de uma vez só**
  (`server.use(http.get(url(path), () => HttpResponse.json({ error: "UNAUTHORIZED" }, { status: 401 }), { once: true }))`,
  como em `infra/api-client.test.ts`) — o `mockApiError` permanente prova o "não renova em laço".
- **`server.use(http.get(...))` cru** só quando a resposta precisa variar a cada requisição.
- **O que o servidor calcula, o handler calcula**: as consultas de Receitas/Despesas montam
  `competenceStatus`, `reference`, `previousAmount`, situação das parcelas, `canDelete`/`canTerminate`
  e `isExpired` a partir do `db`, usando `serverReference()` de `tests/msw/base.ts` (mês
  corrente em UTC do relógio — congele com `freezeDateOnly`). Para testar outra situação, semeie
  dados em outra competência — não edite o campo calculado.
- Os handlers reproduzem os códigos de erro reais do server (`EXPENSE_CATEGORY_NAME_ALREADY_EXISTS`
  409, `VERSION_CONFLICT` 409, `*_NOT_FOUND` 404, `EMAIL_ALREADY_EXISTS` 409,
  `INVALID_CREDENTIALS` 401) e devolvem as **fixtures**.

## Testes de service — assertam a assinatura da requisição

`recordRequests()` grava o caminho **sem** `/api` (`"POST /auth/login"`, `"GET /users/me"`): o
teste fala nos caminhos da API, como o service os escreve.

```ts
const calls = recordRequests();
await CategoriasService.update(category.id, "Casa");

expect(signatures(calls)).toEqual([`PUT /expenses/categories/${category.id}`]);
expect(await bodyOf(calls[0])).toEqual({ name: "Casa" });

await expect(CategoriasService.create("moradia")).rejects.toMatchObject({
  response: { status: 409, data: { error: "EXPENSE_CATEGORY_NAME_ALREADY_EXISTS" } },
});
```

> A asserção mais valiosa dos testes de service é justamente essa: `PUT` vs `PATCH` e `/:id` vs
> `/:id/terminate` são fáceis de errar e invisíveis para o TypeScript.

Título que registra a armadilha: `it("faz PUT em /expenses/categories/:id (não PATCH)")`.

## Interação e espera

- **`userEvent` é usado direto do módulo — não existe `userEvent.setup()` no projeto.** Toda
  interação é `await`: `await userEvent.click(...)`, `await userEvent.type(...)`,
  `await userEvent.keyboard("{Escape}")`, `await userEvent.selectOptions(...)`.
- **`findBy*` para aparecer**; **`waitFor` para sumir** ou para predicado sobre spy:
  ```ts
  expect(await screen.findByText("Nenhuma categoria cadastrada.")).toBeInTheDocument();
  await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  ```
- Mutation de hook dispara dentro de `act`: `act(() => result.current.create.mutate(PAYLOAD));`
- `within(dialog())` escopa consultas ao portal do Radix, com `const dialog = () => screen.getByRole("dialog");`
- Com uma confirmação aberta sobre a Ficha, o Radix marca a Ficha com `aria-hidden`: para provar que
  ela continua aberta, use `screen.getAllByRole("dialog", { hidden: true })`.
- **Sempre `screen`, nunca `container`** — a única exceção é contar skeleton, que não tem papel:
  `expect(container.querySelectorAll(".animate-pulse")).toHaveLength(4)`.

## Como assertar toast — dois modos

**1. Teste de hook** — spy, com a string pt-BR exata e `expect.anything()` para o bag de opções:

```ts
await waitFor(() =>
  expect(toast.error).toHaveBeenCalledWith("Erro ao criar parcelamento.", expect.anything()),
);
```

Retry através do helper local:

```ts
function retryFromToast(toast: ReturnType<typeof spyOnToast>) {
  const [, options] = toast.error.mock.calls.at(-1)!;
  expect(options?.action?.label).toBe("Tentar novamente");
  act(() => {
    options!.action!.onClick();
  });
}
```

e prove o re-disparo com `recordRequests()`:
`expect(calls.filter((c) => c.method === "POST")).toHaveLength(2);`

**2. Teste de página** — `renderPage({ withToasts: true })` e asserção por texto no DOM:

```ts
expect(await screen.findByText("Já existe uma categoria com este nome.")).toBeInTheDocument();
// `getByRole` não enxerga o toast aqui: o Radix Dialog marca os irmãos do
// modal aberto com aria-hidden, removendo-os da árvore de acessibilidade.
expect(screen.getByText("Tentar novamente")).toBeInTheDocument();
```

## Fixtures

Assinatura fixa `makeX(o: Partial<X> = {}): X`, parâmetro de uma letra `o`, defaults primeiro,
`...o` depois, e campo derivado reaplicado **após** o spread para não poder ser quebrado:

```ts
export function makeOneTimeExpense(o: Partial<OneTimeExpense> = {}): OneTimeExpense {
  const category = o.category ?? makeCategory();
  return {
    id: nextId("exp"),
    userId: fixtureUuid(1),
    categoryId: category.id,
    description: "Supermercado",
    amount: 450,
    competenceYear: 2026,
    competenceMonth: 9,
    createdAt: FIXED_DATE,
    updatedAt: FIXED_DATE,
    ...o,
    category,
  };
}
```

Determinismo é regra: **nada de `Math.random` nem faker** — ids sequenciais (`nextId("exp")`,
`fixtureUuid(n)`), `FIXED_DATE`, e `resetFixtureIds()` no `afterEach` global. Valores padrão em
pt-BR (`"Supermercado"`, `"Aluguel"`, `"Moradia"`, `"Salário"`).

## Tempo e sessão

`tests/time.ts`: `NOW = 2026-09-13T12:00:00.000Z`, `NOW_COMPETENCE = { year: 2026, month: 9 }`,
`freezeTime()`, `freezeDateOnly()` (`vi.useFakeTimers({ toFake: ["Date"] })` — é o que testes com
MSW + axios precisam). **Prefira passar um `reference` explícito para `shared/lib/competence.ts` a
congelar o relógio.**

`tests/session.ts` (real, não mockamos `infra/session.ts` — o interceptor do `api-client` precisa
ler o token de verdade):

```ts
export function loginAs(user: User = makeUser()): User {
  if (!db.users.some((u) => u.id === user.id)) db.users.push(user);
  setSession(openSession(user).accessToken);
  return user;
}

/** Encerra a sessão dos dois lados: a aba esquece o token e o servidor, o refresh. */
export function logout(): void {
  clearSession();
  db.session = null;
}
```

`loginAs()` deixa a aba como o login real: access token em memória, indicador `smaug_session` e,
no MSW, refresh válido — então um 401 do recurso renova e refaz. Use o `User` devolvido para
assertar (`const user = loginAs(makeUser({ name: "João Silva" }))`).

Teste que exercita 401/renovação/logout faz `vi.mock("@/infra/navigation", () => ({ redirectToLogin:
vi.fn() }))` — sem o duplo, o jsdom imprime "Not implemented: navigation".

`tests/mocked.ts`: `mockService<T>(real, overrides)` é para **teste de hook cujo assunto é a fiação**
(query key, invalidação, mensagem de toast, callback de retry) — não para transporte. Transporte é
MSW.

## Cobertura (`web/vitest.config.ts`)

Piso global `lines 100 / functions 100 / branches 99 / statements 100`, e gates por glob em 100% para
`shared/lib/**`, `infra/**`, `proxy.ts`, `shared/hooks/**`, `shared/components/**`,
`features/*/services/**`, `features/*/hooks/**`, `features/*/components/**`.
`app/**` é a exceção justificada (`branches: 96`), por causa dos ramos falsos inalcançáveis do idioma
`isOpen={!!deleteTarget}` + `if (deleteTarget)` na página de Categorias. `app/**` inclui o repasse
`app/api/[...path]/route.ts`, coberto por `route.test.ts` (`@vitest-environment node`).
Excluídos por política: `**/*.test.*`, `**/types/index.ts`, `app/layout.tsx`, `app/page.tsx`,
`app/providers.tsx`, `next.config.ts`.

## Armadilhas verificadas (não redescubra)

| Armadilha                                               | Como lidar                                                                                                     |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `formatCurrency` emite **U+00A0** entre `R$` e o número | Asserte `toBe("R$ 1.234,56")` com NBSP. Dentro de query do RTL o normalizador colapsa, e espaço comum funciona |
| `window.location` é **não-configurável** no jsdom 29    | Use o seam `@/infra/navigation` (`redirectToLogin`); nunca `vi.spyOn(window.location, …)`                      |
| `useToast` tem fila global sem reset                    | `spyOnToast()` por padrão; fake timers só nos dois testes do próprio toast                                     |
| `infra/query-client.ts` é singleton com `retry: 3`      | Sempre `createTestQueryClient()`; nunca `app/providers.tsx`                                                    |
| `infra/session.ts` guarda o token por arquivo           | `clearSession()` no `afterEach` global já cuida; `vi.resetModules()` só para provar efeito de carga            |
| `/auth/*` não passa pela renovação do `api-client`      | 401 em `/auth/*` só rejeita: para provar renovação, use um recurso (ex.: `/users/me`) com token vencido        |
| `API_ORIGIN` do route handler é lido por requisição     | No `route.test.ts`, `vi.stubEnv("API_ORIGIN", …)` no `beforeEach` funciona (é lido em runtime, não no import)  |
| `tests/router.tsx` usa deep imports internos do Next    | Estão presos à versão `next@16.4.2`; se o Next subir, é o primeiro lugar a quebrar                             |

## Checklist

- [ ] Teste ao lado do fonte (ou em `tests/integration/` se for página).
- [ ] Título em pt-BR, minúsculo, verbo na 3ª pessoa; `describe` no padrão do tipo.
- [ ] `createTestQueryClient()` / `renderWithProviders`.
- [ ] `setup()` local em teste de hook, redeclarando o `QK` esperado.
- [ ] MSW com `seedDb` para estado e `mockApiError` para erro.
- [ ] Teste de service assertando `signatures(calls)` e `bodyOf(calls[0])`.
- [ ] Toast por spy (hook) ou por texto com `withToasts` (página).
- [ ] Consultas por papel e nome acessível em pt-BR.
- [ ] `npm run --prefix web test:coverage` passando os thresholds do glob correspondente.

## Não faça

- Não use `it("deve …")` — esse é o padrão do server, em inglês.
- Não aninhe `describe`.
- Não chame `userEvent.setup()`.
- Não use o `queryClient` singleton nem `app/providers.tsx`.
- Não use `container` fora do caso do skeleton.
- Não refaça no Vitest um caminho feliz que o E2E já cobre.
- Não gere dado aleatório em fixture.
- Não mocke `infra/session.ts` nem escreva `document.cookie` à mão para logar: use `loginAs()`.
- Não semeie `db.users` só para autenticar — `loginAs(user)` já insere o usuário.
