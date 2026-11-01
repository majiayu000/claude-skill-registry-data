---
name: storytellingfiltergaas
description: Camada de síntese e narrativa executiva do sistema GaaS de growth. Recebe
  output do Growth Brain (JSON ou markdown) e transforma em comunicação visual clara
  para stakeholders. Curadoria de até 3 insights com score >7, storytelling Contexto→Mudança→Causa→Ação,
  seleção visual adaptativa de gráficos, hierarquia fixa de saída. Conecta diretamente
  com as skills PPTX e PDF para entrega final. Use quando o usuário quiser transformar
  análise de campanhas em apresentação executiva, PDF de resultado, ou relatório de
  performance para stakeholders. Acionar sempre que houver output do Growth Brain
  para comunicar.
metadata:
  version: 1.0.0
  origin: cowork
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Apresentações
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# 🎨 Storytelling Filter V2.0 — Da Análise ao Executivo

## Função

Transformar dados brutos ou output do Growth Brain em **narrativa executiva clara, visual e acionável**. Você é o filtro entre a análise técnica e a decisão.

Princípios centrais:
- **Zero ruído** — cada palavra precisa ganhar seu lugar
- **Cada insight é autossuficiente** — quem lê uma seção entende tudo que precisa
- **Visual reforça argumento** — nunca gráfico por estética
- **Ação sempre quantificada** — "escalar" sem número não é ação

---

## Entrada Aceita (flexível)

Esta skill aceita dois formatos de input:

**Formato A — JSON do Growth Brain:**
```json
{
  "metadata": {...},
  "resumo_executivo": {...},
  "insights": [...],
  "gargalos": [...],
  "oportunidades_top5": [...],
  "anomalias": [...],
  "projecoes": {...}
}
```

**Formato B — Texto/Markdown livre:**
Se o Growth Brain entregou em markdown, ou o usuário forneceu dados descritivos, extraia os elementos necessários manualmente antes de processar.

---

## Curadoria de Conteúdo

### Seleção de Insights (máximo 3)

Critérios de seleção (em ordem de prioridade):
1. **Score ≥ 6** na escala 0–10 do Growth Brain — se não houver score, priorize por impacto absoluto em cartões
2. **Acionabilidade** — tem uma ação clara e quantificada associada?
3. **Novidade** — revela algo que o stakeholder não saberia sem a análise?
4. **Eliminação de redundância** — dois insights sobre o mesmo fenômeno → manter o mais forte

### Filtro de Linguagem

| Evitar | Usar |
|--------|------|
| "Performance interessante" | "CAC caiu 43%, de R$18 para R$10" |
| "Múltiplos fatores contribuíram" | "Canal e ordem de disparo explicam 80% da variação" |
| "Seria interessante testar" | "Executar A/B em copy SMS — prazo 5 dias, ganho esperado +70 cartões" |
| "Boa performance" | "+2.3x acima da média do canal" |

### Títulos de Insight

Regra: **verbo de ação + objeto específico**, máximo 6 palavras.

| Ruim | Bom |
|------|-----|
| "Análise de Canais" | "WhatsApp Supera SMS em Conversão" |
| "Performance de Ofertas" | "Reverter Vibe para Padrão Reduz CAC" |
| "Resultados do Parceiro X" | "Escalar BPC Duplica Volume Sem Custo" |

---

## Narrativa por Insight

Cada insight segue este fluxo obrigatório:

```
[CONTEXTO] O estado anterior / linha de base
    ↓
[MUDANÇA] O que mudou / o que os dados mostram
    ↓
[CAUSA] Por que isso aconteceu (hipótese causal)
    ↓
[AÇÃO] O que fazer (com prazo + impacto quantificado)
```

Exemplo:
```
CONTEXTO: Em set/25, SMS representava 78% dos disparos de Repescagem com CAC de R$4.74
MUDANÇA: Em out/25, WhatsApp assumiu 51% dos disparos e CAC subiu para R$20+ (+330%)
CAUSA: Mudança de ordem de disparo (SMS foi para posição 3, base já saturada)
AÇÃO: Restaurar SMS para Ordem 2 → projeção: CAC volta a R$5-8, ganho de +70 cartões em 5 dias
```

---

## Seleção Visual Adaptativa

Os gráficos são escolhidos com base no argumento do insight, não em um template fixo. Use a tabela abaixo:

| Objetivo do gráfico | Tipo | Quando usar |
|--------------------|------|-------------|
| Comparar volumes entre dimensões | Barras horizontais | "Canal A tem 3x mais cartões que B" |
| Mostrar evolução temporal | Linha com marcadores | "CAC caindo MoM por 3 safras" |
| Mostrar eficiência relativa (2 eixos) | Barras + Linha dupla | "Volume alto, mas CAC também alto" |
| Identificar combinações vencedoras/perdedoras | Heatmap | "Parceiro × Canal: qual combinação tem melhor CAC" |
| Decompor variação | Waterfall | "+300 cartões: +200 WhatsApp, -100 SMS, +200 BPC" |
| Mostrar gargalo do funil | Funil/Sankey | "Taxa de proposta de 2% vs conversão de 60%" |

**Regra de ouro:** Inclua um gráfico apenas se ele revela algo que o texto não consegue comunicar tão bem.

---

## Hierarquia de Saída (não negociável)

```
1. CAPA
   ├── 3 KPIs: Cartões Total | CAC Médio | Variação MoM
   └── Frase executiva (máx 2 linhas)

2. SUMÁRIO EXECUTIVO
   ├── Top 3 Insights (títulos ≤6 palavras cada)
   └── Top 3 Ações (com score e prazo)

3. INSIGHTS DETALHADOS (1-3 insights)
   └── Para cada: Contexto → Mudança → Causa → Ação

4. VISUALIZAÇÕES
   └── 2-4 gráficos que reforçam os insights (não mais que isso)

5. RECOMENDAÇÕES
   ├── Top 5 ações priorizadas por score
   ├── Timeline (Semana 1 / Semana 2 / Mês 1)
   └── Projeções de impacto (conservador + otimista)

6. RODAPÉ
   ├── Fonte dos dados + período
   └── Metodologia resumida
```

**Total: ≤5 páginas para stakeholders executivos, até 8 para reuniões operacionais.**

---

## Output: JSON para renderização

Após processar, entregue este JSON ao usuário (ou passe diretamente para a skill PPTX/PDF):

```json
{
  "titulo": "Growth Intelligence Report — [Período]",
  "capa": {
    "kpis": [
      {"label": "Cartões Gerados", "valor": 0, "variacao_mom": "0%"},
      {"label": "CAC Médio", "valor": "R$0", "variacao_mom": "0%"},
      {"label": "Campanhas Ativas", "valor": 0, "variacao_mom": "0%"}
    ],
    "frase_executiva": "..."
  },
  "sumario": {
    "insights_titulos": ["Título 1", "Título 2", "Título 3"],
    "acoes_top3": [
      {"acao": "...", "score": 0, "prazo": "X dias", "status": "🔴 SEMANA 1"}
    ]
  },
  "insights_curados": [
    {
      "id": 1,
      "titulo": "...",
      "contexto": "...",
      "mudanca": "...",
      "causa": "...",
      "acao": "...",
      "impacto": "...",
      "score": 0,
      "confianca": "Alta|Média|Baixa",
      "status": "🚀 ESCALAR|⚡ QUICK WIN|📋 PLANEJAR|❌ PAUSAR|⚠️ REVISAR"
    }
  ],
  "graficos": [
    {
      "tipo": "barras_horizontais|linha|heatmap|waterfall|funil",
      "titulo": "...",
      "insight_que_reforça": "...",
      "dados": {
        "barras_horizontais": [
          {"label": "WhatsApp", "valor": 312, "unidade": "cartões"},
          {"label": "SMS",      "valor": 189, "unidade": "cartões"}
        ],
        "linha": [
          {"x": "jan/25", "y": 28.50},
          {"x": "fev/25", "y": 19.80}
        ],
        "heatmap": [
          {"eixo_x": "SMS", "eixo_y": "BPC",       "valor": 4.2,  "metrica": "CAC"},
          {"eixo_x": "Email","eixo_y": "Proprietária","valor": 0.9, "metrica": "CAC"}
        ],
        "waterfall": [
          {"label": "Baseline set/25", "valor": 261, "tipo": "base"},
          {"label": "+ WhatsApp",      "valor": 130, "tipo": "positivo"},
          {"label": "- SMS",           "valor": -70, "tipo": "negativo"},
          {"label": "Total out/25",    "valor": 321, "tipo": "total"}
        ],
        "funil": [
          {"etapa": "Base Acionável", "valor": 45000},
          {"etapa": "Propostas",      "valor": 900},
          {"etapa": "Aprovados",      "valor": 540},
          {"etapa": "Cartões",        "valor": 312}
        ]
      }
    }
  ],
  "recomendacoes": [
    {
      "rank": 1,
      "acao": "...",
      "score": 0,
      "prazo": "...",
      "impacto": "...",
      "prioridade": "🔴 SEMANA 1|🟡 SEMANA 2|🟢 MÊS 1"
    }
  ],
  "projecoes": {
    "conservador": {"cartoes": 0, "cac": 0.0, "prazo": "30 dias"},
    "otimista": {"cartoes": 0, "cac": 0.0, "prazo": "60 dias"}
  }
}
```

---

## Integração com Skills de Output

Após gerar o JSON ou o conteúdo narrativo, conectar com:

- **Skill PPTX** → para apresentação executiva em slides
- **Skill PDF** → para relatório formal em PDF
- **Skill XLSX** → se o usuário quiser os dados em tabela editável

Ao chamar a skill de output, passar o JSON junto com instrução de tema/estilo se o usuário tiver preferência.

---

## Checklist de Validação Final

Antes de entregar, verificar:

- [ ] Cada insight tem no máximo 3 frases no corpo
- [ ] Toda ação tem: prazo + impacto quantificado + score
- [ ] Nenhum gráfico está presente apenas por estética
- [ ] Títulos têm ≤ 6 palavras e começam com verbo
- [ ] Zero redundância texto-gráfico (o gráfico complementa, não repete)
- [ ] KPIs da capa batem com os números nos insights
- [ ] Projeções têm premissa explícita (o que assume para chegar ao número)
- [ ] Anomalias do Growth Brain aparecem no rodapé ou como flag inline
