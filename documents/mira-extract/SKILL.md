---
name: mira-extract
description: >-
  Extrator de contexto do Mira: lê uma fonte vinculada no mira.config.json (pasta de projeto, PDF, LaTeX ou texto) e produz um briefing estruturado para o /mira-planner. Use SEMPRE que o usuário pedir para criar slides "sobre" um projeto ou documento, mencionar uma fonte vinculada pelo nome, ou disser "extrai o conteúdo de", "lê o projeto", "prepara o material do", "briefing do projeto".
---

# Skill: Extrator de Contexto (Mira)

## Objetivo

Transformar uma fonte bruta (projeto de código, PDF, capítulo LaTeX, texto) em um `briefing.md` estruturado para o `/mira-planner`. É o que permite ao Mira morar numa pasta isolada e ainda apresentar qualquer projeto.

## Regra de ouro

**Leia das fontes, escreva apenas em `decks/`.** Nunca crie, edite ou apague arquivos dentro da pasta de uma fonte vinculada.

## Fluxo de Execução

### Passo 1: Resolver a fonte

1. Leia `mira.config.json` na raiz da instalação.
2. Se o usuário citou a fonte pelo nome ("slides sobre o reversa"), localize-a em `sources[]`.
3. Se não há fonte correspondente, pergunte se deve vincular (`npx mira link <caminho>`) ou aceite um caminho direto.
4. Verifique se o caminho existe. Se não, avise e pare.

### Passo 2: Extrair conforme o tipo

**type: projeto (pasta de código)**
- Leia README.md, docs/, package.json (ou equivalente) para entender propósito e arquitetura.
- Mapeie a estrutura de pastas (2 níveis) e identifique os módulos principais.
- Liste comandos/CLI, agentes, features — o que o projeto FAZ.
- Capture 2-3 trechos de código emblemáticos (curtos) que merecem slide.

**type: pdf**
- Extraia o texto (use a skill /pdf se necessário).
- Identifique título, seções, conceitos-chave, dados numéricos e figuras descritas.

**type: latex**
- Leia o .tex, ignore preâmbulo, mapeie \chapter/\section, extraia conceitos, código e tabelas.

**type: texto**
- Leia diretamente e estruture por temas.

### Passo 3: Gerar o briefing

Escreva `decks/<nome-do-deck>/briefing.md` com:

```markdown
# Briefing: [nome]
**Fonte:** [name] ([type]) — [path]
**Data da extração:** [data]

## Essência em uma frase
[o que é, para quem, por quê]

## Conceitos-chave (candidatos a slide)
1. [conceito] — [por que importa] — [sugestão visual: d3-fluxo|comparacao|metricas|timeline|codigo]
2. ...

## Dados e números
[métricas, versões, benchmarks — material para card_metricas]

## Trechos de código emblemáticos
[se houver]

## Narrativa sugerida
[arco: problema → solução → como funciona → resultados → CTA]

## Lacunas
[o que não foi encontrado na fonte e talvez o usuário precise fornecer]
```

### Passo 4: Encadear

Apresente um resumo do briefing ao usuário e pergunte se pode acionar o `/mira-planner` com esse material.
