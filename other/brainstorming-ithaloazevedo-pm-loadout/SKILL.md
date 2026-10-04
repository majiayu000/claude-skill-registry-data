---
name: brainstorming
description: Use when a PM/product idea, opportunity, problem, solution, feature, experiment, or strategy is still vague and needs collaborative exploration before prioritization, discovery, or Linear specification.
---

# Brainstorming

## Overview

Use brainstorming to turn a vague product thought into a clearer problem frame, opportunity, option set, or decision path. In PM Loadout, brainstorming is conversational by default and must not write files, create Linear artifacts, or commit docs unless the user explicitly asks.

## Core Rule

Do not rush from idea to specification. Clarify enough to choose the next useful PM move.

Ask at most one blocking question at a time. If enough context exists, state assumptions and continue.

## Flow

1. Name the current shape of the idea: problem, user need, solution, bet, metric, launch, or unclear.
2. Separate facts, assumptions, guesses, and open questions.
3. Ask one high-leverage question if blocked.
4. Offer 2-3 possible frames or directions.
5. Recommend the next step and explain the trade-off.
6. Hand off to the next skill only when the user has a clearer goal.

## Common Hand-offs

| If the output is... | Hand off to |
|---|---|
| user/problem hypothesis | `entrevista-usuario`, `jtbd`, `mapa-necessidades` |
| opportunity space | `ost`, `suposicoes` |
| multiple options | `ice`, `advogado-do-diabo`, `gist` |
| strategic uncertainty | `cynefin`, `wardley` |
| ready product artifact | `clickup-spec` |
| quality/readiness question | `checar-servico`, `checar-usabilidade`, `nivel-lancamento` |
| success measurement | `metricas` |

## Output Shape

Prefer this concise shape:

```markdown
**Frame atual**
[what this appears to be]

**O que sabemos**
[facts/evidence]

**Suposicoes**
[assumptions]

**Opcoes**
[2-3 directions]

**Recomendacao**
[best next move]

**Proxima pergunta ou acao**
[one item]
```

## Guardrails

- Do not create a Linear initiative just because an idea sounds promising.
- Do not run prioritization before the options and evidence are clear enough.
- Do not treat internal stakeholder belief as validated user evidence.
- Do not force a full design document; produce one only when the user asks for a durable artifact.
- Do not invoke implementation planning unless the user explicitly wants delivery planning.

## Visual Companion

If a diagram would help, offer a visual companion before using it. This is optional and useful for opportunity trees, flows, maps, and option comparisons.

Read `visual-companion.md` only when the user accepts using a local browser visual.
