---
name: experiment-protocol
description: >
  Run a comparison between several candidate solutions honestly: freeze the
  contract, fan out isolated producers, judge blind, and end in a human
  decision. Use for EXP tasks, for A/B of two approaches, and when measuring
  whether a skill or prompt change actually improved anything.
---

# experiment-protocol

Experimento existe para **produzir diferença observável**, não consenso.
Se os candidatos conversam, você mediu convergência, não qualidade.

## 1. Congele o contrato antes de produzir

Escreva, antes de qualquer candidato: o que é fixo (tokens, escopo, restrições), o que é
livre, e os **eliminatórios** — critérios que reprovam sozinhos, decididos de antemão.
Critério inventado depois de ver o resultado não é critério, é justificativa.

## 2. Fan-out isolado

- Cada produtor trabalha **sozinho**, sem ver os outros candidatos e sem conversar com eles.
- Mesmo contrato, mesmo baseline, mesma fronteira de arquivos para todos.
- Nenhum produtor sabe quantos candidatos existem nem quem produz os outros.

Este é o ponto em que a maioria dos harnesses erra: colaboração entre produtores gera
**erro correlacionado**, e erro correlacionado desaparece na comparação.

## 3. Julgamento cego

- Candidatos chegam ao juiz como `A`, `B`, `C` — sem autor, sem modelo, sem ordem de produção.
- O juiz é read-only e **não** produziu candidato nenhum.
- Ordem: eliminatórios → medida objetiva → ofício (argumentado, e marcado como argumento).
- Nenhum candidato passa os eliminatórios? O resultado é `NENHUM`, não o menos ruim.

## 4. Decisão

O juiz entrega ranking, distância entre candidatos e **a pergunta que sobra**. Quem escolhe
é o coordenador, sob o mandato do dono de 02/11/2026: registra a escolha, o motivo e a pergunta
que sobrou no card, e o dono vê o resultado no marco seguinte. O juiz nunca escolhe — juiz que
escolhe virou implementação disfarçada de método.

## Caso especial: medir uma skill

Uma skill nova é uma hipótese, não uma melhoria. Meça antes de adotar:

- mesma tarefa, N repetições, **com** e **sem** a skill;
- asserções decididas antes: defeito real encontrado, falso positivo, item de aceitação coberto;
- custo também é resultado: tokens e tempo entram na comparação.

A skill entra em definitivo se justificar o próprio custo. Se não justificar, ela sai —
instrução que não evita erro real só ocupa contexto.
