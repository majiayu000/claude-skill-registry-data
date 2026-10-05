---
name: review-work
description: Levantamento de atividade de um membro do time (GitHub + JIRA) durante uma sprint. Aceita nome, GitHub username ou parte do nome e opcionalmente o numero da sprint.
argument-hint: <name-or-username> [sprint-number]
allowed-tools: Bash(gh *), Bash(jira *), Bash(date *), Bash(echo *), Bash(SPRINT_*), Bash(START_*), Bash(END_*), Bash(PAGE=*), Bash(EVENTS=*), Bash(JIRA_USER=*), Bash(MEMBERS=*), Bash(MATCH=*)
---

# Review Work

Levanta a atividade de uma pessoa no GitHub e JIRA durante uma sprint.

## Argumentos

- `$ARGUMENTS`: Primeiro token e o nome ou GitHub username da pessoa (obrigatorio). Segundo token (opcional) e o numero da sprint (inteiro). Se omitido, usa a sprint ativa.

Exemplos:
- `/review-work tirth` — sprint ativa, resolve para tirthct
- `/review-work tirthct 6` — sprint 6
- `/review-work leonardo` — resolve pelo nome real
- `/review-work angel` — resolve para rh-amarin

## Instrucoes

### 1. Parsear argumentos

Extraia do `$ARGUMENTS`:
- `INPUT`: primeiro token (nome ou GitHub username)
- `SPRINT_NUM`: segundo token (numero inteiro, opcional)

Se `INPUT` estiver vazio, informe ao usuario que o nome/username e obrigatorio e pare.

### 2. Resolver GitHub username

O usuario pode fornecer um GitHub username exato, um nome parcial, ou o primeiro nome da pessoa.

#### 2a. Buscar membros da org

Busque todos os membros da org via GitHub API (inclui membros que podem nao estar no OWNERS de repos individuais):

```bash
gh api orgs/openshift-hyperfleet/members --jq '.[].login'
```

Filtre bots conhecidos da lista (nomes que contenham `bot`, `robot`, `cyborg`).

Se a API falhar (ex: permissao insuficiente), use o OWNERS file como fallback:

```bash
gh api repos/openshift-hyperfleet/hyperfleet-sentinel/contents/OWNERS --jq '.content' | base64 --decode
```

#### 2b. Buscar nomes reais

Para cada username da lista, busque o nome real via GitHub API:

```bash
gh api "users/<USERNAME>" --jq '.name // ""'
```

Construa uma lista de pares `username|nome_real`.

#### 2c. Fazer match

Compare o `INPUT` (case-insensitive) contra:
1. GitHub username (match exato ou parcial — ex: `tirth` casa com `tirthct`)
2. Nome real (match parcial — ex: `leonardo` casa com um nome que contenha "leonardo", `angel` casa com "Angel Marin")

**Regras de match:**
- Se match unico: usar esse username automaticamente
- Se multiplos matches: mostrar lista e pedir ao usuario para escolher
- Se nenhum match: mostrar todos os membros disponiveis e pedir ao usuario para escolher

**Exemplo de lista quando ha ambiguidade:**

```
Multiplos matches para "a":
  1. aredenba-rh (Austin Redenbaugh)
  2. rh-amarin (Angel Marin)

Qual o numero do usuario desejado?
```

### 3. Obter dados da sprint

#### 3a. Descobrir sprint ativa (se SPRINT_NUM nao informado)

Busque qualquer ticket na sprint ativa para extrair os dados:

```bash
jira issue list --project HYPERFLEET --jql "sprint in openSprints()" --plain --columns KEY --paginate "0:1"
```

Depois pegue os dados da sprint do ticket:

```bash
jira issue view <KEY> --raw | jq -r '.fields.customfield_10020[-1]'
```

O campo retorna um objeto JSON como:
```json
{"id": 15607, "name": "Hyperfleet Sprint 8", "state": "active", "boardId": 1013, "startDate": "2026-03-16T10:08:33.743Z", "endDate": "2026-04-06T09:00:00.000Z"}
```

Extraia `name`, `startDate` e `endDate` diretamente do objeto.

#### 3b. Buscar sprint por numero (se SPRINT_NUM informado)

Use JQL com o nome da sprint:

```bash
jira issue list --project HYPERFLEET --jql "sprint = 'Hyperfleet Sprint <SPRINT_NUM>'" --plain --columns KEY --paginate "0:1"
```

Depois extraia os dados da sprint do ticket retornado, da mesma forma que em 3a. Procure no array `customfield_10020` a entrada cujo `name` contenha o numero da sprint solicitado.

Se nenhum ticket for encontrado, informe ao usuario que a sprint nao foi encontrada e pare.

### 4. Buscar atividade no GitHub

Use a Events API do GitHub para buscar toda a atividade do usuario no periodo da sprint. A API retorna no maximo 300 eventos e pagina em paginas de 30.

Busque todas as paginas necessarias:

```bash
gh api "users/<GH_USER>/events?per_page=100&page=1" --jq '.[] | select(.created_at >= "<START_DATE>" and .created_at <= "<END_DATE>") | [.type, .created_at, .repo.name, (if .type == "PushEvent" then (.payload.ref // "") else "" end), (if .type == "PullRequestEvent" or .type == "PullRequestReviewEvent" or .type == "PullRequestReviewCommentEvent" then (.payload.pull_request.number | tostring) else "" end), (if .type == "IssueCommentEvent" then (.payload.issue.number | tostring) else "" end)] | @tsv'
```

Continue paginando (page=2, page=3, etc) ate a API retornar array vazio ou todos os eventos estarem fora do periodo da sprint.

**Tipos de evento relevantes:**
- `PushEvent` — push de commits (registrar repo, branch)
- `PullRequestEvent` — abriu/fechou/reabriu PR
- `PullRequestReviewEvent` — review formal (approve, request changes)
- `PullRequestReviewCommentEvent` — comentario inline em review
- `IssueCommentEvent` — comentario geral em issue/PR
- `CreateEvent` — criou branch/tag/repo

### 5. Buscar atividade no JIRA

#### 5a. Descobrir o JIRA username

O GitHub username nem sempre e igual ao JIRA username. Tente encontrar o JIRA username buscando tickets onde o usuario e assignee ou reporter. Se nao conseguir mapear automaticamente, pergunte ao usuario qual o JIRA username da pessoa.

Estrategia: busque tickets recentes do projeto e tente encontrar um match parcial com o GitHub username no campo assignee:

```bash
jira issue list --project HYPERFLEET --jql "assignee = '<GH_USER>'" --plain --columns KEY --paginate "0:1"
```

Se nao encontrar, tente variantes comuns (ex: para `tirthct` tente `tirth`, `tthakkar`, etc). Se encontrar um ticket, extraia o JIRA username:

```bash
jira issue view <KEY> --raw | jq -r '.fields.assignee.name'
```

Se nenhuma variante funcionar, busque tickets recentes do projeto e compare o display name com o nome real do GitHub:

```bash
jira issue list --project HYPERFLEET --jql "updated >= '-30d'" --plain --columns KEY,ASSIGNEE --no-truncate --paginate "0:50"
```

Procure o display name que contenha parte do nome real da pessoa. Depois extraia o JIRA username do ticket encontrado.

#### 5b. Tickets com atividade

Busque tickets onde o usuario foi ativo no periodo da sprint:

```bash
# Tickets assigned ao usuario atualizados no periodo
jira issue list --project HYPERFLEET --jql "assignee = '<JIRA_USER>' AND updated >= '<START_DATE>' AND updated <= '<END_DATE>'" --plain --columns KEY,SUMMARY,STATUS,UPDATED --no-truncate

# Tickets onde o usuario fez transicoes de status
jira issue list --project HYPERFLEET --jql "status changed by <JIRA_USER> AFTER '<START_DATE>'" --plain --columns KEY,SUMMARY,STATUS --no-truncate

# Tickets criados pelo usuario no periodo
jira issue list --project HYPERFLEET --jql "reporter = '<JIRA_USER>' AND created >= '<START_DATE>'" --plain --columns KEY,SUMMARY,STATUS --no-truncate
```

Combine e deduplique os resultados.

#### 5c. Detalhes dos tickets

Para cada ticket encontrado, busque os detalhes para entender a atividade:

```bash
jira issue view <KEY> --raw | jq '{key: .key, summary: .fields.summary, status: .fields.status.name, assignee: (.fields.assignee.displayName // "Unassigned"), storyPoints: (.fields.customfield_10028 // null), type: .fields.issuetype.name}'
```

### 6. Consolidar e apresentar

#### 6a. Agregar por dia

Agrupe toda a atividade (GitHub + JIRA) por dia. Para cada dia no periodo da sprint:

- Conte pushes ao fork/repos
- Conte review comments (PullRequestReviewCommentEvent conta como 1 comment cada)
- Liste PRs envolvidas (com link)
- Liste outras atividades (criacao de branches, issue comments, etc)

#### 6b. Formato de saida

Use markdown tables (pipes `|`) para que links sejam renderizados como clicaveis. NAO use code blocks (` ``` `) ao redor das tabelas — markdown links nao renderizam dentro de code blocks.

Sprint: Hyperfleet Sprint N (DD MMM - DD MMM YYYY)
GitHub: <GH_USER> (<REAL_NAME>) | JIRA: <JIRA_USER>

| Data | Dia | Pushes | Review Comments | PRs | Outras atividades |
|------|-----|--------|-----------------|-----|-------------------|
| 23 Feb | Mon | 2 | 5 | [sentinel#51](https://github.com/openshift-hyperfleet/hyperfleet-sentinel/pull/51) | Criou branch hyperfleet-542 |
| 24 Feb | Tue | — | — | — | — |
| 25 Feb | Wed | 3 | 4 | [sentinel#51](https://github.com/openshift-hyperfleet/hyperfleet-sentinel/pull/51) | Abriu sentinel#51 |

**Regras da tabela:**
- Incluir TODOS os dias do periodo da sprint, mesmo os sem atividade
- Dias sem atividade: usar `—` nas colunas
- Fins de semana sem atividade: agrupar (ex: "01-02 Mar" / "Sat-Sun")
- Fins de semana COM atividade: mostrar individualmente
- PRs com link: usar formato `[repo#N](https://github.com/<org>/repo/pull/N)`
- Pushes e Review Comments: mostrar contagem numerica
- Coluna "Outras atividades": issue comments, criacao de branches, aberturas de PRs

#### 6c. Resumo JIRA

Apos a tabela, mostrar uma secao de atividade JIRA usando markdown table (sem code block):

### JIRA Activity

| Ticket | Type | Summary | Status | SP |
|--------|------|---------|--------|----|
| [HYPERFLEET-542](https://redhat.atlassian.net/browse/HYPERFLEET-542) | Story | Add OTel instrumentation to Sentinel | In Progress | 5 |
| [HYPERFLEET-557](https://redhat.atlassian.net/browse/HYPERFLEET-557) | Task | Update architecture docs | Review | 3 |

#### 6d. Resumo final

Encerre com um paragrafo curto resumindo:
- Total de dias com atividade vs dias uteis na sprint
- Total de pushes, review comments, PRs trabalhadas
- Foco principal do trabalho (qual PR/ticket recebeu mais atencao)
- Tickets JIRA movimentados

## Regras

- Use `gh` CLI para GitHub e `jira` CLI para JIRA
- Analise em portugues
- Dias da semana em ingles (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
- Meses em ingles (Jan, Feb, Mar, etc)
- Se a Events API do GitHub nao retornar dados suficientes (limite de 90 dias / 300 eventos), avise o usuario
- Se nao conseguir mapear o JIRA username, pergunte ao usuario
- Links de PRs: usar formato `[repo#N](https://github.com/<org>/repo/pull/N)` — texto curto com URL completa para terminais que suportam links markdown
- Links de tickets JIRA: usar formato `[HYPERFLEET-XXX](https://redhat.atlassian.net/browse/HYPERFLEET-XXX)`
- A org padrao para PRs e `openshift-hyperfleet`, exceto quando o repo.name retornado pela API indicar outra org (ex: `openshift/release`)
