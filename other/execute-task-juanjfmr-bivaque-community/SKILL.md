---
name: execute-task
description: >
  Execute one task contract from docs/agents/tasks/ (or an inline equivalent)
  end to end. Use when starting implementation work in this repository: it
  fixes the order — measure baseline, implement inside the boundary, prove in
  the same unit, hand off to an independent reviewer. Triggers on "implementar",
  "executar contrato", "corrigir X", "rodar a task".
---

# execute-task

A unidade de execução deste repositório é o **contrato**, não o agente.
Sem contrato, você não sabe o que é "pronto" — e é assim que escopo cresce sozinho.

## 1. Tenha um contrato

Existe um em `docs/agents/tasks/<ID>.task.yml`? Valide:

```sh
node scripts/agents/task-contract.mjs
```

Não existe? Escreva um a partir de `docs/agents/tasks/TEMPLATE.task.yml` **antes** de
codar, e valide. Contrato inválido não vai para execução — o validador diz o que falta.
Campos e semântica: `docs/agents/TASK_CONTRACT.md`.

## 2. Meça o baseline

Reproduza o estado que o contrato declara em `baseline`. Duas saídas possíveis:

- reproduz → siga.
- **não reproduz** → o contrato está errado. Pare e diga. Plano errado é informação,
  não obstáculo.

## 3. Implemente dentro da cerca

- Só dentro de `allowed_paths`. Precisou sair? Pare e reporte — não amplie sozinho.
- `forbidden` vale mesmo quando parece a correção certa.
- Mínimo que satisfaz `acceptance`. Nada especulativo.
- Implementação e prova são **um todo só**. Nunca entregue código sem a prova na mesma unidade.
- Via de permissão: teste positivo **e** negativo.
- Migration aplicada não se edita; coluna de escopo e policy na mesma migration (Padrão 6).

## 4. Prove

Rode o que está em `proof`. Detalhe de qual comando prova o quê: skill `runtime-proof`.
Antes de declarar pronto: skill `gate-before-done`.

## 5. Entregue para revisão independente

Você **não** revisa o que implementou. Entregue:

- o diff,
- a saída **lida** do gate,
- o que ficou fora e por quê.

Não explique sua solução ao revisor antes do primeiro parecer dele: explicação ancora,
e revisor ancorado não é revisor.

## Orçamento

`retry_budget` (padrão 3) conta tentativas de reparo do **mesmo** item. Esgotou:
devolva `FAIL`, `BLOCKED` ou `HUMAN_DECISION`. Nunca `PASS`.
