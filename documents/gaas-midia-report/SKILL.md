---
name: gaas-midia-report
description: Gera, direto no chat, a leitura de "gestão de report" de Mídia Paga (Meta+Google)
  do GaaS — mapeamento de campanha por objetivo de negócio, resultados recentes (spend/CTR/CPC/CPA
  por campanha/objetivo/canal) e alcance de meta/budget por objetivo. Roda SQL ao
  vivo contra o Supabase (projeto `mipiwxadnpwtcgfcedym`), sempre a partir das views
  ponderadas de mídia, nunca reagregando `paid_media_metrics` do zero. Use quando
  o usuário pedir "como está a mídia paga", "resultado das campanhas essa semana/mês",
  "alcance de meta de mídia", "campanhas sem mapeamento", ou quiser conferir divergência
  entre o mapeamento do dashboard e a classificação usada no relatório XLSX.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Mídia paga
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# GaaS — Report de Mídia Paga (Mapeamento, Resultados, Metas)

Você é o analista que dá ao operador uma leitura de 2 minutos sobre mídia paga —
mapeamento de campanha, resultado recente e alcance de meta. Roda SQL direto no
Supabase (`mcp__<supabase>__execute_sql`, `project_id = "mipiwxadnpwtcgfcedym"`) e
escreve a leitura **em texto, direto no chat** — esta skill não escreve em nenhuma
tabela nem gera arquivo. Para relatório executivo em Excel, use `gaas-relatorio-xlsx`;
para insight causal ligado a cartão/CAC, use `growth-brain-intelligence-engine`.

## Por que esta skill existe (o problema real)

Hoje **dashboard e relatório XLSX classificam a mesma campanha de dois jeitos
diferentes**:

- O dashboard (`CampaignMapperModal`/`CampaignMappingsModal`) usa um mapeamento
  manual campanha→objetivo salvo em `paid_media_campaign_mappings`, contra o
  catálogo dinâmico de 6 objetivos em `paid_media_objectives`
  (`marca, b2c, plurix, seguros, aquisicao, rentabilizacao`).
- O exportador XLSX (`midiaPagaMonthlyReportExport.ts` → `classifyFrente()`)
  **ignora esse mapeamento de propósito** e classifica por regex no nome da
  campanha em 4 "frentes" fixas (`Aquisição B2C, Aquisição Plurix, Marca B2C (Copa),
  Seguros`) — ver `references/taxonomia_divergente.md` para a tabela de
  correspondência e por que elas nem sempre batem.

**Esta skill nunca escolhe uma das duas sozinha.** O primeiro passo de qualquer
run é reconciliar: mostrar onde convergem, onde divergem, e quais campanhas não
têm mapeamento nenhum. Só depois disso ela lê resultado e meta.

## Princípios (gotchas reais encontrados em produção, 2026-07-14)

1. **Fonte de números de mídia = as views ponderadas**, nunca `paid_media_metrics`
   cru: `vw_media_campanha_mensal` (grão mês×plataforma×campanha) e
   `vw_media_ad_mensal` (mês×campanha×adset×ad, só linhas com `ad_id` — use para
   drill-down de criativo). Elas já fazem `sum/sum` (nunca `avg` de taxa) e não têm
   dupla contagem entre Meta (nível ad) e Google (nível campanha) — confirmado
   2026-06-10. Não reagregue `paid_media_metrics` do zero.
2. **Armadilha: a coluna `objetivo` da view NÃO é o objetivo de negócio.** É o
   objetivo bruto da campanha na plataforma (`app_installs, traffic, conversion,
   leads, awareness`) — o mesmo `objective` cru de `paid_media_metrics`, sem passar
   pelo mapeamento. Para o objetivo de negócio real (o que o dashboard mostra),
   sempre faça `LEFT JOIN paid_media_campaign_mappings m ON m.campaign_name =
   v.campanha` e use `m.objective`, nunca `v.objetivo`, quando for agrupar por
   objetivo de negócio.
3. **Formato de mês diverge entre tabelas** — `vw_media_campanha_mensal.mes` é
   `'YYYY-MM'` (ex.: `'2026-07'`); `paid_media_budgets.month` e
   `campaign_budgets.month` são `'MM/YYYY'` (ex.: `'07/2026'`). Sempre normalize
   antes de fazer join por mês (ex.: `to_char(to_date(v.mes,'YYYY-MM'),'MM/YYYY')`).
4. **`paid_media_budgets.objective` tem duplicidade de caixa** — já existiram no
   mesmo mês linhas `'aquisicao'` e `'Aquisicao'` para o mesmo objetivo (visto em
   05/2026). Sempre agrupe por `lower(trim(objective))` antes de somar budget por
   objetivo, senão o "budget total" fica errado (soma duas vezes ou aparenta linha
   perdida).
5. **`paid_media_targets` está vazia (0 linhas) e tem um bug conhecido**
   (`ProjectionBox` busca as chaves `'investimento'/'conversoes'/'cpa'`, mas o
   enum de `metric` só aceita `'spend'/'conversions'/'cpm'/'cpc'/'ctr'` — nunca
   bate). Não trate essa tabela como fonte de meta; se o usuário perguntar por que
   a "projeção" do app sempre diz "sem meta definida", essa é a causa raiz —
   avise, não tente consertar sem aprovação (é código do app, fora do escopo desta
   skill de leitura).
6. **CPA aqui é da plataforma** (clique/lead/instalação/conversão configurada),
   **não é CAC de cartão** (~R$6–18 no CRM). Nunca apresente CPA de mídia como se
   fosse custo de cartão. Se o usuário quiser essa ponte, a métrica é
   Spend-to-Card (correlação com `b2c_daily_metrics`, fora do escopo — direcione
   para o módulo "Mídia Analytics" do app ou para `useMediaCorrelation`).
7. **Campanha sem linha em `paid_media_campaign_mappings` = "sem_mapeamento"** —
   sempre reporte esse grupo separado, nunca deixe cair silenciosamente dentro de
   outro objetivo via `coalesce`.
8. **Só `channel` é confiável como `meta`/`google` já normalizado** — mas o
   objetivo bruto da plataforma (`traffic`, `conversion` etc.) varia por conta
   configurada; não assuma que o mesmo texto significa a mesma coisa entre Meta e
   Google.

## Workflow

### 1. Reconciliação de mapeamento (sempre primeiro)

Campanhas ativas numa janela recente sem mapeamento nenhum:

```sql
select distinct campaign
from paid_media_metrics
where date >= current_date - interval '35 days'
  and campaign not in (select campaign_name from paid_media_campaign_mappings)
order by 1;
```

Duplicidade de caixa/whitespace no catálogo de objetivos usado nos budgets (gotcha #4):

```sql
select month, objective, count(*) 
from paid_media_budgets
group by 1, lower(trim(objective))
having count(distinct objective) > 1;
```

Reporte ao usuário: quantas campanhas sem mapeamento, quais (nomes), e se algum
objetivo de budget está duplicado por caixa. **Não invente um mapeamento** —
pergunte ou sinalize para o usuário resolver na UI (`CampaignMapperModal`).

### 2. Resultados recentes (spend, CTR, CPC, CPA por objetivo/canal/campanha)

Sempre via view + join de objetivo de negócio (gotcha #2). Exemplo para o mês
corrente, por objetivo de negócio:

```sql
select coalesce(lower(trim(m.objective)), 'sem_mapeamento') as objetivo_negocio,
       sum(v.spend) spend, sum(v.impressoes) impressoes, sum(v.cliques) cliques,
       sum(v.conversoes) conv,
       round(sum(v.spend)/nullif(sum(v.cliques),0), 4) cpc_pond,
       round(sum(v.spend)/nullif(sum(v.conversoes),0), 2) cpa_pond,
       round(sum(v.cliques)::numeric/nullif(sum(v.impressoes),0)*100, 2) ctr_pond
from vw_media_campanha_mensal v
left join paid_media_campaign_mappings m on m.campaign_name = v.campanha
where v.mes = to_char(current_date, 'YYYY-MM')
group by 1
order by spend desc;
```

Para comparar com o mês anterior (tendência), rode a mesma query trocando
`v.mes = to_char(current_date - interval '1 month', 'YYYY-MM')` e calcule o delta
você mesmo (não invente % — derive de `spend`/`conv`/`cpa_pond` dos dois runs).

Para granularidade diária dentro de "últimas semanas", agregue direto de
`paid_media_metrics` só quando a pergunta for por dia (a view é mensal); mantenha
a mesma ponderação `sum(spend)/sum(clicks)` etc., nunca `avg` de uma coluna de
taxa já calculada.

Por campanha (drill-down), troque o `group by` para `v.campanha` e mantenha o
join de objetivo — assim você já entrega a campanha com seu objetivo de negócio
correto, sem confundir com o `objetivo` bruto da view.

### 3. Metas e alcance (realizado vs. budget por objetivo)

Fonte oficial: `paid_media_budgets` (objetivo/mês) + `campaign_budgets`
(campanha/mês), normalizando caixa e formato de mês (gotchas #3 e #4):

```sql
with budget_mes as (
  select lower(trim(objective)) objetivo, sum(budget::numeric) budget
  from paid_media_budgets
  where month = to_char(current_date, 'MM/YYYY')
  group by 1
),
realizado_mes as (
  select coalesce(lower(trim(m.objective)), 'sem_mapeamento') objetivo,
         sum(v.spend) realizado
  from vw_media_campanha_mensal v
  left join paid_media_campaign_mappings m on m.campaign_name = v.campanha
  where v.mes = to_char(current_date, 'YYYY-MM')
  group by 1
)
select coalesce(b.objetivo, r.objetivo) objetivo,
       b.budget, r.realizado,
       round(r.realizado / nullif(b.budget,0) * 100, 1) as pct_realizado,
       round(r.realizado / nullif(extract(day from current_date)::numeric,0)
             * extract(day from (date_trunc('month', current_date) + interval '1 month - 1 day'))::numeric, 2)
             as projecao_linear_fim_mes
from budget_mes b
full outer join realizado_mes r using (objetivo)
order by realizado desc nulls last;
```

Leia o resultado: objetivo com `realizado` e sem `budget` (ou `objetivo =
'sem_mapeamento'`) é orçamento não planejado — reporte como achado, não ignore.
Objetivo com `pct_realizado` muito acima/abaixo de "dias decorridos/dias do mês
× 100" indica ritmo fora do esperado — cite os números, não qualifique sem eles.

Se o usuário pedir alocação por campanha (não só por objetivo), use
`campaign_budgets` no lugar de `paid_media_budgets`, unindo por
`campaign_name = v.campanha` em vez de por objetivo — lembre que só 6 campanhas
tinham alocação fina na última checagem (2026-07-14), então a maioria do
"realizado" só bate no nível de objetivo, não de campanha individual.

### 4. Apresentar ao usuário

Resposta em PT-BR, direto no chat, com 3 blocos nesta ordem — sempre citando os
números crus, nunca qualificando sem eles:

```
📌 Mapeamento
  - N campanhas ativas sem mapeamento (últimos 35 dias): [nomes]
  - [se houver] Duplicidade de caixa em paid_media_budgets: [objetivo, meses]

📊 Resultados ({mês/período})
  - Por objetivo: spend, CPA, CTR, CPC — maior e menor eficiência
  - Tendência vs. mês anterior (delta %, sempre calculado, nunca estimado)

🎯 Metas e alcance
  - Por objetivo: budget vs. realizado vs. % vs. projeção linear fim de mês
  - Objetivos com spend sem budget cadastrado (achado, não ignorar)
```

## O que NÃO fazer

- Não escreva em nenhuma tabela do Supabase nem gere arquivo — a saída é texto no chat.
- Não escolha sozinho entre a taxonomia do dashboard e a do XLSX quando divergirem — reporte a divergência (ver `references/taxonomia_divergente.md`).
- Não trate `paid_media_targets` como fonte de meta (está vazia e quebrada).
- Não confunda CPA de plataforma com CAC de cartão.
- Não reagregue `paid_media_metrics` cru quando a pergunta cabe nas views mensais — só desça ao dado bruto para granularidade diária ou nível de criativo/ad.

## Referências

- `references/taxonomia_divergente.md` — tabela de correspondência entre o
  catálogo dinâmico de 6 objetivos (dashboard) e as 4 "frentes" fixas do XLSX,
  e onde exatamente elas podem divergir.
- `.claude/skills/gaas-relatorio-xlsx/` — exportador mensal em Excel (usa a
  classificação por regex `classifyFrente`, não o mapeamento do dashboard;
  budgets hardcoded em `FRENTE_BUDGET`/`MONTHLY_BUDGETS`, não conectados a
  `paid_media_budgets`).
- `.claude/skills/gaas-insight-engine/` — padrão de insight causal (CRM); mesma
  lógica de "confiança por volume" pode inspirar severidade aqui, mas esta skill
  não publica em `paid_media_insights`.
- `.claude/skills/gaas-momento-disparo/` — mesmo padrão de SQL direto contra o
  Supabase ao vivo em vez de script Python, usado como modelo desta skill.
