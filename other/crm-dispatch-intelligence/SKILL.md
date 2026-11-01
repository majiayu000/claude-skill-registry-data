---
name: crm-dispatch-intelligence
description: Analisar granularmente cada disparo de aquisição CRM, comparando Activity
  Name, jornada, segmento, canal, oferta, BU e safra com disparos historicamente equivalentes.
  Use para relatórios de produção CRM, diagnóstico de funil, CAC, propostas, aprovados,
  cartões e identificação de disparos que exigem ação.
metadata:
  version: 1.0.1
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Análise CRM
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# CRM Dispatch Intelligence

## Objetivo

Explicar a performance de aquisição no nível do disparo sem esconder dispersão em médias agregadas.

## Pré-condição

Consumir o gate do `$growth-data-quality-monitor`. Respeitar todas as restrições.

## Unidade e baseline

Unidade: uma linha executada de `activities`, identificada por `Activity name / Taxonomia` e data.

Comparável preferencial:

`BU + Segmento + Canal + Etapa + Oferta + tipo de disparo`

Relaxar progressivamente quando a amostra for pequena e registrar o nível de relaxamento.

## Workflow

1. Selecionar somente aquisição e dias fechados.
2. Preservar os campos físicos e a taxonomia original.
3. Calcular por disparo:
   - base total e acionável;
   - custo;
   - abertura e clique quando disponíveis;
   - propostas, aprovados e cartões;
   - taxas derivadas válidas;
   - CAC.
4. Comparar com:
   - disparos equivalentes anteriores;
   - mediana histórica do grupo;
   - últimos 28 dias do grupo;
   - outros disparos do mesmo segmento na janela.
5. Calcular contribuição do disparo para cartões, custo e variação do segmento.
6. Identificar:
   - grande base com baixo resultado;
   - custo alto sem produção;
   - ganho de eficiência;
   - resultado concentrado;
   - campos ausentes que impedem diagnóstico.
7. Produzir ranking completo e destacar somente os itens materiais no resumo.

## Regras

- Não comparar aquisição fria com meio de funil.
- Não tratar conversão zero como dado ausente.
- Não usar média simples de CAC quando a soma de custo e cartões estiver disponível.
- Diferenciar dado nulo de zero.
- Não atribuir causa ao template sem evidência ou `template_id`.
- Registrar baixa confiança quando houver menos de três comparáveis.

## Saída

Seguir [shared-output-contract.md](references/shared-output-contract.md).

Para cada disparo emitir:

- `entity_type: dispatch`
- `entity_id`
- `activity_name`
- `business_date`
- dimensões completas;
- métricas;
- baseline e amostra;
- contribuição;
- achados;
- severidade;
- confiança;
- ação e critério de sucesso.

Emitir também:

- `top_positive_dispatches`
- `top_negative_dispatches`
- `dispatches_requiring_action`
- `coverage_summary`
