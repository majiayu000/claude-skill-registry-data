---
name: query-bravo
description: >
  Use quando o usuário pedir dados, métricas ou análises da casa Bravo
  especificamente — número de jogadores, depósitos, saques, GGR/NGR,
  apostas, KYC, transações de cassino/esporte, ou qualquer métrica
  operacional dessa casa que exija uma query real no banco ar_bravo_prd. Se
  não estiver claro se a pergunta é sobre Tradicional ou Bravo, perguntar
  antes de assumir — são bancos separados, mesmo compartilhando o mesmo
  formato de schema (ver `query-trad` para a Tradicional).
invocation: model
inputs:
  - pergunta de negócio em linguagem natural sobre a casa Bravo (métrica, comparação, exploração)
  - contexto de período/segmento quando fornecido pelo usuário
outputs:
  - SQL proposto (mostrado antes de executar, nunca rodado sem aprovação)
  - resultado da query interpretado em termos de negócio
  - ressalvas (casa = Bravo, período coberto, suposições sobre a métrica, PII omitido)
side_effects: none
context:
  - .claude/skills/query-bravo/SKILL.md (este arquivo — mapa de schemas/tabelas/views da Bravo)
  - .claude/skills/query-trad/SKILL.md (par da Tradicional — mesmo formato, dados diferentes)
completion: >
  A query certa foi identificada no banco certo (ar_bravo_prd), mostrada e aprovada antes de
  rodar, e o resultado foi devolvido em termos de negócio sem PII exposta.
---

# Query Bravo — banco `ar_bravo_prd`

Banco PostgreSQL `ar_bravo_prd` (acesso **somente leitura**, confirmado via teste real —
`CREATE TABLE` é recusado com `cannot execute CREATE TABLE in a read-only transaction`). É uma
instância **separada** do banco da Tradicional (`trad_prd`, ver `query-trad/SKILL.md`), mas
roda o mesmo formato de schema/codebase (`micro-api` compartilhado, confirmado pelo relatório
`relatorio-tecnico-furo-sigap-bravo` de 2026-09) — mesmos nomes de schema/tabela/view, mas
**dados e configuração próprios de cada casa**. Nunca assumir que um fato confirmado na
Tradicional (ex.: qual fornecedor de KYC está ativo) vale para a Bravo sem reconfirmar — ver
seção "Fatos confirmados" abaixo.

## Conexão

Não existe MCP Postgres configurado — a execução é via `psql` no terminal, autenticado por
**usuário/senha fixos** (não é token IAM como o `trad-prd` — credencial enviada por Ícaro via
ClickUp em 2026-09-15, sem expiração automática conhecida).

**Se o alias `bravo-prd` já estiver configurado no shell** (`~/.zshrc`):
```bash
bravo-prd -c "SELECT ..."
```

A senha vive no **Keychain do macOS** (serviço `bravo-prd-pam`, conta `br_ithalo_read`) desde
2026-09-17 — o alias busca com `security find-generic-password`, nunca em texto puro. A senha
**nunca deve ser escrita em nenhum arquivo deste repositório** nem citada em texto puro numa
sessão/log. Se o alias não existir ou falhar, pedir ao usuário para reconfigurá-lo — não
reconstruir a conexão manualmente pedindo a senha na conversa.

| Campo    | Valor                                                                  |
|----------|-------------------------------------------------------------------------|
| Host     | ar-bravo-bet-prd-cluster.c44onum4sztb.us-east-1.rds.amazonaws.com        |
| Porta    | 5432                                                                   |
| Database | ar_bravo_prd                                                           |
| Usuário  | br_ithalo_read (role dedicada, somente leitura confirmada)              |
| Acesso   | Somente leitura (testado: `CREATE TABLE` recusado)                     |

## Regras de uso

Mesmas regras da `query-trad` (Tradicional) — não duplicadas aqui além do essencial:

- Sempre mostre o SQL antes de rodar e espere aprovação explícita.
- Sempre use `LIMIT` em queries exploratórias e filtre por data quando possível.
- Nunca tente `UPDATE`/`DELETE`/`INSERT`/DDL — o banco recusa.
- Nunca exponha CPF/telefone/e-mail/nome completo — agregue ou anonimize.
- **Se não estiver claro se a pergunta é sobre Tradicional ou Bravo, perguntar antes de
  assumir** — são dados de casas diferentes, mesmo com schema no mesmo formato.
- **Confirmar que uma view/tabela existe na Bravo antes de reaproveitar um nome usado na
  Tradicional** — a maioria existe igual (ver seção de views abaixo), mas não assuma sem
  checar quando não estiver nesta lista.

## Schemas disponíveis (levantado em 2026-09-15, só metadados)

| Schema      | Tabelas | Views | Mat. Views | Observação                                    |
|-------------|---------|-------|------------|------------------------------------------------|
| public      | 133     | 32    | 12         | Core PAM — igual em formato à Tradicional      |
| affiliates  | 23      | 5     | 3          | Afiliados e campanhas                          |
| dwh         | 19      | 8     | 2          | Data Warehouse / BI                            |
| integration | 26      | 5     | 2          | Cassino/Esporte — providers, bets, transactions|
| pix         | 10      | 4     | 0          | Operações PIX                                  |
| organizze   | 19      | 0     | 0          | Financeiro Organizze (mesmo formato da Tradicional) |
| smartico    | 1       | 27    | 0          | CRM / Gamificação                              |
| logs        | 1       | 0     | 2          | Auditoria (`audit_changes`, 227 GB)             |
| marketing   | 3       | 2     | 0          | Campanhas                                       |
| msgs        | 3       | 0     | 0          | Mensagens                                       |
| backup      | 53      | 0     | 0          | Cópias antigas — não usar                       |
| **bc_orig** | 6       | 0     | 0          | ⚠️ **Não existe na Tradicional — não investigado ainda.** Nomes de tabela: `document`, `transaction`, `translation` entre outros, ~26 GB cada. Provável importação/migração de uma base anterior ("BC"?) — **não usar sem investigar primeiro** (ver regra de "sem correspondência" abaixo). |
| apuracao, arca, cron, fdw_data, tiger, topology, utils, web_assets | — | — | — | Pequenos/irrelevantes, mesmo padrão da Tradicional |

**Diferença notável vs. Tradicional**: não existe um schema `sigap` separado aqui — as tabelas
de SIGAP da Bravo vivem em `public` (ex.: `public.cpf_impedidos_sigap_queries`, 10 GB, 39M
linhas — grava toda consulta bruta ao SIGAP, é a fonte usada no relatório de furo SIGAP de
2026-09).

## Views e Materialized Views confirmadas (levantado em 2026-09-17)

**⭐ `public.vw_uw_balance` — confirmada, mesmo formato da Tradicional.** 56 colunas, incluindo
`entity_id`, `created`, `deposits`, `withdrawals`, `ggr`, `ngr`, `games_casino`, `games_sport`,
`games_prog`, `prizes_*`, `reward_*`, `ggr_prog`/`ggr_casino`/`ggr_sport`,
`ngr_prog`/`ngr_casino`/`ngr_sport`, `balance`, `balance_daily` — lista de colunas idêntica ao
que `query-trad` documenta para a Tradicional. Testado com dado real (01/09/2026): GGR e NGR do
dia retornaram valores plausíveis sem erro. **Use esta view para qualquer pergunta de
GGR/NGR/depósito/saque diário na Bravo**, mesma recomendação da Tradicional.

Outras views/mat. views existentes em `public` (nomes confirmados via metadados, conteúdo/
colunas não auditados um a um — confirmar antes de usar se a pergunta depender criticamente
delas): `vw_balances`, `vw_entity_balances`, `vw_entities_balance` (+ variantes `_today`/`_old`/
`_new` — mesmo padrão de gerações duplicadas da Tradicional, preferir a sem sufixo e checar
frescor), `vw_entries`, `vw_bonus_bi`, `vw_lottery_games`, `vw_winners`, `vw_web_winners`,
`vw_uw_funds`, `vwm_uw_balance` (materialized, espelho de `vw_uw_balance`),
`vwm_consolidated_daily_entries`, `vwm_consolidated_entry_balances`,
`vwm_consolidated_pending_operations`, `vwm_reseller_daily_balances`, `vw_gps_entities`
(materialized).

## Exemplos de queries frequentes (testado contra produção, 2026-09-17)

```sql
-- GGR/NGR/depósitos de um dia específico
SELECT SUM(ggr) AS ggr_total, SUM(ngr) AS ngr_total, SUM(deposits) AS depositos_total
FROM public.vw_uw_balance
WHERE created = DATE '2026-09-01';
-- Resultado real (01/09/2026): ggr ≈ R$ 471.902,70 · ngr ≈ R$ 323.649,53 · depósitos ≈ R$ 1.137.375,31
```

## Tabelas grandes — tratar com cautela (mesmo critério da Tradicional)

| Tabela | Tamanho | Linhas est. |
|---|---|---|
| `logs.audit_changes` | 227 GB | 171M |
| `integration.transactions` | 210 GB | 248M |
| `integration.bets` | 164 GB | 177M |
| `public.entries` | 92 GB | 236M |
| `public.access_logs` | 64 GB | 58M |
| `dwh.player_events` | 47 GB | 58M |
| `integration.rounds` | 37 GB | 149M |
| `integration.bet_sessions` | 27 GB | 161M |
| `bc_orig.document` / `bc_orig.transaction` | 26 GB cada | ~141-175M |
| `public.cpf_impedidos_sigap_queries` | 10 GB | 39M |
| `public.pending_operations` | 4,4 GB | 1,5M |
| `public.entities` | 3,7 GB | 837k |
| `public.cpf_queries` | 3,1 GB | 1,4M |
| `integration.sport_bets` | 1,4 GB | 223k |

Sempre filtrar por `entity_id`/`created` em qualquer uma dessas — nunca `GROUP BY` amplo sem
filtro (mesmo risco de timeout documentado para a Tradicional em `query-trad`).

## Fatos confirmados especificamente da Bravo — não replicar da Tradicional

**⚠️ Cada casa tem fornecedores e configuração próprios.** Confirmado por consulta direta
(agregada, zero PII) em 2026-09-15:

- **Fornecedor de KYC**: só **Legitimuz** (`data->>'kycProvider' = 'LEGITIMUZ'`, 663.230
  consultas em `public.kyc_pending_actions`). Praticamente nenhum registro de Serasa — a Bravo
  **não** usa os dois fornecedores como a Tradicional usa. Antes de conciliar uma fatura de KYC
  da Bravo, não assumir Serasa como opção.
- **Tipos de ação em `kyc_pending_action_types`** (diferente da Tradicional): `DA` =
  DeleteAccount, `EA` = EditAccount, `KC` = KYC, `PA` = PauseAccount, `RP` = RecoveryPassword,
  `WD` = Withdrawal. **Não existe o tipo `LR` (revalidação de login) confirmado na Tradicional**
  — sempre consultar `SELECT id, name FROM public.kyc_pending_action_types;` antes de assumir
  um código.
- **Agregadores de jogo cadastrados** (`integration.provider_aggregators`): Galaxsys, Everest -
  Sports Book, Softswiss, Vertical Loto, Banana Games, Plug N Play, Popok, Creedroomz — lista
  parecida com a da Tradicional, mas confirmar sempre por `cod`/`name` antes de assumir que um
  agregador existe também aqui.
- **`entity_type_id = 6` como "jogador"**: hipótese forte (mesma convenção usada no relatório de
  furo SIGAP e assumida como consistente com a Tradicional), mas **marcada como suposição não
  100% confirmada** no próprio relatório técnico de origem — reconfirmar se uma análise
  depender criticamente disso.
- **Convenção de soft-delete** (`deleted` = epoch `1970-01-01`, não `NULL`): não reconfirmada
  aqui ainda, mas é a mesma convenção usada em todo o código-fonte compartilhado — tratar como
  provável, confirmar com `MAX()`/amostra antes de uma decisão crítica.

## Sem correspondência clara no schema? Pare e pergunte

Se um pedido (de dado ou de auditoria de fornecedor) apontar para algo que não está mapeado
aqui — em especial qualquer coisa em `bc_orig`, ainda não investigado — **não force o encaixe
na tabela mais parecida**. Diga explicitamente que essa parte não está mapeada, e proponha
investigar antes de responder com um número. Um "não sei ainda, deixa eu confirmar" é sempre
preferível a uma resposta errada com confiança.

## Workflow ao receber uma pergunta sobre dados da Bravo

1. Confirme que a pergunta é mesmo sobre a Bravo (não Tradicional) — se ambíguo, pergunte.
2. Identifique a tabela/view certa usando o mapa acima; prefira `vw_uw_balance`/views existentes
   a reconstruir a lógica manualmente.
3. Monte a query com filtro de data sempre que possível.
4. Mostre o SQL e espere aprovação explícita antes de rodar.
5. Execute via `bravo-prd` pelo Bash.
6. Apresente o resultado em termos de negócio, sem PII crua, com a ressalva de que é dado da
   Bravo (não confundir com número equivalente da Tradicional).

## Contexto de origem

Este acesso existe desde 2026-09-15 (credencial de Ícaro via ClickUp), motivado pela
investigação `relatorio-tecnico-furo-sigap-bravo` (furo no bloqueio SIGAP por
`PROGRAMA_SOCIAL`, já corrigido — commit `5132ff98`, MR!276, ClickUp `868m4541a`). Esse
relatório já validou sete queries reais contra este banco (população SIGAP, recadastro,
depósito/saque via `pending_operations` tipos `SCCX`/`SRCX`, jogadas via
`integration.bets`/`sport_bets`) — bom ponto de partida para qualquer investigação futura que
envolva `cpf_impedidos_sigap_queries` ou `pending_operations`.
