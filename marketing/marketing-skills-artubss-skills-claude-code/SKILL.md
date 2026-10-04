---
name: "marketing-skills"
description: "42 skills e plugins de marketing para agentes Claude Code. 7 pods: conteúdo, SEO, CRO, canais, crescimento, inteligência, vendas. Contexto base + roteador de orquestração. 27 ferramentas Python (somente stdlib)."
version: 2.0.0
author: Ric Neves - Flowgrammers
license: MIT
tags:
  - marketing
  - seo
  - content
  - copywriting
  - cro
  - analytics
  - ai-seo
agents:
  - claude-code
---

# Marketing Skills Division

42 skills de marketing prontas para produção, organizadas em 7 pods especialistas com uma camada de contexto base e orquestração.

## Início Rápido

### Claude Code
```
/read marketing-skill/marketing-ops/SKILL.md
```
O roteador direcionará você para a skill especialista correta.

## Arquitetura

```
marketing-skill/
├── marketing-context/     ← Base: voz da marca, audiência, objetivos
├── marketing-ops/         ← Roteador: direciona para a skill correta
│
├── Content Pod (8)        ← Estratégia → Produção → Edição → Social
├── SEO Pod (5)            ← SEO Tradicional + AI SEO + Schema + Arquitetura
├── CRO Pod (6)            ← Páginas, Formulários, Cadastro, Onboarding, Popups, Paywall
├── Channels Pod (5)       ← Email, Anúncios, Cold Email, Criativo, Social
├── Growth Pod (4)         ← Teste A/B, Referência, Ferramentas Gratuitas, Churn
├── Intelligence Pod (4)   ← Concorrentes, Psicologia, Analytics, Campanhas
└── Sales & GTM Pod (2)    ← Precificação, Estratégia de Lançamento
```

## Configuração Inicial

Execute `marketing-context` para criar seu arquivo `marketing-context.md`. Todas as outras skills leem isso para obter voz da marca, personas de audiência e panorama competitivo. Faça isso uma vez — melhora tudo.

## Visão Geral dos Pods

| Pod | Skills | Ferramentas Python | Principais Capacidades |
|-----|--------|--------------------|------------------------|
| **Foundation** | 2 | 2 | Captura de contexto da marca, roteamento de skills |
| **Content** | 8 | 5 | Estratégia → produção → edição → humanização |
| **SEO** | 5 | 2 | SEO Técnico, AI SEO (AEO/GEO), schema, arquitetura |
| **CRO** | 6 | 0 | Página, formulário, cadastro, integração, popup, otimização de paywall |
| **Channels** | 5 | 2 | Sequências de email, anúncios pagos, cold email, criativo |
| **Growth** | 4 | 2 | Teste A/B, programas de indicação, ferramentas gratuitas, prevenção de churn |
| **Intelligence** | 4 | 4 | Análise de concorrentes, psicologia de marketing, analytics, campanhas |
| **Sales & GTM** | 2 | 1 | Estratégia de precificação, planejamento de lançamento |
| **Standalone** | 4 | 9 | ASO, diretrizes de marca, estratégia PMM, engenharia de prompts |

## Ferramentas Python (27 scripts)

Todos os scripts usam somente stdlib (zero instalações via pip), são orientados a CLI com saída em JSON e incluem dados de exemplo para modo demo.

```bash
# Pontuação de conteúdo
python3 marketing-skill/content-production/scripts/content_scorer.py article.md

# Detecção de escrita por IA
python3 marketing-skill/content-humanizer/scripts/humanizer_scorer.py draft.md

# Análise de voz da marca
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py copy.txt

# Validação de copy de anúncio
python3 marketing-skill/ad-creative/scripts/ad_copy_validator.py ads.json

# Modelagem de cenários de precificação
python3 marketing-skill/pricing-strategy/scripts/pricing_modeler.py

# Geração de plano de rastreamento
python3 marketing-skill/analytics-tracking/scripts/tracking_plan_generator.py
```

## Funcionalidades Únicas

- **AI SEO (AEO/GEO/LLMO)** — Otimize para citações por IA, não apenas para ranqueamento
- **Content Humanizer** — Detecte e corrija padrões de escrita por IA com pontuação
- **Context Foundation** — Um arquivo de contexto de marca alimenta todas as 42 skills
- **Orchestration Router** — Roteamento inteligente por palavra-chave + pontuação de complexidade
- **Zero Dependencies** — Todas as ferramentas Python usam somente stdlib
