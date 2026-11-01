---
name: growth-data-quality-monitor
description: Validar atualização, cobertura, completude, duplicidades e integridade
  das fontes usadas em relatórios de aquisição CRM e mídia paga. Use antes de qualquer
  análise diária ou semanal de growth, especialmente com Supabase, activities, rentabilizacao_activities,
  b2c_daily_metrics, paid_media_metrics, metas e logs de coleta.
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

# Growth Data Quality Monitor

## Objetivo

Determinar quais fontes, métricas e períodos podem sustentar conclusões. Executar antes dos demais especialistas.

## Contexto obrigatório

1. Ler `Afinz-CRM-Midia-Vault/09-Inteligencia-IA/Dossie-Mestre-Operacao-CRM-Midia.md`.
2. Ler as notas das tabelas analisadas quando houver dúvida de schema ou semântica.
3. Consultar dados vivos. Tratar snapshots do vault apenas como referência datada.

## Workflow

1. Descobrir nomes físicos das colunas antes de consultar.
2. Registrar mínimo, máximo e quantidade de datas distintas por fonte.
3. Comparar última data com o último dia fechado esperado.
4. Verificar cobertura diária nas janelas D-1, 7d, 14d e MTD.
5. Procurar duplicidades pela chave natural de cada fonte.
6. Contar nulos em dimensões e métricas críticas.
7. Verificar campanhas de mídia não mapeadas.
8. Ler fila e logs de coleta; separar dados presentes de job saudável.
9. Classificar cada fonte como `ready`, `partial`, `stale` ou `blocked`.
10. Emitir restrições explícitas para os agentes seguintes.

## Regras

- Não interpretar ausência de linha como produção zero.
- Não aceitar `created_at` como data de negócio.
- Usar intervalos semiabertos.
- Reportar Meta e Google separadamente.
- Marcar B2C como desatualizado quando não cobrir o mês corrente.
- Uma fonte pode ter dados recentes e coleta automática quebrada; registrar ambos.

## Saída

Seguir [shared-output-contract.md](references/shared-output-contract.md).

Preencher `data_quality` com:

- `source`
- `business_date_field`
- `min_date`
- `max_date`
- `expected_max_date`
- `missing_dates`
- `duplicate_count`
- `critical_nulls`
- `pipeline_status`
- `readiness`
- `restrictions`

Finalizar com um `gate`:

- `proceed`: todas as análises podem seguir.
- `proceed_with_limits`: informar quais conclusões estão limitadas.
- `stop`: fonte central indisponível ou schema não verificável.
