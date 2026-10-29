---
name: smaug-padroes-gerais
description: Padrões gerais do monorepo Smaug — índice das demais skills, política de idioma, formatação, comentários, commits, branches, regras de dependência e comandos. Leia esta skill ANTES de qualquer tarefa de código no projeto (nova feature, bugfix ou refatoração).
---

# Padrões gerais do Smaug

## Quando usar esta skill

Sempre, como primeiro passo. Ela diz **qual skill específica abrir** e fixa as regras que valem
em todos os pacotes.

## Índice — qual skill abrir

| Tarefa                                                   | Skill                     |
| -------------------------------------------------------- | ------------------------- |
| Entender camadas do backend / adicionar um agregado novo | `server-arquitetura`      |
| Adapter de auth (argon2/jose/crypto), `authConfig`, env  | `server-arquitetura`      |
| Escrever entidade ou value object                        | `server-entidade-dominio` |
| Criar/alterar erro de domínio                            | `server-erros-dominio`    |
| Escrever caso de uso                                     | `server-caso-de-uso`      |
| Escrever porta + repositório Prisma                      | `server-repositorio`      |
| Escrever service da aplicação ou DTO/schema Zod          | `server-servico-dto`      |
| Escrever controller, rota ou middleware (authenticate)   | `server-http`             |
| Registrar dependências                                   | `server-di-container`     |
| Testes do server (unit/integração)                       | `server-testes`           |
| Entender camadas do frontend / criar página              | `web-arquitetura`         |
| Escrever hook de feature (TanStack Query)                | `web-feature-hooks`       |
| Escrever service de feature (axios)                      | `web-feature-services`    |
| Escrever componente de feature ou formulário             | `web-componentes`         |
| Escrever primitivo de UI, hook ou lib compartilhada      | `web-shared-ui`           |
| Mexer em api-client, renovação, api-error, sessão        | `web-infra`               |
| Testes do web (Vitest + RTL + MSW)                       | `web-testes`              |
| Testes E2E (Playwright)                                  | `testes-e2e`              |

## Monorepo

`server/`, `web/` e `e2e/` são **pacotes npm independentes** (não é npm workspaces): cada um tem
`package.json`, lockfile e `node_modules` próprios — mais o pacote da raiz, com o tooling
compartilhado. São **quatro lockfiles**.

```bash
npm run install:all      # obrigatório uma vez: raiz + server + web + e2e
npm run dev              # server (3000) + web (3001)
npm run test             # server e depois web
npm run lint             # eslint (server) + eslint 9 flat config (web)
npm run format           # prettier em todo o repo
npm run validate:deps    # regras de arquitetura — SÓ da raiz
npm run test:e2e         # Playwright, com SQLite exclusivo do run
node e2e/scripts/run-e2e.mjs --grep "<título>"   # E2E com flags do Playwright (ver abaixo)
```

- `npm run dev` precisa de `server/.env` com os segredos de autenticação (`JWT_SECRET`,
  `JWT_KEY_ID`, `PASSWORD_PEPPERS`, `PASSWORD_PEPPER_CURRENT_ID` — modelo em `server/.env.example`)
  e de `web/.env.local` com `API_ORIGIN=http://localhost:3000` (modelo em `web/.env.example`): o
  navegador só fala com o web, e o repasse `web/app/api/[...path]/route.ts` lê `API_ORIGIN` a cada
  requisição. Não existe mais `NEXT_PUBLIC_*` da API inlined no build.
- `npm run test:e2e -- --grep x` **não** repassa a flag (o `npm run --prefix e2e test` do meio a
  consome); só caminho posicional passa (`npm run test:e2e -- tests/smoke.spec.ts`). Para
  `--grep`, `--project`, `--headed` etc. chame o wrapper direto: `node e2e/scripts/run-e2e.mjs …`.

- `npm run --prefix server validate:deps` está **quebrado** (aponta para um `.dependency-cruiser.cjs`
  inexistente). Use sempre o script da raiz.
- `web/` instala estrito (`npm ci`/`npm install` sem flags), como os demais pacotes; com o React 19
  estável não há mais `.npmrc` nem flag de peers.
- Prisma sempre pelos scripts do server (`prisma:generate`, `migrate:deploy`, `migrate:new`,
  `prisma -- <args>`): eles escolhem `prisma/<provider>/` pela `DATABASE_PROVIDER` (ambiente, depois
  `server/.env`), gravam o schema derivado e passam `--config prisma/prisma.config.ts` (a config do
  Prisma 7, ao lado dos schemas derivados, que aponta schema, migrations e URLs do provider) — e nunca
  alteram arquivo versionado. `npx prisma` direto não acha a config e falha. Mudança de schema = editar
  `server/prisma/schema.prisma` + `migrate:new`, que cria a migration em SQLite **e** PostgreSQL.

## Política de idioma

Regra observada em todo o código, sem exceção relevante:

| O quê                                                       | Idioma                                                    |
| ----------------------------------------------------------- | --------------------------------------------------------- |
| Identificadores (classes, funções, variáveis, tipos)        | **inglês**                                                |
| Payloads da API, nomes de campo, endpoints, códigos de erro | **inglês**                                                |
| Nomes de pasta de feature e de rota do Next                 | **português** (`features/despesas`, `app/(app)/receitas`) |
| Texto de UI, mensagens de toast, `aria-label`               | **português**                                             |
| Comentários de código e JSDoc                               | **português**                                             |
| Títulos de teste do **server**                              | **inglês** — `it("should … when …")`                      |
| Títulos de teste do **web** e do **e2e**                    | **português**, minúsculo, verbo na 3ª pessoa              |
| Specs (`specs/`), README, mensagens de commit               | **português**                                             |

## Formatação e lint

Prettier é a única lei de estilo (`.prettierrc`, sem override por pacote):

```json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

O `eslint.config.js` da raiz (aplica a `server/` e `e2e/`) tem `rules: {}` — só
`js.configs.recommended` + `tseslint.configs.recommended`. O `web/` usa ESLint 9 com
configuração flat (`web/eslint.config.mjs`, script `eslint .`): `eslint-config-next/core-web-vitals`

- `eslint-config-next/typescript`, também sem regra própria, exceto liberar
  `no-explicit-any` e `no-non-null-assertion` **em arquivos de teste** (override no mesmo arquivo).

Consequência prática: `any` e `!` são proibidos em código de produção do `web/` e permitidos em
teste. No `server/`, `req.userId!` é a exceção deliberada (ver `server-http`).

Husky + lint-staged rodam o `.lintstagedrc.js` **da raiz** no commit. O bloco `lint-staged` dentro
de `server/package.json` é código morto — nada o invoca.

## Comentários — a regra da casa

Comentário **não descreve o que o código faz**; ele registra o _porquê_, nomeando a falha que foi
observada de verdade e a alternativa que foi descartada. Exemplares a imitar:

- `web/shared/lib/money.ts` (`parseMoneyInput`) — cita o bug do `parseFloat(v.replace(",", "."))` que virava `1.234`.
- `web/infra/api-client.ts` — o interceptor de 401 explica por que só renova quem saiu com o token
  atual ("renovar de novo giraria o refresh token à toa — o que dá 409 na outra aba") e que "Rede ou
  5xx são transitórios".
- `web/vitest.config.ts` — justifica o threshold relaxado de `app/**` e lista as duas alternativas rejeitadas.
- `e2e/src/support/ui.ts` — `waitForHydration` descreve a corrida real (submit nativo virando `GET /login?email=…`).

Não escreva comentário que repete a linha seguinte. Código morto ou comentado não entra
(princípio II da constituição).

## Regras de dependência (`.dependency-cruiser.js`, raiz)

Sete regras `error` e uma `warn`, nesta ordem no arquivo:

1. `no-server-to-web` — `server/` não importa `web/`.
2. `no-web-to-server` — `web/` não importa `server/`.
3. `no-domain-to-infra` — `server/src/domain` não importa `infrastructure`/`presentation`.
4. `no-application-to-infra` — `server/src/application` não importa `infrastructure`/`presentation`.
5. `auth-crypto-only-in-infra` — `argon2` e `jose` só são importados em `server/src/infrastructure/`
   (ficam atrás das portas `PasswordHasher`/`AccessTokenService`).
6. `http-middleware-libs-only-in-presentation` — `cookie-parser` e `express-rate-limit` só em
   `server/src/presentation/`.
7. `no-e2e-to-src` — `e2e/` não importa `server/` nem `web/` (é caixa-preta; fala só HTTP).
8. `no-circular-dependencies` — apenas aviso.

As regras 5 e 6 são o modelo para dependência de runtime com dono: biblioteca nova que deve viver
numa camada só ganha uma regra `from: { path: "^server/src/", pathNot: "^server/src/<camada>/" }`,
`to: { path: "node_modules/(<lib>)/" }`, copiada de uma delas.

```js
{
  name: "auth-crypto-only-in-infra",
  comment:
    "argon2 e jose ficam atrás das portas PasswordHasher/AccessTokenService: só os adapters de server/src/infrastructure os importam",
  severity: "error",
  from: { path: "^server/src/", pathNot: "^server/src/infrastructure/" },
  to: { path: "node_modules/(argon2|jose)/" },
},
```

Rode `npm run validate:deps` (da raiz) antes de abrir PR.

**Furo conhecido (pré-existente):** a config não tem `options.tsConfig`, então o dependency-cruiser
**não resolve o alias `@src/*`** — `import … from "@src/infrastructure/…"` dentro de `domain/` passa
calado pelas regras 3 e 4. Elas só pegam import relativo. As regras 5 e 6 funcionam, porque miram
`node_modules/`. Até o furo ser fechado, a revisão é quem garante a direção das camadas quando o
import usa o alias.

## Git

- **Conventional Commits**: `type(escopo): assunto`. Tipos usados: `feat`, `fix`, `refactor`,
  `docs`, `chore`, `test`.
- Escopo é opcional e vem em dois sabores: **id da feature** (`feat(002-receitas)`,
  `docs(003-despesas)`) ou **pacote/área** (`chore(server)`, `refactor(web)`, `chore(tooling)`).
- Assunto no imperativo; o histórico mistura pt-BR e inglês — prefira pt-BR em código novo.
- Corpo: linha em branco, depois lista de bullets `-` quebrada em ~72 colunas.
- Trailer estabelecido: `Co-Authored-By: Claude <modelo> <noreply@anthropic.com>`.
- Branches: `###-feature-name` (`005-implementacao-web`), merge por PR.

## Spec Kit

Trabalho de feature vive em `specs/###-feature-name/` (`spec.md`, `plan.md`, `research.md`,
`data-model.md`, `tasks.md`, `contracts/`, `checklists/`) e é dirigido pelas skills `speckit.*`
apoiadas em `.specify/`.

- `.specify/memory/constitution.md` é **normativo** e vence a prática ad-hoc. Usa modais
  RFC-2119 em maiúsculas e português (DEVE / NÃO DEVEM / PROIBIDAS), com um `**Rationale**:`
  fechando cada princípio.
- Todo `plan.md` carrega um **Constitution Check** com o tripé por princípio:
  `- **Status**: PASS` / `- **Evidence**: …` / `- **Compliance**: …`.
- `tasks.md` usa `- [ ] T### [P] [US#] descrição com o caminho exato do arquivo`; fases numeradas,
  `**Checkpoint**:` ao fim de cada fase, `🎯 MVP` nas histórias P1.

## Como refatorar sem quebrar o padrão

1. Antes de mudar, abra a skill do elemento e leia a seção **Inconsistências conhecidas**.
2. Quando o código tem dois jeitos de fazer a mesma coisa, **siga o lado indicado pela skill** e
   nunca introduza um terceiro.
3. Refatorar só o que a tarefa exige; YAGNI é mandatório (princípio V).
4. Alteração de contrato da API sempre em par: código de erro novo no `server` entra também na
   tabela `MESSAGES` de `web/infra/api-error.ts` no mesmo PR.
5. Cobertura é gate: `server` exige 100/100/100/100; `web` tem thresholds por glob. Uma refatoração
   que derruba cobertura não passa no CI.
6. `docs/prototipo/` é **referência visual**, não código de produção — não copie padrão de lá
   (roda em React UMD e persiste em `localStorage`).
