---
name: testes-e2e
description: Como escrever testes E2E do Smaug com Playwright no pacote e2e/ — caixa-preta sem importar server/web, fixtures test.ts + scenarios.ts em vez de page objects, seletores por papel, SeedClient por HTTP com Bearer (cadastro/login com senha, importCsv para dado passado), signInBrowser pelo cookie de refresh, access token de 20 s e competência congelada.
---

# Testes E2E (Playwright)

## Quando usar esta skill

Ao escrever ou alterar qualquer coisa em `e2e/`.

```bash
npm run e2e:install-browsers    # uma vez por máquina
npm run test:e2e                # cria SQLite exclusivo do run, roda, descarta
npm run test:e2e:ui
npm run test:e2e:report
node e2e/scripts/run-e2e.mjs --grep "sessão" --project desktop-chromium   # com flags
```

`npm run test:e2e -- --grep x` **não funciona**: o `npm run --prefix e2e test` intermediário
consome a flag. Só caminho posicional atravessa (`npm run test:e2e -- tests/smoke.spec.ts`). Para
qualquer flag do Playwright (`--grep`, `--project`, `--headed`, `--repeat-each`), chame o wrapper
direto; ele repassa tudo, exceto `--keep-db`, que consome.

## A regra que define o pacote: caixa-preta

`e2e/` **não importa nada de `server/` nem de `web/`** — a regra `no-e2e-to-src` do
`.dependency-cruiser.js` é `error`. Ele fala só HTTP e DOM. Por isso existe
`src/support/month-names.ts` duplicando nomes de mês em vez de importar do `web/` — e o arquivo diz
isso no cabeçalho.

`e2e/package.json` tem só três devDeps (`@playwright/test`, `@types/node`, `typescript`): a
restrição é imposta no nível da dependência.

## Estrutura

```
e2e/
  playwright.config.ts · scripts/run-e2e.mjs · README.md
  src/
    api/         seed-client.ts · types.ts
    config/      env.ts
    fixtures/    test.ts · scenarios.ts
    support/     ui.ts · competence.ts · format.ts · month-names.ts
    global-setup.ts · global-teardown.ts
  tests/
    smoke.spec.ts
    auth/ · dados/ · dashboard/ · despesas/ · historico/ · lancamentos/ · receitas/ · responsive/
```

## As quatro regras do `e2e/README.md`

> - **Nunca** literais de mês/ano. Tudo deriva de `competence.current`, congelada no `globalSetup`
>   e propagada por env para todos os workers.
> - **Nunca** semear no passado pelos `create-*`: a API rejeita competência passada. A situação de
>   cada mês (passado/atual/futuro, parcela paga, série encerrada) é calculada pelo **servidor**, com
>   o relógio dele — mexer no relógio do browser não muda nada. Para ter dado passado (um
>   parcelamento já em andamento), importe-o: `seed.importCsv([...])` é o único escritor que
>   dispensa a trava de passado.
> - Valores de parcela são assertados contra o que a API devolveu, nunca contra literais — o
>   arredondamento é regra de domínio.
> - Este pacote é **caixa-preta**: não importa nada de `server/` nem de `web/`.

## Não existem page objects

A estrutura real é em três camadas:

1. **`src/fixtures/test.ts`** — `test = base.extend<Options & Fixtures>({...})` com
   `authenticate` (opção, default `true`), `apiRequest` (contexto de request com `baseURL` na
   **API**, não no web), `seedUser`, `seed` (`SeedClient` com o access token do `seedUser`),
   `context` sobrescrito (aborta Google Fonts e, se `authenticate`, chama `signInBrowser`) e
   `competence`. Exporta também `signInBrowser`, a interface `SeedUser` e a constante
   `SESSION_HINT_COOKIE` (`"smaug_session"`).
   - `seedUser` é **um usuário novo por teste** — `POST /auth/register` com nome
     `E2E ${testInfo.title.slice(0, 40)}`, e-mail `e2e-<uuid>@e2e.local` e senha
     `senha-<uuid>` — e entrega `{ id, name, email, password, session }`: o perfil, a senha em
     claro (para os testes que digitam no `/login`) e a `OpenedSession` **do seed**. Um usuário por
     teste é o que permite `fullyParallel` sem truncar tabela.
   - O navegador recebe uma **sessão separada** da do seed (ver `signInBrowser` abaixo): o "Sair"
     da tela revoga só a dele, e o `seed` continua valendo para asserção depois do logout.
     **Não há fixture de relógio** (`shiftClock` foi removido): desde que a situação das competências
     passou a vir do servidor, `page.clock` não altera "Paga", "Atual" nem "Encerrada".
     O módulo faz `export { expect };` — **o spec importa `expect` e `test` daqui, nunca de
     `@playwright/test`.**
2. **`src/fixtures/scenarios.ts`** — builders em pt-BR `cenarioX(seed, k: CompetenceKit, options?)`,
   cada um com uma `interface CenarioX` de retorno, **devolvendo tudo que criaram** para o spec
   assertar contra a resposta do servidor. Existem: `cenarioDashboardCompleto`,
   `cenarioReceitaFixaVersionada`, `cenarioRecorrenteVersionada`, `cenarioHistoricoMisto`,
   `cenarioCategoriaComVinculo`, `cenarioParcelamento`.
3. **`src/support/ui.ts`** — só o que é **estrutural** na UI: `goto(page, path)` (goto + espera de
   hidratação), `waitForHydration`, `dialog(page)`, `ficha(page, descrição)` (o diálogo da Ficha pelo
   nome acessível), `monthStrip(page)` (faixa de 12 meses), `kpiCard(page, label)`, `monthBadge`,
   `panel`, `hideDevOverlays`, `documentOverflow`.
   Cópia de texto **fica no spec**, para a asserção ser legível no ponto de uso.

### `signInBrowser` — login do navegador sem passar pela tela

Copiado de `e2e/src/fixtures/test.ts`:

```ts
export async function signInBrowser(
  context: BrowserContext,
  api: APIRequestContext,
  user: Pick<SeedUser, "email" | "password">,
  baseURL: string,
): Promise<OpenedSession> {
  const session = await new SeedClient(api).login(user.email, user.password);
  const domain = new URL(baseURL).hostname;
  await context.addCookies([
    {
      name: REFRESH_COOKIE,
      value: session.refreshToken,
      domain,
      path: "/api/auth",
      httpOnly: true,
      sameSite: "Strict",
      secure: false,
    },
    {
      name: SESSION_HINT_COOKIE,
      value: "1",
      domain,
      path: "/",
      httpOnly: false,
      sameSite: "Lax",
      secure: false,
    },
  ]);
  return session;
}
```

- Abre uma sessão **nova** por `POST /auth/login` e põe no contexto o cookie de refresh
  `smaug_refresh` e o indicador `smaug_session=1`. Não há access token no navegador: ao abrir a
  primeira página protegida o web renova em silêncio (`POST /api/auth/refresh`), exatamente como
  numa recarga real.
- `smaug_refresh` vai no **domínio do web** com `path: "/api/auth"` — o par que o navegador enviaria
  ao repasse `/api/auth/refresh` —, `httpOnly` e `SameSite=Strict`, como a API o emite. O indicador
  vai em `path: "/"`, legível pela página, porque é ele que o `proxy.ts` lê.
- Use `domain` + `path`, nunca `url`: o Playwright recusa os dois juntos.
- Para um "segundo dispositivo", crie outro contexto e chame `signInBrowser` nele
  (`tests/auth/sessao.spec.ts`, "sair de todos os dispositivos…"): cada chamada é uma sessão
  independente do mesmo usuário.

Helper específico de um arquivo fica no próprio spec, com JSDoc:

```ts
/** A linha do extrato é um botão cujo nome acessível começa pela descrição. */
function linha(page: Page, description: string): Locator {
  return page.getByRole("button", { name: new RegExp(`^${description}`) });
}
```

## Seletores

**Primário: papel, rótulo e texto** — `getByRole("tab"|"button"|"dialog"|"heading")`, `getByLabel`,
`getByPlaceholder`, `getByText`.

**`data-testid` só para card repetido que não tem papel próprio.** Resta exatamente um:
`category-card`. As linhas do extrato de Receitas/Despesas são botões e as Fichas são diálogos
nomeados pela descrição — consulte-os por papel (`ficha(page, "Notebook")`). Duas armadilhas da
Ficha: há dois botões "Fechar" (o × e o do rodapé — use `.last()`), e `getByText("Mês atual")`
precisa de `{ exact: true }` por causa do botão "Voltar para o mês atual".

`exact: true` também é obrigatório onde um rótulo novo passou a conter outro:

- O menu do shell tem **"Sair"** e **"Sair de todos os dispositivos"** — clique em "Sair" com
  `getByRole("button", { name: "Sair", exact: true })`. O mesmo item quebrou o filtro do Histórico:
  `getByRole("button", { name: "Todos" })` casa "Sair de todos os dispositivos" (o nome acessível é
  comparado por substring e sem caixa), por isso `tests/historico/historico.spec.ts` usa
  `{ name: "Todos", exact: true }`.
- No cadastro, `getByLabel("Senha", { exact: true })`, porque "Confirmar senha" também casaria.

Ao acrescentar texto na UI (botão, item de menu), rode a suíte inteira: um seletor sem `exact` em
outra tela pode passar a casar dois elementos.

**Sempre `goto(page, "/despesas")` do `support/ui.ts`, nunca `page.goto` direto** — a exceção são
os testes de guarda de rota, que querem justamente observar o redirecionamento.

## Seeding — `SeedClient` (`src/api/seed-client.ts`)

Semeia **exclusivamente por HTTP**, nunca escrevendo no SQLite (os ids são `String @id` sem
`@default`, há estado derivado como `nameLower` e a expansão de parcelas, e um segundo escritor
SQLite quebraria os workers paralelos).

Construtor `(api: APIRequestContext, accessToken?: string)`, `asUser(accessToken)` (devolve um
`SeedClient` novo com outro token), getter privado `headers` emitindo
``{ Authorization: `Bearer ${this.accessToken}` }`` (ou `{}` sem token), e um `unwrap<T>` que grita
quando o seed falha:

```ts
private async unwrap<T>(res: APIResponse, what: string): Promise<T> {
  if (!res.ok()) {
    const body = await res.text().catch(() => "<sem corpo>");
    throw new Error(`[seed] ${what} → HTTP ${res.status()}\n${body}`);
  }
  return (await res.json()) as T;
}
```

Métodos agrupados por comentário-faixa (`// ---- usuários`, `// -------- categorias`, …).
Variantes `...Raw` existem onde o teste assere a falha (`deleteCategoryRaw`).

**Usuários: `register` e `login` devolvem `OpenedSession`** — o corpo
`{ accessToken, tokenType: "Bearer", expiresIn, user }` (`AuthSessionDto` em `src/api/types.ts`)
mais o `refreshToken`, tirado do `Set-Cookie`. Ambos falam direto com a API (sem o repasse `/api`
do web) e sem `Origin`, que a guarda de origem de `/auth/*` aceita. Copiado de
`e2e/src/api/seed-client.ts`:

```ts
private async openedSession(res: APIResponse, what: string): Promise<OpenedSession> {
  const session = await this.unwrap<AuthSessionDto>(res, what);
  const prefix = `${REFRESH_COOKIE}=`;
  const cookie = res
    .headersArray()
    .find((h) => h.name.toLowerCase() === "set-cookie" && h.value.startsWith(prefix));
  if (!cookie) throw new Error(`[seed] ${what} → resposta sem o cookie ${REFRESH_COOKIE}`);
  return { ...session, refreshToken: cookie.value.slice(prefix.length).split(";")[0] };
}
```

Use `res.headersArray()`, não `res.headers()`: com mais de um `Set-Cookie` o objeto os junta.

**O seed não renova.** A API do run emite access tokens de **20 s** (`ACCESS_TOKEN_TTL_SECONDS`
em `src/config/env.ts`, mais 5 s de tolerância de relógio da API), e o `seed` usa o token do
cadastro feito no início do teste. Semeie **no começo** do teste: um seed feito mais de ~25 s
depois do cadastro volta 401. Se um teste precisar semear depois de uma espera longa, abra uma
sessão nova (`new SeedClient(apiRequest).login(seedUser.email, seedUser.password)`) e semeie com o
token dela — não aumente o TTL global.

**Dado no passado: `importCsv(rows)`.** Recebe as linhas do CSV sem cabeçalho (o método acrescenta
BOM, cabeçalho e CRLF) e posta em `/data/import`. Monte a competência com `csvCompetence(...)` de
`support/format.ts`:

```ts
// A situação das parcelas vem do relógio do SERVIDOR; o único jeito de ter
// uma parcela já paga é importar a série com o 1º mês no passado.
await seed.importCsv([
  `${csvCompetence(competence.prev)};despesa;Eletrônicos;Notebook;33,34;parcelada;1;3;s1;`,
  `${csvCompetence(competence.current)};despesa;Eletrônicos;Notebook;33,33;parcelada;2;3;s1;`,
  `${csvCompetence(competence.next)};despesa;Eletrônicos;Notebook;33,33;parcelada;3;3;s1;`,
]);
```

## Estilo do spec

```ts
import type { Page } from "@playwright/test";
import { cenarioParcelamento } from "../../src/fixtures/scenarios.js";
import { expect, test } from "../../src/fixtures/test.js";
import { brl, cellAmount, csvCompetence } from "../../src/support/format.js";
import { dialog, ficha, goto } from "../../src/support/ui.js";

test.describe("despesas parceladas", () => {
  test("a Revisão divide R$ 100,00 em 3× com os centavos na 1ª e o servidor grava o mesmo", async ({
    page,
    seed,
  }) => {
    await seed.createCategory("Eletrônicos");
    await goto(page, "/despesas");
    await page.getByRole("button", { name: "Nova despesa" }).click();
```

- **Import relativo com extensão `.js` obrigatória** (ESM + `moduleResolution: "Bundler"`).
- Títulos de `test.describe` e `test` em **pt-BR, minúsculos, linguagem de domínio**
  (`"cria um parcelamento e o card resume o plano"`,
  `"bloqueia primeira parcela em competência passada"`).
- Fixtures desestruturadas na assinatura: `async ({ page, seed, competence })`.
- `test.use({ authenticate: false })` dentro de um `describe` aninhado para casos não autenticados.
- Dinheiro via `brl(...)` (ou `compact`/`cellAmount` na faixa e nas células), mês via
  `monthShort(...)` / `monthLong(...)` / `monthTitle(...)` — **nunca literal**.
- Tabela de rotas vira laço:
  ```ts
  for (const route of APP_ROUTES) {
    test(`visitante em ${route} é mandado para o login`, async ({ page }) => { ... });
  }
  ```
- `expect.poll` para estado eventualmente consistente (limpeza de cookie, tamanho de lista).

## Configuração

`playwright.config.ts`: `fullyParallel: true`, `retries` 2 no CI, `workers` 2 no CI / 4 local,
`timeout: 60_000`, `expect.timeout: 10_000`, `trace: "on-first-retry"`,
`screenshot: "only-on-failure"`, `video: "retain-on-failure"`, `navigationTimeout: 45_000`
(o `next dev` compila sob demanda), `locale: "pt-BR"`, `timezoneId: "UTC"`.

Projetos: `desktop-chromium` (1280×800, ignora `**/*.mobile.spec.ts`) e `mobile-chromium`
(Pixel 5, casa `**/*.mobile.spec.ts`) — **o infixo `.mobile.spec.ts` é o seletor de projeto**.
`firefox` e `webkit` (desktop, também ignorando `.mobile.spec.ts`) só entram com
`E2E_ALL_BROWSERS` setada. Os dois `webServer` usam `reuseExistingServer: false`: nunca
reaproveitar, porque poderia ser o `dev.db`.

Portas: API 3100, Web 3101 (não colidem com o `npm run dev`, em 3000/3001). Knobs de env:

| Variável                        | Default     | Efeito                                                                        |
| ------------------------------- | ----------- | ----------------------------------------------------------------------------- |
| `E2E_API_PORT` / `E2E_WEB_PORT` | 3100 / 3101 | portas da stack                                                               |
| `E2E_API_HOST`                  | `localhost` | host da API; `127.0.0.1` põe web e API em origens diferentes                  |
| `E2E_WEB_MODE`                  | `build`     | `next build` + `next start` vs `next dev` (dev exige o `npm run dev` fechado) |
| `E2E_TMP_DIR`                   | `e2e/.tmp`  | onde o SQLite da execução é criado                                            |
| `E2E_KEEP_DB`                   | —           | preserva o banco ao final (o mesmo que `--keep-db`)                           |
| `E2E_ALL_BROWSERS`              | —           | habilita os projetos `firefox` e `webkit`                                     |

**`serverEnv` é explícito e completo.** O `server/.env` **é** lido pela API do run (o dotenv não
sobrescreve o que já está no `process.env`, mas variável ausente aqui viraria o valor de
desenvolvimento). Por isso o `playwright.config.ts` fixa tudo de que a suíte depende, sem contar com
o `server/.env`:

- `NODE_ENV: "test"`, `DATABASE_PROVIDER: "sqlite"`, `DATABASE_URL`, `PORT`, `LOG_LEVEL: "error"`;
- `CORS_ORIGIN: WEB_URL` — string **idêntica** ao `Origin` do navegador (o `cors()` e a guarda de
  origem comparam exato), por isso o web é sempre `http://localhost:<porta>`;
- segredos **fixos de teste**, públicos de propósito e iguais aos de `server/vitest.config.ts`:
  `JWT_SECRET`, `JWT_KEY_ID: "test"`, `PASSWORD_PEPPERS: "test:<base64>"`,
  `PASSWORD_PEPPER_CURRENT_ID: "test"`;
- `ACCESS_TOKEN_TTL_SECONDS: String(ACCESS_TOKEN_TTL_SECONDS)` (20 s, importado de
  `src/config/env.ts` para spec e config concordarem);
- `ARGON2_MEMORY_KIB: "1024"`, `ARGON2_TIME_COST: "1"`, `ARGON2_PARALLELISM: "1"` — o mínimo que
  `NODE_ENV=test` aceita; com os parâmetros de produção cada cadastro/login custaria segundos;
- `TRUST_PROXY: "loopback"` — o web repassa `/api/*` com `X-Forwarded-For`; sem isso o
  `express-rate-limit` acusa `ERR_ERL_UNEXPECTED_X_FORWARDED_FOR`;
- `AUTH_RATE_LIMIT_{REGISTER_PER_IP,LOGIN_PER_IP,LOGIN_PER_EMAIL,REFRESH_PER_IP}: "100000"` — a
  suíte inteira sai do mesmo IP, e com os limites reais o seed esbarraria no 429.

Variável de ambiente nova obrigatória na API entra **aqui** no mesmo PR, senão o E2E local passa
(pelo `server/.env`) e o do CI quebra.

O `webServer` do web recebe só `env: { API_ORIGIN: API_URL }`: o navegador fala **apenas** com a
origem do web, e o repasse `web/app/api/[...path]/route.ts` lê `API_ORIGIN` em runtime. Nada da
API é inlined no `next build` do wrapper. `tests/smoke.spec.ts` guarda isso: nenhuma requisição do
navegador vai direto a `API_URL`, a de categorias sai por `${WEB_URL}/api/` com `Authorization:
Bearer …`.

`scripts/run-e2e.mjs` recusa rodar se o client do Prisma não for SQLite, poda órfãos
`smaug-e2e-*.db*`, cria `e2e/.tmp/smaug-e2e-<runid>.db`, roda `prisma db push` pelo wrapper do
server (sem `--force-reset`), faz `next build` em modo `build`, sobe o Playwright, limpa
`["", "-journal", "-wal", "-shm"]` no fim e trata SIGINT/SIGTERM/SIGHUP.
`global-setup.ts` recusa banco em `server/prisma` ou `dev.db`, confere que `/health` responde
`provider: "sqlite"`, faz um **`POST /auth/register` de sonda** (espera 201 — prova que o schema
existe **e** que a API subiu com os segredos de autenticação), congela `E2E_BASE_COMPETENCE` no env
e avisa se faltarem menos de 15 min para a virada de mês em UTC. No modo `dev` aquece as rotas; as
protegidas com `Cookie: smaug_session=1`, para o `proxy.ts` deixar passar e a rota compilar de
fato.

## Specs de autenticação (`tests/auth/`)

| Arquivo            | Cobre                                                                                                                                                                                                                                                                         |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cadastro.spec.ts` | cadastro cai no dashboard logado sem mostrar o próprio UUID; a conta nova entra pelo login                                                                                                                                                                                    |
| `login.spec.ts`    | e-mail + senha → dashboard; senha errada e e-mail inexistente com a mesma mensagem; recarga                                                                                                                                                                                   |
| `guards.spec.ts`   | visitante → `/login?next=<rota>` (raiz sem `next`); volta à rota após entrar; `next` externo cai no dashboard; cookie legado `userId` não abre sessão; autenticado em `/login`/`/cadastro` → dashboard; indicador sem refresh válido termina no login com o indicador apagado |
| `sessao.spec.ts`   | recarga em `/despesas`; renovação silenciosa real com token vencido; duas abas recarregadas juntas (409 de conflito tolerado); sair numa aba derruba a outra; sair de todos os dispositivos derruba outro contexto                                                            |

Padrões que só aparecem nelas:

- Testes de tela de login/cadastro usam `test.use({ authenticate: false })` e digitam
  `seedUser.email`/`seedUser.password`; o `seedUser` existe mesmo sem `authenticate`.
- Guardas observam o redirecionamento com `page.goto` cru e assertam a URL exata, com o `next`
  codificado: ``new RegExp(`/login\\?next=${encodeURIComponent(route)}$`)``.
- Cookie legível pela página é gravado por um helper local (`setPageCookie`) com `domain` do
  `baseURL`, `path: "/"`, `httpOnly: false`; a limpeza é assertada com
  `expect.poll(() => cookieValue(context, nome)).toBe("")`.
- Teste que espera o token vencer ajusta o próprio timeout:
  `test.setTimeout(60_000 + ACCESS_TOKEN_TTL_SECONDS * 1000)` e
  `page.waitForTimeout((ACCESS_TOKEN_TTL_SECONDS + 5 + 2) * 1000)`. É o **único** uso legítimo de
  `waitForTimeout`: o que se espera é o relógio da API, não um estado da página.
- Para agir só depois de a página repousar, `sessao.spec.ts` define `abaDoApp(page)` (nome do
  usuário visível + nenhuma chamada a `/api/` em voo há 500 ms): o web pode renovar mais de uma vez
  por carregamento, e agir com uma renovação em voo mistura os efeitos. A resposta da renovação é
  observada com `page.waitForResponse((r) => r.url().endsWith("/api/auth/refresh"))`.

## Divisão com o Vitest

> MSW prova que o frontend se comporta **dado um contrato**; o E2E prova que o contrato é **real**.

Caminho feliz de ponta a ponta é do E2E. Matriz de código de erro, texto de toast, ramo de modal e
guarda de competência é do Vitest (skill `web-testes`).

## Checklist

- [ ] Spec em `tests/<área>/<assunto>.spec.ts` (ou `.mobile.spec.ts` para o projeto mobile).
- [ ] `import { expect, test } from "../../src/fixtures/test.js";` com extensão `.js`.
- [ ] Nenhum import de `server/` ou `web/`.
- [ ] Estado montado por `cenarioX(seed, competence)` ou pelo `SeedClient`, sempre por HTTP, **no
      começo do teste** (o token do seed vence em ~25 s).
- [ ] Navegador autenticado pela fixture `context` (ou `signInBrowser` num contexto extra), nunca
      pela tela, salvo quando a tela de login é o assunto do teste.
- [ ] `goto(page, "/rota")` em vez de `page.goto`.
- [ ] Seletor por papel/rótulo/texto; `data-testid` só se o card não tiver papel; `exact: true`
      quando o nome é prefixo/substring de outro ("Sair", "Todos", "Senha").
- [ ] Variável nova exigida pela API acrescentada ao `serverEnv` do `playwright.config.ts`.
- [ ] Zero literal de mês, ano ou valor de parcela — derive de `competence` e da resposta da API.
- [ ] Estado "passado" produzido com `seed.importCsv(...)`, nunca com `create-*` no passado nem mexendo no relógio.
- [ ] `npm run test:e2e` verde.

## Não faça

- Não importe de `server/` nem de `web/`.
- Não crie page object — use fixture + cenário + `support/ui.ts`.
- Não escreva `"Set/26"`, `2026` ou `R$ 208,33` literal num spec.
- Não semeie competência passada pelos `create-*` (a API recusa de propósito) — use `importCsv`.
- Não use `page.clock` para produzir situação passada: o servidor decide, não o browser.
- Não importe `expect`/`test` de `@playwright/test`.
- Não repita no E2E um caminho que o Vitest já cobre barato.
- Não autentique com header de usuário nem cookie montado à mão com id: a API só aceita
  `Authorization: Bearer <accessToken>`, e o navegador só entra com `smaug_refresh` + indicador
  (`signInBrowser`).
- Não reaproveite a sessão do seed no navegador: cada um tem a sua, para que "Sair" na tela não
  derrube o seed.
- Não aumente `ACCESS_TOKEN_TTL_SECONDS` para "consertar" um seed tardio — semeie antes ou abra
  outra sessão; o TTL curto é o que faz a renovação silenciosa rodar de verdade.
- Não dependa do `server/.env` para a API do run: tudo que a suíte precisa vai no `serverEnv`.
- Não troque `localhost` por `127.0.0.1` no `WEB_URL`/`CORS_ORIGIN`; para testar origens
  diferentes use `E2E_API_HOST=127.0.0.1`, que muda só a API.
- Não passe flags do Playwright por `npm run test:e2e -- --flag`; use `node e2e/scripts/run-e2e.mjs`.

## Inconsistências conhecidas

- **Default de `E2E_WEB_MODE` diverge.** `playwright.config.ts` e `scripts/run-e2e.mjs` usam
  `build`; `src/config/env.ts` usa `process.env.CI ? "build" : "dev"`, e é esse `WEB_MODE` que o
  `global-setup.ts` lê para decidir o aquecimento. Pelo wrapper não há efeito (ele sempre exporta
  `E2E_WEB_MODE`); só num `npx playwright test` solto o setup aquece rotas de um `next start`.
  Siga `build` como default ao documentar ou acrescentar código.
- **`SeedClient.asUser(accessToken)` não tem chamador** em `src/` nem em `tests/` — a sessão do
  "outro dispositivo" é aberta com `new SeedClient(api).login(...)`. Use-o se precisar semear como
  outro usuário; não crie um segundo jeito.
- **`E2E_PASSWORD`** (`"senha-e2e-correta-horse"`) é só o default de `register`/`login`; a fixture
  `seedUser` gera `senha-<uuid>` própria. Em spec, use sempre `seedUser.password`.
- `guards.spec.ts` grava de propósito o cookie legado `userId` da versão anterior (antes da 010)
  para provar que ele não abre sessão e é apagado — é a única menção ao modelo antigo, e é teste
  de regressão, não padrão a copiar.
