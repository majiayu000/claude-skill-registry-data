---
name: adversarial-review
description: >
  Review a diff as an independent adversary rather than a collaborator: spec
  compliance, boundary coherence between producer and consumer, then code
  quality. Use when reviewing someone else's change, auditing a PR, or checking
  work before it closes. Not for reviewing your own implementation.
---

# adversarial-review

Uma revisão vale pela **independência**, não pela extensão da lista.

## Antes de abrir o diff

- Você implementou esta unidade? Então recuse: diga que é o executor e peça outro revisor.
- Leia o **contrato** primeiro, o diff depois. A ordem inversa faz você revisar a solução
  em vez de revisar o pedido.
- Não leia a explicação do implementador antes do seu primeiro parecer. Ela ancora a
  leitura, e ancoragem é exatamente o que torna revisão de agente inútil.

## Estágio 1 — cumpre o contrato?

- Cada item de `acceptance` está atendido? Aponte onde.
- Saiu de `allowed_paths`? Encostou em `forbidden`? Isso é `FAIL`, não ressalva.
- Fez **a mais**? Escopo extra é achado, não bônus.

## Estágio 2 — fronteira (o estágio que build verde não faz)

Leia os **dois lados** de toda fronteira que o diff atravessa. Checklist e os casos que
este repo já embarcou em produção: `references/boundary-checklist.md`.

## Estágio 3 — qualidade

Bug, dead code, caminho triste sem tratamento, teste ausente, estilo Biome.

## Saída

- `arquivo:linha` + severidade. Achado duvidoso marcado como duvidoso.
- Veredito explícito: `PASS`, `PASS-COM-RESSALVA` ou `FAIL` com o que falta.
- Seu `PASS` **não** fecha a tarefa. Quem fecha é a prova de runtime.
