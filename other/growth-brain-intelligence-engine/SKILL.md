---
name: growth-brain-intelligence-engine
description: Motor de inteligência de growth da operação de aquisição de cartão de
  crédito (GaaS). Interpreta o framework de campanhas com conhecimento profundo das
  45 colunas, parceiros, jornadas, canais e etapas de funil. Gera insights causais,
  diagnóstico de gargalos e oportunidades priorizadas. Use sempre que o usuário quiser
  analisar campanhas, entender performance por safra, comparar canais/parceiros/ofertas,
  diagnosticar CAC, ou tomar decisões de alocação de budget. Quando o usuário mencionar
  campanhas, disparos, safra, CAC, cartões gerados, parceiros, jornada ou qualquer
  análise de growth, acione esta skill.
metadata:
  version: 1.0.0
  origin: cowork
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

# 🧠 Growth Brain V4.0 — GaaS Intelligence Engine

## Contexto: O que você sabe sobre esse sistema

Você está operando sobre o **GaaS (Growth as a Service)** — o framework central de gestão de campanhas de aquisição de cartão de crédito da operação de Growth Marketing. Cada linha da base representa uma **campanha/disparo** com até 45 dimensões.

Antes de qualquer análise, internalizar este vocabulário é mandatório. Não adivinhe — use as definições abaixo.

---

## CAMADA 0: INGESTÃO E ENTENDIMENTO DOS DADOS

### 0.1 Classificação de campanhas executadas vs. planejadas

**O campo `Disparado?` nem sempre está preenchido** — não confundir vazio com "não disparado". Use esta lógica em cascata e aceite como **executada** se qualquer condição for verdadeira:

1. `Disparado?` = "Sim"
2. `Status` ∈ {"Enviado", "Realizado"}
3. `Taxa de Entrega` > 0
4. Qualquer métrica de funil (`Propostas`, `Aprovados`, `Emissões`, `Cartões Gerados`) é > 0

Classificar como **Planejada** (excluir da análise de performance) apenas quando **todas** as condições abaixo forem verdadeiras:
- `Disparado?` vazio ou diferente de "Sim"
- `Status` ∈ {"Rascunho", "Scheduled"} ou vazio
- Todas as métricas de funil são nulas ou zero

> Misturar planejado com executado cria métricas falsas de zero performance e contamina qualquer benchmark. Mas descartar por falta de `Disparado?` quando há evidência de execução é igualmente problemático.

### 0.2 Limpeza de dados críticos

Ignorar linhas onde **todos** os seguintes campos são nulos/zero: Cartões Gerados, CAC, Propostas, Aprovados.

Flaggar (não ignorar) linhas com:
- `#DIV/0!` em qualquer campo de taxa → calcular manualmente se possível (Taxa = Volume/Base)
- `Base Acionável = 0` mas `Propostas > 0` → dado inconsistente, reportar
- `CAC > R$150` → alto, investigar se é erro ou caso real
- `Taxa de Conversão > 80%` com volume > 50 → suspeito, verificar sample

### 0.3 Decodificação da Taxonomia

O campo `Activity name / Taxonomia` codifica os atributos principais da campanha em um nome único. Estrutura:

```
{empresa}_{area}_{parceiro}_{tipo_comunicação}_{canal}_{publico}_{descricao}_{periodo}
```

Exemplo: `afz_car_vis_aqs_sms_bpc_aqsleadsparceirosbpcpadrão_pontual`
→ Afinz | Cartões | Visa (bandeira do cartão — raramente varia) | Aquisição | SMS | Público: Parceiro BPC | descrição da jornada | pontual

> `vis` = bandeira Visa. É um campo identificador do produto, não do parceiro comercial. Na prática quase não muda entre campanhas — use-o apenas para confirmar o produto quando necessário, não como dimensão de análise.

**Dicionário completo de siglas:**

| Categoria | Nome | Sigla |
|-----------|------|-------|
| **Empresa** | Afinz | afz |
| | Plurix | plu |
| | Seguros | seg |
| | Sem Parar | spm |
| **Área** | Antecipação de Recebíveis | arv |
| | Cartões | car |
| | Cobrança | cob |
| | Compra Planejada | pnj |
| | Empréstimo | emp |
| | Fidelidade | fid |
| | Maquininha | maq |
| | Recorrente e Assinaturas | rec |
| | Seguros | seg |
| | Não se aplica | nsa |
| **Parceiro** | A e M | aem |
| | Alvorada | alv |
| | B2B2C | bbc |
| | B2C | b2c |
| | Bem Barato | bbt |
| | Boa | boa |
| | Dom Olivio | dom |
| | MoneyMoney | mmy |
| | Nomad | nom |
| | Pagolivre | pgl |
| | Paraná | par |
| | Plurix | plx |
| | Serasa | srs |
| | Vibe | vib |
| | Visa | vis |
| | Visa Classic | cla |
| | Não se aplica | nsa |
| **Tipo de Comunicação** | Aquisição | aqs |
| | Cobrança | cob |
| | Relacionamento | rel |
| | Rentabilização | rnt |
| | Transacionais | trs |
| | Tombamento | tbm |
| | Regulatórios | reg |
| **Canal** | E-mail | email |
| | Push | push |
| | SMS | sms |
| | WhatsApp Marketing | wpp |
| | WhatsApp Utility | wpu |
| | WhatsApp Sessão | wps |
| | RCS | rcs |
| | Instagram | ins |
| | Facebook | fac |
| **Público** | Abandono | abn |
| | Acordo Certo | ac |
| | Alvorada | alv |
| | Aprovados | apr |
| | Aprovados não convertidos | anc |
| | Ativo com limite | atl |
| | Ativo Geral | atv |
| | Base Proprietária | bsp |
| | Bureaus | bur |
| | Carrinho Abandonado | car |
| | Cartonista | cart |
| | Dia | dia |
| | Negados | neg / ngd |
| | Parceiro Bom Pra Crédito | bpc |
| | Parceiro Serasa | srsa |
| | Pré Analisados | pre |
| | Prospect | pro |
| | Upgrade de Oferta | upo |
| | Não se aplica | nsa |
| | Todos | tds |
| **Período** | Manhã | ma |
| | Tarde | ta |
| | Noite | no |
| | Madrugada | md |
| | Todos | td |

Use o dicionário para reconstruir a dimensão correta quando os campos da planilha estiverem incompletos ou em branco. Exemplo: se `Parceiro` está vazio mas a taxonomia contém `_srs_`, o parceiro é Serasa.

---

## VOCABULÁRIO DO FRAMEWORK (conhecimento obrigatório)

### Business Units (BU)
| BU | Descrição | Cor |
|----|-----------|-----|
| B2C | Business to Consumer — base proprietária e leads diretos | Azul |
| B2B2C | Business to Business to Consumer — parceiros varejistas | Verde |
| Plurix | Plataforma Plurix | Roxo |

### Etapas de Aquisição (funil)
| Etapa | Quando usar | Perfil esperado |
|-------|-------------|-----------------|
| Topo de Funil | Primeira oferta para lead frio | Taxa Proposta baixa, volume alto |
| Meio de Funil | Lead que já interagiu mas não converteu | Taxa Conversão maior, volume menor |
| Fundo de Funil | Oportunidade quente — proposta aberta, carrinho abandonado | Alta conversão, **volume pequeno** (gargalo estratégico), custo não necessariamente maior |

> **Nota sobre Fundo de Funil:** É a etapa com maior taxa de conversão, mas representa o menor volume absoluto da operação. Um dos objetivos estratégicos do growth é **aumentar o volume de leads que chegam ao fundo de funil** — não apenas converter os que já estão lá. Ao analisar, sempre separar o diagnóstico em duas perguntas: (1) a conversão dentro do fundo está boa? e (2) estamos alimentando volume suficiente nessa etapa?

### Jornadas (tipos de campanha)
| Jornada | Trigger | Público |
|---------|---------|---------|
| Aquisição | Entrada de nova base de leads | Leads proprietários e parceiros |
| Carrinho Abandonado | Lead simulou proposta ou confirmou em parceiro | Negados com chance + Aprovados que não finalizaram |
| Reativação | Leads sem resposta em até 15 dias | Bases que passaram por aquisição |
| Quarentena | Leads que não responderam múltiplas ações | Descanso forçado, sem ativação por 6 meses |

### Parceiros e perfis típicos
| Parceiro | Sigla | BU | Perfil |
|----------|-------|-----|--------|
| Proprietária | PROPRI | B2C | Base interna, alta qualidade, custo baixo |
| Bom Pra Crédito | BPC | B2C | Leads pré-qualificados, whitelist forte |
| Serasa | SRS | B2C | Leads com scoring externo, boa propensão |
| Dia | DIA | B2B2C | Base CRM varejista, volume alto |
| Alvorada | ALV | B2B2C | Base CRM varejista |
| Acordo Certo | AC | B2C | Perfil de renegociação de dívida |
| Plurix | PLX | Plurix | Base própria da plataforma |
| Institucional | INST | B2C | Campanhas institucionais sem parceiro |

### Canais
| Canal | Custo | Engajamento | Melhor uso |
|-------|-------|-------------|-----------|
| E-mail | Muito baixo | Médio (abertura ~20-30%) | Volume alto, nurturing, leads quentes |
| SMS | Baixo | Alta entrega, baixo clique | Urgência, ação rápida |
| WhatsApp | Médio | Alto (clique > email) | Conversão, carrinho abandonado |
| Push | Baixo | Variável | App owners, base engajada |

### Perfis de Crédito
| Perfil | Descrição |
|--------|-----------|
| Mar Aberto | Sem pré-análise de crédito, mercado amplo |
| Pré-analisado | Análise prévia de crédito realizada |
| Whitelist | Lista aprovada previamente |
| Negados | Foram negados mas têm chance de aprovação |

### Tipos de Oferta
| Tipo | Exemplos |
|------|---------|
| Padrão | Oferta base sem diferencial |
| 200 Vibes | Produto Vibe com bônus de pontos |
| Limite | Oferta focada em limite de crédito |
| Anuidade grátis | Isenção de anuidade |
| Cashback | % de retorno em compras |

---

## MODELO DE DADOS — 45 COLUNAS POR CATEGORIA

### Identificação
`Activity name/Taxonomia`, `Jornada`, `Disparado?`, `Status`, `prog_gaas`

### Segmentação (8 dimensões de análise)
`BU`, `Segmento`, `SIGLA_Segmento`, `Parceiro`, `SIGLA_Parceiro`, `Subgrupos`, `Etapa de aquisição`, `Perfil de Crédito`

### Produto & Oferta
`Produto`, `Oferta`, `Promocional`, `SIGLA_Oferta`, `Oferta 2`, `Promocional 2`, `Canal`, `Ordem de disparo`

### Temporal
`Data de Disparo`, `Data Fim`, `Safra`, `Horário de Disparo`, `Ordem de disparo`

### Métricas de Base
`Base Total`, `Base Acionável`, `% Otimização de base`

### Métricas Financeiras
`Custo Unitário Oferta`, `Custo Total da Oferta`, `Custo unitário do canal`, `Custo total canal`, `Custo Total Campanha`, `CAC`

### Métricas de Funil (sequência obrigatória)
```
Base Acionável
  → Taxa de Entrega    → Entregues
  → Taxa de Abertura   → Abertos
  → Taxa de Clique     → Cliques
  → Taxa de Proposta   → Propostas
  → Taxa de Aprovação  → Aprovados
  → Taxa de Finalização → Emissões
  → Cartões Gerados (Emissões Independentes + Emissões Assistidas)
  → Taxa de Conversão  = Cartões / Base Acionável
```

---

## CAMADA 1: DATA INTERPRETER

### Perguntas obrigatórias ao receber dados

1. **Escopo temporal:** Quais safras estão presentes? Qual é o range de datas?
2. **Volume:** Quantas campanhas executadas? Quantas planejadas?
3. **BUs ativas:** Quais BUs têm dados suficientes para análise?
4. **Completude:** Quais dimensões têm dados suficientes (>30 campanhas)?
5. **Anomalias:** Há `#DIV/0!`? Campos de métrica todos zerados?

### Métricas derivadas a calcular sempre

```
CAC real          = Custo Total Campanha / Cartões Gerados
Yield Rate        = Cartões Gerados / Base Acionável  (conversão end-to-end)
Custo/Proposta    = Custo Total / Propostas
Taxa Efetiva      = Aprovados / Propostas
Eficiência Canal  = Cartões / Custo Total Canal
```

---

## CAMADA 2: GROWTH INSIGHT ENGINE

### Framework PICO (Pattern → Insight → Cause → Opportunity)

#### 2.1 Análise multidimensional obrigatória

Analisar performance cruzando **pelo menos 3 das seguintes dimensões**:
- BU × Canal
- Parceiro × Etapa de Aquisição
- Oferta × Perfil de Crédito
- Jornada × Safra (evolução temporal)
- Canal × Ordem de Disparo (saturação)
- Segmento × Subgrupo

> Por que cruzar dimensões: uma campanha de E-mail Proprietária em Topo de Funil tem benchmark completamente diferente de E-mail BPC em Meio de Funil. Analisar canal isolado não diz nada.

#### 2.2 Raciocínio causal — por que as taxas variam

| Causa | Sinal | Diagnóstico |
|-------|-------|-------------|
| Segmentação ruim | Taxa Proposta < 2%, Conversão > 50% | Base chega mas não é atraída — problema de copy/canal, não de oferta |
| Oferta desalinhada | Taxa Proposta OK, Aprovação baixa | Proposta gerada mas produto não encaixa no perfil |
| Friccão no checkout | Aprovação OK, Finalização baixa | Fluxo de emissão tem problema operacional |
| Canal saturado | Queda progressiva MoM na mesma jornada | Frequência alta demais, base esgotada |
| Perfil errado | CAC alto + todas taxas baixas | Parceiro/segmento não é propício para este produto |

#### 2.3 Template de Insight

```
INSIGHT: [Declaração clara — máximo 2 linhas]

EVIDÊNCIA:
- [Métrica 1 com contexto comparativo]
- [Métrica 2 com contexto comparativo]

CAUSA PROVÁVEL: [Hipótese baseada no framework de causalidade]

CONFIANÇA: Alta/Média/Baixa
[Justificativa: sample size, consistência histórica]

OPORTUNIDADE: [O que fazer com esse conhecimento]
```

#### 2.4 Diagnóstico de Gargalo de Funil

```
Gargalo ATRAÇÃO (Base → Proposta)
  Sinal: Taxa Proposta < 3%, Conversão > 45%
  Ação: Testar copy, mudar canal, revisar segmento

Gargalo CONVERSÃO (Proposta → Cartão)
  Sinal: Taxa Proposta > 4%, Conversão < 35%
  Ação: Simplificar fluxo, melhorar oferta, reduzir fricção na emissão

Gargalo APROVAÇÃO (Proposta → Aprovado)
  Sinal: Taxa Aprovação < 50%
  Ação: Revisar perfil de crédito, refinar segmentação, whitelist

Gargalo FINALIZAÇÃO (Aprovado → Emitido)
  Sinal: Taxa Finalização < 70%
  Ação: Problema operacional — régua de ativação pós-aprovação

Gargalo CUSTO (Taxas OK, CAC alto)
  Sinal: Boa conversão, CAC > 1.5x média
  Ação: Negociar custo de canal/oferta, aumentar volume para diluir fixo
```

---

## CAMADA 3: OPPORTUNITY MAPPER

### Scoring de Oportunidade (escala 0–10)

Cada oportunidade recebe um score de 0 a 10, calculado assim:

```
Score (0–10) = (Impacto × 0.40) + (Facilidade × 0.30) + (Confiança × 0.20) + (Alinhamento × 0.10)

Impacto (0–10):
  10 = melhoria >50% nos cartões ou >30% de redução de CAC
   7 = melhoria de 20–50% nos cartões
   4 = melhoria de 5–20%
   1 = impacto marginal (<5%)

Facilidade (0–10):
  10 = ação imediata: apenas ajuste de budget, copy ou ordem de disparo (1–3 dias)
   6 = requer A/B test ou novo criativo (1–2 semanas)
   3 = nova infra, parceiro ou integração (1+ mês)

Confiança (0–10):
  10 = >50 conversões, performance consistente em ≥3 safras
   6 = 15–50 conversões ou consistente em 2 safras
   3 = <15 conversões ou dado em apenas 1 safra

Alinhamento (0–10):
  10 = move CAC na direção do target E aumenta volume
   5 = melhora uma dimensão sem piorar a outra
   0 = melhora volume mas piora CAC acima do aceitável
```

**Referência de interpretação:**
- Score ≥ 8 → 🚀 ESCALAR JÁ
- Score 6–7 → ⚡ QUICK WIN
- Score 4–5 → 📋 PLANEJAR
- Score < 4 → ❌ IGNORAR ou ⚠️ REVISAR dados

### Matriz de Priorização

```
           │ Alto Impacto     │ Baixo Impacto
───────────┼──────────────────┼──────────────────
Alta       │ 🚀 ESCALAR JÁ   │ ⚡ QUICK WIN
Facilidade │ prioridade 1     │ faça se sobrar tempo
───────────┼──────────────────┼──────────────────
Baixa      │ 📋 PLANEJAR     │ ❌ IGNORAR
Facilidade │ roadmap próx.    │ não vale o esforço
```

---

## CAMADA 4: OUTPUT ESTRUTURADO

### Formato de saída (JSON para Storytelling Filter)

O output desta análise deve ser um JSON estruturado assim:

```json
{
  "metadata": {
    "periodo": "jan/25 - nov/25",
    "campanhas_analisadas": 904,
    "bus_cobertas": ["B2C", "B2B2C"],
    "gerado_em": "YYYY-MM-DD"
  },
  "resumo_executivo": {
    "cartoes_total": 0,
    "cac_medio": 0.0,
    "variacao_mom": 0.0,
    "tldr": "Frase executiva de 1-2 linhas com o bottom line"
  },
  "insights": [
    {
      "id": 1,
      "titulo": "Verbo + Objeto (máx 6 palavras)",
      "padrao": "O que aconteceu",
      "causa": "Por que aconteceu",
      "oportunidade": "O que fazer",
      "metricas": ["dado 1", "dado 2"],
      "score": 0,
      "confianca": "Alta|Média|Baixa",
      "status": "🚀 ESCALAR|⚡ QUICK WIN|📋 PLANEJAR|❌ PAUSAR"
    }
  ],
  "gargalos": [
    {
      "tipo": "ATRAÇÃO|CONVERSÃO|APROVAÇÃO|FINALIZAÇÃO|CUSTO",
      "campanha": "nome ou segmento afetado",
      "diagnostico": "o que está travando",
      "acao": "o que fazer"
    }
  ],
  "oportunidades_top5": [
    {
      "rank": 1,
      "acao": "descrição",
      "impacto": "+X cartões/mês",
      "facilidade": "Alta|Média|Baixa",
      "prazo": "X dias",
      "score": 0
    }
  ],
  "anomalias": ["lista de flags para investigação"],
  "projecoes": {
    "conservador_30d": {"cartoes": 0, "cac": 0.0},
    "otimista_60d": {"cartoes": 0, "cac": 0.0}
  }
}
```

> Se o destinatário pedir markdown em vez de JSON, converta para o formato Report (seção abaixo).

### Formato Report (markdown alternativo)

```markdown
# 🧠 Growth Brain — Intelligence Report
**Período:** [safras] | **BU:** [BUs] | **Base analisada:** [N campanhas]

## 📊 Bottom Line
[TL;DR em 2-3 frases: o que mais importa]

**Maior Win:** [X]
**Maior Risco:** [Y]

## 🔥 Top Insights

### 1. [Título com verbo]
[Contexto → Mudança → Causa → Ação]
**Impacto:** [métrica]
**Confiança:** [nível] — [justificativa]

## 🎯 Top 5 Ações
1. 🚀 [ação] — [impacto estimado]
2. ...

## 🔍 Gargalos Prioritários
[diagnóstico por tipo]

## ⚠️ Anomalias para Investigar
[flags]
```

---

## REGRAS INEGOCIÁVEIS

❌ Nunca classifique como executada uma campanha sem nenhum sinal de execução (métricas zeradas, status Rascunho/Scheduled, Disparado? vazio)
❌ Nunca compare BUs diferentes sem separar a análise
❌ Nunca cite uma métrica sem contexto comparativo ("CAC R$15" → "CAC R$15, 2.3x acima da média de R$6.5")
❌ Nunca liste métricas sem interpretar causalidade
❌ Nunca recomende pausar sem primeiro verificar se o sample é suficiente (>30 conversões)

✅ Sempre aplique a regra cascata de execução (seção 0.3) antes de calcular qualquer métrica — `Disparado?` vazio não significa planejada se houver sinais de execução
✅ Sempre use o dicionário de taxonomia (seção 0.4) para reconstruir dimensões quando campos individuais estiverem em branco
✅ Sempre analise pelo menos 3 dimensões cruzadas
✅ Sempre sinalize anomalias antes de interpretar
✅ Sempre produza output em JSON (ou markdown se explicitamente pedido)
