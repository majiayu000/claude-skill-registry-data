---
name: placar
description: Placar dos operarios do orquestrador - o que esta sessao despachou e ainda nao registrou, quem acerta de primeira por modelo e onde foi o token. Comando do usuario.
argument-hint: "[janela, ex.: 12h ou 7d]"
disable-model-invocation: true
---

# Placar dos operarios

Janela pedida: `$ARGUMENTS`. So vale um numero seguido de `h` ou `d` (ex.: `12h`, `7d`); vazia ou em outro formato, use `7d` e nao repasse o texto recebido pra nenhum comando.

Rode os 4 comandos abaixo na MESMA mensagem, com o Python 3 desta maquina (`python`; se nao existir, `python3` ou `py -3`). Nao rode mais nada e nao edite nada.

1. `python "${CLAUDE_SKILL_DIR}/../orquestrador/operarios.py" retomar` (o que esta sessao despachou; saida 10 = nenhum operario nesta sessao)
2. `python "${CLAUDE_SKILL_DIR}/../orquestrador/operarios.py" resumo --todas --desde <janela>`
3. `python "${CLAUDE_SKILL_DIR}/../orquestrador/operarios.py" ficha`
4. `python "${CLAUDE_SKILL_DIR}/../orquestrador/custo.py"` (se disser "sem sessao", ignore)

Responda ao usuario em ate 12 linhas, em linguagem simples, nesta ordem:

- Nesta sessao: quantos operarios foram despachados, quantos estao sem registro e quais (pela descricao).
- Na janela: a linha `operarios: ...` do resumo, copiada.
- Por modelo: quem acerta de primeira e em que tipo de tarefa (2 ou 3 linhas tiradas da ficha), e os experimentos em aberto.
- Token: a fatia do chefe, dos operarios e do modelo mais caro, com o aviso de que o valor e estimativa a preco de tabela.
- Uma linha final: o que esta pronto, o que falta registrar e o que depende do usuario.

Numero so o que os comandos devolveram. Comando que falhar: diga qual falhou e a mensagem, sem tentar consertar.
