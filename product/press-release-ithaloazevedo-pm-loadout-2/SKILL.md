---
name: press-release
description: Use when a new feature, product, or initiative needs its value proposition stress-tested before entering Delivery. Forces the PM to write a press release and FAQ as if the product is already launched — the Amazon Working Backwards method. If you can't write a clear press release, the problem isn't clear enough to build.
---

# Working Backwards

## Overview

Working Backwards é o método Amazon de clarificar valor antes de construir. Em vez de começar pela solução (o que vamos fazer), você começa pelo resultado (o que o usuário vai ler no dia do lançamento).

Se você não consegue escrever um press release claro, a proposta de valor não está clara o suficiente para entrar em Delivery.

Use antes de promover um Discovery para Delivery, antes de uma spec de alto impacto, ou quando a equipe não consegue articular o valor da feature em uma frase.

## Postura

Esta skill não é um exercício criativo — é um teste de clareza. O press release forçará inconsistências entre o que a equipe acredita que está construindo e o que o usuário vai receber.

Se o press release soar vago, corporativo ou cheio de jargão técnico: a proposta de valor ainda não está clara. Reescreva até soar como algo que um jornalista cobriria ou um usuário compartilharia.

## Fluxo

### 1. Contexto (se ainda não tiver)

Antes de escrever, verifique:
- Quem é o usuário-alvo? (persona, perfil, segmento)
- Qual o problema central que a feature/produto resolve?
- Há pesquisa ou evidência de usuário disponível?
- Qual o contexto do produto? (B2C, B2B, plataforma de apostas, loteria, etc.)

Se o contexto for insuficiente, faça no máximo uma pergunta antes de prosseguir com suposições declaradas.

### 2. Press Release

Redija o press release no seguinte formato. Escreva como se o produto já estivesse lançado hoje:

```
HEADLINE
[O que o produto/feature faz em uma frase. Para quem. Qual o benefício central.]

SUBTÍTULO
[O problema que estava existindo antes e como isso muda.]

CONTEXTO DO MERCADO
[Por que isso importa agora. O que estava acontecendo no mercado/comportamento do usuário que tornou isso necessário.]

O QUE É
[Descrição em linguagem simples do que o usuário pode fazer agora que não conseguia antes. Sem jargão técnico.]

CITAÇÃO — VOZ DA EMPRESA
[O que o líder do produto diria sobre por que isso foi construído. Tom: convicção, não marketing.]

CITAÇÃO — VOZ DO USUÁRIO
[O que um usuário real diria sobre como isso mudou sua experiência. Tom: autêntico, específico.]

COMO COMEÇAR
[O próximo passo para o usuário. Simples e direto.]
```

### 3. FAQ

Após o press release, escreva o FAQ respondendo as perguntas que um jornalista cético ou um usuário novo faria:

- **"Mas isso não é igual a [alternativa X]?"** — qual a diferença real?
- **"E se [edge case óbvio]?"** — como o produto lida?
- **"Por que agora?"** — qual o timing e por que faz sentido neste momento?
- **"Como fica minha [privacidade / dinheiro / dado]?"** — especialmente relevante para contexto de apostas
- **"O que acontece se [falha / problema técnico]?"** — qual o plano de contingência?
- **"Posso confiar nisso?"** — como a empresa demonstra confiabilidade?

Adicione perguntas específicas do domínio (apostas, loteria, regulação) quando relevante.

### 4. Passe Crítico

Após redigir, avalie o press release com estas perguntas:

| Pergunta | Sinal verde | Sinal vermelho |
|---|---|---|
| Um usuário entenderia em 30 segundos? | Sim, sem glossário | Precisa de contexto técnico |
| A headline tem um benefício concreto? | "Saque em 2 minutos" | "Nova experiência integrada" |
| A citação do usuário soa real? | Específica, com emoção | Genérica, corporativa |
| O problema descrito dói de verdade? | Reconhecível, frequente | Vago, hipotético |
| Alguém compartilharia isso? | Sim | Não / talvez |

Se 2 ou mais sinais vermelhos: o problema não está claro o suficiente. Volte para discovery.

### 5. Extração para Spec

Se o press release passou no passe crítico, extraia:

```markdown
**Usuário-alvo**: [quem]
**Problema central**: [dor em uma frase]
**Proposta de valor**: [benefício em uma frase]
**Success signal**: [como saberemos que funcionou — o que o usuário faz diferente]
**Suposição mais crítica**: [o que precisa ser verdade para o press release fazer sentido]
```

Estes elementos alimentam diretamente o `clickup-spec` ou o `redator`.

## Integração

| Depois do Working Backwards... | Use |
|---|---|
| A proposta de valor não está clara | `explorador` + `mapa-necessidades` para mais discovery |
| A suposição mais crítica é de alto risco | `suposicoes` para desenhar o teste |
| Está pronto para especificar | `clickup-spec` → `agente-spec` → `agente-delivery` |
| Quer validar o press release com a banca | `/banca` com o texto do press release como input |

## Guardrails

- Não aceite press releases vagos. "Melhor experiência" não é benefício — é promessa sem substância.
- Se o usuário resistir ao exercício ("já sei o que é, vamos para a spec"), insista: a resistência é o sinal de que o exercício é necessário.
- Para contexto de apostas e loteria: o FAQ deve cobrir privacidade, segurança financeira e conformidade regulatória — o usuário apostador é sensível a esses pontos.
- Não deixe o press release virar documento de marketing. É um teste de clareza, não um anúncio.
- Prefira português no output, salvo o nome do método.
