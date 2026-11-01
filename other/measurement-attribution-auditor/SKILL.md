---
name: measurement-attribution-auditor
description: Auditar confiabilidade de tracking, eventos de conversão, janelas, cobertura
  e atribuição em relatórios de CRM e mídia paga. Use quando conversões mudarem abruptamente,
  plataformas divergirem, houver gasto sem resultado, coleta falhar ou uma análise
  depender de relacionar mídia a cartões.
metadata:
  version: 1.0.1
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Qualidade e mensuração
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Measurement Attribution Auditor

## Objetivo

Definir o que pode ser interpretado como performance e o que deve permanecer como problema de mensuração.

## Pré-condição

Consumir o inventário do `$growth-data-quality-monitor`.

## Workflow

1. Identificar a definição de conversão usada por cada fonte e campanha.
2. Comparar eventos, objetivos e janelas entre períodos.
3. Verificar:
   - queda abrupta de conversões sem queda equivalente de tráfego;
   - mudança de nome, objetivo ou evento;
   - dados presentes com jobs de coleta falhando;
   - divergência entre plataforma e fonte operacional;
   - duplicidade ou ausência de eventos;
   - atraso de maturação.
4. Classificar cada métrica de resultado:
   - `trusted`
   - `directional`
   - `suspect`
   - `blocked`
5. Registrar hipóteses concorrentes, não uma causa única.
6. Definir testes de reconciliação e critério de liberação.

## Atribuição

- Tratar Spend-to-Card como correlacional.
- Não declarar incrementalidade.
- Não deduplicar Meta, Google e CRM sem chave ou regra verificável.
- Não misturar conversão view-through e click-through sem identificação.
- Não converter CPA de plataforma em CAC.

## Saída

Seguir [shared-output-contract.md](references/shared-output-contract.md).

Emitir:

- `metric_trust`
- `tracking_anomalies`
- `attribution_constraints`
- `reconciliation_tests`
- `blocked_conclusions`

Cada anomalia deve indicar evidência, hipóteses, risco de decisão e próximo teste.
