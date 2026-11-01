---
name: paid-media-campaign-analyst
description: Analisar campanhas de mídia paga individualmente e, quando disponível,
  detalhar adsets, anúncios e criativos. Use para relatórios de Meta e Google com
  spend, impressões, alcance, frequência, cliques, CTR, CPC, CPM, conversões, CPA,
  pacing, campanhas sem resultado e ações por campanha.
metadata:
  version: 1.0.1
  origin: codex
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

# Paid Media Campaign Analyst

## Objetivo

Transformar métricas de mídia em diagnóstico e ação no nível de campanha, preservando diferenças de plataforma e objetivo.

## Pré-condição

Consumir o gate do `$growth-data-quality-monitor` e as restrições do `$measurement-attribution-auditor`.

## Hierarquia

Analisar na ordem:

`plataforma -> objetivo -> campanha -> adset -> anúncio/criativo`

Não forçar níveis ausentes.

## Workflow

1. Separar Meta e Google.
2. Resolver mapeamento de objetivo antes de comparar campanhas.
3. Calcular por campanha:
   - spend e participação no total;
   - impressões, alcance e frequência;
   - cliques, CTR, CPC e CPM;
   - conversões e CPA de plataforma;
   - cobertura diária.
4. Comparar:
   - último dia vs. média anterior;
   - 7d vs. 7d;
   - MTD;
   - histórico próprio de 28d.
5. Decompor alterações por adset e anúncio quando possível.
6. Sinalizar:
   - gasto sem conversão;
   - aumento de frequência com queda de CTR;
   - aumento de CPC/CPM;
   - tracking suspeito;
   - campanha sem mapeamento;
   - concentração excessiva de orçamento;
   - campanha eficiente com baixa participação.
7. Separar diagnóstico de tráfego de diagnóstico de conversão.

## Regras

- CPA é conversão de plataforma, não CAC de cartão.
- Não comparar objetivos diferentes como se fossem equivalentes.
- Não recomendar realocação quando tracking estiver bloqueado.
- CTR de Google e Meta pode ter semântica e inventário distintos.
- Frequência ausente no Google não deve virar zero real.
- Campanha de rentabilização em mídia é analisada até clique quando não houver métrica posterior confiável.

## Saída

Seguir [shared-output-contract.md](references/shared-output-contract.md).

Para cada campanha emitir:

- identidade e objetivo;
- métricas e participação;
- comparações;
- cobertura;
- diagnóstico de tráfego;
- diagnóstico de conversão;
- restrição de measurement;
- severidade, confiança e ação.

Incluir:

- `campaigns_requiring_action`
- `spend_without_conversion`
- `efficient_campaigns`
- `tracking_suspects`
