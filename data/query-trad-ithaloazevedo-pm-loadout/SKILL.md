---
name: query-trad
description: >
  Skill para consultar o banco de dados PAM da Tradicional.bet.br (trad_prd).
  Use sempre que o usuário pedir dados, métricas, análises ou informações que
  venham do banco — número de jogadores, depósitos, saques, GGR, NGR, apostas,
  afiliados, bônus, KYC, transações PIX, funil de cadastro, ou qualquer outra
  métrica operacional. Aciona quando o usuário perguntar coisas como "quantos
  jogadores", "qual o GGR de hoje", "me mostra os saques pendentes", "quanto
  foi depositado", "relatório de afiliados", etc.
---

# Query PAM — Tradicional.bet.br

> **Renomeada em 2026-09-22** de `query-pam` para `query-trad`. O nome antigo dizia a
> tecnologia (o PAM), e as duas casas rodam o mesmo PAM — então ele não distinguia nada.
> `query-trad` e `query-bravo` nomeiam a casa, que é o que de fato muda: são bancos
> separados, com dados e configuração próprios.

Banco PostgreSQL `trad_prd` (read replica, acesso **somente SELECT** — o servidor
recusa qualquer escrita, não é questão de confiança). Ver manual de acesso pessoal
do usuário para credenciais e limites de sessão.

## Conexão

Não existe MCP Postgres configurado neste ambiente — a execução é via `psql` no
terminal, autenticado por token IAM da AWS (válido 15min por conexão nova).

**Se o alias `trad-prd` já estiver configurado no shell** (`~/.zshrc`):
```bash
trad-prd -c "SELECT ..."
```

**Caso contrário**, monte a conexão na hora:
```bash
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
export PGPASSWORD=$(aws rds generate-db-auth-token \
  --hostname ar-trad-prd-cluster.cluster-ro-c44onum4sztb.us-east-1.rds.amazonaws.com \
  --port 5432 --region us-east-1 --username ithalo_mendes \
  --profile trad-prd-ithalo_mendes)
psql "host=ar-trad-prd-cluster.cluster-ro-c44onum4sztb.us-east-1.rds.amazonaws.com port=5432 dbname=trad_prd user=ithalo_mendes sslmode=verify-full sslrootcert=$HOME/global-bundle.pem" \
  -c "SELECT ..."
```

| Campo    | Valor                                                              |
|----------|---------------------------------------------------------------------|
| Host     | ar-trad-prd-cluster.cluster-ro-c44onum4sztb.us-east-1.rds.amazonaws.com |
| Porta    | 5432                                                               |
| Database | trad_prd                                                           |
| Acesso   | Apenas SELECT                                                      |

## Regras de uso

- **Sempre mostre o SQL antes de rodar e espere aprovação explícita** — é conexão
  de produção real, sem desfazer. Nunca trate isso como aprovação automática,
  mesmo quando invocado por outro agente/orquestrador.
- Sempre use `LIMIT` em queries exploratórias (máx 1000 linhas).
- Filtre por data sempre que possível — o banco é grande; consulta sem filtro
  pode bater no timeout de 30min do endpoint de leitura.
- Use `created::date` para filtros de data em vez de `created` direto.
- Nunca tente `UPDATE`, `DELETE`, `INSERT` ou DDL — o banco recusa
  (`cannot execute ... in a read-only transaction`); se o pedido exigir escrita,
  explique a limitação e direcione para a equipe de infraestrutura.
- Prefira views e materialized views para análises — são mais rápidas.
- Para métricas financeiras diárias, use `public.vw_uw_balance` ou `public.vwm_uw_balance`.
- **Nunca exponha dado pessoal identificável** (CPF, telefone, e-mail, nome
  completo) na resposta — agregue ou anonimize antes de apresentar.

## Schemas disponíveis

| Schema      | Tabelas | Views | Mat. Views | Descrição                        |
|-------------|---------|-------|------------|-----------------------------------|
| public      | 133     | 35    | 13         | Core PAM                         |
| affiliates  | 23      | 5     | 4          | Afiliados e campanhas            |
| dwh         | 25      | 20    | 3          | Data Warehouse / BI              |
| integration | 25      | 4     | 2          | Integrações externas             |
| pix         | 10      | 4     | 0          | Operações PIX                    |
| organizze   | 19      | 0     | 0          | Financeiro Organizze             |
| sigap       | 20      | 1     | 0          | SIGAP                            |
| marketing   | 3       | 2     | 0          | Campanhas Meta                   |
| smartico    | 1       | 20    | 0          | CRM / Gamificação                |
| logs        | 1       | 0     | 2          | Auditoria                        |
| msgs        | 3       | 0     | 0          | Mensagens                        |

---

## Schema: public (Core PAM)

### Entidades

**`public.entities`** — Todos os participantes (jogadores, revendedores, afiliados)
Colunas: id, parent_id, entity_type_id, json_data, cod, email, status, parent_path, name, fullname, document, cpf, created, updated, deleted, entity_region_id, web_user_id

**`public.entity_types`** — Tipos de entidade
- **6 = jogador** (confirmado via `WHERE entity_type_id = 6` na própria `dwh.vw_funil_cadastro` de produção — não usar `1`, que está incorreto)
- (demais tipos via `SELECT * FROM public.entity_types`)

**`public.entities.json_flags ->> 'cadastroProgresso'`** — objeto JSON com timestamp por micro-evento do fluxo de cadastro (ex.: `telefoneInformado`, `emailEscolhaVista`, `kycIntroVista`, `enderecoConcluido`...). Instrumentação mais granular que os flags booleanos da `vw_funil_cadastro`; nem toda entidade tem esse campo populado (instrumentação aparentemente recente). Útil para funil de conversão etapa a etapa — ver exemplo de query abaixo.

**`public.users`** — Dados de login/acesso
Colunas: id, username, name, email, phone, password, role_id, created, updated, deleted, json_data, entity_id, cpf, document, birth_date, phone_verified, email_verified

**`public.entry_types`** — Tipos de lançamento (hierarquia ltree)
Colunas: id, parent_path, description, type, module, created, updated, deleted, entity_region_id, name

### Financeiro / Transações

**`public.entries`** — Todas as transações financeiras
Colunas: id, entity_id, entry_type_id, transaction, value, created

**`public.balances`** — Saldo atual por entidade e tipo de entrada
Colunas: id, entity_id, entry_type_id, qty, value, created, updated

**`public.withdraw_requests`** — Saques solicitados
Colunas: id, pending_operation_id, entity_id, json_data, status, created, updated, deleted

**`public.pending_operations`** — Operações pendentes (saques, pagamentos)
Colunas: id, pending_operation_type_id, entity_id, entry_id, params, value, status, created, updated, deleted, approved_by, json_data

**`public.credits`** — Créditos (comissões, bônus, prêmios)
Colunas: id, orig_entry_id, dest_entry_id, calculation_id, value, cod, extra_info, type

**`public.cupons`** — Cupons de saque/premiação
Colunas: id, withdraw_request_id, sweepstake_id, entity_id, entry_id, cod, value, json_data

### Bônus

**`public.web_bonuses`** — Bônus web (config, dt_start, dt_end...)
**`public.web_bonus_entities`** — Bônus concedidos por entidade (entity_id, value, expiration_date...)

### Loterias e Sorteios

**`public.lottery_games`** — Apostas realizadas
Colunas: id, sweepstake_id, transmission_id, game_number, value, created, updated, deleted, entity_id, json_data

**`public.lottery_guesses`** — Palpites das apostas
Colunas: id, sweepstake_id, lottery_header_id, value, guess, created, updated, deleted

**`public.lottery_guess_winners`** — Ganhadores por palpite
Colunas: id, lottery_guess_id, created, prize_range, modality_id, prize_value, hits, sweepstake_id, entry_id, entity_id, transmission_id, lottery_game_id, json_data, json_guess

**`public.sweepstakes`** — Sorteios
Colunas: id, ascertained_method_id, cod, dt_start, dt_end, dt_draw, hash, config, created, updated, deleted, entity_region_id, prize_config

**`public.transmissions`** — Transmissões de apostas
Colunas: id, entity_id, qty_games, value, created, entry_id, cod, crc, json_data, updated

**`public.modalities`** — Modalidades de aposta
Colunas: id, ascertained_method_id, name, config, created, updated, deleted, splitted_json, entity_region_id

**`public.drawn`** — Resultados dos sorteios
Colunas: id, sweepstake_id, prize_id, data, created, group, group_description

### KYC / Compliance

**`public.kyc_pending_actions`** — Ações KYC pendentes
Colunas: id, kyc_pending_action_type_id, entity_id, data, status, created, updated, deleted

**`public.documents`** — Documentos enviados
Colunas: id, document, description, entity_id, created, updated, deleted, file_name

**`public.cpf_queries`** — Consultas de CPF
Colunas: id, cpf, response, created, updated, deleted, json_data

---

## Views e Materialized Views principais (public)

### ⭐ vw_uw_balance — Principal para análises financeiras diárias
Colunas: entity_id, created (date), ftd_value, deposits, deposits_qty, withdrawals, withdrawals_qty, games_sold, games_played, prizes, reward, ggr, ngr, games_casino, games_sport, games_prog, prizes_casino, prizes_sport, prizes_prog, ggr_prog, ggr_casino, ggr_sport, ngr_prog, ngr_casino, ngr_sport, income_tax, balance_daily, balance

**Fórmulas:**
- GGR = games_played - prizes
- NGR = games_played + |credits_manual_sub| - (prizes + reward + credits_manual_add)

```sql
-- Exemplo: GGR/NGR do dia de hoje
SELECT
  SUM(ggr)   AS ggr_total,
  SUM(ngr)   AS ngr_total,
  SUM(deposits) AS depositos_total,
  SUM(withdrawals) AS saques_total
FROM public.vw_uw_balance
WHERE created = CURRENT_DATE;
```

**`public.vwm_uw_balance`** — Materialized view histórica (base da vw_uw_balance, mais rápida para ranges grandes)
**`public.vw_entries`** — Entradas com contexto da entidade
**`public.vw_entities_bi`** — Entidades para BI
**`public.vw_lottery_games`** — Jogos com contexto completo
**`public.vw_winners`** — Ganhadores com detalhes
**`public.vwm_consolidated_daily_entries`** — Entradas consolidadas por dia
**`public.vwm_consolidated_entry_balances`** — Saldos consolidados
**`public.vwm_consolidated_pending_operations`** — Operações pendentes consolidadas
**`public.vwm_web_user_resellers`** — Relação web users / revendedores

---

## Schema: affiliates

**`affiliates.affiliates`** — Cadastro de afiliados (id, affiliate_type_id, entity_id, parent_id, parent_path...)
**`affiliates.campaigns`** — Campanhas (id, affiliate_id, campaign_type_id, tag, url, name, config...)
**`affiliates.contracts`** — Contratos (id, name, contract_type_id, json_config...)
**`affiliates.contract_settlements`** — Liquidações de contrato (period_start, period_end, json_data...)
**`affiliates.clients`** — Clientes vinculados a campanhas (campaign_id, affiliate_id, entity_id...)

Views: vw_client_balance, vw_client_balance_aggregated, vw_clients_ftd, vw_contracts
Mat Views: vwm_affiliate_balances, vwm_affiliate_balances2, vwm_affiliate_balances_new

**⚠️ Pegadinha: `affiliates.vw_clients_ftd` só cobre clientes de afiliado, por construção** (`FROM affiliates.clients c JOIN pending_operations po ...`). Um `LEFT JOIN` dessa view para descobrir FTD de tráfego não-afiliado sempre retorna 0/nulo para quem não é cliente de afiliado — isso é artefato de escopo da view, não significa que tráfego direto não converte. Para FTD real de qualquer entidade, use a flag `COALESCE(entities.json_statistics ->> 'ftdEntryId', '') <> ''` (mesma usada em `dwh.vw_funil_cadastro`), não essa view.

**Origem de tráfego sem afiliado**: `dwh.tbl_utm_events_processed` tem `entity_id` direto (bigint) — colunas `utm_source`, `utm_medium`, `utm_campaign`, `is_ftd`, `created` (date). Útil para decompor tráfego "direto" (fora de `affiliates.clients`) por canal real; boa parte desse tráfego pode não ter nenhuma linha aqui (`sem_utm` — genuinamente não rastreado, não é erro).

---

## Schema: dwh (Data Warehouse / BI)

**`dwh.impedidos`** — CPFs impedidos (id, data, created, cpf, entity_id)
**`dwh.player_events`** — Eventos de jogadores (id, entity_id, player_event_type_id, created, detail, json_data)
**`dwh.operation_hourly_statistics_snapshots`** — KPIs operacionais por hora (44+ colunas de métricas)
**`dwh.ga4_events`** — Eventos GA4 (event_name, user_id, site, session_id, page, button, device...)
**`dwh.tbl_utm_events_processed`** — UTM processados (entity_id, entry_id, btag, utm_source...)
**`dwh.pay_broker_transactions`** / **`dwh.pay_qitech_transactions`** — Transações de pagamento

**⚠️ Pegadinhas de `dwh.player_events`** (confirmadas em 01/09/2026 reconciliando contra `public.entities`):
- **`created` é data de ingestão, não de ocorrência.** ~41% dos eventos que chegam num dia ocorreram em dias anteriores (p90 de atraso: 3,4 dias). Para recorte por dia real, use `(json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo'`. Atenção ao fuso: `created` está em horário local e `occurredAt` em UTC.
- **`registration_completed` (`RGC`) NÃO significa cadastro concluído.** O fluxo de revalidação de liveness no login reaproveita a instrumentação do cadastro: 96% dos disparos vêm de conta preexistente (mediana de 195 dias de idade). Para cadastro concluído use **`account_created` (`ACC`)**, que fecha 98–99% com `public.entities`.

**`public.kyc_pending_actions`** (tipo `KC`) — retorno bruto do provedor de KYC (SERASAEX) em `data`: `lastResult`, `lastStatus`, `lastRank`, `lastAlerts`, `lastIndicators`, `kycProvider`. É a única fonte com **motivo de reprovação** ("SEM RISCO APARENTE", "COM RISCO", "NÃO PASSÍVEL DE ANÁLISE", "ALERTA DE RISCO") — as flags de `entities` só dizem verificado/não verificado. Tipo `LR` = revalidação de login. ⚠️ `data` guarda **CPF em texto plano**: só agregar, nunca expor linha individual.

Views: `vw_funil_cadastro` (funil de cadastro — flags de telefone/e-mail/KYC + etapa_alcancada), vw_monitor_risks, vw_utm_data, vw_smartico_*, vw_bet_template
Mat Views: vwm_ngr_financeiro, vwm_utm_data, vwm_utm_events_base

---

## Schema: integration (Casino / Esportes)

**`integration.games`** — Jogos (id, name, game_category_id, config, provider_id...)
**`integration.providers`** — Provedores (id, name, cod, url, provider_aggregator_id...)
**`integration.bets`** — Apostas de casino (entity_id, value, status, json_data...)
**`integration.sport_bets`** — Apostas esportivas (id, entity_id, value, status, json_data, provider_id...)
**`integration.entity_sessions`** — Sessões (id, entity_id, client_ip, created, qty_bets...)

Mat Views: vwm_consolidated_game_stats, vwm_games

---

## Schema: pix

**`pix.transactions`** — Transações PIX (id, parent_path, dispatch_id, entity_id, value, json_data...)
**`pix.dispatches`** — Despachos (id, pending_operation_id, entity_id, status, created...)
**`pix.entity_keys`** — Chaves PIX (id, entity_id, key, created...)

Views: vw_dispatch_transactions_bi, vw_dispatches_bi, vw_transactions

---

## Schema: logs

**`logs.audit_changes`** — Auditoria de mudanças
Colunas: id, table_name, table_id, operation, data_prev, data_cur, created, user_id

Mat Views: vwm_consolidated_adquirente_entries, vwm_consolidated_adquirente_entries2

---

## Schema: smartico (CRM / Gamificação)

Views de sync: vw_smartico_users, vw_smartico_bet, vw_smartico_deposits, vw_smartico_withdrawals, vw_smartico_lottery_games, vw_smartico_sport_bets

---

## Exemplos de queries frequentes

```sql
-- Jogadores novos hoje
-- ⚠️ `deleted` usa sentinela 1970-01-01 para "não deletado", nunca NULL.
--    `deleted IS NULL` retorna zero em silêncio.
SELECT COUNT(*) FROM public.entities
WHERE entity_type_id = 6
  AND created::date = CURRENT_DATE
  AND deleted = TIMESTAMP '1970-01-01 00:00:00';

-- Funil de cadastro granular (cadastroProgresso) — % por etapa, hoje
WITH base AS (
  SELECT id, json_flags -> 'cadastroProgresso' AS cp
  FROM public.entities
  WHERE entity_type_id = 6
    AND created::date = CURRENT_DATE
    AND json_flags -> 'cadastroProgresso' IS NOT NULL
), total AS (
  SELECT COUNT(*) AS n FROM public.entities
  WHERE entity_type_id = 6 AND created::date = CURRENT_DATE
)
SELECT
  chave,
  COUNT(*) AS qtd,
  ROUND(100.0 * COUNT(*) / (SELECT n FROM total), 1) AS pct_do_total
FROM base, jsonb_each_text(cp) AS kv(chave, valor)
GROUP BY chave
ORDER BY qtd DESC;

-- Depósitos e saques da semana
SELECT
  created::date AS dia,
  SUM(deposits) AS depositos,
  SUM(withdrawals) AS saques,
  SUM(ggr) AS ggr
FROM public.vw_uw_balance
WHERE created >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY 1
ORDER BY 1;

-- Saques pendentes
SELECT COUNT(*), SUM(value)
FROM public.pending_operations
WHERE status = 'pending'
  AND deleted = TIMESTAMP '1970-01-01 00:00:00';

-- Top 10 afiliados por clientes ativos
SELECT a.id, COUNT(c.entity_id) AS clientes
FROM affiliates.affiliates a
JOIN affiliates.clients c ON c.affiliate_id = a.id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

---

## Workflow ao receber uma pergunta sobre dados

1. Identifique quais tabelas/views são relevantes usando o schema acima.
2. Monte a query com filtro de data sempre que possível.
3. **Mostre o SQL ao usuário e espere aprovação explícita** — nunca execute direto.
4. Execute via `trad-prd` (ou montagem manual do token+psql) pelo Bash.
5. Apresente o resultado de forma clara — tabelas, totais, variações quando útil, sem PII crua.
6. Se a query retornar muitos dados, agregue antes de apresentar.
