---
name: radar-ia-br
description: Busca e resume as últimas notícias de IA em português a partir de fontes selecionadas. Remove duplicatas e categoriza os tópicos.
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: []
      env: []
---

# Radar Notícias IA BR

## Objetivo

Busca e resume as principais notícias recentes de Inteligência Artificial a partir de fontes curadas.

A skill:
- busca notícias recentes
- remove duplicatas
- categoriza os tópicos
- traduz/resume em português
- retorna:
  - título
  - link
  - categoria
  - resumo curto

## Uso

Invoke com:
- `/radar-ia-br`
- "últimas notícias de IA"
- "resumo IA"
- "o que aconteceu em IA hoje"
- "AI briefing"

Opcionalmente o usuário pode informar quantidade:
- "me mostre 5 notícias de IA"
- "top 10 notícias de IA"

## Fontes preferenciais

Use estas fontes:

### Fontes primárias
- Anthropic News — Company announcements
- Claude Blog — Product updates and guides
- Google AI — Gemini/DeepMind

### Fontes de curadoria
- TLDR AI — Daily AI industry digest
- The Decoder — AI-focused site
- Last Week in AI — Weekly roundup

## Instruções

### Determinar quantidade

Se o usuário informar quantidade:
- usar quantidade solicitada

Caso contrário:
- usar 10 notícias por padrão

Máximo:
- 20 notícias

## Critérios de seleção

Priorize notícias:

1. Recentes (,ax 72 horas)
2. Relevantes para IA generativa, modelos, produtos, pesquisa, agentes, ferramentas ou mercado
3. Publicadas ou destacadas nas fontes 
4. Com impacto potencial para profissionais, criadores, desenvolvedores ou empresas

## Remoção de duplicadas

Se a mesma notícia aparecer em mais de uma fonte:

- mantenha apenas uma entrada
- escolha como link principal a fonte mais original ou mais direta
- mencione fontes adicionais no campo “Também apareceu em”
- não repita a notícia na lista

## Categorias possíveis

Classifique cada notícia em uma destas categorias:

- Lançamento (launch, release, announce, GPT, Claude, Gemini, model)
- Pesquisa (paper, benchmark, study, research)
- Ferramenta para desenvolvedores
- Produto (feature, API, update, tool)
- Mercado (funding, startup, acquisition)
- Segurança em IA (safety, alignment, red team)
- Opinião (opinion, future, prediction)
- Outros

## Formato de saída

Retorne a lista em português no seguinte formato:

```markdown
# Últimas notícias de IA

## 1. [Título da notícia](link)

**Categoria:** Lançamento de produto  
**Fonte principal:** Nome da fonte  
**Também apareceu em:** Fonte 2, Fonte 3  
**Data:** DD/MM/AAAA, se disponível

Resumo em um parágrafo curto explicando o que aconteceu, por que importa e qual é o impacto potencial. Não escreva mais de 4 linhas.

## 2. [Título da notícia](link)

**Categoria:** Pesquisa  
**Fonte principal:** Nome da fonte  
**Também apareceu em:** —  
**Data:** DD/MM/AAAA, se disponível

Resumo em um parágrafo curto explicando o que aconteceu, por que importa e qual é o impacto potencial.
```

# Tratamento de erros

Se algum feed falhar:

continuar normalmente
ignorar feed indisponível

Nunca interromper o briefing completo por falha parcial.

# Regras importantes

Sempre responder em português brasileiro
Nunca copiar texto integral do artigo
Sempre resumir
Sempre incluir link original
Não inventar informações
Não repetir notícias duplicadas
Priorizar clareza
Priorizar fontes originais quando possível