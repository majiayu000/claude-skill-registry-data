---
name: web-infra
description: Camada infra do web do Smaug — api-client (baseURL "/api", Bearer, renovação silenciosa, só 401 encerra sessão), auth-refresh (single-flight por aba), session.ts (access token em memória + indicador smaug_session), tabela de mensagens de api-error.ts e sua ordem de resolução, navigation.ts como seam de teste, router-adapter e query-client.
---

# `infra/` — cliente HTTP, sessão, renovação, erros e navegação

## Quando usar esta skill

Ao mexer em `web/infra/*`, ao adicionar um código de erro da API, ou quando precisar de sessão,
navegação ou configuração do TanStack Query. O repasse `/api` em si (route handler do App Router)
está descrito na skill `web-arquitetura`.

## Mapa da sessão (quem guarda o quê)

| Peça                | Onde vive                                                              | Quem lê                                 |
| ------------------- | ---------------------------------------------------------------------- | --------------------------------------- |
| refresh token       | cookie `httpOnly` `smaug_refresh` (emitido pela API, `Path=/api/auth`) | só o navegador/servidor — nenhum script |
| access token        | variável de módulo em `infra/session.ts` (**só memória**)              | interceptor do `apiClient`              |
| indicador de sessão | cookie `smaug_session=1` (sem segredo, escrito por `session.ts`)       | `proxy.ts` e o bootstrap do `useAuth`   |

**A fonte da verdade é o servidor.** Recarregar a página perde o access token; a sessão é retomada
por uma renovação (`POST /auth/refresh`) que o cookie `httpOnly` autentica sozinho.

## `infra/session.ts` — token em memória + indicador

```ts
const HINT_COOKIE = "smaug_session";
const LEGACY_COOKIE = "userId";
const HINT_MAX_AGE_SECONDS = 30 * 24 * 60 * 60;

let accessToken: string | null = null;

function writeCookie(name: string, value: string, maxAge: number): void {
  document.cookie = `${name}=${value};path=/;max-age=${maxAge};SameSite=Lax`;
}

if (typeof document !== "undefined") writeCookie(LEGACY_COOKIE, "", 0);

/** Access token da aba, ou `null` quando ainda não houve login/renovação. */
export function getAccessToken(): string | null {
  return accessToken;
}

/** Guarda o access token em memória e escreve o indicador de sessão. */
export function setSession(token: string): void {
  accessToken = token;
  if (typeof document === "undefined") return;
  writeCookie(HINT_COOKIE, "1", HINT_MAX_AGE_SECONDS);
}

/** Esquece o access token e apaga o indicador de sessão. */
export function clearSession(): void; // accessToken = null + indicador com max-age=0

/** Indica se o navegador tem o indicador de sessão — usado para decidir se vale renovar. */
export function hasSessionHint(): boolean; // document.cookie contém "smaug_session=1"
```

- **O access token nunca vai para cookie, `localStorage` nem `sessionStorage`.**
- O indicador vive 30 dias (vida máxima da sessão, PRD RN-07): um cookie de sessão do browser sumiria
  ao fechá-lo e mandaria para `/login` quem ainda tem refresh válido.
- O indicador pode divergir do estado real (refresh expirado com indicador presente) **sem recriar o
  laço `/login` ↔ `/dashboard`**, porque o único caminho que encerra a sessão — renovação recusada com
  401 — chama `clearSession()` **antes** de `redirectToLogin()`.
- O cookie `userId` da versão anterior (login por id) é apagado no carregamento do módulo; não o leia.
- Guardas de SSR (`typeof document === "undefined"`) em tudo que toca `document`; cobertas por
  `infra/session.node.test.ts` (`@vitest-environment node`).

## `infra/auth-refresh.ts` — renovação single-flight por aba

```ts
/** Caminho da renovação visto pelo navegador: o repasse `/api` do web, na mesma origem. */
export const REFRESH_URL = "/api/auth/refresh";

const CONFLICT_RETRY_DELAY_MS = 250;

let inFlight: Promise<AuthSession> | null = null;

async function postRefresh(): Promise<AuthSession> {
  const { data } = await axios.post<AuthSession>(REFRESH_URL, undefined, { timeout: 10000 });
  return data;
}

async function renew(): Promise<AuthSession> {
  try {
    let session: AuthSession;
    try {
      session = await postRefresh();
    } catch (error) {
      if ((error as AxiosError).response?.status !== 409) throw error;
      await wait(CONFLICT_RETRY_DELAY_MS);
      session = await postRefresh();
    }
    setSession(session.accessToken);
    return session;
  } catch (error) {
    // Só a renovação recusada com 401 encerra a sessão. O indicador sai ANTES do redirect, senão o
    // proxy devolveria o usuário a `/dashboard` e recriaria o laço com `/login`.
    if ((error as AxiosError).response?.status === 401) {
      clearSession();
      redirectToLogin();
    }
    throw error;
  }
}

export function refreshSession(): Promise<AuthSession> {
  inFlight ??= renew().finally(() => {
    inFlight = null;
  });
  return inFlight;
}

export async function settleRefresh(): Promise<void> {
  await inFlight?.catch(() => undefined);
}
```

Regras:

1. **Usa `axios` puro, não o `apiClient`**: o interceptor do `apiClient` depende deste módulo, e a
   renovação não leva Bearer nem pode disparar outra renovação. O cookie vai sozinho (mesma origem,
   sem `withCredentials`).
2. **Single-flight por aba**: chamadas simultâneas a `refreshSession()` recebem a mesma promessa.
3. **409 `REFRESH_TOKEN_CONFLICT`** (outra aba girou o token) → espera 250 ms e tenta **uma** vez.
4. **401** → `clearSession()` e depois `redirectToLogin()`, e rejeita. **Rede/5xx só rejeitam**, sem
   encerrar nada.
5. `settleRefresh()` espera a renovação em voo **sem propagar a falha** — é o que o interceptor de
   request usa para sair com o token mais novo.
6. Exporta também os tipos `SessionUser` e `AuthSession` (corpo de `/auth/register|login|refresh`).

## `infra/api-client.ts` — a única instância axios

```ts
const apiClient = axios.create({
  baseURL: "/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

interface RetriableConfig extends InternalAxiosRequestConfig {
  /** Marca a requisição que já foi refeita, para não renovar em laço. */
  _retried?: boolean;
  /** Access token com que a requisição saiu (`null` sem sessão em memória). */
  _sentToken?: string | null;
}

apiClient.interceptors.request.use(async (config: RetriableConfig) => {
  await settleRefresh();
  const token = getAccessToken();
  config._sentToken = token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as RetriableConfig | undefined;
    // 401 em `/auth/*` (login errado, renovação recusada) não é "token expirado": só rejeita.
    const isAuthRoute = original?.url?.startsWith("/auth/") ?? false;
    if (error.response?.status !== 401 || !original || isAuthRoute || original._retried) {
      return Promise.reject(error);
    }

    const current = getAccessToken();
    if (current === null || current === original._sentToken) {
      await refreshSession();
    }
    original._retried = true;
    return apiClient(original);
  },
);
```

Regras:

1. **`baseURL: "/api"`** — o navegador só fala com a origem do web; o route handler
   `app/api/[...path]/route.ts` repassa para a API (`API_ORIGIN`, lido em runtime). Por isso **não há
   `withCredentials` nem CORS** do lado do browser, e o cookie `smaug_refresh` vai sozinho.
2. **Bearer injetado aqui**, lendo `getAccessToken()`. Nenhum service monta header de autenticação.
3. O request interceptor é **`async`**: `await settleRefresh()` faz a requisição que sai durante
   uma renovação esperar o token novo, em vez de sair sem ele e voltar 401. O token enviado fica
   gravado em `config._sentToken`.
4. **401 fora de `/auth/*`**:
   - se o token atual **difere** do enviado (outra requisição já renovou) → **refaz com o atual, sem
     renovar** — renovar de novo giraria o refresh à toa e daria 409 na outra aba;
   - se é o mesmo (ou não há token) → `refreshSession()` e refaz **uma vez** (`_retried`).
5. **401 em `/auth/*` só rejeita** (login errado, logout-all com token vencido — quem chama decide).
6. **Só 401 encerra a sessão, e só por `refreshSession()`.** Rede fora, timeout e 5xx (inclusive o
   500/502 do repasse) são transitórios — o erro chega a quem chamou e a sessão continua.

## `infra/api-error.ts` — a tabela de mensagens

Estrutura: uma `const MESSAGES: Record<string, string>` **privada**, com cabeçalho JSDoc
`/** Mensagens em pt-BR para os códigos de erro emitidos pela API. */`, agrupada por blocos
separados por linha em branco, nesta ordem: genéricos (validação, `UNAUTHORIZED`, origem, rate
limit) → autenticação → usuário → categoria → "não encontrado" → regras de data → estado →
parcelamento → exportação/importação. ~50 entradas. A chave é o `error` SCREAMING_SNAKE que o server
devolve; o valor é uma frase completa em pt-BR terminando em ponto.

```ts
const MESSAGES: Record<string, string> = {
  VALIDATION_ERROR: "Dados inválidos. Revise os campos e tente novamente.",
  UNAUTHORIZED: "Sessão inválida. Faça login novamente.",
  ORIGIN_NOT_ALLOWED: "Origem da requisição não permitida. Recarregue a página e tente novamente.",
  TOO_MANY_REQUESTS: "Muitas tentativas. Aguarde alguns minutos e tente novamente.",

  INVALID_CREDENTIALS: "E-mail ou senha incorretos.",
  INVALID_REFRESH_TOKEN: "Sua sessão expirou. Faça login novamente.",
  REFRESH_TOKEN_CONFLICT: "Não foi possível renovar a sessão. Tente novamente.",

  USER_NOT_FOUND: "Usuário não encontrado.",
  EMAIL_ALREADY_EXISTS: "Já existe uma conta com este e-mail.",
  // ...
  IMPORT_NO_VALID_ROWS: "O arquivo não contém nenhum lançamento válido.",
};
```

Funções exportadas, todas recebendo `error: unknown` (ou código) e fazendo o cast internamente:

```ts
export function isInvalidSessionError(error: unknown): boolean {
  return (error as AxiosError)?.response?.status === 401;
}

export function getApiErrorMessage(error: unknown, fallback: string): string;
export function getErrorMessageByCode(code: string, fallback: string): string; // guarda do cliente
export function getImportRowMessage(code: string, value?: string): string; // linhas recusadas
```

**`isInvalidSessionError` é só 401.** 404 (inclusive `USER_NOT_FOUND`), timeout, rede e 5xx são
transitórios ou de negócio e não deslogam ninguém.

**Ordem de resolução de `getApiErrorMessage` (decore, os testes dependem dela):**

0. O corpo passa por `parseErrorBody` — que decodifica `ArrayBuffer`/string JSON (o download do CSV
   usa `responseType: "arraybuffer"`).
1. Se o corpo tem `error === "VALIDATION_ERROR"` **e** `details`, devolve o **primeiro detalhe de
   campo** (`Object.values(body.details).flat()[0]`).
2. Senão, procura `MESSAGES[body.error]`.
3. `code === "ECONNABORTED"` → `"A requisição demorou demais. Verifique sua conexão e tente novamente."`
4. Sem `response` mas com `request` (offline) → `"Não foi possível falar com o servidor. Verifique sua conexão."`
5. Caso contrário, o `fallback` que o chamador passou.

**Regra operacional**: código de erro novo no server entra nessa tabela **no mesmo PR**. Sem isso o
usuário vê o texto genérico de fallback. Nunca escreva a mensagem à mão dentro de um componente ou
hook — sempre `getApiErrorMessage(error, "Erro ao ….")`.

## `infra/navigation.ts` — seam de teste

```ts
/** Manda o usuário para o login, a menos que ele já esteja lá. */
export function redirectToLogin(): void {
  if (typeof window === "undefined") return;
  if (window.location.pathname === "/login") return;
  // A troca de documento é proposital: descarta o cache do React Query da sessão encerrada.
  // eslint-disable-next-line @next/next/no-location-assign-relative-destination
  window.location.href = "/login";
}
```

Existe porque `window.location` **não é configurável no jsdom 29** — não dá para espionar. Toda
navegação "dura" passa por aqui (renovação recusada, logout, logout-all), e os testes fazem mock
deste módulo (`vi.mock("@/infra/navigation", () => ({ redirectToLogin: vi.fn() }))`).

## `infra/router-adapter.ts` — Next atrás de uma interface

```ts
"use client";

export interface RouterAdapter {
  push: (path: string) => void;
  replace: (path: string) => void;
  back: () => void;
}

export function useRouter(): RouterAdapter;
export function useSearchParams(); // { get(key), getAll(key) }
```

**Hook de negócio nunca importa `useRouter`/`useSearchParams` de `next/navigation`** — é regra
normativa da constituição (princípio III do frontend). Passe por este adapter.
(`Sidebar.tsx` importa `usePathname` direto porque o adapter não cobre esse caso; se precisar dele
em hook, estenda o adapter.) O `?next=` do login **não** é lido por `useSearchParams`: a página de
login (Server Component) o lê de `searchParams` e passa por prop — ver `web-arquitetura`.

## `infra/query-client.ts` — singleton

```ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000,
      gcTime: 5 * 60 * 1000,
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
    },
    mutations: { retry: 1 },
  },
});
```

Consumido por `app/providers.tsx`. **Nunca use este singleton em teste** — use
`createTestQueryClient()` (skill `web-testes`), senão o `retry: 3` faz os testes de erro pendurarem.

## Estilo da pasta

Arquivos planos, **kebab-case** (`api-client.ts`, `api-error.ts`, `auth-refresh.ts`,
`router-adapter.ts`, `query-client.ts`, `file-download.ts`), só exports nomeados, sem barril, imports
internos relativos (`./session`, `./auth-refresh`).

## Checklist — adicionar um código de erro novo

- [ ] Classe de erro no `server/src/domain/errors/domain-error.ts` (skill `server-erros-dominio`).
- [ ] Controller (ou middleware) mapeando para o status certo.
- [ ] Entrada em `MESSAGES` de `infra/api-error.ts`, no bloco temático correspondente, em pt-BR,
      terminando em ponto.
- [ ] Teste em `infra/api-error.test.ts`.
- [ ] Se algum fluxo de tela depender dele, teste de integração de página assertando a mensagem.
- [ ] Se for um 401, confira que ele **deve** encerrar a sessão (só a renovação recusada encerra).

## Não faça

- Não crie uma segunda instância de axios (a única exceção é o `axios.post` puro de
  `auth-refresh.ts`, que não pode passar pelo interceptor).
- Não chame a API pelo domínio dela (`http://localhost:3000`, `API_ORIGIN`) a partir do browser —
  tudo sai por `/api`.
- Não deslogue o usuário em erro de rede, timeout, 404 ou 5xx.
- Não chame `refreshSession()` fora do interceptor e do `useAuth` (bootstrap e `logoutAll`).
- Não guarde o access token em cookie, `localStorage` ou `sessionStorage`; não leia o cookie
  `smaug_refresh` (é `httpOnly`) nem trate `smaug_session` como credencial.
- Não redirecione para `/login` sem antes `clearSession()` — o indicador presente recriaria o laço
  com `/dashboard`.
- Não espione `window.location` no teste — use o seam `@/infra/navigation`.
- Não importe `next/navigation` em hook de negócio.
- Não use o `queryClient` singleton em teste.
