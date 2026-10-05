---
name: youtrack
description: >
  Issues, busca, comentários, tags, artigos e registro de trabalho no YouTrack
  Cloud via MCP oficial. Use quando o usuário disser "YouTrack", "criar issue",
  "minhas issues", "buscar tarefas", "comentar na issue", "atribuir para",
  "mudar o estado", "registrar horas", "artigo da knowledge base", ou citar um
  ID tipo PROJ-123. Boards e sprints são da skill youtrack-rest.
metadata:
  version: 1.0.0
---

# YouTrack

Você gerencia issues no YouTrack do usuário via MCP oficial (servidor `youtrack`).

## Pré-requisito e degradação

**Path A — MCP `youtrack` conectado**: use as tools diretamente.

**Path B — MCP ausente/failed**: não simule. Aponte `/pwdev-youtrack:init` e,
se `YOUTRACK_BASE_URL`/token existirem (`check-setup.sh`), ofereça o fallback
REST via `${CLAUDE_PLUGIN_ROOT}/scripts/yt-api.sh` para operações pontuais.
Lembre: env var nova só vale após reiniciar a sessão.

## Mapa de intenção → tool

| Intenção | Tool |
|---|---|
| Buscar issues | `search_issues` (query language abaixo) |
| Detalhar issue | `get_issue` (ID legível `PROJ-123`) |
| Criar issue | `get_issue_fields_schema` **ANTES** → `create_issue` (ou `create_draft_issue` para revisão) |
| Atualizar campos/estado | `update_issue` · responsável: `change_issue_assignee` |
| Comentar / ler comentários | `add_issue_comment` / `get_issue_comments` |
| Tags | `manage_issue_tags` |
| Vincular issues | `link_issues` |
| Registrar horas | `log_work` (formato `1h 30m`) |
| Artigos | `search_articles` / `get_article` / `create_article` / `update_article` |
| Projetos e pessoas | `find_projects` · `get_project` · `find_user` · `get_current_user` |

Detalhes e pegadinhas: `${CLAUDE_PLUGIN_ROOT}/references/mcp-tools.md`.

## Query language — essencial

`assignee: me #Unresolved` · `project: ODARA type: Bug priority: Critical` ·
`State: {In Progress}` · `created: {This week}` · `has: -{Assignee}` ·
`sort by: {updated} desc`. Cheat sheet completo:
`${CLAUDE_PLUGIN_ROOT}/references/query-language.md`.

## Fluxos recomendados

- **Criar issue**: schema do projeto → montar proposta (summary, description,
  campos) → mostrar ao usuário → criar só após confirmação.
- **Triagem**: `assignee: me #Unresolved sort by: {updated} desc` → resumir por
  prioridade/estado → propor ações, executar as confirmadas.
- **Log de trabalho**: confirmar issue, duração e data antes de `log_work` —
  registro de tempo errado suja relatório de faturamento.

## Regras

- **Mutação só com confirmação** — create, update, delete, log_work: mostre o
  que vai fazer antes de fazer.
- **Nunca invente custom field ou valor de enum** — consulte
  `get_issue_fields_schema` na dúvida.
- Comunique-se por IDs legíveis (`PROJ-123`), nunca IDs internos.
- Leia `.claude/pwdev-youtrack-context.md` (projeto/board padrão) antes de
  perguntar o que já está registrado.
- Conteúdo escrito no YouTrack segue o idioma do projeto do usuário.

## Limites

- Não gerencia boards, sprints, anexos nem operações em lote — ver `youtrack-rest`
- Não monta relatórios agregados — ver `/pwdev-youtrack:report`
- Não altera permissões nem configuração administrativa da instância

## Skills relacionadas

`youtrack-rest` — boards, sprints, relatórios de tempo, anexos, bulk
