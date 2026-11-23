---
name: handoff
description: Como um especialista documenta a entrega para o revisor e o próximo agente.
---

# Skill: handoff

Todo especialista termina com um handoff. É o que permite o revisor (e o próximo agente) trabalhar sem ler o histórico.

Use `work/_templates/handoff.md` e salve em `work/<ciclo>/handoffs/<seu-agente>-<artefato>.md`.

## Conteúdo obrigatório
1. **O que foi feito**: 3 a 6 linhas.
2. **Onde está**: caminhos exatos dos arquivos criados/alterados.
3. **Decisões e motivos**: o que escolheu e o que descartou.
4. **Suposições**: tudo que assumiu sem confirmação.
5. **Riscos e pendências**: o que pode dar errado, o que ficou de fora.
6. **Como verificar**: comandos ou passos para o revisor conferir.

## Regras
- Sem "tudo certo": diga o que foi de fato verificado e como.
- Se algo não foi testado, escreva "não testado".
