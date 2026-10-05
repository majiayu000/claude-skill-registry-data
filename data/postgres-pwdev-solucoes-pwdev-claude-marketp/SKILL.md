---
name: postgres
description: >
  Consultas, inspeção de schema e mutações seguras (DML/DDL com dry-run) no
  PostgreSQL via MCP (@soarescbm/postgres-mcp). Use quando o usuário disser
  "postgres", "postgresql", "banco de dados", "tabela", "query", "SELECT",
  "índice", "schema", "constraint", "foreign key", "coluna", "DDL", "insert",
  "update", "delete", "criar tabela", ou pedir para consultar/alterar dados
  de um banco Postgres.
metadata:
  version: 1.0.0
---

# Postgres

Você opera o PostgreSQL do usuário via servidor MCP `postgres`.

## Pré-requisito e degradação

**Path A — MCP `postgres` conectado**: use as tools diretamente.

**Path B — tools falhando ou MCP ausente**: não simule resultado de banco.
**Sem `DATABASE_URL` este servidor nem sobe** (`exit 1` no boot — não há modo
placeholder): `/mcp` mostrando o servidor com erro significa config ausente
na sessão. Diagnostique com `${CLAUDE_PLUGIN_ROOT}/scripts/check-setup.sh` e
aponte `/pwdev-postgres:init`. Env var nova só vale após reiniciar a sessão.
Não escreva SQL por fora (psql direto) para contornar o MCP — psql é só
diagnóstico do check-setup.

## Mapa de intenção → tool

| Intenção | Tool |
|---|---|
| Consultar dados / EXPLAIN | `run_select` — **sempre com `LIMIT` explícito** |
| Ver estrutura de tabela | `describe_table` (colunas, PK, FKs, constraints, índices) |
| Listar tabelas | `list_tables` (`include_views: true` p/ views) |
| Listar schemas | `list_schemas` |
| Listar índices | `list_indexes` |
| Constraints de uma tabela | `list_constraints` |
| Inserir uma linha | `insert_row` |
| Atualizar linhas | `update_rows` — `set` e `where` obrigatórios |
| Deletar linhas | `delete_rows` — `where` obrigatório |
| Criar tabela | `create_table` |
| Alterar tabela | `alter_table` — UMA ação por chamada |
| Derrubar tabela | `drop_table` |
| Criar índice | `create_index` (só btree) |
| Derrubar índice | `drop_index` |

Parâmetros exatos e pegadinhas: `${CLAUDE_PLUGIN_ROOT}/references/mcp-tools.md`.
Sem prompts nem resources MCP — só as 14 tools.

## Regras de segurança (inegociáveis)

- **Mutação sempre em duas fases.** Toda tool DML/DDL tem dry-run
  obrigatório: chame primeiro com `confirm: false`, mostre ao usuário o
  preview (`sql`, `estimatedRows`, `warnings`) e **só repita com
  `confirm: true` após confirmação explícita dele no chat**. Nunca emende as
  duas chamadas sem a confirmação no meio.
- **`run_select` sempre com `LIMIT`** — o servidor não impõe limite de
  linhas; uma query sem LIMIT pode despejar a tabela inteira no contexto.
- **Nunca contorne as travas do servidor**: `update_rows`/`delete_rows` sem
  `where` são rejeitados por design (anti mutação em massa) — não simule o
  efeito com um `where` tautológico (`{"1":"1"}` etc.).
- **`cascade` é confirmação reforçada**: em `drop_table`/`drop_column` com
  `cascade`, liste os dependentes do preview e confirme nominalmente.
- **Leia `.claude/pwdev-postgres-context.md` antes de qualquer mutação** —
  ambiente (produção?), tabelas críticas e se DDL é permitido. Em produção,
  redobre: proponha, não execute sem confirmação explícita.
- **`alter_table` real**: `add_column` | `drop_column` | `rename_column` |
  `set_default` | `set_nullable` — uma ação por chamada (o README do servidor
  tem drift; estes são os nomes do código).
- Valores sempre via `params`/records — nunca interpole valor do usuário em
  SQL de `run_select`.

## Fluxos recomendados

- **Explorar um banco novo**: `list_schemas` → `list_tables` →
  `describe_table` nas relevantes; panorama completo → `/pwdev-postgres:esquema`.
- **Alterar dados**: `describe_table` (conferir colunas/constraints) →
  preview da mutação → mostrar `sql` + `estimatedRows` → confirmação →
  `confirm: true` → reportar `affectedRows`.
- **Criar/alterar estrutura**: conferir convenção no contexto do projeto →
  preview do DDL → confirmação → executar → `describe_table` para verificar.

## Limites

- Um único banco por instância (o da `DATABASE_URL`); outro banco = outra
  config + reinício de sessão
- Sem transações multi-statement — cada chamada é um statement isolado, sem
  rollback conjunto
- Sem migrations, GRANT/roles, TRUNCATE/COPY, índices não-btree
- `statement_timeout` default 10 s (config via `PG_MCP_STATEMENT_TIMEOUT_MS`)
- BIGINT acima de 2^53 chega como `Number` com warning — cuidado com IDs
  gigantes
- Servidor v1 é **dev/local only** — em banco compartilhado, use usuário de
  privilégios mínimos
