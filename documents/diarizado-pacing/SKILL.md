---
name: diarizado-pacing
description: Gera planilhas Excel (.xlsx) de Diarizado de Pacing no formato herdado
  da Jacto — gráficos de linha no topo (Realizado acumulado vs Meta acumulada), um
  cockpit de pacing por objetivo (Acumulado/Meta/Gap%/Projeção) e uma tabela diária
  com pares diário+acumulado por objetivo. Métricas em PT-BR. Use quando o usuário
  pedir "diarizado", "pacing diário", "acompanhamento diário de mídia paga", "planilha
  estilo Jacto", ou quiser projeção de fechamento de mês por objetivo/frente a partir
  de dados diários.
metadata:
  version: 1.0.0
  origin: cowork
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Relatórios
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Diarizado de Pacing (formato Jacto)

## O que esta skill gera
Uma planilha de acompanhamento diário de mídia paga com três camadas verticais, fiéis ao modelo Jacto:

1. **Gráficos no topo** — linha de Realizado acumulado (cor do objetivo) vs Meta acumulada (cinza tracejado), um por objetivo, lado a lado.
2. **Cockpit de pacing** — mini-painel por objetivo, com as métricas em LINHA (Investimento, Volume do KPI, Eficiência CPC/CPM/CPL, Status) e em COLUNA: Acumulado | Meta | Gap % | Projeção fim do mês.
3. **Tabela diária** — Data | Dia da semana | e, por objetivo, os pares [Investimento | Acumulado | Volume-KPI | Acumulado].

Tudo em português (Investimento, Cliques, Impressões, Leads, Eficiência, Status, dias Seg/Ter/...). Pacing é por **investimento** (métrica confiável), com a eficiência (CPC/CPM/CPL) ao lado — segue a boa prática de não pacear por conversão quando o tracking tem lag.

## Como usar
1. Monte um `config.json` (ver `assets/config_exemplo.json`) com:
   - `titulo`, `mes`, `dias_no_mes`, `paleta`, `fonte`
   - `objetivos`: lista, cada um com `nome`, `cor` (hex), `kpi_nome` (CPC/CPM/CPL), `kpi_tipo` (CPC/CPM/CPL), `kpi_volume_label` (Cliques/Impressões/Leads), `budget` (meta do mês) e `dados` = lista de `[data_iso, investimento_dia, volume_kpi_dia]`.
2. Rode: `python scripts/gerar_diarizado.py config.json saida.xlsx`
3. **Sempre** recalcule e valide com o script da skill xlsx: `python recalc.py saida.xlsx` (zero erros esperado).
4. Para conferir visualmente, renderize em PDF/imagem antes de entregar.

## Regras de fidelidade (não quebrar)
- Gráficos ficam no TOPO (linhas reservadas), nunca embaixo da tabela.
- Cockpit e tabela compartilham a MESMA grade de blocos (4 colunas por objetivo) para alinhar — não desalinhar os passos de coluna, senão os merges colidem.
- Acumulados são fórmulas Excel `=SUM(...)`, nunca valores hardcoded — a planilha tem que recalcular sozinha quando o dado muda.
- Meta acumulada = (budget / dias_no_mes) × dia. Projeção = acum / dias_decorridos × dias_no_mes.
- Métricas SEMPRE em PT-BR.

## Fonte do dado (contexto Afinz)
Os dados diários saem do Supabase `paid_media_metrics`, agregados por frente (objetivo) via tag do nome da campanha. Ver memória `midia_paga_report_framework`.
