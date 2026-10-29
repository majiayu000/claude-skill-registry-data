---
name: web-arquitetura
description: Arquitetura do frontend Smaug (web/) — camadas UI → hooks → services → infra, estrutura por feature, política de import e alias, Server vs Client Component, proxy.ts com ?next=, o repasse /api (app/api/[...path]/route.ts com API_ORIGIN em runtime) e as anatomias de página do App Router (CRUD simples, tela de feature com assistente e Ficha, layout autenticado client e login RSC). Leia antes de criar qualquer arquivo em web/.
---

# Arquitetura do web

## Quando usar esta skill

Ao criar uma página, uma feature nova, ou sempre que a dúvida for "onde este arquivo vai" /
"posso importar isso daqui".

## Camadas (normativo — constituição, seção Frontend)

```
UI (components)
      ↓
Hooks
      ↓
Services / API Layer
      ↓
Infra / External
```

Sentido único. **A UI depende de hooks, não de services nem de infra.** Componentes não chamam
`apiClient`. Regra de negócio não vive dentro de JSX.

```
web/
  app/        App Router: (auth)/{login,cadastro}, (app)/{dashboard,receitas,despesas,categorias,historico,dados}
              + api/[...path]/route.ts (repasse /api → API)
  features/   auth · dashboard · receitas · despesas · categorias · historico · dados
              cada uma com components/ hooks/ services/ types/
  shared/     components (primitivos) · hooks · lib · types
  infra/      api-client · auth-refresh · session · api-error · navigation · router-adapter
              · query-client · file-download
  proxy.ts    (guarda de rotas; o antigo middleware da Next 15)
  tests/      harness do Vitest + testes de integração de página
```

## Imports

Aliases (declarados **em dois lugares**: `web/tsconfig.json` e `web/vitest.config.ts` — alias novo
exige editar os dois): `@/*` → `web/`, mais `@/features/*`, `@/shared/*`, `@/infra/*`.

**Regra real, observada no código:**

- **Relativo** quando fica dentro da mesma feature ou da mesma pasta de topo:
  `../services/DespesasService`, `../types`, `../lib/utils`, `./Modal`, `./session`.
- **Alias** ao cruzar fronteira de topo — mesmo de dentro de uma feature:
  `@/shared/hooks/useToast`, `@/infra/api-error`.
- **`app/` sempre alias**, nunca relativo.
- Testes são a exceção: alcançam o harness por caminho relativo longo
  (`../../../tests/render`).

Ordem dentro do arquivo (consistente, não imposta por lint):
react/next → terceiros → módulos com alias → módulos relativos → `import type` por último.

**Não existem barris de re-export.** Os únicos `index.ts` são `features/<f>/types/index.ts` e
`shared/types/index.ts`, e eles _contêm_ as declarações. Importe sempre o arquivo concreto:

```tsx
import { Button } from "@/shared/components/Button";
import { useExpenseMonth } from "@/features/despesas/hooks/useExpenseMonth";
```

## Cross-feature

Compartilhamento acontece por `@/shared` ou `@/infra`. Na prática o código admite **uma exceção**:

- ✅ **Tipos** de outra feature, quando o domínio realmente se relaciona:
  `features/despesas/types` importa `Category` de `@/features/categorias/types`;
  `HistoricoService` agrega tipos de `receitas` e `despesas` — é um agregador por desenho.
- ❌ **Componente, hook ou service** de outra feature. Quando uma segunda feature precisa dele,
  **promova para `shared/`** — foi o que aconteceu com `MonthYearSelect` (`shared/components/`), com
  a navegação de competência (`shared/hooks/useCompetenceNavigation.ts`) e com os blocos de extrato,
  assistente e Ficha usados por Receitas e Despesas (`shared/components/lancamentos/`).
- ❌ Hook de outra feature, nem para dado auxiliar: `DespesasScreen` precisa das categorias, mas
  quem chama `useCategories()` é a **página** `app/(app)/despesas/page.tsx`, que passa
  `categories` por prop.
- ❌ `shared/` importando de `features/` — **sem exceção**. `AppShell` e `Sidebar` recebem o usuário
  (`ShellUser { name }`) e as ações `onLogout`/`onLogoutAll` **por props**; quem chama `useAuth()` e
  liga as props é o layout `app/(app)/layout.tsx` (camada `app/`, que pode compor features).

## Server vs Client Component

Regra: **manter a fronteira RSC o mais baixa possível.** `"use client"` vai no componente que de
fato usa hook/estado/efeito/API de browser — sempre na **primeira linha**, seguida de linha em branco.

| Arquivo                                                                    | Diretiva         |
| -------------------------------------------------------------------------- | ---------------- |
| `app/layout.tsx` (shell + `metadata`)                                      | RSC              |
| `app/page.tsx` (só `redirect("/login")`)                                   | RSC              |
| `app/(app)/layout.tsx` (chama `useAuth` e liga o `AppShell`)               | `"use client"`   |
| `app/(auth)/layout.tsx`, `cadastro/page.tsx`                               | RSC              |
| `app/(auth)/login/page.tsx` (`async`, lê `searchParams`)                   | RSC              |
| `app/api/[...path]/route.ts` (repasse)                                     | route handler    |
| todas as `app/(app)/*/page.tsx`                                            | `"use client"`   |
| hooks de feature, `providers.tsx`, primitivos com estado                   | `"use client"`   |
| componentes de apresentação puros (`KpiCard`, `EntryRow`, `ConfirmDialog`) | **sem diretiva** |

`metadata` só existe em `app/layout.tsx`. Os providers globais (`QueryClientProvider`,
`ToastContainer`, devtools) vivem em `app/providers.tsx`, que consome o **singleton**
`queryClient` de `@/infra/query-client` — não crie `useState(() => new QueryClient())`.

**Não existem `loading.tsx`, `error.tsx` nem `not-found.tsx` no projeto** — e isso é deliberado
(o único route handler é o repasse `app/api/[...path]/route.ts`, descrito abaixo):

- Loading é early-return dentro da própria página client (`if (isLoading) return <Skeleton ... />`)
  ou dentro do container de feature (`LedgerLayout` mostra o esqueleto enquanto `ledger` é `undefined`).
- Erro de mutação vira **toast** (disparado pelo hook); erro de formulário vira bloco inline
  `<div className="rounded-lg border border-red bg-red-light p-3 text-sm text-red">`.
- `shared/components/ErrorBoundary.tsx` existe e é testado, mas **não está montado** em nenhum lugar.

## `proxy.ts`

Gate de rota server-side (na Next 16 o antigo `middleware` virou `proxy`; a função exportada é
`proxy`), lendo o **indicador `smaug_session`** que `infra/session.ts` escreve. O indicador não é
credencial (o refresh token está no cookie `httpOnly` da API) — ele só decide a rota:

```ts
const PUBLIC_ROUTES = ["/login", "/cadastro"];
const SESSION_HINT_COOKIE = "smaug_session";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isPublic = PUBLIC_ROUTES.some(
    (route) => pathname === route || pathname.startsWith(`${route}/`),
  );
  const hasSession = request.cookies.get(SESSION_HINT_COOKIE)?.value === "1";

  if (!isPublic && !hasSession) {
    // Leva a rota pretendida em `?next=` para o login devolver o usuário a ela (design D8). A raiz
    // não vai: depois do login ela cairia em `/dashboard` de qualquer jeito.
    const login = new URL("/login", request.url);
    if (pathname !== "/") login.searchParams.set("next", `${pathname}${request.nextUrl.search}`);
    return NextResponse.redirect(login);
  }

  if (isPublic && hasSession) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
```

- O `next` gravado aqui **não é confiável**: quem o usa é `safeDestination` (em
  `features/auth/hooks/useAuth.ts`), que só aceita caminho interno — recusa `//host`, `/\host`,
  espaço/controle em qualquer posição e qualquer valor cuja origem mude ao ser resolvido como URL.
- O matcher exclui `api`: o repasse não passa pelo gate (a API faz a própria autenticação).

## Repasse `/api` — `app/api/[...path]/route.ts`

O navegador só fala com a origem do web. `apiClient` usa `baseURL: "/api"`, e este route handler
repassa `/api/*` → `${API_ORIGIN}/*`, de modo que o cookie `smaug_refresh` emitido pela API vira
cookie da origem do web (sem CORS nem `withCredentials`):

```ts
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

async function forward(request: Request): Promise<Response> {
  const apiOrigin = process.env.API_ORIGIN?.replace(/\/+$/, "");
  if (!apiOrigin) return new Response(null, { status: 500 });

  const url = new URL(request.url);
  const target = `${apiOrigin}${url.pathname.slice("/api".length)}${url.search}`;
  const hasBody = request.method !== "GET" && request.method !== "HEAD";

  let upstream: Response;
  try {
    upstream = await fetch(target, {
      method: request.method,
      headers: upstreamRequestHeaders(request),
      body: hasBody ? await request.arrayBuffer() : undefined,
      redirect: "manual",
      cache: "no-store",
    });
  } catch {
    return new Response(null, { status: 502 });
  }

  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: downstreamResponseHeaders(upstream),
  });
}

export const GET = forward;
// HEAD, POST, PUT, PATCH, DELETE, OPTIONS = forward
```

Regras:

1. **`API_ORIGIN` é variável de servidor, lida a cada requisição** (sem `NEXT_PUBLIC_`): a mesma
   imagem serve a qualquer destino. Ausente → **500 sem corpo**; API inalcançável → **502 sem
   corpo** — ambos transitórios para o `api-client`, que não derruba a sessão.
2. Não troque por `rewrites()` em `next.config.ts`: reprovou no spike (congela o destino no
   `next build` e falhou em H2/H3 — `specs/010-autenticacao/plan.md`, seção do spike).
3. Destino montado de `request.url`, **não** de `params.path` (o path decodificado perderia
   `%2F`/`%20`).
4. Cabeçalhos de salto (`HOP_BY_HOP`) saem nos dois sentidos; `content-encoding` não é repassado (o
   `fetch` já descomprimiu); **cada `Set-Cookie` é reanexado separado** via `getSetCookie()`.
5. Corpo como `arrayBuffer` — o upload `text/csv` e o download do CSV atravessam byte a byte.
6. Testado em `route.test.ts` ao lado, com `@vitest-environment node` e `fetch` substituído por dublê.

## Anatomia de página — dois formatos (+ layouts de sessão)

### (a) Página CRUD simples — `app/(app)/categorias/page.tsx`

A página é o container: chama o hook, guarda o estado dos modais e dispara as mutations.

```tsx
"use client";

import { useState } from "react";
import { Plus, Tag } from "lucide-react";
import { useCategories } from "@/features/categorias/hooks/useCategories";
// componentes de feature → primitivos de shared → import type

export default function CategoriasPage() {
  const { data: categories, isLoading, create, update, remove } = useCategories();
  const [modal, setModal] = useState<null | "add" | "edit">(null);
  const [selected, setSelected] = useState<CategoryWithCount | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<CategoryWithCount | null>(null);

  const handleSave = (data: { name: string }) => {
    if (modal === "add") {
      create.mutate(data.name, { onSuccess: () => setModal(null) });
    } else if (modal === "edit" && selected) {
      update.mutate({ id: selected.id, name: data.name }, { onSuccess: () => setModal(null) });
    }
  };
  // ...
}
```

Regras:

1. **Um `useState` por modal, seleção e alvo de exclusão** (`selected`, `deleteTarget`).
2. **A mutação é disparada pela página**, fechando o modal num `onSuccess` local.
3. Renderização em três ramos: `isLoading ? <Skeleton/> : !data?.length ? <EmptyState/> : <lista>`.
4. Os modais ficam ao final, sempre montados, controlados por `isOpen`; o `ConfirmDialog` por
   `isOpen={!!deleteTarget}` com um `if (deleteTarget)` defensivo no `onConfirm` — é esse idioma
   que justifica o threshold relaxado de `app/**` no `vitest.config.ts`.
5. Container raiz: `className="p-4 sm:p-7 max-w-[1100px]"`.
6. O componente da página é `export default function <Rota>Page()`.

### (b) Tela de feature — Receitas e Despesas

Quando a tela tem navegação, assistente e Fichas, a página só monta a tela da feature
(`app/(app)/receitas/page.tsx` é `return <ReceitasScreen />;`). Despesas passa as categorias:

```tsx
export default function DespesasPage() {
  const categories = useCategories();
  return <DespesasScreen categories={categories.data ?? []} />;
}
```

`features/despesas/components/DespesasScreen.tsx` é o container:

```tsx
type ModalState =
  | null
  | { t: "new" }
  | { t: "edit"; item: OneTimeExpenseMonthItem }
  | { t: "item"; item: ExpenseMonthItem; status: CompetenceStatus };

export function DespesasScreen({ categories }: DespesasScreenProps) {
  const [modal, setModal] = useState<ModalState>(null);
  const nav = useLedgerNavigation();
  const month = useExpenseMonth(nav.selected);
  const summary = useExpenseYearSummary(nav.selected.year);
  nav.adoptReference(month.data?.reference ?? summary.data?.reference);

  return (
    <LedgerLayout /* textos, navigation={nav}, ledger={month.ledger}, onNew, onOpen */>
      {(modal?.t === "new" || modal?.t === "edit") && <ExpenseWizard /* ... */ />}
      {modal?.t === "item" && <ExpenseFicha /* ... */ />}
    </LedgerLayout>
  );
}
```

Regras:

1. **Um único `ModalState`**, união discriminada por `t` com `null`; o que o modal precisa (item,
   situação da competência) vai **dentro** do estado, não em `useState`s paralelos.
2. Modais são **montados condicionalmente** (`modal?.t === "..." && <X />`): assistente e Ficha
   nascem com o estado inicial certo a cada abertura.
3. **Quem dispara a mutation é o hook do assistente ou da Ficha** (`useExpenseWizard`,
   `useExpenseMutations({ onSuccess })`), não a tela.
4. O "agora" vem do servidor (`reference` da consulta), adotado via `nav.adoptReference(...)` durante
   o render — nunca `new Date()` na tela.
5. Layout, faixa de meses, resumo, lista, estado vazio e erro vêm de `LedgerLayout`
   (`shared/components/lancamentos/`); a tela de feature só fornece textos, dados e modais.

### (c) Layout autenticado e páginas de `(auth)`

`app/(app)/layout.tsx` é **client** e é o ponto onde a sessão é retomada e o menu recebe o usuário:

```tsx
"use client";

import { AppShell } from "@/shared/components/AppShell";
import { useAuth } from "@/features/auth/hooks/useAuth";

/**
 * Layout cliente das rotas autenticadas: é aqui (camada `app/`, que pode compor features) que a
 * sessão é retomada e o menu recebe o usuário e as ações de saída — `shared/` não conhece `auth`.
 */
export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, logout, logoutAll } = useAuth();
  return (
    <AppShell user={user} onLogout={logout} onLogoutAll={logoutAll}>
      {children}
    </AppShell>
  );
}
```

`app/(auth)/login/page.tsx` é **Server Component `async`** e lê o `?next=` de `searchParams`
(no Next 16, uma `Promise`), repassando ao formulário por prop:

```tsx
interface LoginPageProps {
  searchParams: Promise<{ next?: string | string[] }>;
}

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const { next } = await searchParams;
  return (
    // ... cartão com logo e texto
    <LoginForm next={typeof next === "string" ? next : null} />
  );
}
```

`cadastro/page.tsx` é RSC simples que monta `<RegisterForm />` — o cadastro já abre a sessão e vai
para `/dashboard`.

## Checklist — criar uma feature nova

- [ ] `features/<nome-pt-br>/{components,hooks,services,types}`.
- [ ] `types/index.ts` com as interfaces de domínio; `types/schemas.ts` só se houver formulário RHF.
- [ ] `services/<Feature>Service.ts` (skill `web-feature-services`).
- [ ] `hooks/use<Coisa>.ts` (skill `web-feature-hooks`).
- [ ] Componentes (skill `web-componentes`): apresentacionais, e containers só no formato (b).
- [ ] Página em `app/(app)/<rota>/page.tsx` com `"use client"` — a proteção vem de graça do
      `proxy.ts` e do layout de `(app)`; não verifique sessão na página.
- [ ] Rota acrescentada à navegação (`shared/components/Sidebar.tsx` / `BottomNav.tsx`).
- [ ] Teste ao lado de cada fonte + integração de página em `web/tests/integration/` (skill `web-testes`).

## Não faça

- Não chame `apiClient` de dentro de um componente.
- Não importe `useRouter`/`useSearchParams` de `next/navigation` em hook de negócio — use
  `@/infra/router-adapter`.
- Não crie barril `index.ts` de re-export.
- Não importe componente/hook/service de outra feature.
- Não crie `loading.tsx`/`error.tsx` — siga o padrão de early-return + toast.
- Não crie outro route handler para falar com a API nem use `rewrites()`: tudo passa pelo repasse
  `app/api/[...path]/route.ts`.
- Não exponha o endereço da API ao browser (`NEXT_PUBLIC_*`): o destino é `API_ORIGIN`, só no servidor.
- Não use `useSearchParams` num hook que roda no layout de `(app)` (exigiria `<Suspense>` e tiraria o
  menu do SSR) — leia `searchParams` na página Server Component e passe por prop, como faz o login.
- Não navegue para um `next` vindo da URL sem `safeDestination` (redirecionamento aberto).
- Não instancie um `QueryClient` novo em `providers.tsx`.
