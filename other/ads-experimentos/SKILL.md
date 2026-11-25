---
name: ads-experimentos
description: Testes A/B e estudos de lift (incrementalidade) no Meta Ads MCP para clientes da agência. Use quando o usuário quiser provar ao cliente que o anúncio gera resultado, comparar criativos, públicos ou posicionamentos de forma controlada, ou consultar o resultado de um teste. Sempre checa elegibilidade antes e só cria com OK explícito, porque o teste roda de verdade e mexe na entrega.
---

# Experimentos: A/B e lift

**Quando vale:**
- **A/B:** responder "qual é melhor": criativo X contra Y, público A contra B.
- **Lift:** responder "o anúncio está causando resultado que não viria sozinho". É o argumento mais forte de retenção.

**Atenção:** as ferramentas da Meta tendem a sugerir criar o lift na hora. A regra é **propor, explicar o custo e esperar o OK**.

## Passo a passo
1. **Elegibilidade (sempre primeiro):** `ads_experiment_check_eligibility` com `ad_account_id` e, para A/B, `ad_entity_ids` das campanhas, conjuntos ou anúncios candidatos. Relatar para que tipo de teste a conta é elegível e os avisos.
2. **Testes que já existem:** `ads_experiment_list_tests`. Não abrir teste concorrente sem necessidade.
3. **Propor ao usuário:**
   - hipótese;
   - células;
   - KPI principal: para WhatsApp, `cost_per_action_type:onsite_conversion.messaging_first_reply`; para lead, `cost_per_action_type:lead`;
   - duração: A/B de 7 a 14 dias; lift com no mínimo 5 dias (padrão de 30);
   - impacto na verba.
4. **Criar só depois do OK:**
   - **A/B:** `ads_experiment_abtest_create_test`.
     - `cells` com **um** ID por célula, todos do mesmo nível e da mesma conta.
     - Datas em `AAAA-MM-DD`, começando no mínimo amanhã.
     - `primary_kpi` no formato `cost_per_action_type:<ação>` (nunca abreviado).
   - **Lift:** `ads_experiment_lift_create_test` com `ad_account_id`, `start_time` e `end_time`. A ferramenta mapeia sozinha pixel e objetivos.
5. **Acompanhar:**
   - `ads_experiment_abtest_get_test` / `ads_experiment_lift_get_test`;
   - ajuste de A/B com `ads_experiment_abtest_update_test`, também com OK.

## Leitura do resultado
- A/B: vencedor pelo KPI principal, com o nível de confiança informado pela Meta. Sem confiança suficiente = empate.
- Lift: conversões incrementais e o custo por conversão incremental. Traduzir para o cliente em linguagem simples, sem travessão.
