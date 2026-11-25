---
name: ads-diagnostico-cliente
description: Raio-x completo da conta de anúncio de UM cliente da agência pelo Meta Ads MCP. Use quando o usuário perguntar por que um cliente piorou, o que mudar numa conta, como está a campanha da Dra. X, se o custo por conversa ou por lead está alto, ou quiser uma análise para reunião ou relatório. Cruza métricas, tendência, benchmark do setor, leilão, erros, histórico de alterações e, quando existir, os dados reais do seu rastreador. Só leitura; mudanças viram propostas.
---

# Diagnóstico de um cliente (Meta Ads)

**Saída esperada:** um diagnóstico que separa o que é **observação** (número) do que é **causa provável**, e uma lista de **propostas** (nada é alterado aqui).

## Preparação
- Mesmo `client_conversation_id` (20 caracteres) em todas as chamadas, mais `client_model` e `advertiser_request`.

## Passo a passo
1. **Conferir os campos:** `ads_get_field_context` com os campos desejados (ex.: `amount_spent`, `results`, `cost_per_result`, `ctr`, `cpm`, `frequency`, `effective_status`). Usar só os nomes canônicos devolvidos.
2. **Campanhas no período:** `ads_get_ad_entities` com `level=campaign`, `date_preset=last_30d` (ou o período pedido), os `fields` conferidos e `sort` por gasto.
   - Se vier `next_actions`, executar em ordem as ações `read_only` antes de responder. É obrigatório.
3. **Descer de nível onde o gasto se concentra:** `ads_get_ad_entities` com `level=adset` e `level=ad`, usando `filtering` ou `object_ids`.
4. **Tendência:** `ads_insights_performance_trend`. Não aceita período. Usar `hide_ui=true` quando for parte de uma análise maior e `analysis_level` AD ou ADSET (uma chamada por nível).
5. **Comparação com o setor:** `ads_insights_industry_benchmark`, com `conversation_intent` e `conversation_topic` coerentes com o pedido. Olhar o custo por resultado, não o CPM.
6. **Leilão e sobreposição:** `ads_insights_auction_ranking_benchmarks`. Conjuntos competindo entre si viram proposta de consolidar.
7. **Bloqueios e oportunidades:**
   - `ads_get_errors` com `entity_ids` das campanhas ativas;
   - `ads_insights_anomaly_signal`;
   - `ads_get_opportunity_score` (a nota é da conta inteira).
8. **O que mudou:** `ads_account_get_activity_logs` dos últimos 14 dias, para cruzar a queda com edições de orçamento, público ou criativo.
9. **Resultado real (se houver rastreador ou CRM):**
   - Comparar com os leads, agendamentos e vendas registrados no rastreador ou no CRM.
   - O CPA real costuma ser diferente do custo por conversa do Meta.

## Como escrever o diagnóstico
- Começar pelo que mais pesa no dinheiro: onde está o gasto e o que ele está trazendo.
- Cada achado no formato **observação → causa provável → proposta**.
- Propostas concretas ("consolidar os conjuntos A e B", "trocar o criativo X que caiu de CTR"). Executar só depois do OK, pelas skills de criação.
- Texto que vai para o cliente: sem travessão, sem promessa de resultado.

## Armadilhas
- Não chamar `ads_insights_performance_trend` nem o opportunity score antes do `ads_get_ad_entities` inicial, a menos que o pedido seja só isso.
- No nível da conta não existe `cost_per_result` (cada campanha tem um tipo de resultado). Usar o nível de campanha.
- Campanha CTWA: o resultado do Meta é "conversa iniciada", não lead qualificado. Sempre que possível, cruzar com o seu rastreador ou o CRM.
- **Juntar conjuntos (recomendação `fragmentation`):**
  - conferir o `targeting` dos dois lado a lado; só é fragmentação de verdade se o público for o mesmo;
  - a junção completa leva o criativo do conjunto que sai para o que fica (anúncio novo com o mesmo `creative_id`, que preserva o post), soma os orçamentos e pausa o conjunto que sai;
  - nunca fazer só a metade (pausar sem levar o criativo): isso muda o mix de criativos.
