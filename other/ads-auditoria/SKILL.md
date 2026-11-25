---
name: ads-auditoria
description: Auditoria da carteira de contas de anúncio Meta da agência pelo Meta Ads MCP, só leitura. Use quando o usuário pedir revisão geral, "como estão as contas", "o que pegou fogo essa semana", auditoria semanal, contas travadas, sem pagamento ou bloqueadas, ou um panorama de todos os clientes. Produz uma tabela priorizada por conta com gasto, erros de entrega, anomalias e opportunity score, sem alterar nada.
---

# Auditoria da carteira (Meta Ads, só leitura)

**Objetivo:** em uma passada, saber quais contas estão gastando, quais estão travadas e onde agir primeiro. **Nada é alterado.** Se o usuário quiser agir numa recomendação, passar para `ads-diagnostico-cliente` ou `ads-montar-campanha`.

## Preparação
- Gerar um `client_conversation_id` de 20 caracteres (A-Z, a-z, 0-9) e repetir em todas as chamadas do Ads MCP.
- `client_model`: o modelo atual (ex.: `claude-opus-5-5`).
- `advertiser_request`: o pedido com as palavras do usuário.

- Se o usuário mantém uma lista de clientes ativos, auditar só essas contas. As outras só entram se ele pedir uma varredura geral.
- Se aparecer conta nova gastando que não está na lista, **perguntar** se é cliente novo, em vez de auditar.

## Passo a passo
1. **Mapear as contas:** `ads_get_ad_accounts` com `limit=100`. Se vier `next_cursor`, repetir com o cursor. Separar em grupos:
   - `is_ads_mcp_enabled=false` → fora do rollout. Só listar, não consultar.
   - `is_queryable=false` → mostrar `not_queryable_reason`. Normalmente é `UNSETTLED` (saldo pendente) ou `DISABLED`.
   - `has_payment_method=false` → listar como risco de parada.
2. **Descobrir quem está ativo:** para cada conta liberada e consultável, `ads_get_ad_entities` com `ad_account_id`, `level=ad_account`, `date_preset=last_30d` e `include_additional_context=false`. O campo padrão `amount_spent` basta.
   - Conta com gasto > 0 = **ativa** e entra na auditoria. Conta sem o campo `amount_spent` na resposta = gasto zero.
   - Se a resposta trouxer `next_actions`, executar em ordem todas as ações com `read_only=true` e `requires_user_confirmation=false` antes de seguir. Na prática vem `ads_insights_performance_trend` (usar `hide_ui=true`) e depois `ads_get_opportunity_score`.
3. **Campanhas no ar de cada conta ativa:** `ads_get_ad_entities` com:
   - `level=campaign` e `date_preset=last_30d`;
   - `fields=["id","name","effective_status","objective","amount_spent","results","cost_per_result"]`;
   - `filtering=[{"field":"campaign.effective_status","operator":"IN","value":["ACTIVE","WITH_ISSUES"]}]`;
   - `sort=amount_spent_descending`.
   - Isso dá o custo por resultado (conversa, visita ao perfil) de cada campanha no ar.
   - **Conta com gasto no período e nenhuma campanha no ar = "parou de rodar"**: perguntar se foi intencional.
4. **Para cada conta ativa,** fazer em paralelo:
   - `ads_get_errors` com `entity_ids` = **os IDs das campanhas no ar** (passo 3), não o ID da conta. No nível da conta a ferramenta devolve também os erros de campanhas antigas, pausadas há meses, e enche o relatório de ruído;
   - `ads_insights_anomaly_signal` com `ad_account_id`;
   - `ads_get_opportunity_score` com `ad_account_id` (pular se já veio pelo `next_actions`): nota de 0 a 100 + recomendações com `url`.
5. **Controle de equipe (opcional, se o usuário pedir):** `ads_account_get_activity_logs` com `start_time` de 7 dias atrás e `event_category=budget` ou `status`, para saber quem mexeu em orçamento ou status.
6. **Consolidar a tabela:** conta, ID, gasto em 30 dias, campanhas no ar com custo por resultado, erros nas campanhas no ar, anomalias, score, recomendação nº 1 (com `url`) e situação de pagamento.
7. **Priorizar:**
   - 🔴 entrega travada, conta desativada ou saldo pendente;
   - 🟠 anomalia de custo ou queda forte de resultado;
   - 🟡 recomendações do opportunity score;
   - ⚪ sem gasto no período.
8. **Separar observação de causa:** anomalia é sinal para investigar, não conclusão.

## Como ler os sinais
- **"Público estreito"** (`active_delivery_narrow_audience`) em conjunto de remarketing ou público quente é **esperado** pelo método (conversão roda para morno ou quente). Só vira problema em conjunto de topo ou de público frio.
- **Custo por conversa muito acima das outras campanhas da mesma conta** (ex.: R$ 31 contra R$ 8) é o melhor sinal de onde mexer.
- **Recomendação `budget_limited`** em campanha com custo por resultado baixo = proposta de escalar (só com o OK do usuário).
- **Na tabela, as recomendações vão com o `url` que a Meta devolve.** É o atalho que o usuário usa para aplicar no Gerenciador.

## Armadilhas conhecidas
- `ads_get_errors` no nível da conta traz erros de **todos** os filhos, inclusive campanhas antigas pausadas. Por isso, usar os IDs das campanhas no ar. Conta bloqueada aparece em `ads_get_ad_accounts`, não aqui.
- Campanhas antigas de impulsionamento podem aparecer como `ACTIVE` com gasto zero (já terminaram). Ignorar as que não têm gasto no período.
- No nível da conta não existe `cost_per_result`. Usar o nível de campanha.
- O opportunity score é **sempre da conta**. Nunca atribuir a uma campanha.
- O rollout do MCP é gradual: conta que hoje está fora pode entrar depois. Reler a cada auditoria.
- Com dezenas de contas, fazer as chamadas em lotes paralelos e não repetir leitura já feita na mesma conversa.
