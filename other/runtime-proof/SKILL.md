---
name: runtime-proof
description: >
  Turn a contract's acceptance criteria into observed runtime behavior, and
  pick the command that actually proves each one. Use before closing a task,
  when asked whether something works, or when tempted to conclude from the code
  that it must work. Existence is not evidence.
---

# runtime-proof

> Existir não é evidência. Comportamento observado é evidência.

Arquivo criado, rota declarada, componente montado, policy escrita: nada disso prova
nada. A pergunta é sempre **"o que eu observei rodar?"**.

## Escolha do comando

Qual prova prova o quê — e o que cada uma **não** cobre: `references/proof-catalog.md`.

Regra curta:

| A propriedade é sobre… | Prova |
|---|---|
| lógica pura, contrato de módulo | `test:unit` |
| contrato do repositório (script, config, estrutura) | `test:scope` |
| quem pode ver o quê no banco | `test:db` (pgTAP, com positivo **e** negativo) |
| ciclo do usuário na tela | `test:e2e` |
| aparência, alvo de toque, contraste | `node scripts/visual/loop.mjs` |
| qualquer entrega | `gate` (necessário, nunca suficiente sozinho) |

## Antes de chamar vermelho de regressão

Confirme que a falha reproduz num estado limpo. As armadilhas conhecidas (perfil fantasma
"Visual Capture", `dev-server.pid` velho, Docker parado) estão na skill `gate-before-done`.

## Os dois `db:reset` são deliberados

pgTAP roda contra banco **sem** seed (`db:reset --no-seed`); E2E precisa do oposto, porque
autentica como usuário semeado. Colapsar os dois em um só deixa seis asserts de perfil
vermelhos. Se você mexeu em migration, o seed do E2E foi embora: rode o reset **com** seed
(sequência em `supabase/AGENTS.md`) e só então o E2E. Spec que não rodou não fecha nada.

## Veredito

Um destes, sempre com o comando e a saída:

- `PASS` — cada item de `acceptance` tem uma observação que o sustenta.
- `FAIL` — com a classificação: meu diff / pré-existente / armadilha conhecida.
- `BLOCKED` — o ambiente impede a prova. Diga o que falta e o que **foi** provado.
  `BLOCKED` não é `PASS`, e não fecha tarefa.
